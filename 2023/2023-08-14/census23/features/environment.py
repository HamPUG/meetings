import pandas as pd

from features.utilities.scenario_data_container import ScenarioDataContainer


def before_all(context):
    # Return the full table in test output
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 0)


def before_scenario(context, scenario):
    context.data = {}
    context.scenario.test_data = ScenarioDataContainer()
