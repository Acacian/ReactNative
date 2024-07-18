import os
import json
from fastapi import FastAPI
from pydantic import BaseModel
from deeppavlov import build_model
from deeppavlov.core.commands.utils import parse_config

# DOWNLOADS_PATH 환경 변수 확인 및 설정
downloads_path = os.getenv('DOWNLOADS_PATH', '/app/downloads')
os.environ['DOWNLOADS_PATH'] = downloads_path

print(f"DOWNLOADS_PATH: {downloads_path}") 

app = FastAPI()

# config 파일 읽기 및 수정
with open("/app/deep_pavlov_config.json", "r") as config_file:
    config = json.load(config_file)

# DOWNLOADS_PATH를 직접 대체
config['dataset_reader']['data_path'] = config['dataset_reader']['data_path'].replace("{DOWNLOADS_PATH}", downloads_path)

# 수정된 config로 모델 빌드
model = build_model(config, download=True)

class Request(BaseModel):
    text: str

class Response(BaseModel):
    intent: str

@app.post("/predict", response_model=Response)
def predict(request: Request):
    intent = model([request.text])[0]
    return Response(intent=intent)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)