import requests

url = "https://api.batchdata.com/api/v1/property/search"

payload = {
    "searchCriteria": {
        "query": "Phoenix, AZ",
        "mls": {"daysOnMarket": {
                "min": 0,
                "max": 1
            }}
    },
    "options": {
        "skip": 0,
        "take": 5
    }
}
headers = {
    "Content-Type": "application/json",
    "Authorization": "GRMEAsmCA2peIse40ddWPeAIcwmPCF9KfDVKQX1e"
}

response = requests.request("POST", url, json=payload, headers=headers)

print(response.text)