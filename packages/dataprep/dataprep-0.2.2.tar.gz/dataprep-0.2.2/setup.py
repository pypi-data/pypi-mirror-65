# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['dataprep',
 'dataprep.data_connector',
 'dataprep.eda',
 'dataprep.eda.basic',
 'dataprep.eda.correlation',
 'dataprep.eda.missing',
 'dataprep.eda.outlier',
 'dataprep.tests',
 'dataprep.tests.eda']

package_data = \
{'': ['*']}

install_requires = \
['bokeh>=2.0,<2.1',
 'dask[complete]>=2.13,<2.14',
 'holoviews>=1.13,<1.14',
 'jinja2>=2.11,<2.12',
 'jsonpath2>=0.4,<0.5',
 'jsonschema>=3.2,<3.3',
 'lxml>=4.5,<4.6',
 'numpy>=1.18,<1.19',
 'pandas>=1.0,<1.1',
 'requests>=2.23,<2.24',
 'scipy>=1.4,<1.5']

setup_kwargs = {
    'name': 'dataprep',
    'version': '0.2.2',
    'description': 'Dataprep: Data Preparation in Python',
    'long_description': '# Dataprep ![Build Status]\n[Documentation] | [Mail List & Forum] \n\nDataprep let you prepare your data using a single library with a few lines of code.\n\nCurrently, you can use `dataprep` to:\n* Collect data from common data sources (through `dataprep.data_connector`)\n* Do your exploratory data analysis (through `dataprep.eda`)\n* ...more modules are coming\n\n## Installation\n\n```bash\npip install dataprep\n```\n\n## Examples & Usages\n\nDetailed examples can be found in the [examples] folder.\n\n### EDA\n\nThere are common tasks during the exploratory data analysis stage, \nlike a quick look at the columnar distribution, or understanding the correlations\nbetween columns. \n\nThe EDA module categorizes these EDA tasks into functions helping you finish EDA\ntasks with a single function call.\n\n* Want to understand the distributions for each DataFrame column? Use `plot`.\n```python\nfrom dataprep.eda import plot\n\ndf = ...\n\nplot(df)\n```\n<center><img src="https://github.com/sfu-db/dataprep/raw/master/assets/plot(df).png"/></center>\n\n* Want to understand the correlation between columns? Use `plot_correlation`.\n\n```python\nfrom dataprep.eda import plot_correlation\n\ndf = ...\n\nplot_correlation(df)\n```\n<center><img src="https://github.com/sfu-db/dataprep/raw/master/assets/plot_correlation(df).png" width="50%" height="50%"/></center>\n\n* Or, if you want to understand the impact of the missing values for each column, use `plot_missing`.\n\n```python\nfrom dataprep.eda import plot_missing\n\ndf = ...\n\nplot_missing(df)\n```\n<center><img src="https://github.com/sfu-db/dataprep/raw/master/assets/plot_missing(df).png" width="50%" height="50%"/></center>\n\n* You can even drill down to get more information by given `plot`, `plot_correlation` and `plot_missing` a column name.\n\n```python\ndf = ...\n\nplot_missing(df, x="some_column_name")\n```\n\n<center><img src="https://github.com/sfu-db/dataprep/raw/master/assets/plot_missing(df,x).png" width="50%"/></center>\n\nDon\'t forget to checkout the [examples] folder for detailed demonstration!\n\n### Data Connector\n\nYou can download Yelp business search result into a pandas DataFrame, \nusing two lines of code, without taking deep looking into the Yelp documentation!\n\n```python\nfrom dataprep.data_connector import Connector\n\ndc = Connector("yelp", auth_params={"access_token":"<Your yelp access token>"})\ndf = dc.query("businesses", term="ramen", location="vancouver")\n```\n![DataConnectorResult]\n\n\n## Contribution\n\nDataprep is in its early stage. Any contribution including:\n* Filing an issue\n* Providing use cases\n* Writing down your user experience\n* Submitting a PR\n* ...\n\nare greatly appreciated!\n\nPlease take a look at our [wiki] for development documentations!\n\n\n[Build Status]: https://img.shields.io/circleci/build/github/sfu-db/dataprep/master?style=flat-square&token=f68e38757f5c98771f46d1c7e700f285a0b9784d\n[Documentation]: https://sfu-db.github.io/dataprep/\n[Mail list & Forum]: https://groups.google.com/forum/#!forum/dataprep\n[wiki]: https://github.com/sfu-db/dataprep/wiki\n[examples]: https://github.com/sfu-db/dataprep/tree/master/examples\n[DataConnectorResult]: https://github.com/sfu-db/dataprep/raw/master/assets/data_connector.png\n',
    'author': 'SFU Database System Lab',
    'author_email': 'dsl.cs.sfu@gmail.com',
    'url': 'https://github.com/sfu-db/dataprep',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
