from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

from future import standard_library
standard_library.install_aliases()
from builtins import *  # noqa

from talisker.request_id import RequestIdMiddleware
from talisker.context import manager
from talisker.endpoints import StandardEndpointMiddleware


def wrap(app):
    if not getattr(app, '_talisker_wrapped', False):
        wrapped = app
        # added in reverse order
        # expose some standard endpoints
        wrapped = StandardEndpointMiddleware(wrapped)
        # add request id info to thread locals
        wrapped = RequestIdMiddleware(wrapped)
        # clean up thread locals on the way out
        wrapped = manager.make_middleware(wrapped)
        wrapped._talisker_wrapped = True
        wrapped._talisker_original_app = app
        return wrapped
    else:
        return app
