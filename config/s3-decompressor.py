import boto3
import glob
import logging
from pathlib import Path
import sys
import tarfile

def lambda_handler(event, context):
    configure_logger()
    logger = get_logger()

    s3_bucket = event['Records'][0]['s3']['bucket']['name']
    s3_key = event['Records'][0]['s3']['object']['key']

    zipfile_output_dir = "/tmp/"

    zipfile_name = Path(s3_key).with_suffix('').stem
    zipfile_ext = ''.join(Path(s3_key).suffixes)
    zipfile = zipfile_output_dir + zipfile_name + zipfile_ext

    file_input_path = Path(s3_key).parent.as_posix()
    file_output_path = file_input_path.replace("input", "output") + '/'

    download_file(s3_bucket, s3_key, zipfile)
    extract_files(zipfile, zipfile_output_dir)
    upload_files(zipfile_output_dir + zipfile_name, s3_bucket, file_output_path)

    logger.info("Process completed successfully.")

def configure_logger():
    logger = logging.getLogger('s3-decompressor')
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

def get_logger():
    return logging.getLogger('s3-decompressor')

def download_file(s3_bucket, s3_key, output):
    logger = get_logger()
    try:
        s3 = boto3.resource('s3')
        s3.meta.client.download_file(s3_bucket, s3_key, output)
    except Exception as e:
        logger.error(f"There was a problem downloading the file '{s3_key}' from S3 bucket '{s3_bucket}. Exception Message: {e}")
        sys.exit(1)

    logger.info(f"S3 file '{s3_key}' has been downloaded to '{output}'.")

def extract_files(zipfile, output_dir):
    logger = get_logger()
    try:
        tar = tarfile.open(zipfile, "r:gz")
        tar.extractall(path=output_dir)
    except Exception as e:
        logger.error(f"File '{zipfile}' may be corrupt, cannot extract contents from tarfile. Exception Message: {e}")
        sys.exit(1)

    logger.info(f"Files have been extracted to '{output_dir}' directory.")
    tar.close()

def upload_files(zipfile_output_dir, s3_bucket, path):
    logger = get_logger()
    file_list = glob.glob(f'{zipfile_output_dir}/*.log')

    s3 = boto3.resource('s3')
    failed_uploads = 0
    for file in file_list:
        file_name = Path(file).name
        try:
            s3.meta.client.upload_file(file, s3_bucket, path + file_name)
        except Exception as e:
            logger.warning(f"An error occurred when attempting to upload '{file}' to S3. Exception Message: {e}")
            failed_uploads += 1
        else:
            full_s3_filepath = "s3://" + s3_bucket + "/" + path + file_name
            logger.info(f"File uploaded: '{full_s3_filepath}'")

    
    if failed_uploads > 0:
        logger.error(f"S3 upload failed for {failed_uploads} file(s).")
        sys.exit(1)
