import os
from pathlib import Path

from azureml.designer.serving.dagengine.graph_spec import GraphSpecStaticSource
from azureml.designer.serving.dagengine.score_exceptions import ResourceLoadingError
from azureml.studio.core.io.any_directory import AnyDirectory
from azureml.studio.core.logger import get_logger, TimeProfile

logger = get_logger(__name__)


class StaticSource(object):
    """Static resources stored in model_package"""
    def __init__(self, data):
        """Init func

        :param data:
        """
        self.data = data

    @classmethod
    def load(cls,
             graph_spec_static_source: GraphSpecStaticSource,
             artifact_path: Path):
        """Load from graph_spec StaticSource

        :param graph_spec_static_source:
        :param artifact_path:
        :return:
        """
        with TimeProfile(f'Loading static source {graph_spec_static_source.model_name}'):
            try:
                directory_path = artifact_path / graph_spec_static_source.model_name
                data = AnyDirectory.load_dynamic(directory_path)
            except BaseException:
                logger.warning(f"Failed to load static source from {artifact_path}, "
                               f"fall back to legacy logic.", exc_info=True)
                data = _legacy_load_logic(graph_spec_static_source, artifact_path)

            return cls(data)


def _legacy_load_logic(
        graph_spec_static_source: GraphSpecStaticSource,
        artifact_path: Path):
    try:
        from azureml.studio.common.datatypes import DataTypes
        TYPE_NAME_2_DATA_TYPE = {
            'TrainedModel': DataTypes.LEARNER,
            'TransformModule': DataTypes.TRANSFORM,
            'FilterModule': DataTypes.FILTER,
            'ClusterModule': DataTypes.CLUSTER,
            'DataSource': None
        }
    except ImportError:
        logger.warning("Can't import DataTypes from azureml.studio.common.datatypes")
        TYPE_NAME_2_DATA_TYPE = {}

    TYPE_ID_2_FILE_NAME = {
        'IClusterDotNet': 'data.icluster',
        'ITransformDotNet': 'data.itransform',
        'TransformationDirectory': 'data.itransform'
    }

    try:
        # 'ModelDirectory' 'TransformDirectory' 'AnyDirectory' 'DataFrameDirectory' 'AnyFile'
        is_path = graph_spec_static_source.data_type_id in ('GenericFolder', 'AnyFile') or \
                  'Directory' in graph_spec_static_source.data_type_id
        if graph_spec_static_source.data_type_id:
            logger.info(f"graph_spec_static_source.data_type_id = {graph_spec_static_source.data_type_id}")
            if is_path:
                data_type = None
            else:
                try:
                    from azureml.studio.common.datatypes import DataTypes
                    data_type = DataTypes.from_name(graph_spec_static_source.data_type_id)
                except ImportError:
                    logger.warning(f'Failed to get data_type from {graph_spec_static_source.data_type_id}',
                                   exc_info=True)
                    data_type = None
        else:
            logger.warning(f'StaticSource({graph_spec_static_source}) has no data_type_id')
            data_type = TYPE_NAME_2_DATA_TYPE[graph_spec_static_source.type]

        path = artifact_path / graph_spec_static_source.model_name

        if graph_spec_static_source.data_type_id in ('ModelDirectory', 'DataFrameDirectory') and path.is_dir():
            try:
                from azureml.studio.modulehost.handler.port_io_handler import InputHandler
                data = InputHandler.handle_input_directory(path)
                logger.debug(f"loaded {data} from {path} by InputHandler.handle_input_directory")
            except (ImportError, TypeError, FileNotFoundError):
                logger.warning(f'Failed to handle {path} with InputHandler, fall back to path.', exc_info=True)
                data = path
        elif graph_spec_static_source.data_type_id in TYPE_ID_2_FILE_NAME:
            if path.is_dir():
                path = path / TYPE_ID_2_FILE_NAME[graph_spec_static_source.data_type_id]
            if not path.is_file():
                raise ResourceLoadingError(graph_spec_static_source.model_name,
                                           graph_spec_static_source.data_type_id)
            from azureml.studio.modulehost.handler.port_io_handler import InputHandler
            data = InputHandler.handle_input_from_file_name(path, data_type)
        elif graph_spec_static_source.type == 'TrainedModel' and \
                graph_spec_static_source.data_type_id == "ILearnerDotNet" and path.is_file():
            from azureml.studio.modulehost.handler.port_io_handler import InputHandler
            from azureml.studio.common.datatypes import DataTypes
            data = InputHandler.handle_input_from_file_name(path, DataTypes.LEARNER)
        elif graph_spec_static_source.type == 'TrainedModel' and path.is_dir():
            ilearner_path = path / 'data.ilearner'
            metadata_path = path / 'data.metadata'
            if ilearner_path.exists() and metadata_path.exists():
                from azureml.studio.modulehost.handler.port_io_handler import InputHandler
                from azureml.studio.common.datatypes import DataTypes
                data = InputHandler.handle_input_from_file_name(ilearner_path, DataTypes.LEARNER)
            else:
                data = path
        elif is_path and os.path.isdir(path):
            data = path
        else:
            from azureml.studio.modulehost.handler.port_io_handler import InputHandler
            data = InputHandler.handle_input_from_file_name(path, data_type)
            logger.debug(f"loaded {data} from {path} by InputHandler.handle_input_from_file_name")
        return data
    except ResourceLoadingError:
        raise
    except Exception as ex:
        logger.error(f'Error while loading {graph_spec_static_source}: {ex}')
        raise ResourceLoadingError(graph_spec_static_source.model_name, graph_spec_static_source.data_type_id)
