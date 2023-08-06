import pandas as pd
from azureml.studio.core.error import UserError

from azureml.designer.modules.datatransform.common.module_base import ModuleBase
from azureml.designer.modules.datatransform.common.module_parameter import InputPortModuleParameter, \
    OutputPortModuleParameter, ScriptModuleParameter, ModuleParameters
from azureml.designer.modules.datatransform.common.logger import custom_module_logger as logger
# from azureml.designer.modules.datatransform.common.logger import format_obj
from azureml.designer.modules.datatransform.common.module_meta_data import ModuleMetaData
from azureml.designer.modules.datatransform.common.module_spec_node import ModuleSpecNode
from azureml.studio.internal.error import ErrorMapping, InvalidSQLScriptError


class ApplySqlTransModule(ModuleBase):
    def __init__(self):
        meta_data = ModuleMetaData(
            id="90381e80-67c3-4d99-8754-1db785b7ea37",
            name="Apply SQL Transformation",
            category="Data Transformation",
            description="Runs a SQLite query on input datasets to transform the data.")
        parameters = ModuleParameters(
            [
                InputPortModuleParameter(
                    name="t1",
                    friendly_name="t1",
                    is_optional=False),
                InputPortModuleParameter(
                    name="t2",
                    friendly_name="t2",
                    is_optional=True),
                InputPortModuleParameter(
                    name="t3",
                    friendly_name="t3",
                    is_optional=True),
                OutputPortModuleParameter(
                    name="dataset",
                    friendly_name="Result_dataset",
                    is_optional=False),
                ScriptModuleParameter(
                    name="sqlquery",
                    friendly_name="SQL query script",
                    is_optional=False,
                    default_value="select * from t1",
                    language="Sql")])
        module_nodes = [
            ModuleSpecNode.from_module_parameter(parameters["t1"]),
            ModuleSpecNode.from_module_parameter(parameters["t2"], is_optional=True),
            ModuleSpecNode.from_module_parameter(parameters["t3"], is_optional=True),
            ModuleSpecNode.from_module_parameter(parameters["dataset"]),
            ModuleSpecNode.from_module_parameter(parameters["sqlquery"]),
        ]
        conda_config_file = './azureml/designer/modules/datatransform/modules/conda_config/apply_sql_trans_module.yml'
        super().__init__(
            meta_data=meta_data,
            parameters=parameters,
            module_nodes=module_nodes,
            conda_config_file=conda_config_file)

    def run(self):
        from sqlalchemy import create_engine
        import sqlalchemy
        import sqlite3
        import sqlparse
        logger.info("Construct SQLLite Server")
        engine = create_engine('sqlite://', echo=False)

        t1 = self._get_input("t1")
        if t1 is not None:
            if len(t1.columns) == 0:
                ErrorMapping.throw(UserError('t1 is empty dataframe.'))
            logger.info("Insert t1")
            # logger.info(format_obj("t1", t1))
            try:
                t1.to_sql('t1', con=engine, index=False)
            except MemoryError as memerr:
                hint_message = 'Out of memory, please try upgrade compute. ' + str(memerr)
                ErrorMapping.rethrow(memerr, UserError(hint_message))

        t2 = self._get_input("t2")
        if t2 is not None:
            if len(t1.columns) == 0:
                ErrorMapping.throw(UserError('t2 is empty dataframe.'))
            logger.info("Insert t2")
            # logger.info(format_obj("t2", t2))
            try:
                t2.to_sql('t2', con=engine, index=False)
            except MemoryError as memerr:
                hint_message = 'Out of memory, please try upgrade compute. ' + str(memerr)
                ErrorMapping.rethrow(memerr, UserError(hint_message))

        t3 = self._get_input("t3")
        if t3 is not None:
            if len(t3.columns) == 0:
                ErrorMapping.throw(UserError('t3 is empty dataframe.'))
            logger.info("Insert t3 table")
            # logger.info(format_obj("t3", t3))
            try:
                t3.to_sql('t3', con=engine, index=False)
            except MemoryError as memerr:
                hint_message = 'Out of memory, please try upgrade compute. ' + str(memerr)
                ErrorMapping.rethrow(memerr, UserError(hint_message))

        sql_query = self.parameters["sqlquery"].value
        try:
            if sql_query:
                sql_query = sql_query.strip()
                sql_querys = [s.strip() for s in sqlparse.split(sql_query) if self._is_valid_sql_statement(s)]
                if len(sql_querys) > 1:
                    with engine.connect() as con:
                        for query in sql_querys[:-1]:
                            con.execute(query)
                    sql_query = sql_querys[-1]
            output = None
            output = pd.read_sql_query(sql_query, con=engine)
        except sqlalchemy.exc.OperationalError as sqlalchemyex:
            ErrorMapping.rethrow(
                sqlalchemyex, InvalidSQLScriptError(
                    sql_query, sqlalchemyex))
        except sqlite3.Warning as sqlite3warning:
            ErrorMapping.rethrow(
                sqlite3warning, InvalidSQLScriptError(
                    sql_query, sqlite3warning))
        except sqlite3.OperationalError as sqlite3ex:
            ErrorMapping.rethrow(
                sqlite3ex, InvalidSQLScriptError(
                    sql_query, sqlite3ex))
        except sqlite3.ProgrammingError as programEx:
            ErrorMapping.rethrow(
                programEx, InvalidSQLScriptError(
                    sql_query, programEx))
        except sqlalchemy.exc.ResourceClosedError as noselectex:
            ErrorMapping.rethrow(noselectex, UserError(str(noselectex)))
        except Exception as err:
            raise err

        output = self.handle_output_same_column_name(output)
        output = self.handle_output_datetime_column(output)
        self._handle_output("dataset", output)

    def handle_output_datetime_column(self, data: pd.DataFrame):
        return data.applymap(self._convert_datetime)

    def handle_output_same_column_name(self, data: pd.DataFrame):
        new_column_names = []
        exist_column_name = {}
        for column_index in range(len(data.columns)):
            column = data.iloc[:, column_index]
            column_name = column.name
            if column_name in exist_column_name:
                exist_column_name[column_name] = exist_column_name[column_name] + 1
                new_column_names.append(
                    f'{column_name} ({exist_column_name[column_name]})')
            else:
                exist_column_name[column_name] = 1
                new_column_names.append(column_name)
        data.columns = new_column_names
        return data

    def _is_valid_sql_statement(self, statement: str):
        if not statement or not statement.strip():
            return False
        import sqlparse
        for token in sqlparse.parse(statement)[0].flatten():
            if "Token.Comment" not in str(token.ttype) and "Token.Text.Whitespace" not in str(token.ttype):
                return True
        return False

    def _convert_datetime(self, item):
        # the format of datatime string will be like 1978-06-29 07:34:10.000000
        if isinstance(item, str) and len(item) == 26:
            return pd.to_datetime(
                str(item),
                infer_datetime_format=True,
                errors='ignore',
                utc=True)
        return item
