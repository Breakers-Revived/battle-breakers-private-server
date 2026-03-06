"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles the login flow
"""
import re

import sanic

from utils import types
from utils.utils import authorized as auth, generate_authorisation_eg1, bcrypt_hash, create_account, bcrypt_check, \
    username_pattern

from utils.sanic_gzip import Compress

compress = Compress()
login_token = sanic.Blueprint("login_token")


# undocumented
@login_token.route("/id/login/token", methods=["POST"])
@auth(allow_basic=True)
@compress.compress()
async def login_token_route(request: types.BBRequest) -> sanic.response.JSONResponse:
    """
    Authenticate a mobile user logging in / signing up and return a token
    :param request: The request object
    :return: The response object
    """
    # logging in
    if request.headers.get("X-Request-Source-Form") == "login-form":
        if not request.json or not isinstance(request.json.get("username"), str) or not isinstance(request.json.get("password"), str):
            raise sanic.exceptions.InvalidUsage("Invalid request", context={
                "errorMessage": "Username and password are required"})
        username = request.json.get("username")[:32]
        password = request.json.get("password")
        if len(username) > 24:
            if not username_pattern.match(username):
                raise sanic.exceptions.InvalidUsage("Invalid username",
                                                    context={"errorMessage": "This account ID is invalid"})
            else:
                account_data: dict = await request.app.ctx.db["accounts"].find_one(
                    {"_id": {"$regex": re.escape(username.strip()), "$options": "i"}}, {
                        "_id": 1,
                        "displayName": 1,
                        "extra.pwhash": 1
                    })
                if account_data is None:
                    raise sanic.exceptions.InvalidUsage("Invalid credentials", context={
                        "errorMessage": "Invalid username or password"})
                else:
                    if not await bcrypt_check(password, account_data["extra"]["pwhash"].encode()):
                        raise sanic.exceptions.Unauthorized("Invalid credentials", context={
                            "errorMessage": "Invalid username or password"})
                    else:
                        return sanic.response.json(
                            {"username": account_data["displayName"],
                             "authorisationCode": await generate_authorisation_eg1(account_data["_id"],
                                                                                   account_data[
                                                                                       "displayName"]),
                             "id": account_data["_id"], "heading": "Complete Login"
                             }
                        )
        elif len(username) < 3:
            raise sanic.exceptions.InvalidUsage("Invalid username", context={
                "errorMessage": "Your username is too short"})
        elif len(username) > 32:
            raise sanic.exceptions.InvalidUsage("Invalid username", context={
                "errorMessage": "Username/Account ID too long"})
        else:
            if re.match(r"[^@]+@[^@]*\.[^@]*", username):
                account_data: dict = await request.app.ctx.db["accounts"].find_one(
                    {"email": {"$regex": re.escape(username.strip()), "$options": "i"}}, {
                        "_id": 1,
                        "displayName": 1,
                        "extra.pwhash": 1
                    })
            else:
                account_data: dict = await request.app.ctx.db["accounts"].find_one(
                    {"displayName": {"$regex": re.escape(username.strip()), "$options": "i"}}, {
                        "_id": 1,
                        "displayName": 1,
                        "extra.pwhash": 1
                    })
            if account_data is None:
                raise sanic.exceptions.InvalidUsage("Invalid credentials", context={
                    "errorMessage": "Invalid username or password"})
            else:
                if not await bcrypt_check(password, account_data["extra"]["pwhash"].encode()):
                    raise sanic.exceptions.Unauthorized("Invalid credentials", context={
                        "errorMessage": "Invalid username or password"})
                else:
                    return sanic.response.json(
                        {"username": account_data["displayName"],
                         "authorisationCode": await generate_authorisation_eg1(account_data["_id"],
                                                                               account_data["displayName"]),
                         "id": account_data["_id"], "heading": "Complete Login"
                         }
                    )
    elif request.headers.get("X-Request-Source-Form") == "signup-form":
        if not request.json or not isinstance(request.json.get("username"), str) or not isinstance(request.json.get("password"), str):
            raise sanic.exceptions.InvalidUsage("Invalid request", context={
                "errorMessage": "Username and password are required"})
        username = request.json.get("username")[:32]
        password = request.json.get("password")
        if len(username) < 3:
            raise sanic.exceptions.InvalidUsage("Invalid username", context={
                "errorMessage": "Your username is too short"})
        elif len(username) > 24:
            raise sanic.exceptions.InvalidUsage("Invalid username", context={
                "errorMessage": "Username too long"})
        elif len(str(password)) < 4:
            raise sanic.exceptions.InvalidUsage("Invalid password", context={
                "errorMessage": "Your password is too short"})
        elif len(str(password)) > 64:
            raise sanic.exceptions.InvalidUsage("Invalid password", context={
                "errorMessage": "Your password is too long"})
        else:
            # TODO: implement better signup system
            if re.match(r"^[^@]+@[^@]*\.[^@]*$", username):
                account_data: dict = await request.app.ctx.db["accounts"].find_one(
                    {"email": {"$regex": f"^{re.escape(username.strip())}$", "$options": "i"}}, {
                        "_id": 1,
                        "displayName": 1,
                        "extra.pwhash": 1
                    })
            else:
                account_data: dict = await request.app.ctx.db["accounts"].find_one(
                    {"displayName": {"$regex": f"^{re.escape(username.strip())}$", "$options": "i"}}, {
                        "_id": 1,
                        "displayName": 1,
                        "extra.pwhash": 1
                    })
            if account_data is None:
                account_id = await create_account(request.app.ctx.db, username, await bcrypt_hash(password),
                                                  calendar=request.app.ctx.calendar)
                return sanic.response.json(
                    {"username": username,
                     "authorisationCode": await generate_authorisation_eg1(account_id,
                                                                           username),
                     "id": account_id, "heading": "Complete Sign Up"
                     }
                )
            else:
                if not await bcrypt_check(password, account_data["extra"]["pwhash"].encode()):
                    raise sanic.exceptions.Unauthorized("Invalid password", context={
                        "errorMessage": "Your account already exists. The password you entered is incorrect."})
                else:
                    return sanic.response.json(
                        {"username": account_data["displayName"],
                         "authorisationCode": await generate_authorisation_eg1(account_data["_id"],
                                                                               account_data["displayName"]),
                         "id": account_data["_id"], "heading": "Complete Login"
                         }
                    )
    else:
        raise sanic.exceptions.InvalidUsage("Invalid X-Request-Source-Form header")
