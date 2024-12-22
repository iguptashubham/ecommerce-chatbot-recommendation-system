from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from main import response_chat
import uvicorn

class ChatRequest(BaseModel):
    userinput: str

app = FastAPI()

@app.post('/chat')
async def chat_bot(request: ChatRequest):
    try:
        chat_response = response_chat(user_input=request.userinput)
        return chat_response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    uvicorn.run('api:app', host='0.0.0.0', port=600, reload=True)
