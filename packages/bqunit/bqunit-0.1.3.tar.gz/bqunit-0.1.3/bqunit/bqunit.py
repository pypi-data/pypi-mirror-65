from google.cloud.bigquery import Client, table

from .query_builder import QueryBuilder
from .table_mapper import TableMapper


class BQUnit:

    def __init__(self, dataset_name: str, project_id=None):
        self.__client: Client = Client(project=project_id)
        self.__mapper: TableMapper = TableMapper()
        self.__builder: QueryBuilder = QueryBuilder(dataset_name=dataset_name)

    def fixture(self, table_name: str, statement: str, table_suffix=None) -> None:
        """Create a fixture table in BigQuery data set.

        :param table_name:
            Table name to mockup in your test. It must correspond with the query to be tested.
            That is if your query includes BigQuery project id in the FROM clause,
            this parameter should also start with your project id.
        :param statement:
            Select statement for inserting test data into fixture table.
        :param table_suffix:
            If you want to test query with _TABLE_SUFFIX syntax, this parameter must be given.
            For example:
                bq_unit.fixture(table_name='a_data_set.foo_bar_', table_suffix='20200101',...)
            then, you can test your query like below:
                "select * from `a_data_set.foo_bar_*` t1 where _TABLE_SUFFIX = '20200101'"
        """
        self.__mapper.register(table_name)
        temp_table_name = self.__mapper.get(table_name)
        create_statement = self.__builder.build_create_statement(
            f'{temp_table_name}{"" if table_suffix is None else table_suffix}', statement)
        query_job = self.__client.query(create_statement)
        query_job.result()  # Wait for the job to complete

    def test_query(self, query: str, job_config=None) -> table.RowIterator:
        """Run the query to testing data set.

        :param query:
            Query to be tested
        :param job_config: (google.cloud.bigquery.job.QueryJobConfig)
            Configuration options for query jobs.
            see: https://googleapis.dev/python/bigquery/latest/generated/google.cloud.bigquery.job.QueryJobConfig.html
        :return:
            Iterator through HTTP/JSON API row list responses.
            see: https://googleapis.dev/python/bigquery/latest/generated/google.cloud.bigquery.table.RowIterator.html
        """
        tables = self.__builder.extract_table_names(query)
        if any([t not in self.__mapper.registered_tables() for t in tables]):
            raise LookupError(f'One or more tables not found in the fixture.\n'
                              f'tables: {tables}\n'
                              f'Please check all tables are correctly mocked, by calling fixture() method.')
        query_to_test = self.__builder.replace_by_dict(query, self.__mapper.as_dict())
        query_job = self.__client.query(query_to_test, job_config=job_config)
        return query_job.result()

    def teardown(self) -> None:
        """Drop all the tables created by fixture() call."""
        targets = self.__mapper.redirected_tables()
        for target in targets:
            drop_statement = self.__builder.build_drop_statement(target)
            query_job = self.__client.query(drop_statement)
            query_job.result()  # Wait for the job to complete
