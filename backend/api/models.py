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


class GeneratorPayload(BaseModel):
    """Wrapper class for POST text generation payload

    Args:
        prompt: str containing the prompt to pass to the generator
        temperature: temperature paramtere to pass to the generator
    """

    prompt: str
    temperature: Optional[float] = 0.7

    class Config:
        """example object for docs"""

        schema_extra = {
            "example": {
                "prompt": "Hayden dumped his bag at the foot of the stairs and ran up them two at a time. He was so excited to be home that he could hardly contain himself.",
                "temperature": 0.71234132,
            }
        }


class StoryPayload(BaseModel):
    """Wrapper class for POST text to store in database payload

    Args:
        text: text to store in the next child node
    """

    text: str

    class Config:
        """example object for docs"""

        schema_extra = {
            "example": {
                "text": "A piece of generated text that will be store in the next child node of the story tree.",
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


class Settings(BaseModel):
    authjwt_secret_key: str = "secret"
    # Configure application to store and get JWT from cookies
    authjwt_token_location: set = {"cookies"}
    # Disable CSRF Protection for this example. default is True
    authjwt_cookie_csrf_protect: bool = False


# -------------------------------------
#   Classes for story storage
# -------------------------------------
class Story(BaseModel):
    """Wrapper class for storing tree objects in mongo as a dictionary"""

    class Config:
        """required by Pydantic so we can include Tree objects in model"""

        arbitrary_types_allowed = True

    user_id: str
    tree: Tree
    date_time: datetime


class AddNodeResponse(BaseModel):
    """Wrapper class for returning the details ofr a node that we've added to the story tree"""

    class Config:
        """required by Pydantic so we can include Tree objects in model"""

        arbitrary_types_allowed = True

    new_node_id: str
    document_id: str
    story: Tree


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
    surname: str


class UserDetails(BaseModel):
    """UserDetails model for PlotBot users

    Args:
        BaseModel ([type]): [description]
    """

    name: Name  # use nested model definition
    username: str
    password: str  # hashed password
    user_id: str
    email: EmailStr
    user_role: str
    disabled: Optional[bool] = False

    class Config:
        """example object for docs"""

        schema_extra = {
            "example": {
                "name": {"firstname": "Alexei", "surname": "Guinness"},
                "username": "a_dummy_user",
                "password": "us3Th3F0rceLuk3",
                "user_id": "308fdfae-ca09-11eb-b437-f01898e87167",
                "email": "ben@kenobi.com",
                "disabled": False,
                "user_role": "story:reader,story:writer",
            }
        }
