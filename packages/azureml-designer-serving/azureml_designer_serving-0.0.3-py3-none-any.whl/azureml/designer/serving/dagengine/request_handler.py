import importlib
import json
import traceback

from azureml.studio.core.logger import get_logger, TimeProfile
from azureml.designer.serving.dagengine.utils import NpEncoder
from azureml.designer.serving.dagengine.processor import ClassicProcessor, NewProcessor
from azureml.designer.serving.dagengine.score_exceptions import InputDataError
try:
    from azureml.studio.internal.error import ModuleError
except ImportError:
    from azureml.designer.serving.dagengine.score_exceptions import ModuleErrorPlaceHolder as ModuleError
try:
    from azureml.studio.common.error import ModuleError as LegacyModuleError
except ImportError:
    LegacyModuleError = ModuleError

logger = get_logger(__name__)
is_rawhttp = False


def enable_rawhttp():
    global is_rawhttp
    if importlib.util.find_spec('azureml.contrib.services'):
        from azureml.contrib.services.aml_request import rawhttp
        rawhttp(None)
        is_rawhttp = True
    else:
        is_rawhttp = False
        logger.warning('RAWHTTP is not enabled!')


def _construct_errmsg(code, message, details):
    return {'error': {'code': code, 'message': message, 'details': details}}


def _construct_response(message, code, json_str):
    if is_rawhttp:
        from azureml.contrib.services.aml_response import AMLResponse
        ret = AMLResponse(message, code, json_str=json_str)
        ret.headers['Access-Control-Allow-Origin'] = '*'
    else:
        ret = message
    return ret


def handle_request(dag, raw_data, args):
    verbose = False
    try:
        with TimeProfile('Handling http request'):
            request_format = args.get('format', 'swagger')
            is_classic = request_format != 'swagger'
            with_details = args.get('details', 'false').lower() == 'true'
            verbose = args.get('verbose', 'false').lower() == 'true'
            logger.info(f'Run: is_classic = {is_classic}, with_details = {with_details}, verbose = {verbose}')

            if is_classic:
                processor = ClassicProcessor(dag, with_details)
            else:
                processor = NewProcessor(dag)
            response = processor.run(raw_data)
        response_string = json.dumps(response, cls=NpEncoder)
        logger.info(f'Run: output data(raw) = {response_string}')
        ret = _construct_response(response_string, 200, json_str=False)

    except InputDataError as ex:
        error = str(ex)
        logger.error(error, exc_info=True)
        errmsg = _construct_errmsg(400, f'Input Data Error. {error}', '')
        ret = _construct_response(errmsg, 400, json_str=True)

    except ModuleError as ex:
        error = f'Run: User input error is from {dag.error_module} : {ex}'
        logger.error(error, exc_info=True)
        errmsg = _construct_errmsg(400, f'Module Executing Error. {error}', '')
        ret = _construct_response(errmsg, 400, json_str=True)

    except LegacyModuleError as ex:
        error = f'Run: User input error is from {dag.error_module} : {ex}'
        logger.error(error, exc_info=True)
        errmsg = _construct_errmsg(400, f'Module Executing Error. {error}', '')
        ret = _construct_response(errmsg, 400, json_str=True)

    except Exception as ex:
        error = 'Run: Server internal error'
        if dag.error_module:
            error += f' is from Module {dag.error_module}'
        logger.error(f'{error} : {ex}', exc_info=True)
        if verbose:
            error += f' : {ex}\n'
            error += traceback.format_exc()
        errmsg = _construct_errmsg(500, f'Internal Server Error. {error}', '')
        ret = _construct_response(errmsg, 500, json_str=True)

    return ret


def handle_not_supported(request):
    error = f'"{request.method}" is not supported'
    logger.error(error)
    errmsg = _construct_errmsg(400, 'HTTP Method Not Supported', error)
    ret = _construct_response(errmsg, 400, json_str=True)
    return ret
