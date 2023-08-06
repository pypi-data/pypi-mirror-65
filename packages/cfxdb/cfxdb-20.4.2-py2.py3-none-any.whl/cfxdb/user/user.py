##############################################################################
#
#                        Crossbar.io FX
#     Copyright (C) Crossbar.io Technologies GmbH. All rights reserved.
#
##############################################################################

from datetime import datetime
from pprint import pformat

import six

from cfxdb.common import ConfigurationElement


class User(ConfigurationElement):
    """
    CFC user database class using CBOR.
    """

    # oid: uuid.UUID

    # label: Optional[str]
    # description: Optional[str]
    # tags: Optional[List[str]]

    # email: str
    # registered: datetime
    # pubkey: six.text_type

    def __init__(self,
                 oid=None,
                 label=None,
                 description=None,
                 tags=None,
                 email=None,
                 registered=None,
                 pubkey=None,
                 _unknown=None):
        """

        :param oid: Object ID of the user
        :type oid: uuid.UUID

        :param label: Optional user label of the user
        :type label: str

        :param description: Optional user description of the user
        :type description: str

        :param tags: Optional list of user tags on the user
        :type tags: list[str]

        :param email: User email
        :type email: str

        :param registered: Timestamp when the user registered
        :type registered: datetime.datetime

        :param pubkey: Public key of user (HEX encoded Ed25519 32 byte public key).
        :type pubkey: str

        :param _unknown: Any unparsed/unprocessed data attributes
        :type _unknown: None or dict
        """

        ConfigurationElement.__init__(self, oid=oid, label=label, description=description, tags=tags)

        self.email = email
        self.registered = registered
        self.pubkey = pubkey

        # private member with unknown/untouched data passing through
        self._unknown = _unknown

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        if not ConfigurationElement.__eq__(self, other):
            return False

        if other.email != self.email:
            return False
        if other.registered != self.registered:
            return False
        if other.pubkey != self.pubkey:
            return False

        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return '\n{}\n'.format(pformat(self.marshal()))

    def copy(self, other):
        self.oid = other.oid
        self.label = other.label
        self.description = other.description
        self.tags = other.tags
        self.email = other.email
        self.registered = other.registered
        self.pubkey = other.pubkey

        # _unknown is not copied!

    def marshal(self):
        obj = ConfigurationElement.marshal(self)

        assert self.email is None or type(self.email) == six.text_type
        assert self.registered is None or isinstance(self.registered, datetime)
        assert self.pubkey is None or (type(self.pubkey) == six.text_type and len(self.pubkey) == 64)

        registered = int(self.registered.timestamp() * 1000000) if self.registered else None
        obj.update({
            'email': self.email,
            'registered': registered,
            'pubkey': self.pubkey,
        })

        if self._unknown:
            # pass through all attributes unknown
            obj.update(self._unknown)

        return obj

    @staticmethod
    def parse(data):
        assert type(data) == dict

        obj = ConfigurationElement.parse(data)
        data = obj._unknown

        # future attributes (yet unknown) are not only ignored, but passed through!
        _unknown = {}
        for k in data:
            if k not in ['email', 'registered', 'pubkey']:
                val = data.pop(k)
                _unknown[k] = val

        email = data.get('email', None)
        assert email is None or type(email) == six.text_type

        registered = data.get('registered', None)
        assert registered is None or type(registered) == float or type(registered) in six.integer_types
        if registered:
            # registered = datetime.utcfromtimestamp(float(registered) / 1000000.)
            registered = datetime.fromtimestamp(float(registered) / 1000000.)

        # hex string with 256 bit Ed25519 WAMP-cryptosign public key
        pubkey = data.get('pubkey', None)
        assert pubkey is None or (type(pubkey) == six.text_type and len(pubkey) == 64)

        obj = User(oid=obj.oid,
                   label=obj.label,
                   description=obj.description,
                   tags=obj.tags,
                   email=email,
                   registered=registered,
                   pubkey=pubkey,
                   _unknown=_unknown)
        return obj
