from fastapi import FastAPI
from pydantic import BaseModel
from deeppavlov import build_model, configs

app = FastAPI()

# Using ner_ontonotes as an example model
model = build_model(configs.ner.ontonotes_bert_mult, download=True)

class Request(BaseModel):
    text: str

class Response(BaseModel):
    intent: str

@app.post("/predict", response_model=Response)
def predict(request: Request):
    intent = model([request.text])[0]
    return Response(intent=intent)
