# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_schema[allMapsFirstTwo] 1'] = {
    'data': {
        'allMaps': {
            'edges': [
                {
                    'node': {
                        'name': 'lat20190213'
                    }
                },
                {
                    'node': {
                        'name': 'lat20200120'
                    }
                }
            ]
        }
    }
}

snapshots['test_schema[allMapsFirstTwoSort] 1'] = {
    'data': {
        'allMaps': {
            'edges': [
                {
                    'node': {
                        'name': 'lat20200201'
                    }
                },
                {
                    'node': {
                        'name': 'lat20200120'
                    }
                }
            ]
        }
    }
}

snapshots['test_schema[mapByMapID] 1'] = {
    'data': {
        'map': {
            'name': 'lat20190213'
        }
    }
}

snapshots['test_schema[mapByMapID-nonexistent] 1'] = {
    'data': {
        'map': None
    }
}

snapshots['test_schema[mapByName] 1'] = {
    'data': {
        'map': {
            'mapId': '1001'
        }
    }
}

snapshots['test_schema[beamByBeamID] 1'] = {
    'data': {
        'beam': {
            'name': '20180101'
        }
    }
}

snapshots['test_schema[beamByBeamID-nonexistent] 1'] = {
    'data': {
        'beam': None
    }
}

snapshots['test_schema[beamByName] 1'] = {
    'data': {
        'beam': {
            'beamId': '1010'
        }
    }
}

snapshots['test_schema[allSimulations] 1'] = {
    'data': {
        'allSimulations': {
            'edges': [
                {
                    'node': {
                        'name': 'xyz-s1234-20200101'
                    }
                }
            ]
        }
    }
}

snapshots['test_schema[simulationBySimulationID] 1'] = {
    'data': {
        'simulation': {
            'name': 'xyz-s1234-20200101'
        }
    }
}

snapshots['test_schema[simulationBySimulationID-nonexistent] 1'] = {
    'data': {
        'simulation': None
    }
}
