from tornado.web import RequestHandler

from tornado.httpclient import HTTPError
from model import Verify
from .forms import VerifyForm


class VerifyHandler(RequestHandler):
    async def post(self, *args, **kwargs):
        ver = VerifyForm(self.request.arguments)
        email = ver.email.data

