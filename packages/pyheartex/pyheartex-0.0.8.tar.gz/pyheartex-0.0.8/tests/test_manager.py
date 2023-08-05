import pytest
import json
from fakeredis import FakeStrictRedis

from htx import init_model_server
from htx.base_model import BaseModel


class TestPredictor(BaseModel):

    def load(self, serializer_train_output):
        pass

    def predict(self, tasks):
        pass

    def get_output(self, task):
        pass


def train_test_predictor(input_data_dir, output_model_dir):
    return json.dumps({})


# @pytest.fixture
# def redis_with_stashed_resources(redis_pytest):
#     redis_pytest.set(f'project:1:res', json.dumps({'model_dir': 'xxx'}))
#     return redis_pytest


def test_predict():

    init_model_server(
        create_model_func=TestPredictor,
        train_script=train_test_predictor,
        redis=FakeStrictRedis()
    )

    assert 0