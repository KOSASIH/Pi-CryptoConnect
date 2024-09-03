import boto3

def upload_data_to_s3(data, bucket_name, file_name):
    """
    Upload data to AWS S3.

    :param data: Pandas DataFrame with data
    :param bucket_name: S3 bucket name
    :param file_name: File name
    :return: None
    """
    s3 = boto3.client('s3')
    s3.put_object(Body=data.to_csv(index=False), Bucket=bucket_name, Key=file_name)
