import inspect
import json
import re
from abc import ABCMeta
from collections import defaultdict
from typing import NamedTuple, Dict, Callable, Any

from lhub_integ import util
from lhub_integ.decorators import action as action_decorator
from lhub_integ.env import __EnvVar
from jinja2 import Template

from enum import Enum

ENV_VAR_NAME_REGEX = r"^[a-zA-Z_]\w*$"

TRUTHY = {"y", "true", "yes", "1"}
FALSY = {"n", "false", "no", "0"}


# pulled from forms.model.DataType
class DataType(Enum):
    STRING = "string"
    COLUMN = "column"
    NUMBER = "number"
    # no node datatype because integrations can only pull from one node

    # Unsupported by UI but validated by custom integrations
    BOOL = "bool"
    INT = "int"
    JSON = "json"
    JINJA = "jinja"

    def coerce(self, inp):
        if self == self.NUMBER:
            return float(inp)
        elif self == self.INT:
            return int(float(inp))
        elif self == self.BOOL:
            if isinstance(inp, bool):
                return inp
            if inp.lower() in TRUTHY:
                return True
            if inp.lower() in FALSY:
                return False
            raise ValueError(
                "Expected boolean input but {input} could not be coerced into a boolean value"
            )
        elif self == self.JSON:
            if isinstance(inp, dict):
                return inp
            return json.loads(inp)
        else:
            return inp


# pulled from forms.model.InputType
class InputType(Enum):
    TEXT = "text"
    TEXT_AREA = "textarea"
    EMAIL = "email"
    PASSWORD = "password"
    SELECT = "select"
    COLUMN_SELECT = "columnSelect"


class __Param(__EnvVar, metaclass=ABCMeta):
    def __init__(
            self,
            id,
            description=None,
            label=None,
            default=None,
            optional=False,
            options=None,
            data_type=DataType.STRING,
            input_type=InputType.TEXT,
    ):

        self.validate_id(id)
        super().__init__(id, default, optional)
        if label:
            self.label = label
        else:
            self.label = id
        self.description = description
        self.default = default
        self.data_type = data_type
        self.options = options
        if data_type == DataType.COLUMN:
            self.input_type = InputType.InputType.COLUMN_SELECT
        elif options is not None and len(options) > 1:
            self.input_type = InputType.SELECT
        else:
            self.input_type = input_type

    @staticmethod
    def validate_id(param_id: str):
        if re.match(ENV_VAR_NAME_REGEX, param_id) is None:
            util.invalid_integration(
                "invalid_parameter_name",
                f'"{param_id}" is not a valid id for a parameter. '
                f'Parameters must match `{ENV_VAR_NAME_REGEX}`. '
                'Use label to specify a custom display name',
            )

    def read(self):
        raw = super().read()
        return self.data_type.coerce(raw)


class JinjaTemplatedStr(str):
    @classmethod
    def input_type(cls) -> InputType:
        return InputType.TEXT_AREA

    @classmethod
    def data_type(cls) -> DataType:
        return DataType.JINJA


"""
We take most of the param information from our Form.Input case class. 
We don't enable a dependsOn field because if the dataType is a column then it will auto depends on its parent. 
"""


class ConnectionParam(__Param, metaclass=ABCMeta):
    """
    ConnectionParam provides a parameter specified by the connection

    Example usage:

    API_KEY = ConnectionParam('api_key')
    def process_row(url):
      requests.get(url, params={api_key: API_KEY.get()})
    """

    # LHUB-7385: Using simply a list here to preserve insertion order
    # list will suffice as we do check for duplicate connection-param id
    _all = []

    def __init__(self, *args, **kwargs):
        from lhub_integ import util

        super().__init__(*args, **kwargs)
        for conn_param in self._all:
            if conn_param.id == self.id:
                util.invalid_integration(
                    "duplication_connection_param",
                    f"You can't have 2 connection parameters with the same id ({self.id})",
                )
        self._all.append(self)

    @classmethod
    def all(cls):
        return cls._all


class ActionParam(__Param, metaclass=ABCMeta):
    """
    ActionParam provides a parameter specified by the action

    Example usage:

    API_KEY = ActionParam('api_key', action='process_row')

    import requests
    def process_row(url):
      requests.get(url, params={api_key: API_KEY.get()})
    """

    # LHUB-7385: defaultdict uses dict, so insertion order will be preserved. Also, changed from set to list to
    # preserve order of parameters. Since, we do have a duplicate check for action_parameters, this should be a safe
    # change.
    action_map = defaultdict(list)

    def __init__(self, *args, action, **kwargs):
        super().__init__(*args, **kwargs)
        from lhub_integ import util

        caller = inspect.currentframe().f_back
        if type(action) in (list, tuple):
            actions = action
        elif type(action) is str:
            actions = [action_str.strip() for action_str in action.split(',')]
        else:
            raise TypeError("'action' argument can be one of 'list', 'tuple' or 'str' only.")
        for action_str in actions:
            entrypoint = f"{caller.f_globals['__name__']}.{action_str}"
            if entrypoint in self.action_map:
                for action_param in self.action_map[entrypoint]:
                    if action_param.id == self.id:
                        util.invalid_integration(
                            "duplicate_action_param",
                            f"You can't have 2 action parameters with the same id ({action_str})",
                        )
            self.action_map[entrypoint].append(self)

    @classmethod
    def for_action(cls, action: action_decorator):
        return cls.action_map[action.entrypoint]


class ValidationError(NamedTuple):
    message: str
    param: "__EnvVar"

    def to_json(self):
        return {"message": self.message, "inputId": self.param.id}


CONVERTIBLE_TYPES = [int, str, float, bool, JinjaTemplatedStr]


def convert(c):
    def do_convert(raw: Dict[str, Any], column):
        if c == JinjaTemplatedStr:
            template = Template(column)
            return template.render(**raw)
        else:
            value = raw[column]
            if c in [str, float]:
                return c(value)
            if c == int:
                return int(float(value))
            elif c == bool:
                return DataType.BOOL.coerce(value)

    return do_convert


def get_input_converter(entrypoint_fn) -> Dict[str, Callable[[str], Any]]:
    """
    Build the input_conversion map to allow promotion from String to to int, float, and bool
    :param entrypoint_fn:
    :return: Dict from the name of the function arguments to a converter function.
    """
    sig = inspect.signature(entrypoint_fn)
    converter = {}
    from lhub_integ.util import exit_with_instantiation_errors

    for param in sig.parameters:
        annot = sig.parameters[param].annotation
        # The annotation is the Python class -- in these simple cases we can just call
        # the class constructor
        if annot in CONVERTIBLE_TYPES:
            converter[param] = convert(annot)
        elif annot == inspect.Parameter.empty:
            converter[param] = lambda raw, column: raw[column]
        else:
            exit_with_instantiation_errors(
                1,
                [
                    f"Unsupported type annotation: {annot}. Valid annotations are: {CONVERTIBLE_TYPES}"
                ],
            )
    return converter
