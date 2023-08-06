
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
"""FireSpark Data File Schema """

import numpy as np
from pyspark.sql.types import IntegerType, StringType

from petastorm.codecs import ScalarCodec, CompressedImageCodec, NdarrayCodec
from petastorm.unischema import Unischema, UnischemaField


""" Unischema is capable of rendering types of its fields into different 
framework specific formats, such as: Spark StructType, Tensorflow tf.DType
and numpy numpy.dtype. 

- To define a dataset field, you need to specify a type, shape, a codec 
  instance and whether the field is nullable for each field of the Unischema.

"""

TemplateSchema = Unischema('TemplateSchema', [
    UnischemaField('id', np.int32, (), ScalarCodec(IntegerType()), False),
    UnischemaField('image1', np.uint8, (128, 256, 3), CompressedImageCodec('png'), False),
    UnischemaField('array_4d', np.uint8, (None, 128, 30, None), NdarrayCodec(), False),
])


MasSchema = Unischema('MasSchema', [
    UnischemaField('cam', np.string_, (), ScalarCodec(StringType()), False),
    UnischemaField('width', np.int_, (), ScalarCodec(IntegerType()), False),
    UnischemaField('height', np.int_, (), ScalarCodec(IntegerType()), False),
    UnischemaField('depth', np.int_, (), ScalarCodec(IntegerType()), False),
    UnischemaField('format', np.int_, (), ScalarCodec(IntegerType()), False),
    UnischemaField('url', np.string_, (), ScalarCodec(StringType()), True),    
    UnischemaField('imdata', np.uint8, (800, 1280, 3), CompressedImageCodec('jpg'), False),
    UnischemaField('label', np.float64, (None, 5), NdarrayCodec(), False),
])


MasDLSchema = Unischema('DirtyLenseSchema', [
    UnischemaField('cam', np.string_, (), ScalarCodec(StringType()), False),
    UnischemaField('width', np.int_, (), ScalarCodec(IntegerType()), False),
    UnischemaField('height', np.int_, (), ScalarCodec(IntegerType()), False),
    UnischemaField('depth', np.int_, (), ScalarCodec(IntegerType()), False),
    UnischemaField('format', np.int_, (), ScalarCodec(IntegerType()), False),
    UnischemaField('url', np.string_, (), ScalarCodec(StringType()), True),    
    UnischemaField('imdata', np.uint8, (800, 1280, 3), CompressedImageCodec('jpg'), False),
    UnischemaField('label', np.float64, (36, 7), NdarrayCodec(), False),
])