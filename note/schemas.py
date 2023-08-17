from pydantic import BaseModel
from typing import List

class NoteValidator(BaseModel):
    title: str
    description: str
    is_archive: bool = False
    is_trash: bool = False
    reminder: str = None


class CollaboratorValidator(BaseModel):
    note_id: int
    user_ids: List[int]
    is_update: bool = False
