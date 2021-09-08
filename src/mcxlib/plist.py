import plistlib


def dump(data: dict):
    """Print property list to stdout"""
    print(plistlib.dumps(data, fmt=plistlib.FMT_XML).decode('utf-8').strip())


def read(f: str):
    """Read property list"""
    result: dict = dict()

    with open(f, 'rb') as _f:
        result = plistlib.load(_f)

    return result


def read_from_string(s: bytes):
    """Read property list"""
    result: dict = plistlib.loads(s)

    return result


def write(data: dict, f: str):
    """Write property list"""
    with open(f, 'wb') as _f:
        plistlib.dump(data, _f)
