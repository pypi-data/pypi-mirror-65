# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['onlytld']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'onlytld',
    'version': '0.0.4',
    'description': '',
    'long_description': '# onlyTLD\n\nJust only get TLD from domain. No other function. No non-standard library dependencies.\n\nBecause it is simple, it is fast. **One million** queries only require **2.4s**.\n\n## How to use\n\nIn Python3.5+:\n\n```python\nfrom onlytld import get_tld\n\nassert get_tld("chinese.cn") == "cn"\n```\n\n**Support punycode-encoded domain names**: if a punycode-encoded domain is passed in, a punycode-encoded domain will be returned, otherwise a utf8 string will be returned.\n\n## Update TLD List\n\nRefer to https://www.publicsuffix.org/list/, you can run `onlytld.data.fetch_list` regularly in the code or run` python -m onlytld.data` in crontab.\n\n## Use yourself TLD List\n\nMaybe this is useless, but I still set this function.\n\n```python\nfrom onlytld import set_datapath, get_tld\n\nset_datapath(YOUR_FILE_PATH)\n\nassert get_tld("chinese.cn") == "cn"\n```\n\n## Why this\n\nThere are many libraries in pypi that can get tld, such as [publicsuffix2](https://pypi.org/project/publicsuffix2/), [publicsuffixlist](https://pypi.org/project/publicsuffixlist/), [dnspy](https://pypi.org/project/dnspy/), but they have too many functions. I just need a repository that can get tld, and it is best not to have dependencies other than the non-standard library.\n',
    'author': 'abersheeran',
    'author_email': 'me@abersheeran.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/abersheeran/onlytld',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
