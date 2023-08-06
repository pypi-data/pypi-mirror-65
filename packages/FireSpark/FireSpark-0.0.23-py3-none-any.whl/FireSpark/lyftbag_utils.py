from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import logging
import os
import struct
import sys
from abc import ABCMeta, abstractmethod

import cv2
import numpy as np

from google.protobuf.descriptor_pool import DescriptorPool
from google.protobuf.message_factory import MessageFactory
from . protos.mas import lyftbag_pb2

log = logging.getLogger(__name__)
'''
Python implementation of the lyftbag library. Currently supports reading from a lyftbag
file.
'''
'''
Usage:
    with Lyftbag(lyftbag_file_path, topics, start_timestamp_ns, end_timestamp_ns, 'r') as bag:
         for meta, payload in bag.read_messages():
            # meta is the message metadata, as defined in src/avs/messages/lyftbag.proto
            # payload is the serialized proto
'''


class Lyftbag(object):
    def __init__(self,
                 lyftbag,
                 topics=None,
                 start_timestamp_ns=0,
                 end_timestamp_ns=sys.maxsize,
                 mode='r'):
        self.topics = topics
        self.start_timestamp_ns = start_timestamp_ns
        self.end_timestamp_ns = end_timestamp_ns
        if mode == 'r':
            self.lyftbagreader = LyftbagReader.get_instance(lyftbag)
        else:
            raise NotImplementedError(
                'Performing operation {} on lyftbag {} not supported'.format(
                    mode, lyftbag))

    def __iter__(self):
        return self.read_messages()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def read_messages(self):
        return self.lyftbagreader.read_messages(
            self.topics, self.start_timestamp_ns, self.end_timestamp_ns)

    def close(self):
        self.lyftbagreader.close()

    def index(self):
        return self.lyftbagreader.index()


class ReflectionLyftbag(Lyftbag):
    """
    Processes Lyftbags using the Reflection information embedded inside

    USAGE:  read_messages() returns a tuple of (Meta, DeserializedProto). The
            DeserializedProto is a Python object of the proper type.

    with ReflectionLyftbag(filename) as bag:
        for meta, message in bag:
            if meta.topic == '/something':
                do_something_useful(message.some_field_name)
    """

    REFLECTION_TOPIC = '/avs/reflection'

    def __init__(self, *args, **kwargs):
        super(ReflectionLyftbag, self).__init__(*args, **kwargs)

        self.pool = DescriptorPool()
        self.descriptors = {}
        self.type_names = {}
        self.message_prototypes = {}
        self.factory = MessageFactory()

        # Find and initialize reflection information
        self._find_and_decode_reflection_info()

    def __enter__(self):
        return self

    def _find_and_decode_reflection_info(self):
        reflection_messages_iter = self.lyftbagreader.read_messages(
            [self.REFLECTION_TOPIC], self.start_timestamp_ns,
            self.end_timestamp_ns)
        for meta, payload in reflection_messages_iter:
            reflection_message = lyftbag_pb2.ReflectionMessage()
            reflection_message.ParseFromString(payload)
            for fd_proto in reflection_message.payload_descriptors.file:
                self.pool.Add(fd_proto)
                fd = self.pool.FindFileByName(fd_proto.name)
                for key in fd.message_types_by_name:
                    descriptor = fd.message_types_by_name[key]
                    type_name = fd.package if len(fd.package) > 0 else ""
                    type_name += "."
                    type_name += descriptor.name
                    if sys.version_info[0] == 3:
                        string_func = lambda x: bytes(x, 'utf-8')  # noqa: E731
                    else:
                        string_func = str
                    type_hash = LyftbagReaderv00.Hash.hash(
                        [struct.unpack('B', string_func(type_name[char_idx:char_idx + 1]))[0] for char_idx in
                         range(len(type_name))])
                    self.message_prototypes[
                        type_hash] = self.factory.GetPrototype(descriptor)

        if self.message_prototypes == {}:
            raise ValueError('No Reflection messages found in this Lyftbag')

        log.info('Finished decoding reflection data...')

    def get_message_prototype(self, meta):
        return self.message_prototypes.get(
            meta.message_header.payload_type_name_hash)

    def read_messages(self):
        """
        Returns a (Meta, <proto_of_message_type>) instead of (Meta, Payload) like Basic Lyftbag
        :return: (meta, deserialized_proto)
        """
        for meta, payload in super(ReflectionLyftbag, self).read_messages():
            # Reflection doesn't contain info about itself
            if meta.topic == self.REFLECTION_TOPIC:
                message = lyftbag_pb2.ReflectionMessage()
                message.ParseFromString(payload)
                yield meta, message
                continue

            # Get the reflected proto class for this message
            message_type = self.get_message_prototype(meta)
            if message_type is None:
                raise ValueError(
                    '/avs/reflection did not contain information to decode topic {}. payload: {}'
                    .format(meta.topic, payload))

            # Actually create the Proto class instance
            message = message_type()
            message.ParseFromString(payload)
            yield meta, message


'''
Abstract Base Class for the lyftbag reader implementation.
'''
class LyftbagReader(object):
    __metaclass__ = ABCMeta

    K_SIGNATURE_SIZE = 8

    def __init__(self, lyftbag):
        self.lyftbag = lyftbag

    '''
    This function looks at the signature of the lyftbag which is the first 8-bytes and
    determines what is the version. Based on the version it uses corresponding
    implementation.
    '''

    @staticmethod
    def get_instance(lyftbag):
        # Look at the first 8 bytes of the file and from the signature determine the
        # version.
        try:
            with open(lyftbag, 'rb') as f:
                signature = f.read(LyftbagReader.K_SIGNATURE_SIZE)
        except IOError as e:
            raise LyftbagReaderException(
                '{}, error opening file. IOError {}'.format(lyftbag, e))
        if signature == LyftbagReaderv00.Signature.K_SIGNATURE:
            return LyftbagReaderv00(lyftbag)
        else:
            raise LyftbagReaderException(
                'Unsupported version for lyftbag {}, signature found {}'.
                format(lyftbag, signature))

    @abstractmethod
    def read_messages(self, topics, start_timestamp_ns, end_timestamp_ns):
        raise NotImplementedError()

    @abstractmethod
    def close(self):
        raise NotImplementedError()

    @abstractmethod
    def index(self):
        raise NotImplementedError()


class LyftbagReaderException(Exception):
    def __init__(self, value):
        self.value = value

    # __str__ is to print() the value
    def __str__(self):
        return (repr(self.value))


class LyftbagReaderv00(LyftbagReader):
    # This should serve as a version.
    class Signature(object):
        K_SIGNATURE = b"AVSLOG00"

    class RecordHeader(object):
        RECORD_HEADER_SIZE = 24

        def __init__(self, record_header_bytes_array):
            self.sizes_hash, self.metadata_size, self.payload_size = struct.unpack_from(
                'QQQ', record_header_bytes_array)

    class RecordFooter(object):
        RECORD_FOOTER_SIZE = 8

        def __init__(self, record_footer_bytes_array):
            self.data_hash = struct.unpack_from('Q',
                                                record_footer_bytes_array)[0]

    class IndexFooter(object):
        INDEX_FOOTER_SIZE = 24

        def __init__(self, index_bytes_array):
            self.index_hash, self.index_size, self.size_hash = struct.unpack_from(
                'QQQ', index_bytes_array)

    # Implementation coming from src/avs/libs/avs_core/hash.cc
    class Hash(object):

        # Random large prime number.
        K_INIT_HASH = 4759813713137040889

        # Prime number bigger than 256.
        K_POLYNOMIAL_ARGUMENT = 701

        # A pattern containing 64 bits.
        K_64BIT = 2**64 - 1

        @classmethod
        def hash(cls, input_byte_array, init_hash=K_INIT_HASH):
            h = init_hash
            for b in input_byte_array:
                h = (h * cls.K_POLYNOMIAL_ARGUMENT + b) & cls.K_64BIT
            return h

    def __init__(self, lyftbag):
        LyftbagReader.__init__(self, lyftbag)
        try:
            self.file_handle = open(self.lyftbag, 'rb')
        except IOError as e:
            raise LyftbagReaderException(
                '{}, error opening file. IOError {}'.format(self.lyftbag, e))
        except Exception as e:
            raise LyftbagReaderException('{}, error opening file. {}'.format(
                self.lyftbag, e))

        self.file_size = os.path.getsize(self.lyftbag)

        self.validate_signature()
        self.index_footer, self.lyftbag_index = self.validate_index()

        if not self.lyftbag_index:
            self.max_record_file_size = self.file_size
        else:
            self.max_record_file_size = self.file_size - self.index_footer.index_size - \
                                        self.IndexFooter.INDEX_FOOTER_SIZE

        self.file_handle.seek(LyftbagReader.K_SIGNATURE_SIZE)

    def index(self):
        return (self.index_footer, self.lyftbag_index)

    # TODO: Refactor this function and remove the noqa C901
    def read_messages(self, topics, start_timestamp_ns, end_timestamp_ns):  # noqa C901
        def should_yield_message():
            if not meta.topic:
                raise LyftbagReaderException(
                    "Empty topic found for the given message")
            meta.topic = meta.topic if meta.topic.startswith(
                '/') else '/' + meta.topic

            if (not topics or meta.topic in topics) \
                    and start_timestamp_ns <= meta.message_header.wall_timestamp_ns \
                    and meta.message_header.wall_timestamp_ns <= end_timestamp_ns:
                return True
            return False

        if not self.lyftbag_index:
            # TODO(ssakdeo): Reading this way is extremely slow < 3MB/s.
            # Mostly attributed to cost of computing hashes on record, to
            # know end of file. This path if taken only for lyftbags that
            # do not have index information, which is a very small subset.
            while self.file_handle.tell() < self.max_record_file_size:
                try:
                    record_header_byte_array = bytearray(
                        self.file_handle.read(
                            self.RecordHeader.RECORD_HEADER_SIZE))
                except EOFError as e:
                    return
                try:
                    record_header = self.RecordHeader(record_header_byte_array)
                except struct.error as e:
                    assert len(record_header_byte_array) < self.RecordHeader.RECORD_HEADER_SIZE
                    return
                if not LyftbagReaderv00.validate_record_header(record_header):
                    return
                metadata_pos = self.file_handle.tell()
                payload_pos = metadata_pos + record_header.metadata_size
                record_footer_pos = payload_pos + record_header.payload_size
                if self.max_record_file_size < record_footer_pos + self.RecordFooter.RECORD_FOOTER_SIZE:
                    # Entire message not found.
                    return
                # read the metadata bytes
                metadata = self.file_handle.read(record_header.metadata_size)
                # read the payload bytes
                payload = self.file_handle.read(record_header.payload_size)
                # read the record footer
                record_footer = self.RecordFooter(
                    bytearray(
                        self.file_handle.read(
                            self.RecordFooter.RECORD_FOOTER_SIZE)))
                # validate the hash in the record footer is OK.
                if not self.validate_data_hash(metadata, payload,
                                               record_footer):
                    return
                # parse the metadata
                meta = lyftbag_pb2.Metadata()
                meta.ParseFromString(metadata)
                if should_yield_message():
                    yield (meta, payload)
        else:
            for index_item in self.lyftbag_index.items:
                self.file_handle.seek(index_item.payload_offset)
                try:
                    payload = self.file_handle.read(index_item.payload_length)
                except MemoryError as e:
                    # Raised when reading a corrupt offset from a file.
                    raise LyftbagReaderException(
                        "Could not read record in file {} due to corrupt offset {}: {}"
                        .format(self.lyftbag, index_item.record_offset, e))
                meta = index_item.metadata
                if should_yield_message():
                    yield (meta, payload)

    def validate_data_hash(self, metadata, payload, record_footer):
        metadata_byte_array = [struct.unpack('B', bytes(metadata[idx:idx+1]))[0] for idx in range(len(metadata))]
        payload_byte_array = [struct.unpack('B', bytes(payload[idx:idx+1]))[0] for idx in range(len(payload))]
        return self.Hash.hash(metadata_byte_array +
                              payload_byte_array) == record_footer.data_hash

    @staticmethod
    def validate_record_header(record_header):
        metadata_size_hash = LyftbagReaderv00.Hash.hash(
            bytearray(struct.pack('Q', record_header.metadata_size)))
        sizes_hash = LyftbagReaderv00.Hash.hash(
            bytearray(struct.pack('Q', record_header.payload_size)),
            metadata_size_hash)
        return sizes_hash == record_header.sizes_hash

    def validate_signature(self):
        # Check if the file has valid signature.
        if self.file_size < LyftbagReader.K_SIGNATURE_SIZE:
            raise LyftbagReaderException(
                '{}, has a file size of {} and hence no valid signature'.
                format(self.lyftbag, self.file_size))

        found_signature = self.file_handle.read(LyftbagReader.K_SIGNATURE_SIZE)
        if found_signature != self.Signature.K_SIGNATURE:
            raise LyftbagReaderException(
                '{}, has no valid signature, found {}, expected {}'.format(
                    self.lyftbag, found_signature, self.Signature.K_SIGNATURE))

    @staticmethod
    def validate_index_footer(index_footer):
        return LyftbagReaderv00.Hash.hash(
            bytearray(struct.pack(
                'Q', index_footer.index_size))) == index_footer.size_hash

    def validate_index(self):
        # Check if the file has index.
        if self.file_size <= LyftbagReader.K_SIGNATURE_SIZE + self.IndexFooter.INDEX_FOOTER_SIZE:
            return None, None

        # There is a possibility that we have index footer.
        # Let's verify if we have an intact one by comparing hash.
        self.file_handle.seek(-self.IndexFooter.INDEX_FOOTER_SIZE +
                              self.file_size)
        index_footer_byte_array = bytearray(
            self.file_handle.read(self.IndexFooter.INDEX_FOOTER_SIZE))
        index_footer = self.IndexFooter(index_footer_byte_array)

        if not LyftbagReaderv00.validate_index_footer(index_footer):
            return None, None

        # Seek to the beginning of the index.
        self.file_handle.seek(self.file_size -
                              self.IndexFooter.INDEX_FOOTER_SIZE -
                              index_footer.index_size)

        lyftbag_index_content = self.file_handle.read(index_footer.index_size)

        # Read the index contents into a byte array.
        # In Python 2, open(file, 'rb') gets a string, 'GIF89a' for example.
        # In Python 3, open(file, 'rb') gets a bytes object, b'GIF89a'.
        # 'GIF89a'[2] = 'F', and b'GIF89a'[2] = 70 (integer). b'GIF89a'[2:3] = b'F'.
        index_bytearray = bytearray(lyftbag_index_content)
        if index_footer.index_hash != self.Hash.hash(index_bytearray):
            return None, None

        try:
            lyftbag_index = lyftbag_pb2.LyftbagIndex()
            lyftbag_index.ParseFromString(lyftbag_index_content)
        except UnicodeDecodeError:
            return None, None

        return index_footer, lyftbag_index

    def close(self):
        self.file_handle.close()


class CamLoader(object):
    """ Mas lyftbad reader class  """

    def __init__(self, lyftbag, **job):
        self.jc = {
            'topics' : None,
            'start_timestamp_ns' : 0,
            'end_timestamp_ns' : sys.maxsize
        }
        self.jc.update(job)
        self.lyftbag = lyftbag
        self.frames = self._frame_provider()
    
    def _frame_provider(self):
        """ provide camer frames from lyftbag """
        with Lyftbag(self.lyftbag, None, 
                     self.jc['start_timestamp_ns'],
                     self.jc['end_timestamp_ns'],
                     'r') as bag:
            for meta, payload in bag.read_messages():
                assert 'image_compressed' in meta.topic, "Error: pleae provide camera lyftbag!"
                cam_payload = lyftbag_pb2.CompressedImage()
                cam_payload.ParseFromString(payload)
                im = cv2.imdecode(np.fromstring(cam_payload.data, dtype=np.uint8), -1)
                cam_data = {"meta": cam_payload.metadata, "image": im}
                yield cam_data