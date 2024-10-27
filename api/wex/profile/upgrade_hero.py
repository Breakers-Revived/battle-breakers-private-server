"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles upgrading heroes.
"""

import sanic

from utils import types
from utils.enums import ProfileType
from utils.exceptions import errors
from utils.utils import authorized as auth, load_datatable, get_path_from_template_id

from utils.sanic_gzip import Compress

compress = Compress()
wex_profile_upgrade_hero = sanic.Blueprint("wex_profile_upgrade_hero")


# https://github.com/dippyshere/battle-breakers-documentation/blob/main/docs/World%20Explorers%20Service/wex/api/game/v2/profile/accountId/UpgradeHero.md
@wex_profile_upgrade_hero.route("/<accountId>/UpgradeHero", methods=["POST"])
@auth(strict=True)
@compress.compress()
async def upgrade_hero(request: types.BBProfileRequest, accountId: str) -> sanic.response.JSONResponse:
    """
    This endpoint is used to upgrade heroes
    :param request: The request object
    :param accountId: The account id
    :return: The modified profile
    """
    # TODO: validation
    gold_id = (await request.ctx.profile.find_item_by_template_id("Currency:Gold"))[0]
    current_gold = (await request.ctx.profile.get_item_by_guid(gold_id))["quantity"]
    silver_id = (await request.ctx.profile.find_item_by_template_id("Ore:Ore_Silver"))[0]
    current_silver = (await request.ctx.profile.get_item_by_guid(silver_id))["quantity"]
    magicite_id = (await request.ctx.profile.find_item_by_template_id("Ore:Ore_Magicite"))[0]
    current_magicite = (await request.ctx.profile.get_item_by_guid(magicite_id))["quantity"]
    iron_id = (await request.ctx.profile.find_item_by_template_id("Ore:Ore_Iron"))[0]
    current_iron = (await request.ctx.profile.get_item_by_guid(iron_id))["quantity"]
    if request.json.get("bIsInPit"):
        hero_item = await request.ctx.profile.get_item_by_guid(request.json.get("heroItemId"), ProfileType.MONSTERPIT)
    else:
        hero_item = await request.ctx.profile.get_item_by_guid(request.json.get("heroItemId"))
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
    for potion_upgrade in request.json.get("potionItems"):
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
        potion_guid = (await request.ctx.profile.find_item_by_template_id(potion_upgrade.get("templateId")))[0]
        current_potion_quantity = (await request.ctx.profile.get_item_by_guid(potion_guid))["quantity"]
        if current_potion_quantity < potion_upgrade.get("quantity"):
            raise errors.com.epicgames.world_explorers.bad_request(
                errorMessage=f"Not enough {potion_upgrade.get('templateId')}")
        potion_cost = (await load_datatable(
            (await get_path_from_template_id(potion_upgrade.get("templateId"))).replace(
                "res/battle-breakers-data/WorldExplorers/", "").replace(".json", "").replace("\\", "/")))[0]["Properties"][
            "ConsumptionCostGold"]
        for _ in range(potion_upgrade.get("quantity")):
            if current_gold < potion_cost:
                break
            await request.ctx.profile.change_item_quantity(gold_id, current_gold - potion_cost)
            current_gold -= potion_cost
            await request.ctx.profile.change_item_quantity(potion_guid, current_potion_quantity - 1)
            current_potion_quantity -= 1
    for weapon_upgrade in request.json.get("weaponUpgrades"):
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
                    await request.ctx.profile.change_item_quantity(silver_id,
                                                                   current_silver - consumed_item["Count"])
                    current_silver -= consumed_item["Count"]
                case "WExpGenericAccountItemDefinition'Ore_Magicite'":
                    if current_magicite < consumed_item["Count"]:
                        break
                    await request.ctx.profile.change_item_quantity(magicite_id,
                                                                   current_magicite - consumed_item["Count"])
                    current_magicite -= consumed_item["Count"]
                case "WExpGenericAccountItemDefinition'Ore_Iron'":
                    if current_iron < consumed_item["Count"]:
                        break
                    await request.ctx.profile.change_item_quantity(iron_id, current_iron - consumed_item["Count"])
                    current_iron -= consumed_item["Count"]
                case _:
                    raise errors.com.epicgames.world_explorers.bad_request(errorMessage="Invalid item to consume")
    if request.json.get("bIsInPit"):
        await request.ctx.profile.change_item_attribute(request.json.get("heroItemId"), "upgrades", hero_upgrades,
                                                        ProfileType.MONSTERPIT)
    else:
        await request.ctx.profile.change_item_attribute(request.json.get("heroItemId"), "upgrades", hero_upgrades)
    return sanic.response.json(
        await request.ctx.profile.construct_response(request.ctx.profile_id, request.ctx.rvn,
                                                     request.ctx.profile_revisions)
    )
