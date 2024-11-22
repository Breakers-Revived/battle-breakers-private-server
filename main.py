"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).
"""
import os

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
async def attach_db(_app: sanic.app.Sanic[TomlConfig, Type[types.Context]], *_) -> None:
    """
    Called when the server is started
    :param _app: The app
    """
    _app.ctx.db = motor.motor_asyncio.AsyncIOMotorClient(_app.config.DATABASE["URI"])[_app.config.DATABASE["DATABASE"]]
    _app.ctx.db.client.timeoutMS = 1000
    _app.ctx.db.client.socketTimeoutMS = 1000
    _app.ctx.db.client.connectTimeoutMS = 1000
    _app.ctx.db.client.serverSelectionTimeoutMS = 1500
    _app.ctx.calendar = await ScheduledEvents.init_calendar()
    _app.ctx.storefronts = await StoreCatalogue.init_storefront()
    _app.ctx.lightswitch = await LightswitchService.init_lightswitch(_app.ctx.db)


@app.after_server_stop
async def server_stop(_app: sanic.app.Sanic[TomlConfig, Type[types.Context]], *_) -> None:
    """
    Called when the server is stopped
    :param _app: The app
    """
    print("Server stopped")
    print("Flushing changes and saving profiles...")
    for profile in _app.ctx.profiles.values():
        await profile.flush_changes()
        await profile.save_profile()
    for profile in _app.ctx.friends.values():
        await profile.save_friends()
    await _app.ctx.lightswitch.save_lightswitch()


if __name__ == "__main__":
    # workaround for sanic bug on windows where after_server_stop is not called when running with workers
    if os.name == "nt":
        app.run(host=app.config.SERVER["HOST"], port=app.config.SERVER["PORT"], single_process=True)
        # app.run(host=app.config.SERVER["HOST"], port=app.config.SERVER["PORT"], dev=True, debug=True, motd=False)
    else:
        app.run(host=app.config.SERVER["HOST"], port=app.config.SERVER["PORT"], fast=True)
