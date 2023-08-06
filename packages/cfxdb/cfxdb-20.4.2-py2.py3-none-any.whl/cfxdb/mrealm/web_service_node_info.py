##############################################################################
#
#                        Crossbar.io FX
#     Copyright (C) Crossbar.io Technologies GmbH. All rights reserved.
#
##############################################################################

from cfxdb.mrealm.web_service import WebService


class WebServiceNodeInfo(WebService):
    """
    Web service: type "nodeinfo".

    * check_web_path_service_nodeinfo
    """
    def __init__(self, *args, **kwargs):
        WebService.__init__(self, *args, **kwargs)
        self.service_type = 'nodeinfo'

    @staticmethod
    def parse(data):
        obj = WebService.parse(data)
        return obj
