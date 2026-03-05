"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles the account sign up request for mobile
"""
import sanic

from utils import types
from utils.exceptions import errors
from utils.sanic_gzip import Compress
from utils.utils import oauth_response

compress = Compress()
register_login = sanic.Blueprint("register_login")


# undocumented
@register_login.route("/id/registertest", methods=["GET"])
@compress.compress()
async def register_test(request: types.BBRequest) -> sanic.response.JSONResponse:
    """
    This endpoint is used to get the registration page
    :param request: The request object
    :return: The response object
    """
    if not request.app.debug:
        raise errors.com.epicgames.common.not_found()
    return sanic.response.json(
        await oauth_response("3cf78cd3b00b439a8755a878b160c7ad", "Dippyshere MbnM",
                             None,
                             "ec0ebb7e56f6454e86c62299a7b32e20"))
    # return sanic.response.text(str(request.app.ctx.profiles))
