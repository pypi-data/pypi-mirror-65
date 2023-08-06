from collections import defaultdict
from pathlib import Path
from typing import Tuple
import shutil
import tempfile
import zipfile

from azureml.studio.core.logger import get_logger, TimeProfile
from azureml.studio.core.io.image_directory import ImageDirectory
from azureml.designer.serving.dagengine.constants import GRAPH_SPEC_FILE_NAME
from azureml.designer.serving.dagengine.converter import create_dfd_from_dict, create_imd_from_dict, to_dict
from azureml.designer.serving.dagengine.dag_node import DagNode
from azureml.designer.serving.dagengine.graph_spec import GraphSpec
from azureml.designer.serving.dagengine.score_exceptions import DagNodeExecutionError, InputDataError
from azureml.designer.serving.dagengine.static_source import StaticSource

logger = get_logger(__name__)


class Dag(object):
    """Computation graph in web service"""
    def __init__(self, graph_spec: GraphSpec, artifact_path: Path):
        self._graph_spec = graph_spec
        self._artifact_path = artifact_path

        self._static_sources = {}
        # {node_index_str: DagNode}
        self._nodes = {}
        # {parent_port_name: (node_index, child_port_name)}
        self._port_descendants = defaultdict(list)
        # [node_index_str]
        self._ready_nodes_indexes = []
        # {port_name: value}
        self._global_params = {}
        # {input_name: port_name} e.g. {'WebServiceInput0': '0:InputDataset'}
        self._input_to_node_port_mapping = {}
        # {port_name: output_name} e.g. {'2:OutputDFD': 'WebServiceOutput0'}
        self._node_port_to_output_mapping = {}
        # {port_name: DataType}
        self._input_data_types = {}
        # {input_name: schema}
        self._input_schemas = {}
        # {output_name: schema}
        self._output_schemas = {}
        # {output_name: data_obj}
        self._static_outputs = {}
        self._error_module = ''

        self._load_static_sources()
        self._init_nodes()
        self._init_port_descendants()
        self._init_io()

    @property
    def error_module(self):
        """The name of the module which raised Exception in execution"""
        return self._error_module

    @property
    def input_schemas(self):
        return self._input_schemas

    @classmethod
    def load(cls, file_path: Path, extract_to_path: Path = None):
        """Load from model_package file, which is in zip format"""
        if not extract_to_path:
            extract_to_path = Path(tempfile.TemporaryDirectory().name)
        elif extract_to_path.exists():
            shutil.rmtree(extract_to_path)
        with zipfile.ZipFile(file_path) as zf:
            zf.extractall(extract_to_path)
        graph_spec_path = extract_to_path / GRAPH_SPEC_FILE_NAME
        graph_spec = GraphSpec.load(graph_spec_path)
        return cls(graph_spec, extract_to_path)

    def _load_static_sources(self):
        # {index: StaticSource}
        static_sources = {k: StaticSource.load(v, self._artifact_path)
                          for k, v in self._graph_spec.static_sources.items()}
        # {port_name: index}
        static_source_ports = self._graph_spec.static_source_ports
        # {port_name: StaticSource}
        self._static_sources = {k: static_sources[v] for k, v in static_source_ports.items()}

    def _init_nodes(self):
        for index_str, graph_spec_node in self._graph_spec.nodes.items():
            logger.info(f"initializing node {index_str}")
            graph_spec_module = self._graph_spec.modules[graph_spec_node.module_id]
            self._nodes[index_str] = DagNode(
                graph_spec_node=graph_spec_node,
                graph_spec_module=graph_spec_module,
                loaded_static_sources=self._static_sources
            )

    def _init_port_descendants(self):
        for index_str, graph_spec_node in self._graph_spec.nodes.items():
            for k, v in graph_spec_node.input_port_mappings.items():
                self._port_descendants[v].append((index_str, k))

    def _init_io(self):
        for graph_spec_input in self._graph_spec.inputs:
            self._input_to_node_port_mapping[graph_spec_input.input_name] = graph_spec_input.port_name
            self._input_schemas[graph_spec_input.input_name] = graph_spec_input.input_schema
            self._input_data_types[graph_spec_input.input_name] = graph_spec_input.port_data_types[0]
        for graph_spec_output in self._graph_spec.outputs:
            self._node_port_to_output_mapping[graph_spec_output.port_name] = graph_spec_output.output_name
            self._output_schemas[graph_spec_output.output_name] = graph_spec_output.output_schema
        self._static_outputs = {self._node_port_to_output_mapping[k]: v for k, v in self._static_sources.items()
                                if k in self._node_port_to_output_mapping}

    def _send_dynamic_sources_to_nodes(self, dynamic_sources: dict):
        """Send dynamic sources (module outputs) to the modules which depend on them"""
        for src_port_name, data in dynamic_sources.items():
            for node_index, dst_port_name in self._port_descendants[src_port_name]:
                self._nodes[node_index].add_dynamic_input_data(dst_port_name, data)
                if self._nodes[node_index].is_ready:
                    self._ready_nodes_indexes.append(node_index)

    def _execute(self, inputs, global_parameters):
        """Execute with input data(data object, etc. DFD, ImageDirectory, ...)

        :param inputs: {port_name: data_obj}
        :param global_parameters:
        :return:
        """

        dynamic_outputs = {}
        self._send_dynamic_sources_to_nodes(inputs)
        while self._ready_nodes_indexes:
            node_index = self._ready_nodes_indexes.pop()
            node = self._nodes[node_index]
            with TimeProfile(f"Executing node {node_index}: {node.module_name}"):
                node_global_params = {k: global_parameters[v] for k, v in node.global_parameter_mappings}
                try:
                    node_outputs = node.execute(node_global_params)
                except BaseException as e:
                    self._error_module = node.module_name
                    raise DagNodeExecutionError(node_index, node.module_name) from e
                for port_name, data in node_outputs.items():
                    if port_name in self._node_port_to_output_mapping:
                        dynamic_outputs[self._node_port_to_output_mapping[port_name]] = data
                self._send_dynamic_sources_to_nodes(node_outputs)
        return dynamic_outputs

    def execute(self, inputs, global_parameters) -> Tuple[dict, dict]:
        """Execute with input of raw data(str)

        :param inputs: {input_name: raw_data}
        :param global_parameters:
        :return: (outputs, output_schemas)
        """
        if set(inputs.keys()) != set(self._input_to_node_port_mapping.keys()):
            raise InputDataError(self._input_to_node_port_mapping, inputs)
        graph_inputs = {}
        for input_name, raw_input in inputs.items():
            port_name = self._input_to_node_port_mapping[input_name]
            schema = self._input_schemas[input_name]
            input_data_type = self._input_data_types[input_name]
            try:
                if input_data_type == ImageDirectory.TYPE_NAME:
                    input_data = create_imd_from_dict(raw_input, schema)
                else:
                    input_data = create_dfd_from_dict(raw_input, schema)
            except Exception:
                raise InputDataError(schema, raw_input)
            graph_inputs[port_name] = input_data
        dynamic_outputs = self._execute(graph_inputs, global_parameters)
        outputs = dict(**self._static_outputs, **dynamic_outputs)
        # TODO: Support ImageDirectory as output, of which currently there is no use case
        outputs_as_dicts = {k: to_dict(v) for k, v in outputs.items()}
        return outputs_as_dicts, self._output_schemas

    def clear_dynamic_data(self):
        """Reset graph for the next execution"""
        for _, node in self._nodes.items():
            node.clear_dynamic_input_data()
