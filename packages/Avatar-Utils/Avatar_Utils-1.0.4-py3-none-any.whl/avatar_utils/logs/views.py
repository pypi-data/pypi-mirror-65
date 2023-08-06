import traceback

from flask import g, request

from .log import *
from . import logs


@logs.before_app_request
def before_request():
    try:
        log_id = Log.init(request)
        g.log_id = log_id
    except BaseException:
        print("Something went wrong during log initializing. See traceback: " + str(traceback.format_exc()))
        db.session.rollback()


@logs.after_app_request
def after_request(response):
    try:
        if g.log_id is not None:
            Log.complete(g.log_id, response)
        else:
            print('log_id is None, cannot complete logging process')
    except BaseException:
        print("Something went wrong during log completing. See traceback: " + str(traceback.format_exc()))
        db.session.rollback()
    return response
