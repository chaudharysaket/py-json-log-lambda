import logging
import json
import uuid
from datetime import datetime

# Define the JSON formatter class
class JSONFormatter(logging.Formatter):
    def format(self, record):

        log_message = {
            'level': record.levelname.lower(),
            'request_id': getattr(record, 'request_id', None) or str(uuid.uuid4()),  # Use request_id from log record if available
            'message': record.getMessage()
        }
        return json.dumps(log_message)


logger = logging.getLogger("custom_json_logger")
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
console_handler.setFormatter(JSONFormatter())
logger.addHandler(console_handler)

def lambda_handler(event, context):
    # Create a logger adapter to add custom attributes (requestId in this case)
    extra = {'request_id': context.aws_request_id}
    custom_logger = logging.LoggerAdapter(logger, extra)

    # Log a message with the custom attributes
    custom_logger.info("Lambda function started")

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
