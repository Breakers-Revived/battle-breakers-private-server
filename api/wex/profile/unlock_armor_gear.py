"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles unlocking armor gear.
"""

import sanic
import sanic_ext

from utils import types
from utils.exceptions import errors
from utils.utils import authorized as auth, load_datatable, load_character_data, extract_version_info
from utils.validation import MCPValidation, MCPQueryValidation

from utils.sanic_gzip import Compress

compress = Compress()
wex_profile_unlock_armor_gear = sanic.Blueprint("wex_profile_unlock_armor_gear")


# https://github.com/dippyshere/battle-breakers-documentation/blob/main/docs/World%20Explorers%20Service/wex/api/game/v2/profile/accountId/UnlockArmorGear.md
@wex_profile_unlock_armor_gear.route("/<accountId>/UnlockArmorGear", methods=["POST"])
@auth(strict=True)
@sanic_ext.validate(json=MCPValidation.UnlockArmorGear, query=MCPQueryValidation.MCPProfile0)
@compress.compress()
async def unlock_armor_gear(request: types.BBProfileRequest, accountId: str,
                            body: MCPValidation.UnlockArmorGear,
                            query: MCPQueryValidation.MCPProfile0) -> sanic.response.JSONResponse:
    """
    This endpoint is used to unlock armor gear
    :param request: The request object
    :param accountId: The account id
    :param body: The request body
    :param query: The query arguments
    :return: The modified profile
    """
    request_body = body.model_dump()
    hero_item = await request.ctx.profile.get_item_by_guid(request_body.get("heroItemId"))
    if not hero_item.get("templateId").startswith("Character:"):
        raise errors.com.epicgames.world_explorers.bad_request(errorMessage="Invalid character item id")
    if hero_item["attributes"]["armor_unlocked"]:
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
    await request.ctx.profile.change_item_attribute(request_body.get("heroItemId"), "armor_unlocked", True)
    return sanic.response.json(
        await request.ctx.profile.construct_response(request.ctx.profile_id, request.ctx.rvn,
                                                     request.ctx.profile_revisions,
                                                     (await extract_version_info(request.headers.get("User-Agent")))[
                                                         -1])
    )
