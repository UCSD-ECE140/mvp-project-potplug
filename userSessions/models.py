from pydantic import BaseModels

class User(BaseModel):
    """
    Create user class that matches the user table in the database
    Inherit from pydantic BaseModel
    """
    username: str
    password: str
    email: str
    first_name: str
    last_name: str


class Visitor(BaseModel):
    """
    Create visitor class that matches the visitor table in the database
    Inherit from pydantic BaseModel
    """
    username: str
    password: str