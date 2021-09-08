"""Configuration Profile"""
from datetime import datetime
from uuid import uuid4

from . import plist


class Profile:
    """Class to create Configuration Profile"""
    def __init__(self, identifier: str = 'meecxprofile', organization: str = 'com.github.carlashley',
                 display_name: str = 'meecxprofile', removal_allowed: bool = False,
                 description: str = 'MCX Custom Settings for:\n', payload_version: int = 1,
                 payload_type: str = 'Configuration', payload_scope: str = 'System'):
        # Private
        self._payload_version = payload_version
        self._identifier = identifier
        self._organization = organization
        self._display_name = display_name
        self._removal_allowed = removal_allowed
        self._description = description
        self._payload_type = payload_type
        self._payload_scope = payload_scope
        self._profile_uuid = self._make_uuid()

        # Public
        self.data = {'PayloadVersion': self._payload_version,
                     'PayloadOrganization': self._organization,
                     'PayloadRemovalDisallowed': self._removal_allowed,
                     'PayloadUUID': self._profile_uuid,
                     'PayloadType': self._payload_type,
                     'PayloadScope': self._payload_scope,
                     'PayloadDescription': self._description,
                     'PayloadDisplayName': self._display_name,
                     'PayloadIdentifier': self._identifier,
                     'PayloadContent': list()}  # Sub payloads that are provided later

    def _make_uuid(self):
        """UUID generator"""
        return str(uuid4()).upper()

    def _add_payload(self, payload: dict):
        """Add payload to the profile within the PayloadContent list

        :param payload (dict): payload to contain within the profile PayloadContent value"""
        _uuid = self._make_uuid()
        domains = [f'  - {key}' for key, _ in payload.items()]

        if self._description.startswith('MCX Custom Settings for:\n'):
            self.data['PayloadDescription'] += '\n'.join(domains)

        _payload = dict()
        _payload['PayloadVersion'] = 1
        _payload['PayloadUUID'] = _uuid
        _payload['PayloadEnabled'] = True
        _payload['PayloadType'] = 'com.apple.ManagedClient.preferences'
        _payload['PayloadIdentifier'] = f'{self._identifier}.{self._profile_uuid}.alacarte.customsettings.{_uuid}'
        _payload['PayloadContent'] = payload

        self.data['PayloadContent'].append(_payload)

    def add_payload_from_plist(self, payload: dict, domain: str, manage: str, by_host: bool = False, keys: set = set()):
        """Add plist dict contents"""
        valid_manage = ['Always', 'Once']

        if manage not in valid_manage:
            raise ValueError(f'Valid values are {valid_manage}')

        state = 'Forced' if manage == 'Always' else 'Set-Once'
        domain = f'{domain}.ByHost' if by_host else domain

        # Remove keys that aren't required
        if keys:
            for key, value in payload.copy().items():
                if key not in keys:
                    del payload[key]

        _payload = dict()
        _payload[domain] = dict()
        _payload[domain][state] = list()
        _payload[domain][state].append(dict())
        _payload[domain][state][0]['mcx_preference_settings'] = payload

        # Datestamp required if using 'Once' for 'managed'
        if manage == 'Once':
            _payload[domain][state][0]['mcx_data_timestamp'] = datetime.utcnow()

        self._add_payload(payload=_payload)

    def add_payload_from_mcx(self, payload: dict):
        """Add MCX data"""
        self._add_payload(payload=payload)

    def write(self, f: str):
        """Write payload"""
        plist.write(self.payload, f)
