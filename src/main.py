from fastapi import FastAPI
from src.curd_apis import router

app = FastAPI()


app.include_router(router)
