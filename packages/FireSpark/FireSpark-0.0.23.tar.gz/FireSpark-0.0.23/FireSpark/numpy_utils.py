
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

import os
from pathlib import Path

import io
import cv2
import numpy as np
import pandas as pd
import pyarrow.parquet as pq

class NumpyLoaderBase(object):
    """ Base parquet data loader for vanila python numpy framework

            Args:
            path:    local file system path to dataset. All the
                     Parquet files assume the same petastorm schema. 
            url:     file or s3 URL to parquet dataset
            dataset: string, name of the dataset
            columns: categories to load. Availale categories include:
                     (url, depth, width, height, format, imdata, label)
                     default: [imdata, label]
        """
    def __init__(self, **pars):
        self.pars = {
            'path' : "",
            'url' : "",
            'dataset' : "",
            'columns' : ['imdata', 'label']
        }
        self.pars.update(pars)
        self.loader = None
        self.loader_size = 0
        self.loader_meta = None
        self._make_loader()

    def _make_loader(self):
        """ Instantiate numpy dataloader object	"""
        if self.pars['path']:
            parquets = []
            parquets = list(
                Path(os.path.abspath(
                    self.pars['path']
                )).glob('**/*.parquet'))
            if parquets:
                dfs = []
                for f in parquets:
                    dfs.append(
                        pq.read_table(source=f,
                            columns=self.pars['columns']
                        ).to_pandas())
                self.loader = pd.concat(dfs)
                self.loader_size = self.loader.shape[0]
                if not self.loader_meta:
                    _pf = pq.ParquetFile(parquets[0])
                    self.loader_meta = _pf.metadata
        elif self.pars['url'].startswith("file://") or \
            self.pars['url'].startswith("s3://"):
            pass
        else:
            print("/Error/: incorrect URL or PATH string!")
    
    def get_dataset_name(self):
        """ Return dataset name	"""
        return self.pars['dataset']
    
    def __len__(self):
        """ get the length of the dataset loader """
        return self.loader_size
    
    def size(self):
        return self.__len__()
    
    def info(self):
        print('---------schema info-------')
        print(self.loader_meta)
        print('---------counts-------')
        print(self.loader.count())
    
    def __getitem__(self, id):
        example = self.loader.iloc[id]
        im_array = np.frombuffer(example.imdata, np.uint8)
        im = cv2.imdecode(im_array, cv2.IMREAD_COLOR)
        memfile = io.BytesIO(example.label)
        label = np.load(memfile)
        return (im, label)
        



