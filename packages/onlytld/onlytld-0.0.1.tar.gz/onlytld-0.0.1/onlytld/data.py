"""
TLD data

Data from https://github.com/publicsuffix/list/
"""
from os import path
from urllib import request
from typing import Tuple, Set

datapath = path.join(path.dirname(path.abspath(__file__)), "list.dat")


def set_datapath(filepath: str) -> None:
    """
    custom data file path
    """
    global datapath
    datapath = filepath


def fetch_list() -> None:
    """
    fetch TLD list from https://www.publicsuffix.org/list/public_suffix_list.dat
    """
    request.urlretrieve(
        "https://www.publicsuffix.org/list/public_suffix_list.dat", datapath
    )


def parse_list() -> Tuple[Set[str], Set[str], Set[str]]:
    """
    parse rule to three kind: normal, wildcard, exception
    """
    with open(datapath, encoding="utf8") as file:
        txt = file.read()
    datalist = txt.split("// ===END ICANN DOMAINS===")[0]
    normal, wildcard, exception = set(), set(), set()
    for line in datalist.splitlines():  # line: str
        if line.startswith("//"):
            continue
        if line.startswith("*"):
            wildcard.add(line[2:])
        elif line.startswith("!"):
            exception.add(line[1:])
        else:
            normal.add(line)
    return normal, wildcard, exception


if __name__ == "__main__":
    fetch_list()
