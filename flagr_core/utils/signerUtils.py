#!/usr/bin/env python
"""
fla.gr request model for invite requests
"""
from itsdangerous import URLSafeTimedSerializer, BadSignature
import models.setting.settingModel as sm


secret = sm.getSetting("enableRequests", "requestSecret")
requestSigner = URLSafeTimedSerializer(
        secret,
        salt="requestAnInvite")

def requestToken(email):
    return requestSigner.dumps(email)

def requestDetoken(email):
    try:
        return requestSigner.loads(email)
    except BadSignature:
        raise Exception("Could not verify the token, please make sure it is correct.")
