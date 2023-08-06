import re

from azureml.core import Datastore
from azureml.dataprep.api.dataflow import Dataflow
import azureml.dataprep as dataprep
from azureml.studio.core.error import UserError
from azureml.studio.core.io.any_directory import DirectoryIOError
from azureml.studio.core.logger import logger, time_profile
from azureml.studio.core.io.data_frame_directory import DataFrameDirectory
from azureml.data.datapath import DataPath
from azureml.dataprep import read_pandas_dataframe
from pandas import DataFrame
from ..common.workspaceutil import get_workspace, get_time_as_string
from ..common.commonerrorutil import EXPORT_USER_ERROR_GROUP, get_error_group
from azureml.studio.internal.error import ErrorMapping, \
    UnsupportedOutputTypeError, TimeoutOccuredError, IncorrectAzureMLDatastoreError, ParameterParsingError, \
    InvalidDatasetError, NoColumnsSelectedError, ColumnCountNotEqualError
from azureml.studio.internal.error_handler import error_handler
from azureml.dataprep import ColumnSelector
from azureml.dataprep.api.step import column_selection_to_selector_value
import argparse
import os
import azureml.core

logger.debug(f'Executing {os.path.abspath(__file__)}')
logger.debug(f"Azure ML SDK Version: {azureml.core.VERSION}")
logger.debug(f"DataPrep Version: {azureml.dataprep.__version__}")
logger.debug(
    f"azureml.designer.modules.dataio Version: {azureml.designer.modules.dataio.__version__}")


def check_url_format(url_str):
    """Check if input string is a url"""
    result = re.search('^(abfss|adl|https?)://.*$', url_str)
    return True if result else False


class SqlDataTypeRanges:
    BIGINT = (-2**63, 2**63-1)
    INT = (-2**31, 2**31-1)
    SMALLINT = (-2**15, 2**15-1)
    TINYINT = (0, 255)
    NVARCHAR = (0, 50)
    FLOAT = (-1.79E+308, 1.79E+308)


class ExportTabularDataModule:
    @classmethod
    def __init__(cls, input_dict):
        cls.output_datastore = input_dict['Output_data_store']
        cls.output_path = input_dict['Output_path']
        cls.file_type = input_dict['Output_file_type']
        cls.workspace = get_workspace()
        cls.column_list_to_be_saved = input_dict['Column_list_to_be_saved']
        cls.datatable_name = input_dict['Datatable_name']
        cls.column_list_datatable_columns = input_dict['Column_list_datatable_columns']
        cls.number_rows_per_operation = input_dict['Number_rows_per_operation']
        cls.datastore_type = input_dict['Datastore_type']

    @classmethod
    @time_profile
    def write_to_csv(
            cls,
            data_flow,
            directory_path,
            separator=',',
            na='NA',
            error='ERROR',
            single_file=True) -> Dataflow:
        """
        Create a dataflow sequence for exporting as csv. It is almost a copy of Datafow.write_to_csv
        except adding singleFile parameter to it
        """
        from azureml.dataprep.api._datastore_helper import get_datastore_value
        logger.info(f'Export CSV to datastore: {directory_path.datastore_name}')

        data_flow = data_flow.add_step('Microsoft.DPrep.WriteCsvToDatastoreBlock', {
            'datastore': get_datastore_value(directory_path)[1]._to_pod(),
            'separator': separator,
            'singleFile': single_file,
            'na': "",
            'error': error
        })
        return data_flow

    @classmethod
    def get_dataframe_profile(cls, data_flow):
        profile_dict = {}
        profile_columns = data_flow.get_profile().columns
        for key, val in profile_columns.items():
            val = profile_columns[key]
            val_tuple = (val.type.name, val.min, val.max)
            profile_dict[key] = val_tuple
        return profile_dict

    @classmethod
    def get_database_schema(cls, sql_datastore_name, table_name):
        sql_datastore = Datastore.get(cls.workspace, sql_datastore_name)
        sql_query_schema = f"SELECT COLUMN_NAME,DATA_TYPE,CHARACTER_MAXIMUM_LENGTH,IS_NULLABLE FROM " \
                           f"INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='{table_name}'"
        dest_dflow = dataprep.read_sql(sql_datastore, sql_query_schema)
        try:
            table_schema = dest_dflow.to_pandas_dataframe()
            return table_schema
        except Exception as db_exceptions:
            error_message = str(db_exceptions)
            error_code = getattr(db_exceptions, 'error_code', '')
            if error_code != '':
                if error_code in ['AuthenticationFailure', 'DatabaseConnectionError', 'AuthenticationContextMismatch',
                                  'UnexpectedAccessError', 'UnauthorizedAccess', 'OutOfMemory', 'DatabaseLoginError']:
                    ErrorMapping.rethrow(db_exceptions, UserError(error_message))
            network_server_error_group = get_error_group(error_message)
            if network_server_error_group == 'ServerBusy' or network_server_error_group == 'connection issues':
                hint_message = network_server_error_group + ' Please retry. ' + error_message
                ErrorMapping.rethrow(db_exceptions, UserError(hint_message))
            raise db_exceptions

    @classmethod
    def get_converted_type(cls, key):
        switcher = {
            'INTEGER': ['BIGINT', 'INT', 'SMALLINT', 'TINYINT'],
            'DECIMAL': 'FLOAT',
            'STRING': 'NVARCHAR',
            'BOOLEAN': 'BIT',
            'DATE': 'DATETIME2'
        }
        return switcher.get(key, "Invalid type conversions.")

    @classmethod
    def validate_compatibility(cls, df_schema, table_schema):
        table_schema_dict = dict(zip(table_schema['COLUMN_NAME'], table_schema['DATA_TYPE']))
        error_msg = ''
        for key, df_value in df_schema.items():
            if key not in table_schema_dict:
                error_msg += f'{key} is not present in sql table schema,\n'
                continue

            table_col_type = table_schema_dict[key].upper()
            df_col_type = df_value[0].upper()

            if df_col_type == 'INTEGER' and table_col_type not in cls.get_converted_type(df_col_type):
                error_msg += f'{df_col_type} will not be converted to {table_col_type},\n'
            if df_col_type != 'INTEGER' and table_col_type != cls.get_converted_type(df_col_type):
                error_msg += f'{df_col_type} will not be converted to {table_col_type},\n'
            # do not check value range for str, bool, date types
            if df_col_type in ['STRING', 'BOOLEAN', 'DATE']:
                continue

            sql_type_range = getattr(SqlDataTypeRanges, table_col_type)
            if (sql_type_range is not None) and (df_value[1] < sql_type_range[0] or df_value[2] > sql_type_range[1]):
                error_msg += f'(For {key}, profile value range [{df_value[1]}, {df_value[2]}]) ' \
                             f'is not compatible with sql type {table_col_type} range ' \
                             f'[{sql_type_range[0]}, {sql_type_range[1]}],\n'

        if len(error_msg) > 0:
            ErrorMapping.throw(UserError({error_msg}))
        return True

    @classmethod
    def generate_to_nonsql_dataflow(cls, input_port_dfd: DataFrameDirectory,
                                    input_dict: dict = None) -> Dataflow:

        null_keys = [key for key, value in input_dict.items()
                     if key in ['Output_data_store', 'Output_path', 'Output_file_type'] and value is None]
        if len(null_keys) > 0:
            ErrorMapping.throw(ParameterParsingError(arg_name_or_column=', '.join(null_keys)))

        cls.output_datastore = input_dict['Output_data_store']
        cls.output_path = input_dict['Output_path']
        cls.file_type = input_dict['Output_file_type']

        if cls.output_path == '\\' or cls.output_path == "\\\\" or cls.output_path.endswith('/')\
                or cls.output_path.endswith('.') or check_url_format(cls.output_path):
            ErrorMapping.throw(ParameterParsingError(arg_name_or_column='Output_path'))
        if isinstance(input_port_dfd, DataFrameDirectory):
            data_frame = input_port_dfd.data
            logger.info(f"Input port is DFD type: {input_port_dfd}.")
        elif isinstance(input_port_dfd, DataFrame):
            data_frame = input_port_dfd
            logger.info(f"Input port is pandas data frame type.")
        else:
            logger.error(f"Unsupported input_port_dfd type.")
            raise NotImplementedError(
                'Not support non-DataFrameDirectory or non-DataFrame type.')

        # check if pandas DataFrame is empty
        if len(data_frame.index) == 0 or len(data_frame.columns) == 0:
            ErrorMapping.throw(InvalidDatasetError())

        data_flow = read_pandas_dataframe(df=data_frame, in_memory=True)
        data_flow = data_flow.add_step(
            'Microsoft.DPrep.DropColumnsBlock', {
                'columns': column_selection_to_selector_value(
                    ColumnSelector(
                        '__index_level_*', True, True))})

        data_store = Datastore.get(cls.workspace, cls.output_datastore)
        data_path = DataPath(data_store, cls.output_path)
        file_format = cls.file_type.lower()
        if file_format == 'csv':
            data_flow = cls.write_to_csv(
                data_flow, data_path, single_file=True)
        elif file_format == 'tsv':
            data_flow = cls.write_to_csv(
                data_flow, data_path, separator='\t', single_file=True)
        elif file_format == 'parquet':
            # logger.debug(f"parquet file dtypes:\n{data_flow.dtypes}")
            data_flow = data_flow.write_to_parquet(
                data_path, single_file=True)
        else:
            ErrorMapping.throw(UnsupportedOutputTypeError())
        return data_flow

    @classmethod
    def generate_to_sql_dataflow(cls, input_port_dfd: DataFrameDirectory,
                                 input_dict: dict = None) -> Dataflow:
        null_keys = [key for key, value in input_dict.items()
                     if key in ['Output_data_store', 'Datatable_name'] and value is None]
        if len(null_keys) > 0:
            ErrorMapping.throw(ParameterParsingError(arg_name_or_column=', '.join(null_keys)))

        cls.output_datastore = input_dict['Output_data_store']
        cls.column_list_to_be_saved = input_dict['Column_list_to_be_saved']
        cls.datatable_name = input_dict['Datatable_name']
        cls.column_list_datatable_columns = input_dict['Column_list_datatable_columns']
        cls.number_rows_per_operation = input_dict['Number_rows_per_operation']

        data_store = Datastore.get(cls.workspace, cls.output_datastore)

        if isinstance(input_port_dfd, DataFrameDirectory):
            data_frame = input_port_dfd.data
            logger.info(f"Input port is DFD type: {input_port_dfd}.")
        elif isinstance(input_port_dfd, DataFrame):
            data_frame = input_port_dfd
            logger.info(f"Input port is pandas data frame type.")
        else:
            logger.error(f"Unsupported input_port_dfd type.")
            raise NotImplementedError(
                'Not support non-DataFrameDirectory or non-DataFrame type.')

        # check if a pandas DataFrame is empty
        if len(data_frame.index) == 0 or len(data_frame.columns) == 0:
            ErrorMapping.throw(InvalidDatasetError())

        data_flow = read_pandas_dataframe(df=data_frame, in_memory=True)
        data_flow = data_flow.add_step(
            'Microsoft.DPrep.DropColumnsBlock', {
                'columns': column_selection_to_selector_value(
                    ColumnSelector(
                        '__index_level_*', True, True))})

        all_columns = dataprep.ColumnSelector(term=".*", use_regex=True)
        drop_if_all_null = [all_columns, dataprep.ColumnRelationship(dataprep.ColumnRelationship.ALL)]
        data_flow = data_flow.replace_na(columns=all_columns).drop_nulls(*drop_if_all_null)
        df_schema = cls.get_dataframe_profile(data_flow)

        # select columns from pandas DataFrame
        columns_list = [col.strip() for col in cls.column_list_to_be_saved.split(',')]
        columns_to_selected = set(columns_list)
        columns_df = set([*df_schema])
        if not columns_to_selected.issubset(columns_df):
            ErrorMapping.throw(NoColumnsSelectedError(column_set=cls.column_list_to_be_saved))
        data_flow = data_flow.keep_columns(columns=columns_list)

        # rename columns in pandas DataFrame
        column_list_datatable = [col.strip() for col in cls.column_list_datatable_columns.split(',')]
        column_list_saved = [col.strip() for col in cls.column_list_to_be_saved.split(',')]
        if len(column_list_saved) != len(column_list_datatable):
            ErrorMapping.throw(ColumnCountNotEqualError(column_count_1=len(column_list_saved),
                                                        column_count_2=len(column_list_datatable)))
        column_pairs = {}
        for i in range(len(column_list_datatable)):
            old_name = column_list_saved[i]
            new_name = column_list_datatable[i]
            if old_name != new_name:
                column_pairs[old_name] = new_name
        data_flow = data_flow.rename_columns(column_pairs=column_pairs)

        # regenerate DataFrame profile since columns may be selected or renamed
        df_schema = cls.get_dataframe_profile(data_flow)
        table_schema = cls.get_database_schema(cls.output_datastore, cls.datatable_name)
        if table_schema.shape == (0, 0):
            data_flow = data_flow.write_to_sql(data_store, cls.datatable_name,
                                               batch_size=cls.number_rows_per_operation)
        else:
            cls.validate_compatibility(df_schema, table_schema)
            data_flow = data_flow.write_to_sql(data_store, cls.datatable_name,
                                               batch_size=cls.number_rows_per_operation)
        return data_flow

    @classmethod
    # @ErrorHandler('./error_folder')
    @error_handler
    @time_profile
    def run(cls, input_port_dfd: DataFrameDirectory,
            input_dict: dict = None) -> None:
        """
        Export data to various datastore (blob, adls gen1, adls gen2, sql), dprep will handle the detail
          For non-sql datastore:
            1. generate exporting dataflow sequence
            2. create output_path
            3. execute dataflow for exporter
          For sql datastore:
            1. select columns using column_list_to_be_saved
            2. rename columns using column_list_datatable_columns
            3. get table schema
            4. get dataframe profile
            5. write to sql datastore if dataframe profile is compatible with table schema
        """
        try:
            if input_dict['Output_data_store'] is None:
                ErrorMapping.throw(ParameterParsingError(arg_name_or_column='Output_data_store'))

            cls.output_datastore = input_dict['Output_data_store']
            data_store = Datastore.get(cls.workspace, cls.output_datastore)
            if data_store.datastore_type in ['AzureBlob', 'AzureFile', 'AzureDataLake', 'AzureDataLakeGen2']:
                data_flow = cls.generate_to_nonsql_dataflow(input_port_dfd, input_dict)
            elif data_store.datastore_type == 'AzureSqlDatabase':
                data_flow = cls.generate_to_sql_dataflow(input_port_dfd, input_dict)
            else:
                raise NotImplementedError

            step_types = [s.step_type for s in data_flow._steps]
            logger.info(f'Data flow:{step_types}')
            data_flow.run_local()
            logger.info(f"{get_time_as_string()} Export data is done.")
        except Exception as export_exceptions:
            error_message = str(export_exceptions)
            error_code = getattr(export_exceptions, 'error_code', '')
            if error_code != '' and \
                    error_code in ['InvalidPath', 'AuthenticationFailure', 'QueryExecutionError',
                                   'DatabaseConnectionError', 'AuthenticationContextMismatch', 'FailedToReadDataFrame',
                                   'UnexpectedAccessError', 'UnsupportedParquetFile', 'PathTooLong',
                                   'PyArrowMissing', 'OutOfMemory', 'DatabaseLoginError']:
                ErrorMapping.rethrow(export_exceptions, UserError(error_message))

            if 'Could not find datastore' in error_message:
                ErrorMapping.rethrow(export_exceptions, IncorrectAzureMLDatastoreError(
                                                        datastore_name=cls.output_datastore,
                                                        workspace_name=cls.workspace))
            elif any(m in error_message for m in EXPORT_USER_ERROR_GROUP):
                ErrorMapping.rethrow(export_exceptions, UserError(error_message))
            elif 'Cannot access destination table' in str(error_message):
                hint_message = 'Table name follows Sql server identifier naming convention. Please retry. '
                ErrorMapping.rethrow(export_exceptions, UserError(hint_message + error_message))
            else:
                raise export_exceptions

            network_server_error_group = get_error_group(error_message)
            if network_server_error_group == 'ServerBusy' or network_server_error_group == 'connection issues':
                hint_message = network_server_error_group + ' Please retry. ' + error_message
                ErrorMapping.rethrow(export_exceptions, UserError(hint_message))
            if network_server_error_group == 'memory allocation failures':
                hint_message = 'Out of memory, please try upgrade compute. ' + error_message
                ErrorMapping.rethrow(export_exceptions, UserError(hint_message))
            raise export_exceptions


@time_profile
def main(args):
    """Initialize an export tabular data module and export data to the specified data store and data path"""
    logger.info(f'Received argument --input_path: {args.input_path}.')
    logger.info(f'Received argument --output_datastore: {args.output_datastore}.')
    logger.info(f'Received argument --datastore_type: {args.datastore_type}.')
    logger.info(f'Received argument --file_type: {args.file_type}.')
    logger.info(f'Received argument --number_rows_per_operation: {args.number_rows_per_operation}.')
    # logger.debug(f'Received argument --output_path: {args.output_path}.')
    # logger.info(f'Received argument --column_list_to_be_saved: {args.column_list_to_be_saved}.')
    # logger.debug(f'Received argument --datatable_name: {args.datatable_name}.')
    # logger.info(f'Received argument --column_list_datatable_columns: {args.column_list_datatable_columns}.')

    input_dict = {
        'Output_data_store': args.output_datastore,
        'Datastore_type': args.datastore_type,
        'Output_path': args.output_path,
        'Output_file_type': args.file_type,
        'Column_list_to_be_saved': args.column_list_to_be_saved,
        'Datatable_name': args.datatable_name,
        'Column_list_datatable_columns': args.column_list_datatable_columns,
        'Number_rows_per_operation': args.number_rows_per_operation}

    export_tabular_module = ExportTabularDataModule(input_dict)

    try:
        input_data_frame_directory = DataFrameDirectory.load(args.input_path)
    except DirectoryIOError as dfd_error:
        ErrorMapping.rethrow(dfd_error, TimeoutOccuredError())

    logger.info(f"Get input data frame directory {input_data_frame_directory}")
    export_tabular_module.run(input_data_frame_directory, input_dict)


def configs(parser):
    parser.add_argument(
        "--input_path",
        type=str,
        help="Input port or path that data can be accessed")
    parser.add_argument(
        "--output_datastore",
        type=str,
        help="Output datastore name")
    parser.add_argument(
        "--datastore_type",
        type=str,
        default='',
        help="Datastore type")
    parser.add_argument(
        "--output_path",
        type=str,
        help="The path that data to be exported")
    parser.add_argument(
        "--file_type",
        type=str,
        help="The file type to be exported")
    parser.add_argument(
        "--column_list_to_be_saved",
        type=str,
        help="Comma separated list of columns to be saved")
    parser.add_argument(
        "--datatable_name",
        type=str,
        help="Datatable name")
    parser.add_argument(
        "--column_list_datatable_columns",
        type=str,
        help="Comma separated list of datatable columns")
    parser.add_argument(
        "--number_rows_per_operation",
        type=str,
        default=50,
        help="Number of rows written per SQL Azure operation")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    configs(parser)
    args, unknown = parser.parse_known_args()

    main(args)
