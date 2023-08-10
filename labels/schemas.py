from pydantic import BaseModel


class LabelsValidator(BaseModel):
    name: str
    colour_field: str
