import traceback

from azureml.studio.core.error import UserError


class InputDataError(UserError):
    def __init__(self, schema, data, with_traceback=True):
        errmsg = f'Input data are inconsistent with schema.\nSchema: {str(schema)[:256]}\nData: {str(data)[:256]}'
        if with_traceback:
            errmsg += '\n'
            errmsg += traceback.format_exc()
        super().__init__(errmsg)


class ResourceLoadingError(Exception):
    def __init__(self, name, type_name, with_traceback=True):
        errmsg = f'Failed to load {type_name} {name} from Model'
        if with_traceback:
            errmsg += '\n'
            errmsg += traceback.format_exc()
        super().__init__(errmsg)


class GraphSpecContentError(Exception):
    pass


class ModuleErrorPlaceHolder(Exception):
    pass


class DagNodeExecutionError(Exception):
    def __init__(self, node_id, module_name):
        super().__init__(f"Error occurs when executing node {node_id} with module {module_name}.")
