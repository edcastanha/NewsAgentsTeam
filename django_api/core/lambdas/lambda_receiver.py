import json
import os
import django
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.wsgi import get_wsgi_application
import boto3
import logging

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
settings.configure()
django.setup()

# Import your models after Django setup
from news_app.models import News

# AWS SQS client
sqs = boto3.client('sqs')
QUEUE_URL = os.environ.get('SQS_QUEUE_URL')

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def validate_news_data(data):
    """
    Validates the news data format and content.

    Args:
        data (dict): The news data to validate.

    Raises:
        ValueError: If required fields are missing.
        ValidationError: If Django model validation fails.
    """
    required_fields = ['title', 'content', 'source', 'url', 'autor']
    if not all(key in data for key in required_fields):
        raise ValueError(f"Missing required fields: {', '.join(required_fields)}")

    news = News(**data)
    news.full_clean()  # This will raise ValidationError if validation fails
    return news

def lambda_handler(event, context):
    """
    Lambda function to receive messages from SQS,
    validate the JSON format, and process the news data.
    """
    try:
        logger.info(f"Event received: {event}")

        # Process each message in the event
        for record in event['Records']:
            body = json.loads(record['body'])
            logger.info(f"Message body: {body}")

            # Validate the JSON format and content
            news = validate_news_data(body)

            # Process the news data (e.g., save to database, etc.)
            news.save()
            logger.info(f"News data processed successfully")

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'News data processed successfully'})
        }

    except json.JSONDecodeError:
        logger.error("Invalid JSON format")
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid JSON format'})
        }
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        return {
            'statusCode': 400,
            'body': json.dumps({'error': str(e)})
        }
    except ValidationError as e:
        logger.error(f"Django model validation error: {e}")
        return {
            'statusCode': 400,
            'body': json.dumps({'error': str(e)})
        }
    except Exception as err_msg:
        logger.error(f"Unexpected error: {err_msg}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(err_msg)})
        }
