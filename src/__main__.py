from mcxlib import arguments
from mcxlib import common
from mcxlib import defaults
from mcxlib import payload
from mcxlib import plist


def main():
    """main"""
    args = arguments.construct()
    profile = payload.Profile(identifier=args.identifier,
                              organization=args.organization,
                              display_name=args.display_name,
                              removal_allowed=args.removable,
                              description=args.description)

    if args.plist:
        for obj in args.plist:
            source_domain = common.plist_domain_from_path(p=obj)
            preferences = defaults.read(domain=obj)
            profile.add_payload_from_plist(payload=preferences,
                                           domain=source_domain.name,
                                           manage=args.frequency,
                                           by_host=source_domain.by_host,
                                           keys=args.keys)

    if profile.data:
        if args.output:
            plist.write(profile.data, args.output)
        else:
            print(plist.print(profile.data))


if __name__ == '__main__':
    main()
