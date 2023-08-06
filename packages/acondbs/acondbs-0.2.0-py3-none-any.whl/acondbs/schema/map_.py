import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType

from ..models import Map as MapModel

from ..db.sa import sa

##__________________________________________________________________||
class Map(SQLAlchemyObjectType):
    class Meta:
        model = MapModel
        interfaces = (relay.Node, )

class MapConnection(relay.Connection):
    class Meta:
        node = Map

##__________________________________________________________________||
class MapAttribute:
    name = graphene.String()
    date_posted = graphene.Date()
    mapper = graphene.String()
    note = graphene.String()

class CreateMapInput(graphene.InputObjectType, MapAttribute):
    name = graphene.String(required=True)

class UpdateMapInput(graphene.InputObjectType, MapAttribute):
    pass

class CreateMap(graphene.Mutation):
    class Arguments:
        input = CreateMapInput(required=True)

    ok = graphene.Boolean()
    map = graphene.Field(lambda: Map)

    def mutate(root, info, input):
        map = MapModel(**input)
        sa.session.add(map)
        sa.session.commit()
        ok = True
        return CreateMap(map=map, ok=ok)

class UpdateMap(graphene.Mutation):
    class Arguments:
        map_id = graphene.Int()
        input = UpdateMapInput(required=True)

    ok = graphene.Boolean()
    map = graphene.Field(lambda: Map)

    def mutate(root, info, map_id, input):
        map = MapModel.query.filter_by(map_id=map_id).first()
        for k, v in input.items():
            setattr(map, k, v)
        sa.session.commit()
        ok = True
        return UpdateMap(map=map, ok=ok)

class DeleteMap(graphene.Mutation):
    class Arguments:
        map_id = graphene.Int()

    ok = graphene.Boolean()

    def mutate(root, info, map_id):
        map = MapModel.query.filter_by(map_id=map_id).first()
        sa.session.delete(map)
        sa.session.commit()
        ok = True
        return DeleteMap(ok=ok)

##__________________________________________________________________||
