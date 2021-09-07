import subprocess
import sys

from pathlib import Path
from . import plist

VALID_USERS = ['any', 'current']


def defaults(domain: str, host: str = '-currentHost', user: str = 'current'):
    """Subprocess out to defaults to read preference domains

    :param domain (str): the preference domain to read, example: com.apple.Dock
    :param host (str): the host to read preferences from, defaults to current host"""
    # NOTE: '/usr/bin/defaults' may require full disk access
    result: dict = dict()
    defaults = '/usr/bin/defaults'
    host = host if host == '-currentHost' else f'-host {host}'
    domain = f'/Library/Preferences/{domain}' if user == 'any' else domain
    cmd = f'{defaults} {host} export {domain} -'.split(' ')
    p = subprocess.run(cmd, capture_output=True)

    if p.returncode == 0:
        result = plist.read_string(p.stdout)

    return result


def read(domain: str, host: str = 'any', user: str = 'current'):
    """Read preferences via pyobjc, fallback to 'defaults' subprocess

    :param domain (str): the preference domain to read, example: com.apple.Dock
    :param host (str): the host to read preferences from, defaults to any
    :param user (str): teh user to read preferences from, defaults to current"""
    # NOTE: 'kCFPreferencesCurrentHost' does not return any results if the
    #       'user' param is 'current', so 'host' param defaults to 'any',
    #       this behaviour appears to best replicate using the defaults command
    #       per the 'read' method in this package.
    if user not in VALID_USERS:
        raise ValueError(f'\'user\' must be one of {VALID_USERS}')

    result: dict = dict()

    # Some basic file path checking, attempt to read file path, fall back to
    # reading by domain.
    if ('/' in domain or domain.endswith('.plist')) and Path(domain).exists():
        result = plist.read(domain)
    else:
        try:
            from Foundation import (CFPreferencesCopyKeyList,
                                    CFPreferencesCopyMultiple,
                                    kCFPreferencesCurrentUser,
                                    kCFPreferencesAnyUser,
                                    kCFPreferencesCurrentHost,
                                    kCFPreferencesAnyHost,
                                    kCFPreferencesAnyApplication)
            from PyObjCTools.Conversion import pythonCollectionFromPropertyList  # Convert from NSNSDictionary to dict

            domain = kCFPreferencesAnyApplication if domain == 'NSGlobalDomain' else domain
            host = kCFPreferencesCurrentHost if host == '-currentHost' else kCFPreferencesAnyHost
            user = kCFPreferencesCurrentUser if user == 'current' else kCFPreferencesAnyUser
            keys = CFPreferencesCopyKeyList(domain, user, host)
            _result = CFPreferencesCopyMultiple(keys, domain, user, host)
            result = pythonCollectionFromPropertyList(_result)
        except ImportError:
            result = defaults(domain, host)

    return result


def list_domains(user: str = 'current'):
    """Subprocess out to defaults to list available preference domains

    param user (str): the user to read the preference as, defaults to current user"""
    result: list = list()
    cmd = ['/usr/bin/defaults', 'domains']
    p = subprocess.run(cmd, capture_output=True, encoding='utf-8')

    if p.returncode == 0:
        result = sorted([_.replace('.GlobalPreferences_m', '.GlobalPreferences') for _ in p.stdout.strip().split(', ')])
        print(*(r for r in result), sep='\n')
        sys.exit(0)
    else:
        print(p.stderr, file=sys.stdout)
        sys.exit(p.returncode)
