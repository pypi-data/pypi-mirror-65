
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
"""FireSpark AWS utility library """

import os
import logging
import tqdm
from typing import Dict, List, Generator, Tuple
from pathlib import Path

import boto3
from botocore.exceptions import ClientError, ProfileNotFound
from boto3.s3.transfer import TransferConfig


class FireSparkAWS(object):
    """ FireSpark aws class    """
    def __init__(self, profile='magna_data'):
        self.S3_BUCKET_BASE = "s3://"
        self.active = False
        try:
            if profile in boto3.session.Session().available_profiles:
                self.session = boto3.session.Session(profile_name=profile)
                self.client = self.session.client('s3')
                self.active = True
        except ProfileNotFound:
            logging.error("Missing AWS Authentication!")
        self.config = TransferConfig()
    
    def set_configuration(self, **kwargs):
        """ example args:
        use_threads=False
        max_concurrency=10
        multipart_gb=5*1024**3 (5GB)
        """
        self.config = TransferConfig(**kwargs)

    def ls_s3_dir(self, aws_url: str, folders=False) -> List[str]:
        """List everthing under the remote aws url folder.

        Args:
        aws_url: a string to the remote aws directory.
        folders: a boolean. If True only folders are returned.

        Returns:
        A list of items inside aws_url.
        Path to "files" are returned with no trailing /.
        Path to "folders" are returned with trailing /.
        """        
        result = []
        if not self.active: return result
        bucket_name, s3_key = self.url_to_bnk(aws_url)
        try:
            response = self.client.list_objects_v2(
                Bucket=bucket_name,
                Prefix=s3_key,
                Delimiter='/')
        except Exception as e:
            raise ValueError('Failed to list objects with error: {}'.format(str(e)))

        if not folders and len(response.get('Contents', [])) > 0:
            for item in response['Contents']:
                item_key = item['Key'][len(s3_key):]
                result.append(item_key)
        if len(response.get('CommonPrefixes', [])) > 0:
            for item in response['CommonPrefixes']:
                item_key = item['Prefix'][len(s3_key):]
                result.append(item_key)
        return result

    def ls_s3_objects(self, aws_url: str) -> [dict]:
        """ List all objects for the given aws url.

        Args:
        aws_url: a string to the remote aws directory
        
        Returns:
        A [dict] containing the elements in the url container
        """
        if not self.active: return []
        bucket_name, s3_key = self.url_to_bnk(aws_url)
        try:
            contents = self.client.list_objects(Bucket=bucket_name, Prefix=s3_key)['Contents']
        except KeyError:
            # No Contents Key, empty bucket.
            return []
        else:
            return contents

    def download_dir(self, bucket: str, local: str, prefix=''):
        """Download S3 direcotry to local 

        Args:
        client: initialized s3 client object
        prefix: pattern to match in s3
        bucket: s3 bucket with target contents
        local: local path to folder
        """
        if not self.active: return
        keys = []
        dirs = []
        next_token = ''
        base_kwargs = {
            'Bucket':bucket,
            'Prefix':prefix,
        }
        while next_token is not None:
            kwargs = base_kwargs.copy()
            if next_token != '':
                kwargs.update({'ContinuationToken': next_token})
            results = self.client.list_objects_v2(**kwargs)
            contents = results.get('Contents')
            for i in contents:
                k = i.get('Key')
                if k[-1] != '/':
                    keys.append(k)
                else:
                    dirs.append(k)
            next_token = results.get('NextContinuationToken')
        
        for d in dirs:
            dest_pathname = os.path.join(local, d)
            if not os.path.exists(os.path.dirname(dest_pathname)):
                os.makedirs(os.path.dirname(dest_pathname))
        for k in tqdm.tqdm(keys):
            dest_pathname = os.path.join(local, k)
            if not os.path.exists(os.path.dirname(dest_pathname)):
                os.makedirs(os.path.dirname(dest_pathname))
            self.client.download_file(bucket, k, dest_pathname)


    def get_s3_objects(self, bucket: str, prefix='', suffix='') -> Generator:
        """Generate the objects in an S3 bucket.

        Args:
        bucket: Name of the S3 bucket
        prefix: pattern to match in s3 key
        suffix: pattern to match in s3 key
        
        Returns:
        s3 object generator
        """
        if not self.active: return None
        kwargs = {'Bucket': bucket}
        if isinstance(prefix, str):
            kwargs['Prefix'] = prefix
        while True:
            resp = self.client.list_objects_v2(**kwargs)
            try:
                contents = resp['Contents']
            except KeyError:
                return

            for obj in contents:
                key = obj['Key']
                if key.startswith(prefix) and key.endswith(suffix):
                    yield obj

            try:
                kwargs['ContinuationToken'] = resp['NextContinuationToken']
            except KeyError:
                break

    def get_s3_keys(self, bucket: str, prefix='', suffix='', full_key=False) -> Generator:
        """Generate the keys in an S3 bucket.

        Args:
        bucket: Name of the S3 bucket
        prefix: pattern to match in s3 key
        suffix: pattern to match in s3 key
        
        Returns:
        s3 key generator
        """
        if not self.active: return None
        for obj in self.get_s3_objects(bucket, prefix, suffix):
            if full_key:
                yield os.path.join(self.S3_BUCKET_BASE, bucket, obj['Key'])
            else:
                yield obj['Key']

    def upload_file(self, bucket: str, local_file: str, object_name: str) -> bool:
        """Upload a file to an S3 bucket

        Args:
        bucket: Name of the S3 bucket
        local_file: local file to upload
        object_name: S3 object name
        
        Returns:
        uploda status
        """
        if not self.active: return False
        try:
            response = self.client.upload_file(local_file,
                                            bucket,
                                            object_name,
                                            Config=self.config)
        except ClientError as e:
            logging.error(e)
            return False
        return True

    def download_file(self, bucket: str, object_name: str, local_file: str) -> bool:
        """Download a file from an S3 bucket

        Args:
        bucket: Name of the S3 bucket
        object_name: S3 object name
        local_file: local file to save download as
        
        Returns:
        download status
        """
        if not self.active: return False
        try:
            response = self.client.download_file(bucket,
                                                object_name,
                                                local_file,
                                                Config=self.config)
        except ClientError as e:
            logging.error(e)
            return False
        return True
    
    @staticmethod
    def ls_local_objects(local_folder: str) -> [str]:
        """Utils for ls local folder information

        Args:
        local_folder: folder on local disk

        Returns:
        relative names of the files.
        """
        path = Path(local_folder)
        paths = []
        for file_path in path.rglob("*"):
            if file_path.is_dir():
                continue
            str_file_path = str(file_path)
            str_file_path = str_file_path.replace(f'{str(path)}/', "")
            paths.append(str_file_path)
        return paths
    
    @staticmethod
    def url_to_bnk(aws_url: str, isfolder=True) -> Tuple[str, str]:
        """Util for bucket and key info from url"""
        s3_url_list = os.path.relpath(aws_url, "s3://").split('/')
        if len(s3_url_list) < 2:
            raise ValueError('Failed to extract bucket info from {}'.format(aws_url))
        bucket_name = s3_url_list[0]
        task_key = '/'.join(s3_url_list[1:])
        if not task_key.endswith('/') and isfolder:
            task_key += '/'
        return bucket_name, task_key
    
    def sync_from_local(self, local: str, aws_url: str):
        """Sync local to aws_url

        Args:
        local: folder on local disk
        aws_url: destination s3 folder
        """
        if not self.active: return
        assert "s3://" in aws_url, "Incorrect s3 path!"
        bucket_name, s3_key = self.url_to_bnk(aws_url)
        files = self.ls_local_objects(local_folder=local)        
        objects = self.ls_s3_objects(aws_url)
        object_keys = [obj['Key'] for obj in objects]
        for f in files:
            target_key = os.path.join(s3_key, f)
            if not target_key in object_keys:
                local_file = os.path.join(local, f)
                self.upload_file(bucket_name, local_file, target_key)

    def sync_to_local(self, aws_url: str, local: str):
        """Sync aws_url to local

        Args:
        aws_url: source s3 folder
        local: destination folder on local disk        
        """
        if not self.active: return
        assert "s3://" in aws_url, "Incorrect s3 path!"
        bucket_name, s3_key = self.url_to_bnk(aws_url)
        objects = self.ls_s3_objects(aws_url)
        object_keys = [obj['Key'] for obj in objects]
        object_keys.remove(s3_key)
        for ok in object_keys:
            obj = ok[len(s3_key):]
            dst_folder = os.path.join(local, os.path.dirname(obj))
            if not os.path.exists(dst_folder): os.makedirs(dst_folder)
            dst_file = os.path.join(local, obj)
            if not os.path.isfile(dst_file):
                self.download_file(bucket_name, ok, dst_file)
