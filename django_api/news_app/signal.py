import json
import logging
import boto3
from django.conf import settings
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import News

logger = logging.getLogger(__name__)

@receiver(pre_save, sender=News)
def news_pre_save(sender, instance, **kwargs):
    """
    Signal receiver that sends news data to SQS before saving to the database.
    """
    if instance.pk is None:  # Check if it's a new object being created
        try:
            # Send the data to SQS
            sqs = boto3.client('sqs')
            queue_url = settings.SQS_QUEUE_URL
            news_data = {
                'title': instance.title,
                'content': instance.content,
                'source': instance.source,
                'url': instance.url,
                'autor': instance.autor
            }
            response = sqs.send_message(
                QueueUrl=queue_url,
                MessageBody=json.dumps(news_data)
            )

            logger.info(f"News data sent to SQS: {response}")

            # Prevent saving to the database
            raise Exception("News data sent to SQS, not saving to database.")

        except Exception as e:
            logger.error(f"Error sending news data to SQS: {e}")
            raise
