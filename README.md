# s3-reader

[![test](https://github.com/rcmdnk/s3-reader/actions/workflows/test.yml/badge.svg)](https://github.com/rcmdnk/s3-reader/actions/workflows/test.yml)
[![test coverage](https://img.shields.io/badge/coverage-check%20here-blue.svg)](https://github.com/rcmdnk/s3-reader/tree/coverage)

Python library to read S3 file as local file.

## Requirement

- Python 3.9, 3.10, 3.11

## Installation

```bash
$ pip install s3-reader
```

## Usage

```
from s3_reader import File


def check_s3_file(path):
    file = File(path)

    with open(file.path) as f:
        ...

check_s3_file('s3://<bucket>/path/to/file')

```

In this example, the S3 file is downloaded when `file = File(path)` is
executed, and it is stored as a temporary file.

`file.path` refers to the path of the locally stored temporary file.

At the end of the `check_s3_file` function, the file object is deleted, and
consequently, the temporary file is also deleted.

If path refers to a local file instead of an S3 file, File simply copies the
path, and you can use the File object in the same manner.

You can pass following parameters to `File` constructor to setup AWS credential:

```
profile_name : str | None
    AWS profile name.
aws_access_key_id : str | None
    AWS access key id.
aws_secret_access_key : str | None
    AWS secret access key.
aws_session_token : str | None
    AWS session token.
region_name : str | None
    AWS region name.
role_arn : str | None
    AWS role arn for Assume role. If this is set, aws_access_key_id,
    aws_secret_access_key, aws_session_token are replaced by Assume role.
session_name : str
    AWS session name. Default is "s3_reader".
retry_mode : str
    Retry mode for failed requests. Default is "standard".
max_attempts : int
    Maximum number of retry attempts for failed requests. Default is 10.
max_trials : int
    Maximum number of trials to retry after retrieving credential error.
    Default is 10.
```
