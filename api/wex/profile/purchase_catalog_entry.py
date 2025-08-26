"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles purchasing a catalog entry.
"""
import datetime

import sanic

import utils.utils
from utils import types
from utils.exceptions import errors
from utils.utils import authorized as auth

from utils.sanic_gzip import Compress

compress = Compress()
wex_profile_purchase_catalog_entry = sanic.Blueprint("wex_profile_purchase_catalog_entry")


# https://github.com/dippyshere/battle-breakers-documentation/blob/main/docs/World%20Explorers%20Service/wex/api/game/v2/profile/accountId/PurchaseCatalogEntry.md
@wex_profile_purchase_catalog_entry.route("/<accountId>/PurchaseCatalogEntry", methods=["POST"])
@auth(strict=True)
@compress.compress()
async def purchase_catalog_entry(request: types.BBProfileRequest, accountId: str) -> sanic.response.JSONResponse:
    """
    This endpoint is used to purchase a catalog entry.
    :param request: The request object
    :param accountId: The account id
    :return: The modified profile
    """
    if not request.json.get("offerId"):
        raise errors.com.epicgames.modules.gamesubcatalog.invalid_parameter(errorMessage="Offer ID is required.")
    if not request.json.get("purchaseQuantity"):
        raise errors.com.epicgames.modules.gamesubcatalog.invalid_parameter(errorMessage="Quantity is required.")
    if request.json.get("currency") == "RealMoney":
        raise errors.com.epicgames.modules.gamesubcatalog.invalid_parameter()
    offer_id = request.json.get("offerId")
    await request.app.ctx.storefronts.update_storefronts()
    storefronts = request.app.ctx.storefronts
    offer = await storefronts.get_offer_by_id(offer_id)
    if offer is None:
        raise errors.com.epicgames.modules.gamesubcatalog.catalog_out_of_date(offer_id)
    # Check if the expected price matches the actual price for the currency and currency subtype
    expected_price = request.json.get("expectedTotalPrice")
    currency = request.json.get("currency")
    currency_subtype = request.json.get("currencySubType", "")
    for price in offer.prices:
        if price["currencyType"] == currency and price["currencySubType"] == currency_subtype:
            if price["finalPrice"] * request.json.get("purchaseQuantity") != expected_price:
                raise errors.com.epicgames.modules.gamesubcatalog.invalid_parameter(
                    errorMessage=f"Expected price {expected_price} does not match actual price {price['finalPrice']}.")
            break
    else:
        raise errors.com.epicgames.modules.gamesubcatalog.invalid_parameter(
            errorMessage=f"Currency {currency} with subtype {currency_subtype} not found in offer prices.")
    # Check if the sale is not expired
    if datetime.datetime.fromisoformat(
            offer.prices[0]["saleExpiration"].replace("Z", "+00:00")) < datetime.datetime.now(datetime.UTC):
        raise errors.com.epicgames.modules.gamesubcatalog.catalog_out_of_date(offer_id)
    # Check if the offer can be afforded
    mtx_giveaway_id = await request.ctx.profile.find_item_by_template_id("Currency:MtxGiveaway")
    mtx_giveaway = 0
    if mtx_giveaway_id:
        mtx_giveaway = (await request.ctx.profile.get_item_by_guid(mtx_giveaway_id))["quantity"]
    match currency:
        case "GameItem":
            currency_id = await request.ctx.profile.find_item_by_template_id(currency_subtype)
            if not currency_id:
                raise errors.com.epicgames.modules.gamesubcatalog.cannot_afford_purchase(offer_id)
            currency_item = await request.ctx.profile.get_item_by_guid(currency_id)
            if currency_item["quantity"] < expected_price != 0:
                raise errors.com.epicgames.modules.gamesubcatalog.cannot_afford_purchase(offer_id)
        case "MtxCurrency":
            mtx_purchase_bonus_id = await request.ctx.profile.find_item_by_template_id("Currency:MtxPurchaseBonus")
            mtx_purchased_id = await request.ctx.profile.find_item_by_template_id("Currency:MtxPurchased")
            mtx_purchase_bonus = 0
            mtx_purchased = 0
            if mtx_purchase_bonus_id:
                mtx_purchase_bonus = (await request.ctx.profile.get_item_by_guid(mtx_purchase_bonus_id))["quantity"]
            if mtx_purchased_id:
                mtx_purchased = (await request.ctx.profile.get_item_by_guid(mtx_purchased_id))["quantity"]
            total_mtx = mtx_giveaway + mtx_purchase_bonus + mtx_purchased
            if total_mtx < expected_price:
                raise errors.com.epicgames.modules.gamesubcatalog.cannot_afford_purchase(offer_id)
        case "Other":
            if currency_subtype == "LaborPoints":
                labor_force = await request.ctx.profile.get_stat("labor_force")
                stars = await request.ctx.profile.get_stat("num_levels_completed")
                labor_used = labor_force.get("laborUsed", 0)
                if labor_force["lastInterval"] != await utils.utils.format_time(
                        await utils.utils.get_current_12_hour_interval()):
                    labor_used = 0
                labor_points = stars - labor_used
                if labor_points < expected_price:
                    raise errors.com.epicgames.modules.gamesubcatalog.cannot_afford_purchase(offer_id)
            else:
                raise errors.com.epicgames.modules.gamesubcatalog.invalid_parameter(
                    errorMessage=f"Currency subtype {currency_subtype} is not valid.")
        case _:
            raise errors.com.epicgames.modules.gamesubcatalog.invalid_parameter(
                errorMessage=f"Currency {currency} with subtype {currency_subtype} is not valid.")
    daily_limit = await request.ctx.profile.get_stat("daily_purchases")
    # if the last interval is not today, reset the daily purchases
    if daily_limit.get("lastInterval") != await utils.utils.format_time(
            await utils.utils.get_current_24_hour_interval()):
        daily_limit["lastInterval"] = await utils.utils.format_time(await utils.utils.get_current_24_hour_interval())
        daily_limit["purchaseList"] = {}
    # Check if the offer has a daily limit and if it has been exceeded
    if offer.daily_limit != -1:
        if offer_id in daily_limit["purchaseList"]:
            if daily_limit["purchaseList"][offer_id] >= offer.daily_limit:
                raise errors.com.epicgames.modules.gamesubcatalog.purchase_not_allowed(offer.dev_name,
                                                                                       offer.item_grants[0].get(
                                                                                           "templateId", offer_id),
                                                                                       request.json.get(
                                                                                           "purchaseQuantity"),
                                                                                       offer.daily_limit)
        else:
            daily_limit["purchaseList"][offer_id] = 0
        daily_limit["purchaseList"][offer_id] += request.json.get("purchaseQuantity")
    await request.ctx.profile.modify_stat("daily_purchases", daily_limit)
    # Check if the offer has a weekly limit and if it has been exceeded
    weekly_limit = await request.ctx.profile.get_stat("weekly_purchases")
    # if the last interval is not this week, reset the weekly purchases
    if weekly_limit.get("lastInterval") != await utils.utils.format_time(
            await utils.utils.get_current_weekly_interval()):
        weekly_limit["lastInterval"] = await utils.utils.format_time(await utils.utils.get_current_weekly_interval())
        weekly_limit["purchaseList"] = {}
    # Check if the offer has a weekly limit and if it has been exceeded
    if offer.weekly_limit != -1:
        if offer_id in weekly_limit["purchaseList"]:
            if weekly_limit["purchaseList"][offer_id] >= offer.weekly_limit:
                raise errors.com.epicgames.modules.gamesubcatalog.purchase_not_allowed(offer.dev_name,
                                                                                       offer.item_grants[0].get(
                                                                                           "templateId", offer_id),
                                                                                       request.json.get(
                                                                                           "purchaseQuantity"),
                                                                                       offer.weekly_limit)
        else:
            weekly_limit["purchaseList"][offer_id] = 0
        weekly_limit["purchaseList"][offer_id] += request.json.get("purchaseQuantity")
    await request.ctx.profile.modify_stat("weekly_purchases", weekly_limit)
    # Check if the offer has a monthly limit and if it has been exceeded
    monthly_limit = await request.ctx.profile.get_stat("monthly_purchases")
    # if the last interval is not this month, reset the monthly purchases
    if monthly_limit.get("lastInterval") != await utils.utils.format_time(
            await utils.utils.get_current_monthly_interval()):
        monthly_limit["lastInterval"] = await utils.utils.format_time(await utils.utils.get_current_monthly_interval())
        monthly_limit["purchaseList"] = {}
    # Check if the offer has a monthly limit and if it has been exceeded
    if offer.monthly_limit != -1:
        if offer_id in monthly_limit["purchaseList"]:
            if monthly_limit["purchaseList"][offer_id] >= offer.monthly_limit:
                raise errors.com.epicgames.modules.gamesubcatalog.purchase_not_allowed(offer.dev_name,
                                                                                       offer.item_grants[0].get(
                                                                                           "templateId", offer_id),
                                                                                       request.json.get(
                                                                                           "purchaseQuantity"),
                                                                                       offer.monthly_limit)
        else:
            monthly_limit["purchaseList"][offer_id] = 0
        monthly_limit["purchaseList"][offer_id] += request.json.get("purchaseQuantity")
    await request.ctx.profile.modify_stat("monthly_purchases", monthly_limit)
    # Check the requirements require/deny fulfillments
    purchase_list = await request.ctx.profile.get_stat("in_app_purchases")
    if offer.requirements:
        for requirement in offer.requirements:
            if requirement["requirementType"] == "DenyOnFulfillment":
                if purchase_list["fulfillmentCounts"].get(requirement["requiredId"], 0) >= requirement["minQuantity"]:
                    raise errors.com.epicgames.modules.gamesubcatalog.purchase_not_allowed(
                        errorMessage=f"You have already purchased {requirement['requiredId']} {purchase_list['fulfillmentCounts'][requirement['requiredId']]} times, which exceeds the maximum quantity of {requirement['minQuantity']}.")
            elif requirement["requirementType"] == "RequireFulfillment":
                if requirement["requiredId"] not in purchase_list.get("fulfillmentCounts", {}):
                    raise errors.com.epicgames.modules.gamesubcatalog.purchase_not_allowed(
                        errorMessage=f"You do not have the required fulfillment {requirement['requiredId']}.")
                elif purchase_list["fulfillmentCounts"][requirement["requiredId"]] < requirement["minQuantity"]:
                    raise errors.com.epicgames.modules.gamesubcatalog.purchase_not_allowed(
                        errorMessage=f"You do not have enough of the required fulfillment {requirement['requiredId']}.")
    # Check the MTX level minimum and maximum in the meta_info
    if offer.meta_info:
        mtx_level = await request.ctx.profile.get_stat("mtx_level")
        if "MtxLevelMin" in [meta["key"] for meta in offer.meta_info]:
            mtx_level_min = int(
                next(meta["value"] for meta in offer.meta_info if meta["key"] == "MtxLevelMin"))
            if mtx_level < mtx_level_min:
                raise errors.com.epicgames.modules.gamesubcatalog.purchase_not_allowed(
                    errorMessage="You do not meet the minimum MTX level requirement.")
        if "MtxLevelMax" in [meta["key"] for meta in offer.meta_info]:
            mtx_level_max = int(
                next(meta["value"] for meta in offer.meta_info if meta["key"] == "MtxLevelMax"))
            if mtx_level > mtx_level_max:
                raise errors.com.epicgames.modules.gamesubcatalog.purchase_not_allowed(
                    errorMessage="You have exceeded the maximum MTX level requirement.")
    # Check the account level minimum and maximum in the meta_info
    if offer.meta_info:
        account_level = await request.ctx.profile.get_stat("level")
        if "AccountLevelMin" in [meta["key"] for meta in offer.meta_info]:
            account_level_min = int(
                next(meta["value"] for meta in offer.meta_info if meta["key"] == "AccountLevelMin"))
            if account_level < account_level_min:
                raise errors.com.epicgames.modules.gamesubcatalog.purchase_not_allowed(
                    errorMessage="You do not meet the minimum account level requirement.")
        if "AccountLevelMax" in [meta["key"] for meta in offer.meta_info]:
            account_level_max = int(
                next(meta["value"] for meta in offer.meta_info if meta["key"] == "AccountLevelMax"))
            if account_level > account_level_max:
                raise errors.com.epicgames.modules.gamesubcatalog.purchase_not_allowed(
                    errorMessage="You have exceeded the maximum account level requirement.")
    # Check the store level minimum and maximum in the meta_info
    if offer.meta_info:
        store_level = await request.ctx.profile.get_stat("store_level")
        if "StoreLevelMin" in [meta["key"] for meta in offer.meta_info]:
            store_level_min = int(
                next(meta["value"] for meta in offer.meta_info if meta["key"] == "StoreLevelMin"))
            if store_level < store_level_min:
                raise errors.com.epicgames.modules.gamesubcatalog.purchase_not_allowed(
                    errorMessage="You do not meet the minimum store level requirement.")
        if "StoreLevelMax" in [meta["key"] for meta in offer.meta_info]:
            store_level_max = int(
                next(meta["value"] for meta in offer.meta_info if meta["key"] == "StoreLevelMax"))
            if store_level > store_level_max:
                raise errors.com.epicgames.modules.gamesubcatalog.purchase_not_allowed(
                    errorMessage="You have exceeded the maximum store level requirement.")
    # Check the vip level minimum and maximum in the meta_info
    if offer.meta_info:
        vip_level = await request.ctx.profile.get_stat("vip_level")
        if "VipLevelMin" in [meta["key"] for meta in offer.meta_info]:
            vip_level_min = int(
                next(meta["value"] for meta in offer.meta_info if meta["key"] == "VipLevelMin"))
            if vip_level < vip_level_min:
                raise errors.com.epicgames.modules.gamesubcatalog.purchase_not_allowed(
                    errorMessage="You do not meet the minimum VIP level requirement.")
        if "VipLevelMax" in [meta["key"] for meta in offer.meta_info]:
            vip_level_max = int(
                next(meta["value"] for meta in offer.meta_info if meta["key"] == "VipLevelMax"))
            if vip_level > vip_level_max:
                raise errors.com.epicgames.modules.gamesubcatalog.purchase_not_allowed(
                    errorMessage="You have exceeded the maximum VIP level requirement.")
    # TODO: Perform the service from meta_info
    if offer.meta_info:
        for meta in offer.meta_info:
            if meta["key"] == "ServiceName":
                service_name = meta["value"].split(":")[0]
                match service_name:
                    case "ResetLaborPool":
                        await request.ctx.profile.modify_stat("labor_refill_cd", await utils.utils.format_time(
                            datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=2)))
                        await request.ctx.profile.modify_stat("labor_force", {
                            "lastInterval": await utils.utils.format_time(
                                await utils.utils.get_current_12_hour_interval()),
                            "laborUsed": 0})
                    case "PerkReset":
                        perks = await request.ctx.profile.get_stat("rewards_claimed")
                        await request.ctx.profile.modify_stat("account_perks", {})
                        await request.ctx.profile.modify_stat("rewards_claimed", {})
                        for perk in perks:
                            await request.ctx.profile.grant_item(perk, perks[perk])
                    case "MarketRefresh":
                        if meta["value"].split(":")[1] == "0":
                            await request.ctx.profile.modify_stat("market_page", {
                                "unlock_time": await utils.utils.format_time(datetime.datetime.now(datetime.UTC)),
                                "page": 1
                            })
                        else:
                            await request.ctx.profile.modify_stat("market_page", {
                                "unlock_time": await utils.utils.format_time(
                                    datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=1)),
                                "page": 2
                            })
                    case "EnergyRefill":
                        pass
                    case "GameContinue":
                        pass
                    case "SecretShopRefresh":
                        #0-3
                        pass
                    case "FriendsListIncrease":
                        pass
                    case "InventoryUpgrade":
                        pass
                    case _:
                        raise errors.com.epicgames.modules.gamesubcatalog.invalid_parameter(
                            errorMessage=f"Service {service_name} is not valid.")
    items = []
    if offer.item_grants[0]:
        for item_grant in offer.item_grants:
            if item_grant["templateId"].startswith("StandIn:"):
                items.append({
                    "itemType": item_grant["templateId"],
                    "attributes": item_grant.get("attributes", {}),
                    "quantity": item_grant.get("quantity", 1) * request.json.get("purchaseQuantity")
                })
                continue
            elif item_grant["templateId"].startswith("Character:"):
                for _ in range(item_grant["quantity"] * request.json.get("purchaseQuantity")):
                    hero_id = await request.ctx.profile.grant_hero(item_grant["templateId"])
                    items.append({
                        "itemType": item_grant["templateId"],
                        "itemGuid": hero_id,
                        "itemProfile": request.ctx.profile_id,
                        "quantity": 1
                    })
            else:
                if item_grant["templateId"] == "Currency:MtxGiveaway":
                    mtx_giveaway += item_grant.get("quantity", 1)
                item_id = await request.ctx.profile.grant_item(item_grant["templateId"], item_grant.get("quantity", 1))
                items.append({
                    "itemType": item_grant["templateId"],
                    "itemGuid": item_id,
                    "itemProfile": request.ctx.profile_id,
                    "quantity": item_grant.get("quantity", 1) * request.json.get("purchaseQuantity")
                })
    store_level = await request.ctx.profile.get_stat("store_level")
    await request.ctx.profile.modify_stat("store_level", store_level + expected_price)
    # Subtract the currency
    match currency:
        case "GameItem":
            currency_id = await request.ctx.profile.find_item_by_template_id(currency_subtype)
            if not currency_id:
                raise errors.com.epicgames.modules.gamesubcatalog.cannot_afford_purchase(offer_id)
            currency_item = await request.ctx.profile.get_item_by_guid(currency_id)
            if currency_item["quantity"] < expected_price != 0:
                raise errors.com.epicgames.modules.gamesubcatalog.cannot_afford_purchase(offer_id)
            if currency_item["quantity"] - expected_price == 0:
                await request.ctx.profile.remove_item(currency_id)
            else:
                await request.ctx.profile.change_item_quantity(currency_id, currency_item["quantity"] - expected_price)
        case "MtxCurrency":
            mtx_purchase_bonus_id = await request.ctx.profile.find_item_by_template_id("Currency:MtxPurchaseBonus")
            mtx_purchased_id = await request.ctx.profile.find_item_by_template_id("Currency:MtxPurchased")
            mtx_purchase_bonus = 0
            mtx_purchased = 0
            if mtx_purchase_bonus_id:
                mtx_purchase_bonus = (await request.ctx.profile.get_item_by_guid(mtx_purchase_bonus_id))["quantity"]
            if mtx_purchased_id:
                mtx_purchased = (await request.ctx.profile.get_item_by_guid(mtx_purchased_id))["quantity"]
            total_mtx = mtx_giveaway + mtx_purchase_bonus + mtx_purchased
            if total_mtx < expected_price:
                raise errors.com.epicgames.modules.gamesubcatalog.cannot_afford_purchase(offer_id)
            mtx_to_deduct = expected_price
            if mtx_giveaway >= mtx_to_deduct:
                if mtx_giveaway - mtx_to_deduct == 0:
                    await request.ctx.profile.remove_item(mtx_giveaway_id)
                else:
                    await request.ctx.profile.change_item_quantity(mtx_giveaway_id, mtx_giveaway - mtx_to_deduct)
                mtx_to_deduct = 0
            else:
                mtx_to_deduct -= mtx_giveaway
                if mtx_giveaway_id:
                    await request.ctx.profile.remove_item(mtx_giveaway_id)
            if 0 < mtx_to_deduct <= mtx_purchase_bonus:
                if mtx_purchase_bonus - mtx_to_deduct == 0:
                    await request.ctx.profile.remove_item(mtx_purchase_bonus_id)
                else:
                    await request.ctx.profile.change_item_quantity(mtx_purchase_bonus_id,
                                                                   mtx_purchase_bonus - mtx_to_deduct)
                mtx_to_deduct = 0
            elif mtx_to_deduct > 0:
                mtx_to_deduct -= mtx_purchase_bonus
                if mtx_purchase_bonus_id:
                    await request.ctx.profile.remove_item(mtx_purchase_bonus_id)
            if 0 < mtx_to_deduct <= mtx_purchased:
                if mtx_purchased - mtx_to_deduct == 0:
                    await request.ctx.profile.remove_item(mtx_purchased_id)
                else:
                    await request.ctx.profile.change_item_quantity(mtx_purchased_id, mtx_purchased - mtx_to_deduct)
                mtx_to_deduct = 0
        case "Other":
            if currency_subtype == "LaborPoints":
                labor_force = await request.ctx.profile.get_stat("labor_force")
                stars = await request.ctx.profile.get_stat("num_levels_completed")
                labor_used = labor_force.get("laborUsed", 0)
                if labor_force["lastInterval"] != await utils.utils.format_time(
                        await utils.utils.get_current_12_hour_interval()):
                    labor_used = 0
                labor_points = stars - labor_used
                if labor_points < expected_price:
                    raise errors.com.epicgames.modules.gamesubcatalog.cannot_afford_purchase(offer_id)
                labor_used += expected_price
                await request.ctx.profile.modify_stat("labor_force", {
                    "lastInterval": await utils.utils.format_time(await utils.utils.get_current_12_hour_interval()),
                    "laborUsed": labor_used})
    # Update fulfillments
    if daily_limit != -1 and weekly_limit != -1 and monthly_limit != -1:
        if offer_id not in purchase_list.get("fulfillmentCounts", {}):
            purchase_list["fulfillmentCounts"][offer_id] = 0
        purchase_list["fulfillmentCounts"][offer_id] += request.json.get("purchaseQuantity")
    await request.ctx.profile.modify_stat("in_app_purchases", purchase_list)
    await request.ctx.profile.add_notifications({
        "type": "CatalogPurchase",
        "primary": True,
        "lootResult": {
            "items": items
        }
    }, request.ctx.profile_id)
    return sanic.response.json(
        await request.ctx.profile.construct_response(request.ctx.profile_id, request.ctx.rvn,
                                                     request.ctx.profile_revisions)
    )
