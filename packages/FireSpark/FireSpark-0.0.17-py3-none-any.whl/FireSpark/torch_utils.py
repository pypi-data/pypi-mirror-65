
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
"""FireSpark PyTorch Dataloader Library """

import numpy as np
import cv2

from petastorm import make_reader, TransformSpec
from petastorm.pytorch import DataLoader
from torchvision import transforms


class TorchLoaderBase(object):
	""" Base parquet data loader for PyTorch framework

		    Args:
		    url: file or s3 URL to parquet file group
			dataset: string, name of the dataset
			label_type: string, label type, e.g. "detection"
			transform: image tranform object from torchvision 
			n_epochs: number to epochs to iterate through dataset
			batch_size: dataloader batch size
			fields_to_remove: schema fields NOT to use when loading dataset

		    Usage:
			TorchLoaderBase.loader: dataloader object to iterate 
			TorchLoaderBase.get_dataset_name(): get dataset name
		"""
	def __init__(self, url, **pars):
		self.pars = {
			'dataset' : "",
			'label_type' : "detection",
			'transform' : None,
			'n_epochs' : 1,
			'batch_size' : 1,
			'fields_to_remove' : []
		}
		self.pars.update(pars)
		self.loader = None
		if url.startswith("file://") or url.startswith("s3://"):
			self.parquet_dataset_url = url
			if self.pars['transform']:
				self.im_transform = self.pars['transform']
			else:
				self.im_transform = transforms.Compose([
					transforms.ToTensor()
				])
			if self.pars['fields_to_remove']:
				self.fields_to_remove = self.pars['fields_to_remove']
			else:
				self.fields_to_remove = \
					['cam', 'depth', 'format', 'height', 'url', 'width']
			self._make_loader()
		else:
			print("/Error/: incorrect URL path string!")

	def _make_loader(self):
		""" Instantiate torch dataloader object	"""
		transform = TransformSpec(self._transform_row,
				removed_fields=self.fields_to_remove)
		self.loader = DataLoader(
			make_reader(
				dataset_url=self.parquet_dataset_url,
				num_epochs=self.pars['n_epochs'],
				transform_spec=transform),
			batch_size=self.pars['batch_size'])
	
	def _transform_row(self, example):
		result_row = {
			'imdata': self.im_transform(example['imdata']),
			'label': self.parse_label(example['label'])
		}
		return result_row
	
	def parse_label(self, label, max_n=30):
		y_train = label.astype(np.float32)
		if self.pars['label_type'] == "detection":
			paddings = [[0, max_n - y_train.shape[0]], [0, 0]]
			y_train = np.pad(y_train, paddings)
		return y_train
	
	def get_dataset_name(self):
		return self.pars['dataset']


