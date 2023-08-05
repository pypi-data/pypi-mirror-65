# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bqunit']

package_data = \
{'': ['*']}

install_requires = \
['google-cloud-bigquery>=1.24.0,<2.0.0']

setup_kwargs = {
    'name': 'bqunit',
    'version': '0.1.3',
    'description': 'Testing framework for BigQuery SQL',
    'long_description': 'BQUnit\n==========\n\nTesting framework for BigQuery SQL.\n\nWhat is this?\n-------------\n\nBigQuery enables us to execute "super-fast SQL queries\nusing the processing power of Google\'s infrastructure".\n\nHowever, testing query-based data pipelines sometimes become depressing work, because:\n\n* SQL itself takes more responsibility in data transformation logic,\n  and the glue code layer like Python scripts(which is relatively easy to test) doesn\'t.\n* We can\'t imitate BigQuery infrastructure easily.\n  There\'s no Docker image, StandardSQL has many unique syntaxes which can\'t be used on other RDBMS,\n  and above all, Google has huge computing resources than ours.\n\nBQUnit solves this problem, by managing your test data preparation\non your BigQuery data set, which is isolated from your production environment.\n\n\nUsage\n------------\n\nFirst, instantiate BQUnit object::\n\n    bqunit = BQUnit(project_id=\'test-env-123456\', dataset_name=\'bqunit\')\n\n    # If Application Default Credential is set, project id is not required.\n    bqunit = BQUnit(dataset_name=\'bqunit\')\n\nAnd then, mockup your tables by a fixture() method call::\n\n    bqunit.fixture(\n        table_name=\'your-production-123456.foo.bar\',\n        statement="""\n        select 1 as col1, \'str_1\' as col2, true as col3\n        union all\n        select 2, \'str_2\', false\n        """)\n\n**You don\'t need to know where to insert your test data**.\nYou just need to specify your production table name here.\n\nTesting will be like this::\n\n    tested_query = """\n       select col1, col2\n       from `your-production-123456.foo.bar` foo\n       where col1 = 1\n     """\n    query_result = bqunit.test_query(tested_query)\n    assert query_result.total_rows == 1\n\nBQUnit execute your query on test data set, which is created when you called the fixture() method,\nso you can predict its result set correctly, and make assertions.\n\nNote that *query_result* will be RowIterator object of *google-cloud-bigquery* library.\nsee also `google-cloud-bigquery documentation\n<https://googleapis.dev/python/bigquery/latest/generated/google.cloud.bigquery.table.RowIterator.html>`_.\n',
    'author': 'to-lz1',
    'author_email': 'm.toriyama000@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/to-lz1/bqunit',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
