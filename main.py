from fastapi import FastAPI

app = FastAPI()


# path operation decoration
@app.get("/")
def home():
    return {"Hello": "World"}
