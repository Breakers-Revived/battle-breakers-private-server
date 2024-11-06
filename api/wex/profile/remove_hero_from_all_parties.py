"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles removing a hero from all parties
"""

import sanic

from utils import types
from utils.exceptions import errors
from utils.utils import authorized as auth

from utils.sanic_gzip import Compress

compress = Compress()
wex_profile_remove_hero_from_all_parties = sanic.Blueprint("wex_profile_remove_hero_from_all_parties")


# undocumented
@wex_profile_remove_hero_from_all_parties.route("/<accountId>/RemoveHeroFromAllParties", methods=["POST"])
@auth(strict=True)
@compress.compress()
async def remove_hero_parties(request: types.BBProfileRequest, accountId: str) -> sanic.response.JSONResponse:
    """
    This endpoint is used to remove a hero from all parties.
    :param request: The request object
    :param accountId: The account id
    :return: The modified profile
    """
    # TODO: validation
    # TODO: determine when original game calls this and what data it sends
    hero_item = await request.ctx.profile.get_item_by_guid(request.json.get("heroItemId"))
    if hero_item is None:
        raise errors.com.epicgames.world_explorers.bad_request(errorMessage="Invalid hero item id")
    if not hero_item.get("templateId").startswith("Character:"):
        raise errors.com.epicgames.world_explorers.bad_request(errorMessage="Invalid character item id")
    party_instances = await request.ctx.profile.find_item_by_template_id("Party:Instance")
    for party_instance in party_instances:
        party = await request.ctx.profile.get_item_by_guid(party_instance)
        if hero_item["guid"] in party["attributes"]["members"]:
            party["attributes"]["members"].remove(hero_item["guid"])
            await request.ctx.profile.change_item_attribute(party_instance, "members", party["attributes"]["members"])
    return sanic.response.json(
        await request.ctx.profile.construct_response(request.ctx.profile_id, request.ctx.rvn,
                                                    request.ctx.profile_id))
