
# FireSpark -- the Data Work
# Copyright 2020 The FireSpark Author. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""FireSpark Apache Spark dataset utility library """

import os
import cv2
import numpy as np
import ntpath
import itertools
import tqdm

from pyspark.sql import SparkSession
from petastorm.etl.dataset_metadata import materialize_dataset
from petastorm.unischema import dict_to_spark_row
from petastorm.spark_utils import dataset_as_rdd

from . data import schemas
from . protos.mas import image_data_pb2 as im_proto
from .aws_utils import FireSparkAWS as s3


class SparkDataset(object):
	""" Mas FireSpark data processing class  """	
	def __init__(self, **job):
		self.jc = {
			'dataset' : "",
			'source_url' : "",
			'storage_url' : "",
			'workspace' : "/tmp/mas/",
			'n_records' : 1000,
			'core' : 2,
			'schema' : schemas.MasSchema,
			's3profile' : "magna_data",
			'label_fn' : None}
		self.jc.update(job)
		self.spark = SparkSession \
			.builder.config('spark.driver.memory', '2g') \
			.master('local[%d]'%self.jc['core']) \
			.getOrCreate()
		self._proto_work = os.path.join(self.jc['workspace'],
										self.jc['dataset'],
										'proto')
		if not os.path.exists(self._proto_work):
			os.makedirs(self._proto_work)
		self._parquet_work = os.path.join(self.jc['workspace'],
										self.jc['dataset'],
										'parquet')
		if not os.path.exists(self._parquet_work):
			os.makedirs(self._parquet_work)
		self.prepare_label_fn = self.jc['label_fn']
		self.aws = s3(self.jc['s3profile'])
		self._bucket_name = None
		self._bucket_dst = None
		self._s3_key = None
		self._record_list = []
		if self.aws.S3_BUCKET_BASE in self.jc['source_url']:
			self._bucket_name, folder = self.aws.url_to_bnk(
										self.jc['source_url'])
			self._record_list = self.aws.get_s3_keys(
										self._bucket_name,
										folder, ".proto",
										full_key=True)
		else:
			self._record_list = self._record_provider()
		if self.aws.S3_BUCKET_BASE in self.jc['storage_url']:
			self._bucket_dst, self._s3_key = self.aws.url_to_bnk(
											 self.jc['storage_url'])
		else:
			if self.jc['storage_url']:
				if not os.path.exists(self.jc['storage_url']):
					os.makedirs(self.jc['storage_url'])
	
	def _record_provider(self):
		""" provide proto records from source directory	"""
		if not os.path.isdir(self.jc['source_url']): return
		records = []
		for r, _, f in os.walk(self.jc['source_url']):
			local_files = [os.path.join(r, file) for file in f \
						   if '.proto' in file]
			records.extend(local_files)
		for r in records:
			yield r
	
	def _parse_one_proto(self, proto_file):
		""" parse one proto record

			Args:
			proto_file: protobuf record filename or url

			Return:
			protobuf message
		"""
		if self.aws.S3_BUCKET_BASE in proto_file:
			bucket_name, s3_key = self.aws.url_to_bnk(proto_file, False)
			proto_file = os.path.join(self._proto_work, ntpath.basename(s3_key))
			self.aws.download_file(bucket_name, s3_key, proto_file)
		with open(proto_file, "rb") as f:
			proto_message = im_proto.ImageBatchProto().FromString(f.read())
		
		return proto_message
	
	@staticmethod
	def prepare_label(annotation):
		label = []
		for obj in annotation.objects:
			label.append((obj.oclass, obj.cbox.x, obj.cbox.y, obj.cbox.w, obj.cbox.h))
		return np.array(label)

	def _row_generator(self, pd):
		""" generate information from an image proto

			Args:
			pd: image proto message

			Return:
			dictionary of image data and annotation
		"""
		if self.aws.S3_BUCKET_BASE in pd.image_data.image.url:
			bucket, image_key = self.aws.url_to_bnk(pd.image_data.image.url, False)
			im_obj = self.aws.client.get_object(Bucket=bucket, Key=image_key)
			im_data = im_obj["Body"].read()
			im_array = np.fromstring(im_data, np.uint8)
			im = cv2.imdecode(im_array, cv2.IMREAD_COLOR)
		else:
			im = cv2.imread(pd.image_data.image.url)		
		if self.prepare_label_fn:
			label = self.prepare_label_fn(pd.image_data.annotation)
		else:
			label = self.prepare_label(pd.image_data.annotation)

		return {'cam': pd.device.camera_id,
			'width': pd.image_data.image.width,
			'height': pd.image_data.image.height,
			'depth': pd.image_data.image.depth,
			'format': pd.image_data.image.format,
			'url': pd.image_data.image.url,
			'imdata': im,
			'label': label}
	
	def produce_dataset(self):
		""" convert source proto records into parquet files"""

		rowgroup_size_mb = 256
		parquet_url = "file://"+self._parquet_work
		progress_bar = "-"
		
		### petastorm dataset processing
		tot_proc = 0
		for proto_rec in self._record_list:
			proto = self._parse_one_proto(proto_rec)
			raw_proto_list = proto.proto_batch

			print("///: processing {} records from {} ...".format(len(raw_proto_list),
																  proto_rec))
			with materialize_dataset(self.spark, parquet_url, self.jc['schema'], rowgroup_size_mb):        
				idx_sample_list = map(lambda pd: self._row_generator(pd), raw_proto_list)
				sql_row = map(lambda x: dict_to_spark_row(self.jc['schema'], x), idx_sample_list)
				self.spark.createDataFrame(sql_row, self.jc['schema'].as_spark_schema()) \
					.coalesce(5).write.mode('append').parquet(parquet_url)
			tot_proc += len(raw_proto_list)
			progress_bar += progress_bar
			print(progress_bar)
		print("///: totally added {} examples to parquet dataset!".format(tot_proc))
		
		parquet_records = [f for f in os.listdir(self._parquet_work)]
		if self._bucket_dst:
			print("///: sync to bucket ...")
			for parquet in tqdm.tqdm(parquet_records):
				local_key = os.path.join(self._parquet_work, parquet)
				target_key = os.path.join(self._s3_key, parquet)
				self.aws.upload_file(self._bucket_dst, local_key, target_key)
			os.remove(local_key)
		else:
			print("///: sync to destination ...")
			if self.jc['storage_url']:
				for parquet in tqdm.tqdm(parquet_records):
					os.rename(os.path.join(self._parquet_work, parquet),
							  os.path.join(self.jc['storage_url'], parquet))
	
	def query_dataset(self, sql=''):
		""" conduct query over parquet dataset """

		### session
		spark = SparkSession.builder.master('local[1]').getOrCreate()
		
		### exam rdd
		rdd = dataset_as_rdd(self.jc['storage_url'], spark, 
		                     [self.jc['schema'].cam, self.jc['schema'].url]
							 )
		print('An id in the dataset: ', rdd.first().cam)

		### exam dataframe
		dataframe = spark.read.parquet(self.jc['storage_url'])
		dataframe.printSchema()
		print("///: Totally {} proto examples loaded!".format(dataframe.count()))
		dataframe.select('url').show()

		### query
		number_of_rows = spark.sql(
			'SELECT count(url) '
			'from parquet.`{}` '.format(self.jc['storage_url'])).collect()
		print('Number of rows in the dataset: {}'.format(number_of_rows[0][0]))
