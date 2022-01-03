import requests
import json

url = "https://toloka.yandex.com/api/adjuster/adjustments/?mode=RELATIVE_TOP_N&value=5747&ratio=1"

payload = json.dumps({
  "filter": {
    "and": [
      {
        "or": [
          {
            "category": "profile",
            "key": "citizenship",
            "operator": "EQ",
            "value": "RU"
          }
        ]
      }
    ]
  },
  "adultContent": False,
  "projectId": 56044
})
headers = {
  'Authorization': 'OAuth AQAAAABWXSyvAACtpQB3tDhc1UMaihco_BRj8RQ',
  'Content-Type': 'application/json',
  # 'Cookie': 'JSESSIONID=node08qqcqt6ygc3pssu0nw28izrb1.node0'
}

response = requests.request("POST", url, headers=headers, data=payload)
from pprint import pprint
pprint(response.json().get('parameters').get('value'))
