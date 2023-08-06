# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['marshmallow_pynamodb']

package_data = \
{'': ['*']}

install_requires = \
['marshmallow>=3.0.0', 'pynamodb>=4.0.0']

setup_kwargs = {
    'name': 'marshmallow-pynamo-db',
    'version': '0.8.4',
    'description': 'PynamoDB integration with the Marshmallow (de)serialization library',
    'long_description': '# Welcome to Marshmallow-Pynamo-DB\n\n[![Build](https://github.com/chrismaille/marshmallow-pynamodb/workflows/tests/badge.svg)](https://github.com/chrismaille/marshmallow-pynamodb/actions)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/stela)](https://www.python.org)\n[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg)](https://conventionalcommits.org)\n<a href="https://github.com/psf/black"><img alt="Code style: black"\nsrc="https://img.shields.io/badge/code%20style-black-000000.svg"></a>\n\n> Original Project: https://github.com/mathewmarcus/marshmallow-pynamodb\n\n[PynamoDB](https://pynamodb.readthedocs.io/en/latest/) integration with\nthe [Marshmallow](https://marshmallow.readthedocs.io/en/latest/)\n(de)serialization library.\n\n###  Installation\nFrom PyPi:\n```shell\n  $ pip install marshmallow-pynamo-db\n```\n\nFrom GitHub:\n\n```shell\n  $ pip install git+https://github.com/chrismaille/marshmallow-pynamodb#egg=marshmallow_pynamodb\n```\n\n### Declare your models\n\n```python\nfrom pynamodb.models import Model\nfrom pynamodb.attributes import UnicodeAttribute\n\nclass User(Model):\n    class Meta:\n        table_name = "user"\n    email = UnicodeAttribute(null=True)\n    first_name = UnicodeAttribute(range_key=True)\n    last_name = UnicodeAttribute(hash_key=True)\n```\n\n###  Generate marshmallow schemas\n\n```python\nfrom marshmallow_pynamodb import ModelSchema\n\nclass UserSchema(ModelSchema):\n    class Meta:\n        model = User\n\nuser_schema = UserSchema()\n```\n\n### (De)serialize your data\n\n```python\nuser = User(last_name="Smith", first_name="John")\n\nuser_schema.dump(user).data\n# {u\'first_name\': u\'John\', u\'last_name\': u\'Smith\', u\'email\': None}\n\nuser_schema.load({"last_name": "Smith", "first_name": "John"}).data\n# user<Smith>\n```\n\n### Nested models? No problem\n\n```python\nfrom marshmallow_pynamodb.schema import ModelSchema\n\nfrom pynamodb.models import Model\nfrom pynamodb.attributes import (\n    ListAttribute,\n    MapAttribute,\n    NumberAttribute,\n    UnicodeAttribute,\n)\n\nclass Location(MapAttribute):\n    latitude = NumberAttribute()\n    longitude = NumberAttribute()\n    name = UnicodeAttribute()\n\n\nclass Person(MapAttribute):\n    firstName = UnicodeAttribute()\n    lastName = UnicodeAttribute()\n    age = NumberAttribute()\n\n\nclass OfficeEmployeeMap(MapAttribute):\n    office_employee_id = NumberAttribute()\n    person = Person()\n    office_location = Location()\n\n\nclass Office(Model):\n    class Meta:\n        table_name = \'OfficeModel\'\n\n    office_id = NumberAttribute(hash_key=True)\n    address = Location()\n    employees = ListAttribute(of=OfficeEmployeeMap)\n\n\nclass OfficeSchema(ModelSchema):\n    class Meta:\n        model = Office\n\n# noinspection PyTypeChecker\nOfficeSchema().load(\n    {\n        \'office_id\': 789,\n        \'address\': {\n            \'latitude\': 6.98454,\n            \'longitude\': 172.38832,\n            \'name\': \'some_location\'\n        },\n        \'employees\': [\n            {\n                \'office_employee_id\': 123,\n                \'person\': {\n                    \'firstName\': \'John\',\n                    \'lastName\': \'Smith\',\n                    \'age\': 45\n                },\n                \'office_location\': {\n                    \'latitude\': -24.0853,\n                    \'longitude\': 144.87660,\n                    \'name\': \'other_location\'\n                }\n            },\n            {\n                \'office_employee_id\': 456,\n                \'person\': {\n                    \'firstName\': \'Jane\',\n                    \'lastName\': \'Doe\',\n                    \'age\': 33\n                },\n                \'office_location\': {\n                    \'latitude\': -20.57989,\n                    \'longitude\': 92.30463,\n                    \'name\': \'yal\'\n                }\n            }\n        ]\n    }\n)\n# Office<789>\n```\n\n### License\nMIT licensed. See the bundled\n[LICENSE](https://github.com/mathewmarcus/marshmallow-pynamodb/blob/master/LICENSE.txt)\nfile for more details.\n\n### Not working?\n\nDont panic. Get a towel and, please, open a\n[issue](https://github.com/chrismaille/stela/issues).\n',
    'author': 'Mathew Marcus',
    'author_email': 'mathewmarcus456@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/chrismaille/marshmallow-pynamodb',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
