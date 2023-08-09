from pydantic import BaseModel


class NoteValidator(BaseModel):
    title: str
    description: str
    is_archive: bool = False
    is_trash: bool = False
    reminder: str = None
