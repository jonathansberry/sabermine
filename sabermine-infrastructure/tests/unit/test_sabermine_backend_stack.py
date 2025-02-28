import aws_cdk as cdk
import aws_cdk.assertions as assertions
from stack import SabermineBackendStack


def test_lambda_function_created():
    app = cdk.App()
    stack = SabermineBackendStack(app, "TestStack")

    template = assertions.Template.from_stack(stack)

    # Check if a Lambda function is created
    template.resource_count_is("AWS::Lambda::Function", 1)

    # Verify Lambda properties
    template.has_resource_properties("AWS::Lambda::Function", {
        "Runtime": "python3.9",
        "Handler": "index.handler",
        "MemorySize": 512
    })


def test_api_gateway_created():
    app = cdk.App()
    stack = SabermineBackendStack(app, "TestStack")

    template = assertions.Template.from_stack(stack)

    # Check if an API Gateway is created
    template.resource_count_is("AWS::ApiGateway::RestApi", 1)

    # Verify API Gateway has a Lambda integration
    template.has_resource_properties("AWS::ApiGateway::Method", {
        "HttpMethod": "ANY",
        "Integration": {
            "IntegrationHttpMethod": "POST",
            "Type": "AWS_PROXY"
        }
    })
