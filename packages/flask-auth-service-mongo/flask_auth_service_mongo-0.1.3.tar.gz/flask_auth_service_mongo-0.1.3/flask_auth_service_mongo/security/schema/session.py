import graphene
from graphql import GraphQLError
from ...utils.schema import input_to_dictionary
from ..use_cases import RefreshToken as RefreshTokenUseCase

__all__ = (
    'RefreshToken',
)


class RefreshTokenInput(graphene.InputObjectType):
    """Arguments to update a User."""
    refresh_token = graphene.String(required=True)


class RefreshToken(graphene.Mutation):
    token_type = graphene.String()
    access_token = graphene.String()
    refresh_token = graphene.String()
    expires_in = graphene.Int()

    class Arguments():
        input = RefreshTokenInput(required=True)

    def mutate(self, info, input):
        data = input_to_dictionary(input)
        use_case = RefreshTokenUseCase()
        result = use_case.handle(data)

        if result.http_code > 299:
            raise GraphQLError("{}. {}".format(
                result.message,
                result.errors if result.errors else ""
            ))

        return RefreshToken(
            token_type=result.tokens.token_type,
            access_token=result.tokens.access_token,
            refresh_token=result.tokens.refresh_token,
            expires_in=result.tokens.expires_in
        )
