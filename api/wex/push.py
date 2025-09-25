"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles the GCM/FCM push notification registration token server sided storage
"""
import sanic
from sanic import HTTPResponse

from utils import types
from utils.utils import authorized as auth

from utils.sanic_gzip import Compress

compress = Compress()
wex_push = sanic.Blueprint("wex_push")


# undocumented
@wex_push.route("/api/push/<accountId>/register", methods=["POST"])
@auth(strict=True)
@compress.compress()
async def push(request: types.BBRequest, accountId: str) -> HTTPResponse:
    """
    Register a push notification token for the account
    Path Parameters
        accountId: The account ID to register the device for
    Query Parameters
        deviceToken: The device token to register with
        platform: The platform of the device e.g. ANDROID
        locale: The locale of the device e.g. en-AU
        tzOffset: The timezone offset of the device e.g. 10
        rvn: The profile0 revision number e.g. 40532
    :param request: The request object
    :param accountId: The account id
    :return: The response object
    """
    await request.app.ctx.db["push"].update_one({"_id": accountId}, {"$push": {
        "devices": {
            "deviceToken": request.args.get("deviceToken"),
            "platform": request.args.get("platform"),
            "locale": request.args.get("locale"),
            "tzOffset": request.args.get("tzOffset"),
            "rvn": request.args.get("rvn"),
            "timestamp": request.args.get("timestamp")
        }
    }}, upsert=True)
    # async with aiohttp.ClientSession() as session:
    #     await session.post("https://fcm.googleapis.com/fcm/send", headers={
    #         "Authorization": f"key={request.app.ctx.config['fcm_key']}",
    #         "Content-Type": "application/json"
    #     }, json={
    #         "to": request.args.get("deviceToken"),
    #         "notification": {
    #             "title": "Battle Breakers",
    #             "body": "Push notifications have been enabled for your account."
    #         }
    #     })
    return sanic.response.empty()
