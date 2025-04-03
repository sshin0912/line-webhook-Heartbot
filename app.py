from flask import Flask, request
import requests
import json

app = Flask(__name__)

# LINEのアクセストークン（Messaging APIから取得）
LINE_ACCESS_TOKEN = "KFDPQj7iskWtUWVeVk26iFDW8oNglpYwvUYSHGDRYh6V9tr8SoN6OByltHDL0t0gNwfup2w1YcdeJgctY6AYclRZNv/GGB1Cbvw+BPmzklOZolQgb52fZ5jqGMml0CM/7ajY1lecVVvaaGvvTfHM9gdB04t89/1O/w1cDnyilFU="

def send_welcome_message(group_id, user_name):
    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_ACCESS_TOKEN}"
    }
    data = {
        "to": group_id,
        "messages": [{"type": "text", "text": f"ようこそ {user_name}！"}]
    }
    requests.post(url, headers=headers, data=json.dumps(data))

@app.route("/webhook", methods=["POST"])
def webhook():
    body = request.json
    events = body.get("events", [])

    for event in events:
        if event["type"] == "memberJoined":  # メンバー参加イベント
            group_id = event["source"]["groupId"]
            for member in event["joined"]["members"]:
                user_name = get_user_name(member["userId"])
                send_welcome_message(group_id, user_name)

    return "OK"

def get_user_name(user_id):
    url = f"https://api.line.me/v2/bot/profile/{user_id}"
    headers = {
        "Authorization": f"Bearer {LINE_ACCESS_TOKEN}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get("displayName", "ゲスト")
    return "ゲスト"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
