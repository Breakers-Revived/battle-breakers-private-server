"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles foiling hero
"""

import sanic

from utils import types
from utils.enums import ProfileType
from utils.exceptions import errors
from utils.utils import authorized as auth, load_datatable, load_character_data

from utils.sanic_gzip import Compress

compress = Compress()
wex_profile_foil_hero = sanic.Blueprint("wex_profile_foil_hero")


# https://github.com/dippyshere/battle-breakers-documentation/blob/main/docs/World%20Explorers%20Service/wex/api/game/v2/profile/accountId/FoilHero.md
@wex_profile_foil_hero.route("/<accountId>/FoilHero", methods=["POST"])
@auth(strict=True)
@compress.compress()
async def foil_hero(request: types.BBProfileRequest, accountId: str) -> sanic.response.JSONResponse:
    """
    This endpoint is used to foil heroes
    :param request: The request object
    :param accountId: The account id
    :return: The modified profile
    """
    foil_guid = (await request.ctx.profile.find_item_by_template_id("Reagent:Reagent_Foil"))[0]
    current_foil_count = (await request.ctx.profile.get_item_by_guid(foil_guid))["quantity"]
    if request.json.get("bIsInPit"):
        character_data = await load_character_data(
            (await request.ctx.profile.get_item_by_guid(request.json.get("heroItemId"), ProfileType.MONSTERPIT))[
                "templateId"])
        if not character_data[0]["Properties"].get("FoilTable"):
            raise errors.com.epicgames.world_explorers.bad_request(errorMessage="Hero cannot be foiled")
        foil_table = character_data[0]["Properties"]["FoilTable"]["AssetPathName"].replace("/Game/", "Content/").split(
            ".")[0]
        foil_cost = (await load_datatable((await load_datatable(foil_table))[0]["Properties"]["RankRecipes"][0][
                                              "AssetPathName"].replace("/Game/", "Content/").split(".")[0]))[0][
            "Properties"]["ConsumedItems"][0]["Count"]
        if current_foil_count < foil_cost:
            raise errors.com.epicgames.world_explorers.bad_request(errorMessage="Not enough foil")
        # TODO: mark pit as dirty and recalculate power
        await request.ctx.profile.change_item_attribute(request.json.get("heroItemId"), "foil_lvl", 1,
                                                        ProfileType.MONSTERPIT)
    else:
        character_data = await load_character_data(
            (await request.ctx.profile.get_item_by_guid(request.json.get("heroItemId")))["templateId"])
        if not character_data[0]["Properties"].get("FoilTable"):
            raise errors.com.epicgames.world_explorers.bad_request(errorMessage="Hero cannot be foiled")
        foil_table = character_data[0]["Properties"]["FoilTable"]["AssetPathName"].replace("/Game/", "Content/").split(
            ".")[0]
        foil_cost = (await load_datatable((await load_datatable(foil_table))[0]["Properties"]["RankRecipes"][0][
                                              "AssetPathName"].replace("/Game/", "Content/").split(".")[0]))[0][
            "Properties"]["ConsumedItems"][0]["Count"]
        if current_foil_count < foil_cost:
            raise errors.com.epicgames.world_explorers.bad_request(errorMessage="Not enough foil")
        await request.ctx.profile.change_item_attribute(request.json.get("heroItemId"), "foil_lvl", 1)
    await request.ctx.profile.change_item_quantity(foil_guid, current_foil_count - foil_cost)
    # TODO: foil hero activity
    return sanic.response.json(
        await request.ctx.profile.construct_response(request.ctx.profile_id, request.ctx.rvn,
                                                     request.ctx.profile_revisions)
    )
    # {
    #   "changeType": "statModified",
    #   "name": "activity",
    #   "value": {
    #     "a": {
    #       "date": "2022-12-28T00:00:00.000Z",
    #       "claimed": false,
    #       "props": {
    #         "HeroAcquired": 1,
    #         "HeroFoil": 1,
    #         "BaseBonus": 10
    #       }
    #     },
    #     "b": {
    #       "date": "2022-12-27T00:00:00.000Z",
    #       "claimed": true,
    #       "props": {
    #         "BaseBonus": 10,
    #         "EnergySpent": 3
    #       }
    #     },
    #     "standardGift": 10
    #   }
    # }
