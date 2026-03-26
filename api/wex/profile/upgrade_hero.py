"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles upgrading heroes.
"""

import sanic
import sanic_ext

from utils import types
from utils.enums import ProfileType
from utils.exceptions import errors
from utils.utils import authorized as auth, load_datatable, get_path_from_template_id, extract_version_info
from utils.validation import MCPValidation, MCPQueryValidation

from utils.sanic_gzip import Compress

compress = Compress()
wex_profile_upgrade_hero = sanic.Blueprint("wex_profile_upgrade_hero")


# https://github.com/dippyshere/battle-breakers-documentation/blob/main/docs/World%20Explorers%20Service/wex/api/game/v2/profile/accountId/UpgradeHero.md
@wex_profile_upgrade_hero.route("/<accountId>/UpgradeHero", methods=["POST"])
@auth(strict=True)
@sanic_ext.validate(json=MCPValidation.UpgradeHero, query=MCPQueryValidation.MCPProfile0)
@compress.compress()
async def upgrade_hero(request: types.BBProfileRequest, accountId: str,
                       body: MCPValidation.UpgradeHero,
                       query: MCPQueryValidation.MCPProfile0) -> sanic.response.JSONResponse:
    """
    This endpoint is used to upgrade heroes
    :param request: The request object
    :param accountId: The account id
    :param body: The request body
    :param query: The query arguments
    :return: The modified profile
    """
    # TODO: validation
    request_body = body.model_dump()
    gold_id = (await request.ctx.profile.find_item_by_template_id("Currency:Gold"))[0]
    current_gold = (await request.ctx.profile.get_item_by_guid(gold_id))["quantity"]
    silver_id = await request.ctx.profile.find_item_by_template_id("Ore:Ore_Silver")
    current_silver = (await request.ctx.profile.get_item_by_guid(silver_id[0])).get("quantity", 0)
    magicite_id = await request.ctx.profile.find_item_by_template_id("Ore:Ore_Magicite")
    current_magicite = (await request.ctx.profile.get_item_by_guid(magicite_id[0])).get("quantity", 0)
    iron_id = await request.ctx.profile.find_item_by_template_id("Ore:Ore_Iron")
    current_iron = (await request.ctx.profile.get_item_by_guid(iron_id[0])).get("quantity", 0)
    if request_body.get("bIsInPit"):
        hero_item = await request.ctx.profile.get_item_by_guid(request_body.get("heroItemId"), ProfileType.MONSTERPIT)
    else:
        hero_item = await request.ctx.profile.get_item_by_guid(request_body.get("heroItemId"))
    if not hero_item.get("templateId").startswith("Character:"):
        raise errors.com.epicgames.world_explorers.bad_request(errorMessage="Invalid character item id")
    hero_upgrades = hero_item["attributes"]["upgrades"]
    # [
    #     0,  UpgradePotion:UpgradeStrengthMinor
    #     0,  UpgradePotion:UpgradeStrengthMajor
    #     0,  UpgradePotion:UpgradeHealthMinor
    #     0,  UpgradePotion:UpgradeHealthMajor
    #     0,  UpgradePotion:UpgradeMana
    #     0,  WeaponLevel
    #     0,  WeaponStars
    #     0,  ArmorLevel
    #     0   ArmorStars
    # ]
    for potion_upgrade in request_body.get("potionItems"):
        match potion_upgrade.get("templateId"):
            case "UpgradePotion:UpgradeStrengthMinor":
                hero_upgrades[0] += potion_upgrade["quantity"]
            case "UpgradePotion:UpgradeStrengthMajor":
                hero_upgrades[1] += potion_upgrade["quantity"]
            case "UpgradePotion:UpgradeHealthMinor":
                hero_upgrades[2] += potion_upgrade["quantity"]
            case "UpgradePotion:UpgradeHealthMajor":
                hero_upgrades[3] += potion_upgrade["quantity"]
            case "UpgradePotion:UpgradeMana":
                hero_upgrades[4] += potion_upgrade["quantity"]
            case _:
                raise errors.com.epicgames.world_explorers.bad_request(errorMessage="Invalid potion item template id")
        potion_cost = (await load_datatable(
            (await get_path_from_template_id(potion_upgrade.get("templateId"))).replace(
                "res/battle-breakers-data/WorldExplorers/", "").replace(".json", "").replace("\\", "/")))[0][
            "Properties"][
            "ConsumptionCostGold"]
        for _ in range(potion_upgrade.get("quantity")):
            if current_gold < potion_cost:
                break
            current_gold -= potion_cost
            await request.ctx.profile.consume_item("Currency:Gold", potion_cost)
            await request.ctx.profile.consume_item(potion_upgrade.get("templateId"))
    for weapon_upgrade in request_body.get("weaponUpgrades"):
        match weapon_upgrade.get("upgradeType"):
            case "WeaponLevel":
                current_level = hero_upgrades[5]
                hero_upgrades[5] += weapon_upgrade["numUpgrades"]
                promotion_table = \
                    (await load_datatable("Content/Recipes/PT_WeaponLevel"))[0]["Properties"][
                        "RankRecipes"]
            case "WeaponStars":
                current_level = hero_upgrades[6]
                hero_upgrades[6] += weapon_upgrade["numUpgrades"]
                promotion_table = \
                    (await load_datatable("Content/Recipes/PT_WeaponTier"))[0]["Properties"][
                        "RankRecipes"]
            case "ArmorLevel":
                current_level = hero_upgrades[7]
                hero_upgrades[7] += weapon_upgrade["numUpgrades"]
                promotion_table = \
                    (await load_datatable("Content/Recipes/PT_ArmorLevel"))[0]["Properties"][
                        "RankRecipes"]
            case "ArmorStars":
                current_level = hero_upgrades[8]
                hero_upgrades[8] += weapon_upgrade["numUpgrades"]
                promotion_table = \
                    (await load_datatable("Content/Recipes/PT_ArmorTier"))[0]["Properties"][
                        "RankRecipes"]
            case _:
                raise errors.com.epicgames.world_explorers.bad_request(errorMessage="Invalid weapon upgrade type")
        for i in range(current_level, current_level + weapon_upgrade.get("numUpgrades")):
            consumed_item = (await load_datatable(
                promotion_table[i].get("AssetPathName").replace("/Game/", "Content/").split(".")[0]))[0]["Properties"][
                "ConsumedItems"][0]
            match consumed_item.get("ItemDefinition", "").get("ObjectName"):
                case "WExpGenericAccountItemDefinition'Ore_Silver'":
                    if current_silver < consumed_item["Count"]:
                        break
                    await request.ctx.profile.consume_item("Ore:Ore_Silver", consumed_item["Count"])
                    current_silver -= consumed_item["Count"]
                case "WExpGenericAccountItemDefinition'Ore_Magicite'":
                    if current_magicite < consumed_item["Count"]:
                        break
                    await request.ctx.profile.consume_item("Ore:Ore_Magicite", consumed_item["Count"])
                    current_magicite -= consumed_item["Count"]
                case "WExpGenericAccountItemDefinition'Ore_Iron'":
                    if current_iron < consumed_item["Count"]:
                        break
                    await request.ctx.profile.consume_item("Ore:Ore_Iron", consumed_item["Count"])
                    current_iron -= consumed_item["Count"]
                case _:
                    raise errors.com.epicgames.world_explorers.bad_request(errorMessage="Invalid item to consume")
    if request_body.get("bIsInPit"):
        await request.ctx.profile.change_item_attribute(request_body.get("heroItemId"), "upgrades", hero_upgrades,
                                                        ProfileType.MONSTERPIT)
    else:
        await request.ctx.profile.change_item_attribute(request_body.get("heroItemId"), "upgrades", hero_upgrades)
    return sanic.response.json(
        await request.ctx.profile.construct_response(request.ctx.profile_id, request.ctx.rvn,
                                                     request.ctx.profile_revisions,
                                                     (await extract_version_info(request.headers.get("User-Agent")))[
                                                         -1])
    )
