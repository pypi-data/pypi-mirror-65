import pytest
from graphene.test import Client

from acondbs.schema.schema import schema

##__________________________________________________________________||
params = [
    pytest.param(
        '''
        { allSimulations {
             edges { node { name } }
           } }
         ''',
        id='allSimulations'
    ),
    pytest.param(
        '''
        { simulation(simulationId: 1001) { name } }
         ''',
        id='simulationBySimulationID'
    ),
    pytest.param(
        '''
        { simulation(simulationId: 2001) { name } }
         ''',
        id='simulationBySimulationID-nonexistent'
    ),
    pytest.param(
        '''
        { allMaps(first: 2) {
             edges { node { name } }
           } }
         ''',
        id='allMapsFirstTwo'
    ),
    pytest.param(
        '''
        { allMaps(first: 2, sort: DATE_POSTED_DESC) {
             edges { node { name } }
           } }
         ''',
        id='allMapsFirstTwoSort'
    ),
    pytest.param(
        '''
        { map(mapId: 1001) { name } }
         ''',
        id='mapByMapID'
    ),
    pytest.param(
        '''
        { map(mapId: 2001) { name } }
         ''',
        id='mapByMapID-nonexistent'
    ),
    pytest.param(
        '''
        { map(name: "lat20190213") { mapId } }
         ''',
        id='mapByName'
    ),
    pytest.param(
        '''
        { beam(beamId: 1010) { name } }
         ''',
        id='beamByBeamID'
    ),
    pytest.param(
        '''
        { beam(beamId: 2001) { name } }
         ''',
        id='beamByBeamID-nonexistent'
    ),
    pytest.param(
        '''
        { beam(name: "20180101") { beamId } }
         ''',
        id='beamByName'
    ),
]

@pytest.mark.parametrize('query', params)
def test_schema(app, snapshot, query):
    client = Client(schema)
    with app.app_context():
        snapshot.assert_match(client.execute(query))

##__________________________________________________________________||
