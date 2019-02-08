import re
from wtforms_tornado import Form
from wtforms.fields import *
from wtforms.validators import *


class VerifyForm(Form):
    email = StringField(max_length=100)
