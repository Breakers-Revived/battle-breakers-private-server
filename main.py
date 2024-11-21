"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).
"""
from typing_extensions import Any, Type

from api import api
from utils import utils, error_handler, types
import middleware.mcp_middleware

import orjson
import sanic
import sanic_ext
import colorama
import motor.motor_asyncio

from utils.services.calendar.calendar import ScheduledEvents
from utils.services.lightswitch.lightswitch import LightswitchService
from utils.services.storefront.catalog import StoreCatalogue
from utils.toml_config import TomlConfig
from utils.custom_serialiser import custom_serialise

colorama.init()
toml_config = TomlConfig(path="utils/config.toml")
app: sanic.app.Sanic[TomlConfig, Type[types.Context]] = sanic.app.Sanic("dippy_breakers",
                                                                        dumps=lambda obj: orjson.dumps(obj,
                                                                                                       default=
                                                                                                       custom_serialise)
                                                                        , loads=orjson.loads, config=toml_config,
                                                                        ctx=types.Context)

app.blueprint(api)
sanic_ext.Extend(app)
app.ctx.public_key = utils.public_key
app.error_handler = error_handler.CustomErrorHandler()
app.register_middleware(middleware.mcp_middleware.add_mcp_headers, "response")
app.ctx.accounts = {}
app.ctx.friends = {}
app.ctx.profiles = {}
app.ctx.invalid_tokens = []


@app.before_server_start
async def attach_db(*_: Any) -> None:
    """
    Called when the server is started
    :param _: The loop
    """
    app.ctx.db = motor.motor_asyncio.AsyncIOMotorClient(app.config.DATABASE["URI"])[app.config.DATABASE["DATABASE"]]
    app.ctx.db.client.timeoutMS = 1000
    app.ctx.db.client.socketTimeoutMS = 1000
    app.ctx.db.client.connectTimeoutMS = 1000
    app.ctx.db.client.serverSelectionTimeoutMS = 1500
    app.ctx.calendar = await ScheduledEvents.init_calendar()
    app.ctx.storefronts = await StoreCatalogue.init_storefront()
    app.ctx.lightswitch = await LightswitchService.init_lightswitch(app.ctx.db)


@app.before_server_stop
async def server_stop(*_: Any) -> None:
    """
    Called when the server is stopped
    :param _: The loop
    """
    for profile in app.ctx.profiles.values():
        await profile.flush_changes()
        await profile.save_profile()
    for profile in app.ctx.friends.values():
        await profile.save_friends()
    await app.ctx.lightswitch.save_lightswitch()


if __name__ == "__main__":
    app.run(host=app.config.SERVER["HOST"], port=app.config.SERVER["PORT"], auto_reload=True, access_log=False)
