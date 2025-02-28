import random
import string
import boto3
import os
from fastapi import File

AWS_REGION = os.getenv("AWS_REGION", "eu-west-1")
DYNAMODB_TABLE = os.getenv("DYNAMODB_TABLE", "ShortenedURLs")
S3_BUCKET = os.getenv("S3_BUCKET", "sabermine")
BASE_URL = os.getenv("BASE_URL", "https://5bqey8zso9.execute-api.eu-west-1.amazonaws.com/prod/")


def url_from_code(short_code: str):
    return f"{BASE_URL}/{short_code}"


def shorten_url(original_url: str) -> str:
    short_code = generate_unique_code()
    table = get_dynamodb_table()
    table.put_item(Item={"short_code": short_code, "original_url": original_url})
    return url_from_code(short_code)


def retrieve_url(short_code: str) -> str | None:
    table = get_dynamodb_table()
    response = table.get_item(Key={"short_code": short_code})
    if "Item" not in response:
        return None
    return response["Item"].get("original_url")


def generate_short_code(length=7) -> str:
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def get_dynamodb_table():
    dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
    table = dynamodb.Table(DYNAMODB_TABLE)
    return table


def get_s3_bucket():
    s3 = boto3.resource("s3", region_name=AWS_REGION)
    bucket = s3.Bucket(S3_BUCKET)
    return bucket


def is_code_unique(code: str) -> bool:
    table = get_dynamodb_table()
    response = table.get_item(Key={"short_code": code})
    return "Item" not in response


def generate_unique_code() -> str:
    while True:
        code = generate_short_code()
        if is_code_unique(code):
            return code


def upload_file(file: File) -> str:
    bucket = get_s3_bucket()
    bucket.upload_fileobj(file.file, file.filename)
    file_url = f"https://{bucket.name}.s3.{AWS_REGION}.amazonaws.com/{file.filename}"
    return file_url


def get_all_short_urls(limit: int = 10, last_evaluated_key: str = None):
    scan_kwargs = {"Limit": limit}
    if last_evaluated_key:
        scan_kwargs["ExclusiveStartKey"] = {"short_code": last_evaluated_key}
    table = get_dynamodb_table()
    response = table.scan(**scan_kwargs)
    items = response.get("Items", [])
    urls = [
        {**item, 'short_url': url_from_code(item['short_code'])} for item in items
    ]
    next_key = response.get("LastEvaluatedKey")
    return {
        "count": len(urls),
        "short_urls": urls,
        "next_key": next_key.get("short_code") if next_key else None  # Send next key if available
    }
