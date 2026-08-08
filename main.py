from fastapi import FastAPI
import random

app = FastAPI()

@app.get("/helloworld")
async def read_root():  
    return {"message": "Hello, World!"}

@app.get("/teste")
async def funcaoteste():  
    return {"teste": True, "num_aleatorio": random.randint(1, 1000)}
