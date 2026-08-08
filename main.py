from fastapi import FastAPI
import random

app = FastAPI()

@app.get("/")
async def read_root():  
    return {"message": "Hello, World!"} 

@app.get("/teste1")
async def funcao_teste():
    return {"message": True, "num_aleatorio": random.randint(1, 1000)}