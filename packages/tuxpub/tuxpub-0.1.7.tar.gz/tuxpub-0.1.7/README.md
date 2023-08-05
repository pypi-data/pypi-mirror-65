# tuxpub

[![Pipeline Status](https://gitlab.com/Linaro/tuxpub/badges/master/pipeline.svg)](https://gitlab.com/Linaro/tuxpub/pipelines)
[![coverage report](https://gitlab.com/Linaro/tuxpub/badges/master/coverage.svg)](https://gitlab.com/Linaro/tuxpub/commits/master)
[![PyPI version](https://badge.fury.io/py/tuxpub.svg)](https://pypi.org/project/tuxpub/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![PyPI - License](https://img.shields.io/pypi/l/tuxpub)](https://gitlab.com/Linaro/tuxpub/blob/master/LICENSE)
<!--[![Docker Pulls](https://img.shields.io/docker/pulls/tuxpub/tuxpub.svg)](https://hub.docker.com/r/tuxpub/tuxpub)-->

The Serverless File Server

tuxpub is a python/flask application which provides a file browsing interface
to S3, and is designed to be run serverlessly with
[Zappa](https://github.com/Miserlou/Zappa).

An example tuxpub deployment can be found at
[storage.lkft.org](https://storage.lkft.org/).

# Configuration

Configuration is handled through environment variables. The following
configuration variables are used.

- `S3_BUCKET`
  - required: True
  - description: S3 bucket name containing the files to serve. Example:
    `storage.staging.lkft.org`
- `S3_REGION`
  - required: True
  - description: Region containing the S3 bucket. Example:`us-east-1`
- `ROOT_INDEX_LISTING`
  - required: False
  - description: Defaults to `True`. Set to `False` to hide the top level
    directory/file listing.
- `SITE_TITLE`
  - required: False
  - description: Defaults to `Tuxpub`. Set to anything you like for a global
    site title.

# Run Locally

To run locally, install tuxpub, ensure AWS access is available environmentally,
and run:

```shell
S3_BUCKET=storage.staging.lkft.org S3_REGION=us-east-1 ROOT_INDEX_LISTING=True FLASK_APP=tuxpub flask run
```

# Run with Zappa

This application is intended to be ran and deployed with
[Zappa](https://github.com/Miserlou/Zappa) and hosted by AWS [API
Gateway](https://aws.amazon.com/api-gateway/) and
[Lambda](https://aws.amazon.com/lambda/).

To use with Zappa, create an app shim named zappa_init.py:

```python
# When using a flask app factory, this file is required.
# See https://github.com/Miserlou/Zappa/issues/1771
# and https://github.com/Miserlou/Zappa/pull/1775
from tuxpub import create_app
app = create_app()
```

An example zappa_settings.json file may look like:
```json
{
    "dev": {
        "app_function": "zappa_init.app",
        "aws_region": "us-east-1",
        "project_name": "lkft-tuxpub",
        "runtime": "python3.7",
        "s3_bucket": "zappa-tuxpub",
        "environment_variables": {
          "S3_BUCKET": "storage.dev.lkft.org",
          "S3_REGION": "us-east-1",
          "ROOT_INDEX_LISTING": "True",
        }
    }
}
```

# Features

## Export Formats

By default pages are served using HTML. If `export=json` is appended to a
listing URL, a json representation of the page will be provided. This option is
ignored when requesting specific files.

Example:

```sh
curl http://localhost/path/to/files/?export=json
```

## Root Index listing

By default this application will display the directories and files on the root
page. However, a user might not want to allow people to crawl through the S3
bucket. You can set `ROOT_INDEX_LISTING=False`, which will render a empty root
index page.
