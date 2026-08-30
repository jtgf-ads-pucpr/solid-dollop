from fastapi import FastAPI
import random
from pydantic import BaseModel

app = FastAPI()


class Estudante(BaseModel):
    nome: str
    curso: str
    ativo: bool

@app.get("/helloworld")
async def read_root():  
    return {"message": "Hello, World!"}

@app.get("/teste")
async def funcaoteste():  
    return {"teste": True, "num_aleatorio": random.randint(1, 1000)}

@app.post("/estudante/cadastro")
async def cadastrar_estudante(estudante: Estudante):
    return {"message": "Estudante cadastrado com sucesso!", "estudante": estudante}

@app.put("/estudante/update/{id_estudante}")
async def atualizar_estudante(id_estudante: int, estudante: Estudante):
    return {"message": f"Estudante com ID {id_estudante} atualizado com sucesso!", "estudante": estudante}

@app.delete("/estudante/delete/{id_estudante}")
async def deletar_estudante(id_estudante: int):
    return {"message": f"Estudante com ID {id_estudante} deletado com sucesso!"}
