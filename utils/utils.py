"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

This file contains utility functions for the server
"""

import base64
import datetime
import functools
import os
import random
import re
import uuid
import zlib
from inspect import isawaitable
from typing_extensions import Any, Tuple, Optional, Callable

import aiohttp
import bcrypt
import jwt
from pymongo.asynchronous.database import AsyncDatabase
import orjson
import rapidfuzz.process
import sanic
import sanic.log
import aiofiles
import numpy

from async_lru import alru_cache

from utils.crypto.key_config import PRIVATE_KEY_PEM_PATH, PUBLIC_KEY_PEM_PATH, PRIVATE_KEY_PASSWORD
from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key
from cryptography.hazmat.backends import default_backend

from utils.exceptions import errors

# SSL keys
private_key = None
public_key = None

# Load the private key
if os.path.isfile(PRIVATE_KEY_PEM_PATH):
    with open(PRIVATE_KEY_PEM_PATH, 'rb') as f:
        private_key_data = f.read()
        try:
            private_key = load_pem_private_key(private_key_data, password=PRIVATE_KEY_PASSWORD,
                                               backend=default_backend())
        except ValueError as e:
            print("Error happened while trying to load private key PEM file.")
            if len(e.args) == 2 and isinstance(e.args[1], list):
                print(f"{e.args[0]}")
                for arg in e.args[1]:
                    print(f"{arg}")
            else:
                print(e)
            exit(1)
else:
    print(f"Error: no private key PEM file at: {PRIVATE_KEY_PEM_PATH}")
    exit(1)

# Load the public key
if os.path.isfile(PUBLIC_KEY_PEM_PATH):
    with open(PUBLIC_KEY_PEM_PATH, 'rb') as f:
        public_key_data = f.read()
        public_key = load_pem_public_key(public_key_data, backend=default_backend())
else:
    print(f"Error: no public key PEM file at: {PUBLIC_KEY_PEM_PATH}")
    exit(1)

if not os.path.isdir('res/battle-breakers-data/WorldExplorers/Content/'):
    print("Error: no game files found at: res/battle-breakers-data/WorldExplorers/Content/")
    print("Please clone submodules: git submodule update --init --recursive")
    print("Or export PAK contents in JSON format")
    exit(1)

# Cache game files
game_files_list = []
for root, dirs, files in os.walk('res/battle-breakers-data/WorldExplorers/Content/'):
    for file in files:
        game_files_list.append(os.path.join(root, file))
character_files_list = []
for root, dirs, files in os.walk('res/battle-breakers-data/WorldExplorers/Content/Characters'):
    for file in files:
        character_files_list.append(os.path.join(root, file))


async def read_file(filename: str, json: bool = True, raw: bool = True) -> dict[str, Any] | bytes | str:
    """
    Reads a file and returns the contents
    :param filename: The file to read
    :param json: Whether to parse the file as json
    :param raw: Whether to read the file as bytes
    :return: The contents of the file
    """
    sanic.log.logger.debug(f"Reading file: {filename} (json={json}, raw={raw})")
    if json:
        async with aiofiles.open(filename, "rb") as file:
            return orjson.loads((await file.read()))
    if raw:
        async with aiofiles.open(filename, "rb") as file:
            return await file.read()
    async with aiofiles.open(filename) as file:
        return await file.read()


async def write_file(filename: str, contents: Any, json: bool = True, raw: bool = True) -> None:
    """
    Writes to a file
    :param filename: The file to write to
    :param contents: The contents to write
    :param json: Whether to write the contents as json
    :param raw: Whether to write the contents as bytes
    """
    sanic.log.logger.debug(f"Writing file: {filename} (json={json}, raw={raw})")
    if json:
        async with aiofiles.open(filename, "wb") as file:
            await file.write(orjson.dumps(contents))
        return
    if raw:
        async with aiofiles.open(filename, "wb") as file:
            await file.write(contents)
        return
    async with aiofiles.open(filename, "w") as file:
        await file.write(contents)
    return


async def format_time(time: Optional[datetime.datetime | float | int | str] = None) -> str:
    """
    Formats the current time in the correct format for the MCP headers

    :param time: The time to format
    :return: The formatted time string in the format of YYYY-MM-DDTHH:MM:SS.mmmZ (ISO8601)
    """
    sanic.log.logger.debug(f"Formatting time: {time}")
    if time is None:
        sanic.log.logger.debug(
            f"No time provided, using current time: {datetime.datetime.now(datetime.UTC).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'}")
        return datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    else:
        if isinstance(time, datetime.datetime):
            sanic.log.logger.debug(f"Time is datetime: {time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'}")
            return time.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
        # elif isinstance(time, float) or isinstance(time, int):
        #     return datetime.datetime.fromtimestamp(time).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
        elif isinstance(time, str):
            sanic.log.logger.debug(f"Time is string: {datetime.datetime.fromisoformat(time).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'}")
            return datetime.datetime.fromisoformat(time).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
        else:
            sanic.log.logger.debug(f"Time is timestamp: {datetime.datetime.fromtimestamp(time).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'}")
            return datetime.datetime.fromtimestamp(time).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


async def get_nearest_12_hour_interval() -> datetime.datetime:
    """
    Gets the nearest 12 hour interval from the current time
    :return:
    """
    next_12hr = datetime.datetime.now(datetime.UTC) + datetime.timedelta(
        hours=12 - (datetime.datetime.now(datetime.UTC).hour % 12))
    sanic.log.logger.debug(f"Next 12 hour interval: {next_12hr}")
    return datetime.datetime(next_12hr.year, next_12hr.month, next_12hr.day, next_12hr.hour,
                             tzinfo=datetime.timezone.utc)


async def get_current_12_hour_interval() -> datetime.datetime:
    """
    Gets the current 12 hour interval
    :return:
    """
    current_12hr = datetime.datetime.now(datetime.UTC) - datetime.timedelta(
        hours=datetime.datetime.now(datetime.UTC).hour % 12)
    sanic.log.logger.debug(f"Current 12 hour interval: {current_12hr}")
    return datetime.datetime(current_12hr.year, current_12hr.month, current_12hr.day, current_12hr.hour,
                             tzinfo=datetime.timezone.utc)


async def get_nearest_24_hour_interval() -> datetime.datetime:
    """
    Gets the nearest 24 hour interval from the current time
    :return: The nearest 24 hour interval
    """
    next_24hr = datetime.datetime.now(datetime.UTC) + datetime.timedelta(
        hours=24 - (datetime.datetime.now(datetime.UTC).hour % 24))
    sanic.log.logger.debug(f"Next 24 hour interval: {next_24hr}")
    return datetime.datetime(next_24hr.year, next_24hr.month, next_24hr.day, next_24hr.hour,
                             tzinfo=datetime.timezone.utc)


async def get_current_24_hour_interval() -> datetime.datetime:
    """
    Gets the current 24 hour interval
    :return: The current 24 hour interval
    """
    current_24hr = datetime.datetime.now(datetime.UTC) - datetime.timedelta(
        hours=datetime.datetime.now(datetime.UTC).hour % 24)
    sanic.log.logger.debug(f"Current 24 hour interval: {current_24hr}")
    return datetime.datetime(current_24hr.year, current_24hr.month, current_24hr.day, current_24hr.hour,
                             tzinfo=datetime.timezone.utc)


async def get_nearest_weekly_interval() -> datetime.datetime:
    """
    Gets the nearest weekly interval from the current time
    :return: The nearest weekly interval
    """
    next_week = datetime.datetime.now(datetime.UTC) + datetime.timedelta(
        days=(7 - datetime.datetime.now(datetime.UTC).weekday()))
    sanic.log.logger.debug(f"Next week interval: {next_week}")
    return datetime.datetime(next_week.year, next_week.month, next_week.day, tzinfo=datetime.timezone.utc)


async def get_current_weekly_interval() -> datetime.datetime:
    """
    Gets the current weekly interval
    :return: The current weekly interval
    """
    current_week = datetime.datetime.now(datetime.UTC) - datetime.timedelta(
        days=datetime.datetime.now(datetime.UTC).weekday())
    sanic.log.logger.debug(f"Current week interval: {current_week}")
    return datetime.datetime(current_week.year, current_week.month, current_week.day, tzinfo=datetime.timezone.utc)


async def get_nearest_monthly_interval() -> datetime.datetime:
    """
    Gets the nearest monthly interval from the current time
    :return: The nearest monthly interval
    """
    next_month = datetime.datetime.now(datetime.UTC) + datetime.timedelta(
        days=(30 - (datetime.datetime.now(datetime.UTC).day % 30)))
    sanic.log.logger.debug(f"Next month interval: {next_month}")
    return datetime.datetime(next_month.year, next_month.month, 1, tzinfo=datetime.timezone.utc)


async def get_current_monthly_interval() -> datetime.datetime:
    """
    Gets the current monthly interval
    :return: The current monthly interval
    """
    current_month = datetime.datetime.now(datetime.UTC) - datetime.timedelta(
        days=datetime.datetime.now(datetime.UTC).day - 1)
    sanic.log.logger.debug(f"Current month interval: {current_month}")
    return datetime.datetime(current_month.year, current_month.month, 1, tzinfo=datetime.timezone.utc)


async def token_generator() -> str:
    """
    Generates 16 random bytes, converted to hex
    :return: The generated string
    """
    # return ''.join(random.choice(chars).lower() for _ in range(size))
    sanic.log.logger.debug("Generating random token")
    return uuid.UUID(bytes=random.randbytes(16)).hex


async def uuid_generator() -> str:
    """
    Generates a dash-less UUIDv4 string
    :return: The generated string
    """
    sanic.log.logger.debug("Generating random UUID")
    return uuid.uuid4().hex


async def generate_eg1(sub: Optional[str] = None, dn: Optional[str] = None, clid: Optional[str] = None,
                       dvid: Optional[str] = None) -> str:
    """
    Generates an eg1 JWT token for an account
    :param sub: The account id to generate the token for
    :param dn: The display name of the account
    :param clid: The client id of the account
    :param dvid: The device id of the account
    :return: The JWT token
    """
    sanic.log.logger.debug("Generating EG1 JWT token")
    if sub is None:
        raise errors.com.epicgames.bad_request(errorMessage="Account ID is required")
    if clid is None:
        clid = "3cf78cd3b00b439a8755a878b160c7ad"
    if dvid is None:
        dvid = await uuid_generator()
    p = f"wexp:cloudstorage:system=2,account:public:account:*=2,xmpp:session:*:{sub}=1,wexp:push:devices:{sub}=15," \
        f"account:oauth:exchangeTokenCode=15,account:public:account=2,priceengine:shared:offer:price=2," \
        f"wexp:wexp_role:client=15,account:public:account:externalAuths=15,wexp:calendar=2,blockList:{sub}=14," \
        f"account:token:otherSessionsForAccountClient=8,friends:{sub}=15," \
        f"account:token:otherSessionsForAccountClientService=8,wexp:profile:{sub}:*=15," \
        f"account:public:account:deviceAuths=11,wexp:cloudstorage:system:*=2,serviceinstance=2,wexp:storefront=2"
    headers = {"alg": "RS256", "kid": str(uuid.uuid4())}
    return jwt.encode({
        "sub": sub,
        "dvid": dvid,
        "mver": False,
        "clid": clid,
        "dn": dn,
        "am": "exchange_code",
        "p": base64.b64encode(zlib.compress(p.encode())).decode(),
        "iai": sub,
        "sec": 1,
        "clsvc": "wex",
        "t": "s",
        "ic": True,
        "exp": datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=8),
        "iat": datetime.datetime.now(datetime.UTC),
        "jti": await token_generator()
    }, private_key, "RS256", headers)


async def generate_client_eg1(clid: str) -> str:
    """
    Generates an eg1 JWT token for client credentials
    :param clid: The client id to generate the token for
    :return: The JWT token
    """
    sanic.log.logger.debug("Generating EG1 Client Credentials JWT token")
    headers = {"alg": "RS256", "kid": str(uuid.uuid4())}
    if clid in ["3cf78cd3b00b439a8755a878b160c7ad", "3cf78cd3b00b439a8755a878b160c7ad",
                "84cd036b576541e9ad1634c1448c0c30", "e645e4b96298419cbffbfa353ebf8b82",
                "66e03bfeb7db44adaca611dae2674094", "ec813099a59f48d4a338f1901c1609db",
                "016a103319b34d258c0e7d4d2760c985", "f8eac541a1c241939f76d26cf2a673a6"]:
        p = ("wexp:calendar=2,catalog:shared:offers=2,account:public:account:externalAuthOnly=1,"
             "wexp:cloudstorage:system=2,account:public:account=1,wexp:cloudstorage:system:*=2,"
             "affiliate:public:affiliate=2,wexp:storefront=2")
    elif clid == "8e873617d81d4caf89bae28a4b74bbfe":
        p = "account:public:account:externalAuthOnly=1,account:public:account=1"
    elif clid == "34a02cf8f4414e29b15921876da36f9a":
        p = "account:public:account:externalAuthOnly=1,account:public:account=1"  # TODO: add more permissions
    else:
        raise errors.com.epicgames.account.invalid_client_credentials()
    return jwt.encode({
        "p": base64.b64encode(zlib.compress(p.encode())).decode(),
        "clsvc": "wex",
        "t": "s",
        "mver": False,
        "clid": clid,
        "ic": True,
        "am": "client_credentials",
        "exp": datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=4),
        "iat": datetime.datetime.now(datetime.UTC),
        "jti": await token_generator()
    }, private_key, "RS256", headers)


async def generate_refresh_eg1(sub: Optional[str] = None, dn: Optional[str] = None, clid: Optional[str] = None,
                               dvid: Optional[str] = None) -> str:
    """
    Generates an eg1 JWT token for an account
    :param sub: The account id to generate the token for
    :param dn: The display name of the account
    :param clid: The client id of the account
    :param dvid: The device id of the account
    :return: The JWT token
    """
    sanic.log.logger.debug("Generating EG1 Refresh JWT token")
    if sub is None:
        raise errors.com.epicgames.bad_request(errorMessage="Account ID is required")
    if clid is None:
        clid = "3cf78cd3b00b439a8755a878b160c7ad"
    if dvid is None:
        dvid = await uuid_generator()
    headers = {"alg": "RS256", "kid": str(uuid.uuid4())}
    return jwt.encode({
        "sub": sub,
        "dvid": dvid,
        "t": "r",
        "clid": clid,
        "dn": dn,
        "exp": datetime.datetime.now(datetime.UTC) + datetime.timedelta(weeks=52),
        "am": "exchange_code",
        "jti": await token_generator()
    }, private_key, "RS256", headers)


async def generate_authorisation_eg1(sub: Optional[str] = None, dn: Optional[str] = None,
                                     clid: Optional[str] = None) -> str:
    """
    Generates an eg1 JWT token for an account to use as an auth code
    :param sub: The account id to generate the token for
    :param dn: The display name of the account
    :param clid: The client id of the account
    :return: The JWT token
    """
    sanic.log.logger.debug("Generating EG1 Authorisation JWT token")
    if sub is None:
        raise errors.com.epicgames.bad_request(errorMessage="Account ID is required")
    if clid is None:
        clid = "3cf78cd3b00b439a8755a878b160c7ad"
    headers = {"alg": "RS256", "kid": str(uuid.uuid4())}
    return jwt.encode({
        "sub": sub,
        "t": "r",
        "clid": clid,
        "dn": dn,
        "exp": datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=8),
        "am": "exchange_code",
        "jti": await token_generator()
    }, private_key, "RS256", headers)


async def parse_eg1(token: str) -> Optional[dict]:
    """
    Parses an eg1 JWT token
    :param token: The token to parse
    :return: The parsed token
    """
    sanic.log.logger.debug("Parsing EG1 JWT token")
    try:
        token = token.replace("bearer ", "").replace("eg1~", "")
        return jwt.decode(token, public_key, algorithms=["RS256"], leeway=20)
    except Exception as e:
        sanic.log.logger.warning(f"Failed to parse EG1 JWT token: {e}")
        return None


async def verify_google_token(token: str) -> Optional[dict]:
    """
    Verifies a Google token
    :param token: The token to verify
    :return: The token if verified, None otherwise
    """
    sanic.log.logger.debug("Verifying Google token")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://oauth2.googleapis.com/tokeninfo?id_token={token}") as r:
                if r.status != 200:
                    sanic.log.logger.warning(f"Failed to verify Google token: {r.status}")
                    return None
                sanic.log.logger.debug(f"Successfully verified Google token: {r.json()}")
                return await r.json()
    except Exception as e:
        sanic.log.logger.warning(f"Failed to verify Google token: {e}")
        return None


async def verify_owner(request: sanic.request.Request, token: dict) -> bool:
    """
    Verifies that the owner of the token is the owner of the account
    :param request: The request to verify
    :param token: The token to verify
    :return: True if the token is the owner of the account, False otherwise
    """
    sanic.log.logger.debug("Verifying owner of the token")
    account_id = request.match_info.get('accountId')
    if account_id is None:
        account_id = request.form.get("accountId")
    if account_id is None:
        account_id = request.args.get("accountId")
    if account_id is None:
        try:
            account_id = request.json.get("accountId")
        except:
            pass
    if account_id is None:
        sanic.log.logger.warning("Failed to verify owner of the token")
        return False
    if token.get("sub") != account_id:
        sanic.log.logger.warning("Owner of the token does not match the account ID")
        return False
    sanic.log.logger.debug("Successfully verified owner of the token")
    return True


async def verify_request_auth(request: sanic.request.Request, strict: bool = False) -> bool:
    """
    Verifies the authorisation of a request
    :param request: The request to verify
    :param strict: Whether to be strict about account id
    :return: True if the request is authorised, False otherwise
    """
    sanic.log.logger.debug("Verifying request authorisation")
    try:
        if request.headers.get("Authorization", "").startswith("bearer "):
            token = request.headers.get("Authorization", "").replace("bearer ", "").replace("eg1~", "")
            token = jwt.decode(token, public_key, algorithms=["RS256"], leeway=20)
            if token["jti"] in request.app.ctx.invalid_tokens:
                raise errors.com.epicgames.account.auth_token.unknown_oauth_session()
            if strict:
                if not (await verify_owner(request, token)):
                    raise errors.com.epicgames.account.token_account_id_does_not_match_url_accountId()
            else:
                request.ctx.is_owner = await verify_owner(request, token)
            request.ctx.owner = token.get("sub")
            request.ctx.dvid = token.get("dvid")
            sanic.log.logger.debug("Successfully verified request authorisation")
            return True
        else:
            sanic.log.logger.warning("No bearer token found in request")
            return False
    except Exception as e:
        if isinstance(e, errors.com.epicgames.account.auth_token.unknown_oauth_session):
            raise e
        elif isinstance(e, errors.com.epicgames.account.token_account_id_does_not_match_url_accountId):
            raise e
        sanic.log.logger.warning(f"Failed to verify request authorisation: {e}")
        return False


def admin_auth(maybe_func: Any = None) -> Callable:
    """
    Decorator to check if a request is authorized to perform an admin function
    :return: The decorator
    """

    def decorator(f: Callable) -> Callable:
        """
        The decorator
        :param f: The function to decorate
        :return: The decorated function
        """

        @functools.wraps(f)
        async def decorated_function(request: sanic.request.Request, *args,
                                     **kwargs) -> sanic.response.HTTPResponse | sanic.response.JSONResponse:
            """
            The decorated function

            :param request: The request object
            :param args: Arguments to pass to the function
            :param kwargs: Keyword arguments to pass to the function
            :return: The response
            """
            raise errors.com.epicgames.forbidden()

        return decorated_function

    return decorator(maybe_func) if maybe_func else decorator


def authorized(maybe_func: Any = None, *, allow_basic: bool = False, strict: bool = False) -> Callable:
    """
    Decorator to check if a request is authorized
    :return: The decorator
    """

    def decorator(f: Callable) -> Callable:
        """
        The decorator
        :param f: The function to decorate
        :return: The decorated function
        """

        @functools.wraps(f)
        async def decorated_function(request: sanic.request.Request, *args,
                                     **kwargs) -> sanic.response.HTTPResponse | sanic.response.JSONResponse:
            """
            The decorated function

            :param request: The request object
            :param args: Arguments to pass to the function
            :param kwargs: Keyword arguments to pass to the function
            :return: The response
            """
            sanic.log.logger.debug("Verifying request authorisation")
            if allow_basic:
                if request.headers.get("Authorization", "").startswith("basic "):
                    try:
                        token = request.headers.get("Authorization", "").replace("basic ", "")
                        token = base64.b64decode(token).decode()
                        if token[32] == ":":
                            is_authorised = True
                        else:
                            raise Exception()
                    except:
                        is_authorised = False
                else:
                    is_authorised = await verify_request_auth(request, strict)
            else:
                is_authorised = await verify_request_auth(request, strict)

            if is_authorised:
                # the user is authorised
                # run the handler method and return the response
                response = f(request, *args, **kwargs)
                if isawaitable(response):
                    response = await response
                return response
            else:
                # the user is not authorised
                raise errors.com.epicgames.account.oauth.expired_exchange_code()

        return decorated_function

    return decorator(maybe_func) if maybe_func else decorator


async def bcrypt_hash(s: str) -> bytes:
    """
    Hashes a string using bcrypt
    :param s: The string to hash
    :return: The hashed string
    """
    sanic.log.logger.debug("Hashing string")
    return bcrypt.hashpw(s.encode(), bcrypt.gensalt())


async def bcrypt_check(s: str, hashed: bytes) -> bool:
    """
    Checks if a string matches a bcrypt hash
    :param s: The string to check
    :param hashed: The hash to check against
    :return: True if the string matches the hash, False otherwise
    """
    sanic.log.logger.debug("Checking bcrypt hash")
    result = bcrypt.checkpw(s.encode(), hashed)
    sanic.log.logger.debug(f"Hash check result: {result}")
    return result


async def get_account_id_from_display_name(database: AsyncDatabase, display_name: str) -> Optional[str]:
    """
    Gets an account id from a display name
    :param database: The database to get the account id from
    :param display_name: The display name to get the account id for
    :return: The account id
    """
    sanic.log.logger.debug("Getting account id from display name")
    existing_account = await database["accounts"].find_one(
        {"displayName": {"$regex": f"^{re.escape(display_name)}$", "$options": "i"}},
        {"_id": 1}
    )
    sanic.log.logger.debug(f"Existing account id: {existing_account}")
    return existing_account.get("_id") if existing_account else None


async def get_account_id_from_email(database: AsyncDatabase, email: str) -> Optional[str]:
    """
    Gets an account id from an email
    :param database: The database to get the account id from
    :param email: The email to get the account id for
    :return: The account id
    """
    sanic.log.logger.debug("Getting account id from email")
    existing_account = await database["accounts"].find_one(
        {"email": {"$regex": f"^{re.escape(email)}$", "$options": "i"}},
        {"_id": 1}
    )
    sanic.log.logger.debug(f"Existing account id: {existing_account}")
    return existing_account.get("_id") if existing_account else None


async def search_for_display_name(database: AsyncDatabase, display_name: str) -> list[str]:
    """
    Searches for a display name
    :param database: The database to search
    :param display_name: The display name to search for
    :return: A list of account ids
    """
    sanic.log.logger.debug("Searching for display name")
    # ranked_accounts = []
    # async for entry in database["accounts"].find({}, {"_id": 1, "displayName": 1}):
    #     if not entry["displayName"]:
    #         continue
    #     similarity_ratio = difflib.SequenceMatcher(None, entry["displayName"], display_name).ratio()
    #     if similarity_ratio >= 0.4:
    #         ranked_accounts.append({"_id": entry["_id"], "similarity": similarity_ratio})
    # ranked_accounts.sort(key=lambda x: x["similarity"], reverse=True)
    # return [entry["_id"] for entry in ranked_accounts]
    display_names = []
    account_ids = []
    async for entry in database["accounts"].find({}, {"_id": 1, "displayName": 1}):
        if not entry["displayName"]:
            continue
        sanic.log.logger.debug(f"Found display name: {entry['displayName']}")
        display_names.append(entry["displayName"])
        account_ids.append(entry["_id"])
    ranked_accounts = rapidfuzz.process.extract(display_name, display_names, limit=10)
    sanic.log.logger.debug(f"Ranked accounts: {ranked_accounts}")
    return [account_ids[display_names.index(entry[0])] for entry in ranked_accounts]


async def check_if_display_name_exists(database: AsyncDatabase, display_name: str) -> bool:
    """
    Checks if a display name exists
    :param database: The database to check
    :param display_name: The display name to check
    :return: True if the display name exists, False otherwise
    """
    sanic.log.logger.debug("Checking if display name exists")
    existing_account = await database["accounts"].find_one(
        {"displayName": {"$regex": f"^{re.escape(display_name)}$", "$options": "i"}},
        {"_id": 1}
    )
    sanic.log.logger.debug(f"Existing account: {existing_account}")
    return existing_account is not None


async def get_account_data_owner(database: AsyncDatabase, account_id: str) -> Optional[dict]:
    """
    Gets account data from an account id
    :param database: The database to get the data from
    :param account_id: The account id to get the data for
    :return: The account data
    """
    sanic.log.logger.debug(f"Getting account data for {account_id} as owner")
    account_data = await database["accounts"].find_one({"_id": account_id}, {
        "displayName": 1,
        "email": 1,
        "lastLogin": 1,
        "headless": 1,
        "preferredLanguage": 1,
        "lastDisplayNameChange": 1,
        "tfaEnabled": 1,
        "externalAuths": 1
    })
    if not account_data:
        return None
    return {
        "id": account_data["_id"],
        "displayName": account_data["displayName"],
        "email": account_data["email"],
        "lastLogin": account_data["lastLogin"],
        "headless": account_data["headless"],
        "preferredLanguage": account_data["preferredLanguage"],
        "lastDisplayNameChange": account_data["lastDisplayNameChange"],
        "canUpdateDisplayName": (lambda v: (not v) or (
                (datetime.datetime.now(datetime.UTC) - (
                    (lambda d: d if d.tzinfo else d.replace(tzinfo=datetime.UTC))(
                        datetime.datetime.fromisoformat(v.replace('Z', '+00:00')) if isinstance(v, str) else v
                    )
                )).days >= 14
        ))(account_data.get("lastDisplayNameChange")),
        "tfaEnabled": account_data["tfaEnabled"],
        "externalAuths": account_data["externalAuths"],
        "failedLoginAttempts": 0,
        "numberOfDisplayNameChanges": 0,
        "dateOfBirth": "YYYY-MM-DD",
        "ageGroup": "UNKNOWN",
        "country": "AU",
        "name": "",
        "lastName": "",
        "phoneNumber": 0,
        "emailVerified": False,
        "minorExpected": False,
        "minorVerified": False,
        "minorStatus": "UNKNOWN",
        "cabinedMode": False,
        "hasHashedEmail": False
    }


async def get_account_data(database: AsyncDatabase, account_id: str) -> Optional[dict]:
    """
    Gets account data from an account id
    :param database: The database to get the data from
    :param account_id: The account id to get the data for
    :return: The account data
    """
    sanic.log.logger.debug(f"Getting account data for {account_id}")
    account_data = await database["accounts"].find_one({"_id": account_id}, {
        "displayName": 1,
        "externalAuths": 1
    })
    return {
        "id": account_data["_id"],
        "displayName": account_data["displayName"],
        "externalAuths": account_data["externalAuths"]
    }


async def oauth_response(client_id: str = "3cf78cd3b00b439a8755a878b160c7ad", dn: Optional[str] = None,
                         dvid: Optional[str] = None, sub: Optional[str] = None) -> dict:
    """
    Generates an oauth response
    :param client_id: The client id
    :param dn: The display name
    :param dvid: The device id
    :param sub: The account ID
    :return: The oauth response
    """
    sanic.log.logger.debug("Generating oauth response")
    return {
        "access_token": f"eg1~{await generate_eg1(sub, dn, client_id, dvid)}",
        "expires_in": 28800,
        "expires_at": (datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=8)).strftime("%Y-%m-%dT%H:%M"
                                                                                                   ":%S.000Z"),
        "token_type": "bearer",
        "refresh_token": f"eg1~{await generate_refresh_eg1(sub, dn, client_id, dvid)}",
        "refresh_expires": 31449600,
        "refresh_expires_at": await format_time(datetime.datetime.now(datetime.UTC) + datetime.timedelta(weeks=52)),
        "account_id": sub,
        "client_id": client_id,
        "internal_client": True,
        "client_service": "wex",
        "displayName": dn,
        "app": "wex",
        "in_app_id": sub,  # backwards compatability with soft-launch wex clients (circa 2017)
        "device_id": dvid
    }


async def oauth_client_response(client_id: str) -> dict:
    """
    Generates an oauth response for a client
    :param client_id: The client id
    :return: The oauth response
    """
    sanic.log.logger.debug("Generating oauth client response")
    return {
        "access_token": f"eg1~{await generate_client_eg1(client_id)}",
        "expires_in": 14400,
        "expires_at": await format_time(datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=4)),
        "token_type": "bearer",
        "client_id": client_id,
        "internal_client": True,
        "client_service": "wex",
        "scope": [],
        "app": "wex"
    }


async def create_account(database: AsyncDatabase, displayName: Optional[str] = None,
                         password: Optional[bytes] = None, email: Optional[str] = None,
                         calendar=None) -> str:
    """
    Creates an account and prepares all the files
    :param database: The database to create the account in
    :param displayName: The display name
    :param password: The password hash
    :param email: The email
    :param calendar: The calendar class
    :return: The account id
    """
    sanic.log.logger.debug("Creating an account")
    from utils.account_initialisation import initialise_account
    account_id = await initialise_account(database, await uuid_generator(), displayName, password, email, calendar)
    return account_id


async def normalise_string(input_string: Optional[str]) -> Optional[str]:
    """
    Normalises a string
    :param input_string: The string to normalise
    :return: The normalised string
    """
    if input_string is not None:
        normalised_string = ''.join(char.upper() for char in input_string if char.isalpha())
        sanic.log.logger.debug(f"Normalised string from {input_string} to {normalised_string}")
        return normalised_string
    return ""


@alru_cache()
async def load_datatable(datatable: Optional[str]) -> Optional[dict | list]:
    """
    Loads a datatable. As datatables are both static and large, this could be cached
    :param datatable: The datatable path to load
    :return: The datatable
    """
    sanic.log.logger.debug(f"Loading datatable {datatable}")
    if datatable is not None:
        return await read_file(f"res/battle-breakers-data/WorldExplorers/{datatable}.json")
    return None


@alru_cache()
async def get_template_id_from_path(path: Optional[str]) -> Optional[str]:
    """
    Gets a template id from a path
    :param path: The path to get the template id for
    :return: The template id
    """
    sanic.log.logger.debug(f"Getting template id from path {path}")
    if path is not None:
        # I hope you love this, remaps paths from old versions to new versions
        if path in ['/Game/Loot/AccountItems/Vouchers/Voucher_HeroSilver.Voucher_HeroSilver',
                    '/Game/Loot/AccountItems/Reagents/Reagent_Hero_Silver.Reagent_Hero_Silver',
                    '/Game/Loot/AccountItems/Reagents/Reagent_Hero_Gold.Reagent_Hero_Gold',
                    '/Game/Loot/AccountItems/Reagents/Reagent_Hero_Diamond.Reagent_Hero_Diamond',
                    '/Game/Loot/AccountItems/Vouchers/Voucher_HeroBronze.Voucher_HeroBronze',
                    '/Game/Loot/AccountItems/Tokens/TK_Voucher_HeroSilver.TK_Voucher_HeroSilver',
                    '/Game/Loot/AccountItems/Tokens/TK_Voucher_HeroGold.TK_Voucher_HeroGold']:
            path = '/Game/Loot/AccountItems/Tokens/TK_HeroMap_Elemental.TK_HeroMap_Elemental'
        elif path == '/Game/Loot/AccountItems/Reagents/Reagent_Hero_Diamond.Reagent_Hero_Diamond':
            path = '/Game/Loot/AccountItems/Tokens/TK_HeroMap_SuperRare.TK_HeroMap_SuperRare'
        elif path == '/Game/Loot/AccountItems/TreasureMaps/TM_PortalResource.TM_PortalResource':
            path = '/Game/Loot/AccountItems/TreasureMaps/TM_MapResource.TM_MapResource'
        elif path in ['/Game/Loot/AccountItems/Reagents/Reagent_Dark_T05.Reagent_Dark_T05',
                      '/Game/Loot/AccountItems/Reagents/Reagent_Dark_T04.Reagent_Dark_T04']:
            path = '/Game/Loot/AccountItems/Reagents/Reagent_Shard_Dark.Reagent_Shard_Dark'
        elif path in ['/Game/Loot/AccountItems/Reagents/Reagent_Fire_T05.Reagent_Fire_T05',
                      '/Game/Loot/AccountItems/Reagents/Reagent_Fire_T04.Reagent_Fire_T04']:
            path = '/Game/Loot/AccountItems/Reagents/Reagent_Shard_Fire.Reagent_Shard_Fire'
        elif path in ['/Game/Loot/AccountItems/Reagents/Reagent_Light_T05.Reagent_Light_T05',
                      '/Game/Loot/AccountItems/Reagents/Reagent_Light_T04.Reagent_Light_T04']:
            path = '/Game/Loot/AccountItems/Reagents/Reagent_Shard_Light.Reagent_Shard_Light'
        elif path in ['/Game/Loot/AccountItems/Reagents/Reagent_Nature_T05.Reagent_Nature_T05',
                      '/Game/Loot/AccountItems/Reagents/Reagent_Nature_T04.Reagent_Nature_T04']:
            path = '/Game/Loot/AccountItems/Reagents/Reagent_Shard_Nature.Reagent_Shard_Nature'
        elif path in ['/Game/Loot/AccountItems/Reagents/Reagent_Water_T05.Reagent_Water_T05',
                      '/Game/Loot/AccountItems/Reagents/Reagent_Water_T04.Reagent_Water_T04']:
            path = '/Game/Loot/AccountItems/Reagents/Reagent_Shard_Water.Reagent_Shard_Water'
        elif path == '/Game/Loot/AccountItems/Ore/Ore_CrystalShard.Ore_CrystalShard':
            path = '/Game/Loot/AccountItems/Ore/Ore_Magicite.Ore_Magicite'
        path = path.replace("/Game", "WorldExplorers/Content").split(".")[0].replace("WorldExplorers/",
                                                                                     "res/battle-breakers-data/WorldExplorers/")
        data = await read_file(f"{path}.json")
        sanic.log.logger.debug(f"Found data for item with type {data[0].get('Type')}")
        match data[0].get('Type'):
            case "WExpGenericAccountItemDefinition":
                sanic.log.logger.debug(
                    f"Returning {data[0].get('Properties').get('ItemType').split('::')[-1]}:{data[0].get('Name')}")
                return f"{data[0].get('Properties').get('ItemType').split('::')[-1]}:{data[0].get('Name')}"
            case "WExpCharacterDefinition":
                sanic.log.logger.debug(f"Returning Character:{data[0].get('Name').split('CD_')[-1]}")
                return f"Character:{data[0].get('Name').split('CD_')[-1]}"
            case "WExpVoucherItemDefinition":
                return f"Voucher:{data[0].get('Name')}"
            case "WExpUpgradePotionDefinition":
                return f"UpgradePotion:{data[0].get('Name')}"
            case "WExpXpBookDefinition":
                return "Currency:HeroXp_Basic"  # hardcoded as in newer versions, all xp books are one type, otherwise it would be "XpBook:{name}"
            case "WExpTreasureMapDefinition":
                return f"TreasureMap:{data[0].get('Name')}"
            case "WExpTokenDefinition":
                return f"Token:{data[0].get('Name')}"
            case "WExpAccountRewardDefinition":
                return f"AccountReward:{data[0].get('Name')}"
            case "WExpContainerDefinition":
                return f"Container:{data[0].get('Name')}"
            case "WExpGearAffix":
                return f"GearAffix:{data[0].get('Name')}"
            case "WExpGearAccountItemDefinition":
                return f"Gear:{data[0].get('Name')}"
            case "WExpQuestDefinition":
                return f"Quest:{data[0].get('Name')}"
            case "WExpHQMonsterPitDefinition":
                return f"HqBuilding:{data[0].get('Name')}"
            case "WExpHQWorkshopDefinition":
                return f"HqBuilding:{data[0].get('Name')}"
            case "WExpHQBlacksmithDefinition":
                return f"HqBuilding:{data[0].get('Name')}"
            case "WExpHQMineDefinition":
                return f"HqBuilding:{data[0].get('Name')}"
            case "WExpHQHeroTowerDefinition":
                return f"HqBuilding:{data[0].get('Name')}"
            case "WExpHQMarketDefinition":
                return f"HqBuilding:{data[0].get('Name')}"
            case "WExpHQSecretShopDefinition":
                return f"HqBuilding:{data[0].get('Name')}"
            case "WExpHQSmelterDefinition":
                return f"HqBuilding:{data[0].get('Name')}"
            case "WExpHQWorkerLodgesDefinition":
                return f"HqBuilding:{data[0].get('Name')}"
            case "WExpItemDefinition":
                return f"Item:{data[0].get('Name')}"
            case "WExpLTMItemDefinition":
                return f"LTM:{data[0].get('Name')}"
            case "WExpMajorEventTrackerDefinition":
                return f"MajorEventTracker:{data[0].get('Name')}"
            case "WExpMenuData":
                return f"Menu:{data[0].get('Name')}"
            case "WExpPromotionTable":
                return f"PromotionTable:{data[0].get('Name')}"
            case "WExpPersonalEventDefinition":
                return f"PersonalEvent:{data[0].get('Name')}"
            case "WExpRecipe":
                return f"Recipe:{data[0].get('Name')}"
            case "WExpStandInDefinition":
                return f"StandIn:{data[0].get('Name')}"
            case "WExpUpgradePotionDefinition":
                return f"UpgradePotion:{data[0].get('Name')}"
            case "WExpUnlockableDefinition":
                return f"Unlockable:{data[0].get('Name')}"
            case "WExpVoucherItemDefinition":
                return f"Voucher:{data[0].get('Name')}"
            case "WExpHeroChestDefinition":
                return f"HeroChest:{data[0].get('Name')}"
            case "WExpGiftboxDefinition":
                return f"Giftbox:{data[0].get('Name')}"
            case "WExpHammerChestDefinition":
                return f"HammerChest:{data[0].get('Name')}"
            case _:
                return f"{data[0].get('Type')}:{data[0].get('Name')}"
    sanic.log.logger.debug(f"Failed to match template id from path {path}")
    return None


async def find_best_match(input_str: str, item_list: list, split_for_path: bool = False) -> str:
    """
    Finds the best match for a string in a list
    :param input_str: The string to find the best match for
    :param item_list: The list to find the best match in
    :param split_for_path: Whether to split the string for the path
    :return: The best match
    """
    sanic.log.logger.debug(f"Finding best match for {input_str} in list of {len(item_list)} items")
    # best_match = ""
    # best_match_score = 0
    # for item in item_list:
    #     if split_for_path:
    #         score = difflib.SequenceMatcher(None, input_str, item.split("\\")[-1].split(".")[0]).ratio()
    #     else:
    #         score = difflib.SequenceMatcher(None, input_str, item).ratio()
    #     if score > best_match_score:
    #         best_match_score = score
    #         best_match = item
    #     # if score >= 0.95:
    #     #     break
    # print(f"Found best match for {input_str} as {best_match} with score {best_match_score}")
    # return best_match
    if split_for_path:
        result = rapidfuzz.process.extractOne(input_str, item_list, processor=lambda x: x.split("\\")[-1].split(".")[0])
    else:
        result = rapidfuzz.process.extractOne(input_str, item_list)
    sanic.log.logger.debug(f"Found best match for {input_str} as {result[0]} with score {result[1]}")
    return result[0]


@alru_cache(maxsize=256)
async def get_path_from_template_id(template_id: str) -> str:
    """
    Gets the path from a template id
    :param template_id: The template id to get the path for
    :return: The path
    """
    sanic.log.logger.debug(f"Getting path from template id {template_id}")
    if template_id is not None:
        best_match = await find_best_match(template_id, game_files_list, True)
        return best_match
    else:
        sanic.log.logger.debug("No template id provided")
        raise errors.com.epicgames.bad_request(errorMessage="Template ID is required")


@alru_cache(maxsize=32)
async def extract_version_info(user_agent: str) -> Tuple[int, int, int]:
    """
    Extracts the version info from a user agent
    :param user_agent: The user agent to extract the version info from
    :return: The version info as a tuple of (minor_version, revision, changelist)
    """
    sanic.log.logger.debug(f"Extracting version info from user agent {user_agent}")
    modern_version_regex = r"1\.(\d*)\.(\d*)-r(\d*)"
    legacy_version_regex = r"-(\d*)\+\+\+WEX\+Release-1\.(\d*)"
    ultra_legacy_version_regex = r"-(\d*)\+\+\+WEX\+Release-(\d*)"
    ultra_legacy_version_regex_2 = r"Release-(\d*)-CL-(\d*)"
    match = re.search(modern_version_regex, user_agent)
    if match:
        minor_version = int(match.group(1))
        revision = int(match.group(2))
        changelist = int(match.group(3))
        sanic.log.logger.debug(f"Returning version info: {minor_version}, {revision}, {changelist}")
        return minor_version, revision, changelist
    match = re.search(legacy_version_regex, user_agent)
    if match:
        minor_version = int(match.group(2))
        revision = 0
        changelist = int(match.group(1))
        sanic.log.logger.debug(f"Returning version info: {minor_version}, {revision}, {changelist}")
        return minor_version, revision, changelist
    match = re.search(ultra_legacy_version_regex, user_agent)
    if match:
        minor_version = 0
        revision = int(match.group(2))
        changelist = int(match.group(1))
        sanic.log.logger.debug(f"Returning version info: {minor_version}, {revision}, {changelist}")
        return minor_version, revision, changelist
    match = re.search(ultra_legacy_version_regex_2, user_agent)
    if match:
        minor_version = 0
        revision = int(match.group(1))
        changelist = int(match.group(2))
        sanic.log.logger.debug(f"Returning version info: {minor_version}, {revision}, {changelist}")
        return minor_version, revision, changelist
    sanic.log.logger.debug("No match found, returning default version info")
    return 88, 244, 17036752  # Default values if no match is found


async def room_generator(level_id: str, level_info: dict) -> list:
    """
    Generates rooms for a level for levels where data is unavailable
    :param level_id: The level id to generate the rooms for
    :param level_info: The level info from the datatable
    :return: The generated rooms as a list to include in the level notification response
    """
    sanic.log.logger.debug(f"Generating rooms for level {level_id}")
    rooms_count = level_info.get("NumExpectedRooms", 1)
    room_info = (await load_datatable("Content/World/Datatables/LevelRooms"))[0]["Rows"]
    room = {
        "roomName": "Room.Standard.FindExit.Easy.R01",
        "regionName": level_id,
        "depth": 1,
        "worldLevel": int(random.randint(
            int(level_info["BaseWorldLevel"] * 0.92),
            int(level_info["BaseWorldLevel"] * 1.09)
        )),
        "discoveryGoldMult": 1.0,
        "occupants": [{
            "isFriendly": False,
            "killXp": 0,
            "lootTemplateId": "Currency:Gold",
            "lootQuantity": 150
        }]
    }
    return [room]


@alru_cache(maxsize=256)
async def load_character_data(character_id: str) -> dict:
    """
    Loads character data from the datatable
    :param character_id: The character id to load
    :return: The character data as a dict
    """
    sanic.log.logger.debug(f"Loading character data for {character_id}")
    if not character_id.startswith("Character:"):
        raise errors.com.epicgames.world_explorers.bad_request(errorMessage="Invalid character id")
    character_id = character_id.replace("Character:", "CD_")
    best_match = await find_best_match(character_id, character_files_list, True)
    return await load_datatable(
        best_match.replace("res/battle-breakers-data/WorldExplorers/", "").replace(".json", "").replace("\\", "/"))


async def get_curvetable_value(data_table: list[dict], row: str, time_input: float = 0) -> float:
    """
    Gets a value from a curvetable
    :param data_table: The curvetable to get the value from
    :param row: The row to get the value from
    :param time_input: The time to get the value from
    :return: The value from the curvetable
    """
    sanic.log.logger.debug(f"Getting curvetable value for row {row} at time {time_input}")
    row_data = data_table[0]['Rows'][row]
    # ROOT[0].Rows.Default_C_T01.Keys[0].Time
    # clamp to lower bound.
    if time_input < row_data['Keys'][0]['Time']:
        sanic.log.logger.debug(f"Clamping to lower bound, returning {row_data['Keys'][0]['Value']}")
        return row_data['Keys'][0]['Value']

    # clamp to upper bound.
    if time_input >= row_data['Keys'][-1]['Time']:
        sanic.log.logger.debug(f"Clamping to upper bound, returning {row_data['Keys'][-1]['Value']}")
        return row_data['Keys'][-1]['Value']

    # find the two keys that the time_input is between.
    for i in range(len(row_data['Keys']) - 1):
        if row_data['Keys'][i]['Time'] <= time_input < row_data['Keys'][i + 1]['Time']:
            # interpolate between the two keys.
            result = row_data['Keys'][i]['Value'] + (time_input - row_data['Keys'][i]['Time']) / (
                    row_data['Keys'][i + 1]['Time'] - row_data['Keys'][i]['Time']) * (
                             row_data['Keys'][i + 1]['Value'] - row_data['Keys'][i]['Value'])
            sanic.log.logger.debug(f"Interpolated value, returning {result}")
            return result
    sanic.log.logger.debug("No keys found, returning 0")
    return 0


async def calculate_streakbreaker(current_streakbreaker: int, max_streakbreaker: int = 100000,
                                  base_chance: int = 10) -> tuple[bool, int]:
    """
    Calculates a streakbreaker roll
    :param current_streakbreaker: The current streakbreaker value
    :param max_streakbreaker: The maximum streakbreaker value
    :param base_chance: The base chance for the roll
    :return: A tuple of whether the roll succeeded and the new streakbreaker value
    """
    sanic.log.logger.debug(f"Calculating streakbreaker with current {current_streakbreaker}, max {max_streakbreaker}, "
                           f"base chance {base_chance}")
    calculated_probability = (1 / base_chance) + (1 - (1 / base_chance)) / (
            1 + ((max_streakbreaker / current_streakbreaker) if current_streakbreaker else 1) ** 2)
    roll = random.random()
    if roll < calculated_probability:
        sanic.log.logger.debug(f"Streakbreaker succeeded with roll {roll} and probability {calculated_probability}")
        return True, 0
    else:
        sanic.log.logger.debug(f"Streakbreaker failed with roll {roll} and probability {calculated_probability}")
        return False, current_streakbreaker + random.randint(5000, 10000)


async def replace_nth_occurrence(input_string: str, target_string: str, occurrence: int,
                                 replacement_string: str) -> str:
    """
    Replaces the nth occurrence of a string in a string with another string
    :param input_string: The input string to replace in
    :param target_string: The string to replace
    :param occurrence: The occurrence to replace
    :param replacement_string: The string to replace with
    :return: The replaced string
    """
    sanic.log.logger.debug(f"Replacing {occurrence} occurrence of {target_string} in {input_string} with "
                           f"{replacement_string}")
    new_string = input_string
    occurrence_count = 0
    for i in range(len(input_string)):
        if input_string[i:].startswith(target_string):
            occurrence_count += 1
            if occurrence_count == occurrence:
                new_string = input_string[:i] + replacement_string + input_string[i + len(target_string):]
                break
    sanic.log.logger.debug(f"Replaced string: {new_string}")
    return new_string


async def process_choices(input_data: str | int | float | list[
    str | int | float | dict[str, str | int | float | list[int | float]] | list]) -> str | int | float | dict[
    str, str | int | float | list[int | float]] | list[str | int | float | dict[
    str, str | int | float | list[int | float]]]:
    """
    Depending on the input data, this function will return either a random range between two values, a random choice from a list, or the input data.
    
    If the input data is a list of two ints or floats, it will return a random int or float between the two values.
    If the input data is a list of any other type or length, it will return a random choice from the list.
    If the input data is any other type, it will return the input data.
    :param input_data: The input to process
    :return: The processed input
    """
    if isinstance(input_data, list):
        if len(input_data) == 2 and all(isinstance(x, (int, float)) for x in input_data):
            if all(isinstance(x, int) for x in input_data):
                return random.randint(input_data[0], input_data[1])
            return random.uniform(input_data[0], input_data[1])
        return random.choice(input_data)
    return input_data


async def calculate_hero_power(hero_data: dict, add_pit_bonus: bool = False) -> float:
    """
    Calculates the hero power
    :param hero_data: The hero data to calculate the power for
    :param add_pit_bonus: Whether to add the pit bonus to the power
    :return: The hero power
    """
    sanic.log.logger.debug(
        f"Calculating hero power for {hero_data.get('templateId')} at level {hero_data['attributes'].get('level')}")
    power = 0
    character_stats_handle = \
        (await load_character_data(hero_data["templateId"]))[0]["Properties"]["CharacterStatsHandle"]["RowName"]
    character_stats = (await load_datatable("Content/Characters/Datatables/CharacterStats"))[0]["Rows"][
        character_stats_handle]
    power_budget_mult = await get_curvetable_value((await load_datatable("Content/Characters/Datatables/StatScaling")),
                                                   "PowerBudgetMult", hero_data["attributes"]["level"])
    power += power_budget_mult * character_stats["BudgetPoints"]
    for i in range(len(hero_data["attributes"]["upgrades"])):
        power += hero_data["attributes"]["upgrades"][i] * [50, 25, 50, 25, 9, 25, 500, 25, 500][i]
    if add_pit_bonus:
        power += character_stats["MonsterPitBonusPower"]
        if hero_data["attributes"]["foil_lvl"] > 0:
            power += character_stats["MonsterPitFoilBonusPower"]
    sanic.log.logger.debug(f"Calculated hero power: {power}")
    return power


async def safe_path_join(base_path: str, unsafe_path: str, verbose: bool = False) -> str:
    """
    Joins two paths safely and ensures the resulting path is within the base path.
    :param base_path: The base path
    :param unsafe_path: The path to be joined to the base one
    :param verbose: Whether to include paths in the ValueError or not
    :return: The joined output path
    """
    # Join the base path with the unsafe path
    combined_path = os.path.join(base_path, unsafe_path)

    # Get the real (absolute) path, resolving symbolic links and relative paths
    real_path = os.path.realpath(combined_path)

    # Ensure the real path is within the base path
    if not real_path.startswith(os.path.realpath(base_path)):
        # If the final path is outside the base path, raise an error
        if verbose:
            raise ValueError(
                f"Path traversal attempt detected! The unsafe path '{unsafe_path}' leads outside of the base path '{base_path}'")
        else:
            raise ValueError("Path traversal attempt detected!")

    return real_path


async def deterministic_shuffle(item_pool: list, item_count: Optional[int] = -1, weights: Optional[list] = None,
                                rng_seed: Optional[int] = None) -> list:
    """
    Shuffles a list deterministically, to create storefronts that only change on refresh, and will remain consistent across reboots and instances
    :param item_pool: The list to shuffle
    :param item_count: The number of items to shuffle
    :param weights: The weights for each item in the item pool. By default this is uniform
    :param rng_seed: The seed to use for the shuffle. By default this will only change output daily at UTC 0
    :return: The shuffled list
    """
    if rng_seed is None:
        rng_seed = int(datetime.datetime.now(datetime.UTC).strftime("%Y%m%d"))
    generator = numpy.random.default_rng(rng_seed)
    if weights is None:
        weights = [1 / len(item_pool) for _ in item_pool]
    if item_count == -1:
        item_count = len(item_pool)
    selected_items = generator.choice(item_pool, item_count, p=weights, replace=False)
    return selected_items.tolist()

async def reward_for_level(level: int):
    """
    Return reward string for a given level.
    Returns None if level is outside reward range (here: <2 or >999).
    The cycle above is a 20-slot template inferred from your sample data.
    """
    level_cycle = await read_file("res/wex/api/game/v2/balance/perk_cycle.json")
    if level < 2 or level > 999:
        return None
    if level == 984:
        return "ATK_PET"
    if level == 986:
        return "ATK_DEF"
    if level == 999:
        return "Basic_Special"
    idx = (level - 1) % 40   # map level to index in the 20-slot cycle
    return level_cycle[idx]
