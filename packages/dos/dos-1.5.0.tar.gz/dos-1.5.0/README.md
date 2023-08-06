# dos [![PyPi version](https://img.shields.io/pypi/v/dos.svg)](https://pypi.python.org/pypi/dos/) [![](https://img.shields.io/badge/python-3.1+-blue.svg)]((https://www.python.org/downloads/)) ![t](https://img.shields.io/badge/status-stable-green.svg) [![](https://img.shields.io/github/license/pr/dos.svg)](https://github.com/pr/dos/blob/master/LICENSE)

## Introduction

dos is a Python package to make it easy to document and validate a Flask API. Write a single chunk of code to create 
endpoints with both built in validation and automatically generated documentation. The documentation is Open API 3.0 
(formerly known as Swagger) in JSON form. 

## Installation 

You can install the latest version of dos with pip.

```bash
pip install dos
```

## Hello World

> All of this code is found in the [pet_shop](https://github.com/pr/dos/tree/master/examples/tutorial/pet_shop) example. 
> For a more substantive look at dos, please see [dos in depth](#dos-in-depth)

Let's look at the structure of a typical dos endpoint. The following code defines the `/dog/get` endpoint.

```python
from http import HTTPStatus
from dos.schema import ErrorFields
from pet_shop.model import DogFields

def handler():

    # ... database query looking for the dog ...

    if dog_found:
        dog = {
            "name": "Spot",
            "breed": "Poodle"
        }
        return HTTPStatus.OK, dog
    else:
        return HTTPStatus.NOT_FOUND, {"message": "No dog by that name found!"}


def input_schema():
    return DogFields().specialize(only=["name"])


def output_schema():
    return {
        HTTPStatus.OK: DogFields().all(),
        HTTPStatus.NOT_FOUND: ErrorFields().all()
    }
```

Each endpoint is made up of 3 critical components. 

1. `handler()`

The handler defines the endpoint functionality. Adding to the database, calling another endpoint, it all happens here.

2. `input_schema()`

The input_schema defines what fields the endpoint expects. These are typically defined elsewhere and imported, but they
don't have to be.

3.  `output_schema()`

The output_schema defines what fields the endpoint is allowed to expose. Critically, if the handler sets a field that is 
not defined in the output_schema, that field will not be exposed by the API. Because endpoints can produce different HTTP 
statuses, the output_schema is a dictionary where the keys are all the statuses produced by the endpoint.

---

The endpoints import fields typically defined in another file. Here is the DogFields class from above.

```python
from dos import prop
from dos.schema import Fields

class DogFields(Fields):
    base_schema = {
        "name": prop.String("The dog's name."),
        "breed": prop.String("The dog's breed.")
    }

    def __init__(self):
        super().__init__(self.base_schema)
```

Every Fields class needs to have a base_schema, a dictionary made up of dos props. Read more about props [here](#props).

The Field class gives additional functionality outlined [here](#the-field-class).

---

Now that we've defined an endpoint, we can create out flask app. It will look something like this: 

```python
from dos.open_api import OpenAPI
from dos.flask_wrappers import wrap_validation, wrap_handler, wrap_route
from flask import Flask, jsonify, render_template

from pet_shop.api.dog import get as dog_get

def create_app():
    app = Flask(__name__)
    open_api = OpenAPI("Pet Shop API", "1.0")

    handler_mapping = [
        (dog_get, "/dog/get", "get"),
    ]

    for module, path, http_method in handler_mapping:
        handler = wrap_handler(module.__name__, module.handler)
        handler = wrap_validation(handler, module)
        wrap_route(app, handler, path, http_method)
        open_api.document(module, path, http_method)

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/docs")
    def docs(): 
        return render_template("docs.html")

    @app.route("/open_api.json")
    def open_api_endpoint():
        return jsonify(open_api)

    return app

```

This will create a flask app with the endpoint we just defined, as well as documenting it with Open API 3.0 JSON. 

For more about the Flask Wrappers, please look [here](#flask-wrappers)

That's all there is to it. Once the general structure is set up, each additional endpoint should be relatively simple 
to implement.

To run the full working example, please see [pet_shop](https://github.com/pr/dos/tree/master/examples/tutorial/pet_shop). 

## dos in Depth

### Props

The foundation of dos is props. There are nine different prop types, 6 which are represented by Open API:

Name | Python Type | OpenAPI Representation | Additional Notes
--- | --- | --- | ---
Integer | `int` | Yes
Number | `int`, `float`, `decimal.Decimal` | Yes
Numeric | `int`, `float`, `decimal.Decimal`, `str` | No | The string must contain a valid number
String | `str` | Yes
DateTime | `str`, `arrow.Arrow` | No | The string must contain a valid arrow DateTime
Enum | `enum.Enum` | No
Boolean | `bool` | Yes
Object | `dict` | Yes
Array | `list` | Yes

Props are used to capture the structure of the inputs and outputs of endpoints.

Initializing a Prop is simple, and is always done in the context of a python dictionary 
capturing the structure of the JSON.

```python
from dos import prop

base_schema = {
    "name": prop.String(),
}
```

#### Customizing Props

Props take four optional arguments. 
Description is a string explaining what the prop represents, and is displayed in the documentation.

```python
from dos import prop

base_schema = {
    "name": prop.String(description="The dog's name."),
}
```

Required and nullable capture whether the prop is required and nullable. These are used for both validation and Open API.

```python
from dos import prop

base_schema = {
    "name": prop.String(required=False, nullable=True),
}
```

All props have these three arguments, and a final one called validators.

#### Prop Validation 

dos has a few validators built in as exemplars, but feel free to write your own Validators, specific to the domain your API is capturing.

All validators define `supported_prop_classes`, because not all validation is applicable to every prop. 
(You wouldn't validate if an array was a Social Security Number!) 

Using a Validator looks like this:

```python
from dos import prop
from dos.validators import ExactLength

base_schema = {
    "name": prop.String("This string must be 8 characters long", validators=ExactLength(8)),
}
```

The validator itself looks like this:

```python
from dos import prop
from dos.validators import Validator

class ExactLength(Validator):
    supported_prop_classes = [prop.String, prop.Number, prop.Numeric, prop.Integer]

    def __init__(self, exact_length=None):
        self.exact_length = exact_length

    def validate_prop(self, prop_class, prop_value):
        super().validate_prop(prop_class, prop_value)

        if len(prop_value) != self.exact_length:
            return (f"{prop_class.__name__} is not the correct length! The string \'{prop_value}\' is "
                    f"{len(prop_value)} characters long, not {self.exact_length}!")

        return None
```

Every validator needs to define `supported_prop_classes` and a `validate_prop` function. 

If you have a good one, feel free to submit a pull request.

#### Objects and Arrays

Objects and Arrays take additional arguments, due to their special nature.

Objects take their structure, looking something like this: 

```python
from dos import prop

base_schema = {
    "name": prop.Object(structure={
        "name": prop.String("The object has a string in it"),
        "boolean_field": prop.Boolean("And also a boolean")
    }),
}
```

Structure is mandatory, and is a dictionary of props. Validation will look for dictionaries in the JSON that match the 
outlined structure.

Array does a similar thing with the repeated_structure argument. 

```python
from dos import prop

base_schema = {
    "names": prop.Array(repeated_structure=prop.String("just a list of strings")),
}
```

You can even put these together, and have an array of objects!

```python
from dos import prop

base_schema = {
    "names": prop.Array(repeated_structure=prop.String("just a list of strings")),
    "array_of_objects": prop.Array(
        repeated_structure=prop.Object(
            structure={
                "sub_string": prop.String("the string", required=True, nullable=False),
                "required_one": prop.String(required=True, nullable=False)
            }
        ),
        description="A list of plans."
    )
}
```

#### Prop Wrappers

Prop Wrappers are another way to capture what a JSON field expects. Currently, they are used for fields with multiple valid inputs.

Say a field can take either a string or a boolean. dos captures this idea with a prop wrapper.

```python
from dos import prop
from dos import prop_wrapper

base_schema = {
    "boolean_or_string": prop_wrapper.OneOf([
        prop.String(),
        prop.Boolean()
    ]),
}
```

Critically, the OneOf prop wrapper is a just an array of props, meaning all the customization outlined above is still possible.
A convoluted example could be something like this:

```python
from dos import prop
from dos import prop_wrapper
from dos.validators import ExactLength

base_schema = {
    "boolean_or_string": prop_wrapper.OneOf([
        prop.String(validators=ExactLength(7)),
        prop.Boolean(required=False, nullable=False)
    ]),
}
```

All of this is enforced and valid. 

### The Field Class 

Fields are a collection of Props and Prop Wrappers that make up an object. They are a way to give semantically meaningful names to 
collections of Props and Prop Wrappers, and capture the object oriented nature of some APIs. 

```python
from dos import prop
from dos.schema import Fields

class DogFields(Fields):
    base_schema = {
        "name": prop.String("The dog's name."),
        "breed": prop.String("The dog's breed.")
    }

    def __init__(self):
        super().__init__(self.base_schema)
```

All fields need a base_schema, which is where the Props and Prop Wrappers that make up the collection are stored.

#### Field Customization 

The Fields class gives many opportunities for customization of input and output schema.

```python
from http import HTTPStatus
from pet_shop.model import DogFields

def input_schema():
    return DogFields().specialize(only=["name"])

def output_schema():
    return {
        HTTPStatus.OK: DogFields().all(),
    }
```

`specialize` allows picking and choosing props, while `all` will use every prop defined by the Field. 

`specialize` means any Field object can be customized to it's application, by overriding fields on specific props, 
only using some fields, and/or excluding other fields.

```python
from pet_shop.model import DogFields

def input_schema():
    return DogFields().specialize(overrides={
        "breed": {
            "required": False,
        },
    }, exclude=["name"])
```

Thus, it is possible to capture objects coming in and out of the API, while tailoring them to specific use cases.

### Flask Wrappers

Flask Wrappers are how the modules that define API endpoints are integrated with Flask. 

```python
from dos.flask_wrappers import wrap_validation, wrap_handler, wrap_route
from flask import Flask

from pet_shop.api.dog import get as dog_get

app = Flask(__name__)

handler_mapping = [
    (dog_get, "/dog/get", "get"),
]

for module, path, http_method in handler_mapping:
    handler = wrap_handler(module.__name__, module.handler)
    handler = wrap_validation(handler, module)
    wrap_route(app, handler, path, http_method)
```

The handler_mapping is a list of every endpoint that needs to be documented and implemented with dos. The module,
paired with a string representation of its path and the HTTP method it supports, is then processed with flask wrappers.

`wrap_handler` takes the module and extracts the handler. `wrap_validation` parses the input_schema and the output_schema
and adds validation to the handler to enforce their constraints. Finally, `wrap_route` adds the endpoint to the flask app 
itself. 


### Open API 

In same place you create your Flask app, it is easy to also create Open API documentation for that app. 

```python
from dos.open_api import OpenAPI
from flask import Flask

def create_app():
    app = Flask(__name__)
    open_api = OpenAPI("Your API Name", "1.0")
```

You can customize the Open API with contact information, a logo, and tags.

```python
from dos.open_api import OpenAPI

open_api = OpenAPI("Your API Name", "1.0")
open_api.add_contact("Pet Shop Dev Team", "https://www.example.com", "pet_shop@example.com")
open_api.add_logo("/static/pet_shop.png", "#7D9FC3", "Pet Shop", "/")
open_api.add_tag(
    "introduction",
    "Welcome! This is the documentation for the API.",
)
```

Tags are important for organizing endpoints. If you have a `dog/create` and a `/dog/delete` endpoint, create a 
dog tag to group them together.

```python
from dos.open_api import OpenAPI

open_api = OpenAPI("Your API Name", "1.0")
open_api.add_tag(
    "dog",
    "Endpoints for interacting with dogs.",
)
```

If you want to add text to the top of the Open API JSON, so others know how it was made, use the 
disclaimer functionality.


```python
from dos.open_api import OpenAPI

open_api = OpenAPI("Your API Name", "1.0")
open_api.add_disclaimer(
    "This file is generated automatically. Do not edit it directly! Edit "
    "the input_schema and output_schema of the endpoint you are changing."
)
```

Finally, to take the `input_schema` and `output_schema` defined in each endpoint module and make Open API out of it,
call document. 

```python
from dos.open_api import OpenAPI
from pet_shop.api.dog import get as dog_get

open_api = OpenAPI("Your API Name", "1.0")

handler_mapping = [
    (dog_get, "/dog/get", "get"),
]

for module, path, http_method in handler_mapping:
    open_api.document(module, path, http_method)
```

The same code you used for validation will also be used for documentation!

# Acknowledgements

Developed at [Capital Rx](https://cap-rx.com/) with team input and assistance, open sourced with 
permission from [Ryan Kelley, CTO](https://github.com/f0rk). 
