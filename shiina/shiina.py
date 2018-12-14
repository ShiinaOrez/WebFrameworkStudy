import os
import json
import redis
import tools

from werkzeug.utils import cached_property, environ_property, \
     header_property, get_content_type, validate_arguments, ArgumentValidationError
from werkzeug.datastructures import MultiDict, CombinedMultiDict
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException, NotFound, MethodNotAllowed, BadRequest, HTTPException

from functools import wraps, update_wrapper
from wrappers import Request, Response


class Shiina:

    """
    Shiina is:
        A simple python web framework powered by ShiinaOrez.

    Base on werkzeug 0.9
    Version 0.1.0

        You can use it to make a small API(Application programming interface)
        Like this:

    from shiina import Shiina
    app = Shiina()

    @app.viewfunction('/')
    @method('GET', 'POST')
    def origin(request):
        return json.dumps({"msg": 'successful!'})

    Just for study WSGI, werkzeug...
    """

    config = {}
    url2endpoint = {}
    endpoint2func = {}
    func2methods = {}

    """
    viewfunction is a decorator to make a view function

    @app.viewfunction('/example')
    def func():
        pass

    arguments:
        url: view function to dispatch
    """
    def viewfunction(self, url):
        def deco(func):
            endpoint = func.__name__
            if url not in self.url2endpoint.keys():
                self.url2endpoint[url] = endpoint
            else:
                pass
            self.endpoint2func[endpoint] = func
            return func
        return deco

    """
    method is a decorator for rule the request method

    @method('GET', 'POST')
    def func():
        pass

    """
    def method(self, *args, **kwargs):
        arglist = list(args)
        def deco(func):
            self.func2methods[func.__name__] = arglist
            return func
        return deco

    """
    dispatch is a function to dispatch url to the view_functions

    arguments:
    request: BaseRequest object, initial by WSGI environment.

    """
    def dispatch_request(self, request):
        _environ = request.environ
        try:
            endpoint = self.url2endpoint[_environ['PATH_INFO']]
            if _environ['REQUEST_METHOD'] not in self.func2methods[self.endpoint2func[endpoint].__name__]:
                raise MethodNotAllowed()
            _data = request.values.to_dict()
            try:
                args, kwargs = validate_arguments(self.endpoint2func[endpoint],
                                                  (request, ),
                                                  _data)
            except ArgumentValidationError:
                raise BaseRequest("Raise by Dispatch")
            return _data_and_status(self.endpoint2func[endpoint](request, *args, **kwargs))
        except HTTPException as _e:
            return _e

    """
    wsgi_app is a WSGI application

    arguments:
    environ: WSGI environ object, it is a dictionary
    start_response: func to start a response, when you call the response object, is it the argument

    """
    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        data_and_status = self.dispatch_request(request)
        response = data_and_status[0]
        status = data_and_status[1]
        if data_and_status[1] == '' or not tools.check_status(status):
            status = "200 OK"
        if not isinstance(response, HTTPException):
            response = Response(response, mimetype = 'application/json', status = "200 OK")
        else:
            response = response.get_response(environ)
        return response(environ, start_response)

    """
    run is the very simple function to start service
    """
    def run(self):
        from werkzeug.serving import run_simple
        run_simple('127.0.0.1', 5000, self, use_debugger = True, use_reloader = True)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)

def create_app():
    app = Shiina()
    return app

def _data_and_status(data_and_status, default_status = "200 OK"):
    if not isinstance(data_and_status, tuple):
        data_and_status = (data_and_status, default_status)
    return data_and_status
