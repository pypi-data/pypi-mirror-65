# jx-bigquery

JSON Expressions for BigQuery


## Status

March 2020 - Active but incomplete:  Can insert [tidy](https://en.wikipedia.org/wiki/Tidy_data) JSON documents into BigQuery while managing the schema.  Queries are not supported yet.

## Overview

The library is intended to manage multiple BigQuery tables to give the illusion of one table with a dynamically managed schema. 


## Definitions

* `partition` - Big data is split into separate containers based on age. This allows queries on recent data to use less resources, and allows old data to be dropped quickly
* `cluster` - another name for the sorted order of the data in a partition. Sorting by the most common used lookup will make queries faster
* `id` - The set of columns that identifies the document 


## Configuration

* `table` - Any name you wish to give to this table series
* `top_level_fields` - BigQuery demands that control columns are top-level.  Define them here.
* `partition` - 
  * `field` - The dot-delimited field used to partition the tables (must be time datatype)
  * `expire` - When BigQuery will automatically drop your data. 
* `id` - The identification of documents 
  * `field` - the set of columns to uniquely identify this document
  * `version` - column used to determine age of a document; replacing newer with older
* `cluster` - Columns used to sort the partitions 
* `schema` - {name: type} dictionary - needed when there is no data; BigQuery demands column definitions
* `sharded` - *boolean* - set to `true` if you allow this library to track multiple tables. It allows for schema migration (expansion only), and for faster insert from a multitude of machines  
* `account_info` - The information BigQuery provides to connect 

### Example

This is a complicated example. See [tests/config.json](https://github.com/klahnakoski/jx-bigquery/blob/dev/tests/config.json) for a minimal example.

```json
{
    "table": "my_table_name",
    "top_level_fields": {},
    "partition": {
        "field": "submit_time",
        "expire": "2year"
    },
    "id": {
        "field": "id",
        "version": "last_modified"
    },
    "cluster": [
        "id",
        "last_modified"
    ],
    "schema": {
        "id": "integer",
        "submit_time": "time",
        "last_modified": "time"
    },
    "sharded": true,
    "account_info": {
        "private_key_id": {
            "$ref": "env://BIGQUERY_PRIVATE_KEY_ID"
        },
        "private_key": {
            "$ref": "env://BIGQUERY_PRIVATE_KEY"
        },
        "type": "service_account",
        "project_id": "my-project-id",
        "client_email": "me@my_project.iam.gserviceaccount.com",
        "client_id": "12345",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/my-project.iam.gserviceaccount.com"
    }
}
```

## Usage

Setup `Dataset` with an application name

```python
    dataset = bigquery.Dataset(
        dataset=application_name, 
        kwargs=settings
    )
```

Create a table

```python
    destination = dataset.get_or_create_table(settings.destination)
```

Insert documents as you please


```python
    destination.extend(documents)
```

Request a merge when done

```python
    destination.merge()
```

## Running tests


Fork and clone this repo. 

```
git clone https://github.com/klahnakoski/jx-bigquery.git 
cd jx-bigquery
pip install -r requirements.txt
```

You will require a Google API key to run tests. The website will allow you to generate one and download a JSON file with the key.  Update the [tests/config.json](https://github.com/klahnakoski/jx-bigquery/blob/dev/tests/config.json) to point to that file: 


```
# contents of tests/config.json
{
  "destination": {
    "account_info": {
      "$ref": "file:///e:/moz-fx-dev-ekyle-treeherder-a838a7718652.json"
    }
  },
  "constants": {},
  "debug": {
    "trace": true
  }
}
```

Then you can run the tests

```
python -m unittest discover tests
```

> **NOTE** - the tests will create a `testing` dataset and generate/drop tables 
