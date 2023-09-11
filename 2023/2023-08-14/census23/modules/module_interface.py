import abc
import pandas as pd
import copy
import logging
from typing import Dict

log = logging.getLogger(__name__)

Data = Dict[str, pd.DataFrame]


class ModuleInterface(abc.ABC):
    """Base class for processing modules."""

    @property
    @abc.abstractmethod
    def input_variables(self):
        pass

    @property
    @abc.abstractmethod
    def output_variables(self):
        pass

    @abc.abstractmethod
    def main(self, data: Data) -> Data:
        pass

    def get_inputs(self):
        return copy.deepcopy(self.input_variables)

    def get_outputs(self):
        return copy.deepcopy(self.output_variables)

    def get_selected_data(self, data: Data) -> Data:
        """Get the data required for this processing module"""
        data_selected = {}
        input_keys = self.get_inputs().keys()
        data_selected = {
            key: data[key][list(self.get_inputs()[key])]
            for key in input_keys
            if key in data
        }
        return data_selected

    def combine_data(self, data: Data, output: Data, key: str) -> pd.DataFrame:
        """Combine data returned from the processing module with all the data"""
        out_cols = list(self.get_outputs()[key])
        log.debug(f"{out_cols=}")

        # Take the columns from 'output' that are declared as outputs
        data_output = output[key][out_cols]
        log.debug(f"{data_output.columns=}")
        log.debug(f"{data_output.shape=}")
        log.debug(f"{data_output.index=}")

        # Columns from the current 'data' to keep.
        remaining_columns = [
            column for column in data[key].columns if column not in out_cols
        ]
        log.debug(f"{remaining_columns=}")

        # Create a new dataframe with only the remaining columns
        data_to_join = data[key][remaining_columns]
        log.debug(f"{data_to_join.columns=}")
        log.debug(f"{data_to_join.shape=}")
        log.debug(f"{data_to_join.index=}")

        # Join the remainder columns to the module output
        result = data_output.join(data_to_join)
        log.debug(f"{result.columns=}")
        log.debug(f"{result.shape=}")
        log.debug(f"{result.index=}")

        return result

    def main_wrapped(self, data: Data) -> Data:
        data_selected = self.get_selected_data(data)
        data_output_dict = self.main(data_selected)

        data_combined = {}
        for key in data.keys():
            if key in self.get_outputs().keys():
                data_combined[key] = self.combine_data(data, data_output_dict, key)
            else:
                data_combined[key] = data[key]
        return data_combined
