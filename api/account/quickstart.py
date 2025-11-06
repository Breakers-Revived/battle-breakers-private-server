"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles the quick start account creation
"""
import sanic

from utils import types
from utils.utils import authorized as auth, oauth_response, generate_eg1, uuid_generator, create_account, \
    token_generator, format_time

from utils.sanic_gzip import Compress

compress = Compress()
account_quickstart = sanic.Blueprint("account_quickstart")


# undocumented
@account_quickstart.route("/api/public/account", methods=["POST"])
@auth(allow_basic=True)
@compress.compress()
async def quickstart(request: types.BBRequest) -> sanic.response.HTTPResponse:
    """
    Create a quick start account

    :param request: The request object
    :return: The response object
    """
    # TODO: better signup system
    new_account_id = await create_account(request.app.ctx.db, calendar=request.app.ctx.calendar)
    device_id = request.headers.get("X-Epic-Device-ID", await uuid_generator())
    device_authorisation = {
        "deviceId": device_id,
        "accountId": new_account_id,
        "secret": (await token_generator()).upper(),
        "userAgent": request.headers.get("User-Agent"),
        "created": {
            "location": None,
            "ipAddress": request.ip,
            "dateTime": await format_time()
        }
    }
    await request.app.ctx.db["accounts"].update_one(
        {"_id": new_account_id},
        {
            "$set": {"headless": True},
            "$push": {"extra.deviceAuths": device_authorisation}
        }
    )
    return sanic.response.json({
        "accountInfo": {
            "id": new_account_id,
            "failedLoginAttempts": 0,
            "numberOfDisplayNameChanges": 0,
            "ageGroup": "UNKNOWN",
            "headless": True,
            "country": "AU",
            "preferredLanguage": "en",
            "canUpdateDisplayName": True,
            "tfaEnabled": False,
            "emailVerified": False,
            "minorVerified": False,
            "minorExpected": False,
            "minorStatus": "UNKNOWN",
            "cabinedMode": False,
            "hasHashedEmail": False
        },
        "internalAuthKey": f"eg1~{await generate_eg1(sub=new_account_id, dvid=device_id)}",
        "deviceAuth": device_authorisation,
        "oauthSession": await oauth_response(sub=new_account_id, dvid=device_id)
    })
