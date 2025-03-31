import boto3
import pandas as pd
import logging
from botocore.exceptions import ClientError
from io import StringIO

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class S3Uploader:
    """A class to handle uploading data to AWS S3."""

    def __init__(self, bucket_name: str):
        """Initialize the S3Uploader with the specified bucket name.

        Args:
            bucket_name (str): The name of the S3 bucket.
        """
        self.bucket_name = bucket_name
        self.s3_client = boto3.client('s3')

    def upload_data(self, data: pd.DataFrame, file_name: str, file_format: str = 'csv'):
        """
        Upload data to AWS S3.

        Args:
            data (pd.DataFrame): Pandas DataFrame with data.
            file_name (str): The name of the file to be saved in S3.
            file_format (str): The format of the file ('csv' or 'json'). Default is 'csv'.
        """
        try:
            if file_format == 'csv':
                self.upload_csv(data, file_name)
            elif file_format == 'json':
                self.upload_json(data, file_name)
            else:
                raise ValueError("Unsupported file format. Use 'csv' or 'json'.")
        except Exception as e:
            logger.error(f"Failed to upload data to S3: {e}")
            raise

    def upload_csv(self, data: pd.DataFrame, file_name: str):
        """Upload DataFrame as a CSV file to S3."""
        csv_buffer = StringIO()
        data.to_csv(csv_buffer, index=False)
        self._upload_to_s3(csv_buffer.getvalue(), file_name)

    def upload_json(self, data: pd.DataFrame, file_name: str):
        """Upload DataFrame as a JSON file to S3."""
        json_buffer = StringIO()
        data.to_json(json_buffer, orient='records', lines=True)
        self._upload_to_s3(json_buffer.getvalue(), file_name)

    def _upload_to_s3(self, data: str, file_name: str):
        """Helper method to upload data to S3."""
        try:
            self.s3_client.put_object(Body=data, Bucket=self.bucket_name, Key=file_name)
            logger.info(f"Successfully uploaded {file_name} to {self.bucket_name}.")
        except ClientError as e:
            logger.error(f"Client error occurred: {e}")
            raise
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            raise

# Example usage
if __name__ == "__main__":
    # Sample DataFrame
    df = pd.DataFrame({
        'Column1': [1, 2, 3],
        'Column2': ['A', 'B', 'C']
    })

    bucket_name = 'your-bucket-name'
    file_name = 'data/sample_data.csv'

    uploader = S3Uploader(bucket_name)
    uploader.upload_data(df, file_name, file_format='csv')
