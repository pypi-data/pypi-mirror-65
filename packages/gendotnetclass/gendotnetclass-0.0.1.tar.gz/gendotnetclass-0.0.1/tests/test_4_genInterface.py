import pytest
import yaml
from Library.Container import Configs,Action

class TestGen:
    def test_1_start(self):
        with open('tests/app.yaml', 'r') as stream:
            data = yaml.load(stream, Loader=yaml.FullLoader)
        Configs.config.override(data)

    # @pytest.mark.skip(reason="skip this")
    def test_2_genInterface(self):
        action = Action.action()
        action.genInterface()

    def test_3_genericinterface(self):
        action = Action.action()
        action.genGenericInterface()
