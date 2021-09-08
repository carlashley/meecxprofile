import re
import subprocess
import sys

from collections import namedtuple
from pathlib import PurePath

from . import plist


def filter_keys(keys: list):
    """Process filter keys from command line

    :param keys (list): keys to process"""
    # This list gets converted to a dictionary to better handle scenarios of domain/domain value pairs/value
    result = {'by_domains': set(),
              'by_domain_values': dict(),
              'by_values': set()}

    for key in keys:
        if '=' in key:
            domain, value = key.split('=')

            if value and ',' in value:
                value = set(value.split(','))

            if domain and value:
                if not result['by_domain_values'].get(domain):
                    result['by_domain_values'][domain] = set()

                if isinstance(value, set):
                    result['by_domain_values'][domain].union(value)
                else:
                    result['by_domain_values'][domain].add(value)

            if domain and not value:
                result['by_domains'].add(domain.rstrip('='))

            if value and not domain:
                result['by_values'].add(value.lstrip('='))
        else:
            result['by_values'].add(key.lstrip('='))

    return result


def plist_domain_from_path(p: str):
    """Assuming the domain is also the name of the plist file, strip the path and the ending '.plist'
    The regex handles if .ByHost is in the path, or if a MAC address/hardware UUID is in the path

    :param p (str): 'path' - actual file path or other string with a value to scrape preference domain from"""
    result: dict = dict()
    Result = namedtuple('Result', ['by_host', 'name'])
    host_reg = re.compile(r'\.ByHost$|\.[0-9a-fA-F]{12}$|\.[0-9a-fA-F]{8}-([0-9a-fA-F]{4}-){3}[0-9a-fA-F]{12}$')
    basename: str = PurePath(p).name
    _domain: str = PurePath(basename).stem if basename.endswith('.plist') else basename  # Don't take stem if not plist
    _by_host: bool = True if re.search(host_reg, _domain) else False

    result = Result(by_host=_by_host, name=_domain)

    return result


def mcx_from_ds_object(ds_obj: str, keys: dict = dict()):
    """Returns MCX data from a Directory Services object

    :param ds_obj (str): Directory services object, for example /LDAP/Users/jappleseed
    :param keys (list): list of keys or key=value to remove from payload"""
    result: list = list()
    mcx_frequencies = ['Always', 'Forced', 'Often', 'Once', 'Set-Once']
    obj = [s for s in ds_obj.split('/') if not s == '']
    ds_node, ds_path = f'/{obj[0]}', '/'.join(obj[1:])
    cmd = ['/usr/bin/dscl', '-plist', ds_node, 'read', ds_path, 'MCXSettings']
    p = subprocess.run(cmd, capture_output=True, encoding='utf-8')

    if p.returncode == 0:
        # MCX data might be stored in an XML string in the dscl
        data = plist.read_from_string(p.stdout.encode()).get('dsAttrTypeStandard:MCXSettings')
        is_list = isinstance(data, list)

        if data and is_list:
            for item in data:
                mcx_prefs = plist.read_from_string(item.encode()).get('mcx_application_data')
                mcx_prefs_cp = mcx_prefs.copy()

                # Filter out keys not specified, this is a messy nesting of loops
                for mcx_key, mcx_val in mcx_prefs_cp.items():
                    for freq in mcx_frequencies:
                        if mcx_val.get(freq):
                            for elem in mcx_val[freq]:
                                if elem.get('mcx_preference_settings'):
                                    for pref_key, _ in elem['mcx_preference_settings'].copy().items():
                                        index = mcx_val[freq].index(elem)
                                        filter_domains = keys['by_domains']
                                        filter_domain_values = keys['by_domain_values'].get(mcx_key)

                                        # Ignoring filtering by values only, must supply a domain=value filter if specific domain values are to be kept
                                        if filter_domain_values and pref_key not in filter_domain_values:
                                            try:
                                                del mcx_prefs[mcx_key][freq][index]['mcx_preference_settings'][pref_key]
                                            except KeyError:
                                                pass

                                        # Remove any mcx pref domains that are not in the filter, _last_
                                        if filter_domains and mcx_key not in filter_domains:
                                            try:
                                                del mcx_prefs[mcx_key]
                                            except KeyError:
                                                pass
                if mcx_prefs:
                    result.append(mcx_prefs)
    else:
        print(p.stderr, file=sys.stderr)
        sys.exit(p.returncode)

    return result
