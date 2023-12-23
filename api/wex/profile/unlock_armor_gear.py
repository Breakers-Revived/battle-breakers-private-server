"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2023 by Alex Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the [TBD] license.

Handles unlocking armor gear.
"""

import sanic

from utils.exceptions import errors
from utils.utils import authorized as auth, load_datatable, load_character_data

from utils.sanic_gzip import Compress

compress = Compress()
wex_profile_unlock_armor_gear = sanic.Blueprint("wex_profile_unlock_armor_gear")


# https://github.com/dippyshere/battle-breakers-documentation/blob/main/docs/World%20Explorers%20Service/wex/api/game/v2/profile/accountId/UnlockArmorGear.md
@wex_profile_unlock_armor_gear.route("/<accountId>/UnlockArmorGear", methods=["POST"])
@auth(strict=True)
@compress.compress()
async def unlock_armor_gear(request: sanic.request.Request, accountId: str) -> sanic.response.JSONResponse:
    """
    This endpoint is used to unlock armor gear
    :param request: The request object
    :param accountId: The account id
    :return: The modified profile
    """
    hero_item = await request.ctx.profile.get_item_by_guid(request.json.get("heroItemId"))
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
    pending_items = []
    for consumed_item in consumed_items:
        match consumed_item.get("ItemDefinition", "").get("ObjectName"):
            case "WExpGenericAccountItemDefinition'Reagent_Misc_CeremonialSword'":
                consumed_item_guid = \
                    (await request.ctx.profile.find_item_by_template_id("Reagent:Reagent_Misc_CeremonialSword"))[0]
            case "WExpGenericAccountItemDefinition'Reagent_Misc_CeremonialShield'":
                consumed_item_guid = \
                    (await request.ctx.profile.find_item_by_template_id("Reagent:Reagent_Misc_CeremonialShield"))[0]
            case "WExpGenericAccountItemDefinition'Reagent_Shared_MysteryGoo'":
                consumed_item_guid = \
                    (await request.ctx.profile.find_item_by_template_id("Reagent:Reagent_Shared_MysteryGoo"))[0]
            case _:
                raise errors.com.epicgames.world_explorers.bad_request(errorMessage="Invalid consumed item")
        current_quantity = (await request.ctx.profile.get_item_by_guid(consumed_item_guid))["quantity"]
        if current_quantity < consumed_item["Count"]:
            raise errors.com.epicgames.world_explorers.bad_request(
                errorMessage=f"Not enough {consumed_item.get('ItemDefinition', '').get('ObjectName')}")
        pending_items.append({
            "itemGuid": consumed_item_guid,
            "quantity": current_quantity - consumed_item["Count"]
        })
    for pending_item in pending_items:
        await request.ctx.profile.change_item_quantity(pending_item["itemGuid"], pending_item["quantity"])
    await request.ctx.profile.change_item_attribute(request.json.get("heroItemId"), "armor_unlocked", True)
    return sanic.response.json(
        await request.ctx.profile.construct_response(request.ctx.profile_id, request.ctx.rvn,
                                                     request.ctx.profile_revisions)
    )
