from aws_cdk import (
    aws_lambda,
    aws_apigateway,
    aws_dynamodb,
    core,
)

class MeetupDemoStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # create dynamodb table
        meetup_table = aws_dynamodb.Table(
            self, "MeetupTable",
            partition_key=aws_dynamodb.Attribute(
                name="icao",
                type=aws_dynamodb.AttributeType.STRING
            )
        )

        # Create a Lambda from local source
        lambda_func = aws_lambda.Function(
            self, "MeetupLambda",
            code=aws_lambda.Code.asset('lambda'),
            handler="lambda-handler.handler",
            timeout=core.Duration.seconds(300),
            runtime=aws_lambda.Runtime.PYTHON_3_7,
        )

        lambda_func.add_environment("TABLE_NAME", meetup_table.table_name)

        # grant permission to lambda to write to demo table
        meetup_table.grant_write_data(lambda_func)

        # Wrap it behind an API gateway instance
        aws_apigateway.LambdaRestApi(
            self, 'MeetupApiEndpoint',
            handler=lambda_func,
        )
