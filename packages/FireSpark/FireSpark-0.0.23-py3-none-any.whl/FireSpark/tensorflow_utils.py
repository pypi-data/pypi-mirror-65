
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
"""FireSpark Tensorflow Dataloader Library """

import os
from pathlib import Path

import io
import cv2
import numpy as np
from .numpy_utils import NumpyLoaderBase


class TFLoaderBase(NumpyLoaderBase):
    """ Base parquet data loader for Tensorflow

            Args:            
            path:    local file system path to dataset. All the
                     Parquet files assume the same petastorm schema. 
            url:     file or s3 URL to parquet dataset
            dataset: string, name of the dataset
            columns: categories to load. Availale categories include:
                     (url, depth, width, height, format, imdata, label)
                     default: [imdata, label]
            label_type: string, label type, e.g. "detection"
            max_det_counts: maximal number of objects in one frame for
                            detection label_type           

            Usage:
            TFLoaderBase.loader: datafrome object
            TFLoaderBase.get_dataset_name(): get dataset name
        """
    def __init__(self, **pars):
        super().__init__(**pars)
        if not 'transform' in self.pars:
            self.pars['transform'] = None
        if not 'label_type' in self.pars:
            self.pars['label_type'] = 'detection'
        if not 'max_det_counts' in self.pars:
            self.pars['max_det_counts'] = 50
    
    def _tranform(self, example):
        im_array = np.frombuffer(example.imdata, np.uint8)
        im = cv2.imdecode(im_array, cv2.IMREAD_COLOR)
        memfile = io.BytesIO(example.label)
        label = np.load(memfile).astype(np.float32)
        if self.pars['label_type'] == "detection":
            paddings = [
                [0, self.pars['max_det_counts']-label.shape[0]],
                [0, 0]
            ]
            label = np.pad(label, paddings)
        return (im, label)

    def __getitem__(self, id):
        example = self.loader.iloc[id]
        return self._tranform(example)
    
    def generate(self):
        for i in range(self.loader_size):
            example = self.loader.iloc[i]
            yield self._tranform(example)
        
    
    


