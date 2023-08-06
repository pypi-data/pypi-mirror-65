from typing import Optional, Collection, Any

from .param import Param
from .params import Params
from .exceptions import (
    ParserParamRequiredError, ParserTypeError, ParserInvalidChoiceError,
    DuplicateParamError
)

import json
from string import Template


class Parser(object):
    """ Parser class """

    def __init__(self, description: Optional[str] = None, allowed_types: Optional[Collection] = None):
        """ Returns an instance of Parser

        Args:
            description (str): A description of the parser (None)
            allowed_types (list): A list of allowed types (str, int, float, list, dict, bool, None)
        """
        self.description = description
        self.allowed_types = allowed_types or (
            str, int, float, list, dict, bool, None
        )
        self.params = {}

        if allowed_types:
            if not type(allowed_types) in (list, set, tuple):
                raise TypeError(
                    f"Allowed types must be list, set or tuple, not {type(allowed_types)}"
                )

    def add_param(
        self,
        name,
        type=None,
        dest=None,
        description=None,
        required=False,
        choices=None,
        default=None,
        action=None
    ):
        """ Add a parameter to the parser

        Args:
            name (str): The parameter name
            type (type): The type to which the parser should expect
            dest (str): The name of the attribute to be added to the object returned by parse_params()
            description (str): A description of the param
            required (bool): Whether or not the param may be omitted
            choices (container): A container of the allowable values for the argument
            default: The value produced if the argument is absent from the params
            action (callable): An action to perform on the value at the start of parsing, must be a callable
        """

        # Check type
        if type not in self.allowed_types:
            raise ParserTypeError(f"Invalid type '{type}' for param {name}")

        # Check default type
        if default and type:
            try:
                default = type(default)
            except ValueError:
                raise ParserTypeError(
                    f"Invalid default value type '{type}' for param {name}"
                )

        # Create a new Param and add it to the self.params dict {name: Param}
        a = Param(
            name,
            type=type,
            dest=dest,
            description=description,
            required=required,
            default=default,
            choices=choices,
            action=action
        )

        if name in self.params:
            raise DuplicateParamError(f"Duplicate parameter '{name}'")
        else:
            self.params[name] = a

    def parse_params(self, data: dict = None, allow_all: Optional[bool] = False) -> Params:
        """ Parses a dict into param objects """

        raw_data = data
        params = Params()

        if not data:
            data = {}

        for name, param in self.params.items():

            value: Any = data.get(param.name, None)

            if value == "":
                value = None

            # Check choices
            if param.choices:
                if value not in param.choices and value is not None:
                    raise ParserInvalidChoiceError(
                        f"Parameter '{value}' not in choices"
                    )

            # Check required
            if param.required and value is None:
                raise ParserParamRequiredError(
                    f"Missing required parameter '{param.name}'"
                )

            # Check value type
            if value and param.type and type(value) != param.type:
                try:
                    param.type(value)
                except Exception:
                    raise ParserTypeError(
                        f"Incorrect type ({type(value)}) for {param.name}"
                    )

            # Perform any actions
            if param.action and value:
                value = param.action(value)

            # Set the params attribute
            if param.default and value is None:
                setattr(params, param.name, param.default)
                params.add_param(param.name)
            elif param.dest:
                setattr(params, param.dest, value)
                params.add_param(param.name)
            else:
                setattr(params, param.name, value)
                params.add_param(param.name)

        if allow_all:
            for k, v in raw_data.items():
                if k not in params.params:
                    setattr(params, k, v)
                    params.add_param(k)

        return params

    def help(self):
        r = f"""$description

Args:
\t$required

Optional:
\t$optional

            """
        required = []
        optional = []

        for param in self.params.values():
            if param.required:
                required.append(
                    f"{param.name} ({str(param.type)}): {param.description}"
                )
            else:
                optional.append(
                    f"{param.name} ({param.type}): {param.description}"
                )

        t = Template(r)
        return t.substitute(
            description=self.description,
            required="\n".join(required),
            optional="\n".join(optional),
        )
