import json
from pathlib import Path

from azureml.designer.serving.dagengine.score_exceptions import GraphSpecContentError
from azureml.studio.core.logger import get_logger
from azureml.studio.core.utils.dictutils import get_value_by_key_path

logger = get_logger(__name__)


def _parse_port_string(port_string):
    idx, port_type, io_name, data_type = port_string.split(':')
    port_name = ':'.join([idx, port_type])
    return {
        'port_name': port_name,
        'io_name': io_name,
        'data_type': data_type
    }


def _transform_dict_values(dictionary, value_class):
    return {k: value_class(v) for k, v in dictionary.items()}


class _DictBased(object):
    def __init__(self, dct):
        self._dct = dct

    def _get(self, path, default=None):
        return get_value_by_key_path(self._dct, path, default_value=default)

    @property
    def dct(self):
        return self._dct


class GraphSpecNodeDependencies(_DictBased):
    @property
    def conda_channels(self):
        return self._get('CondaChannels')

    @property
    def conda_packages(self):
        return self._get('CondaPackages')

    @property
    def pip_options(self):
        return self._get('PipOptions')

    @property
    def pip_packages(self):
        return self._get('PipPackages')


class GraphSpecNode(_DictBased):
    @property
    def module_id(self):
        return self._get('ModuleId')

    @property
    def input_port_mappings(self):
        return self._get('InputPortMappings')

    @property
    def output_ports(self):
        return self._get('OutputPorts')

    @property
    def parameters(self):
        return self._get('Parameters')

    @property
    def global_parameter_mappings(self):
        return self._get('GlobalParameterMappings')

    @property
    def dependencies(self):
        return GraphSpecNodeDependencies(self._get('Dependencies', {}))


class GraphSpecModuleInput(_DictBased):
    @property
    def name(self):
        return self._get('Name')

    @property
    def label(self):
        return self._get('Label')

    @property
    def data_type_ids(self):
        return self._get('DataTypeIdsList')

    @property
    def is_optional(self):
        return self._get('IsOptional')

    @property
    def is_resource(self):
        return self._get('IsResource')

    @property
    def data_store_mode(self):
        return self._get('DataStoreMode')

    @property
    def data_reference_name(self):
        return self._get('DataReferenceName')

    @property
    def dataset_types(self):
        return self._get('DatasetTypes')


class GraphSpecModule(_DictBased):
    @property
    def name(self):
        return self._get('Name')

    @property
    def module_id(self):
        return self._get('ModuleId')

    @property
    def module_name(self):
        return self._get('ModuleName')

    @property
    def class_name(self):
        return self._get('ClassName')

    @property
    def method_name(self):
        return self._get('MethodName')

    @property
    def pip_requirement(self):
        return self._get('PipRequirement')

    @property
    def inputs(self):
        return [GraphSpecModuleInput(input_dict) for input_dict in self._get('Inputs', [])]

    @property
    def module_version(self):
        return self._get('ModuleVersion')


class GraphSpecStaticSource(_DictBased):
    @property
    def id(self):
        return self._get('Id')

    @property
    def type(self):
        return self._get('Type')

    @property
    def data_type_id(self):
        return self._get('DataTypeId')

    @property
    def file_path(self):
        return self._get('FilePath')

    @property
    def model_name(self):
        return self._get('ModelName')

    @property
    def dataset_type(self):
        return self._get('DatasetType')


class GraphSpecInput(_DictBased):
    def __init__(self, dct):
        super().__init__(dct)
        if not self._get('InputPort'):
            raise GraphSpecContentError(f'InputPort field is missing in input {dct}')
        self._port_info = _parse_port_string(self._get('InputPort'))

    @property
    def input_schema(self):
        return json.loads(self._get('InputSchema', '{}'))

    @property
    def port_data_types(self):
        return self._get('PortDataTypes')

    @property
    def port_name(self):
        return self._port_info['port_name']

    @property
    def input_name(self):
        return self._port_info['io_name']

    @property
    def data_type(self):
        return self._port_info['data_type']


class GraphSpecOutput(_DictBased):
    def __init__(self, dct):
        super().__init__(dct)
        if not self._get('OutputPort'):
            raise GraphSpecContentError(f'OutputPort field is missing in output {dct}')
        self._port_info = _parse_port_string(self._get('OutputPort'))

    @property
    def output_schema(self):
        return json.loads(self._get('OutputSchema', '{}'))

    @property
    def port_name(self):
        return self._port_info['port_name']

    @property
    def output_name(self):
        return self._port_info['io_name']

    @property
    def data_type(self):
        return self._port_info['data_type']


class GraphSpec(_DictBased):
    @property
    def id(self):
        return self._get('Id')

    @property
    def nodes(self):
        return _transform_dict_values(self._get('Nodes', {}), GraphSpecNode)

    @property
    def modules(self):
        return _transform_dict_values(self._get('Modules', {}), GraphSpecModule)

    @property
    def static_sources(self):
        return _transform_dict_values(self._get('StaticSources', {}), GraphSpecStaticSource)

    @property
    def static_source_ports(self):
        return _transform_dict_values(self._get('StaticSourcePorts', {}), str)

    @property
    def inputs(self):
        return [GraphSpecInput(entry) for entry in self._get('Inputs', [])]

    @property
    def outputs(self):
        return [GraphSpecOutput(entry) for entry in self._get('Outputs', [])]

    @classmethod
    def load(cls, file_path: Path):
        with open(file_path) as fp:
            graph_spec_dict = json.load(fp)
        return cls(graph_spec_dict)
