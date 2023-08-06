NAME: str = "init"
DESCRIPTION: str = """\
            Creates a Python virtual environment based on the configuration
            of an existing 'caos.yml' file in the current directory.
            
            If the 'caos.yml' file is not present in the current directory a
            new virtual environment and configuration file are created.\
"""
CLI_USAGE_EXAMPLE: str = """\
            caos init    
            caos init [VIRTUAL_ENV_NAME]
"""

_CAOS_YAML_TEMPLATE="""\
virtual_environment: "{VENV_NAME}"

dependencies:
  pip: "latest"
#  requests: "2.0.0"  # Allow only Exact version
#  numpy: "^1.18.2" # Allow only Minor version changes
#  flask: "~1.1.0"  # Allow only Patch version changes
#  tensorflow: "./local_libs/tensorflow-1.13.1-py3-none-any.whl" # Local WHl
#  tensorflow: "https://storage.googleapis.com/tensorflow/mac/cpu/tensorflow-1.14.0-py3-none-any.whl" # Remote WHl

tasks:
  unittest:
    - "caos python -m unittest discover -v ./"
#
#  start:
#    - "caos python ./main.py"
#
#  test_and_start:
#    - unittest
#    - start
#    - "echo 'Done'"
"""
