from django.core.files.storage import Storage
from storages.backends.s3boto3 import S3Boto3Storage
from botocore.client import Config
import boto3
from django.conf import settings

class IBMCloudObjectStorage(S3Boto3Storage):
    endpoint_url = settings.AWS_S3_ENDPOINT_URL
    access_key = settings.AWS_ACCESS_KEY_ID
    secret_key = settings.AWS_SECRET_ACCESS_KEY
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    file_overwrite = False
    custom_domain = False


    def _get_connection(self):
        if self._connections.connection is None:
            self._connections.connection = boto3.session.Session().client('s3',
                aws_access_key_id=self.access_key,
                aws_secret_access_key=self.secret_key,
                endpoint_url=self.endpoint_url,
                config=Config(signature_version='s3v4')
            )
        return self._connections.connection

    def _save(self, name, content):
        # Set the metadata for the object
        metadata = {'product_id': 'YOUR_PRODUCT_ID'}

        # Upload the file with metadata
        self.connection.upload_fileobj(content, self.bucket_name, name, ExtraArgs={'Metadata': metadata})
        return name
