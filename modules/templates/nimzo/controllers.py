# -*- coding: utf-8 -*-

from gluon import *
from s3 import S3CustomController

TEMPLATE = "nimzo"


class index(S3CustomController):
    """ Custom Home Page """

    def __call__(self):
        self._view(TEMPLATE, "index.html")

        return dict(
            title=current.T(
                "Sahana Eden Humanitarian Management Platform"),
            login_form=current.auth.login(),
            is_index=True)
