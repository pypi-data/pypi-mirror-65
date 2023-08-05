import re


class QueryBuilder:
    def __init__(self, dataset_name: str):
        self.dataset_name = dataset_name

    def build_create_statement(self, table_name: str,
                               select_statement: str) -> str:
        return f'''
        create or replace table {self.dataset_name}.{table_name}
        as {select_statement}
        '''

    def replace_by_dict(self, query: str, mapping: dict) -> str:
        for k, v in mapping.items():
            query = query.replace(k, f'{self.dataset_name}.{v}')
        return query

    def build_drop_statement(self, table_name: str) -> str:
        return f'drop table if exists {self.dataset_name}.{table_name}'

    @staticmethod
    def extract_table_names(source_query: str) -> list:
        # todo: handle table name with suffix
        table_regex = r'from\s+`?([a-zA-Z0-9_\.\-]*)'
        return re.findall(table_regex, source_query, re.MULTILINE)
