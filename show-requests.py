import os
import json
import requests
import time
import urllib3

requests.packages.urllib3.disable_warnings()

api_url_base = 'https://us08-1-vralb.oc.vmware.com/'
host = 'us08-1-vralb.oc.vmware.com'
tenant = "cava"

username = os.environ['CAVAUSER']
password = os.environ['CAVAPWD']

headers = {'Content-Type': 'application/json'}

def extract_values(obj, key):
    """Pull all values of specified key from nested JSON."""
    arr = []
    def extract(obj, arr, key):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr
    results = extract(obj, arr, key)
    return results

def get_token():
    api_url = '{0}/identity/api/tokens'.format(api_url_base)
    data =  {
              "username":username,
              "password":password,
	      "tenant":tenant
            }
    response = requests.post(api_url, headers=headers, data=json.dumps(data), verify=False)
    if response.status_code == 200:
        json_data = json.loads(response.content.decode('utf-8'))
        key = json_data['id']
        return key
    else:
        return None

access_key = get_token()
headers1 = {'Content-Type': 'application/json',
           'Authorization': 'Bearer {0}'.format(access_key)}

url = "https://{0}/catalog-service/api/consumer/requests?limit={1}&$orderby=requestNumber+desc".format(host, 50)
response = requests.get(url, headers=headers1, verify=False)
print (json.dumps(response.json()))
