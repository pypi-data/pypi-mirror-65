from graphql import GraphQLError
from graphql_relay.node.node import from_global_id
from ..constants import responses


def input_to_dictionary(input):
    """Method to convert Graphene inputs to a dictionary"""
    dictionary = {}
    for key in input:
        # Convert GraphQL global id to database id
        if key == 'id':
            try:
                global_id = from_global_id(input[key])
            except Exception:
                raise GraphQLError(responses.ID_NOT_VALID)
            if isinstance(global_id, tuple) and len(global_id) == 2:
                input[key] = global_id[1]
            else:
                raise GraphQLError(responses.ID_NOT_VALID)
        if input[key] is not None:
            dictionary[key] = input[key]
    return dictionary
