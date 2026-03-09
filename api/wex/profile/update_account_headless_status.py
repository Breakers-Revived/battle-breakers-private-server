"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles update headless mcp
"""
import sanic

from utils import types
from utils.sanic_gzip import Compress
from utils.utils import authorized as auth, extract_version_info

compress = Compress()
wex_update_headless = sanic.Blueprint("wex_update_headless")


# undocumented
@wex_update_headless.route("/<accountId>/UpdateAccountHeadlessStatus", methods=["POST"])
@auth(strict=True)
@compress.compress()
async def update_headless(request: types.BBProfileRequest, accountId: str) -> sanic.response.JSONResponse:
    """
    This endpoint is used to set the display name on an account and mark it as non-headless.
    :param request: The request object
    :param accountId: The account id
    :return: The modified profile
    """
    # TODO: Determine what the request provides us with
    await request.ctx.profile.modify_stat("is_headless", False, request.ctx.profile_id)
    await request.app.ctx.db["accounts"].update_one(
        {"_id": accountId},
        {"$set": {"headless": False}}
    )
    return sanic.response.json(
        await request.ctx.profile.construct_response(request.ctx.profile_id, request.ctx.rvn,
                                                     request.ctx.profile_revisions,
                                                     (await extract_version_info(request.headers.get("User-Agent")))[
                                                         -1])
    )
