from functools import wraps

import flask
import json


def role_required(user_session: dict):
    def role_wrapper(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            accesses = json.load(open('configs/access.json'))

            role = user_session.get('role')
            endpoint = flask.request.endpoint

            if endpoint.split('.')[-1] in accesses[role]:
                return func(*args, **kwargs)

            return flask.redirect(f"/?error=Command denied")
        return wrapper
    return role_wrapper
