class Params(object):
    """ Params object """

    def __init__(self):
        self._params = set()

    @property
    def params(self):
        return self._params

    def add_param(self, name: str):
        self._params.add(name)

    def to_dict(self):
        """ Returns a dict of params """

        resp = {}
        for param in self._params:
            resp[param] = getattr(self, param)

        return resp
