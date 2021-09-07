import re

from collections import namedtuple
from pathlib import PurePath


def plist_domain_from_path(p: str):
    """Assuming the domain is also the name of the plist file, strip the path and the ending '.plist'
    The regex handles if .ByHost is in the path, or if a MAC address/hardware UUID is in the path

    :param p (str): 'path' - actual file path or other string with a value to scrape preference domain from"""
    result: dict = dict()
    Result = namedtuple('Result', ['by_host', 'name'])
    host_reg = re.compile(r'\.ByHost$|\.[0-9a-fA-F]{12}$|\.[0-9a-fA-F]{8}-([0-9a-fA-F]{4}-){3}[0-9a-fA-F]{12}$')
    basename: str = PurePath(p).name
    _domain: str = PurePath(basename).stem
    _by_host: bool = True if re.search(host_reg, _domain) else False

    result = Result(by_host=_by_host, name=_domain)

    return result
