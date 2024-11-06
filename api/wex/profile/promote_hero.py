"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles promoting a hero.
"""

import sanic

from utils import types
from utils.enums import ProfileType
from utils.exceptions import errors
from utils.utils import authorized as auth, load_datatable, get_path_from_template_id, get_template_id_from_path, \
    load_character_data

from utils.sanic_gzip import Compress

compress = Compress()
wex_profile_promote_hero = sanic.Blueprint("wex_profile_promote_hero")


# https://github.com/dippyshere/battle-breakers-documentation/blob/main/docs/World%20Explorers%20Service/wex/api/game/v2/profile/accountId/PromoteHero.md
@wex_profile_promote_hero.route("/<accountId>/PromoteHero", methods=["POST"])
@auth(strict=True)
@compress.compress()
async def promote_hero(request: types.BBProfileRequest, accountId: str) -> sanic.response.JSONResponse:
    """
    This endpoint is used to promote a hero.
    :param request: The request object
    :param accountId: The account id
    :return: The modified profile
    """
    # errors.com.epicgames.modules.gameplayutils.recipe_failed - Unable to promote
    # TODO: investigate when prestigePromote is true
    # TODO: validation
    if request.json.get("bIsInPit"):
        hero_item = await request.ctx.profile.get_item_by_guid(request.json.get("heroItemId"), ProfileType.MONSTERPIT)
    else:
        hero_item = await request.ctx.profile.get_item_by_guid(request.json.get("heroItemId"))
    if hero_item is None:
        raise errors.com.epicgames.modules.gameplayutils.recipe_failed(errorMessage="Invalid hero item id")
    hero_data = await load_character_data(hero_item["templateId"])
    promotion_table = await load_datatable(
        hero_data[0]["Properties"]["PromotionTable"]["AssetPathName"].replace("/Game/", "Content/").split(".")[0])
    if len(promotion_table[0]["Properties"]["RankRecipes"]) <= hero_item["attributes"]["rank"]:
        raise errors.com.epicgames.modules.gameplayutils.recipe_failed(errorMessage="Hero is already at max promotion")
    promotion_recipe = (await load_datatable(
        promotion_table[0]["Properties"]["RankRecipes"][hero_item["attributes"]["rank"]]["AssetPathName"].replace("/Game/", "Content/").split(".")[
            0]))[0]["Properties"]
    # There is a check for account level, but since it only ever requires above level 0, it is not necessary
    pending_items = []
    for consumed_item in promotion_recipe["ConsumedItems"]:
        consumed_item_id = (await request.ctx.profile.find_item_by_template_id(
            await get_template_id_from_path(consumed_item["ItemDefinition"]["ObjectPath"])))[0]
        consumed_item_quantity = (await request.ctx.profile.get_item_by_guid(consumed_item_id))["quantity"]
        if consumed_item_quantity < consumed_item["Count"]:
            raise errors.com.epicgames.modules.gameplayutils.recipe_failed(
                errorMessage=f"Not enough {consumed_item['ItemDefinition']['ObjectName']}")
        pending_items.append({
            "itemId": consumed_item_id,
            "quantity": consumed_item_quantity - consumed_item["Count"]
        })
    if request.json.get("bIsInPit"):
        await request.ctx.profile.change_item_attribute(request.json.get("heroItemId"), "rank",
                                                        hero_item["attributes"]["rank"] + 1, ProfileType.MONSTERPIT)
    else:
        await request.ctx.profile.change_item_attribute(request.json.get("heroItemId"), "rank",
                                                        hero_item["attributes"]["rank"] + 1)
    for pending_item in pending_items:
        await request.ctx.profile.change_item_quantity(pending_item["itemId"], pending_item["quantity"])
    # TODO: chest activity
    return sanic.response.json(
        await request.ctx.profile.construct_response(request.ctx.profile_id, request.ctx.rvn,
                                                     request.ctx.profile_revisions)
    )
