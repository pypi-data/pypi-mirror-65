##############################################################################
#
#                        Crossbar.io FX
#     Copyright (C) Crossbar.io Technologies GmbH. All rights reserved.
#
##############################################################################

from typing import Dict

from cfxdb.mrealm.web_service import WebService
from cfxdb.mrealm.web_service_json import WebServiceJson
from cfxdb.mrealm.web_service_static import WebServiceStatic
from cfxdb.mrealm.web_service_node_info import WebServiceNodeInfo

_WEBSERVICE_TYPE_KLASSMAP = {}  # type: Dict[str, object]
_WEBSERVICE_TYPE_KLASSMAP['nodeinfo'] = WebServiceNodeInfo
_WEBSERVICE_TYPE_KLASSMAP['static'] = WebServiceStatic
_WEBSERVICE_TYPE_KLASSMAP['json'] = WebServiceJson


def _parse_webservice(webservice):
    """

    :param webservice:
    :return:
    """
    assert type(webservice) == dict
    assert 'type' in webservice

    if webservice['type'] not in _WEBSERVICE_TYPE_KLASSMAP:
        raise Exception('no webservice of type "{}"'.format(webservice['type']))

    klass = _WEBSERVICE_TYPE_KLASSMAP[webservice['type']]

    return klass.parse(webservice)


def parse_webservice(webservice):
    """

    :param webservice:
    :return:
    """
    assert type(webservice) == dict
    assert 'type' in webservice

    return WebService.parse(webservice)
