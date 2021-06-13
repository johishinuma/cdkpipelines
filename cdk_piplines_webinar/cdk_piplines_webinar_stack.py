from os import path
from aws_cdk import core as cdk
import aws_cdk.aws_lambda as lmd
import aws_cdk.aws_apigateway as apigw

# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core


class CdkPiplinesWebinarStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        this_dir = path.dirname(__file__)

        handler = lmd.Function(self, 'Handler',
            runtime=lmd.Runtime.PYTHON_3_7, 
            handler='handler.handler', 
            code=lmd.Code.from_asset(path.join(this_dir, 'lambda')))
        
        gw = apigw.LambdaRestApi(self, 'Gateway',
            description='Endpoint from a simple Lambda-powered web service',
            handler=handler.current_version)
        
        self.url_output = core.CfnOutput(self, 'Url',
            value=gw.url)
