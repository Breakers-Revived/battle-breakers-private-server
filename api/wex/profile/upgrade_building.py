"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles upgrading buildings.
"""

import sanic
import sanic.log
import sanic_ext

from utils import types
from utils.exceptions import errors
from utils.utils import authorized as auth, get_template_id_from_path, load_datatable, extract_version_info
from utils.validation import MCPValidation, MCPQueryValidation

from utils.sanic_gzip import Compress

compress = Compress()
wex_profile_upgrade_building = sanic.Blueprint("wex_profile_upgrade_building")


# https://github.com/dippyshere/battle-breakers-documentation/blob/main/docs/World%20Explorers%20Service/wex/api/game/v2/profile/accountId/UpgradeBuilding.md
@wex_profile_upgrade_building.route("/<accountId>/UpgradeBuilding", methods=["POST"])
@auth(strict=True)
@sanic_ext.validate(json=MCPValidation.UpgradeBuilding, query=MCPQueryValidation.MCPProfile0)
@compress.compress()
async def upgrade_building(request: types.BBProfileRequest, accountId: str,
                           body: MCPValidation.UpgradeBuilding,
                           query: MCPQueryValidation.MCPProfile0) -> sanic.response.JSONResponse:
    """
    This endpoint is used to upgrade buildings
    :param request: The request object
    :param accountId: The account id
    :param body: The request body
    :param query: The query arguments
    :return: The modified profile
    """
    # TODO: modify chest activity
    request_body = body.model_dump()
    building_item = await request.ctx.profile.get_item_by_guid(request_body.get("buildingItemId"),
                                                               request.ctx.profile_id)
    if not building_item.get("templateId").startswith("HqBuilding:"):
        raise errors.com.epicgames.world_explorers.bad_request(errorMessage="Invalid building item id")
    promotion_table = (await load_datatable((await load_datatable(
        (await load_datatable(f"Content/Menus/Headquarters/{building_item['templateId'].split(':')[-1]}"))[0][
            "Properties"]["PromotionTable"]["ObjectPath"].replace("WorldExplorers/", "").split(".")[0]))[0][
                                                "Properties"]["RankRecipes"][building_item["attributes"]["level"]][
                                                "AssetPathName"].replace("/Game/", "Content/").split(".")[0]))[0][
        "Properties"]
    for item in promotion_table["ConsumedItems"]:
        item_template_id = await get_template_id_from_path(item["ItemDefinition"]["ObjectPath"])
        if item_template_id is None:
            raise errors.com.epicgames.world_explorers.bad_request(errorMessage="Invalid consumed item")
        await request.ctx.profile.consume_item(item_template_id, item["Count"])
        sanic.log.logger.debug(f"Cost: {item['Count']} {item_template_id}")
    if promotion_table.get("MtxCost") is not None:
        # TODO: enforce account level
        await request.ctx.profile.consume_mtx(promotion_table["MtxCost"])
    await request.ctx.profile.change_item_attribute(request_body.get("buildingItemId"), "level",
                                                    building_item["attributes"]["level"] + 1, request.ctx.profile_id)
    sanic.log.logger.debug(
        f"Upgraded building {request_body.get('buildingItemId')} to level {building_item['attributes']['level'] + 1}")
    return sanic.response.json(
        await request.ctx.profile.construct_response(request.ctx.profile_id, request.ctx.rvn,
                                                     request.ctx.profile_revisions,
                                                     (await extract_version_info(request.headers.get("User-Agent")))[
                                                         -1])
    )
