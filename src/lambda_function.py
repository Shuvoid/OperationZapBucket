import boto3
import gzip
import logging
from utilities import object_exists, success_response, error_response

#-------------------------------------------
#lambda handler function
#-------------------------------------------
def lambda_handler(event, context):
    
    logger = logging.getLogger()
    logger.setLevel("INFO")
    
    try:
        # Get the S3 bucket and object key from the event
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']
        
        # removing the file ext
        fileName = key.rstrip(".json") 
        
        # inititalize s3 client
        s3 = boto3.client('s3')

        # Download the original object from S3
        download_path = f'/tmp/{key}'
        s3.download_file(bucket, key, download_path)
        logger.info(f'Downloaded {key} from S3 to {download_path}')

        # Start compressing the json file
        zip_path = f'/tmp/{fileName}.zip'
        with open(download_path, 'rb') as f_in, gzip.open(zip_path, 'wb') as f_out:
            f_out.writelines(f_in)
        logger.info(f'Created ZIP file {zip_path}')

        # Upload the zipped file back to the same S3 bucket
        zip_key = f'{fileName}.zip'
        s3.upload_file(zip_path, bucket, zip_key)
        logger.info(f'Uploaded ZIP file {zip_path} to S3 with key {zip_key}')

        # Check if the ZIP file exists in S3 before deleting the original JSON file
        if object_exists(s3, bucket, zip_key):
            # Delete the original object from the S3 bucket
            s3.delete_object(Bucket=bucket, Key=key)
            logger.info(f'Deleted original JSON file {key} from {bucket}')

            return success_response(200,'Object has been compressed and uploaded successfully!')
        else:
            logger.error(f'ZIP file {zip_key} not found in S3!')
            return error_response(404,'ZIP file not found in S3!')

    except Exception as e:
        logger.exception(f'Error processing event: {str(e)}')
        return error_response(int(e.response['Error']['Code']), str(e))

