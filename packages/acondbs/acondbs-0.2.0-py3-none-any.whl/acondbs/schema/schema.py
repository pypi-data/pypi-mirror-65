import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField

from .simulation import Simulation, SimulationModel
from .map_ import Map, MapModel, MapConnection, CreateMap, UpdateMap, DeleteMap
from .beam import Beam, BeamModel
from .map_file_path import MapFilePath, MapFilePathModel
from .simulation_file_path import SimulationFilePath, SimulationFilePathModel

##__________________________________________________________________||
class Query(graphene.ObjectType):

    version = graphene.String()

    def resolve_version(self, info):
        from .. import __version__
        return __version__

    node = relay.Node.Field()
    all_simulations = SQLAlchemyConnectionField(Simulation._meta.connection)
    all_maps = SQLAlchemyConnectionField(MapConnection)
    all_beams = SQLAlchemyConnectionField(Beam._meta.connection)
    all_map_file_paths = SQLAlchemyConnectionField(MapFilePath)
    all_simulation_file_paths = SQLAlchemyConnectionField(SimulationFilePath._meta.connection)

    simulation = graphene.Field(Simulation, simulation_id=graphene.Int(), name=graphene.String())

    def resolve_simulation(self, info, **kwargs):
        import time, random
        print(kwargs)
        # time.sleep(random.randint(1, 5))
        fields = ('simulation_id', 'name')
        query = Simulation.get_query(info)
        for f in fields:
            v = kwargs.get(f)
            if v is not None:
                query = query.filter(getattr(SimulationModel, f)==v)
                return query.first()
        return None

    map = graphene.Field(Map, map_id=graphene.Int(), name=graphene.String())

    def resolve_map(self, info, **kwargs):
        import time, random
        print(kwargs)
        # time.sleep(random.randint(1, 5))
        fields = ('map_id', 'name')
        query = Map.get_query(info)
        for f in fields:
            v = kwargs.get(f)
            if v is not None:
                query = query.filter(getattr(MapModel, f)==v)
                return query.first()
        return None

    beam = graphene.Field(Beam, beam_id=graphene.Int(), name=graphene.String())

    def resolve_beam(self, info, **kwargs):
        fields = ('beam_id', 'name')
        query = Beam.get_query(info)
        for f in fields:
            v = kwargs.get(f)
            if v is not None:
                query = query.filter(getattr(BeamModel, f)==v)
                return query.first()
        return None
##__________________________________________________________________||
class Mutation(graphene.ObjectType):
    create_map = CreateMap.Field()
    update_map = UpdateMap.Field()
    delete_map = DeleteMap.Field()

##__________________________________________________________________||
schema = graphene.Schema(query=Query, mutation=Mutation, types=[Map, Beam, MapFilePath])

##__________________________________________________________________||
