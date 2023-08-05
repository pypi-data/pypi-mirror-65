# MPM Model Performance Monitoring client

## Installation
Requires Python3.
<pre>
$ pip3 install dcyd -U
$ dcyd-config <i>AN_ALPHANUMERIC_USERNAME</i>
$ export DCYD_CONFIG_FILE=<i>/some/path/</i>dcyd.json
</pre>
`dcyd.json` lands in the local directory by default. It can be moved around, as long as its new path is re-exported in step 3.
## Usage

Here are some usage examples.

### Barebones decorator of your `predict` function:
<pre>
from dcyd.mpm import mpm

@mpm
def my_predict_function(<i>some args</i>, <i>some kwargs</i>):
    ...

    return <i>some response</i>
</pre>

### Decorate your `predict` function, but include some metadata (e.g. `customer_id`, `experiment_group`, `model_version`, `caller_id`, `environment`) for helpful tracking: 
<pre>
from dcyd.mpm import mpm

@mpm(customer_id='asf434', `model_version=2.2, ...)
def my_other_predict_function(<i>some args</i>, <i>some kwargs</i>):
    ...

    return <i>some response</i>
</pre>

###Decorate a method as well:
<pre>
from dcyd.mpm import mpm

class MyModel(object):

  @mpm(transaction_id='a113fdf3434', ...)
  def my_predict_method(self, *args, **kwargs):
    ...
    return <i>some response</i>
</pre>

## Development

1. Clone the repo locally, and switch to a branch other than `master`.
2. Create and activate a virtual environment:
<pre>
$ python3 -m venv <i>my_env_name</i>
</pre>
3. From the directory containing `setup.py`:
```
$ pip3 install .
```
or
```
$ pip3 install -e .
```
(These are in place of `python3 setup.py install` and `python3 setup.py develop`, for reasons explained [here](https://stackoverflow.com/questions/19048732/python-setup-py-develop-vs-install).

### Distributing the package in PyPI

This process comes from [this turorial](https://packaging.python.org/tutorials/packaging-projects/).
1. Increment the version in `setup.py`, using [these rules](https://www.python.org/dev/peps/pep-0440/) (or newer).
2. Install/update some modules:
```
$ pip3 install --user --upgrade setuptools wheel twine
```
3. From the directory containing `setup.py` (and _not_ in a virtual environment), create the wheel:
```
$ rm -rf build/ dist/
$ python3 setup.py sdist bdist_wheel
```
4. Upload the wheel to PyPI:
```
$ python3 -m twine upload dist/*
```
