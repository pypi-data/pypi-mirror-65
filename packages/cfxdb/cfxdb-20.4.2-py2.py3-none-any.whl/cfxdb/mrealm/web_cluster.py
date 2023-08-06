##############################################################################
#
#                        Crossbar.io FX
#     Copyright (C) Crossbar.io Technologies GmbH. All rights reserved.
#
##############################################################################

import pprint

from cfxdb.common import ConfigurationElement


class WebCluster(ConfigurationElement):
    """
    CFC Web Cluster database configuration object.
    """

    STATUS_BY_CODE = {
        0: 'NONE',
        1: 'STOPPED',
        2: 'STARTING',
        3: 'RUNNING',
        4: 'PAUSED',
        5: 'STOPPING',
    }

    STATUS_BY_NAME = {
        'NONE': 0,
        'STOPPED': 1,
        'STARTING': 2,
        'RUNNING': 3,
        'PAUSED': 4,
        'STOPPING': 5,
    }

    STATUS_STOPPED = 1
    STATUS_STARTING = 2
    STATUS_RUNNING = 3
    STATUS_PAUSED = 4
    STATUS_STOPPING = 5

    def __init__(self,
                 oid=None,
                 label=None,
                 description=None,
                 tags=None,
                 name=None,
                 status=None,
                 changed=None,
                 tcp_version=None,
                 tcp_port=None,
                 tcp_shared=None,
                 tcp_interface=None,
                 tcp_backlog=None,
                 tls_key=None,
                 tls_certificate=None,
                 tls_chain_certificates=None,
                 tls_ca_certificates=None,
                 tls_dhparam=None,
                 tls_ciphers=None,
                 http_client_timeout=None,
                 http_hsts=None,
                 http_hsts_max_age=None,
                 http_access_log=None,
                 http_display_tracebacks=None,
                 _unknown=None):
        """

        :param oid: Object ID of node
        :type oid: uuid.UUID

        :param label: Optional user label of node
        :type label: str

        :param description: Optional user description of node
        :type description: str

        :param tags: Optional list of user tags on node
        :type tags: list[str]

        :param tcp_version: IP version, either 4 for 6
        :type tcp_version: int

        :param tcp_port: IP listening port
        :type tcp_port: int

        :param tcp_shared: enable TCP port sharing
        :type tcp_shared: bool

        :param tcp_interface: listen on this interface
        :type tcp_interface: str

        :param tcp_backlog: TCP accept backlog queue size
        :type tcp_backlog: int

        :param tls_key: TLS server private key to use
        :type tls_key: str

        :param tls_certificate: TLS server certificate to use
        :type tls_certificate: str

        :param tls_chain_certificates: TLS certificate chain
        :type tls_chain_certificates: list[str]

        :param tls_ca_certificates: CA certificates to use
        :type tls_ca_certificates: list[str]

        :param tls_dhparam: DH parameter file
        :type tls_dhparam: str

        :param tls_ciphers: Ciphers list
        :type tls_ciphers: str

        :param http_client_timeout: HTTP client inactivity timeout
        :type http_client_timeout: int

        :param http_hsts: enable HTTP strict transport security (HSTS)
        :type http_hsts: bool

        :param http_hsts_max_age: HSTS maximum age to announce
        :type http_hsts_max_age: int

        :param http_access_log: enable Web request access logging
        :type http_access_log: bool

        :param http_display_tracebacks: enable tracebacks when running into Web errors
        :type http_display_tracebacks: bool

        :param _unknown: Any unparsed/unprocessed data attributes
        :type _unknown: None or dict
        """
        ConfigurationElement.__init__(self, oid=oid, label=label, description=description, tags=tags)
        self.name = name
        self.status = status
        self.changed = changed
        self.tcp_version = tcp_version
        self.tcp_port = tcp_port
        self.tcp_shared = tcp_shared
        self.tcp_interface = tcp_interface
        self.tcp_backlog = tcp_backlog
        self.tls_key = tls_key
        self.tls_certificate = tls_certificate
        self.tls_chain_certificates = tls_chain_certificates
        self.tls_ca_certificates = tls_ca_certificates
        self.tls_dhparam = tls_dhparam
        self.tls_ciphers = tls_ciphers
        self.http_client_timeout = http_client_timeout
        self.http_hsts = http_hsts
        self.http_hsts_max_age = http_hsts_max_age
        self.http_access_log = http_access_log
        self.http_display_tracebacks = http_display_tracebacks

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if not ConfigurationElement.__eq__(self, other):
            return False
        if other.name != self.name:
            return False
        if other.status != self.status:
            return False
        if other.changed != self.changed:
            return False
        if other.tcp_version != self.tcp_version:
            return False
        if other.tcp_port != self.tcp_port:
            return False
        if other.tcp_shared != self.tcp_shared:
            return False
        if other.tcp_interface != self.tcp_interface:
            return False
        if other.tcp_backlog != self.tcp_backlog:
            return False
        if other.tls_key != self.tls_key:
            return False
        if other.tls_certificate != self.tls_certificate:
            return False
        if other.tls_chain_certificates != self.tls_chain_certificates:
            return False
        if other.tls_ca_certificates != self.tls_ca_certificates:
            return False
        if other.tls_dhparam != self.tls_dhparam:
            return False
        if other.tls_ciphers != self.tls_ciphers:
            return False
        if other.http_client_timeout != self.http_client_timeout:
            return False
        if other.http_hsts != self.http_hsts:
            return False
        if other.http_hsts_max_age != self.http_hsts_max_age:
            return False
        if other.http_access_log != self.http_access_log:
            return False
        if other.http_display_tracebacks != self.http_display_tracebacks:
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
        assert self.name is None or type(self.name) == str
        assert self.status is None or type(self.status) == int
        assert self.changed is None or type(self.changed) == int
        assert self.tcp_version is None or type(self.tcp_version) == int
        assert self.tcp_port is None or type(self.tcp_port) == int
        assert self.tcp_shared is None or type(self.tcp_shared) == bool
        assert self.tcp_interface is None or type(self.tcp_interface) == str
        assert self.tcp_backlog is None or type(self.tcp_backlog) == int
        assert self.tls_key is None or type(self.tls_key) == str
        assert self.tls_certificate is None or type(self.tls_certificate) == str
        assert self.tls_chain_certificates is None or type(self.tls_chain_certificates) == list
        assert self.tls_ca_certificates is None or type(self.tls_ca_certificates) == list
        assert self.tls_dhparam is None or type(self.tls_dhparam) == str
        assert self.tls_ciphers is None or type(self.tls_ciphers) == str
        assert self.http_client_timeout is None or type(self.http_client_timeout) == int
        assert self.http_hsts is None or type(self.http_hsts) == bool
        assert self.http_hsts_max_age is None or type(self.http_hsts_max_age) == int
        assert self.http_access_log is None or type(self.http_access_log) == bool
        assert self.http_display_tracebacks is None or type(self.http_display_tracebacks) == bool

        obj = ConfigurationElement.marshal(self)

        obj.update({
            u'name': self.name,
            u'status': WebCluster.STATUS_BY_CODE[self.status],
            u'changed': self.changed,
            u'tcp_version': self.tcp_version,
            u'tcp_port': self.tcp_port,
            u'tcp_shared': self.tcp_shared,
            u'tcp_interface': self.tcp_interface,
            u'tcp_backlog': self.tcp_backlog,
            u'tls_key': self.tls_key,
            u'tls_certificate': self.tls_certificate,
            u'tls_chain_certificates': self.tls_chain_certificates,
            u'tls_ca_certificates': self.tls_ca_certificates,
            u'tls_dhparam': self.tls_dhparam,
            u'tls_ciphers': self.tls_ciphers,
            u'http_client_timeout': self.http_client_timeout,
            u'http_hsts': self.http_hsts,
            u'http_hsts_max_age': self.http_hsts_max_age,
            u'http_access_log': self.http_access_log,
            u'http_display_tracebacks': self.http_display_tracebacks,
        })

        return obj

    @staticmethod
    def parse(data):
        """
        Parse generic host language object into an object of this class.

        :param data: Generic host language object
        :type data: dict

        :return: instance of :class:`ManagementRealm`
        """
        assert type(data) == dict

        obj = ConfigurationElement.parse(data)
        data = obj._unknown

        # future attributes (yet unknown) are not only ignored, but passed through!
        _unknown = {}
        for k in data:
            if k not in [
                    'name', 'status', 'changed', 'tcp_version', 'tcp_port', 'tcp_shared', 'tcp_interface',
                    'tcp_backlog', 'tls_key', 'tls_certificate', 'tls_chain_certificates',
                    'tls_ca_certificates', 'tls_dhparam', 'tls_ciphers', 'http_client_timeout', 'http_hsts',
                    'http_hsts_max_age', 'http_access_log', 'http_display_tracebacks'
            ]:
                _unknown[k] = data[k]

        name = data.get('name', None)
        assert name is None or (type(name) == str)

        status = data.get('status', None)
        assert status is None or (type(status) == str)
        status = WebCluster.STATUS_BY_NAME.get(status, None)

        changed = data.get('changed', None)
        assert changed is None or (type(changed) == int)

        tcp_version = data.get('tcp_version', None)
        assert tcp_version is None or (type(tcp_version) == int)

        tcp_port = data.get('tcp_port', None)
        assert tcp_port is None or (type(tcp_port) == int)

        tcp_shared = data.get('tcp_shared', None)
        assert tcp_shared is None or (type(tcp_shared) == bool)

        tcp_interface = data.get('tcp_interface', None)
        assert tcp_interface is None or (type(tcp_interface) == str)

        tcp_backlog = data.get('tcp_backlog', None)
        assert tcp_backlog is None or (type(tcp_backlog) == int)

        tls_key = data.get('tls_key', None)
        assert tls_key is None or (type(tls_key) == str)

        tls_certificate = data.get('tls_certificate', None)
        assert tls_certificate is None or (type(tls_certificate) == str)

        tls_chain_certificates = data.get('tls_chain_certificates', None)
        assert tls_chain_certificates is None or (type(tls_chain_certificates) == list)

        tls_ca_certificates = data.get('tls_ca_certificates', None)
        assert tls_ca_certificates is None or (type(tls_ca_certificates) == list)

        tls_dhparam = data.get('tls_dhparam', None)
        assert tls_dhparam is None or (type(tls_dhparam) == str)

        tls_ciphers = data.get('tls_ciphers', None)
        assert tls_ciphers is None or (type(tls_ciphers) == str)

        http_client_timeout = data.get('http_client_timeout', None)
        assert http_client_timeout is None or (type(http_client_timeout) == int)

        http_hsts = data.get('http_hsts', None)
        assert http_hsts is None or (type(http_hsts) == bool)

        http_hsts_max_age = data.get('http_hsts_max_age', None)
        assert http_hsts_max_age is None or (type(http_hsts_max_age) == int)

        http_access_log = data.get('http_access_log', None)
        assert http_access_log is None or (type(http_access_log) == bool)

        http_display_tracebacks = data.get('http_display_tracebacks', None)
        assert http_display_tracebacks is None or (type(http_display_tracebacks) == bool)

        obj = WebCluster(oid=obj.oid,
                         label=obj.label,
                         description=obj.description,
                         tags=obj.tags,
                         name=name,
                         status=status,
                         changed=changed,
                         tcp_version=tcp_version,
                         tcp_port=tcp_port,
                         tcp_shared=tcp_shared,
                         tcp_interface=tcp_interface,
                         tcp_backlog=tcp_backlog,
                         tls_key=tls_key,
                         tls_certificate=tls_certificate,
                         tls_chain_certificates=tls_chain_certificates,
                         tls_ca_certificates=tls_ca_certificates,
                         tls_dhparam=tls_dhparam,
                         tls_ciphers=tls_ciphers,
                         http_client_timeout=http_client_timeout,
                         http_hsts=http_hsts,
                         http_hsts_max_age=http_hsts_max_age,
                         http_access_log=http_access_log,
                         http_display_tracebacks=http_display_tracebacks,
                         _unknown=_unknown)

        return obj
