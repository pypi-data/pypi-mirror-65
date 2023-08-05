BQUnit
==========

Testing framework for BigQuery SQL.

What is this?
-------------

BigQuery enables us to execute "super-fast SQL queries
using the processing power of Google's infrastructure".

However, testing query-based data pipelines sometimes become depressing work, because:

* SQL itself takes more responsibility in data transformation logic,
  and the glue code layer like Python scripts(which is relatively easy to test) doesn't.
* We can't imitate BigQuery infrastructure easily.
  There's no Docker image, StandardSQL has many unique syntaxes which can't be used on other RDBMS,
  and above all, Google has huge computing resources than ours.

BQUnit solves this problem, by managing your test data preparation
on your BigQuery data set, which is isolated from your production environment.


Usage
------------

First, instantiate BQUnit object::

    bqunit = BQUnit(project_id='test-env-123456', dataset_name='bqunit')

    # If Application Default Credential is set, project id is not required.
    bqunit = BQUnit(dataset_name='bqunit')

And then, mockup your tables by a fixture() method call::

    bqunit.fixture(
        table_name='your-production-123456.foo.bar',
        statement="""
        select 1 as col1, 'str_1' as col2, true as col3
        union all
        select 2, 'str_2', false
        """)

**You don't need to know where to insert your test data**.
You just need to specify your production table name here.

Testing will be like this::

    tested_query = """
       select col1, col2
       from `your-production-123456.foo.bar` foo
       where col1 = 1
     """
    query_result = bqunit.test_query(tested_query)
    assert query_result.total_rows == 1

BQUnit execute your query on test data set, which is created when you called the fixture() method,
so you can predict its result set correctly, and make assertions.

Note that *query_result* will be RowIterator object of *google-cloud-bigquery* library.
see also `google-cloud-bigquery documentation
<https://googleapis.dev/python/bigquery/latest/generated/google.cloud.bigquery.table.RowIterator.html>`_.
