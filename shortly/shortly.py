# coding:utf-8
# /bin/bash/python2
import os
import redis
import urlparse
from werkzeug.wrappers import Request,Response
from werkzeug.routing import Map,Rule
from werkzeug.exceptions import HTTPException,NotFound
from werkzeug.middleware.shared_data import SharedDataMiddleware
from werkzeug.utils import redirect
from jinja2 import Environment,FileSystemLoader


class Shortly(object):
    def __init__(self, config):
        self.redis = redis.Redis(config['redis_host'], config['redis_port'])
        template_path = os.path.join(os.path.dirname(__file__), 'templates')
        self.jinja_env = Environment(loader=FileSystemLoader(template_path),autoescape=True)
        self.url_map = Map([
            Rule('/', endpoint='new_url'),
            Rule('/<short_id>', endpoint='follow_short_link'),
            Rule('/<short_id>+', endpoint='short_link_details')
            ])

    def render_template(self, tempate_name, **context):
        t = self.jinja_env.get_template(template_name)
        return Response(t.render(context),mimetype='text/html')

    def dispatch_request(self, request):
        adapter = self.url_map.bind_to_environ(request.environ)
        try:
            endpoint,values = adapter.match()
            return getattr(self, 'on_' + endpoint)(request, **values)
        except HTTPException,e:
            return e

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        endpoint = 'follow_short_link'
        values = {'short_id':u'foo'}
        return self.wsgi_app(environ,start_response)

def create_app(redis_host="localhost", redis_port=6379, with_static=True):
    app = Shortly({
            "redis_host":       redis_host,
            "redis_port":       redis_port
            })
    if with_static:
        app.wsgi_app = SharedDataMiddleware(app.wsgi_app,{
            '/static': os.path.join(os.path.dirname(__file__),'static')
            })
        return app

if __name__ == '__main__':
    from werkzeug.serving import run_simple
    app = create_app()
    run_simple('0.0.0.0',5000,app,use_debugger=True,use_reloader=True)


