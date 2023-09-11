from behave import *


@given("a dwelling input table")
def load_dwelling_table(context):
    context.scenario.test_data.input_handler.add_table(context.table, "dwelling")
