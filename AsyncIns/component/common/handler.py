from tornado.web import RequestHandler


class RestfulHandler(RequestHandler):

    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', '*')
        self.set_header('Access-Control-Max-Age', 1000)
        self.set_header('Content-type', 'application/json')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, DELETE, PUT, PATCH, OPTIONS')
        self.set_header('Access-Control-Allow-Headers',
                        'Content-Type, Access-Control-Allow-Origin,'
                        'Access-Control-Allow-Headers, X-Requested-By, Access-Control-Allow-Methods')

    def interrupt(self, status_code: int=200, reason='Response was forced to interrupt'):
        resp = dict(message=reason)
        if isinstance(resp, dict):
            self.set_status(status_code)
            self.write(resp)

    def over(self, status_code: int=200, data: dict={'message': 'Response was finish'}):
        self.set_status(status_code)
        self.write(data)
        self.finish()
