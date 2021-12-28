""" Data models module for plotbot.py
"""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, validator, ValidationError
from treelib import Tree

# -------------------------------------
#   API response and payload models
# -------------------------------------


class APIResponse(BaseModel):
    """Wrapper class for responses from an API call

    Args:
        data (dict): data in API response
        code (int): response code (200 for success)
        message (str): message returned from API
    """

    data: dict
    code: int
    message: str


class Payload(BaseModel):
    """Wrapper class for POST request payload

    Args:
        prompt: str containing the prompt to pass to the generator
        temperature: temperature paramtere to pass to the generator
    """

    prompt: str
    temperature: float

    class Config:
        schema_extra = {
            "example": {
                "prompt": "Hayden dumped his bag at the foot of the stairs and ran up them two at a time. He was so excited to be home that he could hardly contain himself.",
                "temperature": 0.71234132,
            }
        }


# -------------------------------------
#   Classes for authentication
# -------------------------------------
class Token(BaseModel):
    """Model for JWT token

    Args:
        access_token (str): hashed string token
        token_type: indicator of JWT token type
    """

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Model for data stored in token

    Args:
        username (str): hashed string token represneting username
        scopes: string list of scopes avialable
        expires: when the token will expire
    """

    username: Optional[str] = None
    scopes: List[str] = []
    expires: datetime


# -------------------------------------
#   Classes for story storage
# -------------------------------------
class StoryTree:
    """Wrapper class for storing tree objects in mongo as a dictionary"""

    def __init__(self, userid: str, tree: Tree):
        self.account_id = account_id
        self.tree = tree
        self.date_time = datetime.utcnow()


# -------------------------------------
#   Classes for UserDetails
# -------------------------------------


class Name(BaseModel):
    """Name subclass used for UserDetails model

    Args:
        firstname (str): firstname of user
        secondname (str): firstname of user
    """

    firstname: str
    secondname: str


class UserDetails(BaseModel):
    """UserDetails model for PlotBot users

    Args:
        BaseModel ([type]): [description]
    """

    name: Name  # use nested model definition
    username: str
    password: str  # hashed password
    userid: Optional[str] = None
    email: EmailStr
    user_role: str
    disabled: Optional[bool] = False

    class Config:
        schema_extra = {
            "example": {
                "name": {"firstname": "Alexei", "surname": "Guinness"},
                "username": "a_dummy_user",
                "password": "us3Th3F0rceLuk3",
                "userid": "308fdfae-ca09-11eb-b437-f01898e87167",
                "email": "ben@kenobi.com",
                "disabled": False,
                "user_role": "story:reader,story:writer",
            }
        }
