from aws_cdk import (
    aws_lambda as lambda_,
    aws_apigateway as apigw,
    core,
)

class MeetupDemoStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create a Lambda from local source
        lambdaFn = lambda_.Function(
            self, "MeetupLambda",
            code=lambda_.Code.asset('lambda'),
            handler="lambda-handler.handler",
            timeout=core.Duration.seconds(300),
            runtime=lambda_.Runtime.PYTHON_3_7,
        )

        # Wrap it behind an API gateway instance
        apigw.LambdaRestApi(
            self, 'MeetupApiEndpoint',
            handler=lambdaFn,
        )
