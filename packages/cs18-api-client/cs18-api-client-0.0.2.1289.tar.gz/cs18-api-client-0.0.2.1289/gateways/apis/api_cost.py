from datetime import datetime

from gateways.apis.api_base_class import ApiBase


class ApiCost(ApiBase):
    def breakdown(self, space_name: str, frm: datetime, until: datetime, criteria: str = 'blueprint'):
        return self.build_route(
            "spaces/{space_name}/cost/breakdown?criteria={criteria}&from={frm}&to={until}".format(**locals()))

    def usage(self, space_name: str, date: datetime):
        return self.build_route("spaces/{space_name}/cost/usage?date={date}".format(**locals()))
