import requests
import jwt
import time
import uuid
import json



AUTH_KEY_PATH = "C:\\DUI\\Django\\bossclean\\places\\authorized_key.json"
FOLDER_ID = "b1gs8v5i852pl0hmdhu3"

def get_iam_token():
    with open(AUTH_KEY_PATH, "r") as f:
        key_data = json.load(f)

    now = int(time.time())
    payload = {
        "aud": "https://iam.api.cloud.yandex.net/iam/v1/tokens",
        "iss": key_data["service_account_id"],
        "iat": now,
        "exp": now + 360,
        "jti": str(uuid.uuid4())
    }

    jwt_token = jwt.encode(
        payload,
        key_data["private_key"],
        algorithm="PS256",
        headers={"kid": key_data["id"]}
    )

    response = requests.post(
        "https://iam.api.cloud.yandex.net/iam/v1/tokens",
        json={"jwt": jwt_token}
    )

    if response.status_code == 200:
        return response.json()["iamToken"]
    else:
        raise Exception(f"IAM токен не получен: {response.status_code} — {response.text}")


def ask_yandex_gpt(prompt):
    iam_token = get_iam_token()
    url = 'https://llm.api.cloud.yandex.net/foundationModels/v1/completion'

    headers = {
        'Authorization': f'Bearer {iam_token}',
        'Content-Type': 'application/json'
    }

    body = {
        "modelUri": f"gpt://{FOLDER_ID}/yandexgpt-lite",
        "completionOptions": {
            "stream": False,
            "temperature": 0.6,
            "maxTokens": 200
        },
        "messages": [
            {
                "role": "user",
                "text": prompt
            }
        ]
    }

    response = requests.post(url, headers=headers, json=body)
    if response.status_code == 200:
        return response.json()["result"]["alternatives"][0]["message"]["text"]
    else:
        return f"Ошибка: {response.status_code} — {response.text}"

def ask_yandex_gpt_with_history(messages):
    iam_token = get_iam_token()
    folder_id = FOLDER_ID

    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"

    headers = {
        "Authorization": f"Bearer {iam_token}",
        "Content-Type": "application/json"
    }

    body = {
        "modelUri": f"gpt://{folder_id}/yandexgpt-lite",
        "completionOptions": {
            "stream": False,
            "temperature": 0.6,
            "maxTokens": 200
        },
        "messages": messages
    }

    response = requests.post(url, headers=headers, json=body)
    if response.status_code == 200:
        return response.json()["result"]["alternatives"][0]["message"]["text"]
    else:
        return f"Ошибка: {response.status_code} — {response.text}"