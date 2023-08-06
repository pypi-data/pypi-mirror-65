from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType

from ..models import MapFilePath as MapFilePathModel

##__________________________________________________________________||
class MapFilePath(SQLAlchemyObjectType):
    class Meta:
        model = MapFilePathModel
        interfaces = (relay.Node, )

# class MapFilePathConnection(relay.Connection):
#     class Meta:
#         node = MapFilePath

##__________________________________________________________________||
