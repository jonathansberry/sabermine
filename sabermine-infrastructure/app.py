#!/usr/bin/env python3
import aws_cdk as cdk
from stack import SabermineBackendStack

app = cdk.App()
SabermineBackendStack(app, "SabermineBackendStack")
app.synth()
