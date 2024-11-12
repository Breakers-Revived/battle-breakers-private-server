"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles the motd of old versions
"""

import aiofiles
import sanic

from utils import types
from utils.sanic_gzip import Compress

compress = Compress()
wex_motd = sanic.Blueprint("wex_motd")


# undocumented
@wex_motd.route("/api/game/v2/motd", methods=['GET'])
@compress.compress()
async def motd(request: types.BBRequest) -> sanic.response.HTTPResponse:
    """
    Handles the motd of 1.0, however this version does not seem to display the news button
    :param request: The request object
    :return: The response object
    """
    async with aiofiles.open("res/account/login/guided/index.html", "rb") as file:
        return sanic.response.raw(await file.read(), content_type="text/html")
