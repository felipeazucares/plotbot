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
from pydantic.error_wrappers import ValidationError

# import fastapi
from treelib import Tree
from fastapi import FastAPI, HTTPException, Body, Depends, Security, status
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    SecurityScopes,
)
from api.helpers import ConsoleDisplay
from api.models import APIResponse, Payload, Token, TokenData, UserDetails
from aitextgen import aitextgen
from jose import JWTError, jwt
import api.config
from api.authentication import Authentication
from passlib.context import CryptContext


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
origins = ["http://localhost:9000", "localhost:9000"]

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
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """main login route for oauth authentication flow - returns bearer token"""
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


async def get_current_user_token(token: str = Depends(oauth2_scheme)):
    """returns current user token for logout"""
    return token


@app.get("/logout")
def logout(token: str = Depends(get_current_user_token)):
    """logsout current user by add token to redis managed blacklist"""
    if oauth.add_blacklist_token(token):
        return ResponseModel(data={"Logout": True}, message="Success")


async def get_current_user(
    security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme)
):
    """authenticate user and scope return user class"""
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
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        expires = payload.get("exp")
        token_data = TokenData(scopes=token_scopes, username=user_id, expires=expires)
    except (JWTError, ValidationError):
        raise credentials_exception
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
    current_user: UserDetails = Security(get_current_user, scopes=["user:reader"])
):
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
        APIResponse: object containing API details and current user
    """
    return APIResponse(
        data={"version": VERSION, "name": NAME, "user": current_user},
        code=200,
        message="Success",
    )


@app.post("/")
async def generate_text(
    get_current_user, scopes=["story:reader"], request: Payload = Body(...)
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

    # todo: we need to log in to be able to know which user a tree an story belongs now add
    # todo: the text to a tree
    # todo: if a tree doesn't already exist then create a new one and save it recording the id

    return APIResponse(data={"text": generated_text}, code=200, message="Success")


# generate a node in a tree with a call to aitextgen witha  given prompt
# write the

# get a version of the tree back from mongo

# get a given version
