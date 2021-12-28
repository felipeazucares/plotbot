"""
    ------------------------
       PLOT BOT API
    ------------------------
    Philip Suggars
    Red Robot Labs - Dec 2021
    Main API module for plotbot.py
    contains main API routes - each route returns an
    APIResponse object

Returns:
    ResponseModel: wrapper class containing response data
"""
import os
import fastapi
from treelib import Tree
from fastapi import FastAPI, HTTPException, Body, Depends, Security, status
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from api.helpers import ConsoleDisplay
from api.models import APIResponse, Payload
from aitextgen import aitextgen


app = FastAPI()
VERSION = "0.1.0"
NAME = "Plotbot"

# get debug flag from env file
DEBUG = bool(os.getenv("DEBUG", "False") == "True")
# setup helper for formatting debug messages
console_display = ConsoleDisplay()
origins = ["http://localhost:9000", "localhost:9000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ------------------------
#       API Routes
# ------------------------


@app.get("/")
async def get() -> dict:
    """Return the API version"""
    return APIResponse(
        data={"version": VERSION, "name": NAME}, code=200, message="Success"
    )


@app.post("/")
async def generate_text(request: Payload = Body(...)) -> APIResponse:
    """generate a text snippet from a given prompt

    Args:
        request (Payload, optional): Payload model containing prompt and temperature settings.
        Defaults to Body(...).

    Raises:
        HTTPException: for an errored response from the generator model

    Returns:
        ResponseModel: data doict contains the generated text
    """

    if DEBUG:
        console_display.show_debug_message(
            message_to_show=f"generate_text({request}) called"
        )
    try:
        ai_instance = aitextgen()
        generated_text = ai_instance.generate_one(
            prompt=request.prompt,
            max_length=100,
            temperature=float(request.temperature),
            repetition_penalty=1,
            num_beams=1,
        )
    except Exception as exception_object:
        console_display.show_exception_message(
            message_to_show="Error occured generating text."
        )
        print(exception_object)
        raise

    # todo: we need to log in to be able to know which user a tree an story belongs now add the text to a tree
    # todo: if a tree doesn't already exist then create a new one and save it recording the id

    return APIResponse(data={"text": generated_text}, code=200, message="Success")


# generate a node in a tree with a call to aitextgen witha  given prompt
# write the

# get a version of the tree back from mongo

# get a given version
