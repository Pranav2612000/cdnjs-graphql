from typing import Optional
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory='static/')

@app.get("/")
def read_root(request: Request):
    #return {"Hello": "World"}
    return templates.TemplateResponse('index.html', context={'request': request})

@app.get("/getinfo/")
def read_item():
    return "GraphQL endpoint to return data"
