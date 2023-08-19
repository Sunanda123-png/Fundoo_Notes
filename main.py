from fastapi import FastAPI, Security, Depends, Request, Response
from fastapi.security import APIKeyHeader
import json
from note.utils import get_token
from user.routes import router as user
from note.routes import note_router as note
from labels.routes import label_router as labels
from note.utils import CustomException
app = FastAPI()


@app.middleware('http')
async def exception_handler(request: Request, call_next):
    try:
        response = await call_next(request)
    except CustomException as ce:
        response = Response(content=json.dumps({'message': str(ce.message), 'status': ce.status_code}),
                            status_code=ce.status_code,
                            media_type='application/json')
    except Exception as ex:
        response = Response(content=json.dumps({'message': str(ex), 'status': 400}),
                             status_code=400,
                             media_type='application/json')
    return response


app.include_router(router=user, tags=["user_api"])
app.include_router(router=note, dependencies=[Depends(get_token), Security(APIKeyHeader(name="token"))],
                   tags=["notes_api"])
app.include_router(router=labels, dependencies=[Depends(get_token), Security(APIKeyHeader(name="token"))],
                   tags=["labels_api"])
