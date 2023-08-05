# Penbox Python 

**v0.2.5 available**: 

```console
pip install pen-py
```

```python
from penpy import DicPlus, Store
```
## Included:

**DicPlus** : A advanced Ordered Dictionnary using . for referecing. 
* class DicPlus()
* Includes a following functions:
    * format()
    * mapping()
    * overwrite()
    * clean_json()
    * from_json()
    * pprint()
    * search() : using jmespath syntax : http://jmespath.org/

**Dates** : A light version of dates handling:
* absolute_date() : from ISO-like to datetime
* relative_date() : from timedelta-like string to datetime
* str_to_timedelta() : from timedelta-like string to timedelta
* TimeFrame object : from a simple timeframe json (see below), can check if a date is included, get the closest date within timeframe for a given date or the next available date within timeframe
```python

timeframe = TimeFrame{
    "mon:fri": "8:11-14:15",
    "sat": "10:11"
})

print(timeframe.get_closest(datetime.now()))
print(timeframe.get_next(datetime.now()))

```


**Secure** : A full version that helps to manage authentication, authorization, signature and signature verification
```python
# app.py create_app()

SECRETS = DicPlus.from_json('secrets.json').secrets 
# Please ask if you need the secrets.json file, that containts auth0 credentials and a PRIVATE-PUBLIC key set for signature.

from .secure import *

mykeyset = KeySet(jsonfile = "keySet.json")

secure = Secure(
    service = "https://notif.pnbx.cc", # Notify here your service
    private_key=SECRETS.private_key,
    authenticator = {
        "client_id":SECRETS.auth0.client_id,
        "client_secret":SECRETS.auth0.client_secret,
        "domain":SECRETS.auth0.domain
    },
    keySet = mykeyset
)

```

```python
# anywhere in the code:

from app import secure

# create bearer headers : authenticate to service (token is automatically refreshed if required only):
headers = secure.auth_headers()

# create signature headers with signed body included:
headers = secure.signed_headers(body, "https://notif.pnbx.cc")

# verify signature against issuers (MUST BE IN KEYSET):
@app.route('/test_signature')
@secure.verify(issuers = ["https://notif.pnbx.cc", "https://penbox.eu.auth0.com/"])
def test_signature():

# authorize API calls for a specific scope:
@app.route('/test_authorize')
@secure.authorize("sms:send email:send")
def test_authorize():

```

**Store** : A light version of ORM using Google Cloud Datastore:
* class Store()
WARNING : to use the datastore, please make sure you reference your google cloud credentials & project json in the env, or provide the filename and project name in argument:

```python
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "pnbx-rd-xxxxxxxx.json"
# OR
mystore = Store('type', credentials="pnbx-rd-xxxxxxxx.json", project = "myproject")
```

- [ ] Please request the json file of r&d account for testing
    
