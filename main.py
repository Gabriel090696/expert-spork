import random

from fastapi import FastAPI

app = FastAPI()
#http://127.0.0.1:8000
@app.get("/")
async def root():
    return {"message" : "Hello World"}


@app.get("/teste1")
async def funcaoteste():
    return {"teste": True,
            'numero_aleatorio': random.randint(1, 1000)}
