# mvb python scripts

misc python scripts by @michaelsvanbeek

Mainly helper functions to ease common Jupyter Notebook, IPython, and Pandas workflows.

## Install

```
pip install mvb
```

PyPi: [https://pypi.org/project/mvb/](https://pypi.org/project/mvb/)

Github: [https://github.com/michaelsvanbeek/mvb_py](https://github.com/michaelsvanbeek/mvb_py)

### Dev Notes

Configure `.pypirc` in HOME directory.  Set username and password.

Compute build and dist directories
```
python setup.py build sdist
```

Upload dist to PyPi
```
twine upload dist/*
```
