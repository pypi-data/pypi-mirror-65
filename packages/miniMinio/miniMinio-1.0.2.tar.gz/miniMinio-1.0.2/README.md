# miniMinio

A thin python helper get either 1) local files or 2) Minio objects. 1) Heavily relies on the default os library while 2) is built off [minio-py](https://github.com/minio/minio-py). The package is designed to provide a seamless switch between testing file operations locally/over a file system and interacting with a minio server when in deployment.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install miniMinio.

```bash
pip install miniMinio
```

## Usage

1. Create a connection that returns a client
2. Use client as a function input for subsequent functions

```python
from miniMinio import create_connection

client = create_connection("some_hostname:port", "access_key", "secret_key")

# For filesystems
client = create_connection("local")

client = create_connection("remote")

```
####For filesystems:

'local' is designed to work when the working directory is at the directory equivalent to a Minio's bucket. Best suited for .exe files

'remote' gives the user the flexibility to specify the bucket.

object_names for file server operations replaces the S3 object naming convention with the **absolute path** of the object

i.e.
```
# Minio object name / Minio Bucket
"Book1.xlsx" / "example_bucket"
# File system object name equivalent
"usr/full/path/to/example_bucket/Book1.xlsx"
```

Filesystems do not need to specify bucket_name

### Functions

```python
all_buckets = get_buckets(client)
```
Returns all bucket *name* and *creation date* as a tuple
```python
get_all_object_details_in_bucket(client, bucket_name=None, attributes=["object_name", "last_modified"], filter_object=("file", "folder"), filter_prefix='')
```
Returns all objects recursively within a specified bucket. Attributes supported  Filter enables the user to filter the objects. 

Supported filters ['file', 'folder', 'excel']. 

Supported attributes (Only for Minio) ['etag', 'last_modified', 'size', 'content_type']

filter_prefix accepts an extension of the path from the bucket to form a new path. The resulting combined path will be the start point of the search
```python
get_all_objects_from_bucket(client, bucket_name, object_name_list, file_path)
```
Transfers all objects in object_name_list to the desired file_path relative to the working directory
```python
get_single_object_content_bytes(client, bucket_name, object_name)
```
Returns bytes of the selected object
```python
get_single_excel_file_content(client, bucket_name, excel_file_object)
```
Returns an <xlrd.book.Book> object

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/) 


