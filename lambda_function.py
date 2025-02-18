import logging
import json
import uuid
from datetime import datetime

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_message = {
            'injected_request_id': getattr(record, 'request_id', None), 
            'message': record.getMessage()
        }
        return json.dumps(log_message)


logger = logging.getLogger("custom_json_logger")
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
console_handler.setFormatter(JSONFormatter())
logger.addHandler(console_handler)

def lambda_handler(event, context):

    injected_request_id = {'request_id': context.aws_request_id}
    custom_logger = logging.LoggerAdapter(logger, injected_request_id)


    custom_logger.info("Test nLambda Log")

    # Simulate some processing
    try:
        # Your processing logic here
        custom_logger.info("Processing succeeded")
    except Exception as e:
        custom_logger.error(f"Error occurred: {str(e)}")
        raise

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
