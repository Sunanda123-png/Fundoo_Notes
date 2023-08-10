from fastapi import FastAPI
from user.routes import router as user
from note.routes import note_router as note
from labels.routes import label_router as labels

app = FastAPI()
app.include_router(router=user)
app.include_router(router=note)
app.include_router(router=labels)
