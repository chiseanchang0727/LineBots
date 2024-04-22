from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import json
import sqlite3
from utils import record_info


app = Flask(__name__)

with open('./configs.json') as file:
    configs = json.load(file)

line_bot_api = configs['channel_access_token']
handler = configs['channel_secret']



@app.route("/callback", methods=['POST'])
def callback():
    # Get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # Get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # Handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg_content = event.message.text
    if '1000' in msg_content:
        user_send = event.source.user_id

        tagged_user = [word for word in msg_content.split() if word.startwith('@')]

        record_info(user_send, tagged_user, msg_content)




if __name__ == "__main__":

    2 