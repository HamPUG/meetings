#!/usr/bin/env python3
from aws_cdk import core as cdk
from aws_cdk import core

from meetup_demo.meetup_demo_stack import MeetupDemoStack

app = core.App()

MeetupDemoStack(app, "MeetupDemoStack",
    env=core.Environment(account='309865535433', region='us-west-1'),
    )

app.synth()
