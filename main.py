from fastapi import FastAPI
from user.routes import router as user
from note.routes import note_router as note

app = FastAPI()
app.include_router(router=user)
app.include_router(router=note)
