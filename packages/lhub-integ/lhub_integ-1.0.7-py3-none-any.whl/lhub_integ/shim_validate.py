"""
Validation Shim for custom integrations
"""
import inspect
from traceback import format_exc
from docstring_parser import parse

import click

from lhub_integ import action, util, connection_validator
from lhub_integ.env import MappedColumnEnvVar
from lhub_integ.params import ConnectionParam, ActionParam, ValidationError
from lhub_integ.util import (
    exit_with_instantiation_errors,
    print_successful_validation_result,
)
from lhub_integ.execution import ExecutionType


@click.command()
@click.option("--entrypoint", "-e", required=False)
@click.option(
    "--validate-connections/--no-validate-connections",
    "check_connections",
    default=False,
)
def main(entrypoint, check_connections):
    validation_errors = []
    try:
        errors, _ = util.import_workdir()
        if errors:
            util.hard_exit_from_instantiation(f"Failed to parse integration: {errors}")

        if not validation_errors:
            if entrypoint is not None:
                validation_errors += validate_entrypoint(entrypoint)
            if check_connections:
                validation_errors += validate_connections()

        validation_errors = [v.to_json() for v in validation_errors]
    except Exception:
        util.hard_exit_from_instantiation(
            message=f"Unexpected exception: {format_exc()}"
        )

    if validation_errors:
        exit_with_instantiation_errors(
            1, validation_errors, message="Integration validation failed."
        )
    else:
        print_successful_validation_result()


def validate_param(param):
    if not param.valid():
        return [ValidationError(message="Parameter must be defined", param=param)]
    try:
        param.read()
    except Exception as ex:
        return [ValidationError(message=str(ex), param=param)]
    return []


def validate_connections():
    errors = []
    try:
        for var in ConnectionParam.all():
            errors += validate_param(var)
        if not errors and connection_validator.validator is not None:
            return normalize_validation_result(connection_validator.validator())
    except Exception as ex:
        util.print_error(str(ex))
        exit(1)

    return errors


def normalize_validation_result(res):
    if res is None:
        return []
    if not isinstance(res, list):
        util.hard_exit_from_instantiation(
            f"Validator functions must return a list of ValidationError (got {res})"
        )
    else:
        return res


def validate_entrypoint(entrypoint):
    module_name = ".".join(entrypoint.split(".")[:-1])
    function_name = entrypoint.split(".")[-1]

    if module_name == "" or function_name == "":
        util.hard_exit_from_instantiation(
            "Bad entrypoint format. `Expected filename.functionname`"
        )

    # Try to import the world and find the entrypoint

    action_object = action.all().get(entrypoint)
    method = action_object.function
    execution_type = action_object.execution_type
    if method is None:
        util.hard_exit_from_instantiation(
            f"No matching action found. Is your action annotated with @action?"
        )
    if not isinstance(execution_type, ExecutionType):
        util.hard_exit_from_instantiation(
            f"Unsupported `execution_type` {str(execution_type)}: {type(execution_type)}. Valid execution-types are: {ExecutionType.get_all_types()}"
        )

    errors = []

    # Read the arguments and environment variables we expect and make sure they've all been defined
    parsed = parse(method.__doc__)
    args, _, _ = inspect.getargs(method.__code__)

    if execution_type == ExecutionType.PROCESS_ONCE and len(args) > 0:
        util.hard_exit_from_instantiation(
            f"`execution_type`: {str(execution_type)} should not have column-args. If you want to execute action once, use ROWS_TO_PROCESS input-fields"
        )

    for arg in args:
        optional = None
        for meta in parsed.meta:
            if len(meta.args) == 2 and meta.args[0] == "optional" and meta.args[1] == arg:
                optional = meta.description.lower() != "false"
        param = MappedColumnEnvVar(arg, optional=optional)
        if not param.valid():
            errors.append(
                ValidationError(
                    message="Column name cannot be empty", param=param
                )
            )

    env_vars = list(ConnectionParam.all()) + list(ActionParam.for_action(action_object))
    for var in env_vars:
        errors += validate_param(var)

    if errors:
        return errors

    if action_object.validator is not None:
        try:
            return normalize_validation_result(action_object.validator())
        except Exception as ex:
            util.hard_exit_from_instantiation(str(ex))
    return []


if __name__ == "__main__":
    main()
