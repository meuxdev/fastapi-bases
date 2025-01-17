# Python Stuff
from typing import Optional
from enum import Enum
# Pydantic
from pydantic import BaseModel, Field, EmailStr, PaymentCardNumber
# FastAPI
from fastapi import FastAPI, Body, Query, Path, status, Response


app = FastAPI()


# Models
class HairColor(Enum):
    """ Hair Color Enum """
    white = "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red"


class CountriesPermited(Enum):
    """ Countries Permited on the API """
    MX = "Mexico"
    COL = "Colombia"
    EU = "Estados Unidos"
    ARG = "Argentina"


class PersonOut(BaseModel):
    """ Person Model for response """
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Alejandro",
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Andrade Soriano",
    )
    age: int = Field(
        ...,
        gt=0,
        le=119,
        example=24,
    )
    # Pydantic Exotic Values
    email: EmailStr = Field(
        ...,
        example="myexapleemail@gmail.com",
    )
    # Optional Values
    payment_card: Optional[PaymentCardNumber] = Field(default=None)
    hair_color: Optional[HairColor] = Field(
        default=HairColor.black,
        example=HairColor.blonde,
    )
    is_married: Optional[bool] = Field(
        default=None,
        example=False,
    )


class Location(BaseModel):
    """ Location Model """
    city: str = Field(
        ...,
        min_length=1,
        max_length=20,
    )
    state: str = Field(
        ...,
        min_length=1,
        max_length=20
    )
    country: Optional[CountriesPermited] = Field(
        default=CountriesPermited.MX
    )

    class Config:
        """ Config Example for docs """
        schema_extra = {
            "example": {
                "city": "La Plata",
                "state": "Los Hornos",
                "country": CountriesPermited.ARG,
            }
        }


class Person(BaseModel):
    """ Person Model """
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Alejandro",
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Andrade Soriano",
    )
    age: int = Field(
        ...,
        gt=0,
        le=119,
        example=24,
    )
    # Pydantic Exotic Values
    email: EmailStr = Field(
        ...,
        example="myexapleemail@gmail.com",
    )
    # Optional Values
    payment_card: Optional[PaymentCardNumber] = Field(default=None)
    hair_color: Optional[HairColor] = Field(
        default=HairColor.black,
        example=HairColor.blonde,
    )
    is_married: Optional[bool] = Field(
        default=None,
        example=False,
    )
    password: str = Field(
        ...,
        min_length=8,
        example="Veryverysecurepassword",
    )

    """
    # CONFIG CLASS BLOCK
    class Config:
        schema_extra = {
            "example": {
                "first_name": "Facundo",
                "last_name": "Garcia Martoni",
                "age": 21,
                "hair_color": HairColor.blonde,
                "is_maried": False
            }

        }
    """


@app.get(
    path="/",
    status_code=status.HTTP_200_OK,
)
def home():
    """
        Endpoint main -> /
        returns hello world JSON
    """
    return {"Hello": "World"}


# Request and Response Body
# Body(...) -> obligatory body parameter
@app.post(
    path="/person/new",
    response_model=Person,
    response_model_exclude={"password"},
    response_model_include={"first_name", "last_name", "age", "hair_color"},
    status_code=status.HTTP_201_CREATED,
)
def create_person(person: Person = Body(...)):
    """/person/new -> creates a new person"""
    return person


# Validations querry params
@app.get(
    path="/person/detail",
    status_code=status.HTTP_200_OK,
)
def show_person(
    # Validations and definitions of the query parameters
    # query parameters should be optional
    # path parameters always should be obligatory
    name: Optional[str] = Query(
        None,
        min_length=1,
        max_length=50,
        title="Person Name",
        description="The name of the person to look.",
        example="Alejandro",
    ),
    # ... -> meaning obligatory
    # age: int = Query(...) | Obligatory Query
    age: Optional[int] = Query(
        None,
        ge=18,
        lt=120,
        title="Person Age",
        description="The age of the person to look.",
        example=24,
    ),
):
    return {name: age}


# Validations: Path Parameters
@app.get(path="/person/detail/{person_id}")
def show_person_path(
    person_id: int = Path(
        ...,
        ge=1,
        title="Id Person",
        description="The Id of the person",
        example=123,
    ),
    response: Response = Response(
        status_code=status.HTTP_200_OK
    ),
):
    if person_id == 666:
        response.status_code = status.HTTP_203_NON_AUTHORITATIVE_INFORMATION
        return {"Response": "Thats an evil number 😈"}
    return {person_id: "It exists!"}


# Validations: Request Body
@app.put(
    path="/person/{person_id}",
    status_code=status.HTTP_202_ACCEPTED
)
def update_person(
    person_id: int = Path(
        ...,
        title="Person Id",
        description="Id to update the person",
        gt=0,
        example=123
    ),
    person: Person = Body(...),
    location: Location = Body(...),
):
    results = person.dict()
    results.update(location.dict())
    return results
