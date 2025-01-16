import os
import time
from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage
from linebot.exceptions import InvalidSignatureError
from linebot.models.events import MessageEvent, TextMessage

app = Flask(__name__)

# LINE API設定
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# ユーザーのリクエストを記録する辞書 (タイムスタンプ付き)
user_requests = {}
REQUEST_EXPIRATION_TIME = 3 * 60 * 60  # 3時間（秒換算）

def cleanup_expired_requests():
    """有効期限が切れたリクエストを削除する"""
    current_time = time.time()
    expired_users = [
        user_id for user_id, timestamp in user_requests.items()
        if current_time - timestamp > REQUEST_EXPIRATION_TIME
    ]
    for user_id in expired_users:
        del user_requests[user_id]

@app.route("/callback", methods=["POST"])
def callback():
    """LINEのWebhookからリクエストを受け取る"""
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        return "Invalid signature", 400

    return "OK", 200

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    """ユーザーからのメッセージを処理"""
    user_id = event.source.user_id
    message = event.message.text

    # 「テスト」と送信された場合
    if message == "テスト":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="test ok")
        )
        return  # 処理を終了

    # 「通話したい」と送信された場合
    if message == "通話したい":
        current_time = time.time()

        # 古いリクエストをクリア
        cleanup_expired_requests()

        # リクエストを記録
        user_requests[user_id] = current_time

        # 他のユーザーのリクエストと一致するか確認
        if len(user_requests) == 2:
            for uid in user_requests.keys():
                line_bot_api.push_message(uid, TextSendMessage(text="お互いが通話を希望しました！"))
            user_requests.clear()  # リクエストをリセット
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="リクエストを記録しました。相手の希望を待っています。")
            )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
