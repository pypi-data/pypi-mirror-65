# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['irons',
 'irons.Notebooks.A - Knowledge transfer.Inputs',
 'irons.Notebooks.A - Knowledge transfer.Modules',
 'irons.Toolbox.Data_management',
 'irons.Toolbox.Inflow_simulation',
 'irons.Toolbox.Reservoir_operating_policy',
 'irons.Toolbox.Reservoir_system_simulation',
 'irons.Toolbox.Weather_forecast',
 'irons.Toolbox.test_functions']

package_data = \
{'': ['*'],
 'irons': ['Toolbox/.pytest_cache/*',
           'Toolbox/.pytest_cache/v/cache/*',
           'Toolbox/test_functions/.pytest_cache/*',
           'Toolbox/test_functions/.pytest_cache/v/cache/*',
           'util/images/*']}

install_requires = \
['bqplot==0.11.6',
 'cdsapi==0.2.5',
 'ipywidgets==7.2.1',
 'matplotlib==3.1.1',
 'netcdf4==1.4.2',
 'numba==0.47.0',
 'numpy==1.16.5',
 'pandas==0.25.1',
 'platypus-opt==1.0.3',
 'plotly==4.4.1']

setup_kwargs = {
    'name': 'irons',
    'version': '0.1.3',
    'description': 'A Python package that enables the simulation, forecasting and optimisation of reservoir systems',
    'long_description': None,
    'author': 'Andres Peñuela',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
