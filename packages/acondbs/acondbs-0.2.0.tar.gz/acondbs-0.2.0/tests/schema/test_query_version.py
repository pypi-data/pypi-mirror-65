import pytest
from graphene.test import Client

import acondbs
from acondbs.schema.schema import schema

##__________________________________________________________________||
params = [
    pytest.param(
        '{ version }',
        {'version': acondbs.__version__},
        id='version'
    ),
]

@pytest.mark.parametrize('query, expected', params)
def test_schema(app, query, expected):
    with app.app_context():
        client = Client(schema)
        result = client.execute(query)
        assert {'data': expected} == result

##__________________________________________________________________||
