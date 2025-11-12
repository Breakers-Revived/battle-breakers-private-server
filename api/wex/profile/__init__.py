"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles the mcp profile subsystem
"""
import sanic
import sanic.log

from utils import types
from utils.profile_system import PlayerProfile
from utils.enums import ProfileType
from .abandon_level import wex_profile_abandon_level
from .add_epic_friend import wex_profile_add_epic_friend
from .add_friend import wex_profile_add_friend
from .add_to_monster_pit import wex_profile_add_to_monster_pit
from .blitz_level import wex_profile_blitz_level
from .bulk_improve_heroes import wex_profile_bulk_improve_heroes
from .buy_back_from_monster_pit import wex_profile_buy_back_from_monster_pit
from .cash_out_workshop import wex_profile_cash_out_workshop
from .claim_account_reward import wex_profile_claim_account_reward
from .claim_come_back_reward import wex_profile_claim_comeback
from .claim_event_rewards import wex_profile_claim_event_rewards
from .claim_gift_points import wex_profile_claim_gift_points
from .claim_login_reward import wex_profile_claim_login
from .claim_notification_optin_reward import wex_profile_claim_notification_opt_in_reward
from .claim_personal_event import wex_profile_claim_personal_event
from .claim_quest_reward import wex_profile_claim_quest_reward
from .claim_territory import wex_profile_claim_territory
from .client_added_external_account import wex_profile_client_ext_acc
from .client_tracked_retention_analytics import wex_profile_client_tracked_retention_analytics
from .collect_hammer_quest_energy import wex_profile_collect_hammer_quest_energy
from .collect_hammer_quest_realtime import wex_profile_collect_hammer_quest_realtime
from .craft_recipe import wex_profile_craft_recipe
from .delete_friend import wex_profile_delete_friend
from .evolve_hero import wex_profile_evolve_hero
from .finalize_level import wex_profile_finalize_level
from .foil_hero import wex_profile_foil_hero
from .generate_daily_quests import wex_profile_generate_daily_quests
from .generate_match_with_friend import wex_profile_generate_match_with_friend
from .generate_matches import wex_profile_generate_matches
from .initialize_level import wex_profile_initialize_level
from .join_matchmaking import wex_profile_join_matchmaking
from .level_up_hero import wex_profile_level_up_hero
from .mark_hero_seen import wex_profile_mark_hero_seen
from .mark_item_seen import wex_profile_mark_item_seen
from .modify_hero_armor import wex_profile_modify_hero_armor
from .modify_hero_gear import wex_profile_modify_hero_gear
from .modify_hero_weapon import wex_profile_modify_hero_weapon
from .open_gift_box import wex_profile_open_gift_box
from .open_hero_chest import wex_profile_open_hero_chest
from .pick_hero_chest import wex_profile_pick_hero_chest
from .promote_hero import wex_profile_promote_hero
from .purchase_catalog_entry import wex_profile_purchase_catalog_entry
from .query_profile import wex_profile_query
from .reconcile import wex_profile_reconcile
from .redeem_token import wex_profile_redeem_token
from .refresh_run_count import wex_profile_refresh_run_count
from .remove_friend import wex_profile_remove_friend
from .remove_from_monster_pit import wex_profile_remove_from_monster_pit
from .remove_hero_from_all_parties import wex_profile_remove_hero_from_all_parties
from .request_preregistration_reward import wex_profile_request_prereg
from .roll_hammer_chests import wex_profile_roll_hammer_chests
from .select_hammer_chest import wex_profile_select_hammer_chest
from .select_start_options import wex_profile_select_start_options
from .sell_gear import wex_profile_sell_gear
from .sell_hero import wex_profile_sell_hero
from .sell_multiple_gear import wex_profile_sell_multiple_gear
from .sell_treasure import wex_profile_sell_treasure
from .send_gift_points import wex_profile_send_gift
from .set_affiliate import wex_profile_set_sac
from .set_default_party import wex_profile_set_default_party
from .set_rep_hero import wex_profile_set_rep_hero
from .suggest_friends import wex_profile_suggest_friends
from .suggestion_response import wex_profile_suggestion_response
from .tap_hammer_chest import wex_profile_tap_hammer_chest
from .unlock_armor_gear import wex_profile_unlock_armor_gear
from .unlock_hero_gear import wex_profile_unlock_hero_gear
from .unlock_region import wex_profile_unlock_region
from .unlock_weapon_gear import wex_profile_unlock_weapon_gear
from .update_account_headless_status import wex_update_headless
from .update_friends import wex_profile_update_friends
from .update_monster_pit_power import wex_profile_update_monster_pit_power
from .update_party import wex_profile_update_party
from .upgrade_building import wex_profile_upgrade_building
from .upgrade_hero import wex_profile_upgrade_hero
from .upgrade_hero_skills import wex_profile_upgrade_hero_skills
from .verify_real_money_purchase import wex_verify_realmoney

wex_profile = sanic.Blueprint.group(wex_profile_abandon_level, wex_profile_add_epic_friend,
                                    wex_profile_add_to_monster_pit, wex_profile_blitz_level,
                                    wex_profile_bulk_improve_heroes, wex_profile_buy_back_from_monster_pit,
                                    wex_profile_cash_out_workshop, wex_profile_claim_account_reward,
                                    wex_profile_claim_event_rewards, wex_profile_claim_login,
                                    wex_profile_claim_notification_opt_in_reward, wex_profile_claim_quest_reward,
                                    wex_profile_claim_territory, wex_profile_client_tracked_retention_analytics,
                                    wex_profile_evolve_hero, wex_profile_finalize_level, wex_profile_foil_hero,
                                    wex_profile_generate_daily_quests, wex_profile_generate_match_with_friend,
                                    wex_profile_initialize_level, wex_profile_join_matchmaking,
                                    wex_profile_level_up_hero, wex_profile_mark_item_seen,
                                    wex_profile_modify_hero_armor, wex_profile_modify_hero_gear,
                                    wex_profile_modify_hero_weapon, wex_profile_open_gift_box,
                                    wex_profile_open_hero_chest, wex_profile_pick_hero_chest, wex_profile_promote_hero,
                                    wex_profile_purchase_catalog_entry, wex_profile_query, wex_profile_reconcile,
                                    wex_profile_remove_from_monster_pit, wex_profile_roll_hammer_chests,
                                    wex_profile_select_hammer_chest, wex_profile_select_start_options,
                                    wex_profile_sell_hero, wex_profile_send_gift, wex_profile_set_default_party,
                                    wex_profile_set_rep_hero, wex_profile_suggestion_response,
                                    wex_profile_tap_hammer_chest, wex_profile_unlock_armor_gear,
                                    wex_profile_unlock_hero_gear, wex_profile_unlock_region,
                                    wex_profile_unlock_weapon_gear, wex_profile_update_friends,
                                    wex_profile_update_monster_pit_power, wex_profile_update_party,
                                    wex_profile_upgrade_building, wex_profile_upgrade_hero,
                                    wex_profile_upgrade_hero_skills, wex_verify_realmoney, wex_update_headless,
                                    wex_profile_suggest_friends, wex_profile_mark_hero_seen,
                                    wex_profile_claim_gift_points, wex_profile_sell_gear,
                                    wex_profile_sell_multiple_gear, wex_profile_sell_treasure,
                                    wex_profile_delete_friend, wex_profile_redeem_token, wex_profile_add_friend,
                                    wex_profile_claim_comeback, wex_profile_claim_personal_event,
                                    wex_profile_client_ext_acc, wex_profile_collect_hammer_quest_energy,
                                    wex_profile_collect_hammer_quest_realtime, wex_profile_craft_recipe,
                                    wex_profile_generate_matches, wex_profile_refresh_run_count,
                                    wex_profile_remove_friend, wex_profile_remove_hero_from_all_parties,
                                    wex_profile_request_prereg, wex_profile_set_sac, url_prefix="/api/game/v2/profile")


@wex_profile.on_request
async def add_mcp_profile(request: types.BBProfileRequest) -> None:
    """
    Adds the profile data to the request context for use in the handlers
    :param request: The request object
    :return: None
    """
    account_id = request.match_info.get('accountId')
    if account_id is not None:
        if account_id not in request.app.ctx.profiles:
            request.app.ctx.profiles[account_id] = await PlayerProfile.init_profile(account_id)
        request.ctx.profile = request.app.ctx.profiles[account_id]
    else:
        request.ctx.profile = None
    if request.args.get("rvn") is None:
        request.ctx.rvn = -1
    else:
        try:
            request.ctx.rvn = int(request.args.get("rvn"))
        except:
            request.ctx.rvn = -1
    if request.args.get("profileId") is None:
        request.ctx.profile_id = ProfileType.from_string("profile0")
    else:
        request.ctx.profile_id = ProfileType.from_string(request.args.get("profileId"))
    request.ctx.profile_revisions = request.headers.get("X-EpicGames-ProfileRevisions")
    sanic.log.logger.debug(f"MCP operation {request.path.split('/')[-1].split('?')[0]} called for {account_id} "
                           f"with profileId {request.ctx.profile_id.name} and rvn {request.ctx.rvn}")
    sanic.log.logger.debug(f"Request body: {request.json}")


@wex_profile.on_response
async def add_profile_revision_header(request: types.BBProfileRequest, response: sanic.response.HTTPResponse) -> None:
    """
    Adds the profile revision header to the response
    :param request: The request object
    :param response: The response object
    :return: None
    """
    if request.ctx.profile is not None:
        response.headers["X-EpicGames-ProfileRevision"] = (
            await request.ctx.profile.get_profile(request.ctx.profile_id))["rvn"]
