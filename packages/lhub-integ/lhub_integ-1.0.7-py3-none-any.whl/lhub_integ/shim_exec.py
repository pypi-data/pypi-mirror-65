"""
Wrap a custom Python script to enable it to work with the integration machinery

Loads ENTRYPOINT from `__ENTRYPOINT` and the column-argument mapping from `___XXXXX`

Usage:
This module is intended to be invoked by `PythonEnvironment`. See `test_shim.py` for a usage example

<set required environment variables> python -m lhub_integ.shim_exec -e <entrypoint>
"""
import json
import sys
import traceback

import click

from docstring_parser import parse

from lhub_integ import util, action, params
from lhub_integ.env import MappedColumnEnvVar
from lhub_integ.params import JinjaTemplatedStr
from lhub_integ.execution import ExecutionType


def _print_result_rows(result, lhub_id=None):
    # Print the results
    if result:
        if isinstance(result, list):
            util.print_each_result_in_list(result, lhub_id)
        else:
            util.print_result(json.dumps(result), lhub_id)


def run_integration(entrypoint_fn):
    type_mapper = params.get_input_converter(entrypoint_fn)

    annotations = util.type_annotations(entrypoint_fn)
    parsed = parse(entrypoint_fn.__doc__)
    # Build a mapping from the columns in the input data to the arguments in our integration
    argument_column_mapping = {}
    for input_argument in type_mapper:
        optional = False
        for meta in parsed.meta:
            if len(meta.args) == 2 and meta.args[0] == "optional" and meta.args[1] == input_argument:
                optional = meta.description.lower() != "false"

        input_value = MappedColumnEnvVar(input_argument, optional=optional).read()
        argument_column_mapping[input_argument] = input_value

    required_columns = {
        k: v
        for k, v in argument_column_mapping.items()
        if annotations.get(k) != JinjaTemplatedStr and v is not None
    }

    for row in sys.stdin.readlines():
        as_dict = json.loads(row)["row"]
        lhub_id = as_dict.get(util.LHUB_ID)
        missing_keys = required_columns.values() - as_dict.keys()
        for column in missing_keys:
            util.print_error(f"Column '{column}' is not present in the data")
        if missing_keys:
            continue
        try:

            # Load the arguments from the input
            def coerce(arg, column):
                try:
                    return type_mapper[arg](as_dict, column)
                except ValueError as ex:
                    util.print_error(
                        f"Invalid value for column {column}: [{ex}]", data=as_dict
                    )
                    raise EndOfLoop()

            arguments = {}
            for arg, column in argument_column_mapping.items():
                arguments[arg] = coerce(arg, column) if column is not None else column

            # Run the integration
            result = entrypoint_fn(**arguments)

            _print_result_rows(result, lhub_id)
        except EndOfLoop:
            pass
        except Exception:
            util.print_error(traceback.format_exc(), data=as_dict, original_lhub_id=lhub_id)


# Uncorrelated results. Used in actions that are `isDataSource`
def run_integration_once(entrypoint_fn):
    result = entrypoint_fn()
    _print_result_rows(result)


class EndOfLoop(Exception):
    pass


@click.command()
@click.option("--entrypoint", "-e", required=True)
def main(entrypoint):
    errors, _ = util.import_workdir()
    if errors:
        util.hard_exit_from_instantiation(str(errors[0]))
    entrypoint_fn = action.all().get(entrypoint).function
    execution_type = action.all().get(entrypoint).execution_type
    assert entrypoint_fn is not None
    if execution_type == ExecutionType.PROCESS_ONCE:
        run_integration_once(entrypoint_fn)
    else:
        run_integration(entrypoint_fn)


if __name__ == "__main__":
    main()
