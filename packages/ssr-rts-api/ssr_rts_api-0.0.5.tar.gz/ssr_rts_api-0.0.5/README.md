# ssr_rts_api

Connect with ease to the rts/ssr channel public API.  
The package is only for accessing the "RTS Archives v3" (broadcast) endpoint

Enjoy exploring RTS (radio télévision suisse romande) channel broadcast open data 📺 !

# Get it
```
$ pip install ssr_rts_api
```

# How it works

Connect to the RTS archives public api can be a little bit confusing. ssr_rts_api is aimed to resolve that issue.

Go to : https://developer.srgssr.ch/apis/rts-archives-v3  
Create your app  
Get your consumer key and secret
  
**Remember, the package is only for accessing the "RTS Archives v3" (broadcast) API**
    
```python
from ssr_rts_api import Client as Cl
```

Pass an object with your credentials for generating a token and
instantiate a client access to the API  
- username = consumer key
- password = consumer secret

```python
obj = {"username": "your_consumer_key",
       "password": "yout_consumer_secret"}

cl = Cl.Client(obj)
```
Get your token trough the Client.token parameter
```python
print(cl.token)
```
Pass an object with the desired request inside the Client.request() method
```python
querystring = {
    "query": "'id'='103'",
    "rows": 0,
    "start": 25, # be careful, RTS api returns no more than 25 documents per request
    "minPublicationDate": 1960,
    "maxPublicationDate": 2020,
    "sort": "publicationDate"
}

results = cl.request(querystring)
data = results.json()
```

Results can be a little bit "too" generous.
Refine the results with the Client.filter() method
```python
filtered = cl.filter_data(data, ['program', 'id'], 103)  # program id : 103 = Temps Présent
```
Use the to_pop argument to pop out fields of the data set.

```python
filtered = cl.filter_data(data, ['isOnline'], 'true', 'sequences')  # pop "sequence" field
```

Save the result with the Client.save() method.
Pass a data array and a mongodb collection in parameters
```python
res = cl.save_data(data, collection)
```
# Last note

Be kind, don't over request the server : use time.sleep()
```python
import time

time.sleep(3) #zzZZZ
```
# Credit

Renato Diaz (rerouj)
renatojour@gmail.com