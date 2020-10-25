import graphene
from typing import Optional
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from starlette.graphql import GraphQLApp
import requests

def getLibraryInfo(name):
    r = requests.get("https://api.cdnjs.com/libraries/" + name)
    return r.json()
class Author(graphene.ObjectType):
    name = graphene.String()
    email = graphene.String()
    def __init__(self, author):
        try:
            self.name = author["name"]
        except:
            self.name = ""
        try:
            self.email = author["email"]
        except:
            self.email = ""

class Library(graphene.ObjectType):
    name = graphene.String()
    keywords = graphene.List(graphene.String)
    authors = graphene.List(Author)
    description= graphene.String()
    license= graphene.String()
    homepage = graphene.String()
    #autoupdate: 

    def __init__(self, name, keywords, description, license, homepage, authors):
        self.name = name
        self.keywords = keywords
        self.description = description
        self.license = license
        self.homepage = homepage
        processed_authors = []
        if(type(authors) == list):
            for author in authors:
                processed_authors.append(Author(author))
            self.authors = processed_authors
        elif(type(authors) == str):
            self.authors = [{"name":authors, "email":""}]

class Query(graphene.ObjectType):
    #library = graphene.String(name=graphene.String(default_value="stranger"))
    #library = Library("react", "frontend", "component-based ui library", "MIT")
    library = graphene.Field(Library, name=graphene.String(default_value="stranger"))
    def resolve_library(self, info, name):
        libData = getLibraryInfo(name)
        return Library(libData["name"], libData["keywords"], libData["description"], libData["license"], libData["homepage"], libData["authors"])

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
