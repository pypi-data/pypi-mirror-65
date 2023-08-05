import graphene
from graphene.relay import Node
from graphene_mongo import MongoengineObjectType
from graphql import GraphQLError
from ...utils.schema import input_to_dictionary
from .. import auth
from ..models import User as UserModel
from ..use_cases import (
    CreateUser as CreateUserUseCase,
    EditUser as EditUserUseCase,
    DeleteUser as DeleteUserUseCase,
    EditPasswordUser,
    ResetPassword as ResetPasswordUseCase
)


__all__ = (
    'UserAttribute',
    'User',
    'CreateUser',
    'UpdateUser',
    'DeleteUser',
    'UpdatePassword',
    'ResetPassword',
)


class UserAttribute:
    username = graphene.String()
    change_password = graphene.Boolean()


class User(MongoengineObjectType, UserAttribute):
    """User Node"""

    class Meta:
        model = UserModel
        interfaces = (Node,)
        exclude_fields = ('password')


class CreateUserInput(graphene.InputObjectType, UserAttribute):
    """Arguments to create a User."""
    username = graphene.String(required=True)
    password = graphene.String(required=True)
    password_confirmed = graphene.String(required=True)
    role = graphene.String(required=True)


class CreateUser(graphene.Mutation):
    user = graphene.Field(lambda: User)

    class Arguments(UserAttribute):
        input = CreateUserInput(required=True)

    def mutate(self, info, input):
        # transforma el request para el caso de uso
        data = input_to_dictionary(input)
        use_case = CreateUserUseCase()
        result = use_case.handle(data)

        if result.http_code > 299:
            raise GraphQLError(result.message)
        return CreateUser(
            user=result.user
        )


class UpdateUserInput(graphene.InputObjectType):
    """Arguments to update a User."""
    id = graphene.ID(required=True)
    change_password = graphene.Boolean(required=True)


class UpdateUser(graphene.Mutation):
    user = graphene.Field(lambda: User)

    class Arguments(UserAttribute):
        input = UpdateUserInput(required=True)

    def mutate(self, info, input):
        # Transform request for use case
        data = input_to_dictionary(input)
        use_case = EditUserUseCase()
        result = use_case.handle(data)

        if result.http_code > 299:
            raise GraphQLError("{}. {}".format(
                result.message,
                result.errors if result.errors else ""
            ))
        return UpdateUser(
            user=result.user
        )


class DeleteUserInput(graphene.InputObjectType):
    """Arguments to delete a User."""
    id = graphene.ID(required=True)


class DeleteUser(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments():
        input = DeleteUserInput(required=True)

    def mutate(self, info, input):
        # transforma el request para el caso de uso
        data = input_to_dictionary(input)
        use_case = DeleteUserUseCase()
        result = use_case.handle(data)

        if result.http_code > 299:
            raise GraphQLError(result.message)
        return DeleteUser(
            ok=True
        )


class UpdatePasswordInput(graphene.InputObjectType):
    """Arguments to update a User."""
    current_password = graphene.String(required=True)
    new_password = graphene.String(required=True)
    password_confirmed = graphene.String(required=True)


class UpdatePassword(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments():
        input = UpdatePasswordInput(required=True)

    def mutate(self, info, input):
        user = auth.current_user()

        # transforma el request para el caso de uso
        data = input_to_dictionary(input)
        data['id'] = str(user.id)

        use_case = EditPasswordUser()
        result = use_case.handle(data)

        if result.http_code > 299:
            raise GraphQLError(result.message)
        return UpdatePassword(
            ok=True
        )


class ResetPasswordInput(graphene.InputObjectType):
    """Arguments to ResetPassword."""
    id = graphene.ID(required=True)


class ResetPassword(graphene.Mutation):
    password = graphene.String()

    class Arguments():
        input = ResetPasswordInput(required=True)

    def mutate(self, info, input):
        data = input_to_dictionary(input)
        use_case = ResetPasswordUseCase()
        result = use_case.handle(data)

        if result.http_code > 299:
            raise GraphQLError(result.message)
        return ResetPassword(
            password=result.password
        )
