# assart

According to Wikipedia, [Assarting](https://en.wikipedia.org/wiki/Assarting) is the act of clearing forested lands for use in agriculture or other purposes. In English land law, it was illegal to assart any part of a royal forest without permission.

In our case, `assart` is **A simple S3 analytic reporting tool_**

**Note: This is an experimental project and the codebase is not yet ready for serious usage.**

## Getting started

### Installation

Due to the experimental nature of the project, it is recommended that `assart` be installed into a virtual environment like so:

```
$ cd ~/venvs
$ python3 -m venv assartenv
$ source assartenv/bin/activate
$ pip install assart
```

### Configuration

`assart` utilizes the AWS Python SDK (`boto3`). By convention, `boto3` sources your AWS credentials and default region from the following locations:

```
$ cat ~/.aws/credentials
[default]
aws_access_key_id = YOUR_AWS_ACCESS_KEY_ID
aws_secret_access_key = YOUR_AWS_SECRET_ACCESS_KEY

$ cat ~/.aws/config
[default]
region = us-east-1
```

### Usage

```
$ assart -h
usage: assart [-h] [-u {KB,MB,GB}]

A simple S3 analytics reporting tool

optional arguments:
  -h, --help            show this help message and exit
  -u {KB,MB,GB}, --unit {KB,MB,GB}
                        Unit of Size

```

### Running

With your credentials configured, the program can be run like so:

```
$ assart
```

By default the program will output a list of the user's s3 buckets, and for each bucket will provide:

- The Bucket name
- The Creation date of the bucket
- The Number of files in the bucket
- The Total size of the files in the bucket
- The Last modified date of the most recent file

## Contributing

The `assart` package is available under a permissive MIT License. Feedback and suggestions are welcome. The package can be built like so:

```
python setup.py sdist bdist_wheel
```

---
