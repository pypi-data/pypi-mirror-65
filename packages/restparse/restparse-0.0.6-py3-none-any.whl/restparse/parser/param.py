class Param(object):
    """ Param class """

    def __init__(
        self,
        name,
        type=None,
        dest=None,
        description=None,
        required=False,
        default=None,
        choices=None,
        action=None
    ):
        """ Returns a new instance of Param:

        Args:
             name (str): The parameter name
        Optional args:
            type (type): The value type
            dest (str): The name to assign the vale to (defaults to the name of the param)
            description (str): A description of the param
            required (bool): If True, the parser will require the param
            default: A default value for the param
            choices (list): A list of available choices
            action (callable): An action to perform on the value at the start of parsing, must be a callable
        """
        self.name = name
        self.type = type
        self.dest = dest
        self.description = description
        self.required = required
        self.default = default
        self.choices = choices
        self.action = action
