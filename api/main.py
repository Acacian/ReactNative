from fastapi import FastAPI
from pydantic import BaseModel
from deeppavlov import build_model
import os

# 필요한 디렉토리 생성
downloads_path = "/app/downloads"
if not os.path.exists(downloads_path):
    os.makedirs(downloads_path)

models_path = "/app/models"
if not os.path.exists(models_path):
    os.makedirs(models_path)

app = FastAPI()

model = build_model("/app/deep_pavlov_config.json", download=True)

class Request(BaseModel):
    text: str

class Response(BaseModel):
    intent: str

@app.post("/predict", response_model=Response)
def predict(request: Request):
    intent = model([request.text])[0]
    return Response(intent=intent)
