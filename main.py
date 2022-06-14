# Python Stuff
from typing import Optional
from enum import Enum
# Pydantic
from pydantic import BaseModel, Field
# FastAPI
from fastapi import FastAPI, Body, Query, Path


app = FastAPI()


# Models

class HairColor(Enum):
    white = "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red"


class Person(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
    )
    age: int = Field(
        ...,
        gt=0,
        le=119
    )
    # Optional Values
    hair_color: Optional[HairColor] = Field(default=None)
    is_married: Optional[bool] = Field(default=None)


class Location(BaseModel):
    city: str = Field(...)
    state: str = Field(...)
    country: str = Field(...)


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


# Validations querry params
@app.get("/person/detail")
def show_person(
    # Validations and definitions of the query parameters
    # query parameters should be optional
    # path parameters always should be obligatory
    name: Optional[str] = Query(
        None,
        min_length=1,
        max_length=50,
        title="Person Name",
        description="The name of the person to look."),
    # ... -> meaning obligatory
    # age: int = Query(...) | Obligatory Query
    age: Optional[int] = Query(
        None,
        ge=18,
        lt=120,
        title="Person Age",
        description="The age of the person to look.")
):
    return {name: age}


# Validations: Path Parameters
@app.get("/person/detail/{person_id}")
def show_person_path(
    person_id: int = Path(
        ...,
        ge=1,
        title="Id Person",
        description="The Id of the person")
):
    return {person_id: "It exists!"}


# Validations: Request Body
@app.put("/person/{person_id}")
def update_person(
    person_id: int = Path(
        ...,
        title="Person Id",
        description="Id to update the person",
        gt=0
    ),
    person: Person = Body(...),
    location: Location = Body(...),
):
    results = person.dict()
    return results
