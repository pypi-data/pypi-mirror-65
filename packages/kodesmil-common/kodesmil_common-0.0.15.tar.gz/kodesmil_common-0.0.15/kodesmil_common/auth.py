
#import requests
import json
import os
from functools import wraps
from flask import request, jsonify, _request_ctx_stack
#from flask_cors import cross_origin
from jose import jwt
from six.moves.urllib.request import urlopen
import firebase_admin
from firebase_admin import auth
firebase_app = firebase_admin.initialize_app()

# Format error response and append status code.
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_token_auth_header():
    """
    Obtains the access token from the Authorization Header
    """
    auth = request.headers.get("Authorization", None)
    if not auth:
        raise AuthError({
            "code": "authorization_header_missing",
            "description": "Authorization header is expected",
        }, 401)

    parts = auth.split()

    if parts[0].lower() != "bearer":
        raise AuthError({
            "code": "invalid_header",
            "description": "Authorization header must start with Bearer",
        }, 401)
    elif len(parts) == 1:
        raise AuthError({
            "code": "invalid_header",
            "description": "Token not found",
        }, 401)
    elif len(parts) > 2:
        raise AuthError({
            "code": "invalid_header",
            "description": "Authorization header must be Bearer token",
        }, 401)

    token = parts[1]
    return token


def requires_auth(f):
    """
    Determines if the access token is valid
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        id_token = get_token_auth_header()
        decoded_token = auth.verify_id_token(id_token)
        if 'uid' in decoded_token:
            uid = decoded_token['uid'] 
            kwargs['user_id'] = uid
            return f(*args, **kwargs)
        else:
            raise AuthError({
                "code": "no_access",
                "description": "User not found",
            }, 401)

    return decorated
