"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Contains validation classes for requests
"""
import uuid
from typing import Annotated

from pydantic import AfterValidator
from typing_extensions import Optional

import pydantic

from utils.exceptions import errors


def UUIDString(v: str) -> str:
    """
    Validates the UUID string

    :param v: The UUID string
    :return: The UUID string
    :raises ValueError: If the UUID string is invalid
    """
    if not isinstance(v, str):
        raise ValueError('UUIDString must be a string')
    try:
        uuid.UUID(v)
    except ValueError:
        raise ValueError('Invalid UUID string')
    return v

def UUIDStringOptional(v: str) -> str:
    """
    Validates a UUID string if present

    :param v: The UUID string
    :return: The UUID string
    :raises ValueError: If the UUID string is invalid
    """
    if not isinstance(v, str):
        raise ValueError('UUIDString must be a string')
    if v == '':
        return v
    try:
        uuid.UUID(v)
    except ValueError:
        raise ValueError('Invalid UUID string')
    return v

def CharacterTemplateId(v: str) -> str:
    """
    Validates the Character Template ID

    :param v: The Character Template ID
    :return: The Character Template ID
    :raises ValueError: If the Character Template ID is invalid
    """
    if not isinstance(v, str):
        raise ValueError('CharacterTemplateId must be a string')
    try:
        if not v.startswith('Character:'):
            raise ValueError('Invalid Character Template ID')
        # TODO: Validate the Character in the template ID
    except ValueError:
        raise ValueError('Invalid Character Template ID')
    return v

def AccountId(v: str) -> str:
    """
    Validates the Account ID string

    :param v: The Account ID string
    :return: The Account ID string
    :raises ValueError: If the Account ID is invalid
    """
    if not isinstance(v, str):
        raise errors.com.epicgames.modules.profile.invalid_account_id_param(v)
    try:
        uuid.UUID(v)
    except ValueError:
        raise errors.com.epicgames.modules.profile.invalid_account_id_param(v)
    return v

def ProfileProfile0(v: str) -> str:
    """
    Validates the Profile ID string

    :param v: The Profile ID string
    :return: The Profile ID string
    :raises ValueError: If the Profile ID is invalid
    """
    if not isinstance(v, str):
        raise errors.com.epicgames.modules.profile.invalid_profile_id_param(v)
    if v not in ["profile0", "levels", "monsterpit", "friends", "multiplayer"]:
        raise errors.com.epicgames.modules.profile.profile_not_found(v)
    if v != "profile0":
        raise errors.com.epicgames.modules.profile.invalid_profile_command("", f"player:profile_{v}", v)
    return v

def ProfileProfile0MonsterPit(v: str) -> str:
    """
    Validates the Profile ID string

    :param v: The Profile ID string
    :return: The Profile ID string
    :raises ValueError: If the Profile ID is invalid
    """
    if not isinstance(v, str):
        raise errors.com.epicgames.modules.profile.invalid_profile_id_param(v)
    if v not in ["profile0", "levels", "monsterpit", "friends", "multiplayer"]:
        raise errors.com.epicgames.modules.profile.profile_not_found(v)
    if v not in ["profile0", "monsterpit"]:
        raise errors.com.epicgames.modules.profile.invalid_profile_command("", f"player:profile_{v}", v)
    return v

def ProfileLevels(v: str) -> str:
    """
    Validates the Profile ID string

    :param v: The Profile ID string
    :return: The Profile ID string
    :raises ValueError: If the Profile ID is invalid
    """
    if not isinstance(v, str):
        raise errors.com.epicgames.modules.profile.invalid_profile_id_param(v)
    if v not in ["profile0", "levels", "monsterpit", "friends", "multiplayer"]:
        raise errors.com.epicgames.modules.profile.profile_not_found(v)
    if v != "levels":
        raise errors.com.epicgames.modules.profile.invalid_profile_command("", f"player:profile_{v}", v)
    return v

def ProfileFriends(v: str) -> str:
    """
    Validates the Profile ID string

    :param v: The Profile ID string
    :return: The Profile ID string
    :raises ValueError: If the Profile ID is invalid
    """
    if not isinstance(v, str):
        raise errors.com.epicgames.modules.profile.invalid_profile_id_param(v)
    if v not in ["profile0", "levels", "monsterpit", "friends", "multiplayer"]:
        raise errors.com.epicgames.modules.profile.profile_not_found(v)
    if v != "friends":
        raise errors.com.epicgames.modules.profile.invalid_profile_command("", f"player:profile_{v}", v)
    return v

def ProfileMonsterpit(v: str) -> str:
    """
    Validates the Profile ID string

    :param v: The Profile ID string
    :return: The Profile ID string
    :raises ValueError: If the Profile ID is invalid
    """
    if not isinstance(v, str):
        raise errors.com.epicgames.modules.profile.invalid_profile_id_param(v)
    if v not in ["profile0", "levels", "monsterpit", "friends", "multiplayer"]:
        raise errors.com.epicgames.modules.profile.profile_not_found(v)
    if v != "monsterpit":
        raise errors.com.epicgames.modules.profile.invalid_profile_command("", f"player:profile_{v}", v)
    return v

def ProfileMultiplayer(v: str) -> str:
    """
    Validates the Profile ID string

    :param v: The Profile ID string
    :return: The Profile ID string
    :raises ValueError: If the Profile ID is invalid
    """
    if not isinstance(v, str):
        raise errors.com.epicgames.modules.profile.invalid_profile_id_param(v)
    if v not in ["profile0", "levels", "monsterpit", "friends", "multiplayer"]:
        raise errors.com.epicgames.modules.profile.profile_not_found(v)
    if v != "multiplayer":
        raise errors.com.epicgames.modules.profile.invalid_profile_command("", f"player:profile_{v}", v)
    return v

def ProfileAny(v: str) -> str:
    """
    Validates the Profile ID string

    :param v: The Profile ID string
    :return: The Profile ID string
    :raises ValueError: If the Profile ID is invalid
    """
    if not isinstance(v, str):
        raise errors.com.epicgames.modules.profile.invalid_profile_id_param(v)
    if v not in ["profile0", "levels", "monsterpit", "friends", "multiplayer"]:
        raise errors.com.epicgames.modules.profile.profile_not_found(v)
    return v

class MCPValidation:
    """
    Validation parent class for MCP requests body
    """

    class AbandonLevel(pydantic.BaseModel):
        """
        Validation class for the abandon level request

        Attributes:
            levelItemId: The level id
            depthCompleted: The depth completed
            levelElement: The level element
            postBattleResults: The post battle results
            dailyQuestZoneType: The daily quest zone type
        """
        levelItemId: Annotated[str, AfterValidator(UUIDString)]
        # These don't get sent when abandoning a level from another device in an old version
        depthCompleted: Optional[int] = None
        # These don't get sent by old clients
        levelElement: Optional[str] = None
        postBattleResults: Optional[dict[str, dict[str, int] | list[Annotated[str, AfterValidator(UUIDString)]] | list[Annotated[str, AfterValidator(CharacterTemplateId)]]]] = None
        dailyQuestZoneType: Optional[int] = None

    class AddEpicFriend(pydantic.BaseModel):
        """
        Validation class for the add epic friend request

        Attributes:
            friendAccountId: The epic account id
        """
        friendAccountId: Annotated[str, AfterValidator(AccountId)]

    class AddFriend(pydantic.BaseModel):
        """
        Validation class for the add friend request (wex + epic)

        Attributes:
            friendAccountId: The epic account id
        """
        friendAccountId: Annotated[str, AfterValidator(AccountId)]

    class AddToMonsterPit(pydantic.BaseModel):
        """
        Validation class for the add to monster pit request

        Attributes:
            characterItemId: The character UUID
        """
        characterItemId: Annotated[str, AfterValidator(UUIDString)]

    class BlitzLevel(pydantic.BaseModel):
        """
        Validation class for the blitz level request

        Attributes:
            manifestVersion: The manifest version
            levelId: The level id
            partyMembers: The party members
            friendInstanceId: The friend instance id
        """
        manifestVersion: Optional[str]
        levelId: str
        partyMembers: list[dict[str, str | Annotated[str, AfterValidator(UUIDStringOptional)]]]
        friendInstanceId: Optional[Annotated[str, AfterValidator(UUIDStringOptional)]]

    class BulkImproveHeroes(pydantic.BaseModel):
        """
        Validation class for the bulk improve heroes request

        Attributes:
            detail: The character ids
        """
        detail: list[dict[str, Annotated[str, AfterValidator(UUIDString)] | list | list[dict[str, int]] | int]]

    class BuyBackFromMonsterPit(pydantic.BaseModel):
        """
        Validation class for the buyback from monster pit request

        Attributes:
            characterTemplateId: The character template id
        """
        characterTemplateId: Annotated[str, AfterValidator(CharacterTemplateId)]

    class CashOutWorkshop(pydantic.BaseModel):
        """
        Validation class for the cash out workshop request

        Attributes:
        """

    class ClaimAccountReward(pydantic.BaseModel):
        """
        Validation class for the claim account reward request

        Attributes:
            perks: The list of perks
        """
        perks: Optional[list[dict[str, Annotated[str, AfterValidator(UUIDString)] | int]]] = None
        rewardItemId: Optional[Annotated[str, AfterValidator(UUIDString)]] = None
        choiceIdx: Optional[int] = 0

    class ClaimComeBackReward(pydantic.BaseModel):
        """
        Validation class for the claim comeback reward request

        Attributes:
        """

    class ClaimEventRewards(pydantic.BaseModel):
        """
        Validation class for the claim battlepass reward request

        Attributes:
        """

    class ClaimGiftPoints(pydantic.BaseModel):
        """
        Validation class for the claim gift point request

        Attributes:
        """
        pass

    class ClaimLoginReward(pydantic.BaseModel):
        """
        Validation class for the claim daily reward request

        Attributes:
        """

    class ClaimNotificationOptInReward(pydantic.BaseModel):
        """
        Validation class for the claim notification opt in request

        Attributes:
        """

    class ClaimPersonalEvent(pydantic.BaseModel):
        """
        Validation class for the claim personal event request

        Attributes:
        """

    class ClaimQuestReward(pydantic.BaseModel):
        """
        Validation class for the claim quest reward request

        Attributes:
            questMcpId: The quest id
        """
        questMcpId: Annotated[str, AfterValidator(UUIDString)]

    class ClaimTerritory(pydantic.BaseModel):
        """
        Validation class for the claim territory request

        Attributes:
            territoryId: The territory id
        """
        territoryId: str

    class ClientAddedExternalAccount(pydantic.BaseModel):
        """
        Validation class for the external account link tracking request

        Attributes:
        """

    class ClientTrackedRetentionAnalytics(pydantic.BaseModel):
        """
        Validation class for the level tracking request

        Attributes:
        """

    class CollectHammerQuest_Energy(pydantic.BaseModel):
        """
        Validation class for the hammer quest energy request

        Attributes:
        """
        pass

    class CollectHammerQuest_Realtime(pydantic.BaseModel):
        """
        Validation class for the hammer quest realtime request

        Attributes:
        """
        pass

    class CraftRecipe(pydantic.BaseModel):
        """
        Validation class for the craft recipe request

        Attributes:
        """
        pass

    class DeleteFriend(pydantic.BaseModel):
        """
        Validation class for the delete friend request

        Attributes:
            friendInstanceId: The friend instance id to unfriend
            friendInstanceIds: The list of friend instance ids to unfriend
        """
        friendInstanceId: Optional[Annotated[str, AfterValidator(UUIDString)]] = None
        friendInstanceIds: Optional[Annotated[str, AfterValidator(UUIDString)]] = None

    class EvolveHero(pydantic.BaseModel):
        """
        Validation class for the evolve hero request

        Attributes:
            heroItemId: The hero UUID
            bIsInPit: If the hero is in the pit
            evoPathName: The evolution path name
        """
        heroItemId: Annotated[str, AfterValidator(UUIDString)]
        bIsInPit: bool
        evoPathName: str

    class FinalizeLevel(pydantic.BaseModel):
        """
        Validation class for the finalise level request

        Attributes:
            levelItemId: The level UUID
            levelElement: The level element
            claimDepth: The claim depth
            claimedItems: The claimed items
            seenCharacters: The seen characters
            postBattleResults: The post battle results
            battleMetaData: The battle metadata AntiCheat report (optional)
            dailyQuestZoneType: The daily quest zone type
            partyItemId: The party UUID
            bShouldGiveBonus: If the player should get a bonus
        """
        levelItemId: Annotated[str, AfterValidator(UUIDString)]
        levelElement: Optional[str] = None
        claimDepth: int
        claimedItems: list[dict[str, str | int]]
        seenCharacters: list
        postBattleResults: Optional[
            dict[str, dict[str, int] | list[Annotated[str, AfterValidator(UUIDStringOptional)]] | list[
                Annotated[str, AfterValidator(CharacterTemplateId)]]]] = None
        battleMetaData: Optional[str] = None
        dailyQuestZoneType: Optional[int] = None
        partyItemId: Optional[str] = None
        bShouldGiveBonus: Optional[bool] = None

    class FoilHero(pydantic.BaseModel):
        """
        Validation class for the foil hero request

        Attributes:
            heroItemId: The hero UUID
            bIsInPit: If the hero is in the pit
        """
        heroItemId: Annotated[str, AfterValidator(UUIDString)]
        bIsInPit: bool

    class GenerateDailyQuests(pydantic.BaseModel):
        """
        Validation class for the daily quests request

        Attributes:
        """

    class GenerateMatchWithFriend(pydantic.BaseModel):
        """
        Validation class for the generate match with friend request

        Attributes:
            friendInstanceId: The friend instance id
        """
        friendInstanceId: Annotated[str, AfterValidator(UUIDString)]

    class GenerateMatches(pydantic.BaseModel):
        """
        Validation class for the generate matches request

        Attributes:
        """
        pass

    class InitializeLevel(pydantic.BaseModel):
        """
        Validation class for the initialise level request

        Attributes:
            manifestVersion: The manifest version
            levelId: The level id
            partyMembers: The party members
            friendInstanceId: The friend instance id
            ltmId: The ltm id
            normalMode: If the level is in normal mode
            blitzMode: If the level is in blitz mode
            teamPower: The team power
        """
        manifestVersion: str
        levelId: str
        partyId: Optional[Annotated[str, AfterValidator(UUIDStringOptional)]] = None
        commanderId: Optional[Annotated[str, AfterValidator(UUIDStringOptional)]] = ""
        partyMembers: Optional[list[dict[str, str | Annotated[str, AfterValidator(UUIDStringOptional)]]]] = None
        friendInstanceId: Annotated[str, AfterValidator(UUIDStringOptional)] = ""
        ltmId: Optional[str] = None
        normalMode: Optional[bool] = None
        blitzMode: Optional[bool] = None
        teamPower: Optional[int] = None

    class JoinMatchmaking(pydantic.BaseModel):
        """
        Validation class for the join match making request

        Attributes:
        """

    class LevelUpHero(pydantic.BaseModel):
        """
        Validation class for the level up hero request

        Attributes:
            heroItemId: The hero UUID
            bIsInPit: If the hero is in the pit
            bMaxOut: If the hero is maxed out
            numLevelUps: The number of level ups
        """
        heroItemId: Annotated[str, AfterValidator(UUIDString)]
        bIsInPit: bool
        bMaxOut: bool
        numLevelUps: int

    class MarkHeroSeen(pydantic.BaseModel):
        """
        Validation class for the mark hero seen request

        Attributes:
            itemId: The item UUID
        """
        heroItemId: Annotated[str, AfterValidator(UUIDString)]

    class MarkItemSeen(pydantic.BaseModel):
        """
        Validation class for the mark item seen request

        Attributes:
            itemId: The item UUID
        """
        itemId: Annotated[str, AfterValidator(UUIDString)]

    class ModifyHeroArmor(pydantic.BaseModel):
        """
        Validation class for the modify hero armor request

        Attributes:
            heroItemId: The hero UUID
            bIsInPit: If the hero is in the pit
            gearArmorItemId: The gear armor UUID
        """
        heroItemId: Annotated[str, AfterValidator(UUIDString)]
        bIsInPit: bool
        gearArmorItemId: Annotated[str, AfterValidator(UUIDStringOptional)]

    class ModifyHeroGear(pydantic.BaseModel):
        """
        Validation class for the modify hero gear request

        Attributes:
            heroItemId: The hero UUID
            bIsInPit: If the hero is in the pit
            gearHeroItemId: The gear UUID
        """
        heroItemId: Annotated[str, AfterValidator(UUIDString)]
        bIsInPit: bool
        gearHeroItemId: Annotated[str, AfterValidator(UUIDStringOptional)]

    class ModifyHeroWeapon(pydantic.BaseModel):
        """
        Validation class for the modify hero weapon request

        Attributes:
            heroItemId: The hero UUID
            bIsInPit: If the hero is in the pit
            gearWeaponItemId: The gear weapon UUID
        """
        heroItemId: Annotated[str, AfterValidator(UUIDString)]
        bIsInPit: bool
        gearWeaponItemId: Annotated[str, AfterValidator(UUIDStringOptional)]

    class OpenGiftBox(pydantic.BaseModel):
        """
        Validation class for the open gift box request

        Attributes:
            itemId: The gift box UUID
        """
        itemId: Annotated[str, AfterValidator(UUIDString)]

    class OpenHeroChest(pydantic.BaseModel):
        """
        Validation class for the open hero chest request

        Attributes:
            towerId: The tower UUID
            itemTemplateId: The item template id
            itemQuantity: The item quantity
        """
        towerId: Annotated[str, AfterValidator(UUIDString)]
        itemTemplateId: Annotated[str, AfterValidator(CharacterTemplateId)]
        itemQuantity: int

    class PickHeroChest(pydantic.BaseModel):
        """
        Validation class for the pick hero chest request

        Attributes:
            towerId: The tower UUID
            heroTrackId: The hero track id
            heroChestType: The hero chest type
        """
        towerId: Annotated[str, AfterValidator(UUIDString)]
        heroTrackId: str
        heroChestType: str

    class PromoteHero(pydantic.BaseModel):
        """
        Validation class for the promote hero request

        Attributes:
            heroItemId: The hero UUID
            bIsInPit: If the hero is in the pit
            prestigePromote: If the hero is being prestige promoted
        """
        heroItemId: Annotated[str, AfterValidator(UUIDString)]
        bIsInPit: bool
        prestigePromote: bool

    class PurchaseCatalogEntry(pydantic.BaseModel):
        """
        Validation class for the purchase catalog entry request

        Attributes:
            offerId: The offer id
            purchaseQuantity: The purchase quantity
            currency: The currency
            currencySubType: The currency subtype
            expectedTotalPrice: The expected total price
            gameContext: The game context
        """
        offerId: str
        purchaseQuantity: int
        currency: str
        currencySubType: str
        expectedPrice: Optional[int] = None
        expectedTotalPrice: Optional[int] = None
        gameContext: Optional[str] = None

    class QueryProfile(pydantic.BaseModel):
        """
        Validation class for the query profile request

        Attributes:
        """

    class Reconcile(pydantic.BaseModel):
        """
        Validation class for the reconcile request

        Attributes:
            friendIdList: The friend UUID list
            outgoingIdList: The outgoing UUID list
            incomingIdList: The incoming UUID list
        """
        friendIdList: list[Annotated[str, AfterValidator(AccountId)]]
        outgoingIdList: list[Annotated[str, AfterValidator(AccountId)]]
        incomingIdList: list[Annotated[str, AfterValidator(AccountId)]]

    class RedeemToken(pydantic.BaseModel):
        """
        Validation class for the redeem token request

        Attributes:
            tokenTemplate: The templateid of the token to redeem
        """
        tokenTemplate: str

    class RefreshRunCount(pydantic.BaseModel):
        """
        Validation class for the refresh run count request

        Attributes:
        """
        pass

    class RemoveFriend(pydantic.BaseModel):
        """
        Validation class for the remove friend request

        Attributes:
            friendInstanceId: The friend instance id to unfriend
            friendInstanceIds: The list of friend instance ids to unfriend
        """
        friendInstanceId: Optional[Annotated[str, AfterValidator(UUIDString)]] = None
        friendInstanceIds: Optional[Annotated[str, AfterValidator(UUIDString)]] = None

    class RemoveFromMonsterPit(pydantic.BaseModel):
        """
        Validation class for the remove from monster pit request

        Attributes:
            characterItemId: The character UUID
        """
        characterItemId: Annotated[str, AfterValidator(UUIDString)]

    class RemoveHeroFromAllParties(pydantic.BaseModel):
        """
        Validation class for the remove hero from all parties request

        Attributes:
            heroItemId: The hero UUID
        """
        heroItemId: Annotated[str, AfterValidator(UUIDString)]

    class RequestPreregistrationReward(pydantic.BaseModel):
        """
        Validation class for the request preregistration reward request

        Attributes:
        """

    class RollHammerChests(pydantic.BaseModel):
        """
        Validation class for the roll hammer chest request

        Attributes:
        """

    class SelectHammerChest(pydantic.BaseModel):
        """
        Validation class for the select hammer chest request

        Attributes:
            chestId: The chest UUID
        """
        chestId: Annotated[str, AfterValidator(UUIDString)]

    class SelectStartOptions(pydantic.BaseModel):
        """
        Validation class for the select start options request

        Attributes:
            characterTemplateId: The character template id
            displayName: The display name
            affiliateId: The affiliate id
        """
        characterTemplateId: Annotated[str, AfterValidator(CharacterTemplateId)]
        displayName: str
        affiliateId: Optional[str] = ""

    class SellGear(pydantic.BaseModel):
        """
        Validation class for the sell gear request

        Attributes:
            itemId: The item UUID to sell
        """
        itemId: Annotated[str, AfterValidator(UUIDString)]

    class SellHero(pydantic.BaseModel):
        """
        Validation class for the sell hero request

        Attributes:
            heroItemId: The hero UUID
            bIsInPit: If the hero is in the pit
        """
        heroItemId: Annotated[str, AfterValidator(UUIDString)]
        bIsInPit: bool

    class SellMultipleGear(pydantic.BaseModel):
        """
        Validation class for the sell multiple gear request

        Attributes:
            itemIds: The item UUIDs to sell
        """
        itemIds: list[Annotated[str, AfterValidator(UUIDString)]]

    class SellTreasure(pydantic.BaseModel):
        """
        Validation class for the sell treasure request

        Attributes:
            itemTemplateId: The item template id
            quantity: The quantity to sell
        """
        itemTemplateId: str
        quantity: int

    class SendGiftPoints(pydantic.BaseModel):
        """
        Validation class for the send gift points request

        Attributes:
        """

    class SetAffiliate(pydantic.BaseModel):
        """
        Validation class for the set sac request

        Attributes:
            affiliateId: The sac
        """
        affiliateId: str

    class SetDefaultParty(pydantic.BaseModel):
        """
        Validation class for the set default party request

        Attributes:
            partyId: The party UUID
            type: The party type
        """
        partyId: Annotated[str, AfterValidator(UUIDString)]
        type: str

    class SetRepHero(pydantic.BaseModel):
        """
        Validation class for the set rep hero request

        Attributes:
            heroId: The hero UUID
            slotIdx: The slot index
        """
        heroId: Annotated[str, AfterValidator(UUIDString)]
        slotIdx: int

    class SuggestFriends(pydantic.BaseModel):
        """
        Validation class for the suggest friends request

        Attributes:
        """

    class SuggestionResponse(pydantic.BaseModel):
        """
        Validation class for the suggestion response request

        Attributes:
            invitedFriendInstanceIds: The invited friend instance ids
            rejectedFriendInstanceIds: The rejected friend instance ids
        """
        invitedFriendInstanceIds: list[Annotated[str, AfterValidator(UUIDString)]]
        rejectedFriendInstanceIds: list[Annotated[str, AfterValidator(UUIDString)]]

    class TapHammerChest(pydantic.BaseModel):
        """
        Validation class for the tap hammer chest request

        Attributes:
        """

    class UnlockArmorGear(pydantic.BaseModel):
        """
        Validation class for the unlock armor gear request

        Attributes:
            heroItemId: The hero UUID
        """
        heroItemId: Annotated[str, AfterValidator(UUIDString)]

    class UnlockHeroGear(pydantic.BaseModel):
        """
        Validation class for the unlock hero gear request

        Attributes:
            heroItemId: The hero UUID
        """
        heroItemId: Annotated[str, AfterValidator(UUIDString)]

    class UnlockRegion(pydantic.BaseModel):
        """
        Validation class for the unlock region request

        Attributes:
            regionId: The region id
        """
        regionId: str

    class UnlockWeaponGear(pydantic.BaseModel):
        """
        Validation class for the unlock weapon gear request

        Attributes:
            heroItemId: The hero UUID
        """
        heroItemId: Annotated[str, AfterValidator(UUIDString)]

    class UpdateAccountHeadlessStatus(pydantic.BaseModel):
        """
        Validation class for the update account headless status request

        Attributes:
        """

    class UpdateFriends(pydantic.BaseModel):
        """
        Validation class for the update friends request

        Attributes:
            friendInstanceId: The friend instance id
        """
        friendInstanceId: Annotated[str, AfterValidator(UUIDStringOptional)]

    class UpdateMonsterPitPower(pydantic.BaseModel):
        """
        Validation class for the update monster pit power request

        Attributes:
        """

    class UpdateParty(pydantic.BaseModel):
        """
        Validation class for the update party request

        Attributes:
            partyItemId: The party UUID
            partyInstance: The party instance
        """
        partyItemId: Annotated[str, AfterValidator(UUIDString)]
        partyInstance: dict[str, list[Annotated[str, AfterValidator(UUIDStringOptional)]] | int | str]

    class UpgradeBuilding(pydantic.BaseModel):
        """
        Validation class for the upgrade building request

        Attributes:
            buildingItemId: The building UUID
        """
        buildingItemId: Annotated[str, AfterValidator(UUIDString)]

    class UpgradeHero(pydantic.BaseModel):
        """
        Validation class for the upgrade hero request

        Attributes:
            heroItemId: The hero UUID
            bIsInPit: If the hero is in the pit
            potionItems: The potion items
            weaponUpgrades: The weapon upgrades
        """
        heroItemId: Annotated[str, AfterValidator(UUIDString)]
        bIsInPit: bool
        potionItems: list[dict[str, str | int]]
        weaponUpgrades: list[dict[str, str | int]]

    class UpgradeHeroSkills(pydantic.BaseModel):
        """
        Validation class for the upgrade hero skills request

        Attributes:
            heroItemId: The hero UUID
            bIsInPit: If the hero is in the pit
            xpToSpend: The xp to spend
        """
        heroItemId: Annotated[str, AfterValidator(UUIDString)]
        bIsInPit: bool
        xpToSpend: int

    class VerifyRealMoneyPurchase(pydantic.BaseModel):
        """
        Validation class for the verify real money purchase request

        Attributes:
            appStore: The app store
            appStoreId: The app store id
            receiptId: The receipt id
            receiptInfo: The receipt info
            purchaseCorrelationId: The purchase correlation id
        """
        appStore: str
        appStoreId: str
        receiptId: str
        receiptInfo: str
        purchaseCorrelationId: Optional[str]

class MCPQueryValidation:
    """
    Validation for MCP requests to use the correct query arguments
    """

    class MCPLevels(pydantic.BaseModel):
        """
        Validation class for MCP requests that apply to the levels profile only

        Attributes:
            profileId: The levels profileId
            rvn: The client's current profile revision
        """
        profileId: Annotated[str, AfterValidator(ProfileLevels)]
        rvn: Optional[int] = -1

    class MCPFriends(pydantic.BaseModel):
        """
        Validation class for MCP requests that apply to the friends profile only

        Attributes:
            profileId: The friends profileId
            rvn: The client's current profile revision
        """
        profileId: Annotated[str, AfterValidator(ProfileFriends)]
        rvn: Optional[int] = -1

    class MCPMonsterpit(pydantic.BaseModel):
        """
        Validation class for MCP requests that apply to the monsterpit profile only

        Attributes:
            profileId: The monsterpit profileId
            rvn: The client's current profile revision
        """
        profileId: Annotated[str, AfterValidator(ProfileMonsterpit)]
        rvn: Optional[int] = -1

    class MCPProfile0(pydantic.BaseModel):
        """
        Validation class for MCP requests that apply to profile0 profile only

        Attributes:
            profileId: The profile0 profile
            rvn: The client's current profile revision
        """
        profileId: Annotated[str, AfterValidator(ProfileProfile0)]
        rvn: Optional[int] = -1

    class MCPProfile0Monsterpit(pydantic.BaseModel):
        """
        Validation class for MCP requests that apply to profile0 or monsterpit profiles

        Attributes:
            profileId: The profile0 or monsterpit profile
            rvn: The client's current profile revision
        """
        profileId: Annotated[str, AfterValidator(ProfileProfile0MonsterPit)]
        rvn: Optional[int] = -1

    class MCPMultiplayer(pydantic.BaseModel):
        """
        Validation class for MCP requests that apply to multiplayer profiles only

        Attributes:
            profileId: The multiplayer profile
            rvn: The client's current profile revision
        """
        profileId: Annotated[str, AfterValidator(ProfileMultiplayer)]
        rvn: Optional[int] = -1

    class MCPAnyProfile(pydantic.BaseModel):
        """
        Validation class for MCP requests that use any profile

        Attributes:
            profileId: Any valid profileId
            rvn: The client's current profile revision
        """
        profileId: Annotated[str, AfterValidator(ProfileAny)]
        rvn: Optional[int] = -1
