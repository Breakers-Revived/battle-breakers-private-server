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
import motor.core
import motor.motor_asyncio
import orjson
import rapidfuzz.process
import sanic
import aiofiles

from async_lru import alru_cache

from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key
from cryptography.hazmat.backends import default_backend

from utils.exceptions import errors

# Load the private key
with open('utils/crypto/bb_private_key.pem', 'rb') as f:
    private_key_data = f.read()
    private_key = load_pem_private_key(private_key_data, password=b'wex_dippy_server', backend=default_backend())

with open('utils/crypto/bb_public_key.pem', 'rb') as f:
    public_key_data = f.read()
    public_key = load_pem_public_key(public_key_data, backend=default_backend())

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
    if json:
        async with aiofiles.open(filename, "rb") as file:
            return orjson.loads((await file.read()))
    if raw:
        async with aiofiles.open(filename, "rb") as file:
            return await file.read()
    async with aiofiles.open(filename, "r") as file:
        return await file.read()


async def write_file(filename: str, contents: Any, json: bool = True, raw: bool = True) -> None:
    """
    Writes to a file
    :param filename: The file to write to
    :param contents: The contents to write
    :param json: Whether to write the contents as json
    :param raw: Whether to write the contents as bytes
    """
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
    if time is None:
        return datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    else:
        if isinstance(time, datetime.datetime):
            return time.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
        # elif isinstance(time, float) or isinstance(time, int):
        #     return datetime.datetime.fromtimestamp(time).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
        elif isinstance(time, str):
            return datetime.datetime.fromisoformat(time).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
        else:
            return datetime.datetime.fromtimestamp(time).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


async def get_nearest_12_hour_interval() -> datetime.datetime:
    """
    Gets the nearest 12 hour interval from the current time
    :return:
    """
    next_12hr = datetime.datetime.now(datetime.UTC) + datetime.timedelta(
        hours=12 - (datetime.datetime.now(datetime.UTC).hour % 12))
    return datetime.datetime(next_12hr.year, next_12hr.month, next_12hr.day, next_12hr.hour,
                             tzinfo=datetime.timezone.utc)


async def get_current_12_hour_interval() -> datetime.datetime:
    """
    Gets the current 12 hour interval
    :return:
    """
    current_12hr = datetime.datetime.now(datetime.UTC) - datetime.timedelta(
        hours=datetime.datetime.now(datetime.UTC).hour % 12)
    return datetime.datetime(current_12hr.year, current_12hr.month, current_12hr.day, current_12hr.hour,
                             tzinfo=datetime.timezone.utc)


async def token_generator() -> str:
    """
    Generates 16 random bytes, converted to hex
    :return: The generated string
    """
    # return ''.join(random.choice(chars).lower() for _ in range(size))
    return uuid.UUID(bytes=random.randbytes(16)).hex


async def uuid_generator() -> str:
    """
    Generates a dash-less UUIDv4 string
    :return: The generated string
    """
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
        "exp": datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=672),
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
    try:
        token = token.replace("bearer ", "").replace("eg1~", "")
        return jwt.decode(token, public_key, algorithms=["RS256"], leeway=20)
    except:
        return None


async def verify_google_token(token: str) -> Optional[dict]:
    """
    Verifies a Google token
    :param token: The token to verify
    :return: The token if verified, None otherwise
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://oauth2.googleapis.com/tokeninfo?id_token={token}") as r:
                if r.status != 200:
                    return None
                return await r.json()
    except:
        return None


async def verify_owner(request: sanic.request.Request, token: dict) -> bool:
    """
    Verifies that the owner of the token is the owner of the account
    :param request: The request to verify
    :param token: The token to verify
    :return: True if the token is the owner of the account, False otherwise
    """
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
        return False
    if token.get("sub") != account_id:
        return False
    return True


async def verify_request_auth(request: sanic.request.Request, strict: bool = False) -> bool:
    """
    Verifies the authorisation of a request
    :param request: The request to verify
    :param strict: Whether to be strict about account id
    :return: True if the request is authorised, False otherwise
    """
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
            return True
        else:
            return False
    except Exception as e:
        if isinstance(e, errors.com.epicgames.account.auth_token.unknown_oauth_session):
            raise e
        elif isinstance(e, errors.com.epicgames.account.token_account_id_does_not_match_url_accountId):
            raise e
        return False


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


async def to_insecure_hash(s: str) -> int:
    """
    Hashes a string
    :param s: The string to hash
    :return: The hash of the string as an integer
    """
    hash_val = 0
    for c in s:
        hash_val = ((hash_val << 5) - hash_val) + ord(c)
        hash_val &= 0xffffffff  # Convert to 32-bit integer
    return hash_val


async def bcrypt_hash(s: str) -> bytes:
    """
    Hashes a string using bcrypt
    :param s: The string to hash
    :return: The hashed string
    """
    return bcrypt.hashpw(s.encode(), bcrypt.gensalt())


async def bcrypt_check(s: str, hashed: bytes) -> bool:
    """
    Checks if a string matches a bcrypt hash
    :param s: The string to check
    :param hashed: The hash to check against
    :return: True if the string matches the hash, False otherwise
    """
    return bcrypt.checkpw(s.encode(), hashed)


async def get_account_id_from_display_name(database: motor.core.AgnosticDatabase, display_name: str) -> Optional[str]:
    """
    Gets an account id from a display name
    :param database: The database to get the account id from
    :param display_name: The display name to get the account id for
    :return: The account id
    """
    existing_account = await database["accounts"].find_one(
        {"displayName": {"$regex": f"^{re.escape(display_name)}$", "$options": "i"}},
        {"_id": 1}
    )
    return existing_account.get("_id") if existing_account else None


async def get_account_id_from_email(database: motor.core.AgnosticDatabase, email: str) -> Optional[str]:
    """
    Gets an account id from an email
    :param database: The database to get the account id from
    :param email: The email to get the account id for
    :return: The account id
    """
    existing_account = await database["accounts"].find_one(
        {"email": {"$regex": f"^{re.escape(email)}$", "$options": "i"}},
        {"_id": 1}
    )
    return existing_account.get("_id") if existing_account else None


async def search_for_display_name(database: motor.core.AgnosticDatabase, display_name: str) -> list[str]:
    """
    Searches for a display name
    :param database: The database to search
    :param display_name: The display name to search for
    :return: A list of account ids
    """
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
        display_names.append(entry["displayName"])
        account_ids.append(entry["_id"])
    ranked_accounts = rapidfuzz.process.extract(display_name, display_names, limit=10)
    return [account_ids[display_names.index(entry[0])] for entry in ranked_accounts]


async def check_if_display_name_exists(database: motor.core.AgnosticDatabase, display_name: str) -> bool:
    """
    Checks if a display name exists
    :param database: The database to check
    :param display_name: The display name to check
    :return: True if the display name exists, False otherwise
    """
    existing_account = await database["accounts"].find_one(
        {"displayName": {"$regex": f"^{re.escape(display_name)}$", "$options": "i"}},
        {"_id": 1}
    )
    return existing_account is not None


async def get_account_data_owner(database: motor.core.AgnosticDatabase, account_id: str) -> Optional[dict]:
    """
    Gets account data from an account id
    :param database: The database to get the data from
    :param account_id: The account id to get the data for
    :return: The account data
    """
    account_data = await database["accounts"].find_one({"_id": account_id}, {
        "displayName": 1,
        "minorVerified": 1,
        "minorStatus": 1,
        "cabinedMode": 1,
        "name": 1,
        "email": 1,
        "failedLoginAttempts": 1,
        "lastLogin": 1,
        "numberOfDisplayNameChanges": 1,
        "dateOfBirth": 1,
        "ageGroup": 1,
        "headless": 1,
        "country": 1,
        "lastName": 1,
        "phoneNumber": 1,
        "preferredLanguage": 1,
        "lastDisplayNameChange": 1,
        "canUpdateDisplayName": 1,
        "tfaEnabled": 1,
        "emailVerified": 1,
        "minorExpected": 1,
        "hasHashedEmail": 1,
        "externalAuths": 1
    })
    if not account_data:
        return None
    return {
        "id": account_data["_id"],
        "displayName": account_data["displayName"],
        "minorVerified": account_data["minorVerified"],
        "minorStatus": account_data["minorStatus"],
        "cabinedMode": account_data["cabinedMode"],
        "name": account_data["name"],
        "email": account_data["email"],
        "failedLoginAttempts": account_data["failedLoginAttempts"],
        "lastLogin": account_data["lastLogin"],
        "numberOfDisplayNameChanges": account_data["numberOfDisplayNameChanges"],
        "dateOfBirth": account_data["dateOfBirth"],
        "ageGroup": account_data["ageGroup"],
        "headless": account_data["headless"],
        "country": account_data["country"],
        "lastName": account_data["lastName"],
        "phoneNumber": account_data["phoneNumber"],
        "preferredLanguage": account_data["preferredLanguage"],
        "lastDisplayNameChange": account_data["lastDisplayNameChange"],
        "canUpdateDisplayName": account_data["canUpdateDisplayName"],
        "tfaEnabled": account_data["tfaEnabled"],
        "emailVerified": account_data["emailVerified"],
        "minorExpected": account_data["minorExpected"],
        "hasHashedEmail": account_data["hasHashedEmail"],
        "externalAuths": account_data["externalAuths"]
    }


async def get_account_data(database: motor.core.AgnosticDatabase, account_id: str) -> Optional[dict]:
    """
    Gets account data from an account id
    :param database: The database to get the data from
    :param account_id: The account id to get the data for
    :return: The account data
    """
    account_data = await database["accounts"].find_one({"_id": account_id}, {
        "displayName": 1,
        "minorVerified": 1,
        "minorStatus": 1,
        "cabinedMode": 1,
        "externalAuths": 1
    })
    return {
        "id": account_data["_id"],
        "displayName": account_data["displayName"],
        "minorVerified": account_data["minorVerified"],
        "minorStatus": account_data["minorStatus"],
        "cabinedMode": account_data["cabinedMode"],
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
    return {
        "access_token": f"eg1~{await generate_eg1(sub, dn, client_id, dvid)}",
        "expires_in": 28800,
        "expires_at": (datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=8)).strftime("%Y-%m-%dT%H:%M"
                                                                                                   ":%S.000Z"),
        "token_type": "bearer",
        "refresh_token": f"eg1~{await generate_refresh_eg1(sub, dn, client_id, dvid)}",
        "refresh_expires": 2419200,
        "refresh_expires_at": await format_time(datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=672)),
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


async def create_account(database: motor.core.AgnosticDatabase, displayName: Optional[str] = None,
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
        return normalised_string
    return ""


@alru_cache()
async def load_datatable(datatable: Optional[str]) -> Optional[dict]:
    """
    Loads a datatable. As datatables are both static and large, this could be cached
    :param datatable: The datatable path to load
    :return: The datatable
    """
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
        match data[0].get('Type'):
            case "WExpGenericAccountItemDefinition":
                return f"{data[0].get('Properties').get('ItemType').split('::')[-1]}:{data[0].get('Name')}"
            case "WExpCharacterDefinition":
                return f"Character:{data[0].get('Name').split('CD_')[-1]}"
            case "WExpVoucherItemDefinition":
                return f"Voucher:{data[0].get('Name')}"
            case "WExpUpgradePotionDefinition":
                return f"UpgradePotion:{data[0].get('Name')}"
            case "WExpXpBookDefinition":
                return "Currency:HeroXp_Basic"  # hardcoded as in newer versions, all xp books are one type
            case "WExpTreasureMapDefinition":
                return f"TreasureMap:{data[0].get('Name')}"
            case "WExpTokenDefinition":
                return f"Token:{data[0].get('Name')}"
            case "WExpAccountRewardDefinition":
                return f"AccountReward:{data[0].get('Name')}"
            case "WExpCharacterDisplay":
                return f"CharacterDisplay:{data[0].get('Name')}"
            case "WExpCharacterEvolutionNode":
                return f"CharacterEvolutionNode:{data[0].get('Name')}"
            case "WExpChunkDefinition":
                return f"Chunk:{data[0].get('Name')}"
            case "WExpContainerDefinition":
                return f"Container:{data[0].get('Name')}"
            case "WExpCharacterHeroGearInfo":
                return f"CharacterHeroGearInfo:{data[0].get('Name')}"
            case "WExpEventDefinition":
                return f"Event:{data[0].get('Name')}"
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
                return f"LTMItem:{data[0].get('Name')}"
            case "WExpLevelArtDefinition":
                return f"LevelArt:{data[0].get('Name')}"
            case "WExpMajorEventTrackerDefinition":
                return f"MajorEventTracker:{data[0].get('Name')}"
            case "WExpMappedStyleData":
                return f"MappedStyle:{data[0].get('Name')}"
            case "WExpMenuData":
                return f"Menu:{data[0].get('Name')}"
            case "WExpOnboardingMenuData":
                return f"OnboardingMenu:{data[0].get('Name')}"
            case "WExpOnboardingGlobalData":
                return f"OnboardingGlobal:{data[0].get('Name')}"
            case "WExpPromotionTable":
                return f"PromotionTable:{data[0].get('Name')}"
            case "WExpProgressionData":
                return f"Progression:{data[0].get('Name')}"
            case "WExpPersonalEventDefinition":
                return f"PersonalEvent:{data[0].get('Name')}"
            case "WExpRecipe":
                return f"Recipe:{data[0].get('Name')}"
            case "WExpStandInDefinition":
                return f"StandIn:{data[0].get('Name')}"
            case "WExpStyleData":
                return f"Style:{data[0].get('Name')}"
            case "WExpSlateAnimationData":
                return f"SlateAnimation:{data[0].get('Name')}"
            case "WExpTileDefinition":
                return f"Tile:{data[0].get('Name')}"
            case "WExpTileGenerator":
                return f"TileGenerator:{data[0].get('Name')}"
            case "WExpUpgradePotionDefinition":
                return f"UpgradePotion:{data[0].get('Name')}"
            case "WExpUnlockableDefinition":
                return f"Unlockable:{data[0].get('Name')}"
            case "WExpVoucherItemDefinition":
                return f"Voucher:{data[0].get('Name')}"
            case "WExpZoneDefinition":
                return f"Zone:{data[0].get('Name')}"
            case "WExpHelpData":
                return f"Help:{data[0].get('Name')}"
            case "WExpCampaignDefinition":
                return f"Campaign:{data[0].get('Name')}"
            case "WExpBasicStyleData":
                return f"Style:{data[0].get('Name')}"
            case "WExpCameraTransitionAsset":
                return f"CameraTransition:{data[0].get('Name')}"
    return None


async def find_best_match(input_str: str, item_list: list, split_for_path: bool = False) -> str:
    """
    Finds the best match for a string in a list
    :param input_str: The string to find the best match for
    :param item_list: The list to find the best match in
    :param split_for_path: Whether to split the string for the path
    :return: The best match
    """
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
        return rapidfuzz.process.extractOne(input_str, item_list, processor=lambda x: x.split("\\")[-1].split(".")[0])[
            0]
    else:
        return rapidfuzz.process.extractOne(input_str, item_list)[0]


@alru_cache(maxsize=256)
async def get_path_from_template_id(template_id: str) -> str:
    """
    Gets the path from a template id
    :param template_id: The template id to get the path for
    :return: The path
    """
    if template_id is not None:
        best_match = await find_best_match(template_id, game_files_list, True)
        return best_match
    else:
        raise errors.com.epicgames.bad_request(errorMessage="Template ID is required")


@alru_cache(maxsize=32)
async def extract_version_info(user_agent: str) -> Tuple[int, int, int]:
    """
    Extracts the version info from a user agent
    :param user_agent: The user agent to extract the version info from
    :return: The version info as a tuple of (minor_version, revision, changelist)
    """
    modern_version_regex = r"1\.(\d*)\.(\d*)-r(\d*)"
    legacy_version_regex = r"-(\d*)\+\+\+WEX\+Release-1\.(\d*)"
    ultra_legacy_version_regex = r"-(\d*)\+\+\+WEX\+Release-(\d*)"
    ultra_legacy_version_regex_2 = r"Release-(\d*)-CL-(\d*)"
    match = re.search(modern_version_regex, user_agent)
    if match:
        minor_version = int(match.group(1))
        revision = int(match.group(2))
        changelist = int(match.group(3))
        return minor_version, revision, changelist
    match = re.search(legacy_version_regex, user_agent)
    if match:
        minor_version = int(match.group(2))
        revision = 0
        changelist = int(match.group(1))
        return minor_version, revision, changelist
    match = re.search(ultra_legacy_version_regex, user_agent)
    if match:
        minor_version = 0
        revision = int(match.group(2))
        changelist = int(match.group(1))
        return minor_version, revision, changelist
    match = re.search(ultra_legacy_version_regex_2, user_agent)
    if match:
        minor_version = 0
        revision = int(match.group(1))
        changelist = int(match.group(2))
        return minor_version, revision, changelist
    return 88, 244, 17036752  # Default values if no match is found


async def room_generator(level_id: str, level_info: dict) -> list:
    """
    Generates rooms for a level for levels where data is unavailable
    :param level_id: The level id to generate the rooms for
    :param level_info: The level info from the datatable
    :return: The generated rooms as a list to include in the level notification response
    """
    rooms_count = level_info.get("NumExpectedRooms", 1)
    room_info = (await load_datatable("Content/World/Datatables/LevelRooms"))[0]["Rows"]
    room = {
        "roomName": "",
        "regionName": level_id,
        "depth": 0,
        "worldLevel": level_info["BaseWorldLevel"],
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
    if not character_id.startswith("Character:"):
        raise errors.com.epicgames.world_explorers.bad_request(errorMessage="Invalid character id")
    character_id = character_id.replace("Character:", "CD_")
    best_match = await find_best_match(character_id, character_files_list, True)
    return await load_datatable(
        best_match.replace("res/battle-breakers-data/WorldExplorers/", "").replace(".json", "").replace("\\", "/"))


@alru_cache(maxsize=64)
async def get_curvetable_value(data_table: dict, row: str, time_input: float = 0) -> float:
    """
    Gets a value from a curvetable
    :param data_table: The curvetable to get the value from
    :param row: The row to get the value from
    :param time_input: The time to get the value from
    :return: The value from the curvetable
    """
    row_data = data_table[0]['Rows'][row]
    # ROOT[0].Rows.Default_C_T01.Keys[0].Time
    # clamp to lower bound.
    if time_input < row_data['Keys'][0]['Time']:
        return row_data['Keys'][0]['Value']

    # clamp to upper bound.
    if time_input >= row_data['Keys'][-1]['Time']:
        return row_data['Keys'][-1]['Value']

    # find the two keys that the time_input is between.
    for i in range(len(row_data['Keys']) - 1):
        if row_data['Keys'][i]['Time'] <= time_input < row_data['Keys'][i + 1]['Time']:
            # interpolate between the two keys.
            return row_data['Keys'][i]['Value'] + (time_input - row_data['Keys'][i]['Time']) / (
                    row_data['Keys'][i + 1]['Time'] - row_data['Keys'][i]['Time']) * (
                    row_data['Keys'][i + 1]['Value'] - row_data['Keys'][i]['Value'])


async def calculate_streakbreaker(current_streakbreaker: int, max_streakbreaker: int = 100000,
                                  base_chance: int = 10) -> tuple[bool, int]:
    """
    Calculates a streakbreaker roll
    :param current_streakbreaker: The current streakbreaker value
    :param max_streakbreaker: The maximum streakbreaker value
    :param base_chance: The base chance for the roll
    :return: A tuple of whether the roll succeeded and the new streakbreaker value
    """
    calculated_probability = (1 / base_chance) + (1 - (1 / base_chance)) / (
            1 + ((max_streakbreaker / current_streakbreaker) if current_streakbreaker else 1) ** 2)
    roll = random.random()
    if roll < calculated_probability:
        return True, 0
    else:
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
    new_string = input_string
    occurrence_count = 0
    for i in range(len(input_string)):
        if input_string[i:].startswith(target_string):
            occurrence_count += 1
            if occurrence_count == occurrence:
                new_string = input_string[:i] + replacement_string + input_string[i + len(target_string):]
                break
    return new_string


async def process_choices(input_data: str | int | float | list[str | int | float | dict[str, str | int | float | list[int | float]] | list]) -> str | int | float | dict[str, str | int | float | list[int | float]] | list[str | int | float | dict[str, str | int | float | list[int | float]]]:
    """
    Depending on the input data, this function will return either a random choice from a list, a random choice from a list, or the input data.
    
    If the input data is a list of two ints or floats, it will return a random int or float between the two values.
    If the input data is a list of any other type or length, it will return a random choice from the list.
    If the input data is any other type, it will return the input data.
    :param input_data: The input to process
    :return: The processed input
    """
    if isinstance(input_data, list):
        if len(input_data) == 2 and all(isinstance(x, (int, float)) for x in input_data):
            return random.uniform(input_data[0], input_data[1])
        return random.choice(input_data)
    return input_data
