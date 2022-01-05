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
from time import tzname
from datetime import timedelta, datetime
from pytz import timezone

# import fastapi
from treelib import Tree
from fastapi import FastAPI, HTTPException, Body, Depends, Security, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    SecurityScopes,
)
from pydantic.error_wrappers import ValidationError
from aitextgen import aitextgen
from jose import JWTError, jwt
from passlib.context import CryptContext
from api.helpers import ConsoleDisplay
from api.models import (
    APIResponse,
    GeneratorPayload,
    StoryPayload,
    Token,
    TokenData,
    UserDetails,
)
from api.authentication import Authentication
import api.database as database
import api.config


# set env vars & application constants
app = FastAPI()
VERSION = "0.1.0"
NAME = "Plotbot"
DEBUG = bool(os.getenv("DEBUG", "False") == "True")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

timezone(tzname[0]).localize(datetime.now())
# setup helper for formatting debug messages
console_display = ConsoleDisplay()
origins = ["http://localhost:9000", "localhost:9000", "http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login",
    scopes={
        "story:reader": "Read story details",
        "story:writer": "write story details",
    },
)
oauth = Authentication()

# ----------------------------
#     Authenticaton routines
# ----------------------------


@app.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> dict:
    """handle oauth login procedure

    Args:
        form_data (OAuth2PasswordRequestForm, optional): requestform with username & password. Defaults to Depends().

    Raises:
        HTTPException: raised when user is not found in user collection

    Returns:
        access_token dict
    """
    user = await oauth.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # creates a token for a given user with an expiry in minutes
    access_token = oauth.create_access_token(
        data={"sub": user.user_id, "scopes": form_data.scopes},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}


async def get_current_user_token(
    token: str = Depends(oauth2_scheme),
) -> str:
    """returns current_user access token

    Args:
        token (str, optional): dict - access_token and token_type. Defaults to Depends(oauth2_scheme).

    Returns:
        token: dict containing access_token and token_type
    """
    return token


@app.get("/logout")
async def logout(token: str = Depends(get_current_user_token)) -> APIResponse:
    """handles oauth logout

    Args:
        token (str, optional): dict - access_token and token_type. Defaults to Depends(get_current_user_token).

    Returns:
        APIResponse: data property contains successful logout message
    """
    if oauth.add_blacklist_token(token):
        return APIResponse(data={"Logout": True}, code=200, message="Success")


async def get_current_user(
    security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme)
) -> UserDetails:
    """get the current logged in user details

    Args:
        security_scopes (SecurityScopes): string containing valid scopes
        token (str, optional):  dict - access_token and token_type. Defaults to Depends(oauth2_scheme).

    Raises:
        credentials_exception: raised if the token is invalid, expired or blacklisted
        HTTPException: raised if user scopes do not match those requested

    Returns:
        User: object containing user's details
    """
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        print(f"token{token}")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        expires = payload.get("exp")
        token_data = TokenData(scopes=token_scopes, username=user_id, expires=expires)
    except (JWTError, ValidationError):
        raise
    user = await oauth.get_user_by_user_id(user_id=token_data.username)
    if user is None:
        raise credentials_exception
    # check token expiration
    if expires is None:
        raise credentials_exception
    if datetime.now(timezone("gmt")) > token_data.expires:
        raise credentials_exception
    # check if the token is blacklisted
    if oauth.is_token_blacklisted(token):
        raise credentials_exception
    # if we have a valid user and the token is not expired get the scopes
    token_data.scopes = list(set(token_data.scopes) & set(user.user_role.split(" ")))
    if DEBUG:
        console_display.show_debug_message(
            message_to_show=f"requested scopes in token:{token_scopes}"
        )
        console_display.show_debug_message(
            message_to_show=f"Required endpoint scopes:{security_scopes.scopes}"
        )

    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=403,
                detail="Insufficient permissions to complete action",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user


async def get_current_active_user_account(
    current_user: UserDetails = Security(get_current_user, scopes=["story:reader"])
) -> str:
    """return user_id for current (logged in) user (hashed salted string)

    Args:
        current_user (UserDetails, optional): user details object for current user. Defaults to Security(get_current_user, scopes=["story:reader"]).

    Raises:
        HTTPException: raises 400 if user is inactive

    Returns:
        str: user_id
    """
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user.user_id


# ------------------------
#       API Routes
# ------------------------


@app.get("/")
async def get(
    current_user: UserDetails = Security(get_current_user, scopes=["story:reader"])
) -> APIResponse:
    """Returns current version of API and user details

    Args:
        current_user (UserDetails, optional): logged in user details. Defaults to Security(get_current_user, scopes=["story:reader"]).

    Returns:
        APIResponse: object containing API details
    """
    return APIResponse(
        data={"version": VERSION, "name": NAME, "user": current_user.username},
        code=200,
        message="Success",
    )


@app.get("/story")
async def get_latest_story_object(
    current_user: UserDetails = Security(get_current_user, scopes=["story:reader"])
) -> APIResponse:
    """Returns current version of a story for the current user

    Args:
        current_user (UserDetails, optional): logged in user details. Defaults to Security(get_current_user, scopes=["story:reader"]).

    Returns:
        APIResponse: object containing Story object wrapped in APIResponse class
    """
    if DEBUG:
        console_display.show_debug_message(
            message_to_show="get_latest_story_object() called"
        )

    try:
        if DEBUG:
            console_display.show_debug_message(
                message_to_show=f"Reading story object from mongodb for user_id:{current_user.user_id}"
            )
        db_storage = database.StoryStorage()
        retrieve_reponse = await db_storage.return_latest_story(
            user_id=current_user.user_id
        )
        # retrieve_reponse.show()
    except Exception as exception_object:
        console_display.show_exception_message(
            message_to_show="Error occured retrieving story from mongodb"
        )
        print(exception_object)
        raise

    return APIResponse(
        data={"story": retrieve_reponse},
        code=200,
        message="Success",
    )


@app.get("/story/{document_id}")
async def get_a_story_object(
    document_id: str,
    current_user: UserDetails = Security(get_current_user, scopes=["story:reader"]),
) -> APIResponse:
    """Returns an identified story for the current user

    Args:
        current_user (UserDetails, optional): logged in user details. Defaults to Security(get_current_user, scopes=["story:reader"]).
        document_id : str : saved database document id
    Returns:
        APIResponse: object containing Story object wrapped in APIResponse class
    """
    if DEBUG:
        console_display.show_debug_message(
            message_to_show="get_a_story_object() called"
        )

    try:
        if DEBUG:
            console_display.show_debug_message(
                message_to_show=f"Reading a story object: {document_id} from mongodb for user_id:{current_user.user_id}"
            )
        db_storage = database.StoryStorage()
        retrieve_reponse = await db_storage.return_a_story(
            user_id=current_user.user_id, document_id=document_id
        )
        retrieve_reponse.show()
    except Exception as exception_object:
        console_display.show_exception_message(
            message_to_show="Error occured retrieving the story from mongodb"
        )
        print(exception_object)
        raise

    return APIResponse(
        data={"story": retrieve_reponse},
        code=200,
        message="Success",
    )


@app.post("/story/")
async def save_text(
    parent_id: str = None,
    current_user: UserDetails = Security(get_current_user, scopes=["story:writer"]),
    request: StoryPayload = Body(...),
) -> APIResponse:
    """save provided text snippet in the next child node of the story tree

    Args:
        current_user (UserDetails, optional): logged in user details.
        request (StoryPayload, optional): Payload model containing text to store.
        Defaults to Body(...).
        pranet_id (str): id of parent node - if None then assumed to be root

    Raises:
        HTTPException: for an errored response from the generator model

    Returns:
        APIResponse: data attribute contains the generated text or an error
    """
    try:
        if DEBUG:
            console_display.show_debug_message(
                message_to_show="Writing text to mongodb story tree"
            )
        db_storage = database.StoryStorage()
        save_reponse = await db_storage.add_text_to_story_tree(
            text=request.text, user_id=current_user.user_id, parent_id=parent_id
        )
    except Exception as exception_object:
        console_display.show_exception_message(
            message_to_show="Error occured storing text in mongodb"
        )
        print(exception_object)
        raise

    return APIResponse(
        data={"save_info": save_reponse, "username": current_user.username},
        code=200,
        message="Success",
    )


@app.get("/text")
async def get_latest_story_text(
    current_user: UserDetails = Security(get_current_user, scopes=["story:reader"])
) -> APIResponse:
    """Returns current version of a story text for the current user

    Args:
        current_user (UserDetails, optional): logged in user details. Defaults to Security(get_current_user, scopes=["story:reader"]).

    Returns:
        APIResponse: object containing text object wrapped in APIResponse class
    """
    if DEBUG:
        console_display.show_debug_message(
            message_to_show="get_latest_story_text() called"
        )

    try:
        if DEBUG:
            console_display.show_debug_message(
                message_to_show=f"Reading story text from mongodb for user_id:{current_user.user_id}"
            )
        db_storage = database.StoryStorage()
        retrieve_reponse = await db_storage.return_latest_story_text(
            user_id=current_user.user_id
        )
    except Exception as exception_object:
        console_display.show_exception_message(
            message_to_show="Error occured retrieving story text from mongodb"
        )
        print(exception_object)
        raise

    return APIResponse(
        data={"text": retrieve_reponse},
        code=200,
        message="Success",
    )


@app.post("/text")
async def generate_text(
    current_user: UserDetails = Security(get_current_user, scopes=["story:writer"]),
    request: GeneratorPayload = Body(...),
) -> APIResponse:
    """generate a text snippet from a given prompt

    Args:
        current_user (UserDetails, optional): logged in user details.
        request (Payload, optional): Payload model containing prompt and temperature settings.
        Defaults to Body(...).

    Raises:
        HTTPException: for an errored response from the generator model

    Returns:
        APIResponse: data attribute contains the generated text or an error
    """

    if DEBUG:
        console_display.show_debug_message(
            message_to_show=f"generate_text({request}) called"
        )
    try:
        if DEBUG:
            console_display.show_debug_message(
                message_to_show="generating text snippet"
            )
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

    return APIResponse(
        data={"generated_text": generated_text, "username": current_user.username},
        code=200,
        message="Success",
    )


@app.get("/save")
async def get_saves(
    current_user: UserDetails = Security(get_current_user, scopes=["story:reader"])
) -> APIResponse:
    """Returns a list of the saved story document ids for current_user

    Args:
        current_user (UserDetails, optional): logged in user details. Defaults to Security(get_current_user, scopes=["story:reader"]).

    Returns:
        APIResponse: object containing list of save document ids
    """
    if DEBUG:
        console_display.show_debug_message(message_to_show="get_saves() called")

    try:
        if DEBUG:
            console_display.show_debug_message(
                message_to_show=f"Getting list of saves for :{current_user.user_id}"
            )
        db_storage = database.StoryStorage()
        retrieve_reponse = await db_storage.list_all_story_saves(
            user_id=current_user.user_id
        )
    except Exception as exception_object:
        console_display.show_exception_message(
            message_to_show="Error occured retrieving list of documents from mongodb"
        )
        print(exception_object)
        raise

    return APIResponse(
        data={"document_ids": retrieve_reponse},
        code=200,
        message="Success",
    )


@app.delete("/save/{document_id}")
async def delete_a_save(
    document_id: str,
    current_user: UserDetails = Security(get_current_user, scopes=["story:writer"]),
) -> APIResponse:
    """Deletess a specified story document associated with the current user

    Args:
        current_user (UserDetails, optional): logged in user details. Defaults to Security(get_current_user, scopes=["story:writer"]).
        document_id: document that we want to delete

    Returns:
        APIResponse: object containing number of docs deleted
    """
    if DEBUG:
        console_display.show_debug_message(message_to_show="delete_a_save() called")

    try:
        if DEBUG:
            console_display.show_debug_message(
                message_to_show=f"deleting {document_id} save for :{current_user.user_id}"
            )
        db_storage = database.StoryStorage()
        retrieve_reponse = await db_storage.delete_a_story_save(
            user_id=current_user.user_id, document_id=document_id
        )
    except Exception as exception_object:
        console_display.show_exception_message(
            message_to_show="Error occured a document from mongodb"
        )
        print(exception_object)
        raise

    return APIResponse(
        data={"deletions": retrieve_reponse},
        code=200,
        message="Success",
    )


@app.delete("/save")
async def delete_all_saves(
    current_user: UserDetails = Security(get_current_user, scopes=["story:writer"])
) -> APIResponse:
    """Deletes all the sotry documents associated with the current user

    Args:
        current_user (UserDetails, optional): logged in user details. Defaults to Security(get_current_user, scopes=["story:reader"]).

    Returns:
        APIResponse: object containing number of docs deleted
    """
    if DEBUG:
        console_display.show_debug_message(message_to_show="delete_all_saves() called")

    try:
        if DEBUG:
            console_display.show_debug_message(
                message_to_show=f"deleting all saves saves for :{current_user.user_id}"
            )
        db_storage = database.StoryStorage()
        retrieve_reponse = await db_storage.delete_all_story_saves(
            user_id=current_user.user_id
        )
    except Exception as exception_object:
        console_display.show_exception_message(
            message_to_show="Error occured deleting documents from mongodb"
        )
        print(exception_object)
        raise

    return APIResponse(
        data={"deletions": retrieve_reponse},
        code=200,
        message="Success",
    )


# todo: route - return concatenated story text
# give the APi a tree object and parse it recursivley to generate a text
# todo: route - get a given save text of the story tree
