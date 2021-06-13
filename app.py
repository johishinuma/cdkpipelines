#!/usr/bin/env python3
from aws_cdk import core

from cdk_piplines_webinar.cdk_piplines_webinar_stack import CdkPiplinesWebinarStack
from cdk_piplines_webinar.pipeline_stack import PipelineStack


app = core.App()

PipelineStack(app, 'PipelineStack', env={
  'account': '652846672077',
  'region': 'ap-northeast-1',
})

app.synth()
