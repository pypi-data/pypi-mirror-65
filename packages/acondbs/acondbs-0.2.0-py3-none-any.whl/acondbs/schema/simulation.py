from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType

from ..models import Simulation as SimulationModel

##__________________________________________________________________||
class Simulation(SQLAlchemyObjectType):
    class Meta:
        model = SimulationModel
        interfaces = (relay.Node, )

##__________________________________________________________________||
