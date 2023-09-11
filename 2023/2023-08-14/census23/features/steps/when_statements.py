from behave import *
from features.utilities.misc_functions import run_module_functional


@when("the {module} module is run")
def run_heating_coding_module(context, module):
    dataframes = context.scenario.test_data.input_handler.get_all_dataframes()
    context.scenario.test_data.outputs_to_verify = [
        {"input_variables": dataframes, "output": {}}
    ]
    full_dataframe_set = {**context.data, **dataframes}

    output = run_module_functional(full_dataframe_set, f"modules.{module}")

    for dataframe in output.keys():
        context.scenario.test_data.outputs_to_verify[0]["output"][dataframe] = output[
            dataframe
        ].to_dict("records")
