# Welcome to Marshmallow-Pynamo-DB

[![Build](https://github.com/chrismaille/marshmallow-pynamodb/workflows/tests/badge.svg)](https://github.com/chrismaille/marshmallow-pynamodb/actions)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/stela)](https://www.python.org)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg)](https://conventionalcommits.org)
<a href="https://github.com/psf/black"><img alt="Code style: black"
src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>

> Original Project: https://github.com/mathewmarcus/marshmallow-pynamodb

[PynamoDB](https://pynamodb.readthedocs.io/en/latest/) integration with
the [Marshmallow](https://marshmallow.readthedocs.io/en/latest/)
(de)serialization library.

###  Installation
From PyPi:
```shell
  $ pip install marshmallow-pynamo-db
```

From GitHub:

```shell
  $ pip install git+https://github.com/chrismaille/marshmallow-pynamodb#egg=marshmallow_pynamodb
```

### Declare your models

```python
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute

class User(Model):
    class Meta:
        table_name = "user"
    email = UnicodeAttribute(null=True)
    first_name = UnicodeAttribute(range_key=True)
    last_name = UnicodeAttribute(hash_key=True)
```

###  Generate marshmallow schemas

```python
from marshmallow_pynamodb import ModelSchema

class UserSchema(ModelSchema):
    class Meta:
        model = User

user_schema = UserSchema()
```

### (De)serialize your data

```python
user = User(last_name="Smith", first_name="John")

user_schema.dump(user).data
# {u'first_name': u'John', u'last_name': u'Smith', u'email': None}

user_schema.load({"last_name": "Smith", "first_name": "John"}).data
# user<Smith>
```

### Nested models? No problem

```python
from marshmallow_pynamodb.schema import ModelSchema

from pynamodb.models import Model
from pynamodb.attributes import (
    ListAttribute,
    MapAttribute,
    NumberAttribute,
    UnicodeAttribute,
)

class Location(MapAttribute):
    latitude = NumberAttribute()
    longitude = NumberAttribute()
    name = UnicodeAttribute()


class Person(MapAttribute):
    firstName = UnicodeAttribute()
    lastName = UnicodeAttribute()
    age = NumberAttribute()


class OfficeEmployeeMap(MapAttribute):
    office_employee_id = NumberAttribute()
    person = Person()
    office_location = Location()


class Office(Model):
    class Meta:
        table_name = 'OfficeModel'

    office_id = NumberAttribute(hash_key=True)
    address = Location()
    employees = ListAttribute(of=OfficeEmployeeMap)


class OfficeSchema(ModelSchema):
    class Meta:
        model = Office

# noinspection PyTypeChecker
OfficeSchema().load(
    {
        'office_id': 789,
        'address': {
            'latitude': 6.98454,
            'longitude': 172.38832,
            'name': 'some_location'
        },
        'employees': [
            {
                'office_employee_id': 123,
                'person': {
                    'firstName': 'John',
                    'lastName': 'Smith',
                    'age': 45
                },
                'office_location': {
                    'latitude': -24.0853,
                    'longitude': 144.87660,
                    'name': 'other_location'
                }
            },
            {
                'office_employee_id': 456,
                'person': {
                    'firstName': 'Jane',
                    'lastName': 'Doe',
                    'age': 33
                },
                'office_location': {
                    'latitude': -20.57989,
                    'longitude': 92.30463,
                    'name': 'yal'
                }
            }
        ]
    }
)
# Office<789>
```

### License
MIT licensed. See the bundled
[LICENSE](https://github.com/mathewmarcus/marshmallow-pynamodb/blob/master/LICENSE.txt)
file for more details.

### Not working?

Dont panic. Get a towel and, please, open a
[issue](https://github.com/chrismaille/stela/issues).
