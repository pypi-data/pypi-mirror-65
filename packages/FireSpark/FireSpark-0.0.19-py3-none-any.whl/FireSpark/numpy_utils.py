
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
"""FireSpark Numpy Dataloader Library """

import itertools
import numpy as np
import cv2
from petastorm import make_reader, TransformSpec

class NumpyLoaderBase(object):
    """ Base parquet data loader for vanila python numpy framework

            Args:
            url: file or s3 URL to parquet file group
            dataset: string, name of the dataset
            n_epochs: number to epochs to iterate through dataset
            fields_to_remove: schema fields NOT to use when loading dataset
            workers_count: number of works, default 10

            Usage:
            TorchLoaderBase.loader: dataloader object to iterate 
            TorchLoaderBase.get_dataset_name(): get dataset name
        """
    def __init__(self, url, **pars):
        self.pars = {
            'dataset' : "",
            'n_epochs' : 1,
            'workers_count' : 10
        }
        self.pars.update(pars)
        self.loader = None
        self.loader_size = 0
        if url.startswith("file://") or url.startswith("s3://"):
            self.parquet_dataset_url = url
            self._make_loader()
        else:
            print("/Error/: incorrect URL path string!")

    def _make_loader(self):
        """ Instantiate numpy dataloader object	"""
        self.loader = make_reader(
            dataset_url=self.parquet_dataset_url,
            num_epochs=self.pars['n_epochs'],
            workers_count=self.pars['workers_count']
        )
    
    def get_dataset_name(self):
        """ Return dataset name	"""
        return self.pars['dataset']
    
    def __len__(self):
        """ get the length of the dataset loader """
        if not self.loader_size:
            self._get_loader_size()
        return self.loader_size
    
    def size(self):
        return self.__len__()
    
    def _get_loader_size(self):
        """ Count dataset samples """
        self.loader_size = sum(1 for _ in self.loader)
        self.loader.reset()
    
    def __getitem__(self, index):
        if not self.loader_size:
            self._get_loader_size()
        if index < self.loader_size:
            try:
                return next(itertools.islice(self.loader,index,index+1))
            except (RuntimeError, TypeError, NameError):
                pass
        



