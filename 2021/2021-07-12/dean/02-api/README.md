
# AWS CDK Python project demo

This is an introductory CDK project presented to the Hamilton Python Meetup group on 12/Jul/2021 demonstrating how to deploy a simple architecture comprised of..

`Api Gateway -> Lambda -> Dynamodb`

Where the stack is defined using Python and the Python Lambda itself reaches out to an external API to source some data to be stored in the Dynamodb table. This repo has a set of branches progressively introducing each of the components. The process you should follow for each is..

 * `git checkout <branchname>`
 * `cdk diff`        compare deployed stack with current state
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * inspect the assets created or updated in your account

## Branch notes

__00-init__

Some of the standard boilerplate has been weeded out but this is essentially what is created after a call to..

```
cdk init app --language python
```

In this state there are no resources to deploy, however you can list the stack itself from the CLI using..

```
cdk ls
```

__01-lambda__

Adds a Python Lambda function that makes a call out to an external airport weather conditions API to fetch some data using an event property specifying an airport location we want the report for. The source of the Lambda itself can be found in `/lambda` and is packaged up as a ZIP file and uploaded to a new S3 bucket for deployment

You will first need to create the 'bootstrap' Stack which sets up an S3 bucket to be used for storing our Lambda source code during deployment..

```
cdk bootstrap
```

And then actually deploy the Lambda using..

```
cdk diff
cdk deploy
```

After deployment you can test invoke the Lambda in the AWS UI or call it from the AWS CLI with a base64 encoded JSON request payload as per the following and check the contents of result.txt..

```
aws lambda invoke --function-name "<FUNCTION-NAME-HERE>" \
  --payload $(echo '{ "icao": "NZHN" }'|base64) ./result.txt
```

You can retrieve the function name using the AWS CLI like this

```
aws lambda list-functions --query "Functions[*].FunctionName"
```

There should only be one entry with a name like _MeetupDemoStack-MeetupLambda-[some-guid-here]_

For help on using the CLI with Lambdas see:
https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-awscli.html

__02-api__

Adds an API gateway referencing the Lambda in proxy mode. If you inspect the Lambda source now you will see it has been altered to check for a specific API resource path '/metar' and to check we have a querystring property in the right format. If so it makes the same external call it did before but now returns a JSON response in the format expected by the API gateway.

Do the usual diff and deploy now to see it in action.

For more background on the input and output formats expected when using a Lambda with the proxy intergration approach with API gateway see: 

https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html

__03-dynamodb__

This final step creates a Dynamodb table and alters the Lambda to save to it. The stack itself also grants access for the Lambda to be able to read/write to the table and passes the name of the created table to the Lambda so we dont have to hard code it.

Deploy the Stack changes in the usual way and invoke the API as usual and now you should see a new entry added to the Dynamodb table.

## Cleaning up

At any time you can run `cdk destroy` to dispose of the assets so you wont be charged for their storage or use.

## Useful resources

* Installing, updating, and uninstalling the AWS CLI v2 
  https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html
* Python CDK API docs
   https://docs.aws.amazon.com/cdk/api/latest/python/
* aws-cdk examples (including Python)
  https://github.com/aws-samples/aws-cdk-examples/tree/master/python
* CDK Python workshop
  https://cdkworkshop.com/30-python.html
* JSii : Framework for building language bindings between JS and others
   https://github.com/aws/jsii

___
The following sections are part of the standard CDK init skeleton output
___

## AWS background info

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization process also creates a virtualenv within this project, stored under the `.venv` directory.  To create the virtualenv it assumes that there is a `python3` (or `python` for Windows) executable in your path with access to the `venv` package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.

To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation



Enjoy!
Dean Stringer (dean@jumpflex.co.nz)
