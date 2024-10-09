from fastapi import FastAPI
from src import curd_apis
from .db import get_db, engine, Base
from .schema import *

app = FastAPI()


@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)


app.include_router(curd_apis.router)
