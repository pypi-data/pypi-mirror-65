##############################################################################
#
#                        Crossbar.io FX
#     Copyright (C) Crossbar.io Technologies GmbH. All rights reserved.
#
##############################################################################

import pprint
import uuid

import six


class WebClusterNodeMembership(object):
    def __init__(self, webcluster_oid=None, node_oid=None, parallel=None, standby=None, _unknown=None):
        self.webcluster_oid = webcluster_oid
        self.node_oid = node_oid
        self.parallel = parallel
        self.standby = standby
        self._unknown = _unknown

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if other.webcluster_oid != self.webcluster_oid:
            return False
        if other.node_oid != self.node_oid:
            return False
        if other.parallel != self.parallel:
            return False
        if other.standby != self.standby:
            return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return '\n{}\n'.format(pprint.pformat(self.marshal()))

    def marshal(self):
        """
        Marshal this object to a generic host language object.

        :return: dict
        """
        obj = {
            'webcluster_oid': str(self.webcluster_oid),
            'node_oid': str(self.node_oid),
            'parallel': self.parallel,
            'standby': self.standby,
        }
        return obj

    @staticmethod
    def parse(data):
        """
        Parse generic host language object into an object of this class.

        :param data: Generic host language object
        :type data: dict

        :return: instance of :class:`WebService`
        """
        assert type(data) == dict

        # future attributes (yet unknown) are not only ignored, but passed through!
        _unknown = {}
        for k in data:
            if k not in ['webcluster_oid', 'node_oid', 'parallel', 'standby']:
                _unknown[k] = data[k]

        webcluster_oid = None
        if 'webcluster_oid' in data:
            assert type(data['webcluster_oid']) == six.text_type
            webcluster_oid = uuid.UUID(data['webcluster_oid'])

        node_oid = None
        if 'node_oid' in data:
            assert type(data['node_oid']) == six.text_type
            node_oid = uuid.UUID(data['node_oid'])

        parallel = None
        if 'parallel' in data and data['parallel']:
            assert type(data['parallel']) == int
            parallel = data['parallel']

        standby = None
        if 'standby' in data and data['standby']:
            assert data['standby'] is None or type(data['standby']) == bool
            standby = data['standby']

        assert webcluster_oid
        assert node_oid

        obj = WebClusterNodeMembership(webcluster_oid=webcluster_oid,
                                       node_oid=node_oid,
                                       parallel=parallel,
                                       standby=standby,
                                       _unknown=_unknown)

        return obj
