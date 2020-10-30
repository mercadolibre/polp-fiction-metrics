from unittest import TestCase
import os


class TestConfig(TestCase):

    def test_config_variable(self):
        from app import config
        assert True