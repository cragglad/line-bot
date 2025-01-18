# 必要なモジュールをインポート済みであること
from linebot.models import TextSendMessage

# Pushメッセージを送信する関数
def send_push_message(user_id, message):
    try:
        line_bot_api.push_message(
            user_id,
            TextSendMessage(text=message)
        )
        print(f"Pushメッセージ送信成功: {message}")
    except Exception as e:
        print(f"Pushメッセージ送信失敗: {e}")

# ハンドラー内でPushメッセージを送信
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    user_message = event.message.text

    if user_message == "テスト":
        # 最初の返信
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="メッセージを受け付けました！")
        )

        # その後のPushメッセージ
        send_push_message(user_id, "test ok")
