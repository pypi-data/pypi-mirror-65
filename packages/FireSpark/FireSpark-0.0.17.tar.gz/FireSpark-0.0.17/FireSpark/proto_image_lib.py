""" FireSpark
Methods for pcking information from raw dataset 
to proto template. 

Instructions:
In order to process protobuf record for a new dataset, 
a dataset object class has to be defined, which 
implementing method to:

1). A record provider method "_example_record()" that take
	one raw dataset record from the original dataset and 
	produce a (image, annotation) tuple. Users defining new
	class have the flexibility to have other data types for
	the record list given that such record can be correctly
	used in "_example_template()" method. 
2). Override the "_example_template()" method if necessary. 
	The output of this method is a template dictionary 
	containing all defined protobuf fields. For user's 
	dataset, filling the dataset inforamtion as much as
	possible in this method. After that, the template dict
	is converted to protobuf message based on target protobuf
	message definition. 
3). If necessary, make change to the protobuf record's naming
	method in "_proto_file()". 

Those are all you need before protobuf database archiving task. 

"""

import os
from .proto_utils import ProtoDataset
from .protos.mas import annotation_pb2 as annotation_proto
from .protos.mas import image_data_pb2 as image_proto


class DowntownDataset(ProtoDataset):
	""" Downtown dataset class """
	def __init__(self, data_source='../tests/data/',
				data_storage='', num_records=29112):
		dataset = "Downtown"
		super().__init__(dataset=dataset,
						 data_source=data_source,
						 data_storage=data_storage,
						 num_records=num_records)
	
	def _example_record(self, f):
		""" Method for providing one downtown dataset example record
			For child classes implemented for different raw datasets,
			this method shall be overridden.

			Returns: a tuple of (image file, annotation file)
		"""
		if '.txt' in f:
			return (f[:-3]+"jpg", f)
		else:
			return None

	def _add_to_proto(self, record):
		""" Method for processing downtown dataset example to protobuf message
			For child classes implemented for different raw datasets,
			this method shall be overridden.

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

		pd = image_proto.ImageDataProto()
		if 'Main' in record[0]:
			pd.device.camera_id = 'AtsBr_ZL_Rr60_v2_FRONT'
			pd.device.calib.optical_center.x = 645.590088
			pd.device.calib.optical_center.y = 404.268311
			pd.device.calib.pose.offset_x = -699.9972
			pd.device.calib.pose.offset_y = -92.075
			pd.device.calib.pose.offset_z = 695.325
			pd.device.calib.pose.rectified_yaw = -180
			pd.device.calib.pose.relative_yaw = 0.938434893
			pd.device.calib.pose.relative_pitch = 72.16128929
			pd.device.calib.pose.relative_roll = 1.779883214
		elif 'LEFT' in record[0]:
			pd.device.camera_id = 'AtsBr_ZL_Rr60_v2_LEFT'
			pd.device.calib.optical_center.x = 646.712524
			pd.device.calib.optical_center.y = 403.630188
			pd.device.calib.pose.offset_x = 920.75
			pd.device.calib.pose.offset_y = -1039.625
			pd.device.calib.pose.offset_z = 920.75
			pd.device.calib.pose.rectified_yaw = -90
			pd.device.calib.pose.relative_yaw = 0.274599064
			pd.device.calib.pose.relative_pitch = 44.01960357
			pd.device.calib.pose.relative_roll = 1.0391655
		elif 'REAR' in record[0]:
			pd.device.camera_id = 'AtsBr_ZL_Rr60_v2_REAR'
			pd.device.calib.optical_center.x = 646.2454
			pd.device.calib.optical_center.y = 404.3708
			pd.device.calib.pose.offset_x = 3736.9386
			pd.device.calib.pose.offset_y = -41.0967
			pd.device.calib.pose.offset_z = 839.1389
			pd.device.calib.pose.rectified_yaw = 0
			pd.device.calib.pose.relative_yaw = -2.397
			pd.device.calib.pose.relative_pitch = 60.1193
			pd.device.calib.pose.relative_roll = 1.2359
		elif 'RIGHT' in record[0]:
			pd.device.camera_id = 'AtsBr_ZL_Rr60_v2_RIGHT'
			pd.device.calib.optical_center.x = 642.071594
			pd.device.calib.optical_center.y = 404.993286
			pd.device.calib.pose.offset_x = 920.75
			pd.device.calib.pose.offset_y = 1039.625
			pd.device.calib.pose.offset_z = 920.75
			pd.device.calib.pose.rectified_yaw = 90
			pd.device.calib.pose.relative_yaw = -1.258962111
			pd.device.calib.pose.relative_pitch = 44.22432222
			pd.device.calib.pose.relative_roll = -2.9152963
		else:
			pd.device.camera_id = 'UNKNOWN'

		pd.device.calib.lens_type = 1
		pd.device.calib.pixelsize = 0.003
		pd.device.calib.focal_length.x = 1.0
		pd.device.calib.focal_length.y = 1.0
		pd.device.calib.radial_distortion_I2W.extend(
			[0, 0.949960, -0.001374, -0.063414, -0.014087, 0.017911])
		pd.device.calib.radial_distortion_W2I.extend(
			[0, 1.044910, 0.074981, -0.148220, 0.303387, -0.132219])
		pd.device.calib.pose.ref_origin = "front axle center at group"
		pd.device.calib.pose.ref_axis_x = "to rear axle"
		pd.device.calib.pose.ref_axis_y = "to vehicle body right"
		pd.device.calib.pose.ref_axis_z = "to up"
		pd.device.calib.pose.rectified_pitch = 0
		pd.device.calib.pose.rectified_roll = 0
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
		return "{}_{}_batch_{}.proto".format(
							self._dataset_name,
							self._pb.proto_batch[0].device.camera_id,
							self._batch_id)
	
	
class DirtyLenseDataset(ProtoDataset):
	""" Dirty-lense dataset class """
	def __init__(self, data_source='',
				data_storage='', num_records=9361):
		dataset = "Dirtylense"
		super().__init__(dataset=dataset,
						 data_source=data_source,
						 data_storage=data_storage,
						 num_records=num_records)

	def _example_record(self, f):
		""" Method for provide one downtown dataset example record
			For child classes implemented for different raw dataset, 
			this method shall be overrided. 

			Return: image and annotation file tuple
		"""
		if '..json' in f:
			imf = f.replace("/Annotations/", "/Images/")
			return (imf[:-5]+"jpg", f)
		else:
			return None

	def _add_to_proto(self, record):
		""" Method for process downtown dataset example to protobuf
			For child classes implemented for different raw dataset, 
			this method shall be overrided. 

			Args:
			record: a tuple of (url, image_array, annotation_string)

			Returns:
			new protobuf message for dataset example
		"""
		imh, imw, imc = record[1].shape
		pd = image_proto.ImageDataProto()
		pd.image_data.image.width = imw
		pd.image_data.image.height = imh
		pd.image_data.image.depth = imc
		pd.image_data.image.format = 1
		pd.image_data.image.url = record[0]
		for c in record[2]['cells']:			
			dl_proto = annotation_proto.DirtyLensCell()
			dl_proto.location.min.x = float(c['left'])
			dl_proto.location.min.y = float(c['top'])
			dl_proto.location.max.x = float(c['right'])
			dl_proto.location.max.y = float(c['bottom'])
			dl_proto.occlusion_type = c['occlusion_type']
			dl_proto.occlusion_percentage = c['occlusion_percentage']
			dl_proto.occlusion_density = c['occlusion_density']
			pd.image_data.annotation.dl_cell.append(dl_proto)
		return pd
	
	def _proto_file(self):
		return "{}_batch_{}.proto".format(
							self._dataset_name,
							self._batch_id)