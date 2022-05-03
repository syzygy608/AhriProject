import requests

class Auth():
    def __init__(self, app_id, app_key):
        self.app_id = app_id
        self.app_key = app_key

    def get_auth_header(self):
        xdate = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
        hashed = hmac.new(self.app_key.encode('utf8'), (f'x-date: {xdate}').encode('utf8'), sha1)
        signature = base64.b64encode(hashed.digest()).decode()
        authorization = (f'hmac username="{self.app_id}", algorithm="hmac-sha1"' +
                         f', headers="x-date", signature="{signature}"')
        return {
            'Authorization': authorization,
            'x-date': xdate,
            'Accept-Encoding': 'gzip'
        }

app_id = "5a3dc309cf854788a53d775058b194c1"

auth = Auth(app_id, app_key)
url = "https://ptx.transportdata.tw/MOTC/v2/Rail/TRA/LiveBoard/Station/4060?%24top=30&%24format=JSON"
response = requests.get(url, headers=auth.get_auth_header())
print(response.json())
