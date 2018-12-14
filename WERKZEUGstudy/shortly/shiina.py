import json
import os
import redis
from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException, NotFound, MethodNotAllowed
from werkzeug.wsgi import SharedDataMiddleware
from werkzeug.utils import redirect
from jinja2 import Environment, FileSystemLoader
from functools import wraps, update_wrapper

class Shiina:
    config = {}
    url2endpoint = {}
    endpoint2func = {}
    func2method = {}

    def viewfunction(self, url):
        def deco(func):
            endpoint = func.__name__
            self.url2endpoint[url] = endpoint
            self.endpoint2func[endpoint] = func
            return func
        return deco

    def method(self, *args, **kwargs):
        l = list(args)
        print (l)
        def deco(func):
            self.func2method[func.__name__] = l
            return func
        return deco

    def dispatch_request(self, request):
        try:
            endpoint = self.url2endpoint[request.environ['PATH_INFO']]
            if request.environ['REQUEST_METHOD'] not in self.func2method[self.endpoint2func[endpoint].__name__]:
                raise MethodNotAllowed()
            return self.endpoint2func[endpoint](request)
        except HTTPException as e:
            return e

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)
        if not isinstance(response, HTTPException):
            response = Response(response, mimetype='application/json')
        else:
#            response = Response(list(str(response)))
            response = response.get_response(environ)
        return response(environ, start_response)

    def run(self):
        from werkzeug.serving import run_simple
        self.redis = redis.Redis(self.config['REDIS_HOST'], self.config['REDIS_PORT'])
        run_simple('127.0.0.1', 5000, self, use_debugger = True, use_reloader = True)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)

def create_app(redis_host = 'localhost', redis_port = 6666, with_static = True):
    app = Shiina()
    app.config['REDIS_HOST'] = redis_host
    app.config['REDIS_PORT'] = redis_port
    if with_static:
        app.wsgi_app = SharedDataMiddleware(
            app.wsgi_app, {
                'static': os.path.join(os.path.dirname(__file__),'static')
            })
    return app



