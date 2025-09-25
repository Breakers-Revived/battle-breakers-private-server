"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Contains validation classes for requests
"""
import uuid
from typing_extensions import Callable, Any, Optional

import pydantic
import pydantic_core


class UUIDString(str):
    """
    Validation class for UUID strings
    """

    @classmethod
    def __get_pydantic_json_schema__(
            cls, core_schema: pydantic_core.core_schema.JsonSchema, handler: pydantic.GetJsonSchemaHandler
    ):
        json_schema = handler(core_schema)
        json_schema.update(type="string", format="binary")
        return json_schema

    @classmethod
    def validate(cls, v: Any, _: pydantic_core.core_schema.ValidationInfo) -> str:
        """
        Validates the UUID string

        :param v: The UUID string
        :param _: The validation info
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

    @classmethod
    def __get_pydantic_core_schema__(
            cls, source: type[Any], handler: Callable[[Any], pydantic_core.core_schema.CoreSchema]
    ):
        return pydantic_core.core_schema.with_info_plain_validator_function(cls.validate)


class CharacterTemplateId(str):
    """
    Validation class for Character Template IDs
    """

    @classmethod
    def __get_pydantic_json_schema__(
            cls, core_schema: pydantic_core.core_schema.JsonSchema, handler: pydantic.GetJsonSchemaHandler
    ):
        json_schema = handler(core_schema)
        json_schema.update(type="string", format="binary")
        return json_schema

    @classmethod
    def validate(cls, v: Any, _: pydantic_core.core_schema.ValidationInfo) -> str:
        """
        Validates the Character Template ID

        :param v: The Character Template ID
        :param _: The validation info
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

    @classmethod
    def __get_pydantic_core_schema__(
            cls, source: type[Any], handler: Callable[[Any], pydantic_core.core_schema.CoreSchema]
    ) -> pydantic_core.core_schema.CoreSchema:
        return pydantic_core.core_schema.with_info_plain_validator_function(cls.validate)


class AccountId(str):
    """
    Validation class for Account ID strings
    """

    @classmethod
    def __get_pydantic_json_schema__(
            cls, core_schema: pydantic_core.core_schema.JsonSchema, handler: pydantic.GetJsonSchemaHandler
    ):
        json_schema = handler(core_schema)
        json_schema.update(type="string", format="binary")
        return json_schema

    @classmethod
    def validate(cls, v: Any, _: pydantic_core.core_schema.ValidationInfo) -> str:
        """
        Validates the Account ID string

        :param v: The Account ID string
        :param _: The validation info
        :return: The Account ID string
        :raises ValueError: If the Account ID is invalid
        """
        if not isinstance(v, str):
            raise ValueError('AccountId must be a string')
        try:
            if len(v) != 32:
                raise ValueError('Invalid Account ID string')
            int(v, 16)
        except ValueError:
            raise ValueError('Invalid Account ID string')
        return v

    @classmethod
    def __get_pydantic_core_schema__(
            cls, source: type[Any], handler: Callable[[Any], pydantic_core.core_schema.CoreSchema]
    ) -> pydantic_core.core_schema.CoreSchema:
        return pydantic_core.core_schema.with_info_plain_validator_function(cls.validate)


class MCPValidation:
    """
    Validation parent class for MCP requests
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
        levelItemId: UUIDString
        # These don't get sent when abandoning a level from another device in an old version
        depthCompleted: Optional[int]
        # These don't get sent by old clients
        levelElement: Optional[str]
        postBattleResults: Optional[dict[str, dict[str, int] | list[UUIDString] | list[CharacterTemplateId]]]
        dailyQuestZoneType: Optional[int]

    class AddFriend(pydantic.BaseModel):
        """
        Validation class for the add friend request (wex + epic)

        Attributes:
            friendAccountId: The epic account id
        """
        friendAccountId: AccountId

    class AddToMonsterPit(pydantic.BaseModel):
        """
        Validation class for the add to monster pit request

        Attributes:
            characterItemId: The character UUID
        """
        characterItemId: UUIDString

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
        partyMembers: list[dict[str, str | UUIDString]]
        friendInstanceId: Optional[UUIDString]

    class BulkImproveHeroes(pydantic.BaseModel):
        """
        Validation class for the bulk improve heroes request

        Attributes:
            detail: The character ids
        """
        detail: list[dict[str, UUIDString | list | list[dict[str, int]] | int]]

    class BuyBackFromMonsterPit(pydantic.BaseModel):
        """
        Validation class for the buyback from monster pit request

        Attributes:
            characterTemplateId: The character template id
        """
        characterTemplateId: CharacterTemplateId

    class ClaimAccountReward(pydantic.BaseModel):
        """
        Validation class for the claim account reward request

        Attributes:
            perks: The list of perks
        """
        perks: list[dict[str, UUIDString | int]]

    class ClaimQuestReward(pydantic.BaseModel):
        """
        Validation class for the claim quest reward request

        Attributes:
            questMcpId: The quest id
        """
        questMcpId: UUIDString

    class ClaimTerritory(pydantic.BaseModel):
        """
        Validation class for the claim territory request

        Attributes:
            territoryId: The territory id
        """
        territoryId: str

    class EvolveHero(pydantic.BaseModel):
        """
        Validation class for the evolve hero request

        Attributes:
            heroItemId: The hero UUID
            bIsInPit: If the hero is in the pit
            evoPathName: The evolution path name
        """
        heroItemId: UUIDString
        bIsInPit: bool
        evoPathName: str

    class FinalizeLevel(pydantic.BaseModel):
        """
        Validation class for the finalize level request

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
        levelItemId: UUIDString
        levelElement: str
        claimDepth: int
        claimedItems: list[dict[str, str | int]]
        seenCharacters: list
        postBattleResults: dict[str, dict[str, int] | list[UUIDString] | list[CharacterTemplateId]]
        battleMetaData: str = None
        dailyQuestZoneType: int
        partyItemId: str
        bShouldGiveBonus: bool

    class FoilHero(pydantic.BaseModel):
        """
        Validation class for the foil hero request

        Attributes:
            heroItemId: The hero UUID
            bIsInPit: If the hero is in the pit
        """
        heroItemId: UUIDString
        bIsInPit: bool

    class GenerateMatchWithFriend(pydantic.BaseModel):
        """
        Validation class for the generate match with friend request

        Attributes:
            friendInstanceId: The friend instance id
        """
        friendInstanceId: UUIDString

    class InitializeLevel(pydantic.BaseModel):
        """
        Validation class for the initialize level request

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
        partyMembers: list[dict[str, str | UUIDString]]
        friendInstanceId: UUIDString
        ltmId: str = None
        normalMode: bool
        blitzMode: bool
        teamPower: int

    class LevelUpHero(pydantic.BaseModel):
        """
        Validation class for the level up hero request

        Attributes:
            heroItemId: The hero UUID
            bIsInPit: If the hero is in the pit
            bMaxOut: If the hero is maxed out
            numLevelUps: The number of level ups
        """
        heroItemId: UUIDString
        bIsInPit: bool
        bMaxOut: bool
        numLevelUps: int

    class MarkItemSeen(pydantic.BaseModel):
        """
        Validation class for the mark item seen request

        Attributes:
            itemId: The item UUID
        """
        itemId: UUIDString

    class ModifyHeroArmor(pydantic.BaseModel):
        """
        Validation class for the modify hero armor request

        Attributes:
            heroItemId: The hero UUID
            bIsInPit: If the hero is in the pit
            gearArmorItemId: The gear armor UUID
        """
        heroItemId: UUIDString
        bIsInPit: bool
        gearArmorItemId: UUIDString

    class ModifyHeroGear(pydantic.BaseModel):
        """
        Validation class for the modify hero gear request

        Attributes:
            heroItemId: The hero UUID
            bIsInPit: If the hero is in the pit
            gearHeroItemId: The gear UUID
        """
        heroItemId: UUIDString
        bIsInPit: bool
        gearHeroItemId: UUIDString

    class ModifyHeroWeapon(pydantic.BaseModel):
        """
        Validation class for the modify hero weapon request

        Attributes:
            heroItemId: The hero UUID
            bIsInPit: If the hero is in the pit
            gearWeaponItemId: The gear weapon UUID
        """
        heroItemId: UUIDString
        bIsInPit: bool
        gearWeaponItemId: UUIDString

    class OpenGiftBox(pydantic.BaseModel):
        """
        Validation class for the open gift box request

        Attributes:
            itemId: The gift box UUID
        """
        itemId: UUIDString

    class OpenHeroChest(pydantic.BaseModel):
        """
        Validation class for the open hero chest request

        Attributes:
            towerId: The tower UUID
            itemTemplateId: The item template id
            itemQuantity: The item quantity
        """
        towerId: UUIDString
        itemTemplateId: CharacterTemplateId
        itemQuantity: int

    class PickHeroChest(pydantic.BaseModel):
        """
        Validation class for the pick hero chest request

        Attributes:
            towerId: The tower UUID
            heroTrackId: The hero track id
            heroChestType: The hero chest type
        """
        towerId: UUIDString
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
        heroItemId: UUIDString
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
        expectedTotalPrice: int
        gameContext: str

    class Reconcile(pydantic.BaseModel):
        """
        Validation class for the reconcile request

        Attributes:
            friendIdList: The friend UUID list
            outgoingIdList: The outgoing UUID list
            incomingIdList: The incoming UUID list
        """
        friendIdList: list[AccountId]
        outgoingIdList: list[AccountId]
        incomingIdList: list[AccountId]

    class RemoveFromMonsterPit(pydantic.BaseModel):
        """
        Validation class for the remove from monster pit request

        Attributes:
            characterItemId: The character UUID
        """
        characterItemId: UUIDString

    class SelectHammerChest(pydantic.BaseModel):
        """
        Validation class for the select hammer chest request

        Attributes:
            chestId: The chest UUID
        """
        chestId: UUIDString

    class SelectStartOptions(pydantic.BaseModel):
        """
        Validation class for the select start options request

        Attributes:
            characterTemplateId: The character template id
            displayName: The display name
            affiliateId: The affiliate id
        """
        characterTemplateId: CharacterTemplateId
        displayName: str
        affiliateId: str

    class SellHero(pydantic.BaseModel):
        """
        Validation class for the sell hero request

        Attributes:
            heroItemId: The hero UUID
            bIsInPit: If the hero is in the pit
        """
        heroItemId: UUIDString
        bIsInPit: bool

    class SetDefaultParty(pydantic.BaseModel):
        """
        Validation class for the set default party request

        Attributes:
            partyId: The party UUID
            type: The party type
        """
        partyId: UUIDString
        type: str

    class SetRepHero(pydantic.BaseModel):
        """
        Validation class for the set rep hero request

        Attributes:
            heroId: The hero UUID
            slotIdx: The slot index
        """
        heroId: UUIDString
        slotIdx: int

    class SuggestionResponse(pydantic.BaseModel):
        """
        Validation class for the suggestion response request

        Attributes:
            invitedFriendInstanceIds: The invited friend instance ids
            rejectedFriendInstanceIds: The rejected friend instance ids
        """
        invitedFriendInstanceIds: list[UUIDString]
        rejectedFriendInstanceIds: list[UUIDString]

    class UnlockArmorGear(pydantic.BaseModel):
        """
        Validation class for the unlock armor gear request

        Attributes:
            heroItemId: The hero UUID
        """
        heroItemId: UUIDString

    class UnlockHeroGear(pydantic.BaseModel):
        """
        Validation class for the unlock hero gear request

        Attributes:
            heroItemId: The hero UUID
        """
        heroItemId: UUIDString

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
        heroItemId: UUIDString

    class UpdateFriends(pydantic.BaseModel):
        """
        Validation class for the update friends request

        Attributes:
            friendInstanceId: The friend instance id
        """
        friendInstanceId: UUIDString

    class UpdateParty(pydantic.BaseModel):
        """
        Validation class for the update party request

        Attributes:
            partyItemId: The party UUID
            partyInstance: The party instance
        """
        partyItemId: UUIDString
        partyInstance: dict[str, list[UUIDString] | int | str]

    class UpgradeBuilding(pydantic.BaseModel):
        """
        Validation class for the upgrade building request

        Attributes:
            buildingItemId: The building UUID
        """
        buildingItemId: UUIDString

    class UpgradeHero(pydantic.BaseModel):
        """
        Validation class for the upgrade hero request

        Attributes:
            heroItemId: The hero UUID
            bIsInPit: If the hero is in the pit
            potionItems: The potion items
            weaponUpgrades: The weapon upgrades
        """
        heroItemId: UUIDString
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
        heroItemId: UUIDString
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
