"""
Environment Variable Wrappers

By wrapping environment variables in our classes, we can find what environment variables the
integration uses at parse time.

User-code should only use `EnvVar` -- `PrefixedEnvVar` subclasses are for internal use only.
"""
import os
from abc import ABCMeta, abstractmethod

from lhub_integ.util import exit_with_instantiation_errors


class __EnvVar:
    """
    __EnvVar should not be instantiated by Integrations! Use ConnectionParam or ActionParam instead
    """

    def __init__(self, id, default=None, optional=False):
        """
        :param id: ID of the environment variable
        """
        self.id = id
        self.default = default
        self.optional = optional or default is not None

    def get_not_empty(self):
        env = os.environ.get(self.id)
        if env and len(env) > 0:
            return env
        else:
            return None

    def valid(self):
        return self.get_not_empty() or self.optional

    def read(self):
        value = self.get_not_empty() or self.default
        if value is None and not self.optional:
            exit_with_instantiation_errors(
                1, [{"message": f"Environment variable {self.id} must be defined"}]
            )
        else:
            return value

    def __str__(self):
        read = self.read()
        if not read:
            return ""
        return read


class PrefixedEnvVar(__EnvVar, metaclass=ABCMeta):
    """
    PrefixedEnvVar wraps Environment variables use for internal signalling to lhub_integ

    Specifically:
    Internal environment variables are prefixed with `__`
    Environment variables that map input columns to parameter ids are prefixed with `___`
    """

    def __init__(self, id, *args, **kwargs):
        super().__init__(self.prefix() + id, *args, **kwargs)

    @classmethod
    @abstractmethod
    def prefix(cls):
        pass


class InternalEnvVar(PrefixedEnvVar):
    @classmethod
    def prefix(cls):
        return "__"


class MappedColumnEnvVar(PrefixedEnvVar):
    @classmethod
    def prefix(cls):
        return "___"
