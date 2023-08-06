<p align="center">
    <a href="https://github.com/caotic-co/caos" target="_blank">
        <img src="https://github.com/caotic-co/caos/blob/master/img/caos.png" height="100px">
    </a>
    <br>
</p>
<p align="center">A simple dependency management tool and tasks executor for Python projects</p> 

[![](https://img.shields.io/pypi/v/caos)](https://pypi.org/project/caos/)
[![](https://img.shields.io/pypi/dm/caos)](https://pypi.org/project/caos/)
[![](https://img.shields.io/github/license/caotic-co/caos)](https://raw.githubusercontent.com/caotic-co/caos/master/LICENSE)
[![](https://img.shields.io/circleci/build/github/caotic-co/caos/master?token=e824c21be60f20bf89d42a743fd56cff55bf20fc)](https://app.circleci.com/pipelines/github/caotic-co/caos)

Installation
------------
Make sure that you have a working **Python >= 3.6** with **pip** and **virtualenv** installed and then execute   
~~~
pip install caos
~~~


Usage Example
------------
<p>
    <img src="https://github.com/caotic-co/caos/blob/master/img/usage_example.gif" height="400px">
</p>

The previous example has the following structure:
~~~
my_project
├── caos.yml
├── main.py
└── tests
    └── test.py
~~~


This is the content of the **caos.yml** file:
```yaml
virtual_environment: "venv"

dependencies:
  pip: "latest"
  flask: "~1.1.0"

tasks:
  unittest:
    - "caos python -m unittest discover -v ./tests"

  start:
    - "caos python ./main.py"

  test_and_start:
    - unittest
    - start
```

This is the content of the **main.py** file:
```python
from flask import Flask
app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello World!"

if __name__ == '__main__':
    app.run(host="127.0.0.1", port="8080")
```

This is the content of the **test.py** file:
```python
import unittest
from main import app

class TestApp(unittest.TestCase):

    def test_hello_world(self):
        self.app = app.test_client()
        response = self.app.get('/')
        self.assertEqual(200, response.status_code)
        self.assertIn(b'Hello World!', response.data)


if __name__ == '__main__':
    unittest.main()
```

For more information about the usage and how to contribute check the [Documentation](https://github.com/caotic-co/caos/blob/master/docs/README.md).
