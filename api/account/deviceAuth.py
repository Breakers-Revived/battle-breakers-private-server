"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2023 by Alex Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the [TBD] license.

Handles the device auth creation for mobile
"""
import sanic

from utils.exceptions import errors
from utils.utils import authorized as auth, uuid_generator, token_generator, format_time

from utils.sanic_gzip import Compress

compress = Compress()
device_auth = sanic.Blueprint("device_auth")


# undocumented
@device_auth.route("/api/public/account/<accountId>/deviceAuth", methods=["POST"])
@auth(strict=True)
@compress.compress()
async def device_auth_create(request: sanic.request.Request, accountId: str) -> sanic.response.JSONResponse:
    """
    Create a device auth for the account
    :param request: The request object
    :param accountId: The account id
    :return: The response object
    """
    device_authorisation = {
        "deviceId": await uuid_generator(),
        "accountId": accountId,
        "secret": (await token_generator()).upper(),
        "userAgent": request.headers.get("User-Agent"),
        "created": {
            "location": None,
            "ipAddress": request.ip,
            "dateTime": await format_time()
        },
        "lastAccess": {
            "location": None,
            "ipAddress": request.ip,
            "dateTime": await format_time()
        },
        "deviceInfo": {
            "type": "",
            "model": "",
            "os": ""
        }
    }
    await request.app.ctx.database["accounts"].update_one({"_id": accountId}, {
        "$push": {
            "extra.deviceAuths": device_authorisation
        }
    })
    return sanic.response.json(device_authorisation)


# undocumented
@device_auth.route("/api/public/account/<accountId>/deviceAuth", methods=["GET"])
@auth(strict=True)
@compress.compress()
async def device_auth_get(request: sanic.request.Request, accountId: str) -> sanic.response.JSONResponse:
    """
    Gets a list of all registered device auths for an account
    :param request: The request object
    :param accountId: The account id
    :return: The response object
    """
    device_auths = await request.app.ctx.database["accounts"].find_one({"_id": accountId}, {"extra.deviceAuths": 1})
    for device in device_auths["extra"]["deviceAuths"]:
        device.pop("secret")
    return sanic.response.json(device_auths["extra"]["deviceAuths"])


# undocumented
@device_auth.route("/api/public/account/<accountId>/deviceAuth/<deviceId>", methods=["GET"])
@auth(strict=True)
@compress.compress()
async def device_auth_info(request: sanic.request.Request, accountId: str,
                           deviceId: str) -> sanic.response.JSONResponse:
    """
    Gets info about the specified device auth for an account
    :param request: The request object
    :param accountId: The account id
    :param deviceId: The device id
    :return: The response object
    """
    device_info = await request.app.ctx.database["accounts"].find_one({"_id": accountId}, {
        "extra.deviceAuths": {
            "$elemMatch": {
                "deviceId": deviceId
            }
        }
    })
    if not device_info:
        raise errors.com.epicgames.account.device_auth.invalid_device_info()
    device_info = device_info["extra"]["deviceAuths"][0]
    device_info.pop("secret")
    return sanic.response.json(device_info)


# undocumented
@device_auth.route("/api/public/account/<accountId>/deviceAuth/<deviceId>", methods=["DELETE"])
@auth(strict=True)
@compress.compress()
async def device_auth_deletion(request: sanic.request.Request, accountId: str,
                               deviceId: str) -> sanic.response.HTTPResponse:
    """
    Remove a device auth for the account
    :param request: The request object
    :param accountId: The account id
    :param deviceId: The device id
    :return: The response object
    """
    device_auths = await request.app.ctx.database["accounts"].find_one({"_id": accountId}, {"extra.deviceAuths": 1})
    for device in device_auths["extra"]["deviceAuths"]:
        if device["deviceId"] == deviceId:
            device_auths["extra"]["deviceAuths"].remove(device)
            break
    else:
        raise errors.com.epicgames.account.device_auth.invalid_device_info()
    await request.app.ctx.database["accounts"].update_one({"_id": accountId}, {
        "$set": {
            "extra.deviceAuths": device_auths["extra"]["deviceAuths"]
        }
    })
    return sanic.response.empty()
