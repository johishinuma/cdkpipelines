from aws_cdk import core
from aws_cdk import aws_codepipeline as codepipline
from aws_cdk import aws_codepipeline_actions as cpactions
from aws_cdk import pipelines

from .webservice_stage import WebServiceStage

class PipelineStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)


        source_artifact = codepipline.Artifact()
        cloud_assembly_artifact = codepipline.Artifact()


        pipeline = pipelines.CdkPipeline(self, 'Piplines',
            cloud_assembly_artifact=cloud_assembly_artifact,
            pipeline_name='WebinaerPipline',
            source_action=cpactions.GitHubSourceAction(
                action_name='Github',
                output=source_artifact,
                oauth_token=core.SecretValue.secrets_manager('github-token2'),
                owner='johishinuma',
                repo='cdkpipelines',
                trigger=cpactions.GitHubTrigger.POLL),
            synth_action=pipelines.SimpleSynthAction(
                source_artifact=source_artifact,
                cloud_assembly_artifact=cloud_assembly_artifact,
                install_command='npm install -g aws-cdk && pip install -r requirements.txt',
                build_command='pytest unittests',
                synth_command='cdk synth')

                )


        pre_prod_app = WebServiceStage(self, 'Pre-prod', env= {
            'account': '652846672077',
            'region': 'ap-northeast-1',
        })
            
        pre_prod_stage = pipeline.add_application_stage(pre_prod_app)

        pre_prod_stage.add_actions(pipelines.ShellScriptAction(
            action_name='Integ',
            run_order=pre_prod_stage.next_sequential_run_order(),
            additional_artifacts=[source_artifact],
            commands=[
                'pip install -r requirements.txt',
                'pytest integtests',
            ],
            use_outputs={
                'SERVICE_URL': pipeline.stack_output(pre_prod_app.url_output)
            }
        ))

        pipeline.add_application_stage(WebServiceStage(self, 'Prod', env= {
            'account': '652846672077',
            'region': 'ap-northeast-1',
        }))





