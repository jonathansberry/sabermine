import pytest
from moto import mock_aws
import boto3
from sabermine_backend.api.logic import DYNAMODB_TABLE, AWS_REGION, S3_BUCKET


@pytest.fixture
def dynamodb_mock():
    """Set up a mock DynamoDB table before each test."""
    with mock_aws():
        dynamodb_client = boto3.client("dynamodb", region_name=AWS_REGION)
        dynamodb_client.create_table(
            TableName=DYNAMODB_TABLE,
            KeySchema=[{"AttributeName": "short_code", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "short_code", "AttributeType": "S"}],
            BillingMode="PAY_PER_REQUEST",
        )
        dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
        yield dynamodb.Table("ShortenedURLs")


@pytest.fixture
def s3_mock():
    """Set up a mock S3 bucket before each test."""
    with mock_aws():
        s3_client = boto3.client("s3", region_name=AWS_REGION)
        s3_client.create_bucket(
            Bucket=S3_BUCKET,
            CreateBucketConfiguration={"LocationConstraint": AWS_REGION},
        )
        s3 = boto3.resource("s3", region_name=AWS_REGION)
        yield s3.Bucket(S3_BUCKET)
