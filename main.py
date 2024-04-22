import uvicorn
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import json
from utils import record_info

app = FastAPI()

# Load configurations
with open('./configs.json') as file:
    configs = json.load(file)

line_bot_api = LineBotApi(configs['channel_access_token'])
handler = WebhookHandler(configs['channel_secret'])

@app.post("/callback")
async def callback(request: Request):
    # Get X-Line-Signature header value
    signature = request.headers.get('x-line-signature')

    # Get request body as text
    body = await request.body()
    body_text = body.decode('utf-8')

    # Handle webhook body
    try:
        handler.handle(body_text, signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    return JSONResponse(content={"detail": "OK"})

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg_content = event.message.text
    if '1000' in msg_content:
        user_send = event.source.user_id
        tagged_user = [word for word in msg_content.split() if word.startswith('@')]  
        record_info(user_send, tagged_user, msg_content)

        confirmation_message = f"1000 is sent to {tagged_user}"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=confirmation_message)
        )

if __name__ == "__main__":

    uvicorn.run(app, host="0.0.0.0", port=8080)
