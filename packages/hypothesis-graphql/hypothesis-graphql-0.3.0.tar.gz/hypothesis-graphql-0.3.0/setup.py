# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['hypothesis_graphql', 'hypothesis_graphql._strategies']

package_data = \
{'': ['*']}

install_requires = \
['graphql-core>=3.1.0,<4.0.0', 'hypothesis>=5.8.0,<6.0.0']

setup_kwargs = {
    'name': 'hypothesis-graphql',
    'version': '0.3.0',
    'description': 'Hypothesis strategies for GraphQL schemas and queries',
    'long_description': 'hypothesis-graphql\n==================\n\n|Build| |Coverage| |Version| |Python versions| |License|\n\nHypothesis strategies for GraphQL schemas, queries and data.\n\n**NOTE** This package is experimental, many things don\'t work yet and documented in a way they are planned to be used.\n\nUsage\n-----\n\nThere are four strategies for different use cases.\n\n1. Schema generation - ``hypothesis_graphql.strategies.schema()``\n2. Query - ``hypothesis_graphql.strategies.query(schema)``.\n3. Response for a query - ``hypothesis_graphql.strategies.response(schema, query)``\n4. Data for a type - ``hypothesis_graphql.strategies.data(schema, type_name)``\n\nAt the moment only ``schema`` & ``query`` are working with some limitations.\n\nLets take this schema as an example:\n\n.. code::\n\n    type Book {\n      title: String\n      author: Author\n    }\n\n    type Author {\n      name: String\n      books: [Book]\n    }\n\n    type Query {\n      getBooks: [Book]\n      getAuthors: [Author]\n    }\n\nThen strategies might be used in this way:\n\n.. code:: python\n\n    from hypothesis import given\n    from hypothesis_graphql import strategies as gql_st\n\n    SCHEMA = """..."""  # the one above\n\n    @given(query=gql_st.query(schema))\n    def test_query(query):\n        ...\n        # This query might be generated:\n        #\n        # query {\n        #   getBooks {\n        #     title\n        #   }\n        # }\n\n    @given(response=gql_st.response(schema, query))\n    def test_response(response):\n        ...\n        # Example response with a query from the example above:\n        #\n        # {\n        #   "data": {\n        #     "getBooks": [\n        #       {"title": "War and Peace"}\n        #     ]\n        #   }\n        # }\n\n    @given(data=gql_st.data(schema, "Book"))\n    def test_data(data):\n        ...\n        # Example data:\n        #\n        # {\n        #   "title": "War and Peace"\n        #   "author": {"name": "Leo Tolstoy"}\n        # }\n\n.. |Build| image:: https://github.com/Stranger6667/hypothesis-graphql/workflows/build/badge.svg\n   :target: https://github.com/Stranger6667/hypothesis-graphql/actions\n.. |Coverage| image:: https://codecov.io/gh/Stranger6667/hypothesis-graphql/branch/master/graph/badge.svg\n   :target: https://codecov.io/gh/Stranger6667/hypothesis-graphql/branch/master\n   :alt: codecov.io status for master branch\n.. |Version| image:: https://img.shields.io/pypi/v/hypothesis-graphql.svg\n   :target: https://pypi.org/project/hypothesis-graphql/\n.. |Python versions| image:: https://img.shields.io/pypi/pyversions/hypothesis-graphql.svg\n   :target: https://pypi.org/project/hypothesis-graphql/\n.. |License| image:: https://img.shields.io/pypi/l/hypothesis-graphql.svg\n   :target: https://opensource.org/licenses/MIT\n',
    'author': 'Dmitry Dygalo',
    'author_email': 'dadygalo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Stranger6667/hypothesis-graphql',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
