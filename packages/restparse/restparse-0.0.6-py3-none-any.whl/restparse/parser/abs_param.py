import abc


class AbsParam(abc.ABC):
    """ Param abstract base class """

    def __init__(
        self,
        name,
        type=None,
        dest=None,
        description=None,
        required=False,
        choices=None,
        default=None,
    ):
        self.name = name
        self.type = type
        self.dest = dest
        self.description = description
        self.required = required
        self.choices = choices
        self.default = default

    def __repr__(self):
        return (
            f"Arg(name={self.name}, type={self.type}, dest={self.dest} description={self.description}, required={self.required}, "
            f"default={self.default}, choices={self.choices}) "
        )
