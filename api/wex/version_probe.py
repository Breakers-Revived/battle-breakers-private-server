"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles the mcp version probe
"""
import datetime

import sanic

from utils import types
from utils.sanic_gzip import Compress
from utils.utils import extract_version_info

compress = Compress()
wex_version_probe = sanic.Blueprint("wex_version_probe")


# https://github.com/dippyshere/battle-breakers-documentation/blob/main/docs/World%20Explorers%20Service/wex/api/game/version-probe.md
@wex_version_probe.route("/api/game/version-probe", methods=['GET'])
@compress.compress()
async def version_probe(request: types.BBRequest) -> sanic.response.HTTPResponse:
    """
    Handles the version probe request
    :param request: The request object
    :return: The response object
    """
    # Version probe can call upon different actions for the client to take
    # The client supports the commands: launch_url:<url>, stop_url:<url>, switch_env:<mcpenv>
    # launch_url will open the url in the client's default browser, and continue the login process
    # stop_url will open the url in the client's default browser, and halt the login process
    # switch_env will switch the client to the specified MCP environment (live, devtesting, etc),
    # the client will then call the version probe again after switching
    # As the 1.6 client only supports switch_env:, we must omit the command from the response
    changelist = (await extract_version_info(request.headers.get("User-Agent")))[-1]
    if not hasattr(request.conn_info.ctx, "probe_count"):
        request.conn_info.ctx.probe_count = 0
    request.conn_info.ctx.probe_count += 1
    if request.conn_info.ctx.probe_count > 1 or (hasattr(request.ctx, "last_probe_time") and 0.5 >= (datetime.datetime.now(tz=datetime.timezone.utc) - request.ctx.last_probe_time).total_seconds() <= 1.5):
        if changelist <= 4371600: # 1.7
            return sanic.response.text("DevTesting")
        return sanic.response.text("switch_env:DevTesting")
    request.ctx.last_probe_time = datetime.datetime.now(tz=datetime.timezone.utc)
    if changelist <= 4371600:
        return sanic.response.text("\r\nBreakers Revived\r\n\r\nServer Emulator created by Dippyshere\r\n\r\n\r\n\r\n\r\nContacting game service...")
    return sanic.response.text(
        "switch_env:\r\nBreakers Revived\r\n\r\nServer Emulator created by Dippyshere\r\n\r\n\r\n\r\n\r\nContacting game service..."
    )
