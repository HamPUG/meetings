import importlib
import sys


def run_module_functional(data, module_path) -> dict:
    """Runs a module with provided data as a parameter"""
    importlib.import_module(f"{module_path}")

    module = sys.modules[module_path]
    module_class = getattr(module, module_path.split(".")[-1])

    # Instantiate the class
    module_instance = module_class()

    modified_data = fill_missing_input_variables_all(
        data, module_instance.get_inputs(), None
    )
    modified_data = module_instance.main_wrapped(modified_data)

    return modified_data


def fill_missing_input_variables_all(data, variables, default_value=""):
    result = {}
    for key in data.keys():
        if key in variables.keys():
            result[key] = fill_missing_input_variables(
                data[key], variables[key], default_value
            )
        else:
            result[key] = data[key]

    return result


def fill_missing_input_variables(data, variables, default_value):
    num_rows = len(data.index)
    for variable in variables:
        if variable not in data.keys():
            data[variable] = [default_value] * num_rows
    return data
