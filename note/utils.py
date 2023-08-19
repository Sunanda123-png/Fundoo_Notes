import datetime
import json

from user.utils import decode_access_token
from fastapi import HTTPException, Request, Depends
from sqlalchemy.orm import Session
from core.db import get_db
from user.models import User
import redis
from redbeat import RedBeatSchedulerEntry as Task
from celery.schedules import crontab
from tasks import celery


def get_token(request: Request, db: Session = Depends(get_db)):
    try:
        token = request.headers.get('token')
        if not token:
            raise HTTPException(status_code=404, detail="Token not found")
        payload = decode_access_token(token)
        user = db.query(User).filter_by(id=payload.get('user')).first()
        if user is None:
            raise HTTPException(status_code=404, detail="user is not in db")
        # return user
        request.state.user = user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


class Cache:
    client = redis.Redis(host="localhost", port=6379, db=0)

    @classmethod
    def save(cls, user_id: int, note: dict):
        user_id = f"user_{user_id}"
        note_id = f"note_{note.get('id')}"
        if "reminder" in note.keys():
            if isinstance(note["reminder"], datetime.datetime):
                note["reminder"] = str(note["reminder"])
        cls.client.hset(user_id, note_id, json.dumps(note))

    @classmethod
    def get_notes(cls, user_id: int):
        user_id = f"user_{user_id}"
        notes = []
        for note_id, note_json in cls.client.hgetall(user_id).items():
            note = json.loads(note_json)
            if not note["is_archive"] and not note["is_trash"]:
                notes.append(note)
        return notes if notes else None

    @classmethod
    def delete_note(cls, user_id: int, note_id: int):
        user_id = f"user_{user_id}"
        note_id = f"note_{note_id}"
        deleted = cls.client.hdel(user_id, note_id)
        return deleted == 1


def add_reminder(note):
    reminders = note.reminder
    if reminders:
        task = Task(name=f'{note.user_id}_{note.id}',
                    task='tasks.send_notification',
                    schedule=crontab(minute=reminders.minute, hour=reminders.hour, day_of_month=reminders.day,
                                     month_of_year=reminders.month),
                    app=celery,
                    args=[note.user.email, note.description, note.title])
        task.save()


class CustomException(Exception):
    def __init__(self, message='Bad Request', status_code=400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}'
