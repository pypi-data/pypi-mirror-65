import graphene
from graphene.relay import Node
from graphene_mongo import MongoengineObjectType
from ..models import Role as RoleModel


__all__ = (
    'Role',
)


class RoleAttribute:
    name = graphene.String()
    permissions = graphene.JSONString()


class Role(MongoengineObjectType, RoleAttribute):
    """Role Node"""

    class Meta:
        model = RoleModel
        interfaces = (Node,)
