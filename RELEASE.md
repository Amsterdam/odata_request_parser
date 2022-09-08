# How to release a new distribution of this project

First update the version number in `pyproject.toml`. 

Then build the project, this will create the `dist` folder

```> python3 -m build```

Then create the file  `~/.pypirc` locally with the following content

```[distutils]
index-servers =
    odata-request-parser

[odata-request-parser]
  repository = https://upload.pypi.org/legacy/
  username = __token__
  password = <PYPI api token>
```   

You can now upload the latest distribution of the project to PYPI

```> python3 -m twine upload --repository odata-request-parser --skip-existing dist/* ```