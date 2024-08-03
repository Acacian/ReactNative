from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging
from main import generate_response, predict_intent

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Request(BaseModel):
    text: str

class Response(BaseModel):
    intent: str
    response: str

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@app.post("/predict", response_model=Response)
async def predict(request: Request):
    logger.info(f"Received predict request: {request.text}")
    try:
        intent = predict_intent(request.text)
        response = generate_response(request.text)
        logger.info(f"Sending predict response: Intent: {intent}, Response: {response}")
        return Response(intent=intent, response=response)
    except Exception as e:
        logger.error(f"Error in predict: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    logger.info(f"Received chat request: {request.message}")
    try:
        response = generate_response(request.message)
        logger.info(f"Sending chat response: {response}")
        return ChatResponse(response=response)
    except Exception as e:
        logger.error(f"Error in chat: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)