import os
import json
import os.path

import azureml.designer.serving.dagengine.score_implementation as score_implementation
from azureml.designer.serving.dagengine.constants import DS_PATH_ENV_VAR_NAME, MODEL_PARENT_PATH_ENV_VAR_NAME
from azureml.studio.core.utils.fileutils import clear_folder

DEFAULT_ARGS = {
    'format': 'swagger',
    'details': 'false',
    'verbose': 'true'
}


class MockRequest(object):
    """Mock the behavior of http request object for test"""
    def __init__(self,
                 method: str = 'POST',
                 args: dict = None,
                 data: str = ''):
        self.method = method
        self.args = args or DEFAULT_ARGS
        self.data = data

    def get_data(self):
        return self.data


def mock_score(test_root_path):
    inputs_path = test_root_path / 'inputs'
    expected_outputs_path = test_root_path / 'expected_outputs'
    temp_output_path = test_root_path / 'gen'
    clear_folder(temp_output_path)

    os.environ[DS_PATH_ENV_VAR_NAME] = str(test_root_path)
    os.environ[MODEL_PARENT_PATH_ENV_VAR_NAME] = str(test_root_path)

    score_implementation.init()
    for input_file_name in os.listdir(inputs_path):
        input_file_path = inputs_path / input_file_name
        with open(input_file_path) as fp:
            input_data = fp.read()
        request = MockRequest(data=input_data)
        response = score_implementation.run(request)
        output_data_bytes = response.get_data()
        output_data = json.loads(output_data_bytes.decode('utf-8'))

        output_file_name = f'out.{input_file_name}'
        output_file_path = temp_output_path / output_file_name
        with open(output_file_path, 'w') as fp:
            json.dump(output_data, fp, indent=4)

        expected_output_file_path = expected_outputs_path / output_file_name
        with open(expected_output_file_path) as fp:
            expected_output_data = json.load(fp)
        assert(output_data == expected_output_data)
