gqlclient
=========

|codecov|

.. image:: https://readthedocs.org/projects/graphql-client/badge/?version=latest
   :target: https://dkistdc.readthedocs.io/projects/graphql-client/en/latest/?badge=latest
   :alt: Documentation Status

A pythonic interface for making requests to a GraphQL server using
standard library or pydantic dataclasses to spare you from string manipulation.

Features
--------

-  Use standard library dataclasses to specify graphql parameters and responses

-  Use `pydantic <https://pypi.org/project/pydantic/>`__ dataclasses to
   specify graphql parameters and responses that have type validation

-  Create and execute GraphQL Queries based upon typed models

-  Create and execute GraphQL Mutations based upon typed models

-  Async support

Installation
------------

.. code:: bash

   pip install gqlclient

with ``asyncio`` support

.. code:: bash

   pip install gqlclient[async]

Examples
--------

**Query**

.. code:: python

   from pydantic.dataclasses import dataclass

   from gqlclient import GraphQLClient

   @dataclass
   class Parameters:
       attr_one: str
       attr_two: int

   @dataclass
   class Response:
       attr_three: int
       attr_four: str
       
   client = GraphQLClient(gql_uri="http://localhost:5000/graphql")
   parameters = Parameters(attr_one="foo", attr_two=3)
   query = client.get_query(query_base="baseType", query_response_cls=Response, query_parameters=parameters)
   print(query)
   #{'query': '{baseType(attr_one: "foo", attr_two: 3){attr_three, attr_four} }'}
   response = client.execute_gql_query(query_base="baseType", query_response_cls=Response, query_parameters=parameters)
   print(response)
   #{"baseType"{"attr_three":5, "attr_four":"bar"}}

**Mutation**

.. code:: python

   from pydantic.dataclasses import dataclass

   from gqlclient import GraphQLClient


   @dataclass
   class Parameters:
       attr_one: str
       attr_two: int


   @dataclass
   class Response:
       attr_three: int
       attr_four: str
       
   client = GraphQLClient(gql_uri="http://localhost:5000/graphql")
   parameters = Parameters(attr_one="foo", attr_two=3)
   query = client.get_mutation(mutation_base="baseMutation", mutation_response_cls=Response, mutation_parameters=parameters)
   print(query)
   #{'query': 'mutation baseType {baseType(attr_one: "foo", attr_two: 3){ok, attr_three, attr_four} }', 'operationName': 'baseType'}

   response = client.execute_gql_mutation(mutation_base="baseMutation", mutation_response_cls=Response, mutation_parameters=parameters)
   print(response)
   #{"baseMutation": {"ok": true, "Response": {"attr_three":5, "attr_four":"bar"} }}

**Encoders**

.. code:: python

    from dataclasses import dataclass

    from gqlclient import GraphQLClient
    from gqlclient import GraphQLClient, dataclass_encoder

    # set the default encoder to dataclass_encoder
    client = GraphQLClient(gql_uri="http://127.0.0.1:30003/graphql", default_response_encoder=dataclass_encoder)

    @dataclass
    class QueryResponse:
        workflowId: int
        workflowName: str
        workflowDescription: str

    response = client.execute_gql_query("workflows", QueryResponse)
    print(response)
    # Response type is a list of dataclasses
    # [QueryResponse(workflowId=1, workflowName='gql3_full - workflow_name', workflowDescription='gql3_full - workflow_description'), QueryResponse(workflowId=2, workflowName='VBI base calibration', workflowDescription='The base set of calibration tasks for VBI.'), QueryResponse(workflowId=3, workflowName='VISP base calibration', workflowDescription='The base set of calibration tasks for VISP.'), QueryResponse(workflowId=4, workflowName='VTF base calibration', workflowDescription='The base set of calibration tasks for VTF.'), QueryResponse(workflowId=5, workflowName='DLNIRSP base calibration', workflowDescription='The base set of calibration tasks for DLNIRSP.'), QueryResponse(workflowId=6, workflowName='CRYONIRSP base calibration', workflowDescription='The base set of calibration tasks for CRYONIRSP.')]

    from gqlclient import json_encoder
    # for this call override the default encoder to the json encoder
    response = client.execute_gql_query("workflows",QueryResponse, response_encoder=json_encoder)
    print(response)
    # Response is a json formatted string
    # '{"workflows": [{"workflowId": 1, "workflowName": "gql3_full - workflow_name", "workflowDescription": "gql3_full - workflow_description"}, {"workflowId": 2, "workflowName": "VBI base calibration", "workflowDescription": "The base set of calibration tasks for VBI."}, {"workflowId": 3, "workflowName": "VISP base calibration", "workflowDescription": "The base set of calibration tasks for VISP."}, {"workflowId": 4, "workflowName": "VTF base calibration", "workflowDescription": "The base set of calibration tasks for VTF."}, {"workflowId": 5, "workflowName": "DLNIRSP base calibration", "workflowDescription": "The base set of calibration tasks for DLNIRSP."}, {"workflowId": 6, "workflowName": "CRYONIRSP base calibration", "workflowDescription": "The base set of calibration tasks for CRYONIRSP."}]}'

.. |codecov| image:: https://codecov.io/bb/dkistdc/graphql_client/branch/master/graph/badge.svg
   :target: https://codecov.io/bb/dkistdc/graphql_client
