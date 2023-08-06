from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType

from ..models import SimulationFilePath as SimulationFilePathModel

##__________________________________________________________________||
class SimulationFilePath(SQLAlchemyObjectType):
    class Meta:
        model = SimulationFilePathModel
        interfaces = (relay.Node, )

##__________________________________________________________________||
