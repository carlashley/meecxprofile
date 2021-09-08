from pprint import pformat

ds_obj_mcx_note = ('The MCX data returned back from \'dscl\' is a string nested in the attribute queried.\n'
                   'Settings can be filtered by using key filters.\n'
                   'Multiple values can be filtered for specific domains by comma seperating the values\n'
                   'Filter syntax examples:\n'
                   ' - \'com.apple.MCX=\' will keep the preference domain \'com.apple.MCX\'.\n'
                   ' - \'com.apple.MCX=com.apple.cachedaccounts.CreateAtLogin\' will keep the preference\n'
                   '   domain value from the \'com.apple.MCX\' preference domain _specifically_.\n'
                   ' - \'com.apple.MCX=com.apple.cachedaccounts.CreateAtLogin,com.apple.cachedaccounts.WarnOnCreate\'\n'
                   '   will keep the two values for the \'com.apple.MCX\' preference domain.\n'
                   'Please note that filtering values is only done if the preference domain is also specified\n\n'
                   'In the example dictionary below:\n'
                   ' - \'com.apple.MCX\' is referred to as the \'preference domain\'.\n'
                   ' - \'com.apple.cachedaccounts.CreateAtLogin\' is referred to as the \'preference domain value\'.\n'
                   '   This domain value should be taken from the \'mcx_preference_settings\' dictionary.\n\n')

ds_obj_mcx_dict_example = {'com.apple.MCX': {'Forced': [{'mcx_preference_settings': {'com.apple.cachedaccounts.CreateAtLogin': True,
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


ds_obj_mcx = f'{ds_obj_mcx_note}{pformat(ds_obj_mcx_dict_example)}'
