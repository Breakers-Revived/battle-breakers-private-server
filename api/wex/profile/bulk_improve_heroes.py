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
    gold_id = (await request.ctx.profile.find_item_by_template_id("Currency:Gold"))[0]
    current_gold = (await request.ctx.profile.get_item_by_guid(gold_id))["quantity"]
    silver_ids = await request.ctx.profile.find_item_by_template_id("Ore:Ore_Silver")
    silver_id = silver_ids[0] if silver_ids else None
    current_silver = (await request.ctx.profile.get_item_by_guid(silver_id)).get("quantity", 0) if silver_id else 0
    magicite_ids = await request.ctx.profile.find_item_by_template_id("Ore:Ore_Magicite")
    magicite_id = magicite_ids[0] if magicite_ids else None
    current_magicite = (await request.ctx.profile.get_item_by_guid(magicite_id)).get("quantity", 0) if magicite_id else 0
    iron_ids = await request.ctx.profile.find_item_by_template_id("Ore:Ore_Iron")
    iron_id = iron_ids[0] if iron_ids else None
    current_iron = (await request.ctx.profile.get_item_by_guid(iron_id)).get("quantity", 0) if iron_id else 0
    xp_guid = await request.ctx.profile.find_item_by_template_id("Currency:HeroXp_Basic")
    current_xp = (await request.ctx.profile.get_item_by_guid(xp_guid[0])).get("quantity", 0)
    xp_datatable = (await load_datatable("Content/Balance/Datatables/XPUnitLevels"))[0]["Rows"]["UnitXPTNLNormal"]["Keys"]
    strength_ma_ids = await request.ctx.profile.find_item_by_template_id("UpgradePotion:UpgradeStrengthMinor")
    strength_ma_potion_guid = strength_ma_ids[0] if strength_ma_ids else None
    strength_ma_potion_quantity = (await request.ctx.profile.get_item_by_guid(strength_ma_potion_guid)).get("quantity", 0) if strength_ma_potion_guid else 0
    strength_mi_ids = await request.ctx.profile.find_item_by_template_id("UpgradePotion:UpgradeStrengthMajor")
    strength_mi_potion_guid = strength_mi_ids[0] if strength_mi_ids else None
    strength_mi_potion_quantity = (await request.ctx.profile.get_item_by_guid(strength_mi_potion_guid)).get("quantity", 0) if strength_mi_potion_guid else 0
    health_ma_ids = await request.ctx.profile.find_item_by_template_id("UpgradePotion:UpgradeHealthMinor")
    health_ma_potion_guid = health_ma_ids[0] if health_ma_ids else None
    health_ma_potion_quantity = (await request.ctx.profile.get_item_by_guid(health_ma_potion_guid)).get("quantity", 0) if health_ma_potion_guid else 0
    health_mi_ids = await request.ctx.profile.find_item_by_template_id("UpgradePotion:UpgradeHealthMajor")
    health_mi_potion_guid = health_mi_ids[0] if health_mi_ids else None
    health_mi_potion_quantity = (await request.ctx.profile.get_item_by_guid(health_mi_potion_guid)).get("quantity", 0) if health_mi_potion_guid else 0
    mana_ids = await request.ctx.profile.find_item_by_template_id("UpgradePotion:UpgradeMana")
    mana_potion_guid = mana_ids[0] if mana_ids else None
    mana_potion_quantity = (await request.ctx.profile.get_item_by_guid(mana_potion_guid)).get("quantity", 0) if mana_potion_guid else 0
    for upgrade in request.json.get("detail"):
        hero_item = await request.ctx.profile.get_item_by_guid(upgrade["heroItemId"])
        hero_upgrades = hero_item["attributes"]["upgrades"]
        # potions
        for potion_upgrade in upgrade["potionItems"]:
            template_id = potion_upgrade.get("templateId")
            requested_qty = max(0, int(potion_upgrade.get("quantity", 0)))
            if requested_qty <= 0:
                continue
            potion_cost = (await load_datatable(
                (await get_path_from_template_id(template_id)).replace(
                    "res/battle-breakers-data/WorldExplorers/", "").replace(".json", "").replace("\\", "/")))[0][
                "Properties"]["ConsumptionCostGold"]
            match template_id:
                case "UpgradePotion:UpgradeStrengthMinor":
                    if strength_ma_potion_guid is None:
                        raise errors.com.epicgames.modules.gameplayutils.recipe_failed(
                            errorMessage=f"Missing item {template_id} in profile")
                    applicable = min(requested_qty, strength_ma_potion_quantity)
                    applied = 0
                    for _ in range(applicable):
                        if current_gold < potion_cost:
                            break
                        await request.ctx.profile.change_item_quantity(gold_id, current_gold - potion_cost)
                        current_gold -= potion_cost
                        await request.ctx.profile.change_item_quantity(strength_ma_potion_guid, strength_ma_potion_quantity - 1)
                        strength_ma_potion_quantity -= 1
                        applied += 1
                    hero_upgrades[0] += applied
                case "UpgradePotion:UpgradeStrengthMajor":
                    if strength_mi_potion_guid is None:
                        raise errors.com.epicgames.modules.gameplayutils.recipe_failed(
                            errorMessage=f"Missing item {template_id} in profile")
                    applicable = min(requested_qty, strength_mi_potion_quantity)
                    applied = 0
                    for _ in range(applicable):
                        if current_gold < potion_cost:
                            break
                        await request.ctx.profile.change_item_quantity(gold_id, current_gold - potion_cost)
                        current_gold -= potion_cost
                        await request.ctx.profile.change_item_quantity(strength_mi_potion_guid, strength_mi_potion_quantity - 1)
                        strength_mi_potion_quantity -= 1
                        applied += 1
                    hero_upgrades[1] += applied
                case "UpgradePotion:UpgradeHealthMinor":
                    if health_ma_potion_guid is None:
                        raise errors.com.epicgames.modules.gameplayutils.recipe_failed(
                            errorMessage=f"Missing item {template_id} in profile")
                    applicable = min(requested_qty, health_ma_potion_quantity)
                    applied = 0
                    for _ in range(applicable):
                        if current_gold < potion_cost:
                            break
                        await request.ctx.profile.change_item_quantity(gold_id, current_gold - potion_cost)
                        current_gold -= potion_cost
                        await request.ctx.profile.change_item_quantity(health_ma_potion_guid, health_ma_potion_quantity - 1)
                        health_ma_potion_quantity -= 1
                        applied += 1
                    hero_upgrades[2] += applied
                case "UpgradePotion:UpgradeHealthMajor":
                    if health_mi_potion_guid is None:
                        raise errors.com.epicgames.modules.gameplayutils.recipe_failed(
                            errorMessage=f"Missing item {template_id} in profile")
                    applicable = min(requested_qty, health_mi_potion_quantity)
                    applied = 0
                    for _ in range(applicable):
                        if current_gold < potion_cost:
                            break
                        await request.ctx.profile.change_item_quantity(gold_id, current_gold - potion_cost)
                        current_gold -= potion_cost
                        await request.ctx.profile.change_item_quantity(health_mi_potion_guid, health_mi_potion_quantity - 1)
                        health_mi_potion_quantity -= 1
                        applied += 1
                    hero_upgrades[3] += applied
                case "UpgradePotion:UpgradeMana":
                    if mana_potion_guid is None:
                        raise errors.com.epicgames.modules.gameplayutils.recipe_failed(
                            errorMessage=f"Missing item {template_id} in profile")
                    applicable = min(requested_qty, mana_potion_quantity)
                    applied = 0
                    for _ in range(applicable):
                        if current_gold < potion_cost:
                            break
                        await request.ctx.profile.change_item_quantity(gold_id, current_gold - potion_cost)
                        current_gold -= potion_cost
                        await request.ctx.profile.change_item_quantity(mana_potion_guid, mana_potion_quantity - 1)
                        mana_potion_quantity -= 1
                        applied += 1
                    hero_upgrades[4] += applied
                case _:
                    raise errors.com.epicgames.world_explorers.bad_request(
                        errorMessage="Invalid potion item template id")
        # weapons
        for weapon_upgrade in upgrade["weaponUpgrades"]:
            upgrade_type = weapon_upgrade.get("upgradeType")
            num_upgrades = max(0, int(weapon_upgrade.get("numUpgrades", 0)))
            if num_upgrades <= 0:
                continue
            match upgrade_type:
                case "WeaponLevel":
                    idx = 5
                    promotion_table = (await load_datatable("Content/Recipes/PT_WeaponLevel"))[0]["Properties"]["RankRecipes"]
                case "WeaponStars":
                    idx = 6
                    promotion_table = (await load_datatable("Content/Recipes/PT_WeaponTier"))[0]["Properties"]["RankRecipes"]
                case "ArmorLevel":
                    idx = 7
                    promotion_table = (await load_datatable("Content/Recipes/PT_ArmorLevel"))[0]["Properties"]["RankRecipes"]
                case"ArmorStars":
                    idx = 8
                    promotion_table = (await load_datatable("Content/Recipes/PT_ArmorTier"))[0]["Properties"]["RankRecipes"]
                case _:
                    raise errors.com.epicgames.world_explorers.bad_request(errorMessage="Invalid weapon upgrade type")
            current_level = hero_upgrades[idx]
            applied_steps = 0
            for i in range(current_level, current_level + num_upgrades):
                consumed_item = (await load_datatable(
                    promotion_table[i].get("AssetPathName").replace("/Game/", "Content/").split(".")[0]))[0][
                    "Properties"]["ConsumedItems"][0]
                obj_name = consumed_item.get("ItemDefinition", "").get("ObjectName")
                count = int(consumed_item.get("Count", 0))
                match obj_name:
                    case "WExpGenericAccountItemDefinition'Ore_Silver'":
                        if count > 0 and silver_id is None:
                            raise errors.com.epicgames.modules.gameplayutils.recipe_failed(
                                errorMessage="Missing resource Ore:Ore_Silver in profile")
                        if current_silver < count:
                            break
                        await request.ctx.profile.change_item_quantity(silver_id, current_silver - count)
                        current_silver -= count
                    case "WExpGenericAccountItemDefinition'Ore_Magicite'":
                        if count > 0 and magicite_id is None:
                            raise errors.com.epicgames.modules.gameplayutils.recipe_failed(
                                errorMessage="Missing resource Ore:Ore_Magicite in profile")
                        if current_magicite < count:
                            break
                        await request.ctx.profile.change_item_quantity(magicite_id, current_magicite - count)
                        current_magicite -= count
                    case "WExpGenericAccountItemDefinition'Ore_Iron'":
                        if count > 0 and iron_id is None:
                            raise errors.com.epicgames.modules.gameplayutils.recipe_failed(
                                errorMessage="Missing resource Ore:Ore_Iron in profile")
                        if current_iron < count:
                            break
                        await request.ctx.profile.change_item_quantity(iron_id, current_iron - count)
                        current_iron -= count
                    case _:
                        raise errors.com.epicgames.world_explorers.bad_request(errorMessage="Invalid item to consume")
                applied_steps += 1
            hero_upgrades[idx] = current_level + applied_steps
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
