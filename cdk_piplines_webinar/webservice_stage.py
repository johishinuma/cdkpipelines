from aws_cdk import core

from .cdk_piplines_webinar_stack import CdkPiplinesWebinarStack

class WebServiceStage(core.Stage):
    
    def __init__(self, scope: core.Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)


        service = CdkPiplinesWebinarStack(self, 'WebSrvice')

        self.url_output = service.url_output



