import json
import logging

#----------------------------------------
# function to check if file exists in s3
#----------------------------------------
def object_exists(s3, bucket, key):
    
    logger = logging.getLogger()
    logger.setLevel("INFO")
    
    try:
        s3.head_object(Bucket=bucket, Key=key)
        logger.info(f'{key} file exists in {bucket} bucket')
        return True
    except s3.exceptions.ClientError as e:
        if e.response['Error']['Code'] == '404':
            return False
        else:
            logger.exception(f'Error processing head_object process: {str(e)}')
            return False

#------------------------------------------
# functions to manage response accordingly
#------------------------------------------
def success_response(status_code, message):
    return {'statusCode': status_code, 'body': json.dumps(message)}

def error_response(status_code, message):
    return {'statusCode': status_code, 'body': json.dumps(f'Error: {message}')}
