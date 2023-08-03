from fastapi import FastAPI
from user.routes import router as user

app = FastAPI()
app.include_router(router=user)

