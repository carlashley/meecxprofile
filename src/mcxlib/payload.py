"""Configuration Profile"""
import plistlib

from datetime import datetime
from uuid import uuid4


class Payload:
    """Class to create Configuration Profile"""
    def __init__(self, identifier: str, organization: str, display_name: str,
                 removal_allowed=False, description='MCX Custom Settings for:\n'):
        # Private
        self._identifier = identifier
        self._organization = organization
        self._display_name = display_name
        self._removal_allowed = removal_allowed
        self._description = description
        self._profile_uuid = self.make_uuid()

        # Public
        self.data = {'PayloadVersion': 1,
                     'PayloadOrganization': self._organization,
                     'PayloadRemovalDisallowed': self._removal_allowed,
                     'PayloadUUID': self._profile_uuid,
                     'PayloadType': 'Configuration',
                     'PayloadScope': 'System',
                     'PayloadDescription': self._description,
                     'PayloadDisplayName': self._display_name,
                     'PayloadIdentifier': self._identifier,
                     'PayloadContent': list()}  # Sub payloads that are provided later

    def make_uuid(self):
        return str(uuid4())

    def add_payload(self, payload: dict):
        """Add payload to the profile within the PayloadContent list

        :param payload (dict): payload to contain within the profile PayloadContent value"""
        _uuid = self.make_uuid()
        domains = [f' - {key}' for key, _ in payload.items()]

        if not self.description:
            self.data['PayloadDescription'] = '\n'.join(domains)

        _payload = dict()
        _payload['PayloadVersion'] = 1
        _payload['PayloadUUID'] = _uuid
        _payload['PayloadEnabled'] = True
        _payload['PayloadType'] = 'com.apple.ManagedClient.preferences'
        _payload['PayloadIdentifier'] = f'MCXToProfile.{self._profile_uuid}.alacarte.customsettings.{_uuid}'
        _payload['PayloadContent'] = payload

        self.data['PayloadContent'].append(_payload)

    def add_payload_from_plist(self, payload: dict, domain: str, manage: str, by_host=False):
        """Add plist dict contents"""
        valid_manage = ['Always', 'Once']

        if manage not in valid_manage:
            raise ValueError(f'Valid values are {valid_manage}')

        state = 'Forced' if manage == 'Always' else 'Set-Once'
        domain = f'{domain}.ByHost' if by_host else domain
        _payload = dict()
        _payload[domain] = dict()
        _payload[domain][state] = list()
        _payload[domain][state].append(dict())
        _payload[domain][state][0]['mcx_preference_settings'] = payload

        # Datestamp required if using 'Once' for 'managed'
        if manage == 'Once':
            _payload[domain][state][0]['mcx_data_timestamp'] = datetime.utcnow()

        self.add_payload(payload=_payload)

    def add_payload_from_mcx(self, payload: dict):
        """Add MCX data"""
        self.add_payload(payload=payload)

    def write(self, f):
        """Write payload"""
        with open(f, 'wb') as _f:
            plistlib.dump(self.data, _f)
