# -*- coding: utf-8 -*-
from setuptools import setup

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
    'version': '0.2.3',
    'description': 'Dataprep: Data Preparation in Python',
    'long_description': '# Dataprep ![Build Status]\n[Documentation] | [Mail List & Forum] \n\nDataprep let you prepare your data using a single library with a few lines of code.\n\nCurrently, you can use `dataprep` to:\n* Collect data from common data sources (through `dataprep.data_connector`)\n* Do your exploratory data analysis (through `dataprep.eda`)\n* ...more modules are coming\n\n## Installation\n\n```bash\npip install dataprep\n```\n\n## Examples & Usages\n\nThe following examples can give you an impression of what dataprep can do:\n\n* [Documentation: Data Connector](https://sfu-db.github.io/dataprep/data_connector.html)\n* [Documentation: EDA](https://sfu-db.github.io/dataprep/eda/introduction.html)\n* [EDA Case Study: Titanic](https://sfu-db.github.io/dataprep/case_study/titanic.html)\n* [EDA Case Study: House Price](https://sfu-db.github.io/dataprep/case_study/house_price.html)\n\n### EDA\n\nThere are common tasks during the exploratory data analysis stage, \nlike a quick look at the columnar distribution, or understanding the correlations\nbetween columns. \n\nThe EDA module categorizes these EDA tasks into functions helping you finish EDA\ntasks with a single function call.\n\n* Want to understand the distributions for each DataFrame column? Use `plot`.\n\n<center><a href="https://sfu-db.github.io/dataprep/eda/introduction.html#analyzing-basic-characteristics-via-plot"><img src="https://github.com/sfu-db/dataprep/raw/master/assets/plot(df).png"/></a></center>\n\n* Want to understand the correlation between columns? Use `plot_correlation`.\n\n<center><a href="https://sfu-db.github.io/dataprep/eda/introduction.html#analyzing-correlation-via-plot-correlation"><img src="https://github.com/sfu-db/dataprep/raw/master/assets/plot_correlation(df).png"/></a></center>\n\n* Or, if you want to understand the impact of the missing values for each column, use `plot_missing`.\n\n<center><a href="https://sfu-db.github.io/dataprep/eda/plot_missing.html#plotting-the-position-of-missing-values-via-plot-missing-df"><img src="https://github.com/sfu-db/dataprep/raw/master/assets/plot_missing(df).png"/></a></center>\n\n* You can drill down to get more information by given `plot`, `plot_correlation` and `plot_missing` a column name. E.g. for `plot_missing`:\n\n<center><a href="https://sfu-db.github.io/dataprep/eda/plot_missing.html#the-impact-on-basic-characteristics-of-missing-values-in-column-x-via-plot-missing-df-x"><img src="https://github.com/sfu-db/dataprep/raw/master/assets/plot_missing(df,x).png"/></a></center>\n\nDon\'t forget to checkout the [examples] folder for detailed demonstration!\n\n### Data Connector\n\nYou can download Yelp business search result into a pandas DataFrame, \nusing two lines of code, without taking deep looking into the Yelp documentation!\n\n```python\nfrom dataprep.data_connector import Connector\n\ndc = Connector("yelp", auth_params={"access_token":"<Your yelp access token>"})\ndf = dc.query("businesses", term="korean", location="seattle")\n```\n<center><a href="https://sfu-db.github.io/dataprep/data_connector.html#getting-web-data-with-connector-query"><img src="https://github.com/sfu-db/dataprep/raw/master/assets/data_connector.png"/></a></center>\n\n\n## Contribution\n\nDataprep is in its early stage. Any contribution including:\n* Filing an issue\n* Providing use cases\n* Writing down your user experience\n* Submitting a PR\n* ...\n\nare greatly appreciated!\n\nPlease take a look at our [wiki] for development documentations!\n\n\n[Build Status]: https://img.shields.io/circleci/build/github/sfu-db/dataprep/master?style=flat-square&token=f68e38757f5c98771f46d1c7e700f285a0b9784d\n[Documentation]: https://sfu-db.github.io/dataprep/\n[Mail list & Forum]: https://groups.google.com/forum/#!forum/dataprep\n[wiki]: https://github.com/sfu-db/dataprep/wiki\n[examples]: https://github.com/sfu-db/dataprep/tree/master/examples\n',
    'author': 'SFU Database System Lab',
    'author_email': 'dsl.cs.sfu@gmail.com',
    'maintainer': 'Weiyuan Wu',
    'maintainer_email': 'youngw@sfu.com',
    'url': 'https://github.com/sfu-db/dataprep',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
