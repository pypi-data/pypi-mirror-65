

import requests
import os

from flask import Flask, request
app = Flask(__name__)
from .dicplus import DicPlus
from .store import Store

SECRETS = DicPlus.from_json('secrets.json').secrets

from .secure import *

mykeyset = KeySet(jsonfile = "keySet.json")

secure = Secure(
    service = "https://notif.pnbx.cc",
    private_key=SECRETS.private_key,
    authenticator = {
        "client_id":SECRETS.auth0.client_id,
        "client_secret":SECRETS.auth0.client_secret,
        "domain":SECRETS.auth0.domain
    },
    keySet = mykeyset
)


@app.route('/test_signer')
def signer():
    url = "https://webhook.site/8dda8c52-84c2-45fa-a8c3-228bfe972b6e"
    body = {
        "test": "123",
        "test2": "3345"
    }
    headers = secure.signed_headers(body, "https://notif.pnbx.cc")
    res = requests.post(url, headers=headers, json=body)
    print(res.status_code)
    return headers


@app.route('/test_signature')
@secure.verify(issuers = ["https://notif.pnbx.cc", "https://penbox.eu.auth0.com/"])
def test_signature():
    print("it worked !!")
    return "Yup worked"


@app.route('/test_authorize')
@secure.authorize("sms:send email:send")
def test_authorize():
    return "Ok"

@app.route('/test_authenticate')
def test_authenticate():
    return secure.auth_headers()

@app.route('/test_store')
def test_store():
    my_store = Store('testing', credentials = "pnbx-rd-ce720f352b00.json", project = "pnbx-rd")
    return str(my_store.key_id)

