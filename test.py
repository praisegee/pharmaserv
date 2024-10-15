import requests
import json


data = {
    "templateUrl": "https://github.com/praisegee/new/blob/main/hco.xlsx",
    "companyId": "234234234",
    "managerId": "895958989",
    "envWebhooks": {
        "dev": "https://dev.copilot.pharmaserv.co/api/v1/webhook/hcp/creation",
        "staging": "https://staging.copilot.pharmaserv.co/api/v1/webhook/hcp/creation",
        "production": "https://prod.copilot.pharmaserv.co/api/v1/webhook/hcp/creation",
    },
}

resp = requests.post("http://127.0.0.1:8000/onboard", json=data)

print(resp.reason)
