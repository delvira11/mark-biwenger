import requests
import json
import re

url = "https://cf.biwenger.com/api/v2/competitions/la-liga/data"

params = {
   # "lang": "en",
   # "score": "5",
   # "callback": "jsonp_1912703209"
}

headers = {
  #   "Host": "cf.biwenger.com",
     "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36",
  #  "Accept": "*/*",
  #  "Accept-Language": "en-GB,en;q=0.9",
  #  "Referer": "https://biwenger.as.com/",
  #  "Accept-Encoding": "gzip, deflate, br",
  #  "Sec-Ch-Ua": '"Chromium";v="141", "Not?A_Brand";v="8"',
  #  "Sec-Ch-Ua-Mobile": "?0",
  #  "Sec-Ch-Ua-Platform": '"Linux"',
}

response = requests.get(url, headers=headers, params=params)

text = response.text
json_text = re.sub(r'^jsonp_\d+\((.*)\)$', r'\1', text)
data = json.loads(json_text)

# i= 0
# for key in data['data']['players']:
#      i += 1
#      print(i)
#      print(data['data']['players'][key])
# #     break



