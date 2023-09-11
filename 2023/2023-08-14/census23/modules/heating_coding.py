from typing import Dict, NewType

import pandas as pd
from modules.module_interface import ModuleInterface

Variable = NewType("Variable", str)
Data = Dict[str, pd.DataFrame]


DWELL_NBR = Variable("dwell_nbr")
D_HEATING_PREDEFINED = Variable("d_heating_predefined")
D_HEATING_TEXT = Variable("d_heating_text")
D_HEATING_CODE_ICS = Variable("d_heating_code_ics")
D_HEATING_PREDEFINED_CODE = Variable("d_heating_predefined_code")
D_HEATING_TEXT_CODE = Variable("d_heating_text_code")
D_HEAT_FUEL_SYNONYM = Variable("d_heat_fuel_synonym")
D_HEATING_TEXT_REMAINDER = Variable("d_heating_text_remainder")
D_HEATING_CODE_DATA_SOURCE = Variable("d_heating_code_data_source")
HEATING_CODES = Variable("_heating_codes")


class heating_coding(ModuleInterface):
    input_variables = {
        "dwelling": [
            DWELL_NBR,
            D_HEATING_PREDEFINED,
            D_HEATING_TEXT,
            D_HEATING_CODE_ICS,
        ]
    }

    output_variables = {
        "dwelling": [D_HEATING_PREDEFINED_CODE, D_HEATING_CODE_DATA_SOURCE]
    }

    predefined_dict = {
        "dont_use": "00",
        "heat_pump": "01",
        "electric_heater": "02",
        "fixed_gas_heater": "03",
        "portable_gas_heater": "04",
        "wood_burner": "05",
        "pellet_fire": "06",
        "coal_burner": "07",
        "other": "08",
    }

    def main(self, input_data: Data) -> Data:
        dwellings = input_data["dwelling"]

        # initialise output columns
        dwellings[
            [D_HEATING_TEXT_CODE, D_HEAT_FUEL_SYNONYM, D_HEATING_TEXT_REMAINDER]
        ] = ""

        # split input dataframe into predefined and other
        is_predefined = dwellings[D_HEATING_PREDEFINED] != ""
        predefined = dwellings[is_predefined]
        other = dwellings[~is_predefined]

        # split input values into lists
        predefined[HEATING_CODES] = predefined[D_HEATING_PREDEFINED].str.split(",")

        # explode the lists into rows
        predefined = predefined.explode(HEATING_CODES, ignore_index=False)

        # map to predefined codes dictionary
        predefined[HEATING_CODES] = predefined[HEATING_CODES].map(self.predefined_dict)

        # join the codes back into a semicolon separated string
        aggregate = predefined.groupby(DWELL_NBR, sort=False)[HEATING_CODES].agg(
            ";".join
        )

        # rename the column
        aggregate = aggregate.rename(D_HEATING_PREDEFINED_CODE)

        # drop duplicates
        predefined.drop_duplicates(subset=DWELL_NBR, inplace=True)

        # join the aggregated codes back into the predefined dataframe
        predefined.reset_index(inplace=True)

        # merge the aggregated codes back into the predefined dataframe
        predefined = predefined.merge(
            aggregate, on=DWELL_NBR, how="left", validate="1:1"
        )

        # set the original index back to the dataframe
        predefined.set_index("index", drop=True, inplace=True)
        predefined.index.name = None

        # join the predefined and other dataframes back together
        dwellings = pd.concat([predefined, other]).sort_index()

        # set data source
        dwellings[D_HEATING_CODE_DATA_SOURCE] = "11"

        dwellings.drop(
            columns=set(dwellings.columns) - set(self.output_variables["dwelling"]),
            inplace=True,
        )

        return {"dwelling": dwellings}
