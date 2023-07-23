# app.py
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageMessage
import os
import logging

app = Flask(__name__)

# ログの設定
logging.basicConfig(filename='app.log', level=logging.ERROR)

# Line botのAPI設定
line_bot_api = LineBotApi(os.environ.get("CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.environ.get("CHANNEL_SECRET"))

@app.route("/callback", methods=["POST"])
def callback():
    # LineからのWebhookリクエストを処理する関数
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        logging.error("InvalidSignatureError occurred")
        abort(400)
    return "OK"

@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    # 画像メッセージを受信した場合の処理
    try:
        reply_text = "申し訳ございません。現在、画像送信での処方せん受付を行っておりません。\nお手数をおかけ致しますが、メニューにあります「処方せん送信」から処方せんを送信するようお願い致します。\n\n「メニュー」が表示できない場合は、一度「トーク画面」から「トーク」へ戻っていただき、再度「たかさご薬局」を選択してください。\n\n「メニュー」はスマートフォンでしか表示されないため、iPadやパソコンからでは現在対応できておりません。"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))
    except Exception as e:
        logging.error(str(e))

if __name__ == "__main__":
    app.run(port=8000)
