""" Implements oAuth2 for fabulator

Raises:
    credentials_exception: when credentials are incorrect or expired

"""
import os
from time import tzname
from datetime import timedelta, datetime
from typing import Optional
import redis
from jose.exceptions import ExpiredSignatureError
from jose import jwt
from pytz import timezone
from passlib.context import CryptContext
from api.helpers import ConsoleDisplay
import api.database as database
from fastapi import HTTPException, status
from api.models import TokenData

REDISHOST = os.getenv(key="REDISHOST")
REDISPORT = os.getenv(key="REDISPORT")
REDISPASSWORD = os.getenv(key="REDISPASSWORD")
USER_COLLECTION_NAME = os.getenv(key="USER_COLLECTION_NAME")
timezone(tzname[0]).localize(datetime.now())
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

DEBUG = bool(os.getenv("DEBUG", "False") == "True")


class Authentication:
    def __init__(self):

        self.SECRET_KEY = os.getenv("SECRET_KEY")
        self.ALGORITHM = os.getenv("ALGORITHM")
        self.ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
        self.user_storage = database.UserStorage()
        self.console_display = ConsoleDisplay()

    def verify_password(self, plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password):
        return pwd_context.hash(password)

    async def get_user_by_username(self, username: str):
        """returns the details for a given userid"""
        return await self.user_storage.get_user_details_by_username(username=username)

    async def get_user_by_user_id(self, user_id: str):
        """returns the details for a given user_id"""
        return await self.user_storage.get_user_details_by_user_id(user_id=user_id)

    async def authenticate_user(self, username: str, password: str):
        """passed a db of users & username and input password, verifies password - returns user"""
        user = await self.get_user_by_username(username)
        if not user:
            return False
        if not self.verify_password(password, user.password):
            return False
        return user

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        """create an access token with an expiry date"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone("gmt")) + expires_delta
        else:
            expire = datetime.now(timezone("gmt")) + timedelta(
                minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES
            )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt

    def add_blacklist_token(self, token):
        """add the given token to the blacklist"""
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        if DEBUG:
            self.console_display.show_debug_message(
                message_to_show=f"REDISHOST:{REDISHOST}"
            )
            self.console_display.show_debug_message(
                message_to_show=f"REDISPORT:{REDISPORT}"
            )
        redis_client = redis.StrictRedis(
            host=REDISHOST, port=REDISPORT, password=REDISPASSWORD
        )

        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            user_id: str = payload.get("sub")
            token_scopes = payload.get("scopes", [])
            expires = payload.get("exp")
            token_data = TokenData(scopes=token_scopes, username=user_id, expires=expires)
        except ExpiredSignatureError:
            raise credentials_exception
        result = redis_client.setex(
            token,
            int((token_data.expires - datetime.now(timezone("gmt"))).total_seconds()),
            1,
        )
        redis_client.close()
        return result

    def is_token_blacklisted(self, token):
        """return true if supplied token is in the blacklist"""
        # need to create a new instance of aioredis to get pytests to work
        if DEBUG:
            self.console_display.show_debug_message(
                message_to_show=f"REDISHOST:{REDISHOST}"
            )
            self.console_display.show_debug_message(
                message_to_show=f"REDISPORT:{REDISPORT}"
            )
        redis_client = redis.StrictRedis(
            host=REDISHOST, port=REDISPORT, password=REDISPASSWORD
        )
        if redis_client.get(token):
            redis_client.close()
            return True
        else:
            redis_client.close()
            return False
