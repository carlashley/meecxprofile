# meecxprofile
_Pronounced meeseeks_
MCX To Profile re-imagined in Python 3

This is a re-imagined version of the [MCX To Profile](https://github.com/timsutton/mcxToProfile) by Tim Sutton.

This version should be entirely self sufficient if the `pyobjc` package is not installed, although some TCC permissions such as `Full Disk` may need to be provided to `defaults`.

## Support
Support is provided "as is". This is not an exact replication of the original MCX To Profile project, but most functionality should exist.

## Usage
Three arguments are required:
```
./meecxprofile --identifier [identifier] --org-name [org name] --display-name [display name]
```

Optional (but mandatory) arguments:
Either `--plist [domain]` or `--ds-obj [ds object]` are required. A file path can also be provided with the `--plist` argument.

Optional arguments:
- `--desc [description]` to set the profile description
- `--removable` to set if the profile can be removed by users
- `--keys` provide a set of specifc keys (when used with `--plist`) or preference domain and values (when used with `--ds-obj`)
- `--freq` set the management frequency using (choices are `always` or `once`, default is `always`)
- `-o/--output` specify the filename to write profile data to (will always have the `.mobileconfig` file extension), default behavior is to print to `stdout`


## Filtering
It's possible to filter specific preferences that you want instead of returning the whole set of preferences.

### Property Lists
When the `--plist` argument is specified, simply provide the relevant preference key to filter. Items that don't match the specified keys will be discard.

For example, to filter the preferences in `com.apple.dock` so only `region`, `tilesize`,  and `autohide` are kept:
```
--keys region tilesize autohide
```

### MCX from Directory Services
When the `--ds-obj` argument is specified, provide either the preference domain, or preference domain and preference keys using this format:
`domain=preference`.
Multiple preference keys can be supplied for the one preference domain by using a comma seperated string:
`domain=preference1,preference2,preference3`.

It is also possible to filter by specific preference domain, simply supply the preference domain using this format:
`domain=`

#### Directory Services Syntax Examples
- `com.apple.MCX=` will discard any preference domain that is _not_ `com.apple.MCX`
- `com.apple.MCX=com.apple.cachedaccounts.CreateAtLogin` will filter the preference domain `com.apple.MCX` and discard any preference key that is _not_ `com.apple.cachedaccounts.CreateAtLogin`
- `com.apple.MCX=com.apple.cachedaccounts.CreateAtLogin,com.apple.cachedaccounts.WarnOnCreate` will filter the preference domain `com.apple.MCX` and discard any preference key that is _not_ `com.apple.cachedaccounts.CreateAtLogin` or `com.apple.cachedaccounts.WarnOnCreate`

Source sample:
```
{'com.apple.MCX': {'Forced': [{'mcx_preference_settings': {'com.apple.cachedaccounts.CreateAtLogin': True,
                                                           'com.apple.cachedaccounts.CreatePHDAtLogin': False,
                               'com.apple.cachedaccounts.WarnOnCreate': False}}]},
 'com.apple.dock': {'Forced': [{'mcx_preference_settings': {'AppItems-Raw': [],
                                                            'DocItems-Raw': [],
                                                            'contents-immutable': False,
                                                            'static-only': False},
                                'mcx_union_policy_keys': [{'mcx_input_key_names': ['AppItems-Raw'],
                                                           'mcx_output_key_name': 'static-apps',
                                                           'mcx_remove_duplicates': True},
                                                          {'mcx_input_key_names': ['DocItems-Raw'],
                                                           'mcx_output_key_name': 'static-others',
                                                           'mcx_remove_duplicates': True},
                                                          {'mcx_input_key_names': ['MCXDockSpecialFolders-Raw'],
                                                           'mcx_output_key_name': 'MCXDockSpecialFolders',
                                                           'mcx_remove_duplicates': True}]}]}}
```
