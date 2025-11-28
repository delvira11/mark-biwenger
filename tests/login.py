import requests

url = "https://biwenger.as.com/api/v2/auth/login"

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36",
    "Content-Type": "application/json; charset=UTF-8",
    "Accept": "application/json",
    "X-Version": "629",
    "X-Lang": "en"
}

data = {
    "email": "sleepwalking1113@gmail.com",
    "password": "Yoquesetio1"
}

response = requests.post(url, headers=headers, json=data)

print(response.status_code)
print(response.text)
