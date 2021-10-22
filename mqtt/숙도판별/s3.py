import boto3
import botocore

BUCKET_NAME = 'tomato-growth-images' # replace with your bucket name

s3 = boto3.resource('s3')

def download(KEY):
    try:
        s3.Bucket(BUCKET_NAME).download_file(KEY, 'image.jpg')
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise
