# Installation

`pip install nomnomdata-engine-tools nomnomdata-engine` 

# Creating a new engine

This will walk through all the information required to create, build and deploy a new engine.

Directory Structure

Initialize a new engine with

`nnd engine-tools create-new <ENGINE_NAME>` 

This will create a new directory with the layout

``` directory
.
├── .dockerignore
├── .gitignore
├── .ex_pyproject.toml
└── engine
    ├── build.dockerfile
    ├── model.yaml
    ├── requirements.txt
    └── pkg
        ├── __init__.py
        ├── executable.py
        └── tests
            ├── __init__.py
            └── test_executable.py
```

## build.dockerfile

Engines are deployed as docker images, so for every engine you must have a build.dockerfile located next to a model.yaml file. You will want to place your python files the 'pkg' directory if you want nnd engine-tools build -rt to work properly.

Look at the template build.dockerfile for an example and more information. You must include 

`CMD nnd engine run pkg/executable.py` 

 Or your engine will not start correctly.

## requirements.txt

Simple pip requirements file. Requirements should be set to a specific version (ie requests==2.18.4) . Only requirements specific to your engine should be included in here. The template requirements.txt shows how to include the packages nomnomdata-cli & nomnomdata-engine which are the easiest way to run your executable.

## executable.py

This is where the code that actually gets run lives.

``` python
from nomnomdata.engine.api import NominodeClient
from nomnomdata.engine.core import Executable

class TemplateExecutable(Executable):
    def __init__(self):
        # Very important to call the inherited __init__ before anything else
        super().__init__("nomigen.{{engine_name}}")

    def do_thing(self):
        self.logger.info("I did a thing!")
        self.logger.info(f"My parameters are {self.params}")
        self.nominode.update_progress(message="I did it!")

``` 

## test_executable.py

Tests! Our run tests command uses pytest to run these inside your docker image, so you can use anything pytest supports. The most important thing is to wrap your test code with a NominodeMock , this essentially sets up a 'fake' nomnominode catching http requests to it.

```python
from nomnomdata.engine.test import NominodeMock
from nomnomdata.engine.test_creds import credentials
from ..executable import TemplateExecutable

config = {

    1: credentials["aws_connection"],

}

params = {
    "config": config,
    'action_name': 'test',
    "aws_connection": {
        "connection_uuid": '2'
    },
    'other_param': 'some variable'

}

# the most basic test possible..
def test_init(self):
    with NominodeMock(params):
        t = TemplateExecutable()
        t.do_thing()

``` 

## model.yaml

This is the description of your engine that will reside in the nomitall database, used by the nominode_ui to dynamically create configuration pages.

```yaml
# the unique identifier for this engine, must be unique across all engines
uuid: NOMNOM_EXAMPLE_DOWNLOADER
alias: "EXAMPLE: Downloader"
description: An Example
# repo information, most of the information is static apart from image
location:
  repo: 445607516549.dkr.ecr.us-east-1.amazonaws.com
  # the :testing tag at the end indicates which ECS tag to use, for staging this should be testing, prod should use alpha
  image: example/api/downloader:testing
  region: us-east-1
  repo_type: aws
# categories this engine fits into, there are no fixed categories at this time
categories:

  + name: example
  + name: s3
  + name: nomnomdata

# this is a list of actions this engine can perform, these map directly to
# functions of your Executable class in executable.py
parameters:

  + action_name: example_function

    description: An example
    display_name: Example Function
    # this is where you can add what connections the engine requires
    # also what adhoc parameters the engine uses.
    # these will be presented to the user to fill in
    parameters:
    # this include parameter is a special directive that allows you include parameters from other files
    # includes that are specific to the engine should be stored in your_engine/models

    - include:
      - 'common/meta_types/user_range.yaml'
    - connection_type_uuid: APP1E-T0NXM

      parameter_name: app_annie_token
      display_name: App Annie Token
      description:  Credential token used to access the App Annie api.
      required: true
      type: connection

    - parameter_name: s3_info

      display_name: S3 Info
      type: group

    - connection_type_uuid: AWS5D-TO99M

      description: AWS Credentials with access to the s3 bucket where the data table lives.
      display_name: AWS Token Credentials
      parameter_name: aws_connection
      parameter_group: s3_info
      required: false
      type: connection

    - connection_type_uuid: AWSS3-BUCKT

      description: S3 Bucket where you want to unload the data to.
      display_name: S3 Bucket
      parameter_name: s3_bucket
      parameter_group: s3_info
      required: false
      type: connection

    - description: Path to a location where data files will be exported

      display_name: S3 Path
      parameter_name: s3_path
      parameter_group: s3_info
      required: True
      type: string
      max: 2048

    - parameter_name: format_options

      display_name: File/Formatting Options
      type: group

    - description: If specified will insert the date into the folder structure.  Example... y=1998/m=12/d=25/file_name.json.gz.

      display_name: Date Folders
      parameter_name: append_date
      parameter_group: format_options
      required: True
      type: enum
      default: True
      choices:

        - True
        - False

```

## nomigen_test_credentials.json

This file exists outside the engine folders, and should be placed in your copy of the engines-config repo, you can find an example of it there. This is where you can store your credentials required by tests. If you set the environment variable NOMIGEN_TEST_CREDENTIALS to the location of your copy of engines-config, these creds will be made accessible via the nomnomdata.engine.test_credentials module at runtime.

``` JSON
{
    "app_annie_token": {
        "token": "your_app_annie_token"
    },
    "aws_connection": {
        "aws_access_key_id": "your_aws_access_key",
        "aws_secret_access_key": "your_aws_secret_access_key"
    },
    "s3_bucket": {
        "bucket": "shughes-test-bucket"
    }
}
```

