from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import json

app = Flask(__name__)

with open('config.json', 'r', encoding='utf8') as jfile:
	jdata = json.load(jfile)

token  = jdata["CHANNEL_ACCESS_TOKEN"]
secret = jdata["CHANNEL_SECRET"]
line_bot_api = LineBotApi(token)
handler = WebhookHandler(secret)

@app.route('/callback', methods = ['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text = True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message = TextMessage)
def handle_message(event):
    msg =  event.message.text
    if msg == "測試" or msg == "test":
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text = "早上好中國，現在我有冰淇淋"))

if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = 1226)
    print(">>>> bot is online <<<<")
  