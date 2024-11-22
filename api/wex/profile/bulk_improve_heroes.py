"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles bulk improve heroes (used for auto upgrade)
"""

import sanic

from utils import types
from utils.exceptions import errors
from utils.utils import authorized as auth, load_datatable, get_path_from_template_id

from utils.sanic_gzip import Compress

compress = Compress()
wex_profile_bulk_improve_heroes = sanic.Blueprint("wex_profile_bulk_improve_heroes")


# https://github.com/dippyshere/battle-breakers-documentation/blob/main/docs/World%20Explorers%20Service/wex/api/game/v2/profile/accountId/BulkImproveHeroes.md
@wex_profile_bulk_improve_heroes.route("/<accountId>/BulkImproveHeroes", methods=["POST"])
@auth(strict=True)
@compress.compress()
async def bulk_improve_heroes(request: types.BBProfileRequest, accountId: str) -> sanic.response.JSONResponse:
    """
    This endpoint is used to upgrade heroes in bulk
    :param request: The request object
    :param accountId: The account id
    :return: The modified profile
    """
    # TODO: validation
    gold_id = (await request.ctx.profile.find_item_by_template_id("Currency:Gold"))[0]
    current_gold = (await request.ctx.profile.get_item_by_guid(gold_id))["quantity"]
    silver_id = await request.ctx.profile.find_item_by_template_id("Ore:Ore_Silver")
    current_silver = (await request.ctx.profile.get_item_by_guid(silver_id[0])).get("quantity", 0)
    magicite_id = await request.ctx.profile.find_item_by_template_id("Ore:Ore_Magicite")
    current_magicite = (await request.ctx.profile.get_item_by_guid(magicite_id[0])).get("quantity", 0)
    iron_id = await request.ctx.profile.find_item_by_template_id("Ore:Ore_Iron")
    current_iron = (await request.ctx.profile.get_item_by_guid(iron_id[0])).get("quantity", 0)
    xp_guid = await request.ctx.profile.find_item_by_template_id("Currency:HeroXp_Basic")
    current_xp = (await request.ctx.profile.get_item_by_guid(xp_guid[0])).get("quantity", 0)
    xp_datatable = (await load_datatable("Content/Balance/Datatables/XPUnitLevels"))[0]["Rows"][
        "UnitXPTNLNormal"]["Keys"]
    strength_ma_potion_guid = await request.ctx.profile.find_item_by_template_id("UpgradePotion:UpgradeStrengthMinor")
    strength_ma_potion_quantity = (await request.ctx.profile.get_item_by_guid(strength_ma_potion_guid[0])).get("quantity", 0)
    strength_mi_potion_guid = await request.ctx.profile.find_item_by_template_id("UpgradePotion:UpgradeStrengthMajor")
    strength_mi_potion_quantity = (await request.ctx.profile.get_item_by_guid(strength_mi_potion_guid[0])).get("quantity", 0)
    health_ma_potion_guid = await request.ctx.profile.find_item_by_template_id("UpgradePotion:UpgradeHealthMinor")
    health_ma_potion_quantity = (await request.ctx.profile.get_item_by_guid(health_ma_potion_guid[0])).get("quantity", 0)
    health_mi_potion_guid = await request.ctx.profile.find_item_by_template_id("UpgradePotion:UpgradeHealthMajor")
    health_mi_potion_quantity = (await request.ctx.profile.get_item_by_guid(health_mi_potion_guid[0])).get("quantity", 0)
    mana_potion_guid = await request.ctx.profile.find_item_by_template_id("UpgradePotion:UpgradeMana")
    mana_potion_quantity = (await request.ctx.profile.get_item_by_guid(mana_potion_guid[0])).get("quantity", 0)
    for upgrade in request.json.get("detail"):
        hero_item = await request.ctx.profile.get_item_by_guid(upgrade["heroItemId"])
        hero_upgrades = hero_item["attributes"]["upgrades"]
        # potions
        for potion_upgrade in upgrade["potionItems"]:
            potion_cost = (await load_datatable(
                (await get_path_from_template_id(potion_upgrade.get("templateId"))).replace(
                    "res/battle-breakers-data/WorldExplorers/", "").replace(".json", "").replace("\\", "/")))[0]["Properties"][
                "ConsumptionCostGold"]
            match potion_upgrade.get("templateId"):
                case "UpgradePotion:UpgradeStrengthMinor":
                    if potion_upgrade["quantity"] > strength_ma_potion_quantity:
                        raise errors.com.epicgames.world_explorers.bad_request(
                            errorMessage=f"Invalid quantity for {potion_upgrade.get('templateId')}")
                    hero_upgrades[0] += potion_upgrade["quantity"]
                    for _ in range(potion_upgrade.get("quantity")):
                        if current_gold < potion_cost:
                            break
                        await request.ctx.profile.change_item_quantity(gold_id, current_gold - potion_cost)
                        current_gold -= potion_cost
                        await request.ctx.profile.change_item_quantity(strength_mi_potion_guid[0],
                                                                       strength_mi_potion_quantity - 1)
                        strength_mi_potion_quantity -= 1
                case "UpgradePotion:UpgradeStrengthMajor":
                    if potion_upgrade["quantity"] > strength_ma_potion_quantity:
                        raise errors.com.epicgames.world_explorers.bad_request(
                            errorMessage=f"Invalid quantity for {potion_upgrade.get('templateId')}")
                    hero_upgrades[1] += potion_upgrade["quantity"]
                    for _ in range(potion_upgrade.get("quantity")):
                        if current_gold < potion_cost:
                            break
                        await request.ctx.profile.change_item_quantity(gold_id, current_gold - potion_cost)
                        current_gold -= potion_cost
                        await request.ctx.profile.change_item_quantity(strength_ma_potion_guid[0],
                                                                       strength_ma_potion_quantity - 1)
                        strength_ma_potion_quantity -= 1
                case "UpgradePotion:UpgradeHealthMinor":
                    if potion_upgrade["quantity"] > health_ma_potion_quantity:
                        raise errors.com.epicgames.world_explorers.bad_request(
                            errorMessage=f"Invalid quantity for {potion_upgrade.get('templateId')}")
                    hero_upgrades[2] += potion_upgrade["quantity"]
                    for _ in range(potion_upgrade.get("quantity")):
                        if current_gold < potion_cost:
                            break
                        await request.ctx.profile.change_item_quantity(gold_id, current_gold - potion_cost)
                        current_gold -= potion_cost
                        await request.ctx.profile.change_item_quantity(health_mi_potion_guid[0],
                                                                       health_mi_potion_quantity - 1)
                        health_mi_potion_quantity -= 1
                case "UpgradePotion:UpgradeHealthMajor":
                    if potion_upgrade["quantity"] > health_ma_potion_quantity:
                        raise errors.com.epicgames.world_explorers.bad_request(
                            errorMessage=f"Invalid quantity for {potion_upgrade.get('templateId')}")
                    hero_upgrades[3] += potion_upgrade["quantity"]
                    for _ in range(potion_upgrade.get("quantity")):
                        await request.ctx.profile.change_item_quantity(gold_id, current_gold - potion_cost)
                        current_gold -= potion_cost
                        await request.ctx.profile.change_item_quantity(health_ma_potion_guid[0],
                                                                       health_ma_potion_quantity - 1)
                        health_ma_potion_quantity -= 1
                case "UpgradePotion:UpgradeMana":
                    if potion_upgrade["quantity"] > mana_potion_quantity:
                        raise errors.com.epicgames.world_explorers.bad_request(
                            errorMessage=f"Invalid quantity for {potion_upgrade.get('templateId')}")
                    hero_upgrades[4] += potion_upgrade["quantity"]
                    for _ in range(potion_upgrade.get("quantity")):
                        await request.ctx.profile.change_item_quantity(gold_id, current_gold - potion_cost)
                        current_gold -= potion_cost
                        await request.ctx.profile.change_item_quantity(mana_potion_guid[0],
                                                                       mana_potion_quantity - 1)
                        mana_potion_quantity -= 1
                case _:
                    raise errors.com.epicgames.world_explorers.bad_request(
                        errorMessage="Invalid potion item template id")
        # weapons
        for weapon_upgrade in upgrade["weaponUpgrades"]:
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
                    promotion_table[i].get("AssetPathName").replace("/Game/", "Content/").split(".")[0]))[0][
                    "Properties"]["ConsumedItems"][0]
                match consumed_item.get("ItemDefinition", "").get("ObjectName"):
                    case "WExpGenericAccountItemDefinition'Ore_Silver'":
                        if current_silver < consumed_item["Count"]:
                            break
                        await request.ctx.profile.change_item_quantity(silver_id[0],
                                                                       current_silver - consumed_item["Count"])
                        current_silver -= consumed_item["Count"]
                    case "WExpGenericAccountItemDefinition'Ore_Magicite'":
                        if current_magicite < consumed_item["Count"]:
                            break
                        await request.ctx.profile.change_item_quantity(magicite_id[0],
                                                                       current_magicite - consumed_item["Count"])
                        current_magicite -= consumed_item["Count"]
                    case "WExpGenericAccountItemDefinition'Ore_Iron'":
                        if current_iron < consumed_item["Count"]:
                            break
                        await request.ctx.profile.change_item_quantity(iron_id[0], current_iron - consumed_item["Count"])
                        current_iron -= consumed_item["Count"]
                    case _:
                        raise errors.com.epicgames.world_explorers.bad_request(errorMessage="Invalid item to consume")
        await request.ctx.profile.change_item_attribute(upgrade["heroItemId"], "upgrades", hero_upgrades)
        # level
        current_hero_level = hero_item["attributes"]["level"]
        new_level = current_hero_level + upgrade["numLevelUps"]
        for i in range(current_hero_level, new_level):
            if current_xp < int(xp_datatable[i - 1]["Value"]):
                break
            await request.ctx.profile.change_item_quantity(xp_guid[0], current_xp - int(xp_datatable[i - 1]["Value"]))
            current_xp -= int(xp_datatable[i - 1]["Value"])
            await request.ctx.profile.change_item_attribute(upgrade["heroItemId"], "level", i + 1)
            await request.ctx.profile.add_notifications({
                "type": "CharacterLevelUp",
                "primary": False,
                "itemId": upgrade["heroItemId"],
                "level": i + 1
            })
    return sanic.response.json(
        await request.ctx.profile.construct_response(request.ctx.profile_id, request.ctx.rvn,
                                                     request.ctx.profile_revisions)
    )
