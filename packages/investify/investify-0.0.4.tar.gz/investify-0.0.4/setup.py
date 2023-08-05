# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['investify']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.1,<8.0.0',
 'lxml>=4.5.0,<5.0.0',
 'requests>=2.23.0,<3.0.0',
 'twilio>=6.38.0,<7.0.0']

entry_points = \
{'console_scripts': ['investify = investify.investify:main']}

setup_kwargs = {
    'name': 'investify',
    'version': '0.0.4',
    'description': 'Get automated price alert based on investing.com prices',
    'long_description': "# investify\n\nUtility tool which scrapes investing.com website for price updates and send whatsapp notification if it breaches a predefined threshold.\n\n\n## Setup\n\nYou can clone the project and simply run the script. You need to have a [twilio](https://www.twilio.com/) account (a free one would do as well). Setup your whatsapp dashboard in twilio first and use that numbers in the script. For the authentication export your Account SSID and Authentication token as follows :-\n\nAccount SSID\n\n    $ export TWILIO_ACCOUNT_SID='ACXXXXXXXXXXXXXXXXXXXXXXXXXXX'\n\nAuthentication token\n\n    $ export TWILIO_AUTH_TOKEN='XXXXXXXXXXXXXXXXXXXXXXXXX'\n\n\n## Usage\n\n```bash\n$ python investify.py +1456789012 +31234567789 crypto btc-usd 6600-6700 --sub-market bitcoin --threshold 10\n```\nThis will notify when btc-usd prices breaches the price band of 6600-6700. It currently resets the price band from the last breached price.\n\nThe tool will logging INFO (or DEBUG) level messages in standard out. This can certainly be redirected to a specified log file.\n\nDebug level messages as follows :-\n```bash\n$ python investify.py --debug +11234567890 +7112356789 crypto btc-usd 6600-6700 --sub-market bitcoin --threshold 10 --interval 0.1\n2020-04-05 20:13:38 [DEBUG] main() - Logging set to debug\n2020-04-05 20:13:38 [DEBUG] main() - crypto/bitcoin/btc-usd end point will be queried.\n2020-04-05 20:13:39 [DEBUG]  run() - Fetched page successfully.\n2020-04-05 20:13:39 [DEBUG]  run() - Price of btc-usd is $6804.9.\n2020-04-05 20:13:39 [ INFO]  run() - Price 6804.9 breached price band [6600.0, 6700.0].\n2020-04-05 20:13:39 [DEBUG]  run() - Resetting price band with threshold value 10.0.\n2020-04-05 20:13:39 [ INFO]  run() - Resetting price band to [6798.0951, 6811.704899999999].\n2020-04-05 20:13:39 [DEBUG]  run() - Sending text.\n2020-04-05 20:13:46 [DEBUG]  run() - Fetched page successfully.\n2020-04-05 20:13:46 [DEBUG]  run() - Price of btc-usd is $6803.6.\n^C\n2020-04-05 20:13:49 [ INFO] main() - Caught interrupt, exiting...\n```\n\nHelp menu for the tool.\n```bash\n$ python investify.py -h\nUsage: investify.py [options...] [to number] [from number] [market] [contract]\n                    [priceband]\n\n  Utiltiy script to notify if instrument price fluctuates out of price band.\n\nOptions:\n  -s, --symbol TEXT      Contract symbol. [default: contract]\n  -t, --threshold FLOAT  Threshold in bps.  [default: 100.0]\n  -i, --interval FLOAT   Interval to perform check (mins).  [default: 1.0]\n  -m, --sub-market TEXT  E.g. crypto is market and bitcoin is sub market.\n  -d, --debug            Print debug messages.\n  -h, --help             Show this message and exit.\n```\n\n`to number` should be your whatsapp number whereas `from number` should the number given by Twilio to be used for your whatsapp sandbox. You can consult official Twilio for whatsapp [page](https://www.twilio.com/docs/whatsapp/api).\n",
    'author': 'Abhishek Guha',
    'author_email': 'abhi.workspace@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/abhi-g80/investify',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
