from werkzeug.utils import cached_property, environ_property, \
     header_property, get_content_type
from werkzeug.datastructures import MultiDict, CombinedMultiDictfrom werkzeug.wrappers import Request as BaseRequest, Response as BaseResponse
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException, NotFound, MethodNotAllowed, BadRequest, HTTPException
from werkzeug.wrappers import Request as BaseRequest, \
                              Response as BaseResponse
import json

class Request(BaseRequest, JSONMixin):
    '''
        self.values is ARGS + FORM + JSON 
    '''
    @cahced_property
    def values(self):
        args = []
        for d in self.args, self.form, self.json:
            if not isinstance(d, MultiDict):
                d = MultiDict(d)
            args.append(d)
        return CombineMultiDict(args)
    pass

class Response(BaseResponse):
    default_status = "200 OK"

    def set_default_status(self, new_status):
        if tools.check_status(new_status):
            self.default_status = new_status
        else:
            raise ValueError


class JSONMixin(object):
    @property
    def json(self):
        return self.get_json()

    def get_json(self):
        data = self._get_data_for_json()
        try:
            rv = json.loads(data)
        except ValueError as e:
            rv = self.on_json_loading_failed(e)
        return rv

    def _get_data_for_json(self):
        return self.get_data()

    def on_json_loading_failed(self, e):
        raise BadRequest("Failed to decode JSON object: {0}".format(e))

