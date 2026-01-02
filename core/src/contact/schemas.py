from ninja import Schema

class ContactOut(Schema):
    id: int
    name: str
    type: str
