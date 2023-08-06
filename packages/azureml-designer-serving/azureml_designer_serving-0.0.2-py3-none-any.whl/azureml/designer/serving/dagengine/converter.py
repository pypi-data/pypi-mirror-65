from pandas import DataFrame
import pandas as pd
import base64

from azureml.studio.core.io.data_frame_directory import DataFrameDirectory
from azureml.studio.core.io.data_frame_visualizer import ElementEncoder
from azureml.studio.core.io.image_directory import ImageDirectory
from azureml.studio.core.io.image_schema import ImageSchema
from azureml.studio.core.data_frame_schema import DataFrameSchema
from azureml.studio.core.logger import get_logger

logger = get_logger(__name__)


def create_dfd_from_dict(json_data, schema_data):
    if schema_data:
        schema = DataFrameSchema.from_dict(schema_data)
        if set(json_data.keys()) != set(schema.column_attributes.names):
            different_names = set(schema.column_attributes.names).difference(set(json_data.keys()))
            raise ValueError(f'Input json_data must have the same column names as the meta data. '
                             f'Different columns are: {different_names}')
        # TODO: Refactor with AnyDirectory.from_json
        try:
            from azureml.studio.common.datatable.data_type_conversion import convert_column_by_element_type
            df = pd.DataFrame()
            for column_name in schema.column_attributes.names:
                column = pd.Series(json_data[column_name])
                target_type = schema.column_attributes[column_name].element_type
                converted_column = convert_column_by_element_type(column, target_type)
                df[column_name] = converted_column
        except ImportError:
            logger.warning("Skip column type conversion because can't import convert_column_by_element_type")
            df = DataFrame(json_data)
        ret = DataFrameDirectory.create(data=df, schema=schema_data)
    else:
        ret = DataFrameDirectory.create(data=DataFrame(json_data))
    return ret


def create_imd_from_dict(json_data, schema_data):
    def string2bytes(image_string):
        image_string = image_string.replace('data:image/png;base64,', '')
        image_string = image_string.replace('data:image/jpeg;base64,', '')
        return base64.b64decode(image_string)
    # Don't change mime type in schema because current implementation of ImageDirectory handles all types of data
    # according to its actual type instead of mime_type in schema
    schema = ImageSchema.from_dict(schema_data)
    image_column_name = schema.get_image_column()
    image_strings = json_data[image_column_name].copy()
    json_data[image_column_name] = [string2bytes(image_string) for image_string in image_strings]
    ret = ImageDirectory.create_from_data(json_data, schema_data)
    return ret


def to_dfd(data):
    ret = data
    if isinstance(data, DataFrameDirectory):
        ret = data
    elif isinstance(data, DataFrame):
        ret = DataFrameDirectory.create(data=data)
    elif isinstance(data, dict):
        ret = DataFrameDirectory.create(data=DataFrame(data))
    elif isinstance(data, str):
        ret = DataFrameDirectory.create(data=DataFrame({'text': [data]}))
    else:
        logger.info(f'pass through the value of type {type(data)}')
    return ret


def to_dict(data):
    ret = None
    if isinstance(data, DataFrameDirectory):
        ret = data.data.to_dict(orient='list')
    elif isinstance(data, DataFrame):
        ret = data.to_dict(orient='list')
    elif isinstance(data, dict):
        ret = data
    else:
        raise NotImplementedError
    # Encode ret to support object columns supported by pipeline: bytes, list, dict
    encoded_ret = {k: [ElementEncoder.encode(item) for item in v] for k, v in ret.items()}
    return encoded_ret
