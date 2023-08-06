# Credentials Safe

<badges>[![version](https://img.shields.io/pypi/v/credsafe.svg)](https://pypi.org/project/credsafe/)
[![license](https://img.shields.io/pypi/l/credsafe.svg)](https://pypi.org/project/credsafe/)
[![pyversions](https://img.shields.io/pypi/pyversions/credsafe.svg)](https://pypi.org/project/credsafe/)  
[![donate](https://img.shields.io/badge/Donate-Paypal-0070ba.svg)](https://paypal.me/foxe6)
[![powered](https://img.shields.io/badge/Powered%20by-UTF8-red.svg)](https://paypal.me/foxe6)
[![made](https://img.shields.io/badge/Made%20with-PyCharm-red.svg)](https://paypal.me/foxe6)
</badges>

<i>Store application credentials in keyring with RSA and AES.</i>

# Hierarchy

```
credsafe
'---- Agent()
    |---- set()
    |---- get()
    '---- rm()
```

# Example

## python
```python
from credsafe import *

# initialize an agent
kp = {  # check easyrsa for more info
    "private_key": b"...",
    "public_key": b"..."
}
import os
# remember these keys otherwise you cannot get credentials
hmac_key = os.urandom(64)
credsafe_agent = Agent(app_name="my app", key_pair=kp)

# set something JSON-serializable for a user
credsafe_agent.set(id="username", pw="password", k="phone", v=123456789)
credsafe_agent.set(id="username", pw="password", k="config", v={"something": "secret"})

# get something for a user
print(credsafe_agent.get(id="username", pw="password", k="phone"))
# 123456789
print(credsafe_agent.get(id="username", pw="password", k="config"))
# {"something": "secret"}

# remove something for a user
credsafe_agent.rm(id="username", pw="password", k="config")
print(credsafe_agent.get(id="username", pw="password", k="config"))
# KeyError

# destroy everything for a user
credsafe_agent.destroy(id="username")
```

## shell
```shell script

```