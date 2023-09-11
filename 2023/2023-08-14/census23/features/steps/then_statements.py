from behave import *
import pandas as pd
from pandas._testing import assert_frame_equal


def assert_equal(expected, actual):
    try:
        assert_frame_equal(expected.sort_index(axis=1), actual.sort_index(axis=1))
    except AssertionError:
        print("Expected =\n\n", expected)
        print("\nActual =\n\n", actual)
        raise


@then("the subset of output {table} table is")
def verify_table_subset_against_outputs(context, table):
    expected = pd.DataFrame(context.table, columns=context.table.headings).astype(str)
    row_output_data = {}
    output_data = []

    for row in context.scenario.test_data.outputs_to_verify[0]["output"][table]:
        [
            row_output_data.update({variable: row[variable]})
            for variable in expected.columns
        ]
        output_data.append(row_output_data)
        row_output_data = {}

    actual = pd.DataFrame(output_data)
    assert_equal(expected, actual)
