# Credentials Safe

<i>Store application credentials in keyring with RSA.</i>

# Hierarchy

```
credsafe
'---- Agent()
    |---- set()
    '---- get()
```

# Example

## python
```python
from credsafe import *

# initialize an agent
kp = {  # check easyrsa for more info
    "private_key": ...,
    "public_key": ...
}
import os
key = os.urandom(64)
credsafe_agent = Agent(app_name="my app", key_pair=kp, hmac_key=key)

# set something for a user
credsafe_agent.set(id="username", pw="password", k="phone", v=123456789)
credsafe_agent.set(id="username", pw="password", k="config", v={"something": "secret"})

# get something for a user
print(credsafe_agent.get(id="username", pw="password", k="phone"))
# 123456789
print(credsafe_agent.get(id="username", pw="password", k="config"))
# {"something": "secret"}
```

## shell
```shell script

```