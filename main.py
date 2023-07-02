from fastapi import FastAPI
from fastapi.params import Body

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/create-post")
def create_posts(payload: dict = Body(...)):
    print(payload)
    return {"message": "successfully created a post"}
