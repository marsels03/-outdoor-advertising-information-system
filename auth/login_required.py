from functools import wraps

import flask


def login_required(user_session: dict):
    def login_wrapper(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if user_session.get('is_auth'):
                return func(*args, **kwargs)

            return flask.redirect(f"/?error=You are not logged in")
        return wrapper
    return login_wrapper
