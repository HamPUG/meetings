import pandas as pd
from behave.model import Table


class InputHandler(object):
    def __init__(self):
        self.raw_input_variables = {}

    def add_table(
        self,
        table: Table,
        dataframe: str,
    ):
        """Split a table input to fit into self.raw_input_variables using the column titles as keys"""
        dataframe_inputs = {}
        for index, variable_name in enumerate(table.headings):
            variable_range = [row[index] for row in table]
            dataframe_inputs[variable_name] = variable_range

        self.raw_input_variables[dataframe] = dataframe_inputs

    def get_all_dataframes(self):
        """Use raw_input_variables to turn all input variables associated with a dataframe into a pandas table"""
        dataframes = self.raw_input_variables.keys()
        dataframe_tables = {}
        for dataframe in dataframes:
            variables_in_dataframe = self.raw_input_variables[dataframe].keys()
            dataframe_tables[dataframe] = pd.DataFrame(
                self.raw_input_variables[dataframe], columns=variables_in_dataframe
            )

        if dataframe_tables == {}:
            raise Exception(f"No dataframes created.")
        return dataframe_tables
