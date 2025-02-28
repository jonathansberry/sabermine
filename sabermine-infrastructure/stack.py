from aws_cdk import (
    Stack,
    RemovalPolicy,
    Duration,
    aws_lambda as _lambda,
    aws_apigateway as apigateway,
    aws_dynamodb as dynamodb,
    aws_s3 as s3
)
from aws_cdk.aws_lambda_python_alpha import PythonFunction
from constructs import Construct


class SabermineBackendStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        table = dynamodb.Table(
            self, "SabermineDynamoDBTable",
            partition_key=dynamodb.Attribute(name="short_code", type=dynamodb.AttributeType.STRING),
            removal_policy=RemovalPolicy.DESTROY  # Probably should RETAIN in production
        )

        bucket = s3.Bucket(
            self, "SabermineS3Bucket",
            removal_policy=RemovalPolicy.DESTROY,  # Probably should RETAIN in production
            auto_delete_objects=True
        )

        lambda_function = PythonFunction(
            self, "SabermineBackendLambda",
            entry="../sabermine-backend/lambda_function",
            handler="handler",
            runtime=_lambda.Runtime.PYTHON_3_12,
            environment={
                "DYNAMODB_TABLE": table.table_name,
                "S3_BUCKET": bucket.bucket_name
            },
            timeout=Duration.seconds(10)
        )

        table.grant_read_write_data(lambda_function)
        bucket.grant_read_write(lambda_function)

        api = apigateway.LambdaRestApi(
            self, "SabermineBackendEndpoint",
            handler=lambda_function,
        )

        # TODO: Add the API Gateway URL to lambda function environment
