from cerberus import Validator as ValidatorCerberus
from bson.objectid import ObjectId


class Validator(ValidatorCerberus):

    def _validate_no_spaces(self, no_spaces, field, value):
        """ Test the value must not contain spaces

        The rule's arguments are validated against this schema:
        {'type': 'boolean'}
        """
        if no_spaces and (' ' in value):
            self._error(field, "Must not contain spaces")

    def _validate_mongo_id(self, mongo_id, field, value):
        """ Test the ObjectId of a value.

        The rule's arguments are validated against this schema:
        {'type': 'boolean'}
        """
        if mongo_id and not ObjectId.is_valid(value):
            self._error(field, "Is not a valid ID")

    def _validate_only_numbers(self, only_numbers, field, value):
        """ Test only numbers of a value.

        The rule's arguments are validated against this schema:
        {'type': 'boolean'}
        """

        if only_numbers and not value.isdigit():
            self._error(field, "Only numeric digits is allowed")
