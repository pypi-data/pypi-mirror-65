import pytest
from graphene.test import Client

from acondbs.schema.schema import schema

##__________________________________________________________________||
params = [
    'Simulation', 'SimulationConnection',
    'SimulationFilePath', 'SimulationFilePathConnection',
    'Map', 'MapConnection',
    'MapFilePath', 'MapFilePathConnection',
    'Beam', 'BeamConnection',
]

@pytest.mark.parametrize('type_name', params)
def test_object(app, snapshot, type_name):
    '''test objects defined
    '''
    query = '''
      query q($type: String!) {
        __type(name: $type) {
          name
          description
          fields {
            name
          }
        }
      }
    '''
    variables = {'type': type_name}
    client = Client(schema)
    with app.app_context():
        snapshot.assert_match(client.execute(query, variables=variables))

##__________________________________________________________________||
