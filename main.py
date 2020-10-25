import graphene
from typing import Optional
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from starlette.graphql import GraphQLApp

class Library(graphene.ObjectType):
    name = graphene.String()
    keywords = graphene.List(graphene.String)
    description= graphene.String()
    #autoupdate: 
    license= graphene.String()

    def __init__(self, name, keywords, description, license):
        self.name = name
        self.keywords = keywords
        self.description = description
        self.license = license

class Query(graphene.ObjectType):
    #library = graphene.String(name=graphene.String(default_value="stranger"))
    #library = Library("react", "frontend", "component-based ui library", "MIT")
    library = graphene.Field(Library)
    def resolve_library(self, info):
        return Library("react", ["frontend", "ui"], "component-based ui library", "MIT")

app = FastAPI()
templates = Jinja2Templates(directory='static/')

@app.get("/")
def read_root(request: Request):
    #return {"Hello": "World"}
    return templates.TemplateResponse('index.html', context={'request': request})

@app.get("/getinfo/")
def read_item():
    return "GraphQL endpoint to return data"

'''
@app.get("/graphiql")
def get_graphiql():
    return GraphQLApp(schema=graphene.Schema(query=Query))
'''

app.add_route("/graphiql", GraphQLApp(schema=graphene.Schema(query=Query, types=[Library])))
