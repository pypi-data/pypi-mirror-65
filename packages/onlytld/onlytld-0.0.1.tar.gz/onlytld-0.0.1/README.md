# onlyTLD

Just only get TLD from domain. No other function. No non-standard library dependencies.

## How to use

In Python3.5+:

```python
from onlytld import get_tld

assert get_tld("chinese.cn") == "cn"
```

## Update TLD List

Refer to https://www.publicsuffix.org/list/, you can run `onlytld.data.fetch_list` regularly in the code or run` python -m onlytld.data` in crontab.

## Use yourself TLD List

Maybe this is useless, but I still set this function.

```python
from onlytld import set_datapath, get_tld

set_datapath(YOUR_FILE_PATH)

assert get_tld("chinese.cn") == "cn"
```

## Why this

There are many libraries in pypi that can get tld, such as [publicsuffix2](https://pypi.org/project/publicsuffix2/), [publicsuffixlist](https://pypi.org/project/publicsuffixlist/), [dnspy](https://pypi.org/project/dnspy/), but they have too many functions. I just need a repository that can get tld, and it is best not to have dependencies other than the non-standard library.
