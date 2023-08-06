
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
"""FireSpark Protobuf utility library """

import os
import copy
import pprint
import ntpath
import random
import cv2
import numpy as np
import tqdm
import json

from google.protobuf.descriptor import FieldDescriptor as FD
from . protos.mas import image_data_pb2 as im_proto
from . protos.mas import annotation_pb2 as annotation_proto
from .aws_utils import FireSparkAWS as s3


class ProtoTemplate(object):
	""" MasProto interface template class    """
	def __init__(self, format="mas"):
		self._template = {}
		self._format = format
		self._update_template()		

	def _proto_dict(self, pro):
		""" Read the fields in a ProtoTemplate object and recursively
		    convert the ProtoTemplate into a dictionary.

		    Args:
		    pro: a ProtoTemplate object

		    Returns:
		    A dictionary containing all the nested fields in a ProtoTemplate
		"""
		tmpdict = {}
		if not pro.IsInitialized():
			return None
		for field in pro.DESCRIPTOR.fields:
			if not field.label == FD.LABEL_REPEATED:
				if not field.type == FD.TYPE_MESSAGE:
					tmpdict[field.name] = getattr(pro, field.name)
				else:
					value = self._proto_dict(getattr(pro, field.name))
					if value:
						tmpdict[field.name] = value
			else:
				if field.type == FD.TYPE_MESSAGE:
					tmpdict[field.name] = \
						[self._proto_dict(v) for v in getattr(pro, field.name)]
				else:
					tmpdict[field.name] = [v for v in getattr(pro, field.name)]
		return tmpdict
	
	def _update_template(self):
		if self._format == "mas":
			img_data = im_proto.ImageDataProto()
			self._template = self._proto_dict(img_data)

	def get_template(self):
		''' Return a deep copy of the proto info'''
		return copy.deepcopy(self._template)

	def get_proto_info(self):
		''' Display proto info'''
		print("============ MAS Proto Template ===========")
		pprint.pprint(self._template)


class ProtoDataset(object):
	""" MAS proto dataset class """
	def __init__(self, **job):
		job_config = {
			'dataset' : "",
			'data_source' : "../tests/data/",
			'data_storage' : "",
			'data_workspace' : "/tmp/mas/",
			'num_records' : 1000,
			'proto_batch_size' : 500,
			'proto_format' : "mas",
			's3profile' : "magna_data"}
		job_config.update(job)
		self._dataset_name = job_config['dataset']
		self._pt = ProtoTemplate(job_config['proto_format'])
		self._batch_size = job_config['proto_batch_size']
		self._record_list = []
		self._n_records = job_config['num_records']
		self._datasrc = job_config['data_source']
		self._datadst = job_config['data_storage'] if job_config['data_storage'] \
						else job_config['data_workspace']
		self._workspace = job_config['data_workspace'] + job_config['dataset']
		if not os.path.exists(self._workspace):
			os.makedirs(self._workspace)
		self.aws = s3(profile=job_config['s3profile'])
		self._bucket_name = None
		self._bucket_dst = None
		self._s3_key = None
		if self.aws.S3_BUCKET_BASE in self._datasrc:			
			self._bucket_name, folder = self.aws.url_to_bnk(self._datasrc)
			self._record_list = self.aws.get_s3_keys(self._bucket_name, folder)
		else:
			self._record_list = self._record_provider()
		if self.aws.S3_BUCKET_BASE in self._datadst:
			self._bucket_dst, self._s3_key = self.aws.url_to_bnk(self._datadst)
		else:
			if not os.path.exists(self._datadst):
				os.makedirs(self._datadst)
		self._num_to_batch = -1
		self._batch_id = 0
		self._pb = None
		self._reset_proto_container()

	def _record_provider(self):
		""" provide raw record files from the source dataset directory """
		if not os.path.isdir(self._datasrc): return
		records = []
		for r, _, f in os.walk(self._datasrc):
			local_files = [os.path.join(r, file) for file in f]
			records.extend(local_files)
		for r in records:
			yield r
	
	def _reset_proto_container(self):
		""" initialize a new batch for proto message packing"""
		self._num_to_batch = 0
		self._pb = im_proto.ImageBatchProto()

	@staticmethod
	def get_data_from_keys(client, bucket, record):
		""" Method for obtaining image and annotation data from a record from s3 bucket.
		    For child classes implemented for different raw datasets, this method shall 
                    be overridden.

		    Returns: a tuple of (url, image array, annotation list)
		"""
		image_key, annot_key = record
		an_obj = client.get_object(Bucket=bucket, Key=annot_key)
		an_data = an_obj["Body"].read().decode('utf-8')
		if ".txt" in annot_key:
			an = an_data.splitlines()
		elif ".json" in annot_key:
			an = json.loads(an_data)
		else:
			an = None
		im_obj = client.get_object(Bucket=bucket, Key=image_key)
		im_data = im_obj["Body"].read()
		im_array = np.fromstring(im_data, np.uint8)
		im = cv2.imdecode(im_array, cv2.IMREAD_COLOR)
		image_file = os.path.join("s3://", bucket, image_key)
		return (image_file, im, an)

	@staticmethod
	def get_data_from_files(record):
		""" Method for obtaining image and annotation data from a local record.
		    For child classes implemented for different raw datasets, this method
                    shall be overridden.

		    Returns: a tuple of (url, image array, annotation list)
		"""
		image_file, annot_file = record
		with open(str(annot_file), 'r') as f:
			if ".txt" in annot_file:
				an = f.readlines()
			elif ".json" in annot_file:
				an = json.load(f)
			else:
				an = None
		im = cv2.imread(image_file)
		return (image_file, im, an)
	
	def _example_record(self, f):
		""" Method for providing one downtown dataset example record
		    For child classes implemented for different raw datasets,
		    this method shall be overridden.

		    Returns: image and annotation file tuple
		"""
		if '.txt' in f:
			return (f[:-3]+"jpg", f)
		else:
			return None
	
	def _add_to_proto(self, record):
		""" Method for processing one downtown dataset example to proto message
		    For child classes implemented for different raw datasets, this method
                    shall be overridden.

		    Args:
		    record: a tuple of (url, image_array, annotation_string)

		    Returns:
		    new protobuf message for dataset example
		"""
		imh, imw, imc = record[1].shape
		obstacles = []
		for line in record[2]:
			a = line.rstrip().split(" ")
			obstacles.append({"class": int(a[0]),
				"bbx": (float(a[1]), float(a[2]), float(a[3]), float(a[4]))})
		if not obstacles: return None
		pd = im_proto.ImageDataProto()
		pd.device.camera_id = 'UNKNOWN'
		pd.image_data.image.width = imw
		pd.image_data.image.height = imh
		pd.image_data.image.depth = imc
		pd.image_data.image.format = 1
		pd.image_data.image.url = record[0]
		for obj in obstacles:
			obj_proto = annotation_proto.ObjectProto()
			obj_proto.oclass = obj['class']
			obj_proto.cbox.x = obj['bbx'][0]
			obj_proto.cbox.y = obj['bbx'][1]
			obj_proto.cbox.w = obj['bbx'][2]
			obj_proto.cbox.h = obj['bbx'][3]
			pd.image_data.annotation.objects.append(obj_proto)
		return pd
	
	def _proto_file(self):
		""" get the filename of a proto batch """
		return "{}_batch_{}.proto".format(self._dataset_name, self._batch_id)
	
	def _gen_proto_record(self):
		""" write a batch of proto messages to a .proto file """
		self._batch_id += 1
		self._pb.batch_id = self._batch_id
		self._pb.num_protos = self._num_to_batch				
		proto_key = self._proto_file()
		proto_file = os.path.join(self._workspace, proto_key)
		with open(proto_file, "wb") as f:
			bytesAsString = self._pb.SerializeToString()
			f.write(bytesAsString)
		
		if self._bucket_dst:
			target_key = os.path.join(self._s3_key, proto_key)
			self.aws.upload_file(self._bucket_dst, proto_file, target_key)
			os.remove(proto_file)
		else:
			if not self._datadst in self._workspace:
				os.rename(proto_file, os.path.join(self._datadst, proto_key))
		self._reset_proto_container()
	
	def proto_info(self):
		""" Dispaly proto definition """
		self._pt.get_proto_info()
	
	def pack_protos(self):
		""" Process mas data examples into proto format in batches
		    For child classes implemented for different raw datasets,
		    this method shall be overridden.
		"""
		num_proc = 0
		for rec in tqdm.tqdm(self._record_list, total=self._n_records):
			record = self._example_record(rec)
			if not record: continue
			if self._bucket_name:
				emp_data = self.get_data_from_keys(self.aws.client, self._bucket_name, record)
			else:
				emp_data = self.get_data_from_files(record)
			proto_data = self._add_to_proto(emp_data)
			if not proto_data: continue
			self._pb.proto_batch.append(proto_data)
			num_proc += 1
			self._num_to_batch += 1

			if self._num_to_batch >= self._batch_size:
				self._gen_proto_record()

		if self._num_to_batch > 0:
			self._gen_proto_record()
		print("///: Totally {} proto records saved to {}".format(num_proc, self._datadst))
	
	def list_protos(self, top_n=5, shuffle=False):
		""" list generated proto files

		    Args:
		    top_n: the first n files to show
		    shuffle: if True, shuffle list before display
		"""
		if self.aws.S3_BUCKET_BASE in self._datadst:
			proto_files = self.aws.ls_s3_dir(self._datadst)
			storage_pl = self._datadst
		elif self._datadst in self._workspace:
			proto_files = os.listdir(self._workspace)
			storage_pl = self._workspace
		else:
			proto_files = os.listdir(self._datadst)
			storage_pl = self._datadst

		if shuffle: random.shuffle(proto_files)
		print("///: There are totally {} proto @ [{}] !".format(len(proto_files), storage_pl))
		print("///: The first {} records are listed here:".format(top_n))
		print(proto_files[:top_n])

	def read_one_proto(self, proto_file):
		""" Display one proto contents

		    Args:
		    proto_file: protobuf record filename or url
		"""
		if self.aws.S3_BUCKET_BASE in proto_file:
			bucket_name, s3_key = self.aws.url_to_bnk(proto_file, False)
			proto_file = os.path.join(self._workspace, ntpath.basename(s3_key))
			self.aws.download_file(bucket_name, s3_key, proto_file)
		if not os.path.isfile(proto_file):
			print("///: protobuf reocord DO NOT exist!")
			return
		with open(proto_file, "rb") as f:
			proto_data = im_proto.ImageBatchProto().FromString(f.read())
		print("///: There are {} image protobuf messages in batch-{}".format(
			len(proto_data.proto_batch), proto_data.batch_id))
		print("///: exemplary proto message:")
		print(proto_data.proto_batch[0])
		print("///: loading successfully")
