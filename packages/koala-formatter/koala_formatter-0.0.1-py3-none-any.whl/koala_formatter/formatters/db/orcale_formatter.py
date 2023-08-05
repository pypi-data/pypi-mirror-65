from collections.abc import Callable
from koala_formatter.formatters.formatter_base import FormatterBase


class OracleFormatter(FormatterBase):

    def __init__(self):
        super().__init__(__name__)

    def __enter__(self):
        return self

    @property
    def collection_node_type(self):
        return "db_table"

    @property
    def required_collection_node_fields(self):
        return tuple(('schema_name', 'table_name', 'table_description', 'team_name'))

    @property
    def resource_node_type(self):
        return "db_table_column"

    @property
    def required_resource_node_fields(self):
        return tuple(('schema_name', 'table_name', 'column_name',
                      'column_description', 'data_type'))

    @property
    def required_edge_fields(self):
        return tuple(('n1', 'n2'))

    @property
    def collection_id_creator(self) -> Callable:
        return lambda column_map: f"{column_map['schema_name']}.{column_map['table_name']}"

    @property
    def resource_id_creator(self) -> Callable:
        return lambda column_map: f"{column_map['schema_name']}.{column_map['table_name']}.{column_map['column_name']}"

    def create_nodes(self, tables, columns):
        return self._create_graph_objects(tables, columns)
