import uvicorn
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import json
from utils import record_info, clear_database

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
    if '1000' == msg_content and event.message.quotedMessageId:
        # timestamp = event.timestamp
        
        user_id = event.source.user_id
        
        user_name = line_bot_api.get_profile(user_id)
                
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"I got {user_name}!")
        )

        
        replied_to_user_id = event.reply_to_message.user_id
        replied_to_user_profile = line_bot_api.get_profile(replied_to_user_id)
        replied_to_user_name = replied_to_user_profile.display_name
        
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"I got {replied_to_user_name}!")
        )

        
        record_info(event.source.user_id, replied_to_user_name, msg_content)
        confirmation_message = f"1000 is sent to {replied_to_user_name}"
        reply_text=confirmation_message   

            
    # elif "!bot, clear the database" == msg_content:
    #     result_message = clear_database()
    #     reply_text=result_message
    
    elif "!bot, Hi" == msg_content:
        reply_text = "Good morning, Master!"
        
    elif "Bot version" == msg_content:
        reply_text = "v1.4"

    line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_text)
        )

if __name__ == "__main__":

    uvicorn.run(app, host="0.0.0.0", port=8080)
