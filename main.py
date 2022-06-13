# Python Stuff
from typing import Optional
# Pydantic
from pydantic import BaseModel
# FastAPI
from fastapi import FastAPI, Body


app = FastAPI()


# Models


class Person(BaseModel):
    first_name: str
    last_name: str
    age: int
    # Optional Values
    hair_color: Optional[str] = None
    is_married: Optional[bool] = None


@app.get("/")
def home():
    """
        / -> branch
        returns hello world JSON
    """
    return {"Hello": "World"}


# Request and Response Body
# Body(...) -> obligatory body parameter
@app.post("/person/new")
def create_person(person: Person = Body(...)):
    """/person/new -> creates a new person"""
    return person
