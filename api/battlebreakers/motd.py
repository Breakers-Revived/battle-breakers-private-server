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
bb_motd = sanic.Blueprint("bb_motd")


# undocumented
@bb_motd.route("/battlebreakers/motd", methods=['GET'])
@compress.compress()
async def motd2(request: types.BBRequest) -> sanic.response.HTTPResponse:
    """
    Handles the motd html of old versions of battle breakers (1.1 - ~1.6)
    These motd news requests on 1.1 - 1.5 expect an HTML website, and all external content is fetched via webview instead of game client
    :param request: The request object
    :return: The response object
    """
    async with aiofiles.open("res/account/login/guided/index.html", "rb") as file:
        return sanic.response.raw(await file.read(), content_type="text/html")
