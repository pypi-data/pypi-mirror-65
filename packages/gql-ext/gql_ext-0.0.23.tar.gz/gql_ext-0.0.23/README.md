# GraphQL Facade

GraphQL Facade is a python application-intermediary between a 
frontend application using GraphQL and a REST application on the backend 
oriented declarative style of the description of the services.

## GraphQL Facade allow

* make a requests to the REST service using GraphQL language
* use batch loading (subject to the rules)

## Adding new REST service to the Application

To add a new service, you need to perform several steps:

1) create a description of the data schema in [graphql syntax](https://graphql.org/learn/)
2) create [REST service description](#rest-service-description) (yaml or json supported)
3) describe [resolvers](#resolvers) (yaml or json)
4) add [schema description](#schemas-description) to main configuration file
5) specify the Base Url of the service in the application settings

## REST service description
```
<service_name>: 
    <endpoint_name>:
        method: <METHOD>
        path: <PATH>
```
`service_name`: Name of your REST API service.  
`endpoint_name`: Name of your REST endpoint.  
`method`: GET, POST, PATCH, PUT, DELETE (GET default)  
`path`: path to yor endpoint

## Resolvers
```
<Parent_name.field_name>:
    endpoint: <service_name.endpoint_name>
    batch: True
    args:
        <param_name>: <param_value>
    loader: <path.to.your.custom.resolver_file.resolver_name>
```
`Parent_name.field_name`: field name in your graphql schema (`Query.name` for example)  
`endpoint`: your rest endpoint for this data field in `service_name`.`endpoint_name` format  
`loader`: path to custom resolver (not a required field). Use python site-packages syntax  
`args`: if you want to use any params to make request to REST you can set args field.
`param_name` - an arbitrary name of the variable, `param_value` - arbitrary value.
To use the attributes of a parent element, use `parent.` the prefix and then the name of the attribute.
for examle `post_is: parent.id`
`batch`: use [batch loading](#batch-loading). False by default  

## Schemas description
```
schemas:
  <schema_name>:
    url: <schema_url>
    resolvers: <path/to/your/resolvers/file>
    sdl:
      - <list/of/paths/to/sdl/directories>
      - <or/and/sdl/files>

rest:
  - <list/of/paths/to/your/rest/description/files>
```
`schema_name`: your schema name  
`url`: url to graphql endpoint (by default equal to schema name)  
`resolvers`: path (relative to base directory) to your resolvers file  
`sdl`: list of paths to `.graphql` files (schema descriptions) or directories with `.graphql` files  
`rest`: list of paths to rest definition files (relative to base directory)  
## REST App connection Example
Let's say you have a REST service with signature:
Input:
```
{
    id: [0, 1, 2],
    q: "any search string"
}
```
Output:
```
{
  "pagination": {
    "total": 0,
    "offset": 0,
    "limit": 0
  },
  "result": [
    {
      "conditions": {},
      "calculator_id": 0,
      "version": 0,
      "created": "2019-08-29T09:09:23.048Z",
      "terms": [
        0
      ],
      "status": "archive",
      "updated": "2019-08-29T09:09:23.048Z",
      "amounts": [
        0
      ],
      "priority": 0,
      "title": "string",
      "meta": {},
      "id": 0
    }
  ]
}
```

for connect your api to GraphQL facade follow that steps:

### preview

As a result of all the steps we get the structure (files and directories that we will not use are omitted)

```
-app
    -graphql
        -calculator
            -sdl
                mutation.graphql
                query.graphql
            loaders.py
            resolvers.yaml
            rest.yaml
        ...
    init_facade.yaml
    ...
...
```
`.graphql` files - description of your data schema  
`loaders.py` custom resolvers (if you need)  
`resolvers.yaml` description of resolvers  
`rest.yaml` description of rest api service  
`init_facade.yaml` description all schemas and file paths for schema  

the file scheme is conditional and not mandatory but it is recommended to adhere to this rule of file location and naming

### 1. describe data schema

the data schema describes data types and arguments
for our REST service it will have the following form

###### app/graphql/calculator/sdl/query.graphql
```
type Query {
    calculators(id: [Int], q: String): Calculators
    }

type Calculators{
    pagination: Pagination
    result: [Calculator]
    }

type Calculator {
    id: Int
    created: String
    updated: String
    calculator_id: Int
    status: String
    version: Int
    title: String
    amounts: [String]
    terms: [Int]
    meta: String
    priority: Int
    conditions: String
    }

type Pagination {
    total: Int
    limit: Int
    offset: Int
    }
```

### 2. REST service description

REST description files contains information about paths to your REST handlers

for our API:

###### app/graphql/calculator/rest.json
```
{
  "calculator": {
    "find_calculators": {
      "method": "GET",
      "path": "/api/v1/pdl_calculators/"
    }
}
```
### 3. describe resolvers

Resolvers files explain how to receive Schema fields 
(which REST handler to use, whether to use bath loading or smth else)

###### app/graphql/calculator/resolvers.json
```
{
  "Query.calculators": {
    "endpoint": "calculator.find_calculators"
  }
}
```
### 4. main configuration file
###### app/init_facade.yaml
Configuration file describe file location for our schema
```
schemas:

  calculator:
    url: calculator
    resolvers: app/graphql/calculator/resolvers
    sdl:
      - app/graphql/calculator/sdl

rest:
  - app/graphql/calculator/rest

```
### 5. base url to config
It is important not to forget to specify URLs in the application settings
We do not specify base_url in yaml or json files to be able to pass base_url as environment variables

Key must match to REST service name in rest.yaml file
###### settings/config.py
```
class Config:
...
    BASE_URLS = {
                 ...
                 'calculator': env.str('calculator_api', default='http:/calculator.prod.com')
                 ...
                }
...
```
## Batch loading

For use batch loading you must follow few simple rules:
* REST API endpoint must accept a list of `id` arguments
* REST must return list of records (which perform a conditions of a request) in `result` field and send `id` field to each row  
for example:
```
{
  "pagination": {
    "total": 2,
    "limit": 10,
    "offset": 0
  },
  "result": [
    {
      "id": 1
    },
    {
      "id": 2
    }
  ],
  "success": true
}
```
* finally set `batch` = `True` in your fields resolver description:
```
Calculator.calculator:
    endpoint: /api/v1/calculator
    batch: True
```