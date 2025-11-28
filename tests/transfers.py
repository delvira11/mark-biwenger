import requests

url = "https://biwenger.as.com/api/v2/home"

headers = {
    "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOjI3NzU4MDQ1LCJpYXQiOjE3NjM4NDY3NDZ9.50VWJ9afeXey3fS49LeN6uluJNUK-FN9Kz4p4Wy-zp4",
    "X-User": "13299804",
    "X-League": "2039584",
    # "X-Version": "629",
    # "X-Lang": "en",
    # "Accept": "application/json",
    # "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)

print(response.status_code)
print(response.text)
