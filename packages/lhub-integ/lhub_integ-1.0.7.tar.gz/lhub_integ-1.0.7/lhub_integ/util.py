from __future__ import print_function

import fileinput
import importlib
import inspect
import json
import sys
from pathlib import Path
from typing import List, Tuple


LHUB_ID = "lhub_id"


def read_all_data():
    """
    If an argument is provided, fileinput.input() will iterate over the lines in that file. Otherwise, it will
    read from stdin. See https://docs.python.org/3/library/fileinput.html
    :return:
    """
    return fileinput.input()


def hard_exit_from_instantiation(message):
    exit_with_instantiation_errors(2, [], message)


def exit_with_instantiation_errors(
    code, errors, message="Integration validation failed."
):
    error_wrapper = {"errors": errors, "message": message}
    print(f"[result] {json.dumps(error_wrapper)}", file=sys.stderr)
    sys.exit(code)


def invalid_integration(code, error):
    raise InvalidIntegration(code, error)


def print_error(message: str, data=None, original_lhub_id=None):
    error = {"has_error": True, "error": message, "data": data}
    print_result(json.dumps(error), original_lhub_id)


def print_result(msg, original_lhub_id=None):
    if original_lhub_id is not None:
        print_correlated_result(msg, original_lhub_id)
    else:
        print(f"[result] {msg}")


def print_correlated_result(msg, original_lhub_id):
    meta_data_dict = {"original_lhub_id": original_lhub_id}
    meta_json = json.dumps(meta_data_dict)
    print(f"[result][meta]{meta_json}[/meta] {msg}")


def print_successful_validation_result():
    print_result("{}")


def print_each_result_in_list(results, original_lhub_id=None):
    if not results:
        return print_result(
            json.dumps({"noResults": "no results returned"}),
            original_lhub_id=original_lhub_id,
        )
    for result in results:
        print_result(json.dumps(result), original_lhub_id=original_lhub_id)


def import_workdir() -> Tuple[List[Exception], List[str]]:
    """
    Attempt to import all the files in the working directory
    :return: A list of errors
    """
    errors = []
    docstrings = []
    for file in Path(".").iterdir():
        if file.suffix == ".py":
            as_module = file.name[: -len(".py")]
            if "." in as_module:
                errors.append(f"Python files cannot contain dots: {as_module}")
                continue
            try:
                module = importlib.import_module(as_module)
                doc = module.__doc__
                if doc:
                    docstrings.append(doc)
            except Exception as ex:
                errors.append(ex)
    return errors, docstrings


def get_entrypoint_fn(entrypoint):
    module_name = ".".join(entrypoint.split(".")[:-1])
    function_name = entrypoint.split(".")[-1]
    module = importlib.import_module(module_name)
    return getattr(module, function_name)


def get_module_docstring(entrypoint):
    module_name = ".".join(entrypoint.split(".")[:-1])
    module = importlib.import_module(module_name)
    if module.__doc__:
        return module.__doc__.strip()
    return None


def type_annotations(fn):
    sig = inspect.signature(fn)
    return {param: sig.parameters[param].annotation for param in sig.parameters}


def deser_output(output: str):
    prefix = "[result]"
    processed = ""
    for line in output.splitlines():
        if line.startswith(prefix):
            processed += line[len(prefix) :]
    try:
        return json.loads(processed)
    except json.decoder.JSONDecodeError:
        raise Exception(f"Could not parse JSON: {output}")


class InvalidIntegration(Exception):
    def __init__(self, key, message):
        super().__init__(f"{message} [{key}]")
