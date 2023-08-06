from typing import Optional

from .data import parse_list

normal, wildcard, exception = None, None, None


def get_tld(domain: str) -> Optional[str]:
    """
    return domain's TLD or None
    """
    global normal, wildcard, exception
    if normal is None or wildcard is None or exception is None:
        normal, wildcard, exception = parse_list()

    for i in range(domain.count(".") + 1):
        suffix = ".".join(domain.split(".")[i:])
        if suffix in exception:
            return ".".join(suffix.split(".")[1:])
        if ".".join(suffix.split(".")[1:]) in wildcard:
            return suffix
        if suffix in normal:
            return suffix
    return None
