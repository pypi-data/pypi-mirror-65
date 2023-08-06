import importlib

from azureml.designer.serving.dagengine.constants import STANDARD_CUSTOM_MODULE_ON_INIT_METHOD_NAME
from azureml.designer.serving.dagengine.graph_spec import GraphSpecNode, GraphSpecModule
from azureml.designer.serving.dagengine.module_host import OfficialModuleHost, StandardCustomModuleHost,\
    LegacyCustomModuleHost


def _remove_index_in_key(d: dict):
    return {k.split(':')[-1]: v for k, v in d.items()}


class DagNode(object):
    """Node data structure in Dag"""
    def __init__(self,
                 graph_spec_node: GraphSpecNode,
                 graph_spec_module: GraphSpecModule,
                 loaded_static_sources: dict = None
                 ):
        self._graph_spec_node = graph_spec_node
        self._graph_spec_module = graph_spec_module
        self._parameters = graph_spec_node.parameters
        self._input_ports = list(graph_spec_node.input_port_mappings.keys())
        self._output_ports = graph_spec_node.output_ports
        self._static_input_data = {k: loaded_static_sources[v] for k, v in
                                   self._graph_spec_node.input_port_mappings.items() if v in loaded_static_sources}
        self._module_host = self._init_module_host()
        self._dynamic_input_data = {}

    @property
    def module_name(self):
        return self._graph_spec_module.name

    @property
    def global_parameter_mappings(self):
        return self._graph_spec_node.global_parameter_mappings

    @property
    def is_ready(self):
        return len(self._dynamic_input_data) + len(self._static_input_data) == len(self._input_ports)

    def add_dynamic_input_data(self, port_name, data):
        self._dynamic_input_data[port_name] = data

    def clear_dynamic_input_data(self):
        self._dynamic_input_data = {}

    def _init_module_host(self):
        module_name = self._graph_spec_module.module_name
        class_name = self._graph_spec_module.class_name
        is_official = module_name.startswith('azureml.studio.')
        static_source_dict = {k: v.data for k, v in self._static_input_data.items()}
        if is_official:
            module_host = OfficialModuleHost(
                module_name=module_name,
                class_name=class_name,
                method_name=self._graph_spec_module.method_name,
                static_source_dict=_remove_index_in_key(static_source_dict),
                parameters=self._parameters
            )
        else:
            module_module = importlib.import_module(module_name)
            module_class = getattr(module_module, class_name)
            if hasattr(module_class, STANDARD_CUSTOM_MODULE_ON_INIT_METHOD_NAME):
                module_host = StandardCustomModuleHost(
                    module_name=module_name,
                    class_name=class_name,
                    static_source_dict=_remove_index_in_key(static_source_dict),
                    parameters=self._parameters,
                    input_port_arg_names=[module_input.name for module_input in self._graph_spec_module.inputs]
                )
            else:
                module_host = LegacyCustomModuleHost(
                    module_name=module_name,
                    class_name=class_name,
                    method_name=self._graph_spec_module.method_name,
                    static_source_dict=_remove_index_in_key(static_source_dict),
                    parameters=self._parameters,
                    input_port_arg_names=[module_input.name for module_input in self._graph_spec_module.inputs]
                )

        return module_host

    def execute(self, global_params=None):
        global_params = global_params or {}
        results = self._module_host.execute(
            dynamic_source_dict=_remove_index_in_key(self._dynamic_input_data),
            global_parameters=global_params
        )
        output_data = {output_port: results[index] for index, output_port in enumerate(self._output_ports)}
        return output_data
