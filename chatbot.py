import requests

def ask_perplexity(api_key, user_input):
    url = "https://api.perplexity.ai/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {
        "model": "sonar",
        "messages": [{"role": "user", "content": user_input}]
    }
    res = requests.post(url, headers=headers, json=payload)
    if res.status_code == 200:
        try:
            return res.json()["choices"][0]["message"]["content"]
        except:
            return "❌ 回覆格式解析失敗，可能是 API 結構改變。"
    else:
        return f"❌ 回覆失敗（HTTP {res.status_code}）：{res.text}"