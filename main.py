from fastapi import FastAPI, Security, Depends
from fastapi.security import APIKeyHeader

from note.utils import get_token
from user.routes import router as user
from note.routes import note_router as note
from labels.routes import label_router as labels

app = FastAPI()
app.include_router(router=user, tags=["user_api"])
app.include_router(router=note, dependencies=[Depends(get_token), Security(APIKeyHeader(name="token"))], tags= ["notes_api"])
app.include_router(router=labels, dependencies=[Depends(get_token), Security(APIKeyHeader(name="token"))], tags=["labels_api"])
