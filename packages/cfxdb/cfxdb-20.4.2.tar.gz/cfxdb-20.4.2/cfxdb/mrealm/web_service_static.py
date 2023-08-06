##############################################################################
#
#                        Crossbar.io FX
#     Copyright (C) Crossbar.io Technologies GmbH. All rights reserved.
#
##############################################################################

from cfxdb.mrealm.web_service import WebService


class WebServiceStatic(WebService):
    """
    Web service: type "static".
    """

    # directory: Optional[str]
    # enable_directory_listing: Optional[bool]
    # mime_types: Optional[Dict[str, str]]
    # cache_timeout: Optional[int]
    def __init__(self, *args, **kwargs):
        WebService.__init__(self, *args, **kwargs)
        self.service_type = 'static'
        self.directory = '.'

    def marshal(self):
        obj = WebService.marshal(self)
        obj.update({'directory': self.directory})

    @staticmethod
    def parse(data):
        # obj = WebServiceStatic.__init__(WebService.parse(data))
        # obj.directory = data.get('directory', None)
        obj = WebService.parse(data)
        obj.directory = data.get('directory', None)
        return obj
