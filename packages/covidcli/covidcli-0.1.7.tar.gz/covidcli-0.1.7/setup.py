# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['covidcli']

package_data = \
{'': ['*'],
 'covidcli': ['.pytest_cache/*', '.pytest_cache/v/cache/*', 'data/*']}

install_requires = \
['click-help-colors>=0.8,<0.9',
 'click>=7.1.1,<8.0.0',
 'pandas==0.25.3',
 'pyfiglet>=0.8.post1,<0.9',
 'tabulate>=0.8.6,<0.9.0']

entry_points = \
{'console_scripts': ['covidcli = covidcli.covidcli:main']}

setup_kwargs = {
    'name': 'covidcli',
    'version': '0.1.7',
    'description': 'Covidcli- A CLI For Tracking and Getting Info About Coronavirus Outbreak',
    'long_description': '## Covidcli \n`covidcli` : A simple CLI for tracking and getting info about Coronavirus(covid19) Outbreak built with python.\n\n\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/covidcli)\n\n[![GitHub license](https://img.shields.io/github/license/Jcharis/covidcli)](https://github.com/Jcharis/covidcli/blob/master/LICENSE)\n\n\n#### Dependencies\n`covidcli` was designed with CLICK with the following dependencies\n+ pandas\n+ pyfiglet\n+ tabulate\n\n\n#### Installation\n```bash\npip install covidcli\n```\n\n#### Screenshot\n![](https://github.com/Jcharis/covidcli/blob/master/images/image01.png)\n\n\n![](https://github.com/Jcharis/covidcli/blob/master/images/image02.png)\n\n### Usage\n#### Show Cases of Coronavirus\n+ shows cases by the following cases ***confirmed|recovered|deaths|all***\n```bash\ncovidcli show confirmed\n```\n```bash\nShowing:: confirmed cases\n===========================================\nNumber of Confirmed Cases:: 5532341.0\n      Province/State         Country/Region      Lat      Long     Date  Confirmed\n0                NaN               Thailand  15.0000  101.0000  1/22/20        2.0\n1                NaN                  Japan  36.0000  138.0000  1/22/20        2.0\n2                NaN              Singapore   1.2833  103.8333  1/22/20        0.0\n3                NaN                  Nepal  28.1667   84.2500  1/22/20        0.0\n4                NaN               Malaysia   2.5000  112.5000  1/22/20        0.0\n...              ...                    ...      ...       ...      ...        ...\n31057            NaN                 Jersey  49.1900   -2.1100  3/23/20        0.0\n31058            NaN            Puerto Rico  18.2000  -66.5000  3/23/20        0.0\n31059            NaN  Republic of the Congo  -1.4400   15.5560  3/23/20        0.0\n31060            NaN            The Bahamas  24.2500  -76.0000  3/23/20        0.0\n31061            NaN             The Gambia  13.4667  -16.6000  3/23/20        0.0\n\n[31062 rows x 6 columns]\n\n```\n\n\n#### Get Latest Cases of Coronavirus\n```bash\ncovidcli get latest\n```\n```bash\nShowing Latest Cases\nAccessed Time::2020-03-24 11:18:56.031077\n=============================\n{\'Confirmed Cases\': 5532341.0, \'Recovered Cases\': 1980983.0, \'Death Cases\': 196876.0}\n\n```\n\n#### Get Previous Cases of Coronavirus\n```bash\ncovidcli get previous\n```\n```bash\nShowing Previous Cases\nPrevious Time::2020-03-22 09:13:44.128850\n=============================\n{\'Confirmed Cases\': 4283692, \'Recovered Cases\': 1606190, \'Death Cases\': 143329}\n\n\n```\n\n#### Fetch and Download Current Dataset\n+ Downloads a clean dataset of the covid19 outbreak in a csv format\n```bash\ncovidcli get dataset\n```\n\n\n#### Get Status of Cases By Country\n+ Get status of cases by countries either as all cases,confirmed,recovered or deaths.\n```bash\ncovidcli get status "Italy"\n```\n```bash\nGet Status of Cases\nCountry::Italy\nAccessed Time::2020-03-24 11:08:49.648721\n=============================\n{\'Confirmed Cases\': 497959.0, \'Recovered Cases\': 50954.0, \'Death Cases\': 39435.0}\n```\n\n#### Search Info By Country\n+ similar to the `get status` it searches for countries\n```bash\ncovidcli search "Italy" --cases confirmed \n```\n```bash\nSearched::Italy\n===================================\nAccessed Time:: 2020-03-24 11:11:40.266145\nTotal Number of confirmed Cases for Italy::497959.0\n\n```\nor\n```bash\ncovidcli search "China" \n```\n```bash\nSearched::China\n===================================\nShowing Latest Data\nAccessed Time:: 2020-03-24 11:12:44.237260\n       Province/State Country/Region      Lat      Long     Date  Confirmed  Recovered  Deaths\n154             Hubei          China  30.9756  112.2707  1/22/20      444.0       28.0    17.0\n158         Guangdong          China  23.3417  113.4244  1/22/20       26.0        0.0     0.0\n159             Henan          China  33.8820  113.6140  1/22/20        5.0        0.0     0.0\n160          Zhejiang          China  29.1832  120.0934  1/22/20       10.0        0.0     0.0\n161             Hunan          China  27.6104  111.7088  1/22/20        4.0        0.0     0.0\n...               ...            ...      ...       ...      ...        ...        ...     ...\n30749  Inner Mongolia          China  44.0935  113.9448  3/23/20       75.0       74.0     1.0\n30750         Ningxia          China  37.2692  106.1655  3/23/20       75.0       75.0     0.0\n30754         Qinghai          China  35.7452   95.9956  3/23/20       18.0       18.0     0.0\n30755           Macau          China  22.1667  113.5500  3/23/20       24.0       10.0     0.0\n30763           Tibet          China  31.6927   88.0924  3/23/20        1.0        1.0     0.0\n\n[2046 rows x 8 columns]\n\n```\n\n#### Get/Show Cases By Date\n```bash\ncovidcli get date 2020-02-20\n```\n```bash\nShowing 2020-02-20 Cases Worldwide \nAccessed Time::2020-03-25 13:41:46.182374\n=============================\nAnalysing Data:  [####################################]  100%\nShowing Case For 2020-02-20\n             Confirmed  Recovered  Deaths\ncases_dates                              \n2020-02-20     76197.0    18177.0  2247.0\n\n```\n\n#### Compare Cases of Multiple Countries\n```bash\ncovidcli compare China Italy Nigeria US\n```\n```bash\nComparison of (\'China\', \'US\', \'Italy\', \'Nigeria\') Affected\nAccessed Time::2020-03-25 13:45:34.795250\n=============================\n                Confirmed  Recovered    Deaths\nCountry/Region                                \nChina           3531169.0  1787212.0  119412.0\n                Confirmed  Recovered  Deaths\nCountry/Region                              \nUS               159039.0      427.0  2276.0\n                Confirmed  Recovered   Deaths\nCountry/Region                               \nItaly            497959.0    50954.0  39435.0\n                Confirmed  Recovered  Deaths\nCountry/Region                              \nNigeria             139.0        8.0     0.0\n\n```\n\n#### For US States\n```bash\ncovidcli get usa Washington\n```\n```bash\nState::Washington\nAccessed Time::2020-04-10 00:50:08.332228\n=============================\n{\'Confirmed Cases\': 3688, \'Death Cases\': 244}\n\n```\n\n#### Credits For Data\n+ https://github.com/CSSEGISandData\n\n#### Fixes and Update\n** Added **\n+ Comparison Between Countries\n+ Get Cases By Date\n+ Active Cases\n\n** Fixes **\n+ Data Discrepancy\n\n\n#### By \n+ Jesse E.Agbe(JCharis)\n+ Jesus Saves @JCharisTech\n\n\n\n#### NB\n+ Contributions Are Welcomed\n+ Notice a bug, please let us know.\n+ Thanks A lot',
    'author': 'Jesse E.Agbe(JCharis)',
    'author_email': 'jcharistech@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Jcharis/covidcli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.3,<4.0',
}


setup(**setup_kwargs)
