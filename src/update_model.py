import os
import zipfile
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv
load_dotenv()


AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION_NAME = 'us-west-1'

# Zip the contents of a directory
def zipdir(path, ziph):
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file), 
                       os.path.relpath(os.path.join(root, file), 
                                       os.path.join(path, '..')))

# Upload file to s3.
def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION_NAME
    )
    
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def update_model():
    # look into serving directory which is defined in the var folder and find the newest model
    folder = "model_output"
    sub_folders = [name for name in os.listdir(folder) if os.path.isdir(os.path.join(folder, name))]
    latest = sub_folders[0]
    for sub_folder in sub_folders:
        if int(sub_folder) > int(latest):
            latest = sub_folder
    
    latest_dir = os.path.join(folder, latest)
    # Zip the newest model directory and upload via s3.
    with zipfile.ZipFile('tmp/model.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipdir(latest_dir, zipf)
        upload_file('tmp/model.zip', 'jokedetection', object_name='model.zip')

if __name__ == '__main__':
    update_model()