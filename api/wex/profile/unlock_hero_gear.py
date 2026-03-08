"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles unlocking hero gear.
"""

import sanic

from utils import types
from utils.exceptions import errors
from utils.utils import authorized as auth, load_datatable, load_character_data

from utils.sanic_gzip import Compress

compress = Compress()
wex_profile_unlock_hero_gear = sanic.Blueprint("wex_profile_unlock_hero_gear")


# https://github.com/dippyshere/battle-breakers-documentation/blob/main/docs/World%20Explorers%20Service/wex/api/game/v2/profile/accountId/UnlockHeroGear.md
@wex_profile_unlock_hero_gear.route("/<accountId>/UnlockHeroGear", methods=["POST"])
@auth(strict=True)
@compress.compress()
async def unlock_hero_gear(request: types.BBProfileRequest, accountId: str) -> sanic.response.JSONResponse:
    """
    This endpoint is used to unlock hero gear
    :param request: The request object
    :param accountId: The account id
    :return: The modified profile
    """
    hero_item = await request.ctx.profile.get_item_by_guid(request.json.get("heroItemId"))
    if not hero_item.get("templateId").startswith("Character:"):
        raise errors.com.epicgames.world_explorers.bad_request(errorMessage="Invalid character item id")
    if hero_item["attributes"]["sidekick_unlocked"]:
        raise errors.com.epicgames.world_explorers.service_not_required(errorMessage="Weapon already unlocked")
    hero_data = await load_character_data(hero_item["templateId"])
    consumed_items = (await load_datatable((await load_datatable(
        hero_data[0]["Properties"]["HeroGearInfo"]["AssetPathName"].replace("/Game/", "Content/").split(".")[0]))[0][
                                               "Properties"]["HeroGearSlotRecipe"][
                                               "ObjectPath"].replace("WorldExplorers/", "").split(".")[
                                               0]))[0]["Properties"]["ConsumedItems"]
    for consumed_item in consumed_items:
        match consumed_item.get("ItemDefinition", "").get("ObjectName"):
            case "WExpGenericAccountItemDefinition'Reagent_Misc_CeremonialSword'":
                await request.ctx.profile.consume_item("Reagent:Reagent_Misc_CeremonialSword", consumed_item["Count"])
            case "WExpGenericAccountItemDefinition'Reagent_Misc_CeremonialShield'":
                await request.ctx.profile.consume_item("Reagent:Reagent_Misc_CeremonialShield", consumed_item["Count"])
            case "WExpGenericAccountItemDefinition'Reagent_Shared_MysteryGoo'":
                await request.ctx.profile.consume_item("Reagent:Reagent_Shared_MysteryGoo", consumed_item["Count"])
            case _:
                raise errors.com.epicgames.world_explorers.bad_request(errorMessage="Invalid consumed item")
    await request.ctx.profile.change_item_attribute(request.json.get("heroItemId"), "sidekick_unlocked", True)
    return sanic.response.json(
        await request.ctx.profile.construct_response(request.ctx.profile_id, request.ctx.rvn,
                                                     request.ctx.profile_revisions)
    )
