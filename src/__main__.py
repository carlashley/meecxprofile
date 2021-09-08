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
                                           keys=args.keys['by_values'])

    if args.ds_object:
        for ds_obj in args.ds_object:
            mcx_data = common.mcx_from_ds_object(ds_obj=ds_obj,
                                                 keys=args.keys)

            if mcx_data:
                for mcx_payload in mcx_data:
                    profile.add_payload_from_mcx(payload=mcx_payload)

    if profile.data:
        if args.output:
            plist.write(profile.data, args.output)
        else:
            plist.dump(profile.data)


if __name__ == '__main__':
    main()
