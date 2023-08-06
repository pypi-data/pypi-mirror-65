from unittest import TestCase
from flask_auth_service_mongo.utils.contract import LoggingInterface


class TestContract(TestCase):

    def test_ok(self):
        log_interface = LoggingInterface()
        msg = "Any message"
        log_interface.debug(msg)
        log_interface.info(msg)
        log_interface.error(msg)
