import logging
import uuid
import json
from datetime import datetime

logger = logging.getLogger("custom_json_logger")
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_date = datetime.utcnow().isoformat() + "Z"
        log_message = {
            'level': record.levelname.lower(),
            'timestamp': log_date,
            'request_id': str(uuid.uuid4()), 
            'message': record.getMessage(),
            'request': 'GET /',
            'user_agent': 'test',
            'event': 'request_started',
            'trace_id': '1-2-3',
            'user_id': "Chrome",
            'domain': 'test.com',
            'ip': '1.1.1.121',
            'logger': 'test.middlewares.request'
        }
        
        return json.dumps(log_message)

console_handler.setFormatter(JSONFormatter())
logger.addHandler(console_handler)

def handler(event, context):
    logger.info("This is a test log message with JSON formatter")
    return {
        'statusCode': 200,
        'body': 'Hello from Lambda!'
    }
