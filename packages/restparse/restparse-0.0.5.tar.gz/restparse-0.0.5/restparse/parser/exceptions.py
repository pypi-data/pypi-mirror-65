class ParserParamRequiredError(Exception):
    """ Raised when a required parameter is not in the parser body """
    ...


class ParserTypeError(TypeError):
    """ Raised when the parser does not get the type it expects """
    ...


class ParserInvalidChoiceError(Exception):
    """ Raised when a value is not in the list of choices """
    ...


class ParamNotFoundError(KeyError):
    """ Raised when a parameter is not found """
    ...


class DuplicateParamError(Exception):
    """ Raised when a duplicate parameter is added to add_param() """
    ...
