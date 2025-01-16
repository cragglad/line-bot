from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextMessage, MessageEvent, TextSendMessage
from linebot.exceptions import InvalidSignatureError

app = Flask(__name__)

# あなたのLINEチャネル情報を設定
LINE_CHANNEL_ACCESS_TOKEN = "あなたのチャネルアクセストークン"
LINE_CHANNEL_SECRET = "あなたのチャネルシークレット"

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/callback", methods=["POST"])
def callback():
    # X-Line-Signatureヘッダーの取得
    signature = request.headers["X-Line-Signature"]
    # リクエストボディの取得
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        return "Invalid signature", 400
    return "OK", 200

# メッセージイベントを処理
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text
    reply_message = f"あなたのメッセージ: {user_message}"
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_message)
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
