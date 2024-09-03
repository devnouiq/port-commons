import boto3
from botocore.exceptions import NoCredentialsError, ClientError


class AWSService:
    def __init__(self, aws_access_key_id=None, aws_secret_access_key=None, region_name='us-east-1'):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name
        )

    def upload_file(self, file_path, bucket_name, s3_key):
        try:
            self.s3_client.upload_file(file_path, bucket_name, s3_key)
            print(
                f"File {file_path} uploaded to {bucket_name}/{s3_key} successfully.")
        except FileNotFoundError:
            print(f"The file {file_path} was not found.")
        except NoCredentialsError:
            print("Credentials not available.")
        except ClientError as e:
            print(f"Failed to upload {file_path} to S3: {e}")

    def upload_screenshot(self, file_path, run_id, step_name, bucket_name):
        # Generate the S3 key using the run ID and step name
        file_name = os.path.basename(file_path)
        s3_key = f"screenshots/{run_id}/{step_name}/{file_name}"
        self.upload_file(file_path, bucket_name, s3_key)
