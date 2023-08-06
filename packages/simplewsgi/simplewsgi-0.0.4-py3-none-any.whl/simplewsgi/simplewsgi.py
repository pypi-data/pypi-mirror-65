from simplewsgi.router import Router

class SimpleWsgi:
    def __init__(self):
        self.router = Router()

    def route(self, path=None, method='GET', callback=None):
        def decorator(callback_func):
            self.router.add(method, path, callback_func)
            return callback_func
        return decorator(callback) if callback else decorator

    def __call__(self, env, start_response):
        method = env['REQUEST_METHOD'].upper()
        path = env['PATH_INFO'] or '/'
        callback, kwargs = self.router.match(method, path)
        start_response('200 OK', [('Content-type', 'text/plain; charset=utf-8')])
        return callback(env, start_response, **kwargs)