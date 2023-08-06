# `Python parser for RESTful HTTP requests`

![Python package](https://github.com/Julian-Nash/restparse/workflows/Python%20package/badge.svg?branch=master)  

A simple, lightweight parser for RESTful HTTP request data. `Python 3.6+`

_Installation_

```sh
pip install restparse
```

_Example usage:_

```py3
from restparse.parser import Parser


parser = Parser(description="RESTful parameter parser")

parser.add_param(
    name="name",
    type=str,
    description="The users name",
    required=True
)
parser.add_param(
    name="age",
    type=int,
    description="The users age",
    required=True
)
parser.add_param(
    name="online",
    type=bool,
    description="Is the user online?",
    default=False
)
parser.add_param(
    name="height",
    type=float,
    description="The users height",
)
parser.add_param(
    name="tags",
    description="Tags",
)

payload = {
    "name": "John Doe",
    "age": "40",
    "online": False,
    "height": 6.2,
    "tags": ["python", "javascript"]
}

params = parser.parse_params(payload)

print(params.name)  # John Doe
print(params.tags)  # ['python', 'javascript']

print(params.to_dict())  # {'name': 'John Doe', 'age': 40, 'online': False, 'height': 6.2, 'tags': ['python', 'javascript']}

```

### `Usage with Flask`

_Parsing query strings:_

```py3
@app.route("/")
def index():
    """ Parsing query strings """

    parser = Parser(description="Parsing query strings")

    parser.add_param(
        "q_from",
        type=int,
        description="Query from"
    )
    parser.add_param(
        "q_to",
        type=int,
        description="Query to"
    )
    parser.add_param(
        "search",
        type=str,
        description="Search query"
    )
    params = parser.parse_params(request.args)

    print(params.q_from)
    print(params.q_to)
    print(params.search)

    return f"Params = from: {params.q_from}, to: {params.q_to}, search: {params.search}"
```

_Parsing request payloads:_

```py3
@app.route("/json", methods=["POST"])
def json_payload():
    """ Parsing request payloads """

    parser = Parser(description="Parsing a request payload")

    parser.add_param(
        "name",
        type=str,
        description="The users name",
        required=True
    )
    parser.add_param(
        "age",
        type=int,
        description="The users age",
        required=True
    )
    parser.add_param(
        "tags",
        type=list,
        description="Tags"
    )
    params = parser.parse_params(request.get_json())

    print(params.name)
    print(params.age)
    print(params.tags)

    return jsonify(params.to_dict())
```

_Parsing form data:_

```py3
@app.route("/form", methods=["POST"])
def form_payload():
    """ Parsing form data """

    parser = Parser(description="Parsing form data")

    parser.add_param(
        "name",
        type=str,
        description="The users name",
        required=True
    )
    parser.add_param(
        "age",
        type=int,
        description="The users age",
        required=True
    )
    params = parser.parse_params(request.form)

    print(params.name)
    print(params.age)

    return redirect(url_for("index"))
```

### `add_param()`

```py3
parser.add_param(
    "name",
    type=str,
    dest="new_name",
    description="A description of the param",
    required=True,
    choices=["foo", "bar"]
)
```

_options:_

```
name (str): The parameter name
type (type): The type to which the parser should expect
dest (str): The name of the attribute to be added to the object returned by parse_params()
description (str): A description of the param
required (bool): Whether or not the param may be omitted
choices (container): A container of the allowable values for the argument
default: The value produced if the argument is absent from the params
```