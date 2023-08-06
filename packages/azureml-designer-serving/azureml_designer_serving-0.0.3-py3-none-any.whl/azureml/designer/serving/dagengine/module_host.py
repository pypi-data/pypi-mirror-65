import importlib
import inspect
from abc import ABC, abstractmethod
from copy import deepcopy

from azureml.designer.serving.dagengine.constants import STANDARD_CUSTOM_MODULE_ON_INIT_METHOD_NAME
from azureml.studio.core.io.data_frame_directory import DataFrameDirectory
from azureml.studio.core.io.model_directory import ModelDirectory
from azureml.studio.core.io.transformation_directory import TransformationDirectory
from azureml.studio.core.logger import get_logger


logger = get_logger(__name__)


# TODO: Let SMT filter out non-UX represented parameters or add tag to distinguish that.
class ModuleHost(ABC):

    @abstractmethod
    def execute(self, dynamic_source_dict: dict, global_parameters: dict):
        pass


class OfficialModuleHost(ModuleHost):
    def __init__(self,
                 module_name,
                 class_name,
                 method_name,
                 static_source_dict: dict,
                 parameters: dict
                 ):
        # Temp workaround for graph without official module
        from azureml.studio.common.datatable.data_table import DataTable
        from azureml.studio.modulehost.module_reflector import ModuleEntry
        from azureml.studio.modulehost.deployment_service_module_host import DeploymentServiceModuleHost
        module_entry = ModuleEntry(module_name, class_name, method_name)
        self._module_host = DeploymentServiceModuleHost(module_entry)
        unfolded_resource_dict = {}
        for k, v in static_source_dict.items():
            # This is contract with core regarding official static sources, i.e. ModelDirectory, TransformationDirectory
            # TODO: Refactor deployment_service_module_host to avoid doing these data transformations here.
            if isinstance(v, (ModelDirectory, TransformationDirectory)):
                unfolded_resource_dict[k] = v.data
            elif isinstance(v, DataFrameDirectory):
                unfolded_resource_dict[k] = DataTable.from_dfd(v)
            else:
                unfolded_resource_dict[k] = v
        self._module_host.resources_dict = deepcopy(unfolded_resource_dict)
        self._module_host.parameters_dict = deepcopy(parameters)

    def execute(self, dynamic_source_dict: dict, global_parameters: dict):
        return self._module_host.execute(deepcopy(dynamic_source_dict), deepcopy(global_parameters))


class LegacyCustomModuleHost(ModuleHost):
    def __init__(self,
                 module_name: str,
                 class_name: str,
                 method_name: str,
                 static_source_dict: dict,
                 parameters: dict,
                 input_port_arg_names: list
                 ):
        self.module = importlib.import_module(module_name)
        self.method_name = method_name
        self.module_class = getattr(self.module, class_name)
        self.static_source_dict = static_source_dict
        self.parameters = parameters
        self.input_port_arg_names = input_port_arg_names
        self.module_instance = self.module_class(deepcopy(parameters))
        self.module_run = getattr(self.module_instance, self.method_name)

    def execute(self, dynamic_source_dict: dict, global_parameters: dict):
        source_dict = {**self.static_source_dict, **dynamic_source_dict}
        run_args = [source_dict.get(arg_name, None) for arg_name in self.input_port_arg_names]
        params = {**self.parameters, **global_parameters}
        run_args.append(params)
        ret = self.module_run(*deepcopy(run_args))
        if not isinstance(ret, (tuple, list)):
            return ret,
        return ret


class StandardCustomModuleHost(ModuleHost):
    def __init__(self,
                 module_name: str,
                 class_name: str,
                 static_source_dict: dict,
                 parameters: dict,
                 input_port_arg_names: list
                 ):
        self.module = importlib.import_module(module_name)
        self.module_class = getattr(self.module, class_name)
        self.static_source_dict = static_source_dict
        self.parameters = parameters
        self.module_instance = self.module_class()
        self.input_port_arg_names = input_port_arg_names
        if hasattr(self.module_instance, STANDARD_CUSTOM_MODULE_ON_INIT_METHOD_NAME):
            kwargs = {k: None for k in self.input_port_arg_names}
            available_kwargs = dict(**static_source_dict, **parameters)
            kwargs.update(available_kwargs)
            normalized_kwargs = StandardCustomModuleHost._normalize_kwargs(kwargs, self.module_instance.on_init)
            self.module_instance.on_init(**deepcopy(normalized_kwargs))

    def execute(self, dynamic_source_dict: dict, global_parameters: dict):
        kwargs = {k: None for k in self.input_port_arg_names}
        available_kwargs = dict(**self.static_source_dict, **dynamic_source_dict,
                                **self.parameters, **global_parameters)
        kwargs.update(available_kwargs)
        normalized_kwargs = StandardCustomModuleHost._normalize_kwargs(kwargs, self.module_instance.run)
        return self.module_instance.run(**deepcopy(normalized_kwargs))

    @classmethod
    def _to_variable_name(cls, origin_name):
        return origin_name.lower().replace(' ', '_')

    @classmethod
    def _normalize_kwargs(cls, kwargs, func):
        normalized_kwargs = {StandardCustomModuleHost._to_variable_name(k): v for k, v in kwargs.items()}
        if inspect.getfullargspec(func).varkw:
            return normalized_kwargs
        else:
            return {k: normalized_kwargs.get(k, None) for k in inspect.getfullargspec(func).args if k != "self"}
