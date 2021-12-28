""" Data models module for plotbot.py
"""
from pydantic import BaseModel

# from treelib import Tree


class APIResponse(BaseModel):
    """Wrapper class for responses from an API call

    Args:
        BaseModel (pydantic basemodel): pydantic basemodel
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
