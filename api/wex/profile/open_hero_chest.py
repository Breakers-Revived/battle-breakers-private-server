"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles opening a hero chest.
"""
import random

import sanic
import sanic_ext

from utils import types
from utils.exceptions import errors
from utils.utils import authorized as auth, read_file_cached, extract_version_info
from utils.validation import MCPValidation, MCPQueryValidation

from utils.sanic_gzip import Compress

compress = Compress()
wex_profile_open_hero_chest = sanic.Blueprint("wex_profile_open_hero_chest")


# https://github.com/dippyshere/battle-breakers-documentation/blob/main/docs/World%20Explorers%20Service/wex/api/game/v2/profile/accountId/OpenHeroChest.md
@wex_profile_open_hero_chest.route("/<accountId>/OpenHeroChest", methods=["POST"])
@auth(strict=True)
@sanic_ext.validate(json=MCPValidation.OpenHeroChest, query=MCPQueryValidation.MCPProfile0)
@compress.compress()
async def open_hero_chest(request: types.BBProfileRequest, accountId: str,
                          body: MCPValidation.OpenHeroChest,
                          query: MCPQueryValidation.MCPProfile0) -> sanic.response.JSONResponse:
    """
    This endpoint is used to open a hero chest.
    :param request: The request object
    :param accountId: The account id
    :param body: The request body
    :param query: The query arguments
    :return: The modified profile
    """
    request_body = body.model_dump()
    tower_data = await request.ctx.profile.get_item_by_guid(request_body.get("towerId"))
    if tower_data is None:
        raise errors.com.epicgames.world_explorers.bad_request(errorMessage="Invalid tower id")
    if not tower_data["attributes"].get("active_chest"):
        raise errors.com.epicgames.world_explorers.bad_request(
            errorMessage="Tower has no active chest. Call PickHeroChest")
    active_chest = tower_data["attributes"]["active_chest"]
    await request.ctx.profile.consume_item(
        tower_data["attributes"][f"{active_chest['heroChestType']}_static_currency_template_id"],
        tower_data["attributes"][f"{active_chest['heroChestType']}_static_currency_amount"])
    if request_body.get("itemTemplateId").split(":")[0] != "Character":
        await request.ctx.profile.grant_item(request_body.get("itemTemplateId"), request_body.get("itemQuantity", 1))
    else:
        await request.ctx.profile.grant_hero(request_body.get("itemTemplateId"),
                                             foil_lvl=1 if active_chest["foilLevel"] > 0 else -1)
    # TODO: chest activity
    await request.ctx.profile.change_item_attribute(request_body.get("towerId"), "active_chest", None)
    hero_tower_data = (await read_file_cached("res/wex/api/game/v2/skybreaker/herotower.json"))[
        active_chest['heroTrackId']]
    new_page_index = tower_data["attributes"]["page_index"]
    if active_chest["heroTrackId"] == "CoreBasic":
        if tower_data["attributes"][f"{active_chest['heroTrackId']}_progress"] + 1 > int(
                list(hero_tower_data[str(new_page_index)].keys())[-1]):
            await request.ctx.profile.change_item_attribute(request_body.get("towerId"),
                                                            f"{active_chest['heroTrackId']}_progress", 0)
            track_progress = 0
            if tower_data["attributes"]["page_index"] + 1 > int(list(hero_tower_data.keys())[-1]):
                new_page_index = int(list(hero_tower_data.keys())[0])
                await request.ctx.profile.grant_item("Reagent:Reagent_HeroMap_SuperRare", 5)
            else:
                new_page_index = tower_data["attributes"]["page_index"] + 1
                await request.ctx.profile.grant_item("Reagent:Reagent_HeroMap_SuperRare", 1)
        else:
            await request.ctx.profile.change_item_attribute(request_body.get("towerId"),
                                                            f"{active_chest['heroTrackId']}_progress",
                                                            tower_data["attributes"][
                                                                f"{active_chest['heroTrackId']}_progress"] + 1)
            track_progress = tower_data["attributes"][f"{active_chest['heroTrackId']}_progress"] + 1
    else:
        await request.ctx.profile.change_item_attribute(request_body.get("towerId"),
                                                        f"{active_chest['heroTrackId']}_progress",
                                                        tower_data["attributes"][
                                                            f"{active_chest['heroTrackId']}_progress"] + 1)
        track_progress = tower_data["attributes"][f"{active_chest['heroTrackId']}_progress"] + 1
    await request.ctx.profile.change_item_attribute(request_body.get("towerId"), "level",
                                                    tower_data["attributes"]["level"] + 1)
    await request.ctx.profile.change_item_attribute(request_body.get("towerId"), "page_index", new_page_index)
    next_hero_track = list(hero_tower_data[str(new_page_index)].keys())[
        track_progress % len(hero_tower_data[str(new_page_index)])]
    new_chest_options = hero_tower_data[str(new_page_index)][str(next_hero_track)]
    new_chest_options["heroTrackId"] = active_chest['heroTrackId']
    new_chest_options["foilLevel"] = 1 if random.randint(0, 100) < 7 else 0
    await request.ctx.profile.change_item_attribute(request_body.get("towerId"), "chest_options", [new_chest_options])
    return sanic.response.json(
        await request.ctx.profile.construct_response(request.ctx.profile_id, request.ctx.rvn,
                                                     request.ctx.profile_revisions,
                                                     (await extract_version_info(request.headers.get("User-Agent")))[
                                                         -1])
    )
