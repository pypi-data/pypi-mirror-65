from mongoengine import (
    StringField,
    DictField,
    ReferenceField,
    DateTimeField,
    BooleanField,
    Document
)


class Role(Document):
    name = StringField(required=True, unique=True)
    permissions = DictField(required=False)


class User(Document):
    username = StringField(required=True, unique=True)
    password = StringField(required=True)

    change_password = BooleanField(default=False)
    """bool: Indica si es necesario realizar cambio de contraseña
    ::
        (default=True)
    """

    role = ReferenceField(
        Role,
        dbref=True,
        required=True
    )


class WhitelistToken(Document):
    uuid_access = StringField(required=True, unique=True)
    uuid_refresh = StringField(required=True, unique=True)
    user = ReferenceField(
        User,
        dbref=True,
        required=True
    )
    created_at = DateTimeField()
