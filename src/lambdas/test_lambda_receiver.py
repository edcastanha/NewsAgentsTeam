import json
import os
from unittest.mock import MagicMock, patch
import pytest
from django.core.exceptions import ValidationError

# Configure Django settings for testing
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Import the function to test after Django setup
from lambdas.lambda_receiver import lambda_handler, validate_news_data
from news_app.models import News

@pytest.fixture
def mock_sqs():
    with patch('lambdas.lambda_receiver.sqs') as mock:
        yield mock

def test_lambda_handler_success():
    event = {
        'Records': [
            {
                'body': json.dumps({
                    'title': 'Test Title',
                    'content': 'Test Content',
                    'source': 'Test Source',
                    'url': 'http://test.com',
                    'autor': 'Test Autor'
                })
            }
        ]
    }
    context = {}
    response = lambda_handler(event, context)
    assert response['statusCode'] == 200
    assert 'News data processed successfully' in json.loads(response['body'])['message']
    assert News.objects.count() == 1

def test_lambda_handler_invalid_json():
    event = {
        'Records': [
            {
                'body': 'invalid json'
            }
        ]
    }
    context = {}
    response = lambda_handler(event, context)
    assert response['statusCode'] == 400
    assert 'Invalid JSON format' in json.loads(response['body'])['error']
    assert News.objects.count() == 0

def test_lambda_handler_missing_fields():
    event = {
        'Records': [
            {
                'body': json.dumps({
                    'title': 'Test Title',
                    'content': 'Test Content',
                    'source': 'Test Source',
                    'url': 'http://test.com'
                })
            }
        ]
    }
    context = {}
    response = lambda_handler(event, context)
    assert response['statusCode'] == 400
    assert 'Missing required fields' in json.loads(response['body'])['error']
    assert News.objects.count() == 0

def test_validate_news_data_success():
    data = {
        'title': 'Test Title',
        'content': 'Test Content',
        'source': 'Test Source',
        'url': 'http://test.com',
        'autor': 'Test Autor'
    }
    validate_news_data(data)

def test_validate_news_data_missing_fields():
    data = {
        'title': 'Test Title',
        'content': 'Test Content',
        'source': 'Test Source',
        'url': 'http://test.com'
    }
    with pytest.raises(ValueError) as excinfo:
        validate_news_data(data)
    assert 'Missing required fields' in str(excinfo.value)

def test_validate_news_data_django_validation_error():
    data = {
        'title': '',  # Assuming title cannot be empty in the model
        'content': 'Test Content',
        'source': 'Test Source',
        'url': 'http://test.com',
        'autor': 'Test Autor'
    }
    with pytest.raises(ValidationError):
        validate_news_data(data)
