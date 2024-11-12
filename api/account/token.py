"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles the token requests
"""
import base64
import re

import sanic

from utils import enums, types
from utils.enums import AuthClient
from utils.exceptions import errors
from utils.profile_system import PlayerProfile
from utils.utils import (authorized as auth, oauth_response, parse_eg1, create_account, verify_google_token,
                         oauth_client_response, bcrypt_check)

from utils.sanic_gzip import Compress

compress = Compress()
token = sanic.Blueprint("account_token")


# https://github.com/dippyshere/battle-breakers-documentation/blob/main/docs/Account%20Service/account/api/oauth/token.md
@token.route("/api/oauth/token", methods=["POST"])
@auth(allow_basic=True)
@compress.compress()
async def oauth_route(request: types.BBRequest) -> sanic.response.JSONResponse:
    """
    Handles the oauth token request
    :param request: The request object
    :return: The response object
    """
    if request.headers.get('Authorization'):
        if request.headers.get('Authorization').startswith('basic'):
            try:
                authorisation = base64.b64decode(request.headers.get('Authorization').split(' ')[1]).decode()
                client_id = authorisation.split(':')[0]
                client_secret = authorisation.split(':')[1]
            except:
                raise errors.com.epicgames.common.oauth.invalid_client()
            auth_clients: list[AuthClient] = enums.AuthClient.from_string(client_id)
            for auth_client in auth_clients:
                if client_secret == auth_client.value[1]:
                    break
            else:
                raise errors.com.epicgames.account.invalid_client_credentials()
            auth_client = auth_clients[0]
        elif request.headers.get('Authorization').startswith('bearer'):
            client_id = "3cf78cd3b00b439a8755a878b160c7ad"
        else:
            raise errors.com.epicgames.common.oauth.oauth_error()
        match request.form.get('grant_type'):
            case 'client_credentials':
                if not request.headers.get('Authorization').startswith('basic'):
                    raise errors.com.epicgames.common.oauth.unsupported_grant_type()
                return sanic.response.json((await oauth_client_response(auth_client.value[0])))
            case 'external_auth':
                match request.form.get('external_auth_type'):
                    case 'google':
                        # TODO: Reinvestigate what this case is
                        sub = request.form.get('external_auth_token').split(':')[0]
                        account: dict = await request.app.ctx.db["accounts"].find_one({"_id": sub}, {
                            "_id": 0,
                            "displayName": 1,
                        })
                        dn = account['displayName']
                        dvid = request.headers.get('X-Epic-Device-ID')
                        return sanic.response.json((await oauth_response(client_id, dn, dvid, sub)))
                    case 'google_id_token':
                        google_token = await verify_google_token(
                            request.form.get('external_auth_token'))
                        if google_token is not None:
                            sub = google_token['sub']
                            account = await request.app.ctx.db["accounts"].find_one(
                                {"externalAuths.google.externalAuthId": sub}, {"displayName": 1})
                            if account:
                                dn = account['displayName']
                                dvid = request.headers.get('X-Epic-Device-ID')
                                return sanic.response.json(await oauth_response(client_id, dn, dvid, account['_id']))
                            # Create an account
                            account_id = await create_account(request.app.ctx.db,
                                                              calendar=request.app.ctx.calendar)
                            await request.app.ctx.db["accounts"].update_one(
                                {"_id": account_id},
                                {
                                    "$set": {
                                        f"externalAuths.google": {
                                            "accountId": account_id,
                                            "type": "google",
                                            "externalAuthId": google_token.get("sub"),
                                            "externalAuthIdType": "google_id_token",
                                            "externalDisplayName": google_token.get("name"),
                                            "authIds": [
                                                {
                                                    "id": google_token.get("sub"),
                                                    "type": "google_id_token"
                                                }
                                            ]
                                        },
                                        "name": google_token.get("given_name"),
                                        "lastName": google_token.get("family_name"),
                                        "headless": True
                                    }
                                }
                            )
                            if account_id not in request.app.ctx.profiles:
                                request.app.ctx.profiles[account_id] = await PlayerProfile.init_profile(account_id)
                            await request.app.ctx.profiles[account_id].modify_stat("is_headless", False)
                            return sanic.response.json(
                                (await oauth_response(sub=account_id)))
                        else:
                            raise errors.com.epicgames.account.external_auth_validate_failed()
                    case 'internal':
                        # Yeah, really! Internal external auth!
                        token = await parse_eg1(
                            request.form.get('external_auth_token').split(":")[-1])
                        if token is not None:
                            return sanic.response.json((await oauth_response(client_id, token['dn'],
                                                                             token['dvid'],
                                                                             token['sub'])))
                        else:
                            raise errors.com.epicgames.account.oauth.expired_exchange_code()
                    case _:
                        raise errors.com.epicgames.account.ext_auth.unknown_external_auth_type()
            case 'authorization_code':
                token = await parse_eg1(request.form.get('code'))
                if token is not None:
                    return sanic.response.json((await oauth_response(client_id, token['dn'],
                                                                     request.headers.get('X-Epic-Device-ID'),
                                                                     token['sub'])))
                else:
                    raise errors.com.epicgames.account.oauth.expired_authorization_code()
            case 'refresh_token':
                token = await parse_eg1(request.form.get('refresh_token'))
                if token is not None:
                    return sanic.response.json((await oauth_response(client_id, token['dn'],
                                                                     request.headers.get('X-Epic-Device-ID'),
                                                                     token['sub'])))
                else:
                    raise errors.com.epicgames.account.auth_token.invalid_refresh_token()
            case 'password':  # backwards compatibility for old clients
                # TODO: support display name and email login
                if len(request.form.get('username').split('@')[0].strip()) < 3:
                    raise errors.com.epicgames.account.invalid_account_credentials()
                elif len(request.form.get('username').split('@')[0].strip()) > 24:
                    raise errors.com.epicgames.account.invalid_account_credentials()
                if len(request.form.get('password')) < 4:
                    raise errors.com.epicgames.account.invalid_account_credentials()
                elif len(request.form.get('password')) > 64:
                    raise errors.com.epicgames.account.invalid_account_credentials()
                # TODO: implement better signup system
                # allows email@. to be used as a username login
                if re.match(r"^[^@]+@[^@]+\.[^@]+$", request.form.get('username')):
                    account_data: dict = await request.app.ctx.db["accounts"].find_one(
                        {"email": {"$regex": f"^{re.escape(request.form.get('username').split('@')[0].strip())}$",
                                   "$options": "i"}}, {
                            "_id": 1,
                            "displayName": 1,
                            "extra.pwhash": 1
                        })
                else:
                    account_data: dict = await request.app.ctx.db["accounts"].find_one(
                        {"displayName": {"$regex": f"^{re.escape(request.form.get('username').split('@')[0].strip())}$",
                                         "$options": "i"}}, {
                            "_id": 1,
                            "displayName": 1,
                            "extra.pwhash": 1
                        })
                if account_data is None:
                    raise errors.com.epicgames.account.account_not_found(
                        request.form.get('username').split("@")[0].strip())
                if not await bcrypt_check(request.form.get('password'),
                                          account_data["extra"]["pwhash"].encode()):
                    raise errors.com.epicgames.account.invalid_account_credentials()
                else:
                    return sanic.response.json((await oauth_response(client_id, account_data['displayName'],
                                                                     request.headers.get(
                                                                         'X-Epic-Device-ID'),
                                                                     account_data["_id"])))
            case 'exchange_code':
                token = await parse_eg1(request.form.get('exchange_code'))
                if token is not None:
                    return sanic.response.json((await oauth_response(client_id, token['dn'],
                                                                     request.headers.get(
                                                                         'X-Epic-Device-ID'),
                                                                     token['sub'])))
                else:
                    raise errors.com.epicgames.account.oauth.expired_exchange_code()
            case 'device_auth':
                if request.form.get('account_id'):
                    account = await request.app.ctx.db["accounts"].find_one({
                        "_id": request.form.get('account_id'),
                        "extra.deviceAuths": {
                            "$elemMatch": {
                                "deviceId": request.form.get('device_id'),
                                "secret": request.form.get('secret')
                            }
                        }
                    })
                    if account:
                        return sanic.response.json(
                            await oauth_response(client_id, account['displayName'], request.form.get('device_id'),
                                                 account["_id"]))
                    else:
                        raise errors.com.epicgames.common.authentication.authentication_failed(
                            request.form.get('account_id'))
                else:
                    raise errors.com.epicgames.account.device_auth.invalid_device_info()
            case _:
                # TODO: misc to implement: continuation_token + device_code + otp + token_to_token
                # ALl of these except opt are unused by any client / launcher. OTP could be used in the future for 2fa.
                # otp fields: otp, challenge
                # token_to_token fields:
                # continuation_token fields:
                # device_code fields:
                raise errors.com.epicgames.common.oauth.unsupported_grant_type()
    else:
        raise errors.com.epicgames.common.oauth.invalid_request()
