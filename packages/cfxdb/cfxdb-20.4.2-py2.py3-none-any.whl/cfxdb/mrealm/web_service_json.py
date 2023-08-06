##############################################################################
#
#                        Crossbar.io FX
#     Copyright (C) Crossbar.io Technologies GmbH. All rights reserved.
#
##############################################################################

from cfxdb.mrealm.web_service import WebService


class WebServiceJson(WebService):
    """
    Web service: type "json".
    """

    # value: object
    # prettify: Optional[bool]
    # allow_cross_origin: Optional[bool]
    # discourage_caching: Optional[bool]
    def __init__(self, *args, **kwargs):
        WebService.__init__(self, *args, **kwargs)
        self.service_type = 'json'
        self.value = 23

    def marshal(self):
        obj = WebService.marshal(self)
        obj.update({'value': self.value})

    @staticmethod
    def parse(data):
        # obj = WebServiceJson()
        # WebServiceJson.__init__(WebService.parse(data))
        obj = WebService.parse(data)
        obj.value = data.get('value', None)
        return obj
