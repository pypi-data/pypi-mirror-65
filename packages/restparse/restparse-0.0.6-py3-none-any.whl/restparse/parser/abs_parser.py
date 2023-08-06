from string import Template
import abc


class AbsParser(abc.ABC):
    """ Parser abstract base class """

    params = {}
    allowed_types = (str, int, float, list, dict, bool, None)

    def __init__(self, description=None, allowed_types=None):
        self.description = description
        if allowed_types:
            self.allowed_types = allowed_types

    @abc.abstractmethod
    def add_param(
        self,
        name,
        type=None,
        dest=None,
        description=None,
        required=False,
        choices=None,
        default=None,
    ):
        pass

    @abc.abstractmethod
    def parse_params(self, data):
        pass

    @abc.abstractmethod
    def get_param(self, name):
        pass

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
                optional.append(f"{param.name} ({param.type}): {param.description}")

        t = Template(r)
        return t.substitute(
            description=self.description,
            required="\n".join(required),
            optional="\n".join(optional),
        )
