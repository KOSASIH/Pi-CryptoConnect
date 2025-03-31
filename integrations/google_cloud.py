import logging
import pandas as pd
from google.cloud import storage
from io import StringIO

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GCSUploader:
    """A class to handle uploading data to Google Cloud Storage."""

    def __init__(self, bucket_name: str):
        """Initialize the GCSUploader with the specified bucket name.

        Args:
            bucket_name (str): The name of the GCS bucket.
        """
        self.bucket_name = bucket_name
        self.client = storage.Client()

    def upload_data(self, data: pd.DataFrame, file_name: str, file_format: str = 'csv'):
        """
        Upload data to Google Cloud Storage.

        Args:
            data (pd.DataFrame): Pandas DataFrame with data.
            file_name (str): The name of the file to be saved in GCS.
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
            logger.error(f"Failed to upload data to GCS: {e}")
            raise

    def upload_csv(self, data: pd.DataFrame, file_name: str):
        """Upload DataFrame as a CSV file to GCS."""
        csv_buffer = StringIO()
        data.to_csv(csv_buffer, index=False)
        self._upload_to_gcs(csv_buffer.getvalue(), file_name, 'text/csv')

    def upload_json(self, data: pd.DataFrame, file_name: str):
        """Upload DataFrame as a JSON file to GCS."""
        json_buffer = StringIO()
        data.to_json(json_buffer, orient='records', lines=True)
        self._upload_to_gcs(json_buffer.getvalue(), file_name, 'application/json')

    def _upload_to_gcs(self, data: str, file_name: str, content_type: str):
        """Helper method to upload data to GCS."""
        try:
            bucket = self.client.bucket(self.bucket_name)
            blob = bucket.blob(file_name)
            blob.upload_from_string(data, content_type=content_type)
            logger.info(f"Successfully uploaded {file_name} to {self.bucket_name}.")
        except Exception as e:
            logger.error(f"An error occurred while uploading to GCS: {e}")
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

    uploader = GCSUploader(bucket_name)
    uploader.upload_data(df, file_name, file_format='csv')
