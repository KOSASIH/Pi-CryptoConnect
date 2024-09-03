from google.cloud import storage

def upload_data_to_gcs(data, bucket_name, file_name):
    """
    Upload data to Google Cloud Storage.

    :param data: Pandas DataFrame with data
    :param bucket_name: GCS bucket name
    :param file_name: File name
    :return: None
    """
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(file_name)
    blob.upload_from_string(data.to_csv(index=False))
