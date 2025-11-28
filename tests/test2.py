import requests

url = "https://biwenger.as.com/api/v2/account"

headers = {
    "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOjI3NzU4MDQ1LCJpYXQiOjE3NjM4NDU5NDR9.1AFdXjuQJmX4WLsz4xRJZeLRUgY0MphTlIc-Wr5zP18",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "X-Version": "629",
    "X-Lang": "en"
}

response = requests.get(url, headers=headers)

print(response.status_code)
print(response.json())
