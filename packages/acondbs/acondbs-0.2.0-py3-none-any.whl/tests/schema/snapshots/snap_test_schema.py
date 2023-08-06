# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_object[Simulation] 1'] = {
    'data': {
        '__type': {
            'description': None,
            'fields': [
                {
                    'name': 'simulationId'
                },
                {
                    'name': 'name'
                },
                {
                    'name': 'datePosted'
                },
                {
                    'name': 'mapper'
                },
                {
                    'name': 'note'
                },
                {
                    'name': 'simulationFilePaths'
                },
                {
                    'name': 'id'
                }
            ],
            'name': 'Simulation'
        }
    }
}

snapshots['test_object[SimulationConnection] 1'] = {
    'data': {
        '__type': {
            'description': None,
            'fields': [
                {
                    'name': 'pageInfo'
                },
                {
                    'name': 'edges'
                }
            ],
            'name': 'SimulationConnection'
        }
    }
}

snapshots['test_object[Map] 1'] = {
    'data': {
        '__type': {
            'description': None,
            'fields': [
                {
                    'name': 'mapId'
                },
                {
                    'name': 'name'
                },
                {
                    'name': 'datePosted'
                },
                {
                    'name': 'mapper'
                },
                {
                    'name': 'note'
                },
                {
                    'name': 'beams'
                },
                {
                    'name': 'mapFilePaths'
                },
                {
                    'name': 'id'
                }
            ],
            'name': 'Map'
        }
    }
}

snapshots['test_object[MapConnection] 1'] = {
    'data': {
        '__type': {
            'description': None,
            'fields': [
                {
                    'name': 'pageInfo'
                },
                {
                    'name': 'edges'
                }
            ],
            'name': 'MapConnection'
        }
    }
}

snapshots['test_object[MapFilePath] 1'] = {
    'data': {
        '__type': {
            'description': None,
            'fields': [
                {
                    'name': 'mapFilePathId'
                },
                {
                    'name': 'mapId'
                },
                {
                    'name': 'path'
                },
                {
                    'name': 'note'
                },
                {
                    'name': 'map'
                },
                {
                    'name': 'id'
                }
            ],
            'name': 'MapFilePath'
        }
    }
}

snapshots['test_object[MapFilePathConnection] 1'] = {
    'data': {
        '__type': {
            'description': None,
            'fields': [
                {
                    'name': 'pageInfo'
                },
                {
                    'name': 'edges'
                }
            ],
            'name': 'MapFilePathConnection'
        }
    }
}

snapshots['test_object[Beam] 1'] = {
    'data': {
        '__type': {
            'description': None,
            'fields': [
                {
                    'name': 'beamId'
                },
                {
                    'name': 'name'
                },
                {
                    'name': 'path'
                },
                {
                    'name': 'inputMapId'
                },
                {
                    'name': 'inputBeamId'
                },
                {
                    'name': 'map'
                },
                {
                    'name': 'parentBeam'
                },
                {
                    'name': 'childBeams'
                },
                {
                    'name': 'id'
                }
            ],
            'name': 'Beam'
        }
    }
}

snapshots['test_object[BeamConnection] 1'] = {
    'data': {
        '__type': {
            'description': None,
            'fields': [
                {
                    'name': 'pageInfo'
                },
                {
                    'name': 'edges'
                }
            ],
            'name': 'BeamConnection'
        }
    }
}

snapshots['test_object[SimulationFilePath] 1'] = {
    'data': {
        '__type': {
            'description': None,
            'fields': [
                {
                    'name': 'simulationFilePathId'
                },
                {
                    'name': 'simulationId'
                },
                {
                    'name': 'path'
                },
                {
                    'name': 'note'
                },
                {
                    'name': 'simulation'
                },
                {
                    'name': 'id'
                }
            ],
            'name': 'SimulationFilePath'
        }
    }
}

snapshots['test_object[SimulationFilePathConnection] 1'] = {
    'data': {
        '__type': {
            'description': None,
            'fields': [
                {
                    'name': 'pageInfo'
                },
                {
                    'name': 'edges'
                }
            ],
            'name': 'SimulationFilePathConnection'
        }
    }
}
