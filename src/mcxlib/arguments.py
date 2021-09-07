import argparse
import sys

from pathlib import PurePath


def error(msg: str, fatal: bool = True, returncode: int = 1):
    """Print arg error"""
    print(f'{sys.argv[0]}: error: argument: {msg}', file=sys.stderr)

    if fatal:
        sys.exit(returncode)


def construct():
    """Create arguments for command line use"""
    result = None
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    add, exc = parser.add_argument, group.add_argument

    # Required for creating the profile
    add('--identifier',
        type=str,
        dest='identifier',
        metavar='[identifier]',
        required=True,
        help='profile bundle identifier, for example \'org.example.foo\'')

    add('--org-name',
        type=str,
        dest='organization',
        metavar='[organization]',
        required=True,
        help='profile organization, for example \'ACME Inc.\'')

    add('--display-name',
        type=str,
        dest='display_name',
        metavar='[display name]',
        required=True,
        help='profile display name, for example \'MCX Settings for ACME\'')

    # Optionals
    add('--desc',
        type=str,
        default='MCX Custom Settings for:\n',
        dest='description',
        metavar='[description]',
        required=False,
        help='profile description, for example \'Includes MCX settings for ACME App\'')

    add('--removable',
        action='store_true',
        default=False,
        dest='removable',
        required=False,
        help='profile can be removed by users, default is disallow (False)')

    exc('--plist',
        type=str,
        nargs='*',
        dest='plist',
        metavar='[plist]',
        required=False,
        help='read from specified property list file or preference domain')

    add('--keys',
        type=str,
        nargs='*',
        default=list(),
        dest='keys',
        metavar='[keys]',
        required=False,
        help=('read specified keys from specified property list file or preference domain'
              ' (does not remove nested keys)'))

    exc('--ds-obj',
        type=str,
        dest='ds_object',
        metavar='[object]',
        required=False,
        help='Directory services object, for example \'/LDAPv3/example/Computers/foo\'')

    add('--freq',
        type=str,
        choices=['always', 'once'],
        default='always',
        dest='frequency',
        metavar='[frequency]',
        required=False,
        help='management frequency, default is \'Always\'')

    add('-o', '--out',
        type=str,
        dest='output',
        metavar=['destination'],
        required=False,
        help='write output to specified destination, for example \'~/Documents/meecxprofile.mobileconfig\'')

    args = parser.parse_args()
    args.frequency = args.frequency.capitalize()

    # Do args checks here
    if args.ds_object:
        error(msg='\'--ds-object\' is not yet implemented')

    if not (args.ds_object or args.plist):
        parser.print_usage()
        error(msg='one of \'--ds-object\', \'--plist\' must be provided')

    if args.keys and not (args.ds_object or args.plist):
        parser.print_usage()
        error(msg='\'--keys\' can only be used with either \'--ds-object\' or \'--plist\'')

    if args.output and not PurePath(args.output).suffix == '.mobileconfig':
        suffix = PurePath(args.output).suffix
        new_fn = args.output.replace(suffix, '.mobileconfig')
        print(f'File \'{args.output}\' renamed to \'{new_fn}\'')
        args.output = new_fn

    result = args

    return result
