import uuid


class Config:
    SECRET_KEY = uuid.uuid4().hex
