# pylint: disable=no-self-use, protected-access
import drvn.installer.example_module as example_module

import pytest


class TestExampleFunction:
    def test_normal(self):
        assert (
            example_module.example_public_function() == "Example return value"
        )
