"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Class based systems for each of the storefronts in the storefront service
"""
from typing_extensions import Any, Self, Optional


class Offer:
    """
    Class based system to handle offers for a catalog entry in the storefront service
    """

    def __init__(self, offer_id: Optional[str] = None, dev_name: Optional[str] = None, offer_type: Optional[str] = None,
                 prices: Optional[list[dict[str, str | int]]] = None, categories: Optional[list[str]] = None,
                 daily_limit: Optional[int] = None, weekly_limit: Optional[int] = None,
                 monthly_limit: Optional[int] = None,
                 refundable: Optional[bool] = None, app_store_id: Optional[list[str]] = None,
                 requirements: Optional[list[dict[str, str | int]]] = None,
                 meta_info: Optional[list[dict[str, str | int]]] = None,
                 catalog_group: Optional[str] = None, catalog_group_priority: Optional[int] = None,
                 sort_priority: Optional[int] = None, title: Optional[str] = None,
                 short_description: Optional[str] = None, description: Optional[str] = None,
                 display_asset_path: Optional[str] = None,
                 item_grants: Optional[list[dict[str, str | int]]] = None) -> None:
        """
        Initialise the offer class.
        This will setup the variables for the offer
        """
        self.offer_id: str = offer_id or ""
        self.dev_name: str = dev_name or ""
        self.offer_type: str = offer_type or ""
        self.prices: list[dict[str, str | int]] = prices or []
        self.categories: list[str] = categories or []
        self.daily_limit: int = daily_limit or -1
        self.weekly_limit: int = weekly_limit or -1
        self.monthly_limit: int = monthly_limit or -1
        self.refundable: bool = refundable or False
        self.app_store_id: list[str] = app_store_id or [
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            ""
        ]
        self.requirements: list[dict[str, str | int]] = requirements or []
        self.meta_info: list[dict[str, str | int]] = meta_info or []
        self.catalog_group: str = catalog_group or ""
        self.catalog_group_priority: int = catalog_group_priority or 0
        self.sort_priority: int = sort_priority or 0
        self.title: str = title or ""
        self.short_description: str = short_description or ""
        self.description: str = description or ""
        self.display_asset_path: str = display_asset_path or ""
        self.item_grants: list[dict[str, str | int]] = item_grants or [{}]

    def __repr__(self) -> str:
        """
        Get the representation of the offer class
        :return: The representation of the offer class
        """
        return f"<Offer>"

    def __str__(self) -> str:
        """
        Get the string of the offer class
        :return: The string of the offer class
        """
        return self.__repr__()

    def __dict__(self) -> dict[str, Any]:
        """
        Get the dictionary of the offer class
        :return: The dictionary of the offer class
        """
        return {
            "offerId": self.offer_id,
            "devName": self.dev_name,
            "offerType": self.offer_type,
            "prices": self.prices,
            "categories": self.categories,
            "dailyLimit": self.daily_limit,
            "weeklyLimit": self.weekly_limit,
            "monthlyLimit": self.monthly_limit,
            "refundable": self.refundable,
            "appStoreId": self.app_store_id,
            "requirements": self.requirements,
            "metaInfo": self.meta_info,
            "catalogGroup": self.catalog_group,
            "catalogGroupPriority": self.catalog_group_priority,
            "sortPriority": self.sort_priority,
            "title": self.title,
            "shortDescription": self.short_description,
            "description": self.description,
            "displayAssetPath": self.display_asset_path,
            "itemGrants": self.item_grants
        }

    def __getitem__(self, key: str) -> Any:
        """
        Get the value of the key in the offer class
        :param key: The key to get the value of
        :return: The value of the key in the offer class
        """
        return getattr(self, key)

    def __setitem__(self, key: str, value: Any) -> None:
        """
        Set the value of the key in the offer class
        :param key: The key to set the value of
        :param value: The value to set the key to
        :return: The value of the key in the offer class
        """
        setattr(self, key, value)

    def __delitem__(self, key: str) -> None:
        """
        Delete the key in the offer class
        :param key: The key to delete
        :return: The value of the key in the offer class
        """
        delattr(self, key)

    def __len__(self) -> int:
        """
        Get the length of the offer
        :return: The length of the offer
        """
        return len(self.__dict__())


class Storefront:
    """
    Class based system to handle a storefront for the storefront catalog service
    """

    def __init__(self) -> None:
        """
        Initialise the storefront class.
        This will setup the variables for the storefront
        """
        self.name: str = ""
        self.catalog_entries: list[Offer] = []

    def __repr__(self) -> str:
        """
        Get the representation of the storefront class
        :return: The representation of the storefront class
        """
        return f"<Storefront>"

    def __str__(self) -> str:
        """
        Get the string of the storefront class
        :return: The string of the storefront class
        """
        return self.__repr__()

    def __dict__(self) -> dict[str, Any]:
        """
        Get the dictionary of the storefront class
        :return: The dictionary of the storefront class
        """
        catalog_entries = []
        for catalog_entry in self.catalog_entries:
            catalog_entries.append(catalog_entry.__dict__())
        return {
            "name": self.name,
            "catalogEntries": catalog_entries
        }

    def __getitem__(self, key: str) -> Any:
        """
        Get the value of the key in the storefront class
        :param key: The key to get the value of
        :return: The value of the key in the storefront class
        """
        return getattr(self, key)

    def __setitem__(self, key: str, value: Any) -> None:
        """
        Set the value of the key in the storefront class
        :param key: The key to set the value of
        :param value: The value to set the key to
        :return: The value of the key in the storefront class
        """
        setattr(self, key, value)

    def __delitem__(self, key: str) -> None:
        """
        Delete the key in the storefront class
        :param key: The key to delete
        :return: The value of the key in the storefront class
        """
        delattr(self, key)

    def __len__(self) -> int:
        """
        Get the length of the storefront
        :return: The length of the storefront
        """
        return len(self.__dict__())

    async def get_offer_by_id(self, offer_id: str) -> Optional[Offer]:
        """
        Get an offer by its ID from the storefront
        :param offer_id: The ID of the offer to get
        :return: The offer with the given ID, or None if not found
        """
        for offer in self.catalog_entries:
            if offer.offer_id == offer_id:
                return offer
        return None


class SecretShopPage3(Storefront):
    """
    Class based system to handle the SecretShopPage3 storefront for the storefront catalog service
    """

    def __init__(self) -> None:
        """
        Initialise the SecretShopPage3 storefront class.
        This will setup the variables for the SecretShopPage3 storefront
        """
        super().__init__()

    async def update_storefront(self) -> None:
        """
        Update the storefront for the SecretShopPage3 storefront class with the latest data
        :return: None
        """
        # temporary implementation
        self.catalog_entries.append(Offer(
            offer_id="151C2CE6E94F49AEB6C98E310B601C93",
            dev_name="SecretShop.Page03.UnderworldTrader.45",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 200, 'dynamicRegularPrice': -1,
                 'finalPrice': 170, 'saleType': 'AmountOff', 'saleExpiration': '9999-12-31T23:59:59.999Z',
                 'basePrice': 170}],
            daily_limit=1,
            meta_info=[{'key': 'VipLevelMin', 'value': '3'}],
            item_grants=[{'templateId': 'Reagent:Reagent_Shard_Fire', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="7BF89D7E6B6C4535867A0D46837E4AB4",
            dev_name="SecretShop.Page03.Misc.20",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Currency:Gold', 'regularPrice': 50000,
                     'dynamicRegularPrice': -1, 'finalPrice': 50000, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 50000}],
            daily_limit=1,
            item_grants=[{'templateId': 'Reagent:Reagent_RXT_Parts_Small', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="BD21C4382AB74F6086951E25EF92310A",
            dev_name="SecretShop.Page03.Ore.04",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 10, 'dynamicRegularPrice': -1,
                 'finalPrice': 10, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 10}],
            daily_limit=3,
            item_grants=[{'templateId': 'Ore:Ore_Magicite', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="98712BB0A82E49E092787E1ECF972DDF",
            dev_name="SecretShop.Page03.Reagent.51",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 200, 'dynamicRegularPrice': -1,
                 'finalPrice': 170, 'saleType': 'AmountOff', 'saleExpiration': '9999-12-31T23:59:59.999Z',
                 'basePrice': 170}],
            daily_limit=1,
            item_grants=[{'templateId': 'Reagent:Reagent_Shard_Fire', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="9A4615BC36F04DC58BF42E06686F34C6",
            dev_name="SecretShop.Page03.CharShard.17",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Currency:Gold', 'regularPrice': 7500000,
                     'dynamicRegularPrice': -1, 'finalPrice': 7500000, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 7500000}],
            daily_limit=1,
            item_grants=[{'templateId': 'Voucher:Voucher_Chest_Gold', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="24D10F44ABF141ABB8551959E4716C14",
            dev_name="SecretShop.Page03.Elixir.13",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Currency:Gold', 'regularPrice': 400000,
                     'dynamicRegularPrice': -1, 'finalPrice': 340000, 'saleType': 'AmountOff',
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 340000}],
            daily_limit=2,
            item_grants=[{'templateId': 'UpgradePotion:UpgradeMana', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="1B46111A36A84D058DAFDF88B12E583E",
            dev_name="SecretShop.Page03.UnderworldTrader.32",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 25, 'dynamicRegularPrice': -1,
                 'finalPrice': 21, 'saleType': 'AmountOff', 'saleExpiration': '9999-12-31T23:59:59.999Z',
                 'basePrice': 21}],
            daily_limit=10,
            meta_info=[{'key': 'VipLevelMin', 'value': '3'}],
            item_grants=[{'templateId': 'UpgradePotion:UpgradeHealthMajor', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="AA5A66165EF440B29492517946D44D2C",
            dev_name="SecretShop.Page03.Free.25",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Currency:Gold', 'regularPrice': 10000,
                     'dynamicRegularPrice': -1, 'finalPrice': 0, 'saleType': 'AmountOff',
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=3,
            item_grants=[{'templateId': 'Currency:Hammer', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="DC18D15274E643BDA2028A87D13A7D28",
            dev_name="SecretShop.Page03.Misc.17",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Currency:Gold', 'regularPrice': 200,
                     'dynamicRegularPrice': -1, 'finalPrice': 170, 'saleType': 'AmountOff',
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 170}],
            daily_limit=5000,
            title="+100 ",
            item_grants=[{'templateId': 'Currency:HeroXp_Basic', 'quantity': 100}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="7AB3166204684F9EA6896CDDEC1BA7A0",
            dev_name="SecretShop.Page03.Free.38",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 2, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleType': 'AmountOff', 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 0}],
            daily_limit=1,
            item_grants=[{'templateId': 'Reagent:Reagent_HeroMap_Elemental', 'quantity': 100}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="D8654A64B37B4A84B9EB8AC40B5EBD74",
            dev_name="SecretShop.Page03.UnderworldTrader.42",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 200, 'dynamicRegularPrice': -1,
                 'finalPrice': 140, 'saleType': 'AmountOff', 'saleExpiration': '9999-12-31T23:59:59.999Z',
                 'basePrice': 140}],
            daily_limit=1,
            meta_info=[{'key': 'VipLevelMin', 'value': '3'}],
            item_grants=[{'templateId': 'Reagent:Reagent_Shard_Light', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="0EBDB5CEB58B4D7C939B7F8588B2E07E",
            dev_name="SecretShop.Page03.Reagent.38",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Currency:Gold', 'regularPrice': 2500,
                     'dynamicRegularPrice': -1, 'finalPrice': 2125, 'saleType': 'AmountOff',
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 2125}],
            daily_limit=10,
            item_grants=[{'templateId': 'Reagent:Reagent_Shared_T02', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="F9EBB700BF2747229DA1FCF580F38D57",
            dev_name="SecretShop.Page03.UnderworldTrader.33",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 5, 'dynamicRegularPrice': -1,
                     'finalPrice': 4, 'saleType': 'AmountOff', 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 4}],
            daily_limit=15,
            meta_info=[{'key': 'VipLevelMin', 'value': '3'}],
            item_grants=[{'templateId': 'UpgradePotion:UpgradeHealthMinor', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="4FB7C722ABA94A478D0DAC94B569686A",
            dev_name="SecretShop.Page03.Shard.20",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 200, 'dynamicRegularPrice': -1,
                 'finalPrice': 170, 'saleType': 'AmountOff', 'saleExpiration': '9999-12-31T23:59:59.999Z',
                 'basePrice': 170}],
            daily_limit=1,
            item_grants=[{'templateId': 'Reagent:Reagent_Shard_Water', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="611267C0B7174C4499804DCEBF51E2F5",
            dev_name="SecretShop.Page03.TreasureMap.13",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 10, 'dynamicRegularPrice': -1,
                 'finalPrice': 10, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 10}],
            daily_limit=10,
            item_grants=[{'templateId': 'TreasureMap:TM_MapResource', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="1D3216FA38B1449E83BD6CE25FE1AA1F",
            dev_name="SecretShop.Page03.Elixir.14",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Currency:Gold', 'regularPrice': 50000,
                     'dynamicRegularPrice': -1, 'finalPrice': 42500, 'saleType': 'AmountOff',
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 42500}],
            daily_limit=5,
            item_grants=[{'templateId': 'UpgradePotion:UpgradeStrengthMajor', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="FC51C6C13E2A4C1A9FC5F1B6D5F0516E",
            dev_name="SecretShop.Page03.Reagent.34",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Currency:Gold', 'regularPrice': 300000,
                     'dynamicRegularPrice': -1, 'finalPrice': 255000, 'saleType': 'AmountOff',
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 255000}],
            daily_limit=1,
            item_grants=[{'templateId': 'Reagent:Reagent_Shard_Water', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="F58DAA01720245339D3A3305432E2F28",
            dev_name="SecretShop.Page03.Reagent.37",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Currency:Gold', 'regularPrice': 300000,
                     'dynamicRegularPrice': -1, 'finalPrice': 255000, 'saleType': 'AmountOff',
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 255000}],
            daily_limit=1,
            item_grants=[{'templateId': 'Reagent:Reagent_Shard_Fire', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="1B0EA58B203A4F78AE48FF028730E87C",
            dev_name="SecretShop.Page03.Elixir.19",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 25, 'dynamicRegularPrice': -1,
                 'finalPrice': 25, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 25}],
            daily_limit=5,
            item_grants=[{'templateId': 'UpgradePotion:UpgradeStrengthMajor', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="6E40D70A546645CD8674A72D8FD21DC2",
            dev_name="SecretShop.Page03.UnderworldTrader.47",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 200, 'dynamicRegularPrice': -1,
                 'finalPrice': 170, 'saleType': 'AmountOff', 'saleExpiration': '9999-12-31T23:59:59.999Z',
                 'basePrice': 170}],
            daily_limit=1,
            meta_info=[{'key': 'VipLevelMin', 'value': '3'}],
            item_grants=[{'templateId': 'Reagent:Reagent_Shard_Nature', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="0393B1388866415787B0C58971D422BA",
            dev_name="SecretShop.Page03.UnderworldTraderGold.06",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Currency:Gold', 'regularPrice': 2500,
                     'dynamicRegularPrice': -1, 'finalPrice': 1500, 'saleType': 'AmountOff',
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 1500}],
            daily_limit=30,
            meta_info=[{'key': 'VipLevelMin', 'value': '3'}],
            item_grants=[{'templateId': 'Reagent:Reagent_Shared_T02', 'quantity': 1}],
        ))

    @classmethod
    async def init_storefront(cls) -> Self:
        """
        Initialise the SecretShopPage3 storefront
        :return: The initialised SecretShopPage3 storefront class
        """
        self: SecretShopPage3 = cls()
        self.name = "SecretShopPage3"
        self.catalog_entries = []
        return self


class SecretShopPage4(Storefront):
    """
    Class based system to handle the SecretShopPage4 storefront for the storefront catalog service
    """

    def __init__(self) -> None:
        """
        Initialise the SecretShopPage4 storefront class.
        This will setup the variables for the SecretShopPage4 storefront
        """
        super().__init__()

    async def update_storefront(self) -> None:
        """
        Update the storefront for the SecretShopPage4 storefront class with the latest data
        :return: None
        """
        # temporary implementation
        self.catalog_entries.append(Offer(
            offer_id="09CF43DF0DC64FFC9C7F40C8D7E051AD",
            dev_name="SecretShop.Page04.TreasureMap.31",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Currency:Gold', 'regularPrice': 500000,
                     'dynamicRegularPrice': -1, 'finalPrice': 425000, 'saleType': 'AmountOff',
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 425000}],
            daily_limit=1,
            item_grants=[{'templateId': 'TreasureMap:TM_Special_UnderwaterTunnel', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="A4804005DEE04226BFCBFEFBA8BFA903",
            dev_name="SecretShop.Page04.Elixir.25",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Currency:Gold', 'regularPrice': 4000,
                     'dynamicRegularPrice': -1, 'finalPrice': 3400, 'saleType': 'AmountOff',
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 3400}],
            daily_limit=30,
            item_grants=[{'templateId': 'UpgradePotion:UpgradeStrengthMinor', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="9C09FF121A51434FBE35E60EF9B5734C",
            dev_name="SecretShop.Page04.CharShard.18",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Currency:Gold', 'regularPrice': 7500000,
                     'dynamicRegularPrice': -1, 'finalPrice': 7500000, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 7500000}],
            daily_limit=1,
            item_grants=[{'templateId': 'Voucher:Voucher_Chest_Gold', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="103FE954E0E242D48D079C2851CD325F",
            dev_name="SecretShop.Page04.Reagent.85",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 200, 'dynamicRegularPrice': -1,
                 'finalPrice': 170, 'saleType': 'AmountOff', 'saleExpiration': '9999-12-31T23:59:59.999Z',
                 'basePrice': 170}],
            daily_limit=2,
            item_grants=[{'templateId': 'Reagent:Reagent_Shard_Light', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="7BBB5FE953ED481E8628BF654D7E6DE6",
            dev_name="SecretShop.Page04.Shard.28",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 200, 'dynamicRegularPrice': -1,
                 'finalPrice': 170, 'saleType': 'AmountOff', 'saleExpiration': '9999-12-31T23:59:59.999Z',
                 'basePrice': 170}],
            daily_limit=1,
            item_grants=[{'templateId': 'Reagent:Reagent_Shard_Light', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="4401C298A06B4B64893906A83AC723EF",
            dev_name="SecretShop.Page04.Free.41",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Currency:Gold', 'regularPrice': 10000,
                     'dynamicRegularPrice': -1, 'finalPrice': 0, 'saleType': 'AmountOff',
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=4,
            item_grants=[{'templateId': 'Currency:Hammer', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="5F5764CFA06B4213A95FC4AA520F2C25",
            dev_name="SecretShop.Page04.Misc.31",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Currency:Gold', 'regularPrice': 200,
                     'dynamicRegularPrice': -1, 'finalPrice': 170, 'saleType': 'AmountOff',
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 170}],
            daily_limit=1000,
            title="+100 ",
            item_grants=[{'templateId': 'Currency:HeroXp_Basic', 'quantity': 100}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="E5FF8D0E66F54FD9BFEACE2398A2A348",
            dev_name="SecretShop.Page04.UnderworldTrader.85",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 10, 'dynamicRegularPrice': -1,
                 'finalPrice': 7, 'saleType': 'AmountOff', 'saleExpiration': '9999-12-31T23:59:59.999Z',
                 'basePrice': 7}],
            daily_limit=20,
            meta_info=[{'key': 'VipLevelMin', 'value': '3'}],
            item_grants=[{'templateId': 'Ore:Ore_Magicite', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="945007F9F5734A37BED76E8FB912E00C",
            dev_name="SecretShop.Page04.TreasureMap.24",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Currency:Gold', 'regularPrice': 40000,
                     'dynamicRegularPrice': -1, 'finalPrice': 34000, 'saleType': 'AmountOff',
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 34000}],
            daily_limit=1,
            item_grants=[{'templateId': 'TreasureMap:TM_Special_BridgeOfLight', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="684D6B3200C5435D87FF9508AC8B1629",
            dev_name="SecretShop.Page04.Reagent.63",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Currency:Gold', 'regularPrice': 300000,
                     'dynamicRegularPrice': -1, 'finalPrice': 255000, 'saleType': 'AmountOff',
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 255000}],
            daily_limit=1,
            item_grants=[{'templateId': 'Reagent:Reagent_Shard_Water', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="42C688E164FB4334A4EDB33B8B0A6192",
            dev_name="SecretShop.Page04.Reagent.70",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Currency:Gold', 'regularPrice': 300000,
                     'dynamicRegularPrice': -1, 'finalPrice': 255000, 'saleType': 'AmountOff',
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 255000}],
            daily_limit=1,
            item_grants=[{'templateId': 'Reagent:Reagent_Shard_Light', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="E2FC949CD107472189555B67A02D02D9",
            dev_name="SecretShop.Page04.Elixir.22",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Currency:Gold', 'regularPrice': 4000,
                     'dynamicRegularPrice': -1, 'finalPrice': 3400, 'saleType': 'AmountOff',
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 3400}],
            daily_limit=30,
            item_grants=[{'templateId': 'UpgradePotion:UpgradeHealthMinor', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="478488F247984757A989D7AEA804B007",
            dev_name="SecretShop.Page04.Free.62",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Currency:Gold', 'regularPrice': 7500000,
                     'dynamicRegularPrice': -1, 'finalPrice': 0, 'saleType': 'AmountOff',
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            item_grants=[{'templateId': 'Voucher:Voucher_Chest_Gold', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="00686C7A6A6A46258BA85D9237896177",
            dev_name="SecretShop.Page04.UnderworldTrader.86",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 25, 'dynamicRegularPrice': -1,
                 'finalPrice': 21, 'saleType': 'AmountOff', 'saleExpiration': '9999-12-31T23:59:59.999Z',
                 'basePrice': 21}],
            daily_limit=10,
            meta_info=[{'key': 'VipLevelMin', 'value': '3'}],
            item_grants=[{'templateId': 'UpgradePotion:UpgradeHealthMajor', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="3ABA30206C98416B984170730F6838A9",
            dev_name="SecretShop.Page04.Reagent.87",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 200, 'dynamicRegularPrice': -1,
                 'finalPrice': 170, 'saleType': 'AmountOff', 'saleExpiration': '9999-12-31T23:59:59.999Z',
                 'basePrice': 170}],
            daily_limit=2,
            item_grants=[{'templateId': 'Reagent:Reagent_Shard_Nature', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="034652FBA49641339A13BDBD71E3BD03",
            dev_name="SecretShop.Page04.Misc.35",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Currency:Gold', 'regularPrice': 50000,
                     'dynamicRegularPrice': -1, 'finalPrice': 50000, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 50000}],
            daily_limit=2,
            item_grants=[{'templateId': 'Reagent:Reagent_RXT_Parts_Small', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="4B01C5CB45874FB795DB426C6B782D3D",
            dev_name="SecretShop.Page04.Ore.05",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Currency:Gold', 'regularPrice': 25000,
                     'dynamicRegularPrice': -1, 'finalPrice': 21250, 'saleType': 'AmountOff',
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 21250}],
            daily_limit=3,
            item_grants=[{'templateId': 'Ore:Ore_Magicite', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="CF797C9843024F7A88375E17B26FCF76",
            dev_name="SecretShop.Page04.UnderworldTrader.68",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 200, 'dynamicRegularPrice': -1,
                 'finalPrice': 170, 'saleType': 'AmountOff', 'saleExpiration': '9999-12-31T23:59:59.999Z',
                 'basePrice': 170}],
            daily_limit=1,
            meta_info=[{'key': 'VipLevelMin', 'value': '3'}],
            item_grants=[{'templateId': 'Reagent:Reagent_Shard_Dark', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="C8A993EEA44948B594F087D2D6D9EB59",
            dev_name="SecretShop.Page04.UnderworldTrader.65",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 200, 'dynamicRegularPrice': -1,
                 'finalPrice': 140, 'saleType': 'AmountOff', 'saleExpiration': '9999-12-31T23:59:59.999Z',
                 'basePrice': 140}],
            daily_limit=1,
            meta_info=[{'key': 'VipLevelMin', 'value': '3'}],
            item_grants=[{'templateId': 'Reagent:Reagent_Shard_Fire', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="0FF150C7D9C6411B9DB11FDB798C2155",
            dev_name="SecretShop.Page04.Elixir.24",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Currency:Gold', 'regularPrice': 50000,
                     'dynamicRegularPrice': -1, 'finalPrice': 42500, 'saleType': 'AmountOff',
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 42500}],
            daily_limit=10,
            item_grants=[{'templateId': 'UpgradePotion:UpgradeStrengthMajor', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="25A3B0B2AB3844C7BE2A7CC9772911DA",
            dev_name="SecretShop.Page04.Shard.26",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 200, 'dynamicRegularPrice': -1,
                 'finalPrice': 170, 'saleType': 'AmountOff', 'saleExpiration': '9999-12-31T23:59:59.999Z',
                 'basePrice': 170}],
            daily_limit=1,
            item_grants=[{'templateId': 'Reagent:Reagent_Shard_Dark', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="5ABFB9FA4C824236B63E384507020A13",
            dev_name="SecretShop.Page04.UnderworldTrader.88",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 100, 'dynamicRegularPrice': -1,
                 'finalPrice': 70, 'saleType': 'AmountOff', 'saleExpiration': '9999-12-31T23:59:59.999Z',
                 'basePrice': 70}],
            daily_limit=2,
            meta_info=[{'key': 'VipLevelMin', 'value': '3'}],
            item_grants=[{'templateId': 'UpgradePotion:UpgradeMana', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="FCDCCBB3BAFD414EB79446CDF3F128F9",
            dev_name="SecretShop.Page04.UnderworldTraderGold.15",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Currency:Gold', 'regularPrice': 4000,
                     'dynamicRegularPrice': -1, 'finalPrice': 2800, 'saleType': 'AmountOff',
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 2800}],
            daily_limit=15,
            meta_info=[{'key': 'VipLevelMin', 'value': '3'}],
            item_grants=[{'templateId': 'UpgradePotion:UpgradeStrengthMinor', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="6BBFC4FB2AEE49AD9C6E288A52B2DFB9",
            dev_name="SecretShop.Page04.UnderworldTraderGold.11",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Currency:Gold', 'regularPrice': 2500,
                     'dynamicRegularPrice': -1, 'finalPrice': 1500, 'saleType': 'AmountOff',
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 1500}],
            daily_limit=30,
            meta_info=[{'key': 'VipLevelMin', 'value': '3'}],
            item_grants=[{'templateId': 'Reagent:Reagent_Shared_T02', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="BA0AA33CB91B4031A769CFF25734131F",
            dev_name="SecretShop.Page04.UnderworldTrader.70",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 200, 'dynamicRegularPrice': -1,
                 'finalPrice': 170, 'saleType': 'AmountOff', 'saleExpiration': '9999-12-31T23:59:59.999Z',
                 'basePrice': 170}],
            daily_limit=1,
            meta_info=[{'key': 'VipLevelMin', 'value': '3'}],
            item_grants=[{'templateId': 'Reagent:Reagent_Shard_Light', 'quantity': 1}],
        ))

    @classmethod
    async def init_storefront(cls) -> Self:
        """
        Initialise the SecretShopPage4 storefront
        :return: The initialised SecretShopPage4 storefront class
        """
        self: SecretShopPage4 = cls()
        self.name = "SecretShopPage4"
        self.catalog_entries = []
        return self


class GemStore(Storefront):
    """
    Class based system to handle the GemStore storefront for the storefront catalog service
    """

    def __init__(self) -> None:
        """
        Initialise the GemStore storefront class.
        This will setup the variables for the GemStore storefront
        """
        super().__init__()

    async def update_storefront(self) -> None:
        """
        Update the storefront for the GemStore storefront class with the latest data
        :return: None
        """
        # temporary implementation
        self.catalog_entries.append(Offer(
            offer_id="3C3D9B0A42C2873D746F4D86FF28C245",
            dev_name="Pouch of Gems",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'RealMoney', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            app_store_id=[
                "",
                "00d74de590684ba9adf5e71842edbc7b",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
            ],
            meta_info=[{'key': 'bShowInGemStore', 'value': 'true'}],
            catalog_group="PouchOfGems",
            sort_priority=-1,
            title="Pouch of Gems",
            display_asset_path="/Game/UMG/Textures/Store/btn_StoreGemPouch.btn_StoreGemPouch",
            item_grants=[{'templateId': 'Currency:MtxPurchased', 'quantity': 500},
                         {'templateId': 'Reagent:Reagent_HeroMap_SuperRare', 'quantity': 10},
                         {'templateId': 'Reagent:Reagent_SupplyPoints_Elite', 'quantity': 100}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="2A5A0D104128328EDC4A27B5617FD200",
            dev_name="Bag of Gems",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'RealMoney', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            app_store_id=[
                "",
                "b1c1372c9d0a428bacde8161117b1b2c",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
            ],
            meta_info=[{'key': 'bShowInGemStore', 'value': 'true'}],
            catalog_group="BagOfGems",
            sort_priority=-3,
            title="Bag of Gems",
            display_asset_path="/Game/UMG/Textures/Store/btn_StoreGemBag.btn_StoreGemBag",
            item_grants=[{'templateId': 'Currency:MtxPurchased', 'quantity': 1000},
                         {'templateId': 'Currency:MtxPurchaseBonus', 'quantity': 250},
                         {'templateId': 'Reagent:Reagent_HeroMap_SuperRare', 'quantity': 30},
                         {'templateId': 'Reagent:Reagent_SupplyPoints_Elite', 'quantity': 100},
                         {'templateId': 'UpgradePotion:UpgradeHealthMajor', 'quantity': 20},
                         {'templateId': 'UpgradePotion:UpgradeStrengthMajor', 'quantity': 20}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="4B05C5C74FD94EA9D568BFAC0C0BDAE1",
            dev_name="Chest of Gems",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'RealMoney', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            app_store_id=[
                "",
                "900ee5f4f4244c00b61ff2a7a3850ab0",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
            ],
            meta_info=[{'key': 'bShowInGemStore', 'value': 'true'}],
            catalog_group="ChestOfGems",
            sort_priority=-4,
            title="Chest of Gems",
            display_asset_path="/Game/UMG/Textures/Store/btn_StoreGemGoldenChest.btn_StoreGemGoldenChest",
            item_grants=[{'templateId': 'Currency:MtxPurchased', 'quantity': 2000},
                         {'templateId': 'Currency:MtxPurchaseBonus', 'quantity': 700},
                         {'templateId': 'Reagent:Reagent_HeroMap_SuperRare', 'quantity': 60},
                         {'templateId': 'Reagent:Reagent_SupplyPoints_Elite', 'quantity': 200},
                         {'templateId': 'UpgradePotion:UpgradeHealthMajor', 'quantity': 40},
                         {'templateId': 'UpgradePotion:UpgradeStrengthMajor', 'quantity': 40}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="2D1D3AD847EABB6E86064997D9787928",
            dev_name="Castle Treasury",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'RealMoney', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            app_store_id=[
                "",
                "7d270c7e78d3439db8afe81bcd0b6b6a",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
            ],
            meta_info=[{'key': 'bShowInGemStore', 'value': 'true'}],
            catalog_group="CastleTreasury",
            sort_priority=-6,
            title="Castle Treasury",
            display_asset_path="/Game/UMG/Textures/Store/btn_StoreGemCastleTreasury.btn_StoreGemCastleTreasury",
            item_grants=[{'templateId': 'Currency:MtxPurchased', 'quantity': 3000},
                         {'templateId': 'Currency:MtxPurchaseBonus', 'quantity': 1200},
                         {'templateId': 'Reagent:Reagent_HeroMap_SuperRare', 'quantity': 100},
                         {'templateId': 'Reagent:Reagent_SupplyPoints_Elite', 'quantity': 300},
                         {'templateId': 'UpgradePotion:UpgradeHealthMajor', 'quantity': 75},
                         {'templateId': 'UpgradePotion:UpgradeStrengthMajor', 'quantity': 75}],
        ))

    @classmethod
    async def init_storefront(cls) -> Self:
        """
        Initialise the GemStore storefront
        :return: The initialised GemStore storefront class
        """
        self: GemStore = cls()
        self.name = "GemStore"
        self.catalog_entries = []
        return self


class SecretShopPage2(Storefront):
    """
    Class based system to handle the SecretShopPage2 storefront for the storefront catalog service
    """

    def __init__(self) -> None:
        """
        Initialise the SecretShopPage2 storefront class.
        This will setup the variables for the SecretShopPage2 storefront
        """
        super().__init__()

    async def update_storefront(self) -> None:
        """
        Update the storefront for the SecretShopPage2 storefront class with the latest data
        :return: None
        """
        # temporary implementation
        self.catalog_entries.append(Offer(
            offer_id="9E05107B537941859339D708DEF82679",
            dev_name="SecretShop.Page02.Misc.09",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Currency:Gold', 'regularPrice': 50000,
                     'dynamicRegularPrice': -1, 'finalPrice': 50000, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 50000}],
            daily_limit=1,
            item_grants=[{'templateId': 'Reagent:Reagent_RXT_Parts_Small', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="B0BD3890216C42D28285B77FC750051F",
            dev_name="SecretShop.Page02.UnderworldTrader.01",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 10, 'dynamicRegularPrice': -1,
                 'finalPrice': 7, 'saleType': 'AmountOff', 'saleExpiration': '9999-12-31T23:59:59.999Z',
                 'basePrice': 7}],
            daily_limit=20,
            meta_info=[{'key': 'VipLevelMin', 'value': '3'}],
            item_grants=[{'templateId': 'Ore:Ore_Magicite', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="34F46030F78C47ED939B794A7A3777A9",
            dev_name="SecretShop.Page02.Elixir.01",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Currency:Gold', 'regularPrice': 50000,
                     'dynamicRegularPrice': -1, 'finalPrice': 42500, 'saleType': 'AmountOff',
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 42500}],
            daily_limit=5,
            item_grants=[{'templateId': 'UpgradePotion:UpgradeHealthMajor', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="A50A59860E2F475CB46C776EA16A9250",
            dev_name="SecretShop.Page02.Reagent.08",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Currency:Gold', 'regularPrice': 300000,
                     'dynamicRegularPrice': -1, 'finalPrice': 255000, 'saleType': 'AmountOff',
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 255000}],
            daily_limit=1,
            item_grants=[{'templateId': 'Reagent:Reagent_Shard_Light', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="F44CCE1A5D0D4EA4A5183146552A2433",
            dev_name="SecretShop.Page02.Free.06",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Currency:Gold', 'regularPrice': 10000,
                     'dynamicRegularPrice': -1, 'finalPrice': 0, 'saleType': 'AmountOff',
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=2,
            item_grants=[{'templateId': 'Currency:Hammer', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="0C0DAF0C60974015A4D5632A8169254E",
            dev_name="SecretShop.Page02.Reagent.18",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 200, 'dynamicRegularPrice': -1,
                 'finalPrice': 170, 'saleType': 'AmountOff', 'saleExpiration': '9999-12-31T23:59:59.999Z',
                 'basePrice': 170}],
            daily_limit=1,
            item_grants=[{'templateId': 'Reagent:Reagent_Shard_Water', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="8F81793505DF49D6B3372C7FDC08DB66",
            dev_name="SecretShop.Page02.Reagent.21",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 200, 'dynamicRegularPrice': -1,
                 'finalPrice': 170, 'saleType': 'AmountOff', 'saleExpiration': '9999-12-31T23:59:59.999Z',
                 'basePrice': 170}],
            daily_limit=1,
            item_grants=[{'templateId': 'Reagent:Reagent_Shard_Fire', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="8B8FE8A9518C49099287DD050EE9060C",
            dev_name="SecretShop.Page02.Ore.01",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Currency:Gold', 'regularPrice': 25000,
                     'dynamicRegularPrice': -1, 'finalPrice': 21250, 'saleType': 'AmountOff',
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 21250}],
            daily_limit=3,
            item_grants=[{'templateId': 'Ore:Ore_Magicite', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="7DAA2A52A3E4458198BB70269DF55209",
            dev_name="SecretShop.Page02.UnderworldTrader.09",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 200, 'dynamicRegularPrice': -1,
                 'finalPrice': 200, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 200}],
            daily_limit=1,
            meta_info=[{'key': 'VipLevelMin', 'value': '3'}],
            item_grants=[{'templateId': 'Reagent:Reagent_HeroMap_Elemental', 'quantity': 100}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="48EB602356C048F3A9A19EF018EB9BF0",
            dev_name="SecretShop.Page02.TreasureMap.10",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 400, 'dynamicRegularPrice': -1,
                 'finalPrice': 400, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 400}],
            daily_limit=1,
            item_grants=[{'templateId': 'TreasureMap:TM_Special_UnderwaterTunnel', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="E535BC0CBAE84684B91234566ECF74FA",
            dev_name="SecretShop.Page02.UnderworldTrader.27",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 400, 'dynamicRegularPrice': -1,
                 'finalPrice': 280, 'saleType': 'AmountOff', 'saleExpiration': '9999-12-31T23:59:59.999Z',
                 'basePrice': 280}],
            daily_limit=1,
            meta_info=[{'key': 'VipLevelMin', 'value': '3'}],
            item_grants=[{'templateId': 'TreasureMap:TM_Special_PlanetCore', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="8E4C9A53F13E40B78E0FDA5CC6D1B2D2",
            dev_name="SecretShop.Page02.Misc.07",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 5, 'dynamicRegularPrice': -1,
                     'finalPrice': 5, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 5}],
            daily_limit=5,
            item_grants=[{'templateId': 'Currency:Hammer', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="CFC5DEA6DBEA480D9D7A2DCDB35AA3FB",
            dev_name="SecretShop.Page02.UnderworldTraderGold.03",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Currency:Gold', 'regularPrice': 4000,
                     'dynamicRegularPrice': -1, 'finalPrice': 2800, 'saleType': 'AmountOff',
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 2800}],
            daily_limit=15,
            meta_info=[{'key': 'VipLevelMin', 'value': '3'}],
            item_grants=[{'templateId': 'UpgradePotion:UpgradeHealthMinor', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="F98D0C2D7D584714B96F13E2801E659E",
            dev_name="SecretShop.Page02.Reagent.23",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 200, 'dynamicRegularPrice': -1,
                 'finalPrice': 170, 'saleType': 'AmountOff', 'saleExpiration': '9999-12-31T23:59:59.999Z',
                 'basePrice': 170}],
            daily_limit=1,
            item_grants=[{'templateId': 'Reagent:Reagent_Shard_Light', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="8EFF230AFB9D4273B9076596BCE005C3",
            dev_name="SecretShop.Page02.Elixir.02",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Currency:Gold', 'regularPrice': 4000,
                     'dynamicRegularPrice': -1, 'finalPrice': 3400, 'saleType': 'AmountOff',
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 3400}],
            daily_limit=15,
            item_grants=[{'templateId': 'UpgradePotion:UpgradeHealthMinor', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="8B6AC0B2A35D44D39D08DF9DF22268CE",
            dev_name="SecretShop.Page02.Elixir.05",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Currency:Gold', 'regularPrice': 4000,
                     'dynamicRegularPrice': -1, 'finalPrice': 3400, 'saleType': 'AmountOff',
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 3400}],
            daily_limit=15,
            item_grants=[{'templateId': 'UpgradePotion:UpgradeStrengthMinor', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="E7CF296997F54E3EAD7E6EEFD67BAD22",
            dev_name="SecretShop.Page02.Shard.10",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 200, 'dynamicRegularPrice': -1,
                 'finalPrice': 170, 'saleType': 'AmountOff', 'saleExpiration': '9999-12-31T23:59:59.999Z',
                 'basePrice': 170}],
            daily_limit=1,
            item_grants=[{'templateId': 'Reagent:Reagent_Shard_Water', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="C9963A8B16474B64A99EB9108AF3C1EE",
            dev_name="SecretShop.Page02.CharShard.03",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Currency:Gold', 'regularPrice': 4000000,
                     'dynamicRegularPrice': -1, 'finalPrice': 4000000, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 4000000}],
            daily_limit=1,
            item_grants=[{'templateId': 'Reagent:Reagent_Misc_CeremonialShield', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="DDCEB10173F8441B99603CED9EEBCB6E",
            dev_name="SecretShop.Page02.UnderworldTrader.19",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 1, 'dynamicRegularPrice': -1,
                     'finalPrice': 1, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 1}],
            daily_limit=40,
            meta_info=[{'key': 'VipLevelMin', 'value': '3'}],
            item_grants=[{'templateId': 'Reagent:Reagent_Shared_T02', 'quantity': 1}],
        ))

    @classmethod
    async def init_storefront(cls) -> Self:
        """
        Initialise the SecretShopPage2 storefront
        :return: The initialised SecretShopPage2 storefront class
        """
        self: SecretShopPage2 = cls()
        self.name = "SecretShopPage2"
        self.catalog_entries = []
        return self


class WeeklyChallenge(Storefront):
    """
    Class based system to handle the WeeklyChallenge storefront for the storefront catalog service
    """

    def __init__(self) -> None:
        """
        Initialise the WeeklyChallenge storefront class.
        This will setup the variables for the WeeklyChallenge storefront
        """
        super().__init__()

    async def update_storefront(self) -> None:
        """
        Update the storefront for the WeeklyChallenge storefront class with the latest data
        This rotation never changed
        :return: None
        """
        # temporary implementation
        self.catalog_entries.append(Offer(
            offer_id="9D1888E891BD43AB9DA003D288880200",
            dev_name="WeeklyChallenge.WCStore.12",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:WCCoins', 'regularPrice': 5,
                     'dynamicRegularPrice': -1, 'finalPrice': 5, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 5}],
            weekly_limit=5,
            sort_priority=99,
            item_grants=[{'templateId': 'Reagent:Reagent_WC_Hero_TripleCombo', 'quantity': 4}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="373A66DDC30E4CDE8E9554C596654D41",
            dev_name="WeeklyChallenge.WCStore.10",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:WCCoins', 'regularPrice': 40,
                     'dynamicRegularPrice': -1, 'finalPrice': 40, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 40}],
            weekly_limit=3,
            sort_priority=40,
            item_grants=[{'templateId': 'Reagent:Reagent_HeroMap_Elemental', 'quantity': 100}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="0E116A56E39E435799ED39B090E21676",
            dev_name="WeeklyChallenge.WCStore.13",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:WCCoins', 'regularPrice': 5,
                     'dynamicRegularPrice': -1, 'finalPrice': 5, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 5}],
            weekly_limit=12,
            sort_priority=100,
            item_grants=[{'templateId': 'Token:TK_Voucher_HeroBattle', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="C4C98274DEB14C21B56C5D3C13CEEC0C",
            dev_name="WeeklyChallenge.WCStore.04",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:WCCoins', 'regularPrice': 5,
                     'dynamicRegularPrice': -1, 'finalPrice': 5, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 5}],
            weekly_limit=5,
            sort_priority=10,
            item_grants=[{'templateId': 'Reagent:Reagent_Shard_Nature', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="58A2382E60FF4D3991084DF21FA1483B",
            dev_name="WeeklyChallenge.WCStore.02",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:WCCoins', 'regularPrice': 5,
                     'dynamicRegularPrice': -1, 'finalPrice': 2, 'saleType': 'AmountOff',
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 2}],
            weekly_limit=20,
            sort_priority=75,
            item_grants=[{'templateId': 'Currency:SkillXP', 'quantity': 100}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="F8489AEE810640B9A35538FA4F09C70D",
            dev_name="WeeklyChallenge.WCStore.09",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:WCCoins', 'regularPrice': 5,
                     'dynamicRegularPrice': -1, 'finalPrice': 5, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 5}],
            weekly_limit=15,
            sort_priority=50,
            item_grants=[{'templateId': 'Ore:Ore_Magicite', 'quantity': 10}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="398723C11EFD41B3A0BDC06CF004DFFD",
            dev_name="WeeklyChallenge.WCStore.05",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:WCCoins', 'regularPrice': 5,
                     'dynamicRegularPrice': -1, 'finalPrice': 5, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 5}],
            weekly_limit=5,
            sort_priority=10,
            item_grants=[{'templateId': 'Reagent:Reagent_Shard_Water', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="10DA3DE368464C318176A75C2C3E7E93",
            dev_name="WeeklyChallenge.WCStore.08",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:WCCoins', 'regularPrice': 50,
                     'dynamicRegularPrice': -1, 'finalPrice': 50, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 50}],
            weekly_limit=1,
            sort_priority=101,
            item_grants=[{'templateId': 'Currency:MtxGiveaway', 'quantity': 200}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="87ED883B16D642DD9BA19ACE31FC3948",
            dev_name="WeeklyChallenge.WCStore.07",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:WCCoins', 'regularPrice': 5,
                     'dynamicRegularPrice': -1, 'finalPrice': 5, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 5}],
            weekly_limit=5,
            sort_priority=10,
            item_grants=[{'templateId': 'Reagent:Reagent_Shard_Dark', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="47296335F3D34052AED9B0B767C23687",
            dev_name="WeeklyChallenge.WCStore.03",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:WCCoins', 'regularPrice': 5,
                     'dynamicRegularPrice': -1, 'finalPrice': 5, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 5}],
            weekly_limit=5,
            sort_priority=10,
            item_grants=[{'templateId': 'Reagent:Reagent_Shard_Fire', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="4E70CCEAF17741D7ABFF418EE6CBEFE9",
            dev_name="WeeklyChallenge.WCStore.06",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:WCCoins', 'regularPrice': 5,
                     'dynamicRegularPrice': -1, 'finalPrice': 5, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 5}],
            weekly_limit=5,
            sort_priority=10,
            item_grants=[{'templateId': 'Reagent:Reagent_Shard_Light', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="F574035687484FD8BFEE2D967605F9E3",
            dev_name="WeeklyChallenge.WCStore.01",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:WCCoins', 'regularPrice': 1,
                     'dynamicRegularPrice': -1, 'finalPrice': 1, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 1}],
            weekly_limit=100,
            sort_priority=75,
            item_grants=[{'templateId': 'Reagent:Reagent_Shared_T02', 'quantity': 5}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="5AB9FCAC16A84AA8B48196DEF5B939D8",
            dev_name="WeeklyChallenge.WCStore.11",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:WCCoins', 'regularPrice': 5,
                     'dynamicRegularPrice': -1, 'finalPrice': 5, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 5}],
            weekly_limit=10,
            sort_priority=60,
            item_grants=[{'templateId': 'Reagent:Reagent_Misc_CeremonialSword', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="45EC4E0C917949938D50E24F19870EB9",
            dev_name="WeeklyChallenge.WCStore.14",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:WCCoins', 'regularPrice': 20,
                     'dynamicRegularPrice': -1, 'finalPrice': 20, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 20}],
            weekly_limit=1,
            requirements=[{'requirementType': 'DenyOnFulfillment', 'requiredId': '48268FEC4038F934733109AFAE874A71',
                           'minQuantity': 1}],
            sort_priority=41,
            display_asset_path="/Game/Characters/Classes/Assassin/Multi_Slasher/CD_Assassin_R2_Nature_Slasher_T03"
                               ".CD_Assassin_R2_Nature_Slasher_T03",
            item_grants=[{'templateId': 'Character:Assassin_R2_Nature_Slasher_T03', 'quantity': 1}],
        ))

    @classmethod
    async def init_storefront(cls) -> Self:
        """
        Initialise the WeeklyChallenge storefront
        :return: The initialised WeeklyChallenge storefront class
        """
        self: WeeklyChallenge = cls()
        self.name = "WeeklyChallenge"
        self.catalog_entries = []
        return self


class HeroStore(Storefront):
    """
    Class based system to handle the HeroStore storefront for the storefront catalog service
    """

    def __init__(self) -> None:
        """
        Initialise the HeroStore storefront class.
        This will setup the variables for the HeroStore storefront
        """
        super().__init__()

    async def update_storefront(self) -> None:
        """
        Update the storefront for the HeroStore storefront class with the latest data
        :return: None
        """
        # temporary implementation
        self.catalog_entries.append(Offer(
            offer_id="virtual:/1i158746eh4k7p47okhaog3c91[0]1#0",
            dev_name="[VIRTUAL]1 x Night Hunter Lana for 2000 GameItem : Reagent:Reagent_Hero_Event",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Hero_Event', 'regularPrice': 2000,
                     'dynamicRegularPrice': 2000, 'finalPrice': 2000, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 2000}],
            monthly_limit=2,
            app_store_id=[
            ],
            meta_info=[{'key': 'bIsNewHero', 'value': 'FALSE'}, {'key': 'bIsSpecialHero', 'value': 'FALSE'}],
            sort_priority=120,
            item_grants=[{'templateId': 'Character:Blademaster_VR2_Water_SilverWhip_T04', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="virtual:/1i158746eh4k7p47okhaog3c91[0]1#1",
            dev_name="[VIRTUAL]1 x Arte Plein for 100 GameItem : Reagent:Reagent_SupplyPoints_Elite",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_SupplyPoints_Elite',
                     'regularPrice': 100, 'dynamicRegularPrice': 100, 'finalPrice': 100,
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 100}],
            monthly_limit=2,
            app_store_id=[
            ],
            meta_info=[{'key': 'bIsNewHero', 'value': 'FALSE'}, {'key': 'bIsSpecialHero', 'value': 'FALSE'}],
            sort_priority=20,
            item_grants=[{'templateId': 'Character:Pet_VR2_FlyByNight_Light_T04', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="FC9F55324B665622C6E85D987C5DE358",
            dev_name="Fire Cloudpuff 2",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_SupplyPoints_Elite',
                     'regularPrice': 800, 'dynamicRegularPrice': -1, 'finalPrice': 800,
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 800}],
            daily_limit=1,
            requirements=[{'requirementType': 'DenyOnFulfillment', 'requiredId': 'F15984F442336A13D30447B2C57DD7AA',
                           'minQuantity': 2},
                          {'requirementType': 'RequireFulfillment', 'requiredId': 'E3069A27428C5C1D05892DA6244406B4',
                           'minQuantity': 2}],
            meta_info=[{'key': 'AccountLevelMin', 'value': '200'}],
            sort_priority=31,
            item_grants=[{'templateId': 'Character:Pet_SR1_Cloudpuff_Fire_T05', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="virtual:/00ig9fpo66b4605vafo7jvidec[0]191#12",
            dev_name="[VIRTUAL]1 x Flame the Raccoon for -1 GameItem : Reagent:Reagent_SupplyPoints_Elite",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_SupplyPoints_Elite',
                     'regularPrice': 100, 'dynamicRegularPrice': 100, 'finalPrice': 100, 'saleType': 'Strikethrough',
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 100}],
            monthly_limit=2,
            app_store_id=[
            ],
            sort_priority=30,
            item_grants=[{'templateId': 'Character:Pet_SR1_Fire_InfernoRacoon_T05', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="virtual:/00ig9fpo66b4605vafo7jvidec[0]191#13",
            dev_name="[VIRTUAL]1 x Painguin for -1 GameItem : Reagent:Reagent_SupplyPoints_Elite",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_SupplyPoints_Elite',
                     'regularPrice': 50, 'dynamicRegularPrice': 50, 'finalPrice': 50, 'saleType': 'Strikethrough',
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 50}],
            monthly_limit=2,
            app_store_id=[
            ],
            sort_priority=20,
            item_grants=[{'templateId': 'Character:Pet_UC1_Painguin_Water_T03', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="virtual:/00ig9fpo66b4605vafo7jvidec[0]191#10",
            dev_name="[VIRTUAL]1 x Commander Shorty for -1 GameItem : Reagent:Reagent_SupplyPoints_Elite",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_SupplyPoints_Elite',
                     'regularPrice': 100, 'dynamicRegularPrice': 100, 'finalPrice': 100, 'saleType': 'Strikethrough',
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 100}],
            monthly_limit=2,
            app_store_id=[
            ],
            sort_priority=30,
            item_grants=[{'templateId': 'Character:Pet_SR2_Fire_Corgi_T05', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="virtual:/00ig9fpo66b4605vafo7jvidec[0]191#11",
            dev_name="[VIRTUAL]1 x Rain Deer for -1 GameItem : Reagent:Reagent_SupplyPoints_Elite",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_SupplyPoints_Elite',
                     'regularPrice': 100, 'dynamicRegularPrice': 100, 'finalPrice': 100, 'saleType': 'Strikethrough',
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 100}],
            monthly_limit=2,
            app_store_id=[
            ],
            sort_priority=30,
            item_grants=[{'templateId': 'Character:Pet_VR2_Reindeer_Water_T04', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="virtual:/00ig9fpo66b4605vafo7jvidec[0]191#0",
            dev_name="[VIRTUAL]1 x Kurohomura for -1 GameItem : Reagent:Reagent_Hero_Event",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Hero_Event', 'regularPrice': 5000,
                     'dynamicRegularPrice': 5000, 'finalPrice': 5000, 'saleType': 'Strikethrough',
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 5000}],
            monthly_limit=2,
            app_store_id=[
            ],
            sort_priority=120,
            item_grants=[{'templateId': 'Character:MartialArtist_SR2_Fire_SeveringBlow_T05', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="90106DE84F9DD0698624BDA0B515F7B6",
            dev_name="Dark Cloudpuff 1",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_SupplyPoints_Elite',
                     'regularPrice': 800, 'dynamicRegularPrice': -1, 'finalPrice': 800,
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 800}],
            daily_limit=1,
            requirements=[{'requirementType': 'DenyOnFulfillment', 'requiredId': 'BD6B06874A8AEA8FD6EF89A3F43F489F',
                           'minQuantity': 1},
                          {'requirementType': 'RequireFulfillment', 'requiredId': 'C4A82E024E03977BE786D09365878807',
                           'minQuantity': 1}],
            meta_info=[{'key': 'AccountLevelMin', 'value': '200'}],
            sort_priority=31,
            item_grants=[{'templateId': 'Character:Pet_SR1_Cloudpuff_Dark_T05', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="virtual:/00ig9fpo66b4605vafo7jvidec[0]191#3",
            dev_name="[VIRTUAL]1 x Noble Ward Mirra for -1 GameItem : Reagent:Reagent_Hero_Event",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Hero_Event', 'regularPrice': 2000,
                     'dynamicRegularPrice': 2000, 'finalPrice': 2000, 'saleType': 'Strikethrough',
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 2000}],
            monthly_limit=2,
            app_store_id=[
            ],
            sort_priority=110,
            item_grants=[{'templateId': 'Character:Warrior_VR1_Light_Deflect_T04', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="virtual:/00ig9fpo66b4605vafo7jvidec[0]191#4",
            dev_name="[VIRTUAL]1 x Beastman Champion for -1 GameItem : Reagent:Reagent_Hero_Event",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Hero_Event', 'regularPrice': 2000,
                     'dynamicRegularPrice': 2000, 'finalPrice': 2000, 'saleType': 'Strikethrough',
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 2000}],
            monthly_limit=2,
            app_store_id=[
            ],
            sort_priority=110,
            item_grants=[{'templateId': 'Character:Warrior_VR2_Dark_Rampage_T04', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="virtual:/00ig9fpo66b4605vafo7jvidec[0]191#1",
            dev_name="[VIRTUAL]1 x Kumiho the Fox for -1 GameItem : Reagent:Reagent_Hero_Event",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Hero_Event', 'regularPrice': 2000,
                     'dynamicRegularPrice': 2000, 'finalPrice': 2000, 'saleType': 'Strikethrough',
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 2000}],
            monthly_limit=2,
            app_store_id=[
            ],
            sort_priority=110,
            item_grants=[{'templateId': 'Character:Assassin_VR1_Fire_HiddenStrike_T04', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="E02009F74D1498D74D16B3B8B5E0D21C",
            dev_name="Nature Cloudpuff 1",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_SupplyPoints_Elite',
                     'regularPrice': 800, 'dynamicRegularPrice': -1, 'finalPrice': 800,
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 800}],
            daily_limit=1,
            requirements=[{'requirementType': 'DenyOnFulfillment', 'requiredId': '8772B1374685F66D9F9B54A0A3C026B5',
                           'minQuantity': 1}],
            sort_priority=31,
            item_grants=[{'templateId': 'Character:Pet_SR1_Cloudpuff_Nature_T05', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="virtual:/00ig9fpo66b4605vafo7jvidec[0]191#2",
            dev_name="[VIRTUAL]1 x Jarellia the Feral for -1 GameItem : Reagent:Reagent_Hero_Event",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Hero_Event', 'regularPrice': 2000,
                     'dynamicRegularPrice': 2000, 'finalPrice': 2000, 'saleType': 'Strikethrough',
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 2000}],
            monthly_limit=2,
            app_store_id=[
            ],
            sort_priority=110,
            item_grants=[{'templateId': 'Character:Cleric_VR2_Nature_FeralStrike_T04', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="virtual:/00ig9fpo66b4605vafo7jvidec[0]191#7",
            dev_name="[VIRTUAL]1 x Heavenguard Kaleb for -1 GameItem : Reagent:Reagent_Hero_Event",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Hero_Event', 'regularPrice': 800,
                     'dynamicRegularPrice': 800, 'finalPrice': 800, 'saleType': 'Strikethrough',
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 800}],
            monthly_limit=2,
            app_store_id=[
            ],
            sort_priority=100,
            item_grants=[{'templateId': 'Character:HolyKnight_R1_Light_Resurrect_T03', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="virtual:/00ig9fpo66b4605vafo7jvidec[0]191#8",
            dev_name="[VIRTUAL]1 x Mechshade Dagen for -1 GameItem : Reagent:Reagent_Hero_Event",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Hero_Event', 'regularPrice': 800,
                     'dynamicRegularPrice': 800, 'finalPrice': 800, 'saleType': 'Strikethrough',
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 800}],
            monthly_limit=2,
            app_store_id=[
            ],
            sort_priority=100,
            item_grants=[{'templateId': 'Character:Ninja_UC1_Fire_SwiftStrike_T03', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="BFF081A44C9D7D7EDA18269F1ACC2CFD",
            dev_name="Dark Cloudpuff 2",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_SupplyPoints_Elite',
                     'regularPrice': 800, 'dynamicRegularPrice': -1, 'finalPrice': 800,
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 800}],
            daily_limit=1,
            requirements=[{'requirementType': 'DenyOnFulfillment', 'requiredId': 'BD6B06874A8AEA8FD6EF89A3F43F489F',
                           'minQuantity': 2},
                          {'requirementType': 'RequireFulfillment', 'requiredId': 'C4A82E024E03977BE786D09365878807',
                           'minQuantity': 2}],
            meta_info=[{'key': 'AccountLevelMin', 'value': '200'}],
            sort_priority=31,
            item_grants=[{'templateId': 'Character:Pet_SR1_Cloudpuff_Dark_T05', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="virtual:/00ig9fpo66b4605vafo7jvidec[0]191#5",
            dev_name="[VIRTUAL]1 x Ejo The Messenger for -1 GameItem : Reagent:Reagent_Hero_Event",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Hero_Event', 'regularPrice': 2000,
                     'dynamicRegularPrice': 2000, 'finalPrice': 2000, 'saleType': 'Strikethrough',
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 2000}],
            monthly_limit=2,
            app_store_id=[
            ],
            sort_priority=110,
            item_grants=[{'templateId': 'Character:SpiritWarrior_VR2_Light_KindFist_T04', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="virtual:/00ig9fpo66b4605vafo7jvidec[0]191#6",
            dev_name="[VIRTUAL]1 x Kunoichi Melina for -1 GameItem : Reagent:Reagent_Hero_Event",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Hero_Event', 'regularPrice': 800,
                     'dynamicRegularPrice': 800, 'finalPrice': 800, 'saleType': 'Strikethrough',
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 800}],
            monthly_limit=2,
            app_store_id=[
            ],
            sort_priority=100,
            item_grants=[{'templateId': 'Character:Ninja_R2_Water_TripleStab_T03', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="F74CDC054D2A0F40EC89B6915936EF8E",
            dev_name="Fire Cloudpuff 1",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_SupplyPoints_Elite',
                     'regularPrice': 800, 'dynamicRegularPrice': -1, 'finalPrice': 800,
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 800}],
            daily_limit=1,
            requirements=[{'requirementType': 'DenyOnFulfillment', 'requiredId': 'F15984F442336A13D30447B2C57DD7AA',
                           'minQuantity': 1},
                          {'requirementType': 'RequireFulfillment', 'requiredId': 'E3069A27428C5C1D05892DA6244406B4',
                           'minQuantity': 1}],
            meta_info=[{'key': 'AccountLevelMin', 'value': '100'}],
            sort_priority=31,
            item_grants=[{'templateId': 'Character:Pet_SR1_Cloudpuff_Fire_T05', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="virtual:/00ig9fpo66b4605vafo7jvidec[0]191#9",
            dev_name="[VIRTUAL]1 x Ancient Pact Palgrus for -1 GameItem : Reagent:Reagent_SupplyPoints_Elite",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_SupplyPoints_Elite',
                     'regularPrice': 200, 'dynamicRegularPrice': 200, 'finalPrice': 200, 'saleType': 'Strikethrough',
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 200}],
            monthly_limit=2,
            app_store_id=[
            ],
            sort_priority=40,
            item_grants=[{'templateId': 'Character:Pet_SR1_Palgrus_Light_T05', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="839D87504767FFC769757B978FE78604",
            dev_name="Nature Cloudpuff 2",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_SupplyPoints_Elite',
                     'regularPrice': 800, 'dynamicRegularPrice': -1, 'finalPrice': 800,
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 800}],
            daily_limit=1,
            requirements=[{'requirementType': 'DenyOnFulfillment', 'requiredId': '8772B1374685F66D9F9B54A0A3C026B5',
                           'minQuantity': 2},
                          {'requirementType': 'RequireFulfillment', 'requiredId': 'BD6B06874A8AEA8FD6EF89A3F43F489F',
                           'minQuantity': 1}],
            meta_info=[{'key': 'AccountLevelMin', 'value': '200'}],
            sort_priority=31,
            item_grants=[{'templateId': 'Character:Pet_SR1_Cloudpuff_Nature_T05', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="3CC5B90E4322D33C641808A14CF2A6CE",
            dev_name="Light Cloudpuff 1",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_SupplyPoints_Elite',
                     'regularPrice': 800, 'dynamicRegularPrice': -1, 'finalPrice': 800,
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 800}],
            daily_limit=1,
            requirements=[{'requirementType': 'DenyOnFulfillment', 'requiredId': 'E3069A27428C5C1D05892DA6244406B4',
                           'minQuantity': 1},
                          {'requirementType': 'RequireFulfillment', 'requiredId': '8772B1374685F66D9F9B54A0A3C026B5',
                           'minQuantity': 1}],
            meta_info=[{'key': 'AccountLevelMin', 'value': '50'}],
            sort_priority=31,
            item_grants=[{'templateId': 'Character:Pet_SR1_Cloudpuff_Light_T05', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="C1C466504D2FE8078ACBD99E3C086AED",
            dev_name="Water Cloudpuff 2",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_SupplyPoints_Elite',
                     'regularPrice': 800, 'dynamicRegularPrice': -1, 'finalPrice': 800,
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 800}],
            daily_limit=1,
            requirements=[{'requirementType': 'DenyOnFulfillment', 'requiredId': 'C4A82E024E03977BE786D09365878807',
                           'minQuantity': 2},
                          {'requirementType': 'RequireFulfillment', 'requiredId': 'F15984F442336A13D30447B2C57DD7AA',
                           'minQuantity': 2}],
            meta_info=[{'key': 'AccountLevelMin', 'value': '200'}],
            sort_priority=31,
            item_grants=[{'templateId': 'Character:Pet_SR1_Cloudpuff_Water_T05', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="77BE70724F1603F9475694ADCA777E6A",
            dev_name="Water Cloudpuff 1",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_SupplyPoints_Elite',
                     'regularPrice': 800, 'dynamicRegularPrice': -1, 'finalPrice': 800,
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 800}],
            daily_limit=1,
            requirements=[{'requirementType': 'DenyOnFulfillment', 'requiredId': 'C4A82E024E03977BE786D09365878807',
                           'minQuantity': 1},
                          {'requirementType': 'RequireFulfillment', 'requiredId': 'F15984F442336A13D30447B2C57DD7AA',
                           'minQuantity': 1}],
            meta_info=[{'key': 'AccountLevelMin', 'value': '150'}],
            sort_priority=31,
            item_grants=[{'templateId': 'Character:Pet_SR1_Cloudpuff_Water_T05', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="93CD385542C69DD7E6760D9D7E726CFA",
            dev_name="Light Cloudpuff 2",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_SupplyPoints_Elite',
                     'regularPrice': 800, 'dynamicRegularPrice': -1, 'finalPrice': 800,
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 800}],
            daily_limit=1,
            requirements=[{'requirementType': 'DenyOnFulfillment', 'requiredId': 'E3069A27428C5C1D05892DA6244406B4',
                           'minQuantity': 2},
                          {'requirementType': 'RequireFulfillment', 'requiredId': '8772B1374685F66D9F9B54A0A3C026B5',
                           'minQuantity': 2}],
            meta_info=[{'key': 'AccountLevelMin', 'value': '200'}],
            sort_priority=31,
            item_grants=[{'templateId': 'Character:Pet_SR1_Cloudpuff_Light_T05', 'quantity': 1}],
        ))

    @classmethod
    async def init_storefront(cls) -> Self:
        """
        Initialise the HeroStore storefront
        :return: The initialised HeroStore storefront class
        """
        self: HeroStore = cls()
        self.name = "HeroStore"
        self.catalog_entries = []
        return self


class Featured(Storefront):
    """
    Class based system to handle the Featured storefront for the storefront catalog service
    """

    def __init__(self) -> None:
        """
        Initialise the Featured storefront class.
        This will setup the variables for the Featured storefront
        """
        super().__init__()

    async def update_storefront(self) -> None:
        """
        Update the storefront for the Featured storefront class with the latest data
        :return: None
        """
        self.catalog_entries.append(Offer(
            offer_id="0DC7697ABCD7416C9C082C91BC0959A3",
            dev_name="StorefrontStacked.Page01.ElementalHeroes.58",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 500, 'dynamicRegularPrice': -1,
                 'finalPrice': 500, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 500}],
            daily_limit=1,
            meta_info=[{'key': 'ButtonClassPath',
                        'value': "WidgetBlueprint'/Game/UMG/Store/B_StoreButton_Bundles.B_StoreButton_Bundles'"},
                       {'key': 'Type', 'value': 'ElementalHero'}, {'key': 'HideQuantityRemaining', 'value': 'True'}],
            catalog_group="ElementalHeroes",
            catalog_group_priority=58,
            sort_priority=72,
            title="Elemental Heroes",
            item_grants=[{'templateId': 'Reagent:Reagent_Hero_Event', 'quantity': 500},
                         {'templateId': 'Reagent:Reagent_HeroMap_Elemental', 'quantity': 140},
                         {'templateId': 'Currency:Hammer', 'quantity': 4},
                         {'templateId': 'Reagent:Reagent_Shard_Nature', 'quantity': 3},
                         {'templateId': 'Reagent:Reagent_Foil', 'quantity': 15},
                         {'templateId': 'UpgradePotion:UpgradeStrengthMinor', 'quantity': 5},
                         {'templateId': 'Reagent:Reagent_Hero_Event', 'quantity': 100}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="308A41F23E4A4AC79AD9C9ADEF517D0A",
            dev_name="StorefrontMtx.L370000.MtxGift.36",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '44BB81AA4D528D13F5B64F857A30D41A',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': 'CD425F9A4614451770592D976A9CB72A',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '370000'}],
            sort_priority=1000,
            title="Support Gift 48",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="BE0A976B8D4A43DF83B18EEC0C5D6888",
            dev_name="StorefrontMtx.L440000.MtxGift.44",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '621ED4A24CF22364662C8B86D5681DBB',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '15B714264A35B80083536D821A2C9203',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '440000'}],
            sort_priority=1000,
            title="Support Gift 55",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="4EF045C2E40C4E228D0BA34B69520227",
            dev_name="StorefrontMtx.L980000.MtxGift.110",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': 'FB4E32F849408CFC50038494DF0B371C',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '8F30DCC84E3D5ACB54275796E2D75E5B',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '980000'}],
            sort_priority=1000,
            title="Support Gift 109",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="0E4C27E5A11F4C00BD402FCBEC94DB96",
            dev_name="StorefrontMtx.L950000.MtxGift.107",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '4C16D22849A940EFD2805FA3770F4289',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '9D90D9D043CA0596F6266EB2C3DC9C64',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '950000'}],
            sort_priority=1000,
            title="Support Gift 106",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="C23FF150D2AF4E2CABE0BC052E8FAFF0",
            dev_name="StorefrontLevel.L550000.LevelUpChest.27",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 5000, 'dynamicRegularPrice': -1,
                 'finalPrice': 5000, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 5000}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '92077EB243071AD9F0E7A2B5F2F71D7F',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '8A2CF2B442B4177565F52196364A120F',
                           'minQuantity': 1}],
            meta_info=[{'key': 'ButtonClassPath',
                        'value': "WidgetBlueprint'/Game/UMG/Store/B_StoreButton_Bundles.B_StoreButton_Bundles'"},
                       {'key': 'StoreLevelMin', 'value': '550000'}],
            sort_priority=60,
            title="Super Magic Chest",
            description="A Diamond Hero Crystal, 5000 Magic Tickets and 8 items!",
            item_grants=[{'templateId': 'Reagent:Reagent_Hero_Event', 'quantity': 5000},
                         {'templateId': 'Reagent:Reagent_HeroMap_SuperRare', 'quantity': 100},
                         {'templateId': 'Reagent:Reagent_HeroMap_Elemental', 'quantity': 500},
                         {'templateId': 'Reagent:Reagent_SupplyPoints_Elite', 'quantity': 200},
                         {'templateId': 'UpgradePotion:UpgradeHealthMajor', 'quantity': 50},
                         {'templateId': 'UpgradePotion:UpgradeStrengthMajor', 'quantity': 50},
                         {'templateId': 'UpgradePotion:UpgradeMana', 'quantity': 10}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="FA23253B9D024B658F57FF2CA2548EA1",
            dev_name="StorefrontMtx.L60000.MtxGift.64",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': 'E83060694EC9CA80654B84AF64340D5D',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '014262EC477B66DE83109CA381FED5AD',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '60000'}],
            sort_priority=1000,
            title="Support Gift 13",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="BC59DAB14818A2910F892BBBEB77772F",
            dev_name="Kailani (Light)",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Voucher:Voucher_Hero_Blademaster_Light_Bladestorm',
                     'regularPrice': 1, 'dynamicRegularPrice': -1, 'finalPrice': 1,
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 1}],
            meta_info=[{'key': 'AffordOnly', 'value': 'true'}, {'key': 'ButtonClassPath',
                                                                'value': "WidgetBlueprint'/Game/UMG/Store"
                                                                         "/B_StoreButton_Hero.B_StoreButton_Hero'"},
                       {'key': 'type', 'value': 'Random'}, {'key': 'AutoRedeem', 'value': 'true'}],
            sort_priority=9999,
            title="Kailani",
            description="Free Kailani from her crystal!",
            item_grants=[{'templateId': 'Character:Blademaster_VR1_Light_BladeStorm_T04', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="DA4FAC9829FD4E3197E2E46E33EADBF7",
            dev_name="StorefrontMtx.L5000.MtxGift.51",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '0C425A7840E80B644949B2AD5291BD98',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '1E024004419DCE5D80EBC9B0A07D5957',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '5000'}],
            sort_priority=1000,
            title="Support Gift 2",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="AEDFBC344E6D551E9F25728FFD343012",
            dev_name="Elemental Hero Resources",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 500, 'dynamicRegularPrice': -1,
                 'finalPrice': 500, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 500}],
            meta_info=[{'key': 'ButtonClassPath',
                        'value': "WidgetBlueprint'/Game/UMG/Store/B_StoreButton_Bundles.B_StoreButton_Bundles'"},
                       {'key': 'type', 'value': 'ElementalHero'}],
            catalog_group="ElementalHeroes",
            sort_priority=72,
            title="Elemental Heroes",
            item_grants=[{'templateId': 'Reagent:Reagent_Hero_Event', 'quantity': 500},
                         {'templateId': 'Reagent:Reagent_HeroMap_Elemental', 'quantity': 140},
                         {'templateId': 'Currency:Hammer', 'quantity': 4},
                         {'templateId': 'Reagent:Reagent_Misc_CeremonialSword', 'quantity': 2},
                         {'templateId': 'Currency:Gold', 'quantity': 100000},
                         {'templateId': 'TreasureMap:TM_MapResource', 'quantity': 10},
                         {'templateId': 'UpgradePotion:UpgradeMana', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="DA1950BDDCAC4175B4A4732940B5CA40",
            dev_name="StorefrontStacked.Page01.ElementalHeroes.270",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 500, 'dynamicRegularPrice': -1,
                 'finalPrice': 500, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 500}],
            daily_limit=1,
            meta_info=[{'key': 'ButtonClassPath',
                        'value': "WidgetBlueprint'/Game/UMG/Store/B_StoreButton_Bundles.B_StoreButton_Bundles'"},
                       {'key': 'Type', 'value': 'ElementalHero'}, {'key': 'HideQuantityRemaining', 'value': 'True'}],
            catalog_group="ElementalHeroes",
            catalog_group_priority=270,
            sort_priority=72,
            title="Elemental Heroes",
            item_grants=[{'templateId': 'Reagent:Reagent_Hero_Event', 'quantity': 500},
                         {'templateId': 'Reagent:Reagent_HeroMap_Elemental', 'quantity': 140},
                         {'templateId': 'Currency:Hammer', 'quantity': 4},
                         {'templateId': 'Reagent:Reagent_HeroMap_SuperRare', 'quantity': 15},
                         {'templateId': 'Currency:Hammer', 'quantity': 3},
                         {'templateId': 'Reagent:Reagent_Hero_Event', 'quantity': 100},
                         {'templateId': 'Reagent:Reagent_Shared_T02', 'quantity': 50}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="38BC8BF259A743158704262464691EC2",
            dev_name="StorefrontMtx.L520000.MtxGift.55",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '06EED93D416CC285D8F887BA31411157',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '131F08B046089B1F82D8B5AF558E8742',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '520000'}],
            sort_priority=1000,
            title="Support Gift 63",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="30F1E03644EF73FDE0776CB66B3AA586",
            dev_name="12HR Basic Chest (Silver) - 25",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 100, 'dynamicRegularPrice': -1,
                 'finalPrice': 25, 'saleType': 'AmountOff', 'saleExpiration': '9999-12-31T23:59:59.999Z',
                 'basePrice': 25}],
            daily_limit=1,
            meta_info=[{'key': 'DAILYCHEST', 'value': 'true'}, {'key': 'type', 'value': 'dailylootbox'},
                       {'key': 'AccountLevelMin', 'value': '4'}, {'key': 'ButtonClassPath',
                                                                  'value': "WidgetBlueprint'/Game/UMG/Store"
                                                                           "/B_StoreButton_Bundles_Small"
                                                                           ".B_StoreButton_Bundles_Small'"}],
            catalog_group="Silver Chest",
            catalog_group_priority=3,
            sort_priority=115,
            title="12hr Basic Chest",
            item_grants=[{'templateId': 'Reagent:Reagent_Hero_Event', 'quantity': 100},
                         {'templateId': 'Currency:Hammer', 'quantity': 4}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="D654B24038F54728B460219036D8F180",
            dev_name="StorefrontLevel.L370000.LevelUpChest.17",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 5000, 'dynamicRegularPrice': -1,
                 'finalPrice': 5000, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 5000}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '9599934D4B2CFBC377CB67AB131F6B6B',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '4685928D450EBBA5B93598A2F37CFFF6',
                           'minQuantity': 1}],
            meta_info=[{'key': 'ButtonClassPath',
                        'value': "WidgetBlueprint'/Game/UMG/Store/B_StoreButton_Bundles.B_StoreButton_Bundles'"},
                       {'key': 'StoreLevelMin', 'value': '370000'}],
            sort_priority=60,
            title="Super Magic Chest",
            description="A Diamond Hero Crystal, 5000 Magic Tickets and 8 items!",
            item_grants=[{'templateId': 'Reagent:Reagent_Hero_Event', 'quantity': 5000},
                         {'templateId': 'Reagent:Reagent_HeroMap_SuperRare', 'quantity': 100},
                         {'templateId': 'Reagent:Reagent_HeroMap_Elemental', 'quantity': 500},
                         {'templateId': 'Reagent:Reagent_SupplyPoints_Elite', 'quantity': 200},
                         {'templateId': 'UpgradePotion:UpgradeHealthMajor', 'quantity': 50},
                         {'templateId': 'UpgradePotion:UpgradeStrengthMajor', 'quantity': 50},
                         {'templateId': 'UpgradePotion:UpgradeMana', 'quantity': 10}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="F002805939174124BF0C0F6AF5D2ED67",
            dev_name="StorefrontMtx.L290000.MtxGift.26",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '267A66044012B4293233CDB9199F91B2',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': 'F121FD584020B3BB4215BFB6C2723B63',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '290000'}],
            sort_priority=1000,
            title="Support Gift 40",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="F69DDAA3D24F4ED394D8E8EEDE7C7E67",
            dev_name="StorefrontMtx.L310000.MtxGift.29",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '24422CC946D4BBEF26BD38B1E8D4F1AB',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '4EB892244CC62635C6631D97E8A4DDAD',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '310000'}],
            sort_priority=1000,
            title="Support Gift 42",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="8B935496EDA84D2C8E1FDF67A11563D5",
            dev_name="StorefrontMtx.L340000.MtxGift.32",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '68F61AF9403A19EE7CB6B38B33A64EFE',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '4A66472743F146E7160266946FD8A5D2',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '340000'}],
            sort_priority=1000,
            title="Support Gift 45",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="C53D402C9561495AB8EF51A566FD3281",
            dev_name="StorefrontMtx.L470000.MtxGift.48",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '45A93AE643E53808914DC59CCE641783',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': 'DA4EB1D64213B51C77AE75B0DFC453EF',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '470000'}],
            sort_priority=1000,
            title="Support Gift 58",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="E29FF6EAD94B47C2AE55CCFF782D23FA",
            dev_name="StorefrontMtx.L160000.MtxGift.11",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '85CCBB5D4A8BFFD46A252F8401CC2BBC',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': 'E9A7C0524017B2C6740E14849A88DAA2',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '160000'}],
            sort_priority=1000,
            title="Support Gift 27",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="7A984F384AD542F4A3461EB525323DE5",
            dev_name="StorefrontLevel.L20000.LevelUpChest.07",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 5000, 'dynamicRegularPrice': -1,
                 'finalPrice': 5000, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 5000}],
            daily_limit=1,
            requirements=[{'requirementType': 'DenyOnFulfillment', 'requiredId': '70FF4DEA4EAAAFFC1CB40FAFC63DB495',
                           'minQuantity': 1}],
            meta_info=[{'key': 'ButtonClassPath',
                        'value': "WidgetBlueprint'/Game/UMG/Store/B_StoreButton_Bundles.B_StoreButton_Bundles'"},
                       {'key': 'StoreLevelMin', 'value': '20000'}],
            sort_priority=60,
            title="Super Magic Chest",
            description="A Diamond Hero Crystal, 5000 Magic Tickets and 8 items!",
            item_grants=[{'templateId': 'Reagent:Reagent_Hero_Event', 'quantity': 5000},
                         {'templateId': 'Reagent:Reagent_HeroMap_SuperRare', 'quantity': 100},
                         {'templateId': 'Reagent:Reagent_HeroMap_Elemental', 'quantity': 500},
                         {'templateId': 'Reagent:Reagent_SupplyPoints_Elite', 'quantity': 200},
                         {'templateId': 'UpgradePotion:UpgradeHealthMajor', 'quantity': 50},
                         {'templateId': 'UpgradePotion:UpgradeStrengthMajor', 'quantity': 50},
                         {'templateId': 'UpgradePotion:UpgradeMana', 'quantity': 10}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="2E10853B4E8B01964C2863B64D6250C9",
            dev_name="Mega Magic Chest (Weekly)",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 2000, 'dynamicRegularPrice': -1,
                 'finalPrice': 2000, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 2000}],
            weekly_limit=1,
            meta_info=[{'key': 'CHEST', 'value': 'true'}, {'key': 'ButtonClassPath',
                                                           'value': "WidgetBlueprint'/Game/UMG/Store"
                                                                    "/B_StoreButton_Bundles.B_StoreButton_Bundles'"},
                       {'key': 'IsGold', 'value': 'true'}, {'key': 'StoreLevelMin', 'value': '10000'}],
            sort_priority=65,
            title="Mega Magic Chest",
            description="A Gold Hero Crystal, 2000 Magic Tickets and 8 items! Available weekly.",
            item_grants=[{'templateId': 'Reagent:Reagent_HeroMap_Elemental', 'quantity': 1000},
                         {'templateId': 'Reagent:Reagent_HeroMap_SuperRare', 'quantity': 20},
                         {'templateId': 'Reagent:Reagent_Shared_MysteryGoo', 'quantity': 1},
                         {'templateId': 'Reagent:Reagent_Hero_Event', 'quantity': 2000},
                         {'templateId': 'Currency:SkillXP', 'quantity': 1000},
                         {'templateId': 'Currency:SkillXP', 'quantity': 1000},
                         {'templateId': 'Reagent:Reagent_Foil', 'quantity': 35}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="FFB78A3B3ED44432B894798F85DBF271",
            dev_name="StorefrontMtx.L880000.MtxGift.98",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '3BB881624BB8EB2F2D8B36A69F151905',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '08B7254D4901A7E821940F840BC24CC7',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '880000'}],
            sort_priority=1000,
            title="Support Gift 99",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="677D766C44F2213FD71B8D88EA623E4F",
            dev_name="Diamond Hero",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Voucher:Voucher_HeroDiamond', 'regularPrice': 1,
                     'dynamicRegularPrice': -1, 'finalPrice': 1, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 1}],
            meta_info=[{'key': 'AffordOnly', 'value': 'true'}, {'key': 'ButtonClassPath',
                                                                'value': "WidgetBlueprint'/Game/UMG/Store"
                                                                         "/B_StoreButton_Hero.B_StoreButton_Hero'"},
                       {'key': 'type', 'value': 'diamond'}, {'key': 'AutoRedeem', 'value': 'false'}],
            sort_priority=107,
            title="Diamond Hero",
            description="Add a powerful super rare hero to your team!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="7B41B217FD8B43A087021D1DCED6A3E4",
            dev_name="StorefrontMtx.L970000.MtxGift.109",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '2502E968436E5D2DF78BB1A266AA3C5B',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': 'FB4E32F849408CFC50038494DF0B371C',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '970000'}],
            sort_priority=1000,
            title="Support Gift 108",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="DBE0AB3035D24330A8D2CCE57F2FAD53",
            dev_name="StorefrontMtx.L890000.MtxGift.99",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '08B7254D4901A7E821940F840BC24CC7',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': 'B0DE74BB4B8CE1FE2370A5B60FBBA4EF',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '890000'}],
            sort_priority=1000,
            title="Support Gift 100",
            description="Can we have your autograph?",
        ))
        self.catalog_entries.append(Offer(
            offer_id="14F0BCD6DA8648CF81A7F967206B956B",
            dev_name="StorefrontMtx.L530000.MtxGift.56",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '131F08B046089B1F82D8B5AF558E8742',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '75A4D216442030897C9954A407FF0D5E',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '530000'}],
            sort_priority=1000,
            title="Support Gift 64",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="BADBF14AE73849119250EEA2FA1864F8",
            dev_name="StorefrontStacked.Page01.ElementalHeroes.179",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 500, 'dynamicRegularPrice': -1,
                 'finalPrice': 500, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 500}],
            daily_limit=1,
            meta_info=[{'key': 'ButtonClassPath',
                        'value': "WidgetBlueprint'/Game/UMG/Store/B_StoreButton_Bundles.B_StoreButton_Bundles'"},
                       {'key': 'Type', 'value': 'ElementalHero'}, {'key': 'HideQuantityRemaining', 'value': 'True'}],
            catalog_group="ElementalHeroes",
            catalog_group_priority=179,
            sort_priority=72,
            title="Elemental Heroes",
            item_grants=[{'templateId': 'Reagent:Reagent_Hero_Event', 'quantity': 500},
                         {'templateId': 'Reagent:Reagent_HeroMap_Elemental', 'quantity': 140},
                         {'templateId': 'Currency:Hammer', 'quantity': 4},
                         {'templateId': 'Reagent:Reagent_HeroMap_SuperRare', 'quantity': 15},
                         {'templateId': 'UpgradePotion:UpgradeHealthMajor', 'quantity': 5},
                         {'templateId': 'Reagent:Reagent_Hero_Event', 'quantity': 100},
                         {'templateId': 'Currency:SkillXP', 'quantity': 250}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="AC273E28438624F50FF33AAE8D95480A",
            dev_name="Starter Pack (S1)",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'RealMoney', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            app_store_id=[
                "",
                "9d517678254c4b27ab85f0d1d149784b",
                "bb_StarterPack1_C",
                "",
                "bb_starterpack1",
                "",
                "",
                "",
                "",
                "sam_kalestarter",
            ],
            requirements=[{'requirementType': 'DenyOnFulfillment', 'requiredId': '78314B1A48C50D547BBCC79EE27F767F',
                           'minQuantity': 1}],
            meta_info=[{'key': 'ButtonClassPath',
                        'value': "WidgetBlueprint'/Game/UMG/Store/B_StoreButton_AccountUpgrade"
                                 ".B_StoreButton_AccountUpgrade'"},
                       {'key': 'type', 'value': 'starterpack'}, {'key': 'bUseBannerForDetails', 'value': 'true'}],
            catalog_group="StarterPacks",
            catalog_group_priority=3,
            sort_priority=74,
            title="Starter Pack",
            short_description="A poison Ninja, gems, and resources to help you get started! ",
            description="<RT.CapsGreen>Recruit the poison ninja, Swiftslayer Kale!</>\r\n\r\n<RT.CapsGold>Includes "
                        "resources to upgrade Kale.</>",
            item_grants=[{'templateId': 'Currency:MtxPurchased', 'quantity': 300},
                         {'templateId': 'Character:Ninja_VR2_Nature_ThrowSword_T04', 'quantity': 1},
                         {'templateId': 'Currency:Gold', 'quantity': 300000},
                         {'templateId': 'Currency:HeroXp_Basic', 'quantity': 50000},
                         {'templateId': 'Reagent:Reagent_Shard_Nature', 'quantity': 25},
                         {'templateId': 'UpgradePotion:UpgradeStrengthMajor', 'quantity': 25},
                         {'templateId': 'UpgradePotion:UpgradeHealthMajor', 'quantity': 25}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="B3341C5A4F58010E79D702B1041C7C6C",
            dev_name="RocketFuel",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'RealMoney', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            app_store_id=[
                "",
                "311791cce7004593aa1884638613ae7f",
                "bb_RocketFuel_C",
                "",
                "bb_rocketfuel",
                "",
                "",
                "",
                "",
                "sam_warpspeed",
            ],
            requirements=[{'requirementType': 'DenyOnFulfillment', 'requiredId': '6d8ead1f183b4a85b68b74867374ad57',
                           'minQuantity': 1}],
            meta_info=[{'key': 'ButtonClassPath',
                        'value': "WidgetBlueprint'/Game/UMG/Store/B_StoreButton_AccountUpgrade"
                                 ".B_StoreButton_AccountUpgrade'"},
                       {'key': 'HideQuantityRemaining', 'value': 'True'}],
            catalog_group="StarterPacks",
            catalog_group_priority=3,
            sort_priority=74,
            title="Warp Speed",
            short_description="Ludicrous speed! Unlocks the ultimate warp speed mode plus 700 Gems!",
            description="What just happened?!\r\n\r\n* Unlocks Warp gameplay speed with roughly twice the speed of "
                        "normal play!\r\n* 700 Gems",
            item_grants=[{'templateId': 'StandIn:RocketFuel', 'quantity': 1, 'attributes': {'FakeQuantity': 1}}, {
                'templateId': 'Currency:MtxPurchased', 'quantity': 700}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="BA3E1D74569F40BFA48961037B3B618D",
            dev_name="StorefrontLevel.L470000.LevelUpChest.22",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 5000, 'dynamicRegularPrice': -1,
                 'finalPrice': 5000, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 5000}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '7363B7F84E1B0550EA36748DEFE29C23',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': 'CC1A5B204B3FDB3CBAF3AFA3211D4307',
                           'minQuantity': 1}],
            meta_info=[{'key': 'ButtonClassPath',
                        'value': "WidgetBlueprint'/Game/UMG/Store/B_StoreButton_Bundles.B_StoreButton_Bundles'"},
                       {'key': 'StoreLevelMin', 'value': '470000'}],
            sort_priority=60,
            title="Super Magic Chest",
            description="A Diamond Hero Crystal, 5000 Magic Tickets and 8 items!",
            item_grants=[{'templateId': 'Reagent:Reagent_Hero_Event', 'quantity': 5000},
                         {'templateId': 'Reagent:Reagent_HeroMap_SuperRare', 'quantity': 100},
                         {'templateId': 'Reagent:Reagent_HeroMap_Elemental', 'quantity': 500},
                         {'templateId': 'Reagent:Reagent_SupplyPoints_Elite', 'quantity': 200},
                         {'templateId': 'UpgradePotion:UpgradeHealthMajor', 'quantity': 50},
                         {'templateId': 'UpgradePotion:UpgradeStrengthMajor', 'quantity': 50},
                         {'templateId': 'UpgradePotion:UpgradeMana', 'quantity': 10}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="FC5C9E5F0CFF4C1D8C023E5BE2E4EBF0",
            dev_name="StorefrontLevel.L250000.LevelUpChest.10",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 5000, 'dynamicRegularPrice': -1,
                 'finalPrice': 5000, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 5000}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '33BA8DE54E81E8CFBEE108AC31F3E454',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': 'BD992F7F42063F197AB4EC921CD0BC16',
                           'minQuantity': 1}],
            meta_info=[{'key': 'ButtonClassPath',
                        'value': "WidgetBlueprint'/Game/UMG/Store/B_StoreButton_Bundles.B_StoreButton_Bundles'"},
                       {'key': 'StoreLevelMin', 'value': '250000'}],
            sort_priority=60,
            title="Super Magic Chest",
            description="A Diamond Hero Crystal, 5000 Magic Tickets and 8 items!",
            item_grants=[{'templateId': 'Reagent:Reagent_Hero_Event', 'quantity': 5000},
                         {'templateId': 'Reagent:Reagent_HeroMap_SuperRare', 'quantity': 100},
                         {'templateId': 'Reagent:Reagent_HeroMap_Elemental', 'quantity': 500},
                         {'templateId': 'Reagent:Reagent_SupplyPoints_Elite', 'quantity': 200},
                         {'templateId': 'UpgradePotion:UpgradeHealthMajor', 'quantity': 50},
                         {'templateId': 'UpgradePotion:UpgradeStrengthMajor', 'quantity': 50},
                         {'templateId': 'UpgradePotion:UpgradeMana', 'quantity': 10}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="97B98203D02A4F7D9182D248E505F5D5",
            dev_name="StorefrontMtx.L550000.MtxGift.59",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '9527715345720336DC2B3C88C4A56130',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '59D7755A4258A764FA399CA8C384A3A1',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '550000'}],
            sort_priority=1000,
            title="Support Gift 66",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="704A4ECEC4B048A39F8A50A10D53F486",
            dev_name="StorefrontMtx.L35000.MtxGift.33",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': 'C5F31BC54E89D885DEA27695C7F8AF3E',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '319E25444D07F24B97FF6FA1552EDBD7',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '35000'}],
            sort_priority=1000,
            title="Support Gift 8",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="1E8EC21E9BDD43FA996568DC90444FE3",
            dev_name="StorefrontStacked.Page01.ElementalHeroes.14",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 500, 'dynamicRegularPrice': -1,
                 'finalPrice': 500, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 500}],
            daily_limit=1,
            meta_info=[{'key': 'ButtonClassPath',
                        'value': "WidgetBlueprint'/Game/UMG/Store/B_StoreButton_Bundles.B_StoreButton_Bundles'"},
                       {'key': 'Type', 'value': 'ElementalHero'}, {'key': 'HideQuantityRemaining', 'value': 'True'}],
            catalog_group="ElementalHeroes",
            catalog_group_priority=14,
            sort_priority=72,
            title="Elemental Heroes",
            item_grants=[{'templateId': 'Reagent:Reagent_Hero_Event', 'quantity': 500},
                         {'templateId': 'Reagent:Reagent_HeroMap_Elemental', 'quantity': 140},
                         {'templateId': 'Currency:Hammer', 'quantity': 4},
                         {'templateId': 'Currency:Hammer', 'quantity': 4},
                         {'templateId': 'TreasureMap:TM_MapResource', 'quantity': 10},
                         {'templateId': 'Reagent:Reagent_RXT_Parts_Small', 'quantity': 5},
                         {'templateId': 'Reagent:Reagent_HeroMap_Elemental', 'quantity': 15}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="BDC1D23B131B420EBCA6E7DCA26A7AD9",
            dev_name="StorefrontMtx.L620000.MtxGift.67",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '4A6141634D3AC5AC701DD0B2F0AD8F9E',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': 'C4306C5E41B21FEE9C5192B7617A362E',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '620000'}],
            sort_priority=1000,
            title="Support Gift 73",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="52B546C54328062C50FE80BCB60E3ABA",
            dev_name="Account Level Up Package - Basic (Release)",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'RealMoney', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            app_store_id=[
                "",
                "8e60722d2cd54953907351b5a94debc5",
                "bb_levelup_release",
                "",
                "bb_levelup_release",
                "",
                "",
                "",
                "",
                "sam_levelup_release",
            ],
            requirements=[{'requirementType': 'DenyOnFulfillment', 'requiredId': '59F5930D4800D4810BE9DDBBBD694FA6',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '8383C7924A5B37A8C656A69987543CF4',
                           'minQuantity': 1}],
            meta_info=[{'key': 'type', 'value': 'accountlevelup'}, {'key': 'ButtonClassPath',
                                                                    'value': "WidgetBlueprint'/Game/UMG/Store"
                                                                             "/B_StoreButton_AccountUpgrade"
                                                                             ".B_StoreButton_AccountUpgrade'"},
                       {'key': 'AccountLevelMin', 'value': '35'}, {'key': 'AccountLevelMax', 'value': '250'},
                       {'key': 'MtxLevelMin', 'value': '100'}, {'key': 'PreviewFulfillmentClassPath',
                                                                'value': "CatalogFulfillment'/Game/Catalog"
                                                                         "/Fulfillments/Bundles/Sale"
                                                                         "/Release_LevelUpPackage_Basic"
                                                                         ".Release_LevelUpPackage_Basic'"}],
            sort_priority=29,
            title="Level-Up Pack",
            short_description="Rewards every 10 levels up to level 150, including Legendary Hero Traces!",
            description="<RT.CapsGreen>Complete Skybreaker Quests as you level!</>\r\n<RT.BasicMed>Receive a Level Up "
                        "Package every 10 levels from 10 to 150</>\r\n<RT.BasicMed>Packages are retroactive</>  "
                        "\r\n\r\n<RT.CapsGold>Level Up Package Contents</> \r\n  <RT.BasicMed>1000 Core Hero "
                        "Traces</>\r\n<RT.BasicMed>100k Gold</>\r\n\r\n<RT.BasicMed>The final package contains 100 "
                        "Legendary Hero Traces!</>",
            item_grants=[{'templateId': 'Giftbox:GB_LevelUpPackage_Basic01', 'quantity': 1},
                         {'templateId': 'Reagent:Reagent_HeroMap_Elemental', 'quantity': 1000}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="83A8B57EDDDF4D7BA4A8D189A6672346",
            dev_name="StorefrontMtx.L930000.MtxGift.104",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '3EEBE6C44ADC45AAD484B19A00BD9134',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '2468A46347C548FE8C4702A77B29CE07',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '930000'}],
            sort_priority=1000,
            title="Support Gift 104",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="07A6E16C3E344E0F9D6AE9B175F7F1F4",
            dev_name="StorefrontMtx.L350000.MtxGift.34",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '4A66472743F146E7160266946FD8A5D2',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '2AE410184EAB8943E57EABACB2480680',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '350000'}],
            sort_priority=1000,
            title="Support Gift 46",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="DD6ECF854F2BE5BF7A98C69581050EFB",
            dev_name="Light Hero",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'GameItem', 'currencySubType': 'Voucher:Voucher_HeroSilver_Light', 'regularPrice': 1,
                 'dynamicRegularPrice': -1, 'finalPrice': 1, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                 'basePrice': 1}],
            meta_info=[{'key': 'AffordOnly', 'value': 'true'}, {'key': 'ButtonClassPath',
                                                                'value': "WidgetBlueprint'/Game/UMG/Store"
                                                                         "/B_StoreButton_Hero.B_StoreButton_Hero'"},
                       {'key': 'type', 'value': 'light'}, {'key': 'AutoRedeem', 'value': 'false'}],
            sort_priority=101,
            title="Light Hero",
            description="Summon a hero to join your team!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="C18C7668C17F4F7CBA6574DA321F0214",
            dev_name="StorefrontLevel.L530000.LevelUpChest.26",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 5000, 'dynamicRegularPrice': -1,
                 'finalPrice': 5000, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 5000}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '2505AD4D4B9A19FBB46D0B9EBC1EA56C',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '92077EB243071AD9F0E7A2B5F2F71D7F',
                           'minQuantity': 1}],
            meta_info=[{'key': 'ButtonClassPath',
                        'value': "WidgetBlueprint'/Game/UMG/Store/B_StoreButton_Bundles.B_StoreButton_Bundles'"},
                       {'key': 'StoreLevelMin', 'value': '530000'}],
            sort_priority=60,
            title="Super Magic Chest",
            description="A Diamond Hero Crystal, 5000 Magic Tickets and 8 items!",
            item_grants=[{'templateId': 'Reagent:Reagent_Hero_Event', 'quantity': 5000},
                         {'templateId': 'Reagent:Reagent_HeroMap_SuperRare', 'quantity': 100},
                         {'templateId': 'Reagent:Reagent_HeroMap_Elemental', 'quantity': 500},
                         {'templateId': 'Reagent:Reagent_SupplyPoints_Elite', 'quantity': 200},
                         {'templateId': 'UpgradePotion:UpgradeHealthMajor', 'quantity': 50},
                         {'templateId': 'UpgradePotion:UpgradeStrengthMajor', 'quantity': 50},
                         {'templateId': 'UpgradePotion:UpgradeMana', 'quantity': 10}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="4744940B4BF99738ACA115A616EC8C4E",
            dev_name="Underworld Trader (T3)",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'RealMoney', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            app_store_id=[
                "",
                "395a588577834f4089f14440868a3785",
                "bb_viptier3_release",
                "",
                "bb_viptier3_release",
                "",
                "",
                "",
                "",
                "sam_viptier3_release",
            ],
            requirements=[{'requirementType': 'DenyOnFulfillment', 'requiredId': 'BE8A7A4F48546D69D0F8DF873120B3E6',
                           'minQuantity': 1}],
            meta_info=[{'key': 'VipLevelMin', 'value': '2'}, {'key': 'AccountLevelMin', 'value': '50'},
                       {'key': 'ButtonClassPath',
                        'value': "WidgetBlueprint'/Game/UMG/Store/B_StoreButton_AccountUpgrade"
                                 ".B_StoreButton_AccountUpgrade'"},
                       {'key': 'VipLevelMax', 'value': '2'}, {'key': 'type', 'value': 'accountupgrade'},
                       {'key': 'InspectItem', 'value': 'Character:Pet_SR1_Cloudpuff_Fire_T05'},
                       {'key': 'PreviewFulfillmentClassPath',
                        'value': "CatalogFulfillment'/Game/Catalog/Fulfillments/AccountUpgrades/Release_VIP_Tier3"
                                 ".Release_VIP_Tier3'"},
                       {'key': 'bShowInGemStore', 'value': 'true'}],
            catalog_group="AccountUpgrades",
            sort_priority=40,
            title="Underworld Trader Collection",
            short_description="A unique pet, free secret shop entry, quests, gems, a hero and more!",
            description="<RT.CapsGreen>Fierce Cloudpuff</> <RT.BasicMed>- a pet that greatly reduces enemy "
                        "DEF!</>\r\n\r\n<RT.CapsBlue>Includes Permanent Account Upgrades</>",
            display_asset_path="/Game/UMG/Textures/Store/btn_StoreGemGoldenChest.btn_StoreGemGoldenChest",
            item_grants=[{'templateId': 'Character:Pet_SR1_Cloudpuff_Fire_T05', 'quantity': 1},
                         {'templateId': 'StandIn:FreeSecretShopItem', 'quantity': 1},
                         {'templateId': 'StandIn:QuestLimit', 'quantity': 1},
                         {'templateId': 'Currency:MtxPurchased', 'quantity': 1500},
                         {'templateId': 'Currency:MtxPurchaseBonus', 'quantity': 1000},
                         {'templateId': 'Reagent:Reagent_HeroMap_Elemental', 'quantity': 500},
                         {'templateId': 'Reagent:Reagent_Shard_Dark', 'quantity': 15},
                         {'templateId': 'Reagent:Reagent_Shard_Fire', 'quantity': 15},
                         {'templateId': 'Reagent:Reagent_Shard_Light', 'quantity': 15},
                         {'templateId': 'Reagent:Reagent_Shard_Nature', 'quantity': 15},
                         {'templateId': 'Reagent:Reagent_Shard_Water', 'quantity': 15}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="6F897EF24E6F4DA3B73E3AE752FAE63E",
            dev_name="StorefrontMtx.L390000.MtxGift.38",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '4FF613E04A689AD396C48C814D9A8E2C',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': 'B5A4BF784C406402BF3D8CBD24A7CF39',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '390000'}],
            sort_priority=1000,
            title="Support Gift 50",
            description="You help make the game a reality!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="67519B03CC6C4378AEDAF416942FF857",
            dev_name="StorefrontMtx.L770000.MtxGift.85",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': 'F3D83DC94DA0E904C3C56DB7D5961108',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': 'C64C6E59441A5349F9AE91A876893321',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '770000'}],
            sort_priority=1000,
            title="Support Gift 88",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="EF80BD4FE3BD41728165D99E9709B7FF",
            dev_name="StorefrontMtx.L450000.MtxGift.46",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '15B714264A35B80083536D821A2C9203',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '38DB359C4DE88053A370F78B24A69908',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '450000'}],
            sort_priority=1000,
            title="Support Gift 56",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="FA390CC7ABF14CD98B9D1AB5224D16C4",
            dev_name="StorefrontMtx.L460000.MtxGift.47",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '38DB359C4DE88053A370F78B24A69908',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '45A93AE643E53808914DC59CCE641783',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '460000'}],
            sort_priority=1000,
            title="Support Gift 57",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="4F588386C6704F6DBA808F99D46DCB28",
            dev_name="StorefrontLevel.L310000.LevelUpChest.13",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 5000, 'dynamicRegularPrice': -1,
                 'finalPrice': 5000, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 5000}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '3B8A9D74477DAF56B37DDE84F453A9E5',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': 'E65689DC44393C8ED32C3EA98549786A',
                           'minQuantity': 1}],
            meta_info=[{'key': 'ButtonClassPath',
                        'value': "WidgetBlueprint'/Game/UMG/Store/B_StoreButton_Bundles.B_StoreButton_Bundles'"},
                       {'key': 'StoreLevelMin', 'value': '310000'}],
            sort_priority=60,
            title="Super Magic Chest",
            description="A Diamond Hero Crystal, 5000 Magic Tickets and 8 items!",
            item_grants=[{'templateId': 'Reagent:Reagent_Hero_Event', 'quantity': 5000},
                         {'templateId': 'Reagent:Reagent_HeroMap_SuperRare', 'quantity': 100},
                         {'templateId': 'Reagent:Reagent_HeroMap_Elemental', 'quantity': 500},
                         {'templateId': 'Reagent:Reagent_SupplyPoints_Elite', 'quantity': 200},
                         {'templateId': 'UpgradePotion:UpgradeHealthMajor', 'quantity': 50},
                         {'templateId': 'UpgradePotion:UpgradeStrengthMajor', 'quantity': 50},
                         {'templateId': 'UpgradePotion:UpgradeMana', 'quantity': 10}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="E3FA29E54B6A44079C5E95D24A6FE231",
            dev_name="StorefrontStacked.Page01.ElementalHeroes.71",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 500, 'dynamicRegularPrice': -1,
                 'finalPrice': 500, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 500}],
            daily_limit=1,
            meta_info=[{'key': 'ButtonClassPath',
                        'value': "WidgetBlueprint'/Game/UMG/Store/B_StoreButton_Bundles.B_StoreButton_Bundles'"},
                       {'key': 'Type', 'value': 'ElementalHero'}, {'key': 'HideQuantityRemaining', 'value': 'True'}],
            catalog_group="ElementalHeroes",
            catalog_group_priority=71,
            sort_priority=72,
            title="Elemental Heroes",
            item_grants=[{'templateId': 'Reagent:Reagent_Hero_Event', 'quantity': 500},
                         {'templateId': 'Reagent:Reagent_HeroMap_Elemental', 'quantity': 140},
                         {'templateId': 'Currency:Hammer', 'quantity': 4},
                         {'templateId': 'Reagent:Reagent_HeroMap_SuperRare', 'quantity': 20},
                         {'templateId': 'Reagent:Reagent_Foil', 'quantity': 5},
                         {'templateId': 'Reagent:Reagent_Shared_T02', 'quantity': 50},
                         {'templateId': 'Reagent:Reagent_HeroMap_SuperRare', 'quantity': 4}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="DC6CB1284AF36F773B0B6BA18DD64B25",
            dev_name="Treasure Hunter (T2)",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'RealMoney', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            app_store_id=[
                "",
                "20621749aaa04a49b28a2e68049470cb",
                "bb_viptier2_release",
                "",
                "bb_viptier2_release",
                "",
                "",
                "",
                "",
                "sam_viptier2_release",
            ],
            requirements=[{'requirementType': 'DenyOnFulfillment', 'requiredId': 'BE8A7A4F48546D69D0F8DF873120B3E6',
                           'minQuantity': 1}],
            meta_info=[{'key': 'VipLevelMin', 'value': '1'}, {'key': 'AccountLevelMin', 'value': '25'},
                       {'key': 'ButtonClassPath',
                        'value': "WidgetBlueprint'/Game/UMG/Store/B_StoreButton_AccountUpgrade"
                                 ".B_StoreButton_AccountUpgrade'"},
                       {'key': 'VipLevelMax', 'value': '1'}, {'key': 'type', 'value': 'accountupgrade'},
                       {'key': 'InspectItem', 'value': 'Character:Pet_SR1_Cloudpuff_Light_T05'},
                       {'key': 'PreviewFulfillmentClassPath',
                        'value': "CatalogFulfillment'/Game/Catalog/Fulfillments/AccountUpgrades/Release_VIP_Tier2"
                                 ".Release_VIP_Tier2'"},
                       {'key': 'bShowInGemStore', 'value': 'true'}],
            catalog_group="AccountUpgrades",
            sort_priority=40,
            title="Treasure Hunter Collection",
            short_description="A unique pet, free daily treasure maps, more teams, quests, gems, a hero and more!",
            description="<RT.CapsGreen>Cuddly Cloudpuff</> <RT.BasicMed> - a pet that resurrects and "
                        "heals!</>\r\n\r\n<RT.CapsBlue>Includes Permanent Account "
                        "Upgrades</>\r\n\r\n<RT.BasicMed>Treasure Hunts grant 5 Lockpicks and a daily bonus resource</>"
                        "",
            display_asset_path="/Game/UMG/Textures/Store/btn_StoreGemGoldenChest.btn_StoreGemGoldenChest",
            item_grants=[{'templateId': 'Party:Instance', 'quantity': 5},
                         {'templateId': 'Character:Pet_SR1_Cloudpuff_Light_T05', 'quantity': 1},
                         {'templateId': 'StandIn:DailyTreasureHuntChest', 'quantity': 1},
                         {'templateId': 'StandIn:TeamSlotsUpgrade', 'quantity': 1, 'attributes': {'FakeQuantity': 5}},
                         {'templateId': 'StandIn:InventoryUpgrade', 'quantity': 1, 'attributes': {'FakeQuantity': 25}},
                         {'templateId': 'StandIn:QuestLimit', 'quantity': 1, 'attributes': {'FakeQuantity': 1}},
                         {'templateId': 'Currency:MtxPurchased', 'quantity': 1500},
                         {'templateId': 'Currency:MtxPurchaseBonus', 'quantity': 750},
                         {'templateId': 'Reagent:Reagent_Hero_Event', 'quantity': 5000},
                         {'templateId': 'Reagent:Reagent_HeroMap_Elemental', 'quantity': 500},
                         {'templateId': 'Ore:Ore_Magicite', 'quantity': 100},
                         {'templateId': 'Ore:Ore_Silver', 'quantity': 1000},
                         {'templateId': 'Ore:Ore_Iron', 'quantity': 1000}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="AAB70BA93409477483295CDBDE2C6A50",
            dev_name="StorefrontMtx.L380000.MtxGift.37",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': 'CD425F9A4614451770592D976A9CB72A',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '4FF613E04A689AD396C48C814D9A8E2C',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '380000'}],
            sort_priority=1000,
            title="Support Gift 49",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="C988BA4B4BACFC5FE4C7389B7C594249",
            dev_name="Unwavering Guardian (T4)",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'RealMoney', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            app_store_id=[
                "",
                "760156eb63ad49b68861a5b269b73b48",
                "bb_viptier4_release",
                "",
                "bb_viptier4_release",
                "",
                "",
                "",
                "",
                "sam_viptier4_release",
            ],
            requirements=[{'requirementType': 'DenyOnFulfillment', 'requiredId': 'BE8A7A4F48546D69D0F8DF873120B3E6',
                           'minQuantity': 1}],
            meta_info=[{'key': 'VipLevelMin', 'value': '3'}, {'key': 'AccountLevelMin', 'value': '75'},
                       {'key': 'ButtonClassPath',
                        'value': "WidgetBlueprint'/Game/UMG/Store/B_StoreButton_AccountUpgrade"
                                 ".B_StoreButton_AccountUpgrade'"},
                       {'key': 'VipLevelMax', 'value': '3'}, {'key': 'type', 'value': 'accountupgrade'},
                       {'key': 'InspectItem', 'value': 'Character:Pet_SR1_Cloudpuff_Water_T05'},
                       {'key': 'PreviewFulfillmentClassPath',
                        'value': "CatalogFulfillment'/Game/Catalog/Fulfillments/AccountUpgrades/Release_VIP_Tier4"
                                 ".Release_VIP_Tier4'"},
                       {'key': 'bShowInGemStore', 'value': 'true'}],
            catalog_group="AccountUpgrades",
            sort_priority=40,
            title="Unwavering Guardian Collection",
            short_description="A unique pet, additional Rep Hero, use friends twice per day, quests, gems, a hero and "
                              "more!",
            description="<RT.CapsGreen>Olympian Cloudpuff</> <RT.BasicMed>- a pet that heals mana and prevents "
                        "debuffs!</>\r\n\r\n<RT.CapsBlue>Includes Permanent Account Upgrades</>",
            display_asset_path="/Game/UMG/Textures/Store/btn_StoreGemGoldenChest.btn_StoreGemGoldenChest",
            item_grants=[{'templateId': 'Character:Pet_SR1_Cloudpuff_Water_T05', 'quantity': 1},
                         {'templateId': 'Reagent:Reagent_HeroMap_SuperRare', 'quantity': 100},
                         {'templateId': 'StandIn:AdditionalRepHero', 'quantity': 1},
                         {'templateId': 'StandIn:AdditionalDailyFriendHeroUse', 'quantity': 2},
                         {'templateId': 'StandIn:AdditionalDailyGiftPoints', 'quantity': 1,
                          'attributes': {'FakeQuantity': 80}}, {'templateId': 'StandIn:QuestLimit', 'quantity': 1},
                         {'templateId': 'Currency:MtxPurchased', 'quantity': 1500},
                         {'templateId': 'Currency:MtxPurchaseBonus', 'quantity': 1500},
                         {'templateId': 'Currency:Hammer', 'quantity': 100},
                         {'templateId': 'Reagent:Reagent_HeroMap_Elemental', 'quantity': 500}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="1B6973A9D3614272B05A4E2C04279938",
            dev_name="StorefrontMtx.L280000.MtxGift.25",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '6EC4CB2241CDD5FFA61D059F0266A988',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '267A66044012B4293233CDB9199F91B2',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '280000'}],
            sort_priority=1000,
            title="Support Gift 39",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="2B004E8E91C74873954573F401C495A7",
            dev_name="StorefrontMtx.L130000.MtxGift.07",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': 'A21C10754CF2A279F3E72E959D1D7A6C',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '9E833A024D8FD5EAD1C4AD83D739AD24',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '130000'}],
            sort_priority=1000,
            title="Support Gift 24",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="248ABDECD33A48C2BED83CDAA3675FBD",
            dev_name="StorefrontStacked.Page01.ElementalHeroes.286",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 500, 'dynamicRegularPrice': -1,
                 'finalPrice': 500, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 500}],
            daily_limit=1,
            meta_info=[{'key': 'ButtonClassPath',
                        'value': "WidgetBlueprint'/Game/UMG/Store/B_StoreButton_Bundles.B_StoreButton_Bundles'"},
                       {'key': 'Type', 'value': 'ElementalHero'}, {'key': 'HideQuantityRemaining', 'value': 'True'}],
            catalog_group="ElementalHeroes",
            catalog_group_priority=286,
            sort_priority=72,
            title="Elemental Heroes",
            item_grants=[{'templateId': 'Reagent:Reagent_Hero_Event', 'quantity': 500},
                         {'templateId': 'Reagent:Reagent_HeroMap_Elemental', 'quantity': 140},
                         {'templateId': 'Currency:Hammer', 'quantity': 4},
                         {'templateId': 'Currency:SkillXP', 'quantity': 1500},
                         {'templateId': 'Currency:SkillXP', 'quantity': 250},
                         {'templateId': 'Reagent:Reagent_Shared_T02', 'quantity': 35},
                         {'templateId': 'Reagent:Reagent_HeroMap_Elemental', 'quantity': 50}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="8E37E79715ED430D9E983BE445E3E33E",
            dev_name="StorefrontLevel.L115000.LevelUpChest.02",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 5000, 'dynamicRegularPrice': -1,
                 'finalPrice': 5000, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 5000}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '5E0F227449A65CEEA0E5A9BBC01329CF',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '62A30DED4F2E3F8863CE0DB8B97125D5',
                           'minQuantity': 1}],
            meta_info=[{'key': 'ButtonClassPath',
                        'value': "WidgetBlueprint'/Game/UMG/Store/B_StoreButton_Bundles.B_StoreButton_Bundles'"},
                       {'key': 'StoreLevelMin', 'value': '115000'}],
            sort_priority=60,
            title="Super Magic Chest",
            description="A Diamond Hero Crystal, 5000 Magic Tickets and 8 items!",
            item_grants=[{'templateId': 'Reagent:Reagent_Hero_Event', 'quantity': 5000},
                         {'templateId': 'Reagent:Reagent_HeroMap_SuperRare', 'quantity': 100},
                         {'templateId': 'Reagent:Reagent_HeroMap_Elemental', 'quantity': 500},
                         {'templateId': 'Reagent:Reagent_SupplyPoints_Elite', 'quantity': 200},
                         {'templateId': 'UpgradePotion:UpgradeHealthMajor', 'quantity': 50},
                         {'templateId': 'UpgradePotion:UpgradeStrengthMajor', 'quantity': 50},
                         {'templateId': 'UpgradePotion:UpgradeMana', 'quantity': 10}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="7ACC9E3E4AD65D51D44D11A63EF00EA7",
            dev_name="Water Hero",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'GameItem', 'currencySubType': 'Voucher:Voucher_HeroSilver_Water', 'regularPrice': 1,
                 'dynamicRegularPrice': -1, 'finalPrice': 1, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                 'basePrice': 1}],
            meta_info=[{'key': 'AffordOnly', 'value': 'true'}, {'key': 'ButtonClassPath',
                                                                'value': "WidgetBlueprint'/Game/UMG/Store"
                                                                         "/B_StoreButton_Hero.B_StoreButton_Hero'"},
                       {'key': 'type', 'value': 'water'}, {'key': 'AutoRedeem', 'value': 'false'}],
            sort_priority=101,
            title="Water Hero",
            description="Summon a hero to join your team!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="2C88F53240C5132C629A23B0E569E7D1",
            dev_name="PowerEfflux Nature",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem',
                     'currencySubType': 'Voucher:Voucher_Hero_TreasureHunter_Nature_PowerEfflux', 'regularPrice': 1,
                     'dynamicRegularPrice': -1, 'finalPrice': 1, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 1}],
            meta_info=[{'key': 'AffordOnly', 'value': 'true'}, {'key': 'ButtonClassPath',
                                                                'value': "WidgetBlueprint'/Game/UMG/Store"
                                                                         "/B_StoreButton_Hero.B_StoreButton_Hero'"},
                       {'key': 'type', 'value': 'Random'}, {'key': 'AutoRedeem', 'value': 'true'}],
            sort_priority=9999,
            item_grants=[{'templateId': 'Character:TreasureHunter_R2_Nature_PowerEfflux_T03', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="4FADFAEED7004CD39245418BA1A6CC9A",
            dev_name="StorefrontMtx.L90000.MtxGift.100",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': 'E462EAA14B27F738FAC2B6B8428DD2FA',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '740E811445C06D5E4FD71E84F559593C',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '90000'}],
            sort_priority=1000,
            title="Support Gift 19",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="20127E956D94499FA2183DD86B048897",
            dev_name="StorefrontMtx.L800000.MtxGift.89",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': 'F0B52CD74EB72783AE8286BC75F1BEF1',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '26D8C467410A6F8B2D0216B98EC18F0B',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '800000'}],
            sort_priority=1000,
            title="Support Gift 91",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="AC5A697455F3455BBC4A0979994C89E7",
            dev_name="StorefrontMtx.L760000.MtxGift.84",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '95D438054A0CFA5ECC5EF582961AD9FC',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': 'F3D83DC94DA0E904C3C56DB7D5961108',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '760000'}],
            sort_priority=1000,
            title="Support Gift 87",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="B8751CE54CF5526D9E11E8BF4533FDC9",
            dev_name="12HR Basic Chest (Silver) (Battle Breaker)",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 100, 'dynamicRegularPrice': -1,
                 'finalPrice': 0, 'saleType': 'AmountOff', 'saleExpiration': '9999-12-31T23:59:59.999Z',
                 'basePrice': 0}],
            daily_limit=1,
            meta_info=[{'key': 'DAILYCHEST', 'value': 'true'}, {'key': 'VipLevelMin', 'value': '1'},
                       {'key': 'type', 'value': 'dailylootboxbb'}, {'key': 'ButtonClassPath',
                                                                    'value': "WidgetBlueprint'/Game/UMG/Store"
                                                                             "/B_StoreButton_Bundles_Small"
                                                                             ".B_StoreButton_Bundles_Small'"}],
            catalog_group="Silver Chest",
            catalog_group_priority=4,
            sort_priority=115,
            title="12hr Basic Chest",
            item_grants=[{'templateId': 'Reagent:Reagent_Hero_Event', 'quantity': 100},
                         {'templateId': 'Currency:Hammer', 'quantity': 4}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="56718B3E46FF8E47EA366CB62B14A85C",
            dev_name="Rare Meeg Crystal",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Voucher:Voucher_HeroMeegRare', 'regularPrice': 1,
                     'dynamicRegularPrice': -1, 'finalPrice': 1, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 1}],
            meta_info=[{'key': 'AffordOnly', 'value': 'true'}, {'key': 'ButtonClassPath',
                                                                'value': "WidgetBlueprint'/Game/UMG/Store"
                                                                         "/B_StoreButton_Hero.B_StoreButton_Hero'"},
                       {'key': 'type', 'value': 'meeg'}],
            sort_priority=104,
            title="Rare Meeg Crystal",
            description="Crack it open to find something special!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="76DF2F7323A04D68903405C18C9A1993",
            dev_name="StorefrontLevel.L350000.LevelUpChest.16",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 5000, 'dynamicRegularPrice': -1,
                 'finalPrice': 5000, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 5000}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '2F18BCC44E753971B12564A1449C37B5',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '9599934D4B2CFBC377CB67AB131F6B6B',
                           'minQuantity': 1}],
            meta_info=[{'key': 'ButtonClassPath',
                        'value': "WidgetBlueprint'/Game/UMG/Store/B_StoreButton_Bundles.B_StoreButton_Bundles'"},
                       {'key': 'StoreLevelMin', 'value': '350000'}],
            sort_priority=60,
            title="Super Magic Chest",
            description="A Diamond Hero Crystal, 5000 Magic Tickets and 8 items!",
            item_grants=[{'templateId': 'Reagent:Reagent_Hero_Event', 'quantity': 5000},
                         {'templateId': 'Reagent:Reagent_HeroMap_SuperRare', 'quantity': 100},
                         {'templateId': 'Reagent:Reagent_HeroMap_Elemental', 'quantity': 500},
                         {'templateId': 'Reagent:Reagent_SupplyPoints_Elite', 'quantity': 200},
                         {'templateId': 'UpgradePotion:UpgradeHealthMajor', 'quantity': 50},
                         {'templateId': 'UpgradePotion:UpgradeStrengthMajor', 'quantity': 50},
                         {'templateId': 'UpgradePotion:UpgradeMana', 'quantity': 10}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="D09C2DE994A040E08A3B556A24EF7D35",
            dev_name="StorefrontLevel.L150000.LevelUpChest.04",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 5000, 'dynamicRegularPrice': -1,
                 'finalPrice': 5000, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 5000}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': 'FE6C666D41BCDBA0704ED29B8A1FD492',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '4E0DF6CB4D36D1EF2CC5CBAA87EE65B1',
                           'minQuantity': 1}],
            meta_info=[{'key': 'ButtonClassPath',
                        'value': "WidgetBlueprint'/Game/UMG/Store/B_StoreButton_Bundles.B_StoreButton_Bundles'"},
                       {'key': 'StoreLevelMin', 'value': '150000'}],
            sort_priority=60,
            title="Super Magic Chest",
            description="A Diamond Hero Crystal, 5000 Magic Tickets and 8 items!",
            item_grants=[{'templateId': 'Reagent:Reagent_Hero_Event', 'quantity': 5000},
                         {'templateId': 'Reagent:Reagent_HeroMap_SuperRare', 'quantity': 100},
                         {'templateId': 'Reagent:Reagent_HeroMap_Elemental', 'quantity': 500},
                         {'templateId': 'Reagent:Reagent_SupplyPoints_Elite', 'quantity': 200},
                         {'templateId': 'UpgradePotion:UpgradeHealthMajor', 'quantity': 50},
                         {'templateId': 'UpgradePotion:UpgradeStrengthMajor', 'quantity': 50},
                         {'templateId': 'UpgradePotion:UpgradeMana', 'quantity': 10}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="C989E0D7E21E4299937EB5FB452074A5",
            dev_name="StorefrontStacked.Page01.ElementalHeroes.117",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 500, 'dynamicRegularPrice': -1,
                 'finalPrice': 500, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 500}],
            daily_limit=1,
            meta_info=[{'key': 'ButtonClassPath',
                        'value': "WidgetBlueprint'/Game/UMG/Store/B_StoreButton_Bundles.B_StoreButton_Bundles'"},
                       {'key': 'Type', 'value': 'ElementalHero'}, {'key': 'HideQuantityRemaining', 'value': 'True'}],
            catalog_group="ElementalHeroes",
            catalog_group_priority=117,
            sort_priority=72,
            title="Elemental Heroes",
            item_grants=[{'templateId': 'Reagent:Reagent_Hero_Event', 'quantity': 500},
                         {'templateId': 'Reagent:Reagent_HeroMap_Elemental', 'quantity': 140},
                         {'templateId': 'Currency:Hammer', 'quantity': 4},
                         {'templateId': 'Currency:SkillXP', 'quantity': 2000},
                         {'templateId': 'Reagent:Reagent_Shard_Dark', 'quantity': 1},
                         {'templateId': 'Reagent:Reagent_SupplyPoints_Elite', 'quantity': 10},
                         {'templateId': 'Reagent:Reagent_Hero_Event', 'quantity': 100}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="36A94DC99D984FC78A56AB821EBA78DF",
            dev_name="StorefrontStacked.Page01.ElementalHeroes.55",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 500, 'dynamicRegularPrice': -1,
                 'finalPrice': 500, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 500}],
            daily_limit=1,
            meta_info=[{'key': 'ButtonClassPath',
                        'value': "WidgetBlueprint'/Game/UMG/Store/B_StoreButton_Bundles.B_StoreButton_Bundles'"},
                       {'key': 'Type', 'value': 'ElementalHero'}, {'key': 'HideQuantityRemaining', 'value': 'True'}],
            catalog_group="ElementalHeroes",
            catalog_group_priority=55,
            sort_priority=72,
            title="Elemental Heroes",
            item_grants=[{'templateId': 'Reagent:Reagent_Hero_Event', 'quantity': 500},
                         {'templateId': 'Reagent:Reagent_HeroMap_Elemental', 'quantity': 140},
                         {'templateId': 'Currency:Hammer', 'quantity': 4},
                         {'templateId': 'UpgradePotion:UpgradeHealthMinor', 'quantity': 40},
                         {'templateId': 'Reagent:Reagent_HeroMap_Elemental', 'quantity': 50},
                         {'templateId': 'Reagent:Reagent_SupplyPoints_Elite', 'quantity': 10},
                         {'templateId': 'Reagent:Reagent_Shared_MysteryGoo', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="9D811D35983A4EB284B7F7B8A008C7DE",
            dev_name="StorefrontMtx.L590000.MtxGift.63",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '9632B0144E806B1508858E8526C8C7D2',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '670D0A5340ABB9757D737B96CA72AD20',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '590000'}],
            sort_priority=1000,
            title="Support Gift 70",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="D92B6BD03F754DED9FA649FBF4A135F8",
            dev_name="StorefrontMtx.L400000.MtxGift.40",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': 'B5A4BF784C406402BF3D8CBD24A7CF39',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '5D2606E94E550BB7A3BDE59294A9A6E9',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '400000'}],
            sort_priority=1000,
            title="Support Gift 51",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="3AA4AB3F4AF719A69F444792ABE587C6",
            dev_name="Elemental Hero Resources (Master of the Hoard)",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 500, 'dynamicRegularPrice': -1,
                 'finalPrice': 350, 'saleType': 'AmountOff', 'saleExpiration': '9999-12-31T23:59:59.999Z',
                 'basePrice': 350}],
            daily_limit=1,
            meta_info=[{'key': 'VipLevelMin', 'value': '5'}, {'key': 'ButtonClassPath',
                                                              'value': "WidgetBlueprint'/Game/UMG/Store"
                                                                       "/B_StoreButton_Bundles.B_StoreButton_Bundles'"},
                       {'key': 'type', 'value': 'ElementalHero'}],
            sort_priority=72,
            title="12hr Elemental Heroes",
            item_grants=[{'templateId': 'Reagent:Reagent_Hero_Event', 'quantity': 500},
                         {'templateId': 'Reagent:Reagent_HeroMap_Elemental', 'quantity': 140},
                         {'templateId': 'Currency:Hammer', 'quantity': 4},
                         {'templateId': 'Reagent:Reagent_SupplyPoints_Elite', 'quantity': 5},
                         {'templateId': 'Reagent:Reagent_HeroMap_Elemental', 'quantity': 60},
                         {'templateId': 'Reagent:Reagent_Foil', 'quantity': 10},
                         {'templateId': 'Currency:SkillXP', 'quantity': 500},
                         {'templateId': 'Reagent:Reagent_HeroMap_SuperRare', 'quantity': 10},
                         {'templateId': 'Reagent:WCCoins', 'quantity': 2},
                         {'templateId': 'Reagent:Reagent_Hero_Event', 'quantity': 200}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="1D9B7236AA01476EA8FCFC7EA41B7DBB",
            dev_name="StorefrontLevel.L35000.LevelUpChest.15",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 5000, 'dynamicRegularPrice': -1,
                 'finalPrice': 5000, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 5000}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '70FF4DEA4EAAAFFC1CB40FAFC63DB495',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': 'BD7EBC794C6B9B123BFCDBA223F68A0E',
                           'minQuantity': 1}],
            meta_info=[{'key': 'ButtonClassPath',
                        'value': "WidgetBlueprint'/Game/UMG/Store/B_StoreButton_Bundles.B_StoreButton_Bundles'"},
                       {'key': 'StoreLevelMin', 'value': '35000'}],
            sort_priority=60,
            title="Super Magic Chest",
            description="A Diamond Hero Crystal, 5000 Magic Tickets and 8 items!",
            item_grants=[{'templateId': 'Reagent:Reagent_Hero_Event', 'quantity': 5000},
                         {'templateId': 'Reagent:Reagent_HeroMap_SuperRare', 'quantity': 100},
                         {'templateId': 'Reagent:Reagent_HeroMap_Elemental', 'quantity': 500},
                         {'templateId': 'Reagent:Reagent_SupplyPoints_Elite', 'quantity': 200},
                         {'templateId': 'UpgradePotion:UpgradeHealthMajor', 'quantity': 50},
                         {'templateId': 'UpgradePotion:UpgradeStrengthMajor', 'quantity': 50},
                         {'templateId': 'UpgradePotion:UpgradeMana', 'quantity': 10}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="0FD29E0C4216F082922E1494F5349D1B",
            dev_name="PowerEfflux Fire",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'GameItem', 'currencySubType': 'Voucher:Voucher_Hero_TreasureHunter_Fire_PowerEfflux',
                 'regularPrice': 1, 'dynamicRegularPrice': -1, 'finalPrice': 1,
                 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 1}],
            meta_info=[{'key': 'AffordOnly', 'value': 'true'}, {'key': 'ButtonClassPath',
                                                                'value': "WidgetBlueprint'/Game/UMG/Store"
                                                                         "/B_StoreButton_Hero.B_StoreButton_Hero'"},
                       {'key': 'type', 'value': 'Random'}, {'key': 'AutoRedeem', 'value': 'true'}],
            sort_priority=9999,
            item_grants=[{'templateId': 'Character:TreasureHunter_R2_Fire_PowerEfflux_T03', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="829B782A46AF980800255085B160AA45",
            dev_name="PowerEfflux Water",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'GameItem', 'currencySubType': 'Voucher:Voucher_Hero_TreasureHunter_Water_PowerEfflux',
                 'regularPrice': 1, 'dynamicRegularPrice': -1, 'finalPrice': 1,
                 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 1}],
            meta_info=[{'key': 'AffordOnly', 'value': 'true'}, {'key': 'ButtonClassPath',
                                                                'value': "WidgetBlueprint'/Game/UMG/Store"
                                                                         "/B_StoreButton_Hero.B_StoreButton_Hero'"},
                       {'key': 'type', 'value': 'Random'}, {'key': 'AutoRedeem', 'value': 'true'}],
            sort_priority=9999,
            item_grants=[{'templateId': 'Character:TreasureHunter_R2_Water_PowerEfflux_T03', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="8137EFA4F4CF40E990A05FB00FA79FA2",
            dev_name="StorefrontStacked.Page01.ElementalHeroes.273",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 500, 'dynamicRegularPrice': -1,
                 'finalPrice': 500, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 500}],
            daily_limit=1,
            meta_info=[{'key': 'ButtonClassPath',
                        'value': "WidgetBlueprint'/Game/UMG/Store/B_StoreButton_Bundles.B_StoreButton_Bundles'"},
                       {'key': 'Type', 'value': 'ElementalHero'}, {'key': 'HideQuantityRemaining', 'value': 'True'}],
            catalog_group="ElementalHeroes",
            catalog_group_priority=273,
            sort_priority=72,
            title="Elemental Heroes",
            item_grants=[{'templateId': 'Reagent:Reagent_Hero_Event', 'quantity': 500},
                         {'templateId': 'Reagent:Reagent_HeroMap_Elemental', 'quantity': 140},
                         {'templateId': 'Currency:Hammer', 'quantity': 4},
                         {'templateId': 'Reagent:Reagent_Foil', 'quantity': 10},
                         {'templateId': 'UpgradePotion:UpgradeStrengthMajor', 'quantity': 5},
                         {'templateId': 'Reagent:Reagent_HeroMap_Elemental', 'quantity': 25},
                         {'templateId': 'Ore:Ore_Magicite', 'quantity': 10}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="A654319C5EE0461BA572B0C9782B5CBD",
            dev_name="StorefrontLevel.L570000.LevelUpChest.28",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 5000, 'dynamicRegularPrice': -1,
                 'finalPrice': 5000, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 5000}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '8A2CF2B442B4177565F52196364A120F',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': 'BD23EFDD4B93572E335B939B59627F0F',
                           'minQuantity': 1}],
            meta_info=[{'key': 'ButtonClassPath',
                        'value': "WidgetBlueprint'/Game/UMG/Store/B_StoreButton_Bundles.B_StoreButton_Bundles'"},
                       {'key': 'StoreLevelMin', 'value': '570000'}],
            sort_priority=60,
            title="Super Magic Chest",
            description="A Diamond Hero Crystal, 5000 Magic Tickets and 8 items!",
            item_grants=[{'templateId': 'Reagent:Reagent_Hero_Event', 'quantity': 5000},
                         {'templateId': 'Reagent:Reagent_HeroMap_SuperRare', 'quantity': 100},
                         {'templateId': 'Reagent:Reagent_HeroMap_Elemental', 'quantity': 500},
                         {'templateId': 'Reagent:Reagent_SupplyPoints_Elite', 'quantity': 200},
                         {'templateId': 'UpgradePotion:UpgradeHealthMajor', 'quantity': 50},
                         {'templateId': 'UpgradePotion:UpgradeStrengthMajor', 'quantity': 50},
                         {'templateId': 'UpgradePotion:UpgradeMana', 'quantity': 10}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="1BEE99CB4CEFE7BF2518CBAF5CA81023",
            dev_name="Meeg Crystal",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Voucher:Voucher_HeroMeeg', 'regularPrice': 1,
                     'dynamicRegularPrice': -1, 'finalPrice': 1, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 1}],
            meta_info=[{'key': 'AffordOnly', 'value': 'true'}, {'key': 'ButtonClassPath',
                                                                'value': "WidgetBlueprint'/Game/UMG/Store"
                                                                         "/B_StoreButton_Hero.B_StoreButton_Hero'"},
                       {'key': 'type', 'value': 'meeg'}],
            sort_priority=103,
            title="Meeg Crystal",
            description="Crack it open to find something special!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="3C9A2002402C57AFCEE6D6843AB1F283",
            dev_name="Mining Crystal",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Voucher:Voucher_Hero_Mine', 'regularPrice': 1,
                     'dynamicRegularPrice': -1, 'finalPrice': 1, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 1}],
            meta_info=[{'key': 'AffordOnly', 'value': 'true'}, {'key': 'ButtonClassPath',
                                                                'value': "WidgetBlueprint'/Game/UMG/Store"
                                                                         "/B_StoreButton_Hero.B_StoreButton_Hero'"},
                       {'key': 'type', 'value': 'Random'}, {'key': 'AutoRedeem', 'value': 'false'}],
            sort_priority=102,
            title="Mining Crystal",
            description="Crack it open to find something special!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="FB62DDCE8FFE4C74B06BCADE173F1CB0",
            dev_name="StorefrontMtx.L110000.MtxGift.05",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '7696BED040A499C469CBB9BA6A24F830',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '1369D9784B1B9096135B08BD23386E2D',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '110000'}],
            sort_priority=1000,
            title="Support Gift 22",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="71DAB8E8505D41F4B4D99CCD00B9B499",
            dev_name="StorefrontLevel.L50000.LevelUpChest.24",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 5000, 'dynamicRegularPrice': -1,
                 'finalPrice': 5000, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 5000}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': 'BD7EBC794C6B9B123BFCDBA223F68A0E',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': 'FC8853B24429F824CE4837B1A3C5B58A',
                           'minQuantity': 1}],
            meta_info=[{'key': 'ButtonClassPath',
                        'value': "WidgetBlueprint'/Game/UMG/Store/B_StoreButton_Bundles.B_StoreButton_Bundles'"},
                       {'key': 'StoreLevelMin', 'value': '50000'}],
            sort_priority=60,
            title="Super Magic Chest",
            description="A Diamond Hero Crystal, 5000 Magic Tickets and 8 items!",
            item_grants=[{'templateId': 'Reagent:Reagent_Hero_Event', 'quantity': 5000},
                         {'templateId': 'Reagent:Reagent_HeroMap_SuperRare', 'quantity': 100},
                         {'templateId': 'Reagent:Reagent_HeroMap_Elemental', 'quantity': 500},
                         {'templateId': 'Reagent:Reagent_SupplyPoints_Elite', 'quantity': 200},
                         {'templateId': 'UpgradePotion:UpgradeHealthMajor', 'quantity': 50},
                         {'templateId': 'UpgradePotion:UpgradeStrengthMajor', 'quantity': 50},
                         {'templateId': 'UpgradePotion:UpgradeMana', 'quantity': 10}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="BDC695F4D26346E7A28DEEA1C513E79A",
            dev_name="RandomNonRMTSale.BuildingMaterialBundle.04",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 200, 'dynamicRegularPrice': -1,
                 'finalPrice': 175, 'saleType': 'AmountOff', 'saleExpiration': '9999-12-31T23:59:59.999Z',
                 'basePrice': 175}],
            daily_limit=1,
            meta_info=[{'key': 'AccountLevelMin', 'value': '50'}, {'key': 'RotatingSale', 'value': 'True'},
                       {'key': 'ButtonClassPath',
                        'value': "WidgetBlueprint'/Game/UMG/Store/B_StoreButton_Bundles_Small"
                                 ".B_StoreButton_Bundles_Small'"}],
            sort_priority=74,
            title="Building Materials",
            short_description="10 Building Materials",
            item_grants=[{'templateId': 'Reagent:Reagent_Hero_Event', 'quantity': 200},
                         {'templateId': 'Reagent:Reagent_SupplyPoints_BuildingUpgrade', 'quantity': 10}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="94115A059B484EB1A600E070F9D9102D",
            dev_name="StorefrontLevel.L450000.LevelUpChest.21",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 5000, 'dynamicRegularPrice': -1,
                 'finalPrice': 5000, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 5000}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': 'B949A38F4F1AFF040AF09EA67355F09B',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '7363B7F84E1B0550EA36748DEFE29C23',
                           'minQuantity': 1}],
            meta_info=[{'key': 'ButtonClassPath',
                        'value': "WidgetBlueprint'/Game/UMG/Store/B_StoreButton_Bundles.B_StoreButton_Bundles'"},
                       {'key': 'StoreLevelMin', 'value': '450000'}],
            sort_priority=60,
            title="Super Magic Chest",
            description="A Diamond Hero Crystal, 5000 Magic Tickets and 8 items!",
            item_grants=[{'templateId': 'Reagent:Reagent_Hero_Event', 'quantity': 5000},
                         {'templateId': 'Reagent:Reagent_HeroMap_SuperRare', 'quantity': 100},
                         {'templateId': 'Reagent:Reagent_HeroMap_Elemental', 'quantity': 500},
                         {'templateId': 'Reagent:Reagent_SupplyPoints_Elite', 'quantity': 200},
                         {'templateId': 'UpgradePotion:UpgradeHealthMajor', 'quantity': 50},
                         {'templateId': 'UpgradePotion:UpgradeStrengthMajor', 'quantity': 50},
                         {'templateId': 'UpgradePotion:UpgradeMana', 'quantity': 10}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="51B8402D754E4FC3838D8F4B98A94CF4",
            dev_name="StorefrontLevel.L100000.LevelUpChest.01",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 5000, 'dynamicRegularPrice': -1,
                 'finalPrice': 5000, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 5000}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '1CE9D551409C5DF76678DBBD81B4FDB9',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '5E0F227449A65CEEA0E5A9BBC01329CF',
                           'minQuantity': 1}],
            meta_info=[{'key': 'ButtonClassPath',
                        'value': "WidgetBlueprint'/Game/UMG/Store/B_StoreButton_Bundles.B_StoreButton_Bundles'"},
                       {'key': 'StoreLevelMin', 'value': '100000'}],
            sort_priority=60,
            title="Super Magic Chest",
            description="A Diamond Hero Crystal, 5000 Magic Tickets and 8 items!",
            item_grants=[{'templateId': 'Reagent:Reagent_Hero_Event', 'quantity': 5000},
                         {'templateId': 'Reagent:Reagent_HeroMap_SuperRare', 'quantity': 100},
                         {'templateId': 'Reagent:Reagent_HeroMap_Elemental', 'quantity': 500},
                         {'templateId': 'Reagent:Reagent_SupplyPoints_Elite', 'quantity': 200},
                         {'templateId': 'UpgradePotion:UpgradeHealthMajor', 'quantity': 50},
                         {'templateId': 'UpgradePotion:UpgradeStrengthMajor', 'quantity': 50},
                         {'templateId': 'UpgradePotion:UpgradeMana', 'quantity': 10}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="950669FD059D457881B7E91872EBFA2B",
            dev_name="StorefrontMtx.L730000.MtxGift.80",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '6C731B18416AC27CC6F29CBD0FC2CB8A',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '28A9A2AE472680E9279EAAAC80FE133B',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '730000'}],
            sort_priority=1000,
            title="Support Gift 84",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="013BF4ADEA4248BDA5F988DC4B975C01",
            dev_name="StorefrontMtx.L600000.MtxGift.65",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '670D0A5340ABB9757D737B96CA72AD20',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '99C4CD6341895994F96C418162800C4B',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '600000'}],
            sort_priority=1000,
            title="Support Gift 71",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="EE7D33624F974A0C8E3422CA8624EC6F",
            dev_name="StorefrontMtx.L95000.MtxGift.106",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '740E811445C06D5E4FD71E84F559593C',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': 'FF31B86842EFA7A884529E90768AE3D3',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '95000'}],
            sort_priority=1000,
            title="Support Gift 20",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="B93CAA874C45B7BA06BD2CAD25531475",
            dev_name="Battle Pass (Free)",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 1000, 'dynamicRegularPrice': -1,
                 'finalPrice': 0, 'saleType': 'Strikethrough', 'saleExpiration': '9999-01-01T12:00:00.000Z',
                 'basePrice': 0}],
            monthly_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': 'BE8A7A4F48546D69D0F8DF873120B3E6',
                           'minQuantity': 1}],
            meta_info=[{'key': 'BonusOverride', 'value': '3000'}, {'key': 'ButtonClassPath',
                                                                   'value': "WidgetBlueprint'/Game/UMG/Store"
                                                                            "/B_StoreButton_Battlepass"
                                                                            ".B_StoreButton_Battlepass'"}],
            catalog_group="BattlePass",
            catalog_group_priority=2,
            sort_priority=500,
            title="Battle Pass",
            description="100 Gems every day for 30 days\r\nUnlocks premium Battle Pass rewards",
            display_asset_path="/Game/UMG/Textures/Store/btn_StoreGemBag.btn_StoreGemBag",
        ))
        self.catalog_entries.append(Offer(
            offer_id="D824D5FD9D0B4FBABD4D2E46E7A46808",
            dev_name="StorefrontMtx.L500000.MtxGift.53",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '105F8AFD4D3AF0210CFBDEBD62E6DCF8',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '2BFCE5B9460735E737669585D1895444',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '500000'}],
            sort_priority=1000,
            title="Support Gift 61",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="9E81909035A74E51979A66A3A0C7A246",
            dev_name="StorefrontMtx.L830000.MtxGift.92",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': 'AE3B458F433DE9BEF76CFFAFA6E5824B',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': 'EBB0863F49BB7043079813B5FCC2D915',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '830000'}],
            sort_priority=1000,
            title="Support Gift 94",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="A2278665382A4A389D9244FBBAC8354C",
            dev_name="StorefrontMtx.L700000.MtxGift.77",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': 'B133B6DC440D5686E38D49BBE35CD861',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '47201DAA4E39ECA176CD35AA4CF9A699',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '700000'}],
            sort_priority=1000,
            title="Support Gift 81",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="62924A7FC9A642DDBAD1A37DD96A5D0B",
            dev_name="StorefrontStacked.Page01.ElementalHeroes.319",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 500, 'dynamicRegularPrice': -1,
                 'finalPrice': 500, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 500}],
            daily_limit=1,
            meta_info=[{'key': 'ButtonClassPath',
                        'value': "WidgetBlueprint'/Game/UMG/Store/B_StoreButton_Bundles.B_StoreButton_Bundles'"},
                       {'key': 'Type', 'value': 'ElementalHero'}, {'key': 'HideQuantityRemaining', 'value': 'True'}],
            catalog_group="ElementalHeroes",
            catalog_group_priority=319,
            sort_priority=72,
            title="Elemental Heroes",
            item_grants=[{'templateId': 'Reagent:Reagent_Hero_Event', 'quantity': 500},
                         {'templateId': 'Reagent:Reagent_HeroMap_Elemental', 'quantity': 140},
                         {'templateId': 'Currency:Hammer', 'quantity': 4},
                         {'templateId': 'Reagent:Reagent_HeroMap_Elemental', 'quantity': 150},
                         {'templateId': 'Reagent:Reagent_Foil', 'quantity': 15},
                         {'templateId': 'UpgradePotion:UpgradeMana', 'quantity': 1},
                         {'templateId': 'Reagent:Reagent_Shard_Light', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="5AF2C9FC073D45D3AB409505BE6D7AE1",
            dev_name="StorefrontMtx.L40000.MtxGift.39",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '319E25444D07F24B97FF6FA1552EDBD7',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '10EF29A04E418C8E417CF7A40892E612',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '40000'}],
            sort_priority=1000,
            title="Support Gift 9",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="B2971E9916EC449ABF1D616E9910F68A",
            dev_name="StorefrontMtx.L870000.MtxGift.97",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '04AB19D44110BECA0DE37CAF7632195A',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '3BB881624BB8EB2F2D8B36A69F151905',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '870000'}],
            sort_priority=1000,
            title="Support Gift 98",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="192802C3DF17413BBA249D240FC7232C",
            dev_name="StorefrontMtx.L840000.MtxGift.93",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': 'EBB0863F49BB7043079813B5FCC2D915',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '594167794856DBCA4304328EDC133E15',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '840000'}],
            sort_priority=1000,
            title="Support Gift 95",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="DC4CC6470406467CAD3351C2C0C200FE",
            dev_name="StorefrontMtx.L20000.MtxGift.15",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': 'C92799DE44F0657A1C85C5BF6A1CC2B0',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '1DA1BAEC49524F730C07AA9D285CDDB3',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '20000'}],
            sort_priority=1000,
            title="Support Gift 5",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="BB705E9BC71545A99E81673915D9A376",
            dev_name="StorefrontMtx.L45000.MtxGift.45",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '10EF29A04E418C8E417CF7A40892E612',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '8352FBF848AB462C24BEEFABE6E373C0',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '45000'}],
            sort_priority=1000,
            title="Support Gift 10",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="8ED348DB4F6A6FA2A9AE28BCEA46D27B",
            dev_name="Silver Hero",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Voucher:Voucher_HeroSilver', 'regularPrice': 1,
                     'dynamicRegularPrice': -1, 'finalPrice': 1, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 1}],
            meta_info=[{'key': 'AffordOnly', 'value': 'true'}, {'key': 'ButtonClassPath',
                                                                'value': "WidgetBlueprint'/Game/UMG/Store"
                                                                         "/B_StoreButton_Hero.B_StoreButton_Hero'"},
                       {'key': 'type', 'value': 'silver'}, {'key': 'AutoRedeem', 'value': 'false'}],
            catalog_group="Silver Hero",
            sort_priority=100,
            title="Silver Hero",
            description="Summon a hero to join your team!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="ABBC1B5E4378416FAE163D70C9C9E491",
            dev_name="StorefrontMtx.L790000.MtxGift.87",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '6CBE11F4473C198CA22818827EF10200',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': 'F0B52CD74EB72783AE8286BC75F1BEF1',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '790000'}],
            sort_priority=1000,
            title="Support Gift 90",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="28634F6497D74ABABBF37FFD65613D5A",
            dev_name="StorefrontMtx.L910000.MtxGift.102",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '163B90B54347AA6F1BA40AA087DADF38',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': 'AA2F5806432BBFC19852F78A885B0659',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '910000'}],
            sort_priority=1000,
            title="Support Gift 102",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="EB904E19F7224C3A965A54FD4763BDA6",
            dev_name="StorefrontLevel.L410000.LevelUpChest.19",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 5000, 'dynamicRegularPrice': -1,
                 'finalPrice': 5000, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 5000}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': 'C1580AC74C42EEC07C38AB84A73A3A70',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': 'D0A62F8540F76D50B172988D31FF1B47',
                           'minQuantity': 1}],
            meta_info=[{'key': 'ButtonClassPath',
                        'value': "WidgetBlueprint'/Game/UMG/Store/B_StoreButton_Bundles.B_StoreButton_Bundles'"},
                       {'key': 'StoreLevelMin', 'value': '410000'}],
            sort_priority=60,
            title="Super Magic Chest",
            description="A Diamond Hero Crystal, 5000 Magic Tickets and 8 items!",
            item_grants=[{'templateId': 'Reagent:Reagent_Hero_Event', 'quantity': 5000},
                         {'templateId': 'Reagent:Reagent_HeroMap_SuperRare', 'quantity': 100},
                         {'templateId': 'Reagent:Reagent_HeroMap_Elemental', 'quantity': 500},
                         {'templateId': 'Reagent:Reagent_SupplyPoints_Elite', 'quantity': 200},
                         {'templateId': 'UpgradePotion:UpgradeHealthMajor', 'quantity': 50},
                         {'templateId': 'UpgradePotion:UpgradeStrengthMajor', 'quantity': 50},
                         {'templateId': 'UpgradePotion:UpgradeMana', 'quantity': 10}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="027A52624DAEE845BA4669A1DB5BD41E",
            dev_name="Magic Chest (Voucher)",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Voucher:Voucher_Chest_Gold', 'regularPrice': 1,
                     'dynamicRegularPrice': -1, 'finalPrice': 1, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 1}],
            meta_info=[{'key': 'CHEST', 'value': 'true'}, {'key': 'ButtonClassPath',
                                                           'value': "WidgetBlueprint'/Game/UMG/Store"
                                                                    "/B_StoreButton_Chest.B_StoreButton_Chest'"},
                       {'key': 'IsGold', 'value': 'true'}, {'key': 'AffordOnly', 'value': 'true'}],
            catalog_group="Gold Chest",
            catalog_group_priority=10,
            sort_priority=72,
            title="Magic Chest",
            description="Core Hero Shards, Magic Tickets and other valuable items",
        ))
        self.catalog_entries.append(Offer(
            offer_id="A505E68607D146F386B78A517839ED81",
            dev_name="StorefrontMtx.L65000.MtxGift.70",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '014262EC477B66DE83109CA381FED5AD',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': 'CC60997C47B1FCD9384468BAC133D076',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '65000'}],
            sort_priority=1000,
            title="Support Gift 14",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="8989143BA8024C2BBA89391E83BB99D6",
            dev_name="StorefrontMtx.L230000.MtxGift.19",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '1110F75F4FC800DF80F5C4969C7A7E79',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '3D7C6B744A5C5B729A984FA0EF7E8350',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '230000'}],
            sort_priority=1000,
            title="Support Gift 34",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="5CF426ED68EE4063A8DFB3BA8CD27281",
            dev_name="StorefrontMtx.L70000.MtxGift.76",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': 'CC60997C47B1FCD9384468BAC133D076',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': 'BEAC240147D696F03A55E796BF77ACD7',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '70000'}],
            sort_priority=1000,
            title="Support Gift 15",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="7D98BDEAF8A544399D11788935E8F24E",
            dev_name="StorefrontMtx.L990000.MtxGift.111",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '8F30DCC84E3D5ACB54275796E2D75E5B',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '2056F0AF47450E7F5739F6988E4CE902',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '990000'}],
            sort_priority=1000,
            title="Support Gift 110",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="8A679D4D1B174E3C8913C5B9F67C91EB",
            dev_name="StorefrontMtx.L430000.MtxGift.43",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '217EAEFF478385E11EA0EC8451C8F2BF',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '621ED4A24CF22364662C8B86D5681DBB',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '430000'}],
            sort_priority=1000,
            title="Support Gift 54",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="91208574988D40589F260EE1E473DC9C",
            dev_name="StorefrontMtx.L860000.MtxGift.96",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '983F329B4E8428567D4563A2B427F174',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '04AB19D44110BECA0DE37CAF7632195A',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '860000'}],
            sort_priority=1000,
            title="Support Gift 97",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="54B67FB8A7EA4116B23BEF1CB0843919",
            dev_name="StorefrontLevel.L65000.LevelUpChest.29",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 5000, 'dynamicRegularPrice': -1,
                 'finalPrice': 5000, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 5000}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': 'FC8853B24429F824CE4837B1A3C5B58A',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '2CFBBA1041E1576AD0A0B4AC3CDD4DB8',
                           'minQuantity': 1}],
            meta_info=[{'key': 'ButtonClassPath',
                        'value': "WidgetBlueprint'/Game/UMG/Store/B_StoreButton_Bundles.B_StoreButton_Bundles'"},
                       {'key': 'StoreLevelMin', 'value': '65000'}],
            sort_priority=60,
            title="Super Magic Chest",
            description="A Diamond Hero Crystal, 5000 Magic Tickets and 8 items!",
            item_grants=[{'templateId': 'Reagent:Reagent_Hero_Event', 'quantity': 5000},
                         {'templateId': 'Reagent:Reagent_HeroMap_SuperRare', 'quantity': 100},
                         {'templateId': 'Reagent:Reagent_HeroMap_Elemental', 'quantity': 500},
                         {'templateId': 'Reagent:Reagent_SupplyPoints_Elite', 'quantity': 200},
                         {'templateId': 'UpgradePotion:UpgradeHealthMajor', 'quantity': 50},
                         {'templateId': 'UpgradePotion:UpgradeStrengthMajor', 'quantity': 50},
                         {'templateId': 'UpgradePotion:UpgradeMana', 'quantity': 10}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="A3F4E0E64EF86C6926881799A0A2306B",
            dev_name="12hr Treasure Hunt",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Currency:Gold', 'regularPrice': 0,
                     'dynamicRegularPrice': -1, 'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 0}],
            daily_limit=1,
            meta_info=[{'key': 'VipLevelMin', 'value': '2'}, {'key': 'HideWhenEmpty', 'value': 'true'}],
            catalog_group_priority=1,
            sort_priority=116,
            title="12hr Treasure Hunt",
            description="5 Free Lockpicks, and Random Items for Treasure Hunters!",
            item_grants=[{'templateId': 'TreasureMap:TM_MapResource', 'quantity': 5}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="3B824A17BD8F49598D37583041A7CE15",
            dev_name="StorefrontStacked.Page01.ElementalHeroes.05",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 500, 'dynamicRegularPrice': -1,
                 'finalPrice': 500, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 500}],
            daily_limit=1,
            meta_info=[{'key': 'ButtonClassPath',
                        'value': "WidgetBlueprint'/Game/UMG/Store/B_StoreButton_Bundles.B_StoreButton_Bundles'"},
                       {'key': 'Type', 'value': 'ElementalHero'}, {'key': 'HideQuantityRemaining', 'value': 'True'}],
            catalog_group="ElementalHeroes",
            catalog_group_priority=5,
            sort_priority=72,
            title="Elemental Heroes",
            item_grants=[{'templateId': 'Reagent:Reagent_Hero_Event', 'quantity': 500},
                         {'templateId': 'Reagent:Reagent_HeroMap_Elemental', 'quantity': 140},
                         {'templateId': 'Currency:Hammer', 'quantity': 4},
                         {'templateId': 'Currency:SkillXP', 'quantity': 2500},
                         {'templateId': 'Reagent:Reagent_Shard_Nature', 'quantity': 1},
                         {'templateId': 'Reagent:Reagent_HeroMap_Elemental', 'quantity': 50},
                         {'templateId': 'Reagent:Reagent_HeroMap_SuperRare', 'quantity': 2}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="00C859D3544B4A068DD98BA905453CDF",
            dev_name="StorefrontMtx.L180000.MtxGift.13",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '18A5EC98493012C7A7AF869D43CDEE69',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '933C99554A70D66D804FA98829541A99',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '180000'}],
            sort_priority=1000,
            title="Support Gift 29",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="6BDBD627913D4D29B3F964519108DFF3",
            dev_name="StorefrontMtx.L15000.MtxGift.09",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '5796DC4E4A30D4075B12D1A809D1B1CC',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': 'C92799DE44F0657A1C85C5BF6A1CC2B0',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '15000'}],
            sort_priority=1000,
            title="Support Gift 4",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="BB92D0ACAF394753AD5E63DBC16446B9",
            dev_name="StorefrontMtx.L75000.MtxGift.82",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': 'BEAC240147D696F03A55E796BF77ACD7',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '2F90E8A14D3676B9182AD8B21C227F80',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '75000'}],
            sort_priority=1000,
            title="Support Gift 16",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="C1F8A25AC7964A86A1E8CA88C29122C5",
            dev_name="Storefront.HeroBundle.04",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 4500, 'dynamicRegularPrice': -1,
                 'finalPrice': 4500, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 4500}],
            daily_limit=1,
            weekly_limit=1,
            meta_info=[{'key': 'ButtonClassPath',
                        'value': "WidgetBlueprint'/Game/UMG/Store/B_StoreButton_AccountUpgrade"
                                 ".B_StoreButton_AccountUpgrade'"},
                       {'key': 'HideQuantityRemaining', 'value': 'True'}, {'key': 'Type', 'value': 'herobundle'}],
            sort_priority=74,
            title="HeroBundle",
            description="<RT.CapsGreen>A hero and upgrade resources!</>",
            item_grants=[{'templateId': 'Character:DragonKnight_SR1_Water_DragonForm_T05', 'quantity': 1},
                         {'templateId': 'Reagent:Reagent_Hero_Event', 'quantity': 2500},
                         {'templateId': 'Currency:Gold', 'quantity': 2113000},
                         {'templateId': 'Currency:HeroXp_Basic', 'quantity': 1260000},
                         {'templateId': 'Currency:SkillXP', 'quantity': 9100},
                         {'templateId': 'UpgradePotion:UpgradeHealthMinor', 'quantity': 74},
                         {'templateId': 'UpgradePotion:UpgradeHealthMajor', 'quantity': 74},
                         {'templateId': 'UpgradePotion:UpgradeStrengthMinor', 'quantity': 74},
                         {'templateId': 'UpgradePotion:UpgradeStrengthMajor', 'quantity': 74},
                         {'templateId': 'UpgradePotion:UpgradeMana', 'quantity': 25},
                         {'templateId': 'Ore:Ore_Iron', 'quantity': 4024},
                         {'templateId': 'Ore:Ore_Silver', 'quantity': 4024},
                         {'templateId': 'Ore:Ore_Magicite', 'quantity': 270},
                         {'templateId': 'Reagent:Reagent_Shared_T02', 'quantity': 450},
                         {'templateId': 'Reagent:Reagent_Shard_Water', 'quantity': 69}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="5237BDCFC050424A8BD2259DD4D8B9DC",
            dev_name="StorefrontMtx.L330000.MtxGift.31",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '7B06B6394E50D13C7248F0947280C2DE',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '68F61AF9403A19EE7CB6B38B33A64EFE',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '330000'}],
            sort_priority=1000,
            title="Support Gift 44",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="ECFD8517354946DCA6FA22718F1A9D34",
            dev_name="StorefrontMtx.L30000.MtxGift.27",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': 'D9467EB349B5955D042B6DB98B0BF2CA',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': 'C5F31BC54E89D885DEA27695C7F8AF3E',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '30000'}],
            sort_priority=1000,
            title="Support Gift 7",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="2A7965024E8D465BA6FEC553DF3B9111",
            dev_name="StorefrontLevel.L230000.LevelUpChest.09",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 5000, 'dynamicRegularPrice': -1,
                 'finalPrice': 5000, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 5000}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '735551394081781279D60F858635BC84',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '33BA8DE54E81E8CFBEE108AC31F3E454',
                           'minQuantity': 1}],
            meta_info=[{'key': 'ButtonClassPath',
                        'value': "WidgetBlueprint'/Game/UMG/Store/B_StoreButton_Bundles.B_StoreButton_Bundles'"},
                       {'key': 'StoreLevelMin', 'value': '230000'}],
            sort_priority=60,
            title="Super Magic Chest",
            description="A Diamond Hero Crystal, 5000 Magic Tickets and 8 items!",
            item_grants=[{'templateId': 'Reagent:Reagent_Hero_Event', 'quantity': 5000},
                         {'templateId': 'Reagent:Reagent_HeroMap_SuperRare', 'quantity': 100},
                         {'templateId': 'Reagent:Reagent_HeroMap_Elemental', 'quantity': 500},
                         {'templateId': 'Reagent:Reagent_SupplyPoints_Elite', 'quantity': 200},
                         {'templateId': 'UpgradePotion:UpgradeHealthMajor', 'quantity': 50},
                         {'templateId': 'UpgradePotion:UpgradeStrengthMajor', 'quantity': 50},
                         {'templateId': 'UpgradePotion:UpgradeMana', 'quantity': 10}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="C6476F994723A27C298B289058A918EF",
            dev_name="Dark Hero",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'GameItem', 'currencySubType': 'Voucher:Voucher_HeroSilver_Dark', 'regularPrice': 1,
                 'dynamicRegularPrice': -1, 'finalPrice': 1, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                 'basePrice': 1}],
            meta_info=[{'key': 'AffordOnly', 'value': 'true'}, {'key': 'ButtonClassPath',
                                                                'value': "WidgetBlueprint'/Game/UMG/Store"
                                                                         "/B_StoreButton_Hero.B_StoreButton_Hero'"},
                       {'key': 'type', 'value': 'dark'}, {'key': 'AutoRedeem', 'value': 'false'}],
            sort_priority=101,
            title="Dark Hero",
            description="Summon a hero to join your team!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="6E7A466943619D1EE062BC8A09843F5F",
            dev_name="Nature Hero",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'GameItem', 'currencySubType': 'Voucher:Voucher_HeroSilver_Nature', 'regularPrice': 1,
                 'dynamicRegularPrice': -1, 'finalPrice': 1, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                 'basePrice': 1}],
            meta_info=[{'key': 'AffordOnly', 'value': 'true'}, {'key': 'ButtonClassPath',
                                                                'value': "WidgetBlueprint'/Game/UMG/Store"
                                                                         "/B_StoreButton_Hero.B_StoreButton_Hero'"},
                       {'key': 'type', 'value': 'nature'}, {'key': 'AutoRedeem', 'value': 'false'}],
            sort_priority=101,
            title="Nature Hero",
            description="Summon a hero to join your team!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="BA24852247819DFDC572E0A0D5DA7563",
            dev_name="Hero Inventory",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 75, 'dynamicRegularPrice': -1,
                 'finalPrice': 75, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 75}],
            meta_info=[{'key': 'ServiceName', 'value': 'InventoryUpgrade'}, {'key': 'type', 'value': 'heroinventory'}],
            sort_priority=20,
            title="+5 Hero Inventory",
            description="Increases your maximum hero inventory size",
            item_grants=[{'templateId': 'StandIn:InventoryUpgrade', 'quantity': 5, 'attributes': {'FakeQuantity': 5}}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="755141BDB10248D0B71FF1899D4BF672",
            dev_name="StorefrontMtx.L560000.MtxGift.60",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '59D7755A4258A764FA399CA8C384A3A1',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': 'A33BE83644AFCC2B562D7EBDF37EC3BC',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '560000'}],
            sort_priority=1000,
            title="Support Gift 67",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="1A3A6DF349882AE8D962699646D832EB",
            dev_name="Master of the Hoard (T5)",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'RealMoney', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            app_store_id=[
                "",
                "2be4ab85c1ae42bab895be28ab6cb99e",
                "bb_viptier5_release",
                "",
                "bb_viptier5_release",
                "",
                "",
                "",
                "",
                "sam_viptier5_release",
            ],
            requirements=[{'requirementType': 'DenyOnFulfillment', 'requiredId': 'BE8A7A4F48546D69D0F8DF873120B3E6',
                           'minQuantity': 1}],
            meta_info=[{'key': 'VipLevelMin', 'value': '4'}, {'key': 'AccountLevelMin', 'value': '100'},
                       {'key': 'ButtonClassPath',
                        'value': "WidgetBlueprint'/Game/UMG/Store/B_StoreButton_AccountUpgrade"
                                 ".B_StoreButton_AccountUpgrade'"},
                       {'key': 'VipLevelMax', 'value': '4'}, {'key': 'type', 'value': 'accountupgrade'},
                       {'key': 'InspectItem', 'value': 'Character:Pet_SR1_Cloudpuff_Dark_T05'},
                       {'key': 'PreviewFulfillmentClassPath',
                        'value': "CatalogFulfillment'/Game/Catalog/Fulfillments/AccountUpgrades/Release_VIP_Tier5"
                                 ".Release_VIP_Tier5'"},
                       {'key': 'bShowInGemStore', 'value': 'true'}],
            catalog_group="AccountUpgrades",
            sort_priority=40,
            title="Master of the Hoard",
            short_description="A unique pet, extra pets for your Monster Pit, quests, gems, a hero and more!",
            description="<RT.CapsGreen>Dreadlord Cloudpuff</> <RT.BasicMed>- a pet that DEVOURS "
                        "EVERYTHING!</>\r\n\r\n<RT.CapsBlue>Includes Permanent Account "
                        "Upgrades</>\r\n\r\n<RT.BasicMed>Extra of each Cloudpuff pet for your Monster Pit!</>",
            display_asset_path="/Game/UMG/Textures/Store/btn_StoreGemCastleTreasury.btn_StoreGemCastleTreasury",
            item_grants=[{'templateId': 'Character:Pet_SR1_Cloudpuff_Dark_T05', 'quantity': 2}, {
                'templateId': 'Reagent:Reagent_HeroMap_SuperRare', 'quantity': 100}, {
                             'templateId': 'StandIn:ExtraFreeMarketplaceItem', 'quantity': 1}, {
                             'templateId': 'StandIn:DailydiscountonMagicChests', 'quantity': 1}, {
                             'templateId': 'StandIn:InventoryUpgrade', 'quantity': 1,
                             'attributes': {'FakeQuantity': 50}}, {
                             'templateId': 'StandIn:QuestLimit', 'quantity': 1}, {'templateId': 'Currency:MtxPurchased',
                                                                                  'quantity': 1500}, {
                             'templateId': 'Currency:MtxPurchaseBonus', 'quantity': 3000}, {
                             'templateId': 'Character:Pet_SR1_Cloudpuff_Fire_T05', 'quantity': 1}, {
                             'templateId': 'Character:Pet_SR1_Cloudpuff_Light_T05', 'quantity': 1}, {
                             'templateId': 'Character:Pet_SR1_Cloudpuff_Nature_T05', 'quantity': 1}, {
                             'templateId': 'Character:Pet_SR1_Cloudpuff_Water_T05', 'quantity': 1}, {
                             'templateId': 'Reagent:Reagent_HeroMap_Elemental', 'quantity': 500}, {
                             'templateId': 'Reagent:Reagent_Shared_MysteryGoo', 'quantity': 5}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="8098D5CE791B43C2A91EEFEF8CEEE999",
            dev_name="StorefrontStacked.Page01.ElementalHeroes.107",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 500, 'dynamicRegularPrice': -1,
                 'finalPrice': 500, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 500}],
            daily_limit=1,
            meta_info=[{'key': 'ButtonClassPath',
                        'value': "WidgetBlueprint'/Game/UMG/Store/B_StoreButton_Bundles.B_StoreButton_Bundles'"},
                       {'key': 'Type', 'value': 'ElementalHero'}, {'key': 'HideQuantityRemaining', 'value': 'True'}],
            catalog_group="ElementalHeroes",
            catalog_group_priority=107,
            sort_priority=72,
            title="Elemental Heroes",
            item_grants=[{'templateId': 'Reagent:Reagent_Hero_Event', 'quantity': 500},
                         {'templateId': 'Reagent:Reagent_HeroMap_Elemental', 'quantity': 140},
                         {'templateId': 'Currency:Hammer', 'quantity': 4},
                         {'templateId': 'TreasureMap:TM_MapResource', 'quantity': 20},
                         {'templateId': 'Reagent:Reagent_Hero_Event', 'quantity': 100},
                         {'templateId': 'Currency:SkillXP', 'quantity': 500},
                         {'templateId': 'UpgradePotion:UpgradeStrengthMinor', 'quantity': 5}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="2813E8EAD8024D068BDFCDAF56D1D0ED",
            dev_name="StorefrontMtx.L410000.MtxGift.41",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '5D2606E94E550BB7A3BDE59294A9A6E9',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '7B18E62F43F3DCDEBF31738AB90E4919',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '410000'}],
            sort_priority=1000,
            title="Support Gift 52",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="4EF029313A9D40FBA5AE920512BB1959",
            dev_name="StorefrontMtx.L200000.MtxGift.16",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '23D6690D45EBBE60E00EFE9563C24B89',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '6FC6A72A456C12719AA6488176878E18',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '200000'}],
            sort_priority=1000,
            title="Support Gift 31",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="44A778063A9E4114AF436FED6A7F4AF1",
            dev_name="StorefrontMtx.L300000.MtxGift.28",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': 'F121FD584020B3BB4215BFB6C2723B63',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '24422CC946D4BBEF26BD38B1E8D4F1AB',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '300000'}],
            sort_priority=1000,
            title="Support Gift 41",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="1C8A7645673446BBAFE6B8FC20E73024",
            dev_name="StorefrontMtx.L360000.MtxGift.35",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '2AE410184EAB8943E57EABACB2480680',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '44BB81AA4D528D13F5B64F857A30D41A',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '360000'}],
            sort_priority=1000,
            title="Support Gift 47",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="78CE7FF1DC4C43048E0CBE6087F0832F",
            dev_name="StorefrontMtx.L10000.MtxGift.02",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '1E024004419DCE5D80EBC9B0A07D5957',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '5796DC4E4A30D4075B12D1A809D1B1CC',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '10000'}],
            sort_priority=1000,
            title="Support Gift 3",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="BE1A51D47D2B4084B728E09C6F05433B",
            dev_name="StorefrontStacked.Page01.ElementalHeroes.07",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 500, 'dynamicRegularPrice': -1,
                 'finalPrice': 500, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 500}],
            daily_limit=1,
            meta_info=[{'key': 'ButtonClassPath',
                        'value': "WidgetBlueprint'/Game/UMG/Store/B_StoreButton_Bundles.B_StoreButton_Bundles'"},
                       {'key': 'Type', 'value': 'ElementalHero'}, {'key': 'HideQuantityRemaining', 'value': 'True'}],
            catalog_group="ElementalHeroes",
            catalog_group_priority=7,
            sort_priority=72,
            title="Elemental Heroes",
            item_grants=[{'templateId': 'Reagent:Reagent_Hero_Event', 'quantity': 500},
                         {'templateId': 'Reagent:Reagent_HeroMap_Elemental', 'quantity': 140},
                         {'templateId': 'Currency:Hammer', 'quantity': 4},
                         {'templateId': 'Currency:SkillXP', 'quantity': 1500},
                         {'templateId': 'Currency:SkillXP', 'quantity': 250},
                         {'templateId': 'Reagent:Reagent_Shared_T02', 'quantity': 35},
                         {'templateId': 'Reagent:Reagent_HeroMap_Elemental', 'quantity': 50}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="B95EDE8ACC1048D6A103A8014D741EFA",
            dev_name="StorefrontMtx.L780000.MtxGift.86",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': 'C64C6E59441A5349F9AE91A876893321',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '6CBE11F4473C198CA22818827EF10200',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '780000'}],
            sort_priority=1000,
            title="Support Gift 89",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="58EA7D322B8B4899B7661864BE961B93",
            dev_name="StorefrontMtx.L630000.MtxGift.68",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': 'C4306C5E41B21FEE9C5192B7617A362E',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '81A9C0044109547F2FC6A285D37B5A8F',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '630000'}],
            sort_priority=1000,
            title="Support Gift 74",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="EE9A031A709B4994A33A956CA1E58373",
            dev_name="StorefrontStacked.Page01.ElementalHeroes.60",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 500, 'dynamicRegularPrice': -1,
                 'finalPrice': 500, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 500}],
            daily_limit=1,
            meta_info=[{'key': 'ButtonClassPath',
                        'value': "WidgetBlueprint'/Game/UMG/Store/B_StoreButton_Bundles.B_StoreButton_Bundles'"},
                       {'key': 'Type', 'value': 'ElementalHero'}, {'key': 'HideQuantityRemaining', 'value': 'True'}],
            catalog_group="ElementalHeroes",
            catalog_group_priority=60,
            sort_priority=72,
            title="Elemental Heroes",
            item_grants=[{'templateId': 'Reagent:Reagent_Hero_Event', 'quantity': 500},
                         {'templateId': 'Reagent:Reagent_HeroMap_Elemental', 'quantity': 140},
                         {'templateId': 'Currency:Hammer', 'quantity': 4},
                         {'templateId': 'Reagent:Reagent_SupplyPoints_Elite', 'quantity': 50},
                         {'templateId': 'Reagent:Reagent_Misc_CeremonialSword', 'quantity': 1},
                         {'templateId': 'Currency:SkillXP', 'quantity': 250},
                         {'templateId': 'Reagent:Reagent_Shared_T02', 'quantity': 50}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="0E8DC9AB6426424EBCF9344ABD01C2FA",
            dev_name="StorefrontMtx.L490000.MtxGift.50",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '03F40DBD424A80428272648B6B6FDA5B',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '105F8AFD4D3AF0210CFBDEBD62E6DCF8',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '490000'}],
            sort_priority=1000,
            title="Support Gift 60",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="B7BEE44E78FD400DB2C4DE7C53C7D6C7",
            dev_name="StorefrontStacked.Page01.ElementalHeroes.258",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 500, 'dynamicRegularPrice': -1,
                 'finalPrice': 500, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 500}],
            daily_limit=1,
            meta_info=[{'key': 'ButtonClassPath',
                        'value': "WidgetBlueprint'/Game/UMG/Store/B_StoreButton_Bundles.B_StoreButton_Bundles'"},
                       {'key': 'Type', 'value': 'ElementalHero'}, {'key': 'HideQuantityRemaining', 'value': 'True'}],
            catalog_group="ElementalHeroes",
            catalog_group_priority=258,
            sort_priority=72,
            title="Elemental Heroes",
            item_grants=[{'templateId': 'Reagent:Reagent_Hero_Event', 'quantity': 500},
                         {'templateId': 'Reagent:Reagent_HeroMap_Elemental', 'quantity': 140},
                         {'templateId': 'Currency:Hammer', 'quantity': 4},
                         {'templateId': 'Reagent:Reagent_Hero_Event', 'quantity': 200},
                         {'templateId': 'UpgradePotion:UpgradeStrengthMajor', 'quantity': 5},
                         {'templateId': 'Reagent:Reagent_Shared_T02', 'quantity': 50},
                         {'templateId': 'Reagent:Reagent_Shard_Water', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="2BE20BABD3604E69A847695432EBFC51",
            dev_name="StorefrontMtx.L740000.MtxGift.81",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '28A9A2AE472680E9279EAAAC80FE133B',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '5F6B767A47A95247E35E80AE9A702A6E',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '740000'}],
            sort_priority=1000,
            title="Support Gift 85",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="E258A1838CA645B287B60F558B43D28D",
            dev_name="StorefrontLevel.L290000.LevelUpChest.12",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 5000, 'dynamicRegularPrice': -1,
                 'finalPrice': 5000, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 5000}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': 'AB17757F431499E83A7550A80E1A66BC',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '3B8A9D74477DAF56B37DDE84F453A9E5',
                           'minQuantity': 1}],
            meta_info=[{'key': 'ButtonClassPath',
                        'value': "WidgetBlueprint'/Game/UMG/Store/B_StoreButton_Bundles.B_StoreButton_Bundles'"},
                       {'key': 'StoreLevelMin', 'value': '290000'}],
            sort_priority=60,
            title="Super Magic Chest",
            description="A Diamond Hero Crystal, 5000 Magic Tickets and 8 items!",
            item_grants=[{'templateId': 'Reagent:Reagent_Hero_Event', 'quantity': 5000},
                         {'templateId': 'Reagent:Reagent_HeroMap_SuperRare', 'quantity': 100},
                         {'templateId': 'Reagent:Reagent_HeroMap_Elemental', 'quantity': 500},
                         {'templateId': 'Reagent:Reagent_SupplyPoints_Elite', 'quantity': 200},
                         {'templateId': 'UpgradePotion:UpgradeHealthMajor', 'quantity': 50},
                         {'templateId': 'UpgradePotion:UpgradeStrengthMajor', 'quantity': 50},
                         {'templateId': 'UpgradePotion:UpgradeMana', 'quantity': 10}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="D27930BFF58E46DE91E47576770BAB02",
            dev_name="StorefrontMtx.L240000.MtxGift.20",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '3D7C6B744A5C5B729A984FA0EF7E8350',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': 'DABF7ABF421751F780FC11BBDFD39273',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '240000'}],
            sort_priority=1000,
            title="Support Gift 35",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="383622516E564DDF9E4BA5C8DD2FCE1E",
            dev_name="StorefrontStacked.Page01.ElementalHeroes.33",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 500, 'dynamicRegularPrice': -1,
                 'finalPrice': 500, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 500}],
            daily_limit=1,
            meta_info=[{'key': 'ButtonClassPath',
                        'value': "WidgetBlueprint'/Game/UMG/Store/B_StoreButton_Bundles.B_StoreButton_Bundles'"},
                       {'key': 'Type', 'value': 'ElementalHero'}, {'key': 'HideQuantityRemaining', 'value': 'True'}],
            catalog_group="ElementalHeroes",
            catalog_group_priority=33,
            sort_priority=72,
            title="Elemental Heroes",
            item_grants=[{'templateId': 'Reagent:Reagent_Hero_Event', 'quantity': 500},
                         {'templateId': 'Reagent:Reagent_HeroMap_Elemental', 'quantity': 140},
                         {'templateId': 'Currency:Hammer', 'quantity': 4},
                         {'templateId': 'Ore:Ore_Magicite', 'quantity': 35},
                         {'templateId': 'Reagent:Reagent_RXT_Parts_Small', 'quantity': 5},
                         {'templateId': 'Currency:Gold', 'quantity': 100000},
                         {'templateId': 'Currency:Hammer', 'quantity': 3}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="51AD2AF99D66429A95B68D7181A20C32",
            dev_name="StorefrontStacked.Page01.ElementalHeroes.275",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 500, 'dynamicRegularPrice': -1,
                 'finalPrice': 500, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 500}],
            daily_limit=1,
            meta_info=[{'key': 'ButtonClassPath',
                        'value': "WidgetBlueprint'/Game/UMG/Store/B_StoreButton_Bundles.B_StoreButton_Bundles'"},
                       {'key': 'Type', 'value': 'ElementalHero'}, {'key': 'HideQuantityRemaining', 'value': 'True'}],
            catalog_group="ElementalHeroes",
            catalog_group_priority=275,
            sort_priority=72,
            title="Elemental Heroes",
            item_grants=[{'templateId': 'Reagent:Reagent_Hero_Event', 'quantity': 500},
                         {'templateId': 'Reagent:Reagent_HeroMap_Elemental', 'quantity': 140},
                         {'templateId': 'Reagent:Reagent_Shard_Water', 'quantity': 1},
                         {'templateId': 'Reagent:Reagent_Shard_Fire', 'quantity': 1},
                         {'templateId': 'Reagent:Reagent_Shard_Nature', 'quantity': 1},
                         {'templateId': 'Reagent:Reagent_Shard_Dark', 'quantity': 1},
                         {'templateId': 'Reagent:Reagent_Shard_Light', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="C95A3A6C7FB843F7BCB7AE050543CDE8",
            dev_name="StorefrontMtx.L220000.MtxGift.18",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '7E46090E45019AAB5F8BCEBD6BCB33F8',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '1110F75F4FC800DF80F5C4969C7A7E79',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '220000'}],
            sort_priority=1000,
            title="Support Gift 33",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="BC6B9262EFD24623ABFE28A145A39191",
            dev_name="StorefrontMtx.L150000.MtxGift.10",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': 'B3EC21C9458D51BEB1BA22999A375658',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '85CCBB5D4A8BFFD46A252F8401CC2BBC',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '150000'}],
            sort_priority=1000,
            title="Support Gift 26",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="AC14388926684BD8BEF7981099996B34",
            dev_name="StorefrontLevel.L390000.LevelUpChest.18",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 5000, 'dynamicRegularPrice': -1,
                 'finalPrice': 5000, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 5000}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '4685928D450EBBA5B93598A2F37CFFF6',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': 'C1580AC74C42EEC07C38AB84A73A3A70',
                           'minQuantity': 1}],
            meta_info=[{'key': 'ButtonClassPath',
                        'value': "WidgetBlueprint'/Game/UMG/Store/B_StoreButton_Bundles.B_StoreButton_Bundles'"},
                       {'key': 'StoreLevelMin', 'value': '390000'}],
            sort_priority=60,
            title="Super Magic Chest",
            description="A Diamond Hero Crystal, 5000 Magic Tickets and 8 items!",
            item_grants=[{'templateId': 'Reagent:Reagent_Hero_Event', 'quantity': 5000},
                         {'templateId': 'Reagent:Reagent_HeroMap_SuperRare', 'quantity': 100},
                         {'templateId': 'Reagent:Reagent_HeroMap_Elemental', 'quantity': 500},
                         {'templateId': 'Reagent:Reagent_SupplyPoints_Elite', 'quantity': 200},
                         {'templateId': 'UpgradePotion:UpgradeHealthMajor', 'quantity': 50},
                         {'templateId': 'UpgradePotion:UpgradeStrengthMajor', 'quantity': 50},
                         {'templateId': 'UpgradePotion:UpgradeMana', 'quantity': 10}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="9F5D14DBF6A346CB95C7FDC036469CF3",
            dev_name="StorefrontMtx.L570000.MtxGift.61",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': 'A33BE83644AFCC2B562D7EBDF37EC3BC',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': 'B1BF9CB842881A9E2E5D4CABB1F932F5',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '570000'}],
            sort_priority=1000,
            title="Support Gift 68",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="DC2B26E3496E49EBBFAB104EB935863C",
            dev_name="StorefrontStacked.Page01.ElementalHeroes.353",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 500, 'dynamicRegularPrice': -1,
                 'finalPrice': 500, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 500}],
            daily_limit=1,
            meta_info=[{'key': 'ButtonClassPath',
                        'value': "WidgetBlueprint'/Game/UMG/Store/B_StoreButton_Bundles.B_StoreButton_Bundles'"},
                       {'key': 'Type', 'value': 'ElementalHero'}, {'key': 'HideQuantityRemaining', 'value': 'True'}],
            catalog_group="ElementalHeroes",
            catalog_group_priority=353,
            sort_priority=72,
            title="Elemental Heroes",
            item_grants=[{'templateId': 'Reagent:Reagent_Hero_Event', 'quantity': 500},
                         {'templateId': 'Reagent:Reagent_HeroMap_Elemental', 'quantity': 140},
                         {'templateId': 'Currency:Hammer', 'quantity': 4},
                         {'templateId': 'Reagent:Reagent_Shared_T02', 'quantity': 150},
                         {'templateId': 'UpgradePotion:UpgradeHealthMinor', 'quantity': 5},
                         {'templateId': 'TreasureMap:TM_Special_GhostShip', 'quantity': 1},
                         {'templateId': 'TreasureMap:TM_MapResource', 'quantity': 10}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="E2CA822D40AEA5AB943DAB975B3038CB",
            dev_name="Gold Hero",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Voucher:Voucher_HeroGold', 'regularPrice': 1,
                     'dynamicRegularPrice': -1, 'finalPrice': 1, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 1}],
            meta_info=[{'key': 'AffordOnly', 'value': 'true'}, {'key': 'ButtonClassPath',
                                                                'value': "WidgetBlueprint'/Game/UMG/Store"
                                                                         "/B_StoreButton_Hero.B_StoreButton_Hero'"},
                       {'key': 'type', 'value': 'gold'}, {'key': 'AutoRedeem', 'value': 'false'}],
            sort_priority=102,
            title="Gold Hero",
            description="Add a powerful very rare or higher hero to your team!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="F576C3C4BC21415E8CE3146BE68C6C6F",
            dev_name="StorefrontMtx.L170000.MtxGift.12",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': 'E9A7C0524017B2C6740E14849A88DAA2',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '18A5EC98493012C7A7AF869D43CDEE69',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '170000'}],
            sort_priority=1000,
            title="Support Gift 28",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="A1EDCFBAEC4B4A7DB26CAFD1A40DFA71",
            dev_name="StorefrontMtx.L670000.MtxGift.73",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '9CBA0101494E26B58A5408872F3C4353',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': 'E053B31F4111B3AF758685885D5CBED9',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '670000'}],
            sort_priority=1000,
            title="Support Gift 78",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="F2B4DF2B8640487D8A3CB46B1485F804",
            dev_name="StorefrontStacked.Page01.ElementalHeroes.379",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 500, 'dynamicRegularPrice': -1,
                 'finalPrice': 500, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 500}],
            daily_limit=1,
            meta_info=[{'key': 'ButtonClassPath',
                        'value': "WidgetBlueprint'/Game/UMG/Store/B_StoreButton_Bundles.B_StoreButton_Bundles'"},
                       {'key': 'Type', 'value': 'ElementalHero'}, {'key': 'HideQuantityRemaining', 'value': 'True'}],
            catalog_group="ElementalHeroes",
            catalog_group_priority=379,
            sort_priority=72,
            title="Elemental Heroes",
            item_grants=[{'templateId': 'Reagent:Reagent_Hero_Event', 'quantity': 500},
                         {'templateId': 'Reagent:Reagent_HeroMap_Elemental', 'quantity': 140},
                         {'templateId': 'Currency:Hammer', 'quantity': 4},
                         {'templateId': 'Reagent:Reagent_HeroMap_Elemental', 'quantity': 50},
                         {'templateId': 'UpgradePotion:UpgradeStrengthMinor', 'quantity': 5},
                         {'templateId': 'TreasureMap:TM_ForestOfMixedEmotions_Map8', 'quantity': 1},
                         {'templateId': 'Reagent:Reagent_RXT_Parts_Small', 'quantity': 5}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="2397FE674EA1F134D3C8B2A21B53F131",
            dev_name="Drake",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Voucher:Voucher_Hero_Mage_Fire_BurningSword',
                     'regularPrice': 1, 'dynamicRegularPrice': -1, 'finalPrice': 1,
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 1}],
            meta_info=[{'key': 'AffordOnly', 'value': 'true'}, {'key': 'ButtonClassPath',
                                                                'value': "WidgetBlueprint'/Game/UMG/Store"
                                                                         "/B_StoreButton_Hero.B_StoreButton_Hero'"},
                       {'key': 'type', 'value': 'Random'}, {'key': 'AutoRedeem', 'value': 'true'}],
            sort_priority=9999,
            title="Drake",
            description="Free Drake from his crystal!",
            item_grants=[{'templateId': 'Character:Mage_Starter_Fire_BurningSwordCombo_T03', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="F2BACD7BABA64833B4563E71D778B516",
            dev_name="StorefrontMtx.L120000.MtxGift.06",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '1369D9784B1B9096135B08BD23386E2D',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': 'A21C10754CF2A279F3E72E959D1D7A6C',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '120000'}],
            sort_priority=1000,
            title="Support Gift 23",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="2B3B76515F044F84A2AB7A8EF16CBF17",
            dev_name="StorefrontMtx.L320000.MtxGift.30",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '4EB892244CC62635C6631D97E8A4DDAD',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '7B06B6394E50D13C7248F0947280C2DE',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '320000'}],
            sort_priority=1000,
            title="Support Gift 43",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="D7A61CEE232947F2A381B0B215928C2F",
            dev_name="StorefrontMtx.L540000.MtxGift.57",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '75A4D216442030897C9954A407FF0D5E',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '9527715345720336DC2B3C88C4A56130',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '540000'}],
            sort_priority=1000,
            title="Support Gift 65",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="ECA4EAF1D6F743C1B1E52724871501ED",
            dev_name="StorefrontMtx.L1000.MtxGift.01",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'DenyOnFulfillment', 'requiredId': '0C425A7840E80B644949B2AD5291BD98',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '1000'}],
            sort_priority=1000,
            title="Support Gift 1",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="514EE1B2422FB17AB8F8618B385F66FA",
            dev_name="Basic Chest (Silver)",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 100, 'dynamicRegularPrice': -1,
                 'finalPrice': 100, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 100}],
            daily_limit=1,
            meta_info=[{'key': 'DAILYCHEST', 'value': 'true'}, {'key': 'type', 'value': 'dailylootbox'},
                       {'key': 'AccountLevelMin', 'value': '4'}, {'key': 'ButtonClassPath',
                                                                  'value': "WidgetBlueprint'/Game/UMG/Store"
                                                                           "/B_StoreButton_Bundles_Small"
                                                                           ".B_StoreButton_Bundles_Small'"}],
            catalog_group="Silver Chest",
            sort_priority=115,
            title="Basic Chest",
            item_grants=[{'templateId': 'Reagent:Reagent_Hero_Event', 'quantity': 100},
                         {'templateId': 'Currency:Hammer', 'quantity': 4}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="FBA88017C7ED4E24AD29A55FF2A8AFEC",
            dev_name="StorefrontLevel.L490000.LevelUpChest.23",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 5000, 'dynamicRegularPrice': -1,
                 'finalPrice': 5000, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 5000}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': 'CC1A5B204B3FDB3CBAF3AFA3211D4307',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '90C2A42E4DD0334F1E67DEA8D228B8F0',
                           'minQuantity': 1}],
            meta_info=[{'key': 'ButtonClassPath',
                        'value': "WidgetBlueprint'/Game/UMG/Store/B_StoreButton_Bundles.B_StoreButton_Bundles'"},
                       {'key': 'StoreLevelMin', 'value': '490000'}],
            sort_priority=60,
            title="Super Magic Chest",
            description="A Diamond Hero Crystal, 5000 Magic Tickets and 8 items!",
            item_grants=[{'templateId': 'Reagent:Reagent_Hero_Event', 'quantity': 5000},
                         {'templateId': 'Reagent:Reagent_HeroMap_SuperRare', 'quantity': 100},
                         {'templateId': 'Reagent:Reagent_HeroMap_Elemental', 'quantity': 500},
                         {'templateId': 'Reagent:Reagent_SupplyPoints_Elite', 'quantity': 200},
                         {'templateId': 'UpgradePotion:UpgradeHealthMajor', 'quantity': 50},
                         {'templateId': 'UpgradePotion:UpgradeStrengthMajor', 'quantity': 50},
                         {'templateId': 'UpgradePotion:UpgradeMana', 'quantity': 10}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="6DF17286032D4A818AAF86C100B06AB1",
            dev_name="StorefrontMtx.L80000.MtxGift.88",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '2F90E8A14D3676B9182AD8B21C227F80',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': 'A53DFF334DBCB6079E9D1A9AB22F902C',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '80000'}],
            sort_priority=1000,
            title="Support Gift 17",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="6E0A0982102E4273B8B9348EC2FC1B56",
            dev_name="StorefrontLevel.L270000.LevelUpChest.11",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 5000, 'dynamicRegularPrice': -1,
                 'finalPrice': 5000, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 5000}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': 'BD992F7F42063F197AB4EC921CD0BC16',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': 'AB17757F431499E83A7550A80E1A66BC',
                           'minQuantity': 1}],
            meta_info=[{'key': 'ButtonClassPath',
                        'value': "WidgetBlueprint'/Game/UMG/Store/B_StoreButton_Bundles.B_StoreButton_Bundles'"},
                       {'key': 'StoreLevelMin', 'value': '270000'}],
            sort_priority=60,
            title="Super Magic Chest",
            description="A Diamond Hero Crystal, 5000 Magic Tickets and 8 items!",
            item_grants=[{'templateId': 'Reagent:Reagent_Hero_Event', 'quantity': 5000},
                         {'templateId': 'Reagent:Reagent_HeroMap_SuperRare', 'quantity': 100},
                         {'templateId': 'Reagent:Reagent_HeroMap_Elemental', 'quantity': 500},
                         {'templateId': 'Reagent:Reagent_SupplyPoints_Elite', 'quantity': 200},
                         {'templateId': 'UpgradePotion:UpgradeHealthMajor', 'quantity': 50},
                         {'templateId': 'UpgradePotion:UpgradeStrengthMajor', 'quantity': 50},
                         {'templateId': 'UpgradePotion:UpgradeMana', 'quantity': 10}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="E50D5FCCC2C44C4681BE63FDE8A5C731",
            dev_name="StorefrontMtx.L920000.MtxGift.103",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': 'AA2F5806432BBFC19852F78A885B0659',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '3EEBE6C44ADC45AAD484B19A00BD9134',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '920000'}],
            sort_priority=1000,
            title="Support Gift 103",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="C554B16748E84873B5953ADB1C502025",
            dev_name="StorefrontLevel.L210000.LevelUpChest.08",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 5000, 'dynamicRegularPrice': -1,
                 'finalPrice': 5000, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 5000}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': 'D3E0B11D45BF46F1353F309ABC413135',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '735551394081781279D60F858635BC84',
                           'minQuantity': 1}],
            meta_info=[{'key': 'ButtonClassPath',
                        'value': "WidgetBlueprint'/Game/UMG/Store/B_StoreButton_Bundles.B_StoreButton_Bundles'"},
                       {'key': 'StoreLevelMin', 'value': '210000'}],
            sort_priority=60,
            title="Super Magic Chest",
            description="A Diamond Hero Crystal, 5000 Magic Tickets and 8 items!",
            item_grants=[{'templateId': 'Reagent:Reagent_Hero_Event', 'quantity': 5000},
                         {'templateId': 'Reagent:Reagent_HeroMap_SuperRare', 'quantity': 100},
                         {'templateId': 'Reagent:Reagent_HeroMap_Elemental', 'quantity': 500},
                         {'templateId': 'Reagent:Reagent_SupplyPoints_Elite', 'quantity': 200},
                         {'templateId': 'UpgradePotion:UpgradeHealthMajor', 'quantity': 50},
                         {'templateId': 'UpgradePotion:UpgradeStrengthMajor', 'quantity': 50},
                         {'templateId': 'UpgradePotion:UpgradeMana', 'quantity': 10}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="68C82ED49FA34AEF8D2B8A3F9C0DF0DF",
            dev_name="StorefrontMtx.L640000.MtxGift.69",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '81A9C0044109547F2FC6A285D37B5A8F',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '75C7E43249236441B9002F8B752C6117',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '640000'}],
            sort_priority=1000,
            title="Support Gift 75",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="5A8C3360408F40E3839FDAE5DF2380DD",
            dev_name="StorefrontMtx.L850000.MtxGift.95",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '594167794856DBCA4304328EDC133E15',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '983F329B4E8428567D4563A2B427F174',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '850000'}],
            sort_priority=1000,
            title="Support Gift 96",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="9A2BE5888F4D4BFE874D0CCB292DA9B4",
            dev_name="StorefrontLevel.L170000.LevelUpChest.05",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 5000, 'dynamicRegularPrice': -1,
                 'finalPrice': 5000, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 5000}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '4E0DF6CB4D36D1EF2CC5CBAA87EE65B1',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '96AF5DA3462C0C7D5C35CD9104F4527B',
                           'minQuantity': 1}],
            meta_info=[{'key': 'ButtonClassPath',
                        'value': "WidgetBlueprint'/Game/UMG/Store/B_StoreButton_Bundles.B_StoreButton_Bundles'"},
                       {'key': 'StoreLevelMin', 'value': '170000'}],
            sort_priority=60,
            title="Super Magic Chest",
            description="A Diamond Hero Crystal, 5000 Magic Tickets and 8 items!",
            item_grants=[{'templateId': 'Reagent:Reagent_Hero_Event', 'quantity': 5000},
                         {'templateId': 'Reagent:Reagent_HeroMap_SuperRare', 'quantity': 100},
                         {'templateId': 'Reagent:Reagent_HeroMap_Elemental', 'quantity': 500},
                         {'templateId': 'Reagent:Reagent_SupplyPoints_Elite', 'quantity': 200},
                         {'templateId': 'UpgradePotion:UpgradeHealthMajor', 'quantity': 50},
                         {'templateId': 'UpgradePotion:UpgradeStrengthMajor', 'quantity': 50},
                         {'templateId': 'UpgradePotion:UpgradeMana', 'quantity': 10}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="590CF0040E92446A844487CB525E6670",
            dev_name="StorefrontMtx.L960000.MtxGift.108",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '9D90D9D043CA0596F6266EB2C3DC9C64',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '2502E968436E5D2DF78BB1A266AA3C5B',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '960000'}],
            sort_priority=1000,
            title="Support Gift 107",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="0CF30DAE0AAD4F5C84E77B4CE11CC8C3",
            dev_name="StorefrontLevel.L130000.LevelUpChest.03",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 5000, 'dynamicRegularPrice': -1,
                 'finalPrice': 5000, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 5000}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '62A30DED4F2E3F8863CE0DB8B97125D5',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': 'FE6C666D41BCDBA0704ED29B8A1FD492',
                           'minQuantity': 1}],
            meta_info=[{'key': 'ButtonClassPath',
                        'value': "WidgetBlueprint'/Game/UMG/Store/B_StoreButton_Bundles.B_StoreButton_Bundles'"},
                       {'key': 'StoreLevelMin', 'value': '130000'}],
            sort_priority=60,
            title="Super Magic Chest",
            description="A Diamond Hero Crystal, 5000 Magic Tickets and 8 items!",
            item_grants=[{'templateId': 'Reagent:Reagent_Hero_Event', 'quantity': 5000},
                         {'templateId': 'Reagent:Reagent_HeroMap_SuperRare', 'quantity': 100},
                         {'templateId': 'Reagent:Reagent_HeroMap_Elemental', 'quantity': 500},
                         {'templateId': 'Reagent:Reagent_SupplyPoints_Elite', 'quantity': 200},
                         {'templateId': 'UpgradePotion:UpgradeHealthMajor', 'quantity': 50},
                         {'templateId': 'UpgradePotion:UpgradeStrengthMajor', 'quantity': 50},
                         {'templateId': 'UpgradePotion:UpgradeMana', 'quantity': 10}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="3335B52DB36C420E9C895A68B3BD022B",
            dev_name="StorefrontMtx.L680000.MtxGift.74",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': 'E053B31F4111B3AF758685885D5CBED9',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '156018564EE5F273B9CED8AA57AEDC62',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '680000'}],
            sort_priority=1000,
            title="Support Gift 79",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="D2D01CE41D784BEC9D290052AAEBE0F4",
            dev_name="StorefrontMtx.L750000.MtxGift.83",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '5F6B767A47A95247E35E80AE9A702A6E',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '95D438054A0CFA5ECC5EF582961AD9FC',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '750000'}],
            sort_priority=1000,
            title="Support Gift 86",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="FB6B59AF4C220FECC40AB191117F097E",
            dev_name="Fire Hero",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'GameItem', 'currencySubType': 'Voucher:Voucher_HeroSilver_Fire', 'regularPrice': 1,
                 'dynamicRegularPrice': -1, 'finalPrice': 1, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                 'basePrice': 1}],
            meta_info=[{'key': 'AffordOnly', 'value': 'true'}, {'key': 'ButtonClassPath',
                                                                'value': "WidgetBlueprint'/Game/UMG/Store"
                                                                         "/B_StoreButton_Hero.B_StoreButton_Hero'"},
                       {'key': 'type', 'value': 'fire'}, {'key': 'AutoRedeem', 'value': 'false'}],
            sort_priority=101,
            title="Fire Hero",
            description="Summon a hero to join your team!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="39F07E3E516543E0BCBC9A859AC9702A",
            dev_name="StorefrontMtx.L480000.MtxGift.49",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': 'DA4EB1D64213B51C77AE75B0DFC453EF',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '03F40DBD424A80428272648B6B6FDA5B',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '480000'}],
            sort_priority=1000,
            title="Support Gift 59",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="1F0A4B5E9692404FBE92F2782061477C",
            dev_name="StorefrontMtx.L25000.MtxGift.21",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '1DA1BAEC49524F730C07AA9D285CDDB3',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': 'D9467EB349B5955D042B6DB98B0BF2CA',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '25000'}],
            sort_priority=1000,
            title="Support Gift 6",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="D1F92D5C4225429DBC2EE8F02136C6E1",
            dev_name="StorefrontMtx.L820000.MtxGift.91",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '82A8D4B544A9DC38C604F0A54305097C',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': 'AE3B458F433DE9BEF76CFFAFA6E5824B',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '820000'}],
            sort_priority=1000,
            title="Support Gift 93",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="7D8D23C4B1ED4094B4AA3AC08A0FB825",
            dev_name="StorefrontStacked.Page01.ElementalHeroes.385",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 500, 'dynamicRegularPrice': -1,
                 'finalPrice': 500, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 500}],
            daily_limit=1,
            meta_info=[{'key': 'ButtonClassPath',
                        'value': "WidgetBlueprint'/Game/UMG/Store/B_StoreButton_Bundles.B_StoreButton_Bundles'"},
                       {'key': 'Type', 'value': 'ElementalHero'}, {'key': 'HideQuantityRemaining', 'value': 'True'}],
            catalog_group="ElementalHeroes",
            catalog_group_priority=385,
            sort_priority=72,
            title="Elemental Heroes",
            item_grants=[{'templateId': 'Reagent:Reagent_Hero_Event', 'quantity': 500},
                         {'templateId': 'Reagent:Reagent_HeroMap_Elemental', 'quantity': 140},
                         {'templateId': 'Currency:Hammer', 'quantity': 4},
                         {'templateId': 'Reagent:Reagent_Shard_Fire', 'quantity': 2},
                         {'templateId': 'UpgradePotion:UpgradeHealthMinor', 'quantity': 6},
                         {'templateId': 'Currency:Gold', 'quantity': 100000},
                         {'templateId': 'Reagent:Reagent_HeroMap_Elemental', 'quantity': 20}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="C18AE9179A5547F7BCFEBECE59DD3CE2",
            dev_name="StorefrontMtx.L510000.MtxGift.54",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '2BFCE5B9460735E737669585D1895444',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '06EED93D416CC285D8F887BA31411157',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '510000'}],
            sort_priority=1000,
            title="Support Gift 62",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="32277ADF4C9D4C1FA8D9A7334A9AE5A7",
            dev_name="StorefrontLevel.L510000.LevelUpChest.25",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 5000, 'dynamicRegularPrice': -1,
                 'finalPrice': 5000, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 5000}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '90C2A42E4DD0334F1E67DEA8D228B8F0',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '2505AD4D4B9A19FBB46D0B9EBC1EA56C',
                           'minQuantity': 1}],
            meta_info=[{'key': 'ButtonClassPath',
                        'value': "WidgetBlueprint'/Game/UMG/Store/B_StoreButton_Bundles.B_StoreButton_Bundles'"},
                       {'key': 'StoreLevelMin', 'value': '510000'}],
            sort_priority=60,
            title="Super Magic Chest",
            description="A Diamond Hero Crystal, 5000 Magic Tickets and 8 items!",
            item_grants=[{'templateId': 'Reagent:Reagent_Hero_Event', 'quantity': 5000},
                         {'templateId': 'Reagent:Reagent_HeroMap_SuperRare', 'quantity': 100},
                         {'templateId': 'Reagent:Reagent_HeroMap_Elemental', 'quantity': 500},
                         {'templateId': 'Reagent:Reagent_SupplyPoints_Elite', 'quantity': 200},
                         {'templateId': 'UpgradePotion:UpgradeHealthMajor', 'quantity': 50},
                         {'templateId': 'UpgradePotion:UpgradeStrengthMajor', 'quantity': 50},
                         {'templateId': 'UpgradePotion:UpgradeMana', 'quantity': 10}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="6443EFAC8C5F487F8B0783D62C2CB7F1",
            dev_name="StorefrontLevel.L80000.LevelUpChest.30",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 5000, 'dynamicRegularPrice': -1,
                 'finalPrice': 5000, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 5000}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '2CFBBA1041E1576AD0A0B4AC3CDD4DB8',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '1CE9D551409C5DF76678DBBD81B4FDB9',
                           'minQuantity': 1}],
            meta_info=[{'key': 'ButtonClassPath',
                        'value': "WidgetBlueprint'/Game/UMG/Store/B_StoreButton_Bundles.B_StoreButton_Bundles'"},
                       {'key': 'StoreLevelMin', 'value': '80000'}],
            sort_priority=60,
            title="Super Magic Chest",
            description="A Diamond Hero Crystal, 5000 Magic Tickets and 8 items!",
            item_grants=[{'templateId': 'Reagent:Reagent_Hero_Event', 'quantity': 5000},
                         {'templateId': 'Reagent:Reagent_HeroMap_SuperRare', 'quantity': 100},
                         {'templateId': 'Reagent:Reagent_HeroMap_Elemental', 'quantity': 500},
                         {'templateId': 'Reagent:Reagent_SupplyPoints_Elite', 'quantity': 200},
                         {'templateId': 'UpgradePotion:UpgradeHealthMajor', 'quantity': 50},
                         {'templateId': 'UpgradePotion:UpgradeStrengthMajor', 'quantity': 50},
                         {'templateId': 'UpgradePotion:UpgradeMana', 'quantity': 10}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="E7C8F4A5BEF346569914B0911F685243",
            dev_name="StorefrontMtx.L900000.MtxGift.101",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': 'B0DE74BB4B8CE1FE2370A5B60FBBA4EF',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '163B90B54347AA6F1BA40AA087DADF38',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '900000'}],
            sort_priority=1000,
            title="Support Gift 101",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="8B48FD5A28A84BF6ACBF802869C885AA",
            dev_name="StorefrontMtx.L55000.MtxGift.58",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '713EA5E949A65138904884983F430D2F',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': 'E83060694EC9CA80654B84AF64340D5D',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '55000'}],
            sort_priority=1000,
            title="Support Gift 12",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="13086EDC4986EA7550441BB6DDEBC650",
            dev_name="12HR Basic Chest (Silver) - 75",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 100, 'dynamicRegularPrice': -1,
                 'finalPrice': 75, 'saleType': 'AmountOff', 'saleExpiration': '9999-12-31T23:59:59.999Z',
                 'basePrice': 75}],
            daily_limit=1,
            meta_info=[{'key': 'DAILYCHEST', 'value': 'true'}, {'key': 'type', 'value': 'dailylootbox'},
                       {'key': 'AccountLevelMin', 'value': '4'}, {'key': 'ButtonClassPath',
                                                                  'value': "WidgetBlueprint'/Game/UMG/Store"
                                                                           "/B_StoreButton_Bundles_Small"
                                                                           ".B_StoreButton_Bundles_Small'"}],
            catalog_group="Silver Chest",
            catalog_group_priority=1,
            sort_priority=115,
            title="12hr Basic Chest",
            item_grants=[{'templateId': 'Reagent:Reagent_Hero_Event', 'quantity': 100},
                         {'templateId': 'Currency:Hammer', 'quantity': 4}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="257F44392A774BAC99DBC6DB46D00AD3",
            dev_name="StorefrontStacked.Page01.ElementalHeroes.283",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 500, 'dynamicRegularPrice': -1,
                 'finalPrice': 500, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 500}],
            daily_limit=1,
            meta_info=[{'key': 'ButtonClassPath',
                        'value': "WidgetBlueprint'/Game/UMG/Store/B_StoreButton_Bundles.B_StoreButton_Bundles'"},
                       {'key': 'Type', 'value': 'ElementalHero'}, {'key': 'HideQuantityRemaining', 'value': 'True'}],
            catalog_group="ElementalHeroes",
            catalog_group_priority=283,
            sort_priority=72,
            title="Elemental Heroes",
            item_grants=[{'templateId': 'Reagent:Reagent_Hero_Event', 'quantity': 500},
                         {'templateId': 'Reagent:Reagent_HeroMap_Elemental', 'quantity': 140},
                         {'templateId': 'Currency:Hammer', 'quantity': 4},
                         {'templateId': 'Currency:MtxGiveaway', 'quantity': 100},
                         {'templateId': 'Currency:MtxGiveaway', 'quantity': 100},
                         {'templateId': 'Currency:MtxGiveaway', 'quantity': 100},
                         {'templateId': 'Reagent:Reagent_HeroMap_Elemental', 'quantity': 50}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="CB55B1898B9E4C49A5280C544489EDFF",
            dev_name="StorefrontMtx.L420000.MtxGift.42",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '7B18E62F43F3DCDEBF31738AB90E4919',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '217EAEFF478385E11EA0EC8451C8F2BF',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '420000'}],
            sort_priority=1000,
            title="Support Gift 53",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="E6B8C4BC6E2C419B99A40B122846041D",
            dev_name="StorefrontMtx.L580000.MtxGift.62",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': 'B1BF9CB842881A9E2E5D4CABB1F932F5',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '9632B0144E806B1508858E8526C8C7D2',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '580000'}],
            sort_priority=1000,
            title="Support Gift 69",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="84D0111E4E03D3ABF723AAA9E2070047",
            dev_name="Team Slot",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 150, 'dynamicRegularPrice': -1,
                 'finalPrice': 150, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 150}],
            requirements=[{'requirementType': 'DenyOnFulfillment', 'requiredId': '233CFA5B48709E1D65BD5F8FA57EA5DA',
                           'minQuantity': 5}],
            meta_info=[{'key': 'ServiceName', 'value': 'InventoryUpgrade'}, {'key': 'type', 'value': 'teamslot'}],
            sort_priority=19,
            title="+1 Team Slot",
            description="Increases your maximum number of teams by 1 and maximum hero inventory by 5",
            display_asset_path="/Game/UMG/Textures/Icons/AccountUpgradeItems/T_Team_Slots.T_Team_Slots",
            item_grants=[{'templateId': 'Party:Instance', 'quantity': 1},
                         {'templateId': 'StandIn:TeamSlotsUpgrade', 'quantity': 1, 'attributes': {'FakeQuantity': 1}},
                         {'templateId': 'StandIn:InventoryUpgrade', 'quantity': 1, 'attributes': {'FakeQuantity': 5}}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="4AAFA1673E3141ABB0F2AF09714F27E2",
            dev_name="StorefrontMtx.L610000.MtxGift.66",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '99C4CD6341895994F96C418162800C4B',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '4A6141634D3AC5AC701DD0B2F0AD8F9E',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '610000'}],
            sort_priority=1000,
            title="Support Gift 72",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="960FC988A26E413784BC2C14B9B9476C",
            dev_name="StorefrontMtx.L190000.MtxGift.14",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '933C99554A70D66D804FA98829541A99',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '23D6690D45EBBE60E00EFE9563C24B89',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '190000'}],
            sort_priority=1000,
            title="Support Gift 30",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="6FA8142C85A247DC9FC72F31B50640D1",
            dev_name="StorefrontMtx.L660000.MtxGift.72",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': 'FFAE4C824BC126932854A6A3199B1EB8',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '9CBA0101494E26B58A5408872F3C4353',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '660000'}],
            sort_priority=1000,
            title="Support Gift 77",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="AD01C48577C34BACAC8F5F8BA932A9FB",
            dev_name="StorefrontMtx.L940000.MtxGift.105",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '2468A46347C548FE8C4702A77B29CE07',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '4C16D22849A940EFD2805FA3770F4289',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '940000'}],
            sort_priority=1000,
            title="Support Gift 105",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="FEB439F03D9345099C012D82E36875A9",
            dev_name="StorefrontMtx.L260000.MtxGift.23",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '82C167B44E347F8BD9E219832900351C',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '30919EB548919E3CF1BAB6B4BD4819A6',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '260000'}],
            sort_priority=1000,
            title="Support Gift 37",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="D7BAC4E0E44F45259B8537050E4B606B",
            dev_name="StorefrontStacked.Page01.ElementalHeroes.212",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 500, 'dynamicRegularPrice': -1,
                 'finalPrice': 500, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 500}],
            daily_limit=1,
            meta_info=[{'key': 'ButtonClassPath',
                        'value': "WidgetBlueprint'/Game/UMG/Store/B_StoreButton_Bundles.B_StoreButton_Bundles'"},
                       {'key': 'Type', 'value': 'ElementalHero'}, {'key': 'HideQuantityRemaining', 'value': 'True'}],
            catalog_group="ElementalHeroes",
            catalog_group_priority=212,
            sort_priority=72,
            title="Elemental Heroes",
            item_grants=[{'templateId': 'Reagent:Reagent_Hero_Event', 'quantity': 500},
                         {'templateId': 'Reagent:Reagent_HeroMap_Elemental', 'quantity': 140},
                         {'templateId': 'Currency:Hammer', 'quantity': 4},
                         {'templateId': 'Reagent:Reagent_SupplyPoints_BuildingUpgrade', 'quantity': 5},
                         {'templateId': 'Currency:SkillXP', 'quantity': 500},
                         {'templateId': 'Reagent:Reagent_SupplyPoints_Elite', 'quantity': 20},
                         {'templateId': 'Reagent:Reagent_HeroMap_Elemental', 'quantity': 50}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="8588ED0351984C47943B6C15740E2785",
            dev_name="StorefrontMtx.L1000000.MtxGift.04",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '2056F0AF47450E7F5739F6988E4CE902',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '5BCAA5BA43680543482B429D3A2558B5',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '1000000'}],
            sort_priority=1000,
            title="Support Gift 111",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="912DCAF2533047178E59CAAA87474695",
            dev_name="StorefrontMtx.L650000.MtxGift.71",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '75C7E43249236441B9002F8B752C6117',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': 'FFAE4C824BC126932854A6A3199B1EB8',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '650000'}],
            sort_priority=1000,
            title="Support Gift 76",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="BA34F0F54407C1A6C6DE75AEF04555C9",
            dev_name="12HR Basic Chest (Silver) - 50",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 100, 'dynamicRegularPrice': -1,
                 'finalPrice': 50, 'saleType': 'AmountOff', 'saleExpiration': '9999-12-31T23:59:59.999Z',
                 'basePrice': 50}],
            daily_limit=1,
            meta_info=[{'key': 'DAILYCHEST', 'value': 'true'}, {'key': 'type', 'value': 'dailylootbox'},
                       {'key': 'AccountLevelMin', 'value': '4'}, {'key': 'ButtonClassPath',
                                                                  'value': "WidgetBlueprint'/Game/UMG/Store"
                                                                           "/B_StoreButton_Bundles_Small"
                                                                           ".B_StoreButton_Bundles_Small'"}],
            catalog_group="Silver Chest",
            catalog_group_priority=2,
            sort_priority=115,
            title="12hr Basic Chest",
            item_grants=[{'templateId': 'Reagent:Reagent_Hero_Event', 'quantity': 100},
                         {'templateId': 'Currency:Hammer', 'quantity': 4}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="12F2000A4BE70D0E848622A2AB0B4784",
            dev_name="Battle Hero",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Voucher:Voucher_HeroBattle', 'regularPrice': 1,
                     'dynamicRegularPrice': -1, 'finalPrice': 1, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 1}],
            meta_info=[{'key': 'AffordOnly', 'value': 'true'}, {'key': 'ButtonClassPath',
                                                                'value': "WidgetBlueprint'/Game/UMG/Store"
                                                                         "/B_StoreButton_Hero.B_StoreButton_Hero'"},
                       {'key': 'type', 'value': 'battle'}],
            sort_priority=108,
            title="Battle Hero",
            description="Add a powerful hero to your team!",
            item_grants=[{'templateId': 'Character:SpiritWarrior_SR2_Fire_IronMonkey_T04', 'quantity': 1},
                         {'templateId': 'Character:HolyKnight_SR2_Light_Seraph_T05', 'quantity': 1},
                         {'templateId': 'Character:Warrior_SR2_Nature_Behemoth_T05', 'quantity': 1},
                         {'templateId': 'Character:Spellsword_SR2_Dark_DarkGale_T05', 'quantity': 1},
                         {'templateId': 'Character:Ninja_SR2_Fire_DeathBlossom_T05', 'quantity': 1},
                         {'templateId': 'Character:DragonKnight_SR1_Water_DragonForm_T05', 'quantity': 1},
                         {'templateId': 'Character:Mage_SR2_Water_Blizzard_T05', 'quantity': 1},
                         {'templateId': 'Character:Assassin_SR2_Dark_PhantomDash_T05', 'quantity': 1},
                         {'templateId': 'Character:Blademaster_SR2_Water_SpinningEdge_T05', 'quantity': 1},
                         {'templateId': 'Character:Shadowknight_SR2_Fire_Reaver_T05', 'quantity': 1},
                         {'templateId': 'Character:Mage_SR2_Light_Anubis_T04', 'quantity': 1},
                         {'templateId': 'Character:Warmage_SR2_Nature_Earthquake_T05', 'quantity': 1},
                         {'templateId': 'Character:Ninja_SR2_Dark_Zed_T05', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="2A9FE2864271324688238A93EA48350F",
            dev_name="Battle Pass (Recurring)",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'RealMoney', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            monthly_limit=1,
            app_store_id=[
                "",
                "1bb845075f334ecaae7b55e421ab3dea",
                "bb_battlepass",
                "",
                "bb_battlepass",
                "",
                "",
                "",
                "",
                "sam_battlepass",
            ],
            meta_info=[{'key': 'BonusOverride', 'value': '3000'}, {'key': 'ButtonClassPath',
                                                                   'value': "WidgetBlueprint'/Game/UMG/Store"
                                                                            "/B_StoreButton_Battlepass"
                                                                            ".B_StoreButton_Battlepass'"}],
            catalog_group="BattlePass",
            catalog_group_priority=1,
            sort_priority=500,
            title="Battle Pass",
            description="100 Gems every day for 30 days\r\nUnlocks premium Battle Pass rewards",
            display_asset_path="/Game/UMG/Textures/Store/btn_StoreGemBag.btn_StoreGemBag",
        ))
        self.catalog_entries.append(Offer(
            offer_id="4F06CD5B4A764BDAE79A6FA00F4CB161",
            dev_name="Battle Breaker (T1)",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'RealMoney', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            app_store_id=[
                "",
                "11b1aad3c22d4fe58c361b8c913477d6",
                "bb_viptier1_release",
                "",
                "bb_viptier1_release",
                "",
                "",
                "",
                "",
                "sam_viptier1_release",
            ],
            requirements=[{'requirementType': 'DenyOnFulfillment', 'requiredId': 'BE8A7A4F48546D69D0F8DF873120B3E6',
                           'minQuantity': 1}],
            meta_info=[{'key': 'VipLevelMin', 'value': '0'}, {'key': 'AccountLevelMin', 'value': '0'},
                       {'key': 'ButtonClassPath',
                        'value': "WidgetBlueprint'/Game/UMG/Store/B_StoreButton_AccountUpgrade"
                                 ".B_StoreButton_AccountUpgrade'"},
                       {'key': 'VipLevelMax', 'value': '0'}, {'key': 'type', 'value': 'accountupgrade'},
                       {'key': 'InspectItem', 'value': 'Character:Pet_SR1_Cloudpuff_Nature_T05'},
                       {'key': 'PreviewFulfillmentClassPath',
                        'value': "CatalogFulfillment'/Game/Catalog/Fulfillments/AccountUpgrades/Release_VIP_Tier1"
                                 ".Release_VIP_Tier1'"},
                       {'key': 'bShowInGemStore', 'value': 'true'}],
            catalog_group="AccountUpgrades",
            sort_priority=40,
            title="Battle Breaker Collection",
            short_description="A unique pet, free daily chests, more teams, quests, gems, a hero and more!",
            description="<RT.CapsGreen>Chocolate Cloudpuff</> <RT.BasicMed> - A pet that attacks all "
                        "enemies!</>\r\n\r\n<RT.CapsBlue>Includes Permanent Account Upgrades</>\r\n\r\n"
                        "<RT.BasicMed>Free Basic Chests contain 4 Hammers and 100 Magic Tickets</>",
            display_asset_path="/Game/UMG/Textures/Store/btn_StoreGemGoldenChest.btn_StoreGemGoldenChest",
            item_grants=[{'templateId': 'Party:Instance', 'quantity': 3},
                         {'templateId': 'Character:Pet_SR1_Cloudpuff_Nature_T05', 'quantity': 1},
                         {'templateId': 'StandIn:FreeTwiceDailyLootBox', 'quantity': 1},
                         {'templateId': 'StandIn:TeamSlotsUpgrade', 'quantity': 1, 'attributes': {'FakeQuantity': 3}},
                         {'templateId': 'StandIn:InventoryUpgrade', 'quantity': 1, 'attributes': {'FakeQuantity': 15}},
                         {'templateId': 'StandIn:QuestLimit', 'quantity': 1, 'attributes': {'FakeQuantity': 1}},
                         {'templateId': 'Currency:MtxPurchased', 'quantity': 1500},
                         {'templateId': 'Currency:MtxPurchaseBonus', 'quantity': 500},
                         {'templateId': 'Reagent:Reagent_HeroMap_Elemental', 'quantity': 500}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="DD47D093977147099DBDCD8880D6690F",
            dev_name="StorefrontMtx.L140000.MtxGift.08",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '9E833A024D8FD5EAD1C4AD83D739AD24',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': 'B3EC21C9458D51BEB1BA22999A375658',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '140000'}],
            sort_priority=1000,
            title="Support Gift 25",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="0C7081BD42D0497891D134ACF1F121E3",
            dev_name="StorefrontMtx.L270000.MtxGift.24",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '30919EB548919E3CF1BAB6B4BD4819A6',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '6EC4CB2241CDD5FFA61D059F0266A988',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '270000'}],
            sort_priority=1000,
            title="Support Gift 38",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="58667C9294D94098B7E8D47B7B1A2CF2",
            dev_name="StorefrontStacked.Page01.ElementalHeroes.394",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 500, 'dynamicRegularPrice': -1,
                 'finalPrice': 500, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 500}],
            daily_limit=1,
            meta_info=[{'key': 'ButtonClassPath',
                        'value': "WidgetBlueprint'/Game/UMG/Store/B_StoreButton_Bundles.B_StoreButton_Bundles'"},
                       {'key': 'Type', 'value': 'ElementalHero'}, {'key': 'HideQuantityRemaining', 'value': 'True'}],
            catalog_group="ElementalHeroes",
            catalog_group_priority=394,
            sort_priority=72,
            title="Elemental Heroes",
            item_grants=[{'templateId': 'Reagent:Reagent_Hero_Event', 'quantity': 500},
                         {'templateId': 'Reagent:Reagent_HeroMap_Elemental', 'quantity': 140},
                         {'templateId': 'Currency:Hammer', 'quantity': 4},
                         {'templateId': 'Reagent:Reagent_SupplyPoints_BuildingUpgrade', 'quantity': 5},
                         {'templateId': 'Currency:SkillXP', 'quantity': 500},
                         {'templateId': 'Reagent:Reagent_SupplyPoints_Elite', 'quantity': 20},
                         {'templateId': 'Reagent:Reagent_HeroMap_Elemental', 'quantity': 50}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="4D80E4E8AC384F49A12F10A08E139A31",
            dev_name="StorefrontLevel.L430000.LevelUpChest.20",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 5000, 'dynamicRegularPrice': -1,
                 'finalPrice': 5000, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 5000}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': 'D0A62F8540F76D50B172988D31FF1B47',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': 'B949A38F4F1AFF040AF09EA67355F09B',
                           'minQuantity': 1}],
            meta_info=[{'key': 'ButtonClassPath',
                        'value': "WidgetBlueprint'/Game/UMG/Store/B_StoreButton_Bundles.B_StoreButton_Bundles'"},
                       {'key': 'StoreLevelMin', 'value': '430000'}],
            sort_priority=60,
            title="Super Magic Chest",
            description="A Diamond Hero Crystal, 5000 Magic Tickets and 8 items!",
            item_grants=[{'templateId': 'Reagent:Reagent_Hero_Event', 'quantity': 5000},
                         {'templateId': 'Reagent:Reagent_HeroMap_SuperRare', 'quantity': 100},
                         {'templateId': 'Reagent:Reagent_HeroMap_Elemental', 'quantity': 500},
                         {'templateId': 'Reagent:Reagent_SupplyPoints_Elite', 'quantity': 200},
                         {'templateId': 'UpgradePotion:UpgradeHealthMajor', 'quantity': 50},
                         {'templateId': 'UpgradePotion:UpgradeStrengthMajor', 'quantity': 50},
                         {'templateId': 'UpgradePotion:UpgradeMana', 'quantity': 10}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="87B83C340D7E450690D016361886165A",
            dev_name="StorefrontStacked.Page01.ElementalHeroes.455",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 500, 'dynamicRegularPrice': -1,
                 'finalPrice': 500, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 500}],
            daily_limit=1,
            meta_info=[{'key': 'ButtonClassPath',
                        'value': "WidgetBlueprint'/Game/UMG/Store/B_StoreButton_Bundles.B_StoreButton_Bundles'"},
                       {'key': 'Type', 'value': 'ElementalHero'}, {'key': 'HideQuantityRemaining', 'value': 'True'}],
            catalog_group="ElementalHeroes",
            catalog_group_priority=455,
            sort_priority=72,
            title="Elemental Heroes",
            item_grants=[{'templateId': 'Reagent:Reagent_Hero_Event', 'quantity': 500},
                         {'templateId': 'Reagent:Reagent_HeroMap_Elemental', 'quantity': 140},
                         {'templateId': 'Currency:Hammer', 'quantity': 4},
                         {'templateId': 'Reagent:Reagent_HeroMap_SuperRare', 'quantity': 20},
                         {'templateId': 'Reagent:Reagent_Foil', 'quantity': 5},
                         {'templateId': 'Reagent:Reagent_Shared_T02', 'quantity': 50},
                         {'templateId': 'Reagent:Reagent_HeroMap_SuperRare', 'quantity': 4}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="BA86647B407D2BFA34518093A26CB26B",
            dev_name="Heroic Chest (Monthly)",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 1500, 'dynamicRegularPrice': -1,
                 'finalPrice': 1500, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 1500}],
            monthly_limit=1,
            meta_info=[{'key': 'CHEST', 'value': 'true'}, {'key': 'ButtonClassPath',
                                                           'value': "WidgetBlueprint'/Game/UMG/Store"
                                                                    "/B_StoreButton_Bundles.B_StoreButton_Bundles'"},
                       {'key': 'IsGold', 'value': 'true'}, {'key': 'StoreLevelMin', 'value': '1000'}],
            sort_priority=66,
            title="Heroic Chest",
            description="Contains at least 10 hero crystals, including at least 5 silver or better! Available monthly.",
            item_grants=[{'templateId': 'Reagent:Reagent_HeroMap_Elemental', 'quantity': 1500},
                         {'templateId': 'Reagent:Reagent_HeroMap_SuperRare', 'quantity': 10},
                         {'templateId': 'Currency:SkillXP', 'quantity': 500},
                         {'templateId': 'Reagent:Reagent_Shard_Dark', 'quantity': 10},
                         {'templateId': 'Reagent:Reagent_Shard_Fire', 'quantity': 10},
                         {'templateId': 'Reagent:Reagent_Shard_Light', 'quantity': 10},
                         {'templateId': 'Reagent:Reagent_Shard_Nature', 'quantity': 10},
                         {'templateId': 'Reagent:Reagent_Shard_Water', 'quantity': 10},
                         {'templateId': 'Reagent:Reagent_Hero_Event', 'quantity': 1500}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="D2AA14F471D940B3B886850283CFB3D5",
            dev_name="StorefrontMtx.L100000.MtxGift.03",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': 'FF31B86842EFA7A884529E90768AE3D3',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '7696BED040A499C469CBB9BA6A24F830',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '100000'}],
            sort_priority=1000,
            title="Support Gift 21",
            description="Holy Wukong, you're amazing!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="4AD5A49787A24EB381BC2704CFF45D23",
            dev_name="StorefrontMtx.L690000.MtxGift.75",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '156018564EE5F273B9CED8AA57AEDC62',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': 'B133B6DC440D5686E38D49BBE35CD861',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '690000'}],
            sort_priority=1000,
            title="Support Gift 80",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="4115479349B94BE7AB11135FF8542A04",
            dev_name="StorefrontLevel.L190000.LevelUpChest.06",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 5000, 'dynamicRegularPrice': -1,
                 'finalPrice': 5000, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 5000}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '96AF5DA3462C0C7D5C35CD9104F4527B',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': 'D3E0B11D45BF46F1353F309ABC413135',
                           'minQuantity': 1}],
            meta_info=[{'key': 'ButtonClassPath',
                        'value': "WidgetBlueprint'/Game/UMG/Store/B_StoreButton_Bundles.B_StoreButton_Bundles'"},
                       {'key': 'StoreLevelMin', 'value': '190000'}],
            sort_priority=60,
            title="Super Magic Chest",
            description="A Diamond Hero Crystal, 5000 Magic Tickets and 8 items!",
            item_grants=[{'templateId': 'Reagent:Reagent_Hero_Event', 'quantity': 5000},
                         {'templateId': 'Reagent:Reagent_HeroMap_SuperRare', 'quantity': 100},
                         {'templateId': 'Reagent:Reagent_HeroMap_Elemental', 'quantity': 500},
                         {'templateId': 'Reagent:Reagent_SupplyPoints_Elite', 'quantity': 200},
                         {'templateId': 'UpgradePotion:UpgradeHealthMajor', 'quantity': 50},
                         {'templateId': 'UpgradePotion:UpgradeStrengthMajor', 'quantity': 50},
                         {'templateId': 'UpgradePotion:UpgradeMana', 'quantity': 10}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="738EDDCB487527431B5F4EAF8910BDC6",
            dev_name="Forgotten Crystal",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Voucher:Voucher_Hero_Custom_Interceptor',
                     'regularPrice': 1, 'dynamicRegularPrice': -1, 'finalPrice': 1,
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 1}],
            meta_info=[{'key': 'AffordOnly', 'value': 'true'}, {'key': 'ButtonClassPath',
                                                                'value': "WidgetBlueprint'/Game/UMG/Store"
                                                                         "/B_StoreButton_Hero.B_StoreButton_Hero'"},
                       {'key': 'type', 'value': 'Random'}, {'key': 'AutoRedeem', 'value': ''}],
            sort_priority=109,
            title="Forgotten Crystal",
            description="Crack it open to find something special!",
            item_grants=[{'templateId': 'Character:Knight_VR2_Dark_Interceptor_T04', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="948A70086E534831A04D844F6BA480FD",
            dev_name="StorefrontMtx.L50000.MtxGift.52",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '8352FBF848AB462C24BEEFABE6E373C0',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '713EA5E949A65138904884983F430D2F',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '50000'}],
            sort_priority=1000,
            title="Support Gift 11",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="4F9CA9E2D6754B9882A9373921421099",
            dev_name="StorefrontMtx.L210000.MtxGift.17",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '6FC6A72A456C12719AA6488176878E18',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '7E46090E45019AAB5F8BCEBD6BCB33F8',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '210000'}],
            sort_priority=1000,
            title="Support Gift 32",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="211FAECFED4E4D9D9D784A7EC675CD5B",
            dev_name="StorefrontLevel.L330000.LevelUpChest.14",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 5000, 'dynamicRegularPrice': -1,
                 'finalPrice': 5000, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 5000}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': 'E65689DC44393C8ED32C3EA98549786A',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '2F18BCC44E753971B12564A1449C37B5',
                           'minQuantity': 1}],
            meta_info=[{'key': 'ButtonClassPath',
                        'value': "WidgetBlueprint'/Game/UMG/Store/B_StoreButton_Bundles.B_StoreButton_Bundles'"},
                       {'key': 'StoreLevelMin', 'value': '330000'}],
            sort_priority=60,
            title="Super Magic Chest",
            description="A Diamond Hero Crystal, 5000 Magic Tickets and 8 items!",
            item_grants=[{'templateId': 'Reagent:Reagent_Hero_Event', 'quantity': 5000},
                         {'templateId': 'Reagent:Reagent_HeroMap_SuperRare', 'quantity': 100},
                         {'templateId': 'Reagent:Reagent_HeroMap_Elemental', 'quantity': 500},
                         {'templateId': 'Reagent:Reagent_SupplyPoints_Elite', 'quantity': 200},
                         {'templateId': 'UpgradePotion:UpgradeHealthMajor', 'quantity': 50},
                         {'templateId': 'UpgradePotion:UpgradeStrengthMajor', 'quantity': 50},
                         {'templateId': 'UpgradePotion:UpgradeMana', 'quantity': 10}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="B022D1E267054BFF9DCF24818AD903EC",
            dev_name="StorefrontMtx.L85000.MtxGift.94",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': 'A53DFF334DBCB6079E9D1A9AB22F902C',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': 'E462EAA14B27F738FAC2B6B8428DD2FA',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '85000'}],
            sort_priority=1000,
            title="Support Gift 18",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="70355DD2040E4BA28092B4CAD3845F42",
            dev_name="StorefrontMtx.L710000.MtxGift.78",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '47201DAA4E39ECA176CD35AA4CF9A699',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '4F5DC10D401646573926DCA4714C2832',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '710000'}],
            sort_priority=1000,
            title="Support Gift 82",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="ADABB65340E1355361F29B95C23C808A",
            dev_name="Magic Tickets (Weekly)",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 600, 'dynamicRegularPrice': -1,
                 'finalPrice': 600, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 600}],
            weekly_limit=1,
            meta_info=[{'key': 'CHEST', 'value': 'true'}, {'key': 'ButtonClassPath',
                                                           'value': "WidgetBlueprint'/Game/UMG/Store"
                                                                    "/B_StoreButton_Bundles.B_StoreButton_Bundles'"},
                       {'key': 'IsGold', 'value': 'true'}, {'key': 'StoreLevelMin', 'value': '10000'}],
            sort_priority=64,
            title="Weekly Tickets",
            description="Magic Tickets available weekly.",
            item_grants=[{'templateId': 'Reagent:Reagent_Hero_Event', 'quantity': 2000},
                         {'templateId': 'Currency:SkillXP', 'quantity': 1000},
                         {'templateId': 'Reagent:Reagent_Shard_Dark', 'quantity': 3},
                         {'templateId': 'Reagent:Reagent_Shard_Fire', 'quantity': 3},
                         {'templateId': 'Reagent:Reagent_Shard_Light', 'quantity': 3},
                         {'templateId': 'Reagent:Reagent_Shard_Nature', 'quantity': 3},
                         {'templateId': 'Reagent:Reagent_Shard_Water', 'quantity': 3}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="A6DBCA724BBEAB05DACF89AA9069BAAF",
            dev_name="Factory Crystal",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Voucher:Voucher_Hero_Workshop', 'regularPrice': 1,
                     'dynamicRegularPrice': -1, 'finalPrice': 1, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 1}],
            meta_info=[{'key': 'AffordOnly', 'value': 'true'}, {'key': 'ButtonClassPath',
                                                                'value': "WidgetBlueprint'/Game/UMG/Store"
                                                                         "/B_StoreButton_Hero.B_StoreButton_Hero'"},
                       {'key': 'type', 'value': 'bronze'}],
            sort_priority=99,
            title="Factory Crystal",
            description="Summon a hero to join your team!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="21A1EB7D8107434B9CFC565C272CB81C",
            dev_name="StorefrontMtx.L720000.MtxGift.79",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '4F5DC10D401646573926DCA4714C2832',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '6C731B18416AC27CC6F29CBD0FC2CB8A',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '720000'}],
            sort_priority=1000,
            title="Support Gift 83",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="DB541806BB6C472E8752D4736615F32B",
            dev_name="StorefrontMtx.L810000.MtxGift.90",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '26D8C467410A6F8B2D0216B98EC18F0B',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '82A8D4B544A9DC38C604F0A54305097C',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '810000'}],
            sort_priority=1000,
            title="Support Gift 92",
            description="Thank you for your support!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="17D807BC774545BA809D43F0CC8ABF7C",
            dev_name="StorefrontStacked.Page01.ElementalHeroes.252",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 500, 'dynamicRegularPrice': -1,
                 'finalPrice': 500, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 500}],
            daily_limit=1,
            meta_info=[{'key': 'ButtonClassPath',
                        'value': "WidgetBlueprint'/Game/UMG/Store/B_StoreButton_Bundles.B_StoreButton_Bundles'"},
                       {'key': 'Type', 'value': 'ElementalHero'}, {'key': 'HideQuantityRemaining', 'value': 'True'}],
            catalog_group="ElementalHeroes",
            catalog_group_priority=252,
            sort_priority=72,
            title="Elemental Heroes",
            item_grants=[{'templateId': 'Reagent:Reagent_Hero_Event', 'quantity': 500},
                         {'templateId': 'Reagent:Reagent_HeroMap_Elemental', 'quantity': 140},
                         {'templateId': 'Currency:Hammer', 'quantity': 4},
                         {'templateId': 'UpgradePotion:UpgradeStrengthMinor', 'quantity': 20},
                         {'templateId': 'TreasureMap:TM_MapResource', 'quantity': 10},
                         {'templateId': 'Reagent:Reagent_Shard_Fire', 'quantity': 1},
                         {'templateId': 'Currency:Hammer', 'quantity': 3}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="0B78AE2326EE49E1833C0E808660DE46",
            dev_name="StorefrontMtx.L250000.MtxGift.22",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': 'DABF7ABF421751F780FC11BBDFD39273',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '82C167B44E347F8BD9E219832900351C',
                           'minQuantity': 1}],
            meta_info=[{'key': 'MtxLevelMin', 'value': '250000'}],
            sort_priority=1000,
            title="Support Gift 36",
            description="Thank you for your support!",
        ))

    @classmethod
    async def init_storefront(cls) -> Self:
        """
        Initialise the Featured storefront
        :return: The initialised Featured storefront class
        """
        self: Featured = cls()
        self.name = "Featured"
        self.catalog_entries = []
        return self


class SecretShop(Storefront):
    """
    Class based system to handle the SecretShop storefront for the storefront catalog service
    """

    def __init__(self) -> None:
        """
        Initialise the SecretShop storefront class.
        This will setup the variables for the SecretShop storefront
        """
        super().__init__()

    async def update_storefront(self) -> None:
        """
        Update the storefront for the SecretShop storefront class with the latest data
        This rotation never changed
        :return: None
        """
        return None

    @classmethod
    async def init_storefront(cls) -> Self:
        """
        Initialise the SecretShop storefront
        :return: The initialised SecretShop storefront class
        """
        self: SecretShop = cls()
        self.name = "SecretShop"
        self.catalog_entries = []
        return self


class MagicTicket(Storefront):
    """
    Class based system to handle the MagicTicket storefront for the storefront catalog service
    """

    def __init__(self) -> None:
        """
        Initialise the MagicTicket storefront class.
        This will setup the variables for the MagicTicket storefront
        """
        super().__init__()

    async def update_storefront(self) -> None:
        """
        Update the storefront for the MagicTicket storefront class with the latest data
        This rotation never changed
        :return: None
        """
        return None

    @classmethod
    async def init_storefront(cls) -> Self:
        """
        Initialise the MagicTicket storefront
        :return: The initialised MagicTicket storefront class
        """
        self: MagicTicket = cls()
        self.name = "MagicTicket"
        self.catalog_entries = []
        return self


class Services(Storefront):
    """
    Class based system to handle the Services storefront for the storefront catalog service
    """

    def __init__(self) -> None:
        """
        Initialise the Services storefront class.
        This will setup the variables for the Services storefront
        """
        super().__init__()

    async def update_storefront(self) -> None:
        """
        Update the storefront for the Services storefront class with the latest data
        This rotation never changed
        :return: None
        """
        # temporary implementation
        self.catalog_entries.append(Offer(
            offer_id="17E5A9AD45B206FE96CCCC9412334C52",
            dev_name="EnergyRefill 2",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 50, 'dynamicRegularPrice': -1,
                 'finalPrice': 50, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 50}],
            daily_limit=1,
            meta_info=[{'key': 'ServiceName', 'value': 'EnergyRefill'}],
            catalog_group="EnergyRefill",
            catalog_group_priority=5,
        ))
        self.catalog_entries.append(Offer(
            offer_id="99F1C1E54A13B8C6B89E8D98E65676FF",
            dev_name="FriendLimitIncrease",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 100, 'dynamicRegularPrice': -1,
                 'finalPrice': 100, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 100}],
            meta_info=[{'key': 'ServiceName', 'value': 'FriendsListIncrease'}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="F827239E4C5947CBF1F1C1ADDE3C7AE1",
            dev_name="Respec Account Reward Perks Monthly Discount",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 25, 'dynamicRegularPrice': -1,
                 'finalPrice': 0, 'saleType': 'AmountOff', 'saleExpiration': '9999-12-31T23:59:59.999Z',
                 'basePrice': 0}],
            monthly_limit=1,
            meta_info=[{'key': 'ServiceName', 'value': 'PerkReset'}],
            catalog_group="Respec",
            catalog_group_priority=999,
        ))
        self.catalog_entries.append(Offer(
            offer_id="7458C6424BE7E47690D51296E48779F8",
            dev_name="EnergyRefill 5",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 150, 'dynamicRegularPrice': -1,
                 'finalPrice': 150, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 150}],
            daily_limit=5,
            meta_info=[{'key': 'ServiceName', 'value': 'EnergyRefill'}],
            catalog_group="EnergyRefill",
            catalog_group_priority=2,
        ))
        self.catalog_entries.append(Offer(
            offer_id="63C49DB84063166931C697BEE8B9B760",
            dev_name="Market Page 2",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 50, 'dynamicRegularPrice': -1,
                 'finalPrice': 50, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 50}],
            meta_info=[{'key': 'ServiceName', 'value': 'MarketRefresh:0'}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="2774D5334FCAEDB2D1FF0AA795B90335",
            dev_name="EnergyRefill 4",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 100, 'dynamicRegularPrice': -1,
                 'finalPrice': 100, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 100}],
            daily_limit=5,
            meta_info=[{'key': 'ServiceName', 'value': 'EnergyRefill'}],
            catalog_group="EnergyRefill",
            catalog_group_priority=3,
        ))
        self.catalog_entries.append(Offer(
            offer_id="0AC74A144F231B56B2CD149D688A3B60",
            dev_name="SecretShop Page 2",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 100, 'dynamicRegularPrice': -1,
                 'finalPrice': 100, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 100}],
            meta_info=[{'key': 'ServiceName', 'value': 'SecretShopRefresh:1'}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="2ED72F49457A0AF78377308A8086F63C",
            dev_name="SecretShop Page 1 - FREE",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            meta_info=[{'key': 'ServiceName', 'value': 'SecretShopRefresh:0'}, {'key': 'VipLevelMin', 'value': '3'}],
            catalog_group="SecretShopP1",
            catalog_group_priority=10,
        ))
        self.catalog_entries.append(Offer(
            offer_id="0A36979A4B20A28E20ACEC8924F9724D",
            dev_name="SecretShop Page 1",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 100, 'dynamicRegularPrice': -1,
                 'finalPrice': 100, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 100}],
            meta_info=[{'key': 'ServiceName', 'value': 'SecretShopRefresh:0'}],
            catalog_group="SecretShopP1",
        ))
        self.catalog_entries.append(Offer(
            offer_id="150BAC374E7A2C4635F41F850FEBB9E2",
            dev_name="EnergyRefill 3",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 75, 'dynamicRegularPrice': -1,
                 'finalPrice': 75, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 75}],
            daily_limit=1,
            meta_info=[{'key': 'ServiceName', 'value': 'EnergyRefill'}],
            catalog_group="EnergyRefill",
            catalog_group_priority=4,
        ))
        self.catalog_entries.append(Offer(
            offer_id="F1DEEED84A1577DB97EA8C8D0E55D3E0",
            dev_name="EnergyRefill 6",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 200, 'dynamicRegularPrice': -1,
                 'finalPrice': 200, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 200}],
            daily_limit=7,
            meta_info=[{'key': 'ServiceName', 'value': 'EnergyRefill'}],
            catalog_group="EnergyRefill",
            catalog_group_priority=1,
        ))
        self.catalog_entries.append(Offer(
            offer_id="DAAF98114D3B28BFAD4E4D9D73B8070D",
            dev_name="SecretShop Page 3",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 200, 'dynamicRegularPrice': -1,
                 'finalPrice': 200, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 200}],
            meta_info=[{'key': 'ServiceName', 'value': 'SecretShopRefresh:2'}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="942F8072452726BC0EADC0BB4F9127B9",
            dev_name="GameContinue",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 40, 'dynamicRegularPrice': -1,
                 'finalPrice': 40, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 40}],
            meta_info=[{'key': 'ServiceName', 'value': 'GameContinue'}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="13DA45224BB94323B35251AF8DC1CFE7",
            dev_name="EnergyRefill 1",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 0, 'dynamicRegularPrice': -1,
                     'finalPrice': 0, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            meta_info=[{'key': 'ServiceName', 'value': 'EnergyRefill'}],
            catalog_group="EnergyRefill",
            catalog_group_priority=6,
        ))
        self.catalog_entries.append(Offer(
            offer_id="CB2A2D9B42605E706C93F69EB9CBB079",
            dev_name="Market Page 3",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 100, 'dynamicRegularPrice': -1,
                 'finalPrice': 100, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 100}],
            meta_info=[{'key': 'ServiceName', 'value': 'MarketRefresh:1'}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="A8D2354E4AE98209AEF8B5B26F0E8FE1",
            dev_name="Respec Account Reward Perks Unrestricted",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 25, 'dynamicRegularPrice': -1,
                 'finalPrice': 25, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 25}],
            meta_info=[{'key': 'ServiceName', 'value': 'PerkReset'}],
            catalog_group="Respec",
        ))
        self.catalog_entries.append(Offer(
            offer_id="AF44DAA04EFE95AFFFF49BBDC767BFBC",
            dev_name="ResetLaborPool",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 100, 'dynamicRegularPrice': -1,
                 'finalPrice': 100, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 100}],
            meta_info=[{'key': 'ServiceName', 'value': 'ResetLaborPool'}],
        ))

    @classmethod
    async def init_storefront(cls) -> Self:
        """
        Initialise the Services storefront
        :return: The initialised Services storefront class
        """
        self: Services = cls()
        self.name = "Services"
        self.catalog_entries = []
        return self


class Marketplace(Storefront):
    """
    Class based system to handle the Marketplace storefront for the storefront catalog service
    """

    def __init__(self) -> None:
        """
        Initialise the Marketplace storefront class.
        This will setup the variables for the Marketplace storefront
        """
        super().__init__()

    async def update_storefront(self) -> None:
        """
        Update the storefront for the Marketplace storefront class with the latest data
        :return: None
        """
        # temporary implementation
        self.catalog_entries.append(Offer(
            offer_id="EABB0649D0784B589A3936CAD9394E90",
            dev_name="Marketplace.L05.Page01.PowerSource.01",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Currency:Gold', 'regularPrice': 2500,
                     'dynamicRegularPrice': -1, 'finalPrice': 2500, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 2500}],
            daily_limit=10,
            meta_info=[{'key': 'MarketLevel', 'value': '5'}, {'key': 'MaxMarketLevel', 'value': '9'}],
            item_grants=[{'templateId': 'Reagent:Reagent_Shared_T02', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="5C869FEC2EF6493FBFA719BC6D8D6E7F",
            dev_name="Marketplace.L07.Page01.MapFragments.04",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Currency:Gold', 'regularPrice': 20000,
                     'dynamicRegularPrice': -1, 'finalPrice': 20000, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 20000}],
            daily_limit=5,
            meta_info=[{'key': 'MarketLevel', 'value': '7'}, {'key': 'MaxMarketLevel', 'value': '10'}],
            item_grants=[{'templateId': 'TreasureMap:TM_MapResource', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="F55CF5E14C4B4B1EA0971EBC021399AC",
            dev_name="Marketplace.L10.Page01.PowerSource.04",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Currency:Gold', 'regularPrice': 2500,
                     'dynamicRegularPrice': -1, 'finalPrice': 2500, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 2500}],
            daily_limit=15,
            meta_info=[{'key': 'MarketLevel', 'value': '10'}, {'key': 'MaxMarketLevel', 'value': '14'}],
            item_grants=[{'templateId': 'Reagent:Reagent_Shared_T02', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="041AA6191ECA4DFB81DAF2D9D9A21455",
            dev_name="Marketplace.L01.Page1.VIP5.FreeBonus.11",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Currency:Gold', 'regularPrice': 500000,
                     'dynamicRegularPrice': -1, 'finalPrice': 0, 'saleType': 'AmountOff',
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            meta_info=[{'key': 'MarketLevel', 'value': '1'}, {'key': 'VipLevelMin', 'value': '5'}],
            item_grants=[{'templateId': 'TreasureMap:TM_Special_UnderwaterTunnel', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="1AEEA8721EAA4675BD0C27E0E5D0B671",
            dev_name="Marketplace.L03.Page01.MapFragments.01",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Currency:Gold', 'regularPrice': 20000,
                     'dynamicRegularPrice': -1, 'finalPrice': 20000, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 20000}],
            daily_limit=3,
            meta_info=[{'key': 'MarketLevel', 'value': '3'}, {'key': 'MaxMarketLevel', 'value': '6'}],
            item_grants=[{'templateId': 'TreasureMap:TM_MapResource', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="C5C7E1B486234B6187B058C39B593227",
            dev_name="Marketplace.L19.Page01.Misc.10",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Currency:Gold', 'regularPrice': 50000,
                     'dynamicRegularPrice': -1, 'finalPrice': 50000, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 50000}],
            daily_limit=1,
            meta_info=[{'key': 'MarketLevel', 'value': '19'}],
            item_grants=[{'templateId': 'Reagent:Reagent_RXT_Parts_Small', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="81352A762AEF4DF3A135ABDE10F7F8AF",
            dev_name="Marketplace.L08.Page01.Free.41",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Currency:Gold', 'regularPrice': 300000,
                     'dynamicRegularPrice': -1, 'finalPrice': 0, 'saleType': 'AmountOff',
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            meta_info=[{'key': 'MarketLevel', 'value': '8'}],
            item_grants=[{'templateId': 'Reagent:Reagent_Shard_Fire', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="FFDF84C8D20040D9A621BBAD1905E512",
            dev_name="Marketplace.L11.Page01.TreasureMap.01",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Currency:Gold', 'regularPrice': 20000,
                     'dynamicRegularPrice': -1, 'finalPrice': 20000, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 20000}],
            daily_limit=7,
            meta_info=[{'key': 'MarketLevel', 'value': '11'}, {'key': 'MaxMarketLevel', 'value': '15'}],
            item_grants=[{'templateId': 'TreasureMap:TM_MapResource', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="0E8B6DFAF5E24B599CE899BE87AA68E0",
            dev_name="Marketplace.L20.Page01.Free.56",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Currency:Gold', 'regularPrice': 20000,
                     'dynamicRegularPrice': -1, 'finalPrice': 0, 'saleType': 'AmountOff',
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=2,
            meta_info=[{'key': 'MarketLevel', 'value': '20'}],
            item_grants=[{'templateId': 'TreasureMap:TM_MapResource', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="EDD888A58AFB41FC91F8ADD2D6EC0056",
            dev_name="Marketplace.L01.Page01.Free.04",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Currency:Gold', 'regularPrice': 4000,
                     'dynamicRegularPrice': -1, 'finalPrice': 0, 'saleType': 'AmountOff',
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=10,
            meta_info=[{'key': 'MarketLevel', 'value': '1'}],
            item_grants=[{'templateId': 'UpgradePotion:UpgradeStrengthMinor', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="AF93D694E58543EF98B468964274E872",
            dev_name="Marketplace.L06.Page01.Token.04",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Currency:Gold', 'regularPrice': 35000,
                     'dynamicRegularPrice': -1, 'finalPrice': 35000, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 35000}],
            daily_limit=5,
            meta_info=[{'key': 'MarketLevel', 'value': '6'}],
            item_grants=[{'templateId': 'Reagent:Reagent_HeroMap_Elemental', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="6239684CD2BE41B2B0F1B8C6D7D20161",
            dev_name="Marketplace.L16.Page01.TreasureMap.04",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Currency:Gold', 'regularPrice': 20000,
                     'dynamicRegularPrice': -1, 'finalPrice': 20000, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 20000}],
            daily_limit=10,
            meta_info=[{'key': 'MarketLevel', 'value': '16'}],
            item_grants=[{'templateId': 'TreasureMap:TM_MapResource', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="39BD7B473E32484DA911B4FB7457E641",
            dev_name="Marketplace.L04.Page01.MinorElixir.02",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Currency:Gold', 'regularPrice': 4000,
                     'dynamicRegularPrice': -1, 'finalPrice': 4000, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 4000}],
            daily_limit=8,
            meta_info=[{'key': 'MarketLevel', 'value': '4'}],
            item_grants=[{'templateId': 'UpgradePotion:UpgradeHealthMinor', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="13280B37F682412FBA401E92D58EB004",
            dev_name="Marketplace.L13.Page01.MapsMisc.05",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Currency:Gold', 'regularPrice': 75000,
                     'dynamicRegularPrice': -1, 'finalPrice': 75000, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 75000}],
            daily_limit=1,
            meta_info=[{'key': 'MarketLevel', 'value': '13'}],
            item_grants=[{'templateId': 'TreasureMap:TM_Special_GhostShip', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="A23380E9D8FA4416B5788267240CFD81",
            dev_name="Marketplace.L17.Page01.Shard.05",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 200, 'dynamicRegularPrice': -1,
                 'finalPrice': 200, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 200}],
            daily_limit=1,
            meta_info=[{'key': 'MarketLevel', 'value': '17'}],
            item_grants=[{'templateId': 'Reagent:Reagent_Shard_Water', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="EE1F612AAF12423796D37664C6112810",
            dev_name="Marketplace.L18.Page01.Hero.01",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Currency:Gold', 'regularPrice': 300000,
                     'dynamicRegularPrice': -1, 'finalPrice': 300000, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 300000}],
            daily_limit=1,
            meta_info=[{'key': 'MarketLevel', 'value': '18'}],
            item_grants=[{'templateId': 'Reagent:Reagent_HeroMap_Bronze', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="D9BCA86159D5410CBAB6687A9A1DE760",
            dev_name="Marketplace.L12.Page01.Reagent.09",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 200, 'dynamicRegularPrice': -1,
                 'finalPrice': 200, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 200}],
            daily_limit=2,
            meta_info=[{'key': 'MarketLevel', 'value': '12'}],
            item_grants=[{'templateId': 'Reagent:Reagent_Shard_Nature', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="6E0FC91CCB2F45C78D66AF2ACA1A2166",
            dev_name="Marketplace.L15.Page01.PowerSource.07",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Currency:Gold', 'regularPrice': 2500,
                     'dynamicRegularPrice': -1, 'finalPrice': 2500, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 2500}],
            daily_limit=20,
            meta_info=[{'key': 'MarketLevel', 'value': '15'}],
            item_grants=[{'templateId': 'Reagent:Reagent_Shared_T02', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="0F8591634D9742168B7DEDC93BEA50EC",
            dev_name="Marketplace.L02.Page01.XP.01",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Currency:Gold', 'regularPrice': 200,
                     'dynamicRegularPrice': -1, 'finalPrice': 200, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 200}],
            daily_limit=100000,
            meta_info=[{'key': 'MarketLevel', 'value': '2'}],
            title="+100 ",
            item_grants=[{'templateId': 'Currency:HeroXp_Basic', 'quantity': 100}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="907B61B3FE024F15A63065697EC6679D",
            dev_name="Marketplace.L14.Page01.ElixirAll.04",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Currency:Gold', 'regularPrice': 50000,
                     'dynamicRegularPrice': -1, 'finalPrice': 50000, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 50000}],
            daily_limit=3,
            meta_info=[{'key': 'MarketLevel', 'value': '14'}],
            item_grants=[{'templateId': 'UpgradePotion:UpgradeStrengthMajor', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="2C78C3AE58DF4AB39F7922702D5DBD56",
            dev_name="Marketplace.L09.Page01.MajorElixir.03",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Currency:Gold', 'regularPrice': 50000,
                     'dynamicRegularPrice': -1, 'finalPrice': 50000, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 50000}],
            daily_limit=4,
            meta_info=[{'key': 'MarketLevel', 'value': '9'}],
            item_grants=[{'templateId': 'UpgradePotion:UpgradeStrengthMajor', 'quantity': 1}],
        ))

    @classmethod
    async def init_storefront(cls) -> Self:
        """
        Initialise the Marketplace storefront
        :return: The initialised Marketplace storefront class
        """
        self: Marketplace = cls()
        self.name = "Marketplace"
        self.catalog_entries = []
        return self


class MarketplacePage3(Storefront):
    """
    Class based system to handle the MarketplacePage3 storefront for the storefront catalog service
    """

    def __init__(self) -> None:
        """
        Initialise the MarketplacePage3 storefront class.
        This will setup the variables for the MarketplacePage3 storefront
        """
        super().__init__()

    async def update_storefront(self) -> None:
        """
        Update the storefront for the MarketplacePage3 storefront class with the latest data
        :return: None
        """
        # temporary implementation
        self.catalog_entries.append(Offer(
            offer_id="B078B74487B843CBA1CA78BF47D11663",
            dev_name="Marketplace.L02.Page03.XP.03",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Currency:Gold', 'regularPrice': 200,
                     'dynamicRegularPrice': -1, 'finalPrice': 200, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 200}],
            daily_limit=100000,
            meta_info=[{'key': 'MarketLevel', 'value': '2'}],
            title="+100 ",
            item_grants=[{'templateId': 'Currency:HeroXp_Basic', 'quantity': 100}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="3A3C486F14E5478B826BE2D8C98FB03E",
            dev_name="Marketplace.L09.Page03.MajorElixir.09",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Currency:Gold', 'regularPrice': 50000,
                     'dynamicRegularPrice': -1, 'finalPrice': 50000, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 50000}],
            daily_limit=4,
            meta_info=[{'key': 'MarketLevel', 'value': '9'}],
            item_grants=[{'templateId': 'UpgradePotion:UpgradeHealthMajor', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="F9EBEC41A0CB4D7CBA4DF497C1F350DC",
            dev_name="Marketplace.L05.Page03.PowerSource.03",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Currency:Gold', 'regularPrice': 2500,
                     'dynamicRegularPrice': -1, 'finalPrice': 2500, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 2500}],
            daily_limit=10,
            meta_info=[{'key': 'MarketLevel', 'value': '5'}, {'key': 'MaxMarketLevel', 'value': '9'}],
            item_grants=[{'templateId': 'Reagent:Reagent_Shared_T02', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="2AEFDF81DAAF449DA3B6114547C5FD4B",
            dev_name="Marketplace.L15.Page03.PowerSource.09",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Currency:Gold', 'regularPrice': 2500,
                     'dynamicRegularPrice': -1, 'finalPrice': 2500, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 2500}],
            daily_limit=20,
            meta_info=[{'key': 'MarketLevel', 'value': '15'}],
            item_grants=[{'templateId': 'Reagent:Reagent_Shared_T02', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="33690248A5A9443ABB6CB9FD44AA7093",
            dev_name="Marketplace.L08.Page03.Free.30",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Currency:Gold', 'regularPrice': 50000,
                     'dynamicRegularPrice': -1, 'finalPrice': 0, 'saleType': 'AmountOff',
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=3,
            meta_info=[{'key': 'MarketLevel', 'value': '8'}],
            item_grants=[{'templateId': 'UpgradePotion:UpgradeHealthMajor', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="B6B8AF20474E43679B8A397660ACD4F4",
            dev_name="Marketplace.L03.Page03.MapFragments.03",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Currency:Gold', 'regularPrice': 20000,
                     'dynamicRegularPrice': -1, 'finalPrice': 20000, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 20000}],
            daily_limit=3,
            meta_info=[{'key': 'MarketLevel', 'value': '3'}, {'key': 'MaxMarketLevel', 'value': '6'}],
            item_grants=[{'templateId': 'TreasureMap:TM_MapResource', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="D6FAE32C32E4461BAE8BD1C7A26A8B04",
            dev_name="Marketplace.L14.Page03.ElixirAll.15",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Currency:Gold', 'regularPrice': 4000,
                     'dynamicRegularPrice': -1, 'finalPrice': 4000, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 4000}],
            daily_limit=8,
            meta_info=[{'key': 'MarketLevel', 'value': '14'}],
            item_grants=[{'templateId': 'UpgradePotion:UpgradeStrengthMinor', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="E703B5D01BA64A739523418E93F91F29",
            dev_name="Marketplace.L20.Page03.Free.128",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Currency:Gold', 'regularPrice': 50000,
                     'dynamicRegularPrice': -1, 'finalPrice': 0, 'saleType': 'AmountOff',
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=3,
            meta_info=[{'key': 'MarketLevel', 'value': '20'}],
            item_grants=[{'templateId': 'Token:TK_HolyKnight_VR1_Water_Flood_T04', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="F689CCDD95084E7D85C7E60D71952488",
            dev_name="Marketplace.L04.Page03.MinorElixir.12",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Currency:Gold', 'regularPrice': 4000,
                     'dynamicRegularPrice': -1, 'finalPrice': 4000, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 4000}],
            daily_limit=8,
            meta_info=[{'key': 'MarketLevel', 'value': '4'}],
            item_grants=[{'templateId': 'UpgradePotion:UpgradeStrengthMinor', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="0DF8DDAA584C446FAC782412957C1317",
            dev_name="Marketplace.L10.Page03.PowerSource.06",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Currency:Gold', 'regularPrice': 2500,
                     'dynamicRegularPrice': -1, 'finalPrice': 2500, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 2500}],
            daily_limit=15,
            meta_info=[{'key': 'MarketLevel', 'value': '10'}, {'key': 'MaxMarketLevel', 'value': '14'}],
            item_grants=[{'templateId': 'Reagent:Reagent_Shared_T02', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="C75D93889BAA461E81FD953F45EC7470",
            dev_name="Marketplace.L17.Page03.Shard.29",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 200, 'dynamicRegularPrice': -1,
                 'finalPrice': 200, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 200}],
            daily_limit=1,
            meta_info=[{'key': 'MarketLevel', 'value': '17'}],
            item_grants=[{'templateId': 'Reagent:Reagent_Shard_Dark', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="A66B3964E34440CC95D808376AA43571",
            dev_name="Marketplace.L18.Page03.Hero.09",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Currency:Gold', 'regularPrice': 300000,
                     'dynamicRegularPrice': -1, 'finalPrice': 300000, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 300000}],
            daily_limit=1,
            meta_info=[{'key': 'MarketLevel', 'value': '18'}],
            item_grants=[{'templateId': 'Reagent:Reagent_HeroMap_Bronze', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="0915073C157343C6A3FA71358627B429",
            dev_name="Marketplace.L06.Page03.Token.18",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Currency:Gold', 'regularPrice': 35000,
                     'dynamicRegularPrice': -1, 'finalPrice': 35000, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 35000}],
            daily_limit=5,
            meta_info=[{'key': 'MarketLevel', 'value': '6'}],
            item_grants=[{'templateId': 'Reagent:Reagent_HeroMap_Elemental', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="E3A5A5D4745F4931A9648ECDCAAE5FD9",
            dev_name="Marketplace.L01.Page3.VIP5.FreeBonus.84",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Currency:Gold', 'regularPrice': 50000,
                     'dynamicRegularPrice': -1, 'finalPrice': 0, 'saleType': 'AmountOff',
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=3,
            meta_info=[{'key': 'MarketLevel', 'value': '1'}, {'key': 'VipLevelMin', 'value': '5'}],
            item_grants=[{'templateId': 'Token:TK_SpiritWarrior_VR1_Fire_BlazingPalm_T04', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="0AD5FA6EB6FC48DC8FC348B0DF76A359",
            dev_name="Marketplace.L13.Page03.MapsMisc.29",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 50, 'dynamicRegularPrice': -1,
                 'finalPrice': 50, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 50}],
            daily_limit=2,
            meta_info=[{'key': 'MarketLevel', 'value': '13'}],
            item_grants=[{'templateId': 'TreasureMap:TM_Special_GhostShip', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="3646C35690D942EE9F1DBD219C0E88E4",
            dev_name="Marketplace.L07.Page03.MapFragments.09",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 10, 'dynamicRegularPrice': -1,
                 'finalPrice': 10, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 10}],
            daily_limit=7,
            meta_info=[{'key': 'MarketLevel', 'value': '7'}, {'key': 'MaxMarketLevel', 'value': '10'}],
            item_grants=[{'templateId': 'TreasureMap:TM_MapResource', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="8A20EC4E951F459C945A7C33EC708400",
            dev_name="Marketplace.L16.Page03.TreasureMap.06",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Currency:Gold', 'regularPrice': 20000,
                     'dynamicRegularPrice': -1, 'finalPrice': 20000, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 20000}],
            daily_limit=10,
            meta_info=[{'key': 'MarketLevel', 'value': '16'}],
            item_grants=[{'templateId': 'TreasureMap:TM_MapResource', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="936D0DDB4E1444789C150AC366041A6A",
            dev_name="Marketplace.L01.Page03.Free.15",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Currency:Gold', 'regularPrice': 2500,
                     'dynamicRegularPrice': -1, 'finalPrice': 0, 'saleType': 'AmountOff',
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=10,
            meta_info=[{'key': 'MarketLevel', 'value': '1'}],
            item_grants=[{'templateId': 'Reagent:Reagent_Shared_T02', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="AE0FB5D594884B13AECE50E188E02024",
            dev_name="Marketplace.L12.Page03.Reagent.28",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 200, 'dynamicRegularPrice': -1,
                 'finalPrice': 200, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 200}],
            daily_limit=2,
            meta_info=[{'key': 'MarketLevel', 'value': '12'}],
            item_grants=[{'templateId': 'Reagent:Reagent_Shard_Light', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="5098EC09AE1240E0B258B909443E5944",
            dev_name="Marketplace.L11.Page03.TreasureMap.03",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Currency:Gold', 'regularPrice': 20000,
                     'dynamicRegularPrice': -1, 'finalPrice': 20000, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 20000}],
            daily_limit=7,
            meta_info=[{'key': 'MarketLevel', 'value': '11'}, {'key': 'MaxMarketLevel', 'value': '15'}],
            item_grants=[{'templateId': 'TreasureMap:TM_MapResource', 'quantity': 1}],
        ))

    @classmethod
    async def init_storefront(cls) -> Self:
        """
        Initialise the MarketplacePage3 storefront
        :return: The initialised MarketplacePage3 storefront class
        """
        self: MarketplacePage3 = cls()
        self.name = "MarketplacePage3"
        self.catalog_entries = []
        return self


class MarketplacePage2(Storefront):
    """
    Class based system to handle the MarketplacePage2 storefront for the storefront catalog service
    """

    def __init__(self) -> None:
        """
        Initialise the MarketplacePage2 storefront class.
        This will setup the variables for the MarketplacePage2 storefront
        """
        super().__init__()

    async def update_storefront(self) -> None:
        """
        Update the storefront for the MarketplacePage2 storefront class with the latest data
        :return: None
        """
        # temporary implementation
        self.catalog_entries.append(Offer(
            offer_id="58798C7B134441AAA0D371FBF2CF817B",
            dev_name="Marketplace.L10.Page02.PowerSource.05",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Currency:Gold', 'regularPrice': 2500,
                     'dynamicRegularPrice': -1, 'finalPrice': 2500, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 2500}],
            daily_limit=15,
            meta_info=[{'key': 'MarketLevel', 'value': '10'}, {'key': 'MaxMarketLevel', 'value': '14'}],
            item_grants=[{'templateId': 'Reagent:Reagent_Shared_T02', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="519B321DE41C46039A8FE1FE7ABA266A",
            dev_name="Marketplace.L16.Page02.TreasureMap.05",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Currency:Gold', 'regularPrice': 20000,
                     'dynamicRegularPrice': -1, 'finalPrice': 20000, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 20000}],
            daily_limit=10,
            meta_info=[{'key': 'MarketLevel', 'value': '16'}],
            item_grants=[{'templateId': 'TreasureMap:TM_MapResource', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="AD54252342DA49A790FBAA13A957453E",
            dev_name="Marketplace.L20.Page02.Free.102",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Currency:Gold', 'regularPrice': 500000,
                     'dynamicRegularPrice': -1, 'finalPrice': 0, 'saleType': 'AmountOff',
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            meta_info=[{'key': 'MarketLevel', 'value': '20'}],
            item_grants=[{'templateId': 'TreasureMap:TM_Special_UnderwaterTunnel', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="A600FB452FBA4D0C8F486E0D94F74AC3",
            dev_name="Marketplace.L17.Page02.Shard.14",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 200, 'dynamicRegularPrice': -1,
                 'finalPrice': 200, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 200}],
            daily_limit=1,
            meta_info=[{'key': 'MarketLevel', 'value': '17'}],
            item_grants=[{'templateId': 'Reagent:Reagent_Shard_Nature', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="5D6CCF79A7804AE4ABAD7089C5E4F6DE",
            dev_name="Marketplace.L15.Page02.PowerSource.08",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Currency:Gold', 'regularPrice': 2500,
                     'dynamicRegularPrice': -1, 'finalPrice': 2500, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 2500}],
            daily_limit=20,
            meta_info=[{'key': 'MarketLevel', 'value': '15'}],
            item_grants=[{'templateId': 'Reagent:Reagent_Shared_T02', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="7FA05AFC2E6D47408CECED87FE65885A",
            dev_name="Marketplace.L11.Page02.TreasureMap.02",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Currency:Gold', 'regularPrice': 20000,
                     'dynamicRegularPrice': -1, 'finalPrice': 20000, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 20000}],
            daily_limit=7,
            meta_info=[{'key': 'MarketLevel', 'value': '11'}, {'key': 'MaxMarketLevel', 'value': '15'}],
            item_grants=[{'templateId': 'TreasureMap:TM_MapResource', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="B58DB4E6621A4CFAB02B51AFF60AA6C8",
            dev_name="Marketplace.L01.Page02.Free.20",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Currency:Gold', 'regularPrice': 20000,
                     'dynamicRegularPrice': -1, 'finalPrice': 0, 'saleType': 'AmountOff',
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=4,
            meta_info=[{'key': 'MarketLevel', 'value': '1'}],
            item_grants=[{'templateId': 'TreasureMap:TM_MapResource', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="2D611F4EE3754D8B90532258662AD450",
            dev_name="Marketplace.L12.Page02.Reagent.17",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'MtxCurrency', 'currencySubType': '', 'regularPrice': 200, 'dynamicRegularPrice': -1,
                 'finalPrice': 200, 'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 200}],
            daily_limit=2,
            meta_info=[{'key': 'MarketLevel', 'value': '12'}],
            item_grants=[{'templateId': 'Reagent:Reagent_Shard_Fire', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="941D2080864C413E82C475BDE3AB9D4B",
            dev_name="Marketplace.L18.Page02.Hero.05",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Currency:Gold', 'regularPrice': 300000,
                     'dynamicRegularPrice': -1, 'finalPrice': 300000, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 300000}],
            daily_limit=1,
            meta_info=[{'key': 'MarketLevel', 'value': '18'}],
            item_grants=[{'templateId': 'Reagent:Reagent_HeroMap_Bronze', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="A6DBC56D94404CAFAA3029F60C91278C",
            dev_name="Marketplace.L03.Page02.MapFragments.02",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Currency:Gold', 'regularPrice': 20000,
                     'dynamicRegularPrice': -1, 'finalPrice': 20000, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 20000}],
            daily_limit=3,
            meta_info=[{'key': 'MarketLevel', 'value': '3'}, {'key': 'MaxMarketLevel', 'value': '6'}],
            item_grants=[{'templateId': 'TreasureMap:TM_MapResource', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="49CB7EDCCB824D14A3985616EB4F2AD6",
            dev_name="Marketplace.L04.Page02.MinorElixir.07",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Currency:Gold', 'regularPrice': 4000,
                     'dynamicRegularPrice': -1, 'finalPrice': 4000, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 4000}],
            daily_limit=4,
            meta_info=[{'key': 'MarketLevel', 'value': '4'}],
            item_grants=[{'templateId': 'UpgradePotion:UpgradeStrengthMinor', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="C0622CF3FAFA4BB683164CC3D04C6C90",
            dev_name="Marketplace.L06.Page02.Token.11",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Currency:Gold', 'regularPrice': 35000,
                     'dynamicRegularPrice': -1, 'finalPrice': 35000, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 35000}],
            daily_limit=5,
            meta_info=[{'key': 'MarketLevel', 'value': '6'}],
            item_grants=[{'templateId': 'Reagent:Reagent_HeroMap_Elemental', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="6EE2C458BD5E4735BEDEA9E32F3CA110",
            dev_name="Marketplace.L09.Page02.MajorElixir.06",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Currency:Gold', 'regularPrice': 50000,
                     'dynamicRegularPrice': -1, 'finalPrice': 50000, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 50000}],
            daily_limit=8,
            meta_info=[{'key': 'MarketLevel', 'value': '9'}],
            item_grants=[{'templateId': 'UpgradePotion:UpgradeHealthMajor', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="CAABCC7003D94EF89055B7FA43B41A10",
            dev_name="Marketplace.L14.Page02.ElixirAll.10",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Currency:Gold', 'regularPrice': 4000,
                     'dynamicRegularPrice': -1, 'finalPrice': 4000, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 4000}],
            daily_limit=8,
            meta_info=[{'key': 'MarketLevel', 'value': '14'}],
            item_grants=[{'templateId': 'UpgradePotion:UpgradeStrengthMinor', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="A0B2F31FF9CB49168673201F9D47DD6F",
            dev_name="Marketplace.L05.Page02.PowerSource.02",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Currency:Gold', 'regularPrice': 2500,
                     'dynamicRegularPrice': -1, 'finalPrice': 2500, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 2500}],
            daily_limit=10,
            meta_info=[{'key': 'MarketLevel', 'value': '5'}, {'key': 'MaxMarketLevel', 'value': '9'}],
            item_grants=[{'templateId': 'Reagent:Reagent_Shared_T02', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="57E7ABFEFD81485D82627A837A6C04BC",
            dev_name="Marketplace.L02.Page02.XP.02",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Currency:Gold', 'regularPrice': 200,
                     'dynamicRegularPrice': -1, 'finalPrice': 200, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 200}],
            daily_limit=100000,
            meta_info=[{'key': 'MarketLevel', 'value': '2'}],
            title="+100 ",
            item_grants=[{'templateId': 'Currency:HeroXp_Basic', 'quantity': 100}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="76DB6DE5DCDD4B75AE5516C0F8947A97",
            dev_name="Marketplace.L01.Page2.VIP5.FreeBonus.40",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Currency:Gold', 'regularPrice': 20000,
                     'dynamicRegularPrice': -1, 'finalPrice': 0, 'saleType': 'AmountOff',
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=4,
            meta_info=[{'key': 'MarketLevel', 'value': '1'}, {'key': 'VipLevelMin', 'value': '5'}],
            item_grants=[{'templateId': 'TreasureMap:TM_MapResource', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="6CC4B7084D6D4BA7B4047A06FD779C41",
            dev_name="Marketplace.L07.Page02.MapFragments.06",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Currency:Gold', 'regularPrice': 20000,
                     'dynamicRegularPrice': -1, 'finalPrice': 20000, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 20000}],
            daily_limit=5,
            meta_info=[{'key': 'MarketLevel', 'value': '7'}, {'key': 'MaxMarketLevel', 'value': '10'}],
            item_grants=[{'templateId': 'TreasureMap:TM_MapResource', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="BEE599801C434893A007379FC9B7AA49",
            dev_name="Marketplace.L13.Page02.MapsMisc.21",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Currency:Gold', 'regularPrice': 500000,
                     'dynamicRegularPrice': -1, 'finalPrice': 500000, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 500000}],
            daily_limit=1,
            meta_info=[{'key': 'MarketLevel', 'value': '13'}],
            item_grants=[{'templateId': 'TreasureMap:TM_Special_UnderwaterForest', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="043FF5832D904BFB908819797E39FA6C",
            dev_name="Marketplace.L08.Page02.Free.38",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Currency:Gold', 'regularPrice': 20000,
                     'dynamicRegularPrice': -1, 'finalPrice': 0, 'saleType': 'AmountOff',
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=5,
            meta_info=[{'key': 'MarketLevel', 'value': '8'}],
            item_grants=[{'templateId': 'TreasureMap:TM_MapResource', 'quantity': 1}],
        ))

    @classmethod
    async def init_storefront(cls) -> Self:
        """
        Initialise the MarketplacePage2 storefront
        :return: The initialised MarketplacePage2 storefront class
        """
        self: MarketplacePage2 = cls()
        self.name = "MarketplacePage2"
        self.catalog_entries = []
        return self


class Events(Storefront):
    """
    Class based system to handle the Events storefront for the storefront catalog service
    """

    def __init__(self) -> None:
        """
        Initialise the Events storefront class.
        This will setup the variables for the Events storefront
        """
        super().__init__()

    async def update_storefront(self) -> None:
        """
        Update the storefront for the Events storefront class with the latest data
        :return: None
        """
        # temporary implementation
        self.catalog_entries.append(Offer(
            offer_id="118F973449C241E0A3AE5D90BAE43A9B",
            dev_name="Event.Evergreen5.25",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Event_Evergreen5',
                     'regularPrice': 1500, 'dynamicRegularPrice': -1, 'finalPrice': 1500,
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 1500}],
            meta_info=[{'key': 'EventLimit', 'value': '5'}],
            sort_priority=203,
            item_grants=[{'templateId': 'Voucher:Voucher_HeroSilver_Fire', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="2AA18AB9BBCC45D7A38271FC1335C528",
            dev_name="Event.Evergreen5.17",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Event_Evergreen5', 'regularPrice': 20,
                 'dynamicRegularPrice': -1, 'finalPrice': 20, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                 'basePrice': 20}],
            meta_info=[{'key': 'EventLimit', 'value': '50'}],
            sort_priority=186,
            item_grants=[{'templateId': 'UpgradePotion:UpgradeHealthMinor', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="5BA1F2A8139C47B2B2482C2E0971789A",
            dev_name="Event.Evergreen5.09",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Event_Evergreen5',
                     'regularPrice': 3750, 'dynamicRegularPrice': -1, 'finalPrice': 3750,
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 3750}],
            meta_info=[{'key': 'EventLimit', 'value': '10'}],
            sort_priority=194,
            item_grants=[{'templateId': 'Reagent:Reagent_Misc_CeremonialSword', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="F60BF3D2F8514F83B75C24D7ED1DBB7F",
            dev_name="Event.Evergreen5.05",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Event_Evergreen5',
                     'regularPrice': 1000, 'dynamicRegularPrice': -1, 'finalPrice': 1000,
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 1000}],
            meta_info=[{'key': 'EventLimit', 'value': '1'}],
            sort_priority=198,
            item_grants=[{'templateId': 'Currency:Hammer', 'quantity': 35}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="BCD54AA28F954A26A81D1ACF425B731B",
            dev_name="Event.Evergreen5.21",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Event_Evergreen5', 'regularPrice': 500,
                 'dynamicRegularPrice': -1, 'finalPrice': 500, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                 'basePrice': 500}],
            meta_info=[{'key': 'EventLimit', 'value': '10'}],
            sort_priority=182,
            item_grants=[{'templateId': 'UpgradePotion:UpgradeMana', 'quantity': 5}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="70105EB742C14099B8209AECC629A419",
            dev_name="Event.Evergreen5.30",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Event_Evergreen5',
                     'regularPrice': 20000, 'dynamicRegularPrice': -1, 'finalPrice': 20000,
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 20000}],
            meta_info=[{'key': 'EventLimit', 'value': '2'}],
            sort_priority=179,
            item_grants=[{'templateId': 'Reagent:Reagent_Hero_Event', 'quantity': 500}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="4671AC9243F04158BA0A671C47E40357",
            dev_name="Event.Evergreen5.02",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Event_Evergreen5', 'regularPrice': 80,
                 'dynamicRegularPrice': -1, 'finalPrice': 80, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                 'basePrice': 80}],
            meta_info=[{'key': 'EventLimit', 'value': '500'}],
            sort_priority=200,
            item_grants=[{'templateId': 'Currency:MtxGiveaway', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="8A5705927EA848D6BC18BA6024DB082F",
            dev_name="Event.Evergreen5.07",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Event_Evergreen5',
                     'regularPrice': 1000, 'dynamicRegularPrice': -1, 'finalPrice': 1000,
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 1000}],
            meta_info=[{'key': 'EventLimit', 'value': '600'}],
            sort_priority=196,
            item_grants=[{'templateId': 'Reagent:Reagent_SupplyPoints_Elite', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="19826B8037F14BCD92D05E86AD38BAA7",
            dev_name="Event.Evergreen5.15",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Event_Evergreen5',
                     'regularPrice': 2250, 'dynamicRegularPrice': -1, 'finalPrice': 2250,
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 2250}],
            meta_info=[{'key': 'EventLimit', 'value': '50'}],
            sort_priority=188,
            item_grants=[{'templateId': 'Reagent:Reagent_Shard_Fire', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="03476EA74FE84B2D8869B794E9AB13B1",
            dev_name="Event.Evergreen5.23",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Event_Evergreen5',
                     'regularPrice': 1500, 'dynamicRegularPrice': -1, 'finalPrice': 1500,
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 1500}],
            meta_info=[{'key': 'EventLimit', 'value': '5'}],
            sort_priority=201,
            item_grants=[{'templateId': 'Voucher:Voucher_HeroSilver_Water', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="44E4A75E182F44499560B44AC2045E3F",
            dev_name="Event.Evergreen5.29",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Event_Evergreen5', 'regularPrice': 375,
                 'dynamicRegularPrice': -1, 'finalPrice': 375, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                 'basePrice': 375}],
            meta_info=[{'key': 'EventLimit', 'value': '5'}],
            sort_priority=180,
            item_grants=[{'templateId': 'Reagent:Reagent_RXT_Parts_Small', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="B9D624B3EA8B4E65AB8C8D345EBD4160",
            dev_name="Event.Evergreen5.10",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Event_Evergreen5',
                     'regularPrice': 10000, 'dynamicRegularPrice': -1, 'finalPrice': 10000,
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 10000}],
            meta_info=[{'key': 'EventLimit', 'value': '5'}],
            sort_priority=193,
            item_grants=[{'templateId': 'Reagent:Reagent_Misc_CeremonialShield', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="AC3AED5C0D4A45679C717A8291FF3035",
            dev_name="Event.Evergreen5.14",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Event_Evergreen5',
                     'regularPrice': 2250, 'dynamicRegularPrice': -1, 'finalPrice': 2250,
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 2250}],
            meta_info=[{'key': 'EventLimit', 'value': '50'}],
            sort_priority=189,
            item_grants=[{'templateId': 'Reagent:Reagent_Shard_Light', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="21F36F0179DF492AA516F2AEF866FF93",
            dev_name="Event.Evergreen5.28",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Event_Evergreen5',
                     'regularPrice': 20000, 'dynamicRegularPrice': -1, 'finalPrice': 20000,
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 20000}],
            meta_info=[{'key': 'EventLimit', 'value': '10'}],
            sort_priority=175,
            item_grants=[{'templateId': 'Reagent:Reagent_Shared_MysteryGoo', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="2248DBFC177047ED81102FCC05B7E443",
            dev_name="Event.Evergreen5.19",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Event_Evergreen5', 'regularPrice': 250,
                 'dynamicRegularPrice': -1, 'finalPrice': 250, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                 'basePrice': 250}],
            meta_info=[{'key': 'EventLimit', 'value': '50'}],
            sort_priority=184,
            item_grants=[{'templateId': 'UpgradePotion:UpgradeHealthMajor', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="47100E5C59E34A41965723ED4279D169",
            dev_name="Event.Evergreen5.27",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Event_Evergreen5',
                     'regularPrice': 1500, 'dynamicRegularPrice': -1, 'finalPrice': 1500,
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 1500}],
            meta_info=[{'key': 'EventLimit', 'value': '5'}],
            sort_priority=205,
            item_grants=[{'templateId': 'Voucher:Voucher_HeroSilver_Nature', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="2B1912598BDA405398B9BE602DDBAADB",
            dev_name="Event.Evergreen5.18",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Event_Evergreen5', 'regularPrice': 20,
                 'dynamicRegularPrice': -1, 'finalPrice': 20, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                 'basePrice': 20}],
            meta_info=[{'key': 'EventLimit', 'value': '50'}],
            sort_priority=185,
            item_grants=[{'templateId': 'UpgradePotion:UpgradeStrengthMinor', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="694DF940A0B64A57B307C96A8AD01625",
            dev_name="Event.Evergreen5.20",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Event_Evergreen5', 'regularPrice': 250,
                 'dynamicRegularPrice': -1, 'finalPrice': 250, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                 'basePrice': 250}],
            meta_info=[{'key': 'EventLimit', 'value': '50'}],
            sort_priority=183,
            item_grants=[{'templateId': 'UpgradePotion:UpgradeStrengthMajor', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="17D499D6924D457A97D1CCF9D288B560",
            dev_name="Event.Evergreen5.01",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Event_Battlepass4', 'regularPrice': 1,
                 'dynamicRegularPrice': -1, 'finalPrice': 1, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                 'basePrice': 1}],
            meta_info=[{'key': 'EventLimit', 'value': '-1'}],
            sort_priority=1000,
            item_grants=[{'templateId': 'Currency:Gold', 'quantity': 50}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="3447B3D6A72C45808DCBDFAA40D419F2",
            dev_name="Event.Evergreen5.06",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Event_Evergreen5', 'regularPrice': 500,
                 'dynamicRegularPrice': -1, 'finalPrice': 500, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                 'basePrice': 500}],
            meta_info=[{'key': 'EventLimit', 'value': '2'}],
            sort_priority=197,
            item_grants=[{'templateId': 'Currency:Hammer', 'quantity': 15}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="A03EEC2CF7F84562BB5C8DFC590E9A8B",
            dev_name="Event.Evergreen5.32",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Event_Evergreen5',
                     'regularPrice': 5300, 'dynamicRegularPrice': -1, 'finalPrice': 5300,
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 5300}],
            meta_info=[{'key': 'EventLimit', 'value': '2'}],
            sort_priority=177,
            item_grants=[{'templateId': 'Reagent:Reagent_HeroMap_Elemental', 'quantity': 100}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="971D7E24B79346A0BD438C56FFE96EF4",
            dev_name="Event.Evergreen5.26",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Event_Evergreen5',
                     'regularPrice': 1500, 'dynamicRegularPrice': -1, 'finalPrice': 1500,
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 1500}],
            meta_info=[{'key': 'EventLimit', 'value': '5'}],
            sort_priority=204,
            item_grants=[{'templateId': 'Voucher:Voucher_HeroSilver_Light', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="BBC5CF7F162B4A0CAB62E4178FAA5AE4",
            dev_name="Event.Evergreen5.33",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Event_Evergreen5', 'regularPrice': 500,
                 'dynamicRegularPrice': -1, 'finalPrice': 500, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                 'basePrice': 500}],
            meta_info=[{'key': 'EventLimit', 'value': '1'}],
            sort_priority=176,
            item_grants=[{'templateId': 'Ore:Ore_Magicite', 'quantity': 150}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="97D41A20AAA44322B668D34E94C5FD80",
            dev_name="Event.Evergreen5.16",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Event_Evergreen5',
                     'regularPrice': 2250, 'dynamicRegularPrice': -1, 'finalPrice': 2250,
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 2250}],
            meta_info=[{'key': 'EventLimit', 'value': '50'}],
            sort_priority=187,
            item_grants=[{'templateId': 'Reagent:Reagent_Shard_Nature', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="506B6EEDC04049E582A78BDAA3325957",
            dev_name="Event.Evergreen5.12",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Event_Evergreen5',
                     'regularPrice': 2250, 'dynamicRegularPrice': -1, 'finalPrice': 2250,
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 2250}],
            meta_info=[{'key': 'EventLimit', 'value': '50'}],
            sort_priority=191,
            item_grants=[{'templateId': 'Reagent:Reagent_Shard_Water', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="6DEA55F7D6B341B2ADCBEEEF00928B51",
            dev_name="Event.Evergreen5.34",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Event_Evergreen5',
                     'regularPrice': 6000, 'dynamicRegularPrice': -1, 'finalPrice': 6000,
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 6000}],
            meta_info=[{'key': 'EventLimit', 'value': '5'}],
            sort_priority=175,
            item_grants=[{'templateId': 'Reagent:Reagent_Shard_Gear', 'quantity': 2}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="A64379243F464023BC51B53FFE544B33",
            dev_name="Event.Evergreen5.22",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Event_Evergreen5',
                     'regularPrice': 1000, 'dynamicRegularPrice': -1, 'finalPrice': 1000,
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 1000}],
            meta_info=[{'key': 'EventLimit', 'value': '6'}],
            sort_priority=181,
            item_grants=[{'templateId': 'Reagent:Reagent_Foil', 'quantity': 50}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="5971DB99866D42138724247D2A8BBF42",
            dev_name="Event.Evergreen5.13",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Event_Evergreen5',
                     'regularPrice': 2250, 'dynamicRegularPrice': -1, 'finalPrice': 2250,
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 2250}],
            meta_info=[{'key': 'EventLimit', 'value': '50'}],
            sort_priority=190,
            item_grants=[{'templateId': 'Reagent:Reagent_Shard_Dark', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="F3EA4EAF49284D23927F04EA03CF6EF0",
            dev_name="Event.Evergreen5.11",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Event_Evergreen5',
                     'regularPrice': 22500, 'dynamicRegularPrice': -1, 'finalPrice': 22500,
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 22500}],
            meta_info=[{'key': 'EventLimit', 'value': '1'}],
            sort_priority=192,
            item_grants=[{'templateId': 'Reagent:Reagent_Misc_CeremonialArmor', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="BFD783F78FAA4E30B48E1922E4889C90",
            dev_name="Event.Evergreen5.03",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Event_Evergreen5', 'regularPrice': 500,
                 'dynamicRegularPrice': -1, 'finalPrice': 500, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                 'basePrice': 500}],
            meta_info=[{'key': 'EventLimit', 'value': '1'}],
            sort_priority=200,
            item_grants=[{'templateId': 'Currency:MtxGiveaway', 'quantity': 250}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="E29E9E4FE1DA4D799EDA4FA2726D7D9B",
            dev_name="Event.Evergreen5.04",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Event_Evergreen5', 'regularPrice': 4,
                 'dynamicRegularPrice': -1, 'finalPrice': 4, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                 'basePrice': 4}],
            meta_info=[{'key': 'EventLimit', 'value': '20000'}],
            sort_priority=199,
            item_grants=[{'templateId': 'Currency:SkillXP', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="7597B2B7C7524125BAFA7E6D875B79BC",
            dev_name="Event.Evergreen5.31",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Event_Evergreen5', 'regularPrice': 15,
                 'dynamicRegularPrice': -1, 'finalPrice': 15, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                 'basePrice': 15}],
            meta_info=[{'key': 'EventLimit', 'value': '300'}],
            sort_priority=178,
            item_grants=[{'templateId': 'Reagent:Reagent_Shared_T02', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="E630784D7E3345FF958A4AEC3D121315",
            dev_name="Event.Evergreen5.24",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Event_Evergreen5',
                     'regularPrice': 1500, 'dynamicRegularPrice': -1, 'finalPrice': 1500,
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 1500}],
            meta_info=[{'key': 'EventLimit', 'value': '5'}],
            sort_priority=202,
            item_grants=[{'templateId': 'Voucher:Voucher_HeroSilver_Dark', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="96898B4CC1C84B3886E7AAF22C772BD4",
            dev_name="Event.Evergreen5.08",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Event_Evergreen5',
                     'regularPrice': 50000, 'dynamicRegularPrice': -1, 'finalPrice': 50000,
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 50000}],
            meta_info=[{'key': 'EventLimit', 'value': '2'}],
            sort_priority=195,
            item_grants=[{'templateId': 'Currency:HeroXp_Basic', 'quantity': 500000}],
        ))

    @classmethod
    async def init_storefront(cls) -> Self:
        """
        Initialise the Events storefront
        :return: The initialised Events storefront class
        """
        self: Events = cls()
        self.name = "Events"
        self.catalog_entries = []
        return self


class Workshop(Storefront):
    """
    Class based system to handle the Workshop storefront for the storefront catalog service
    """

    def __init__(self) -> None:
        """
        Initialise the Workshop storefront class.
        This will setup the variables for the Workshop storefront
        """
        super().__init__()

    async def update_storefront(self) -> None:
        """
        Update the storefront for the Workshop storefront class with the latest data
        This rotation never changed
        :return: None
        """
        # temporary implementation
        self.catalog_entries.append(Offer(
            offer_id="45916F474E404CCBB616CB74F1894575",
            dev_name="Workshop.Page01.ClassTraining.31",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Misc_ShadowEssence', 'regularPrice': 5,
                 'dynamicRegularPrice': -1, 'finalPrice': 5, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                 'basePrice': 5}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '38278D54469AA644404255919ABC67CF',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': 'E7EEA718452DEDED4574BD9D51CE23A1',
                           'minQuantity': 1}],
            meta_info=[{'key': 'WorkshopLevel', 'value': '0'}, {'key': 'ForceShowFirstItemInGrant', 'value': 'true'}],
            display_asset_path="/Game/Loot/AccountItems/Reagents/Reagent_ClassTraining_Strength"
                               ".Reagent_ClassTraining_Strength",
            item_grants=[{'templateId': 'Reagent:Reagent_ClassTraining_Strength', 'quantity': 1},
                         {'templateId': 'Currency:Gold', 'quantity': 10000}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="4495EE859818440992EA8CE752EB7CCB",
            dev_name="Workshop.L01.Page01.BuildRockbeast.04",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Pet_Rockbeast', 'regularPrice': 1,
                     'dynamicRegularPrice': -1, 'finalPrice': 1, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 1}],
            meta_info=[{'key': 'WorkshopLevel', 'value': '1'}, {'key': 'AffordOnly', 'value': 'true'}],
            sort_priority=3,
            item_grants=[{'templateId': 'Character:Pet_R1_Rockbeast_Nature_T03', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="31258E3431B24968A9BAD843C4B38E0F",
            dev_name="Workshop.L07.Page01.BuildingMaterials.01",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'Other', 'currencySubType': 'LaborPoints', 'regularPrice': 200,
                     'dynamicRegularPrice': -1, 'finalPrice': 200, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 200}],
            meta_info=[{'key': 'WorkshopLevel', 'value': '7'}],
            sort_priority=7,
            item_grants=[{'templateId': 'Reagent:Reagent_SupplyPoints_BuildingUpgrade', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="E5A0AEC7C763489B91669EFB5B53078A",
            dev_name="Workshop.L01.Page01.BuildRxT.02",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_RXT_Parts_Small', 'regularPrice': 100,
                 'dynamicRegularPrice': -1, 'finalPrice': 100, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                 'basePrice': 100}],
            meta_info=[{'key': 'WorkshopLevel', 'value': '1'}, {'key': 'AffordOnly', 'value': 'true'}],
            sort_priority=5,
            item_grants=[{'templateId': 'Character:Warrior_SR2_Fire_RoboGuy_T05', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="650F4214FB8F415DAA935EACF4893AAB",
            dev_name="Workshop.L01.Page01.BuildRandomGear.06",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Shard_Gear', 'regularPrice': 20,
                     'dynamicRegularPrice': -1, 'finalPrice': 20, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 20}],
            daily_limit=1,
            meta_info=[{'key': 'WorkshopLevel', 'value': '1'}],
            sort_priority=8,
            title="Build Random Armor  (VeryRare)",
            description="Construct a random Very Rare armor!",
            display_asset_path="/Game/UMG/Textures/HeroGear/T_Gear_Armor_Random_03_VeryRare"
                               ".T_Gear_Armor_Random_03_VeryRare",
        ))
        self.catalog_entries.append(Offer(
            offer_id="B22688D6EA8B4BC1A990F6B904B145C8",
            dev_name="Workshop.L24.Page01.BuildingMaterials.10",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'Other', 'currencySubType': 'LaborPoints', 'regularPrice': 200,
                     'dynamicRegularPrice': -1, 'finalPrice': 100, 'saleType': 'AmountOff',
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 100}],
            daily_limit=8,
            meta_info=[{'key': 'WorkshopLevel', 'value': '24'}, {'key': 'MaxWorkshopLevel', 'value': '25'}],
            sort_priority=14,
            item_grants=[{'templateId': 'Reagent:Reagent_SupplyPoints_BuildingUpgrade', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="5158AE01433D1424F81668A8BA65EFE3",
            dev_name="Rocket Fuel (Ancient Factory)",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'Other', 'currencySubType': 'LaborPoints', 'regularPrice': 50,
                     'dynamicRegularPrice': -1, 'finalPrice': 50, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 50}],
            daily_limit=1,
            requirements=[{'requirementType': 'DenyOnFulfillment', 'requiredId': '6A5DCF444886DF11888AD192153B3FD1',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '9E41C3CA4B15890914C587ABBEBC8E76',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '878728D44A2CA0901731C387D18FEED5',
                           'minQuantity': 1}],
            meta_info=[{'key': 'WorkshopLevel', 'value': '3'}],
            sort_priority=4,
            title="Rocket Fuel",
            description="Supercharged gameplay speed!\r\n\r\nNew speed is set automatically, but can be changed in "
                        "Gameplay Settings.",
            item_grants=[{'templateId': 'StandIn:RocketFuel', 'quantity': 1, 'attributes': {'FakeQuantity': 1}}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="931EA8A6B50F4BE6AF48413864DD1378",
            dev_name="Workshop.Page01.ClassTraining.17",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Misc_ShadowEssence', 'regularPrice': 1,
                 'dynamicRegularPrice': -1, 'finalPrice': 1, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                 'basePrice': 1}],
            daily_limit=1,
            requirements=[{'requirementType': 'DenyOnFulfillment', 'requiredId': '8550273E418A227A2CCFE7B8825472FF',
                           'minQuantity': 1}],
            meta_info=[{'key': 'WorkshopLevel', 'value': '0'}, {'key': 'AffordOnly', 'value': 'true'},
                       {'key': 'ForceShowFirstItemInGrant', 'value': 'true'}],
            sort_priority=19,
            display_asset_path="/Game/Loot/AccountItems/Reagents/Reagent_ClassTraining_Insight"
                               ".Reagent_ClassTraining_Insight",
            item_grants=[{'templateId': 'Reagent:Reagent_ClassTraining_Insight', 'quantity': 1},
                         {'templateId': 'Currency:Gold', 'quantity': 10000}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="365906993CE0432388FCA98F20FD6A0A",
            dev_name="Workshop.Page01.ClassTraining.24",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Misc_ShadowEssence', 'regularPrice': 5,
                 'dynamicRegularPrice': -1, 'finalPrice': 5, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                 'basePrice': 5}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': 'E7EEA718452DEDED4574BD9D51CE23A1',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': 'EBDAA0DC4684721269F4F29A5494519E',
                           'minQuantity': 1}],
            meta_info=[{'key': 'WorkshopLevel', 'value': '0'}, {'key': 'ForceShowFirstItemInGrant', 'value': 'true'}],
            display_asset_path="/Game/Loot/AccountItems/Reagents/Reagent_ClassTraining_Insight"
                               ".Reagent_ClassTraining_Insight",
            item_grants=[{'templateId': 'Reagent:Reagent_ClassTraining_Insight', 'quantity': 1},
                         {'templateId': 'Currency:Gold', 'quantity': 10000}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="999B0F083D8B46EDB4E0B786E36E0165",
            dev_name="Workshop.L16.Page01.BuildingMaterials.07",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'Other', 'currencySubType': 'LaborPoints', 'regularPrice': 200,
                     'dynamicRegularPrice': -1, 'finalPrice': 100, 'saleType': 'AmountOff',
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 100}],
            daily_limit=5,
            meta_info=[{'key': 'WorkshopLevel', 'value': '16'}, {'key': 'MaxWorkshopLevel', 'value': '19'}],
            sort_priority=14,
            item_grants=[{'templateId': 'Reagent:Reagent_SupplyPoints_BuildingUpgrade', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="0FFCA8E24D464BECB885EC09B65E45E8",
            dev_name="Workshop.L08.Page01.BuildingMaterials.04",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'Other', 'currencySubType': 'LaborPoints', 'regularPrice': 200,
                     'dynamicRegularPrice': -1, 'finalPrice': 100, 'saleType': 'AmountOff',
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 100}],
            daily_limit=2,
            meta_info=[{'key': 'WorkshopLevel', 'value': '8'}, {'key': 'MaxWorkshopLevel', 'value': '9'}],
            sort_priority=14,
            item_grants=[{'templateId': 'Reagent:Reagent_SupplyPoints_BuildingUpgrade', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="7D36124B1CC549FF8D0232CE8DABA132",
            dev_name="Workshop.L10.Page01.BuildingMaterials.05",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'Other', 'currencySubType': 'LaborPoints', 'regularPrice': 200,
                     'dynamicRegularPrice': -1, 'finalPrice': 100, 'saleType': 'AmountOff',
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 100}],
            daily_limit=3,
            meta_info=[{'key': 'WorkshopLevel', 'value': '10'}, {'key': 'MaxWorkshopLevel', 'value': '11'}],
            sort_priority=14,
            item_grants=[{'templateId': 'Reagent:Reagent_SupplyPoints_BuildingUpgrade', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="CD1D13838980415E9FEAFC4FCE51ABB3",
            dev_name="Workshop.Page01.ClassTraining.11",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Misc_ShadowEssence', 'regularPrice': 3,
                 'dynamicRegularPrice': -1, 'finalPrice': 3, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                 'basePrice': 3}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '689616B946BB3263CDD4F99952A3A666',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '814943904E314407D9148283C9E2F844',
                           'minQuantity': 1}],
            meta_info=[{'key': 'WorkshopLevel', 'value': '0'}, {'key': 'ForceShowFirstItemInGrant', 'value': 'true'}],
            display_asset_path="/Game/Loot/AccountItems/Reagents/Reagent_ClassTraining_Endurance"
                               ".Reagent_ClassTraining_Endurance",
            item_grants=[{'templateId': 'Reagent:Reagent_ClassTraining_Endurance', 'quantity': 1},
                         {'templateId': 'Currency:Gold', 'quantity': 10000}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="1DC95D1B125242FF8BA3627A833468CF",
            dev_name="Workshop.Page01.ClassTraining.29",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Misc_ShadowEssence', 'regularPrice': 4,
                 'dynamicRegularPrice': -1, 'finalPrice': 4, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                 'basePrice': 4}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': 'D98E59024D2A05BB8E7773BD4951B36F',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': 'CF03EC6145560777C8E2D58CD8588386',
                           'minQuantity': 1}],
            meta_info=[{'key': 'WorkshopLevel', 'value': '0'}, {'key': 'ForceShowFirstItemInGrant', 'value': 'true'}],
            display_asset_path="/Game/Loot/AccountItems/Reagents/Reagent_ClassTraining_Strength"
                               ".Reagent_ClassTraining_Strength",
            item_grants=[{'templateId': 'Reagent:Reagent_ClassTraining_Strength', 'quantity': 1},
                         {'templateId': 'Currency:Gold', 'quantity': 10000}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="D52DE0B0CCB74BA0BBA4A5F8866B9CA1",
            dev_name="Workshop.L22.Page01.BuildRandomItem.11",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'Other', 'currencySubType': 'LaborPoints', 'regularPrice': 50,
                     'dynamicRegularPrice': -1, 'finalPrice': 50, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 50}],
            daily_limit=10,
            meta_info=[{'key': 'WorkshopLevel', 'value': '22'}, {'key': 'MaxWorkshopLevel', 'value': '23'}],
            sort_priority=20,
            title="Build Random Item",
            description="Construct a random item, with a chance to get a hero!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="B57C78F0A96E47C895E5B5B1085AE4FC",
            dev_name="Workshop.Page01.ClassTraining.05",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Misc_ShadowEssence', 'regularPrice': 4,
                 'dynamicRegularPrice': -1, 'finalPrice': 4, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                 'basePrice': 4}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': 'D98E59024D2A05BB8E7773BD4951B36F',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': 'CF03EC6145560777C8E2D58CD8588386',
                           'minQuantity': 1}],
            meta_info=[{'key': 'WorkshopLevel', 'value': '0'}, {'key': 'ForceShowFirstItemInGrant', 'value': 'true'}],
            display_asset_path="/Game/Loot/AccountItems/Reagents/Reagent_ClassTraining_Agility"
                               ".Reagent_ClassTraining_Agility",
            item_grants=[{'templateId': 'Reagent:Reagent_ClassTraining_Agility', 'quantity': 1},
                         {'templateId': 'Currency:Gold', 'quantity': 10000}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="3E2101505C1C4109A84C065202C734E9",
            dev_name="Workshop.Page01.ClassTraining.12",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Misc_ShadowEssence', 'regularPrice': 4,
                 'dynamicRegularPrice': -1, 'finalPrice': 4, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                 'basePrice': 4}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '814943904E314407D9148283C9E2F844',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': 'D98E59024D2A05BB8E7773BD4951B36F',
                           'minQuantity': 1}],
            meta_info=[{'key': 'WorkshopLevel', 'value': '0'}, {'key': 'ForceShowFirstItemInGrant', 'value': 'true'}],
            display_asset_path="/Game/Loot/AccountItems/Reagents/Reagent_ClassTraining_Endurance"
                               ".Reagent_ClassTraining_Endurance",
            item_grants=[{'templateId': 'Reagent:Reagent_ClassTraining_Endurance', 'quantity': 1},
                         {'templateId': 'Currency:Gold', 'quantity': 10000}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="360F091A509142E7A55A1ED2F051104F",
            dev_name="Workshop.L01.Page01.BuildRandomGear.01",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Shard_Gear', 'regularPrice': 4,
                     'dynamicRegularPrice': -1, 'finalPrice': 4, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 4}],
            daily_limit=1,
            meta_info=[{'key': 'WorkshopLevel', 'value': '1'}],
            sort_priority=13,
            title="Build Random Weapon  (Uncommon)",
            description="Construct a random Uncommon weapon!",
            display_asset_path="/Game/UMG/Textures/HeroGear/T_Gear_Weapon_Random_01_Uncommon"
                               ".T_Gear_Weapon_Random_01_Uncommon",
        ))
        self.catalog_entries.append(Offer(
            offer_id="998A2925D6294C8EAF0B0A1791936B0F",
            dev_name="Workshop.L12.Page01.BuildingMaterials.06",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'Other', 'currencySubType': 'LaborPoints', 'regularPrice': 200,
                     'dynamicRegularPrice': -1, 'finalPrice': 100, 'saleType': 'AmountOff',
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 100}],
            daily_limit=4,
            meta_info=[{'key': 'WorkshopLevel', 'value': '12'}, {'key': 'MaxWorkshopLevel', 'value': '15'}],
            sort_priority=14,
            item_grants=[{'templateId': 'Reagent:Reagent_SupplyPoints_BuildingUpgrade', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="9CE722D5F83F487BA1024EF1C7B4827F",
            dev_name="Workshop.Page01.ClassTraining.30",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Misc_ShadowEssence', 'regularPrice': 4,
                 'dynamicRegularPrice': -1, 'finalPrice': 4, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                 'basePrice': 4}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': 'CF03EC6145560777C8E2D58CD8588386',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '38278D54469AA644404255919ABC67CF',
                           'minQuantity': 1}],
            meta_info=[{'key': 'WorkshopLevel', 'value': '0'}, {'key': 'ForceShowFirstItemInGrant', 'value': 'true'}],
            display_asset_path="/Game/Loot/AccountItems/Reagents/Reagent_ClassTraining_Strength"
                               ".Reagent_ClassTraining_Strength",
            item_grants=[{'templateId': 'Reagent:Reagent_ClassTraining_Strength', 'quantity': 1},
                         {'templateId': 'Currency:Gold', 'quantity': 10000}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="AB831651BD0C42E7A7D38C2D4EF67F93",
            dev_name="Workshop.Page01.ClassTraining.08",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Misc_ShadowEssence', 'regularPrice': 5,
                 'dynamicRegularPrice': -1, 'finalPrice': 5, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                 'basePrice': 5}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': 'E7EEA718452DEDED4574BD9D51CE23A1',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': 'EBDAA0DC4684721269F4F29A5494519E',
                           'minQuantity': 1}],
            meta_info=[{'key': 'WorkshopLevel', 'value': '0'}, {'key': 'ForceShowFirstItemInGrant', 'value': 'true'}],
            display_asset_path="/Game/Loot/AccountItems/Reagents/Reagent_ClassTraining_Agility"
                               ".Reagent_ClassTraining_Agility",
            item_grants=[{'templateId': 'Reagent:Reagent_ClassTraining_Agility', 'quantity': 1},
                         {'templateId': 'Currency:Gold', 'quantity': 10000}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="A72A10C090554E3FAFFAAC7E509A0A39",
            dev_name="Workshop.L20.Page01.BuildRandomItem.10",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'Other', 'currencySubType': 'LaborPoints', 'regularPrice': 50,
                     'dynamicRegularPrice': -1, 'finalPrice': 50, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 50}],
            daily_limit=9,
            meta_info=[{'key': 'WorkshopLevel', 'value': '20'}, {'key': 'MaxWorkshopLevel', 'value': '21'}],
            sort_priority=20,
            title="Build Random Item",
            description="Construct a random item, with a chance to get a hero!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="EECEA07EAB504F7280ED968778C29E84",
            dev_name="Workshop.L03.Page01.BuildRandomItem.02",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'Other', 'currencySubType': 'LaborPoints', 'regularPrice': 50,
                     'dynamicRegularPrice': -1, 'finalPrice': 50, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 50}],
            daily_limit=1,
            meta_info=[{'key': 'WorkshopLevel', 'value': '3'}, {'key': 'MaxWorkshopLevel', 'value': '4'}],
            sort_priority=20,
            title="Build Random Item",
            description="Construct a random item, with a chance to get a hero!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="C0BDD96231EC43C48A6BC4CA5CE2ED3F",
            dev_name="Workshop.L26.Page01.BuildingMaterials.11",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'Other', 'currencySubType': 'LaborPoints', 'regularPrice': 200,
                     'dynamicRegularPrice': -1, 'finalPrice': 100, 'saleType': 'AmountOff',
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 100}],
            daily_limit=9,
            meta_info=[{'key': 'WorkshopLevel', 'value': '26'}],
            sort_priority=14,
            item_grants=[{'templateId': 'Reagent:Reagent_SupplyPoints_BuildingUpgrade', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="C2C29029295349C8A43165B228D1E15B",
            dev_name="Workshop.L01.Page01.BuildRxT.01",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_RXT_Parts_Small', 'regularPrice': 100,
                 'dynamicRegularPrice': -1, 'finalPrice': 100, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                 'basePrice': 100}],
            meta_info=[{'key': 'WorkshopLevel', 'value': '1'}, {'key': 'AffordOnly', 'value': 'true'}],
            sort_priority=5,
            item_grants=[{'templateId': 'Character:Warrior_SR2_Dark_RoboGuy_T05', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="0CDCCE77C1B94CA18F4A969520953C8C",
            dev_name="Workshop.Page01.ClassTraining.03",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Misc_ShadowEssence', 'regularPrice': 3,
                 'dynamicRegularPrice': -1, 'finalPrice': 3, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                 'basePrice': 3}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '689616B946BB3263CDD4F99952A3A666',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '814943904E314407D9148283C9E2F844',
                           'minQuantity': 1}],
            meta_info=[{'key': 'WorkshopLevel', 'value': '0'}, {'key': 'ForceShowFirstItemInGrant', 'value': 'true'}],
            display_asset_path="/Game/Loot/AccountItems/Reagents/Reagent_ClassTraining_Agility"
                               ".Reagent_ClassTraining_Agility",
            item_grants=[{'templateId': 'Reagent:Reagent_ClassTraining_Agility', 'quantity': 1},
                         {'templateId': 'Currency:Gold', 'quantity': 10000}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="3C03DFB85A5C4A43B2CEA594466A74B9",
            dev_name="Workshop.L18.Page01.BuildRandomItem.09",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'Other', 'currencySubType': 'LaborPoints', 'regularPrice': 50,
                     'dynamicRegularPrice': -1, 'finalPrice': 50, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 50}],
            daily_limit=8,
            meta_info=[{'key': 'WorkshopLevel', 'value': '18'}, {'key': 'MaxWorkshopLevel', 'value': '19'}],
            sort_priority=20,
            title="Build Random Item",
            description="Construct a random item, with a chance to get a hero!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="D9FD18151FFE4B2DBE2467572A8584DB",
            dev_name="Workshop.Page01.ClassTraining.07",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Misc_ShadowEssence', 'regularPrice': 5,
                 'dynamicRegularPrice': -1, 'finalPrice': 5, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                 'basePrice': 5}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '38278D54469AA644404255919ABC67CF',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': 'E7EEA718452DEDED4574BD9D51CE23A1',
                           'minQuantity': 1}],
            meta_info=[{'key': 'WorkshopLevel', 'value': '0'}, {'key': 'ForceShowFirstItemInGrant', 'value': 'true'}],
            display_asset_path="/Game/Loot/AccountItems/Reagents/Reagent_ClassTraining_Agility"
                               ".Reagent_ClassTraining_Agility",
            item_grants=[{'templateId': 'Reagent:Reagent_ClassTraining_Agility', 'quantity': 1},
                         {'templateId': 'Currency:Gold', 'quantity': 10000}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="595DAC9B5C734AEA88D8C5140D81AE8F",
            dev_name="Workshop.L01.Page01.BuildRockbeast.05",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Pet_Rockbeast', 'regularPrice': 1,
                     'dynamicRegularPrice': -1, 'finalPrice': 1, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 1}],
            meta_info=[{'key': 'WorkshopLevel', 'value': '1'}, {'key': 'AffordOnly', 'value': 'true'}],
            sort_priority=3,
            item_grants=[{'templateId': 'Character:Pet_R1_Rockbeast_Water_T03', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="592665652C524356A87F92B9778695DE",
            dev_name="Workshop.L01.Page01.BuildRandomGear.05",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Shard_Gear', 'regularPrice': 10,
                     'dynamicRegularPrice': -1, 'finalPrice': 10, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 10}],
            daily_limit=1,
            meta_info=[{'key': 'WorkshopLevel', 'value': '1'}],
            sort_priority=9,
            title="Build Random Armor  (Rare)",
            description="Construct a random Rare armor!",
            display_asset_path="/Game/UMG/Textures/HeroGear/T_Gear_Armor_Random_02_Rare.T_Gear_Armor_Random_02_Rare",
        ))
        self.catalog_entries.append(Offer(
            offer_id="AEADDA2C0873472FB05E03C6BD9B3B1B",
            dev_name="Workshop.L01.Page01.BuildRockbeast.01",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Pet_Rockbeast', 'regularPrice': 1,
                     'dynamicRegularPrice': -1, 'finalPrice': 1, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 1}],
            meta_info=[{'key': 'WorkshopLevel', 'value': '1'}, {'key': 'AffordOnly', 'value': 'true'}],
            sort_priority=3,
            item_grants=[{'templateId': 'Character:Pet_R1_Rockbeast_Dark_T03', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="FA483E537A324DFF8B544B5144123E82",
            dev_name="Workshop.Page01.ClassTraining.20",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Misc_ShadowEssence', 'regularPrice': 4,
                 'dynamicRegularPrice': -1, 'finalPrice': 4, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                 'basePrice': 4}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '814943904E314407D9148283C9E2F844',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': 'D98E59024D2A05BB8E7773BD4951B36F',
                           'minQuantity': 1}],
            meta_info=[{'key': 'WorkshopLevel', 'value': '0'}, {'key': 'ForceShowFirstItemInGrant', 'value': 'true'}],
            display_asset_path="/Game/Loot/AccountItems/Reagents/Reagent_ClassTraining_Insight"
                               ".Reagent_ClassTraining_Insight",
            item_grants=[{'templateId': 'Reagent:Reagent_ClassTraining_Insight', 'quantity': 1},
                         {'templateId': 'Currency:Gold', 'quantity': 10000}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="3EA0E03038C84C80B11F63C4CE1DC3E5",
            dev_name="Workshop.L01.Page01.BuildRxT.04",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_RXT_Parts_Small', 'regularPrice': 100,
                 'dynamicRegularPrice': -1, 'finalPrice': 100, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                 'basePrice': 100}],
            meta_info=[{'key': 'WorkshopLevel', 'value': '1'}, {'key': 'AffordOnly', 'value': 'true'}],
            sort_priority=5,
            item_grants=[{'templateId': 'Character:Warrior_SR2_Nature_RoboGuy_T05', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="EA1E69D4A20245E39FB900BB30DCD4FC",
            dev_name="Workshop.Page01.ClassTraining.04",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Misc_ShadowEssence', 'regularPrice': 4,
                 'dynamicRegularPrice': -1, 'finalPrice': 4, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                 'basePrice': 4}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '814943904E314407D9148283C9E2F844',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': 'D98E59024D2A05BB8E7773BD4951B36F',
                           'minQuantity': 1}],
            meta_info=[{'key': 'WorkshopLevel', 'value': '0'}, {'key': 'ForceShowFirstItemInGrant', 'value': 'true'}],
            display_asset_path="/Game/Loot/AccountItems/Reagents/Reagent_ClassTraining_Agility"
                               ".Reagent_ClassTraining_Agility",
            item_grants=[{'templateId': 'Reagent:Reagent_ClassTraining_Agility', 'quantity': 1},
                         {'templateId': 'Currency:Gold', 'quantity': 10000}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="7B08EFFB6BE04482A0779C1E1B50A6BF",
            dev_name="Workshop.Page01.ClassTraining.10",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Misc_ShadowEssence', 'regularPrice': 2,
                 'dynamicRegularPrice': -1, 'finalPrice': 2, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                 'basePrice': 2}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '8550273E418A227A2CCFE7B8825472FF',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '689616B946BB3263CDD4F99952A3A666',
                           'minQuantity': 1}],
            meta_info=[{'key': 'WorkshopLevel', 'value': '0'}, {'key': 'ForceShowFirstItemInGrant', 'value': 'true'}],
            display_asset_path="/Game/Loot/AccountItems/Reagents/Reagent_ClassTraining_Endurance"
                               ".Reagent_ClassTraining_Endurance",
            item_grants=[{'templateId': 'Reagent:Reagent_ClassTraining_Endurance', 'quantity': 1},
                         {'templateId': 'Currency:Gold', 'quantity': 10000}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="A42A8112B2B14853962A04F428248A15",
            dev_name="Workshop.Page01.ClassTraining.25",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Misc_ShadowEssence', 'regularPrice': 1,
                 'dynamicRegularPrice': -1, 'finalPrice': 1, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                 'basePrice': 1}],
            daily_limit=1,
            requirements=[{'requirementType': 'DenyOnFulfillment', 'requiredId': '8550273E418A227A2CCFE7B8825472FF',
                           'minQuantity': 1}],
            meta_info=[{'key': 'WorkshopLevel', 'value': '0'}, {'key': 'AffordOnly', 'value': 'true'},
                       {'key': 'ForceShowFirstItemInGrant', 'value': 'true'}],
            sort_priority=19,
            display_asset_path="/Game/Loot/AccountItems/Reagents/Reagent_ClassTraining_Strength"
                               ".Reagent_ClassTraining_Strength",
            item_grants=[{'templateId': 'Reagent:Reagent_ClassTraining_Strength', 'quantity': 1},
                         {'templateId': 'Currency:Gold', 'quantity': 10000}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="660D4B073413491D97DEAA063B1DE063",
            dev_name="Workshop.L01.Page01.BuildRxT.05",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_RXT_Parts_Small', 'regularPrice': 100,
                 'dynamicRegularPrice': -1, 'finalPrice': 100, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                 'basePrice': 100}],
            meta_info=[{'key': 'WorkshopLevel', 'value': '1'}, {'key': 'AffordOnly', 'value': 'true'}],
            sort_priority=5,
            item_grants=[{'templateId': 'Character:Warrior_SR2_Water_RoboGuy_T05', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="FAA4E77185704DCC9484B5F26808AFF4",
            dev_name="Workshop.Page01.ClassTraining.16",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Misc_ShadowEssence', 'regularPrice': 5,
                 'dynamicRegularPrice': -1, 'finalPrice': 5, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                 'basePrice': 5}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': 'E7EEA718452DEDED4574BD9D51CE23A1',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': 'EBDAA0DC4684721269F4F29A5494519E',
                           'minQuantity': 1}],
            meta_info=[{'key': 'WorkshopLevel', 'value': '0'}, {'key': 'ForceShowFirstItemInGrant', 'value': 'true'}],
            display_asset_path="/Game/Loot/AccountItems/Reagents/Reagent_ClassTraining_Endurance"
                               ".Reagent_ClassTraining_Endurance",
            item_grants=[{'templateId': 'Reagent:Reagent_ClassTraining_Endurance', 'quantity': 1},
                         {'templateId': 'Currency:Gold', 'quantity': 10000}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="8837ABE8704D4ACB92188D3067B323F1",
            dev_name="Workshop.L12.Page01.BuildRandomItem.06",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'Other', 'currencySubType': 'LaborPoints', 'regularPrice': 50,
                     'dynamicRegularPrice': -1, 'finalPrice': 50, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 50}],
            daily_limit=5,
            meta_info=[{'key': 'WorkshopLevel', 'value': '12'}, {'key': 'MaxWorkshopLevel', 'value': '13'}],
            sort_priority=20,
            title="Build Random Item",
            description="Construct a random item, with a chance to get a hero!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="EE26D473FA3847BA9FFADACDF05F8E77",
            dev_name="Workshop.L01.Page01.BuildRockbeast.02",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Pet_Rockbeast', 'regularPrice': 1,
                     'dynamicRegularPrice': -1, 'finalPrice': 1, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 1}],
            meta_info=[{'key': 'WorkshopLevel', 'value': '1'}, {'key': 'AffordOnly', 'value': 'true'}],
            sort_priority=3,
            item_grants=[{'templateId': 'Character:Pet_R1_Rockbeast_Fire_T03', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="A444DDB665B34F7E9B9B244038418DAE",
            dev_name="Workshop.L01.Page01.BuildRandomItem.01",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'Other', 'currencySubType': 'LaborPoints', 'regularPrice': 50,
                     'dynamicRegularPrice': -1, 'finalPrice': 0, 'saleType': 'AmountOff',
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 0}],
            daily_limit=1,
            meta_info=[{'key': 'WorkshopLevel', 'value': '1'}],
            sort_priority=21,
            title="Build Random Item",
            description="Construct a random item, with a chance to get a hero!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="7BAF4F0929C042888CE8F7548BC895FB",
            dev_name="Workshop.L05.Page01.BuildRandomItem.03",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'Other', 'currencySubType': 'LaborPoints', 'regularPrice': 50,
                     'dynamicRegularPrice': -1, 'finalPrice': 50, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 50}],
            daily_limit=2,
            meta_info=[{'key': 'WorkshopLevel', 'value': '5'}, {'key': 'MaxWorkshopLevel', 'value': '6'}],
            sort_priority=20,
            title="Build Random Item",
            description="Construct a random item, with a chance to get a hero!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="AEDDC9EBE4374E09A6BAAF79EEBBB6A9",
            dev_name="Workshop.Page01.ClassTraining.13",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Misc_ShadowEssence', 'regularPrice': 4,
                 'dynamicRegularPrice': -1, 'finalPrice': 4, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                 'basePrice': 4}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': 'D98E59024D2A05BB8E7773BD4951B36F',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': 'CF03EC6145560777C8E2D58CD8588386',
                           'minQuantity': 1}],
            meta_info=[{'key': 'WorkshopLevel', 'value': '0'}, {'key': 'ForceShowFirstItemInGrant', 'value': 'true'}],
            display_asset_path="/Game/Loot/AccountItems/Reagents/Reagent_ClassTraining_Endurance"
                               ".Reagent_ClassTraining_Endurance",
            item_grants=[{'templateId': 'Reagent:Reagent_ClassTraining_Endurance', 'quantity': 1},
                         {'templateId': 'Currency:Gold', 'quantity': 10000}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="EA114DA3C08B4A68BD20FCD409819FBD",
            dev_name="Workshop.L01.Page01.BuildRandomGear.04",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Shard_Gear', 'regularPrice': 4,
                     'dynamicRegularPrice': -1, 'finalPrice': 4, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 4}],
            daily_limit=1,
            meta_info=[{'key': 'WorkshopLevel', 'value': '1'}],
            sort_priority=10,
            title="Build Random Armor  (Uncommon)",
            description="Construct a random Uncommon armor!",
            display_asset_path="/Game/UMG/Textures/HeroGear/T_Gear_Armor_Random_01_Uncommon"
                               ".T_Gear_Armor_Random_01_Uncommon",
        ))
        self.catalog_entries.append(Offer(
            offer_id="6C7C7CAC26C642B394F60C9260DB86EE",
            dev_name="Workshop.L01.Page01.BuildStarterPets.01",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'Other', 'currencySubType': 'LaborPoints', 'regularPrice': 12,
                     'dynamicRegularPrice': -1, 'finalPrice': 12, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 12}],
            daily_limit=1,
            requirements=[{'requirementType': 'DenyOnFulfillment', 'requiredId': '8299F3BC42C1058E5AFC2ABF92E17A31',
                           'minQuantity': 1}],
            meta_info=[{'key': 'WorkshopLevel', 'value': '1'}],
            title="Starter Pets",
            description="A box of pets! Can be opened on the World Map.",
            item_grants=[{'templateId': 'Giftbox:GB_StarterPets', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="3234AE487D1E4282884CEE01FDE27AF2",
            dev_name="Workshop.L07.Page01.BuildingMaterials.02",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Ore:Ore_Magicite', 'regularPrice': 10,
                     'dynamicRegularPrice': -1, 'finalPrice': 10, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 10}],
            meta_info=[{'key': 'WorkshopLevel', 'value': '7'}],
            sort_priority=6,
            item_grants=[{'templateId': 'Reagent:Reagent_SupplyPoints_BuildingUpgrade', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="DD13BD9BFB834706B160634B80D2960C",
            dev_name="Workshop.L01.Page01.BuildRockbeast.03",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Pet_Rockbeast', 'regularPrice': 1,
                     'dynamicRegularPrice': -1, 'finalPrice': 1, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 1}],
            meta_info=[{'key': 'WorkshopLevel', 'value': '1'}, {'key': 'AffordOnly', 'value': 'true'}],
            sort_priority=3,
            item_grants=[{'templateId': 'Character:Pet_R1_Rockbeast_Light_T03', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="7D679A9B638743F7931F6C36C0A14E6E",
            dev_name="Workshop.L16.Page01.BuildRandomItem.08",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'Other', 'currencySubType': 'LaborPoints', 'regularPrice': 50,
                     'dynamicRegularPrice': -1, 'finalPrice': 50, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 50}],
            daily_limit=7,
            meta_info=[{'key': 'WorkshopLevel', 'value': '16'}, {'key': 'MaxWorkshopLevel', 'value': '17'}],
            sort_priority=20,
            title="Build Random Item",
            description="Construct a random item, with a chance to get a hero!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="53C0C070FB9D427D961922FAFC6C53F2",
            dev_name="Workshop.L20.Page01.BuildingMaterials.08",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'Other', 'currencySubType': 'LaborPoints', 'regularPrice': 200,
                     'dynamicRegularPrice': -1, 'finalPrice': 100, 'saleType': 'AmountOff',
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 100}],
            daily_limit=6,
            meta_info=[{'key': 'WorkshopLevel', 'value': '20'}, {'key': 'MaxWorkshopLevel', 'value': '21'}],
            sort_priority=14,
            item_grants=[{'templateId': 'Reagent:Reagent_SupplyPoints_BuildingUpgrade', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="E881D28285B04871A41BC585729F1430",
            dev_name="Workshop.L22.Page01.BuildingMaterials.09",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'Other', 'currencySubType': 'LaborPoints', 'regularPrice': 200,
                     'dynamicRegularPrice': -1, 'finalPrice': 100, 'saleType': 'AmountOff',
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 100}],
            daily_limit=7,
            meta_info=[{'key': 'WorkshopLevel', 'value': '22'}, {'key': 'MaxWorkshopLevel', 'value': '23'}],
            sort_priority=14,
            item_grants=[{'templateId': 'Reagent:Reagent_SupplyPoints_BuildingUpgrade', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="792ABE08EFD4445A978160AA95676104",
            dev_name="Workshop.Page01.ClassTraining.14",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Misc_ShadowEssence', 'regularPrice': 4,
                 'dynamicRegularPrice': -1, 'finalPrice': 4, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                 'basePrice': 4}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': 'CF03EC6145560777C8E2D58CD8588386',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '38278D54469AA644404255919ABC67CF',
                           'minQuantity': 1}],
            meta_info=[{'key': 'WorkshopLevel', 'value': '0'}, {'key': 'ForceShowFirstItemInGrant', 'value': 'true'}],
            display_asset_path="/Game/Loot/AccountItems/Reagents/Reagent_ClassTraining_Endurance"
                               ".Reagent_ClassTraining_Endurance",
            item_grants=[{'templateId': 'Reagent:Reagent_ClassTraining_Endurance', 'quantity': 1},
                         {'templateId': 'Currency:Gold', 'quantity': 10000}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="94F85A09F8CA4CD1B760D4A4AE598983",
            dev_name="Workshop.Page01.ClassTraining.23",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Misc_ShadowEssence', 'regularPrice': 5,
                 'dynamicRegularPrice': -1, 'finalPrice': 5, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                 'basePrice': 5}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '38278D54469AA644404255919ABC67CF',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': 'E7EEA718452DEDED4574BD9D51CE23A1',
                           'minQuantity': 1}],
            meta_info=[{'key': 'WorkshopLevel', 'value': '0'}, {'key': 'ForceShowFirstItemInGrant', 'value': 'true'}],
            display_asset_path="/Game/Loot/AccountItems/Reagents/Reagent_ClassTraining_Insight"
                               ".Reagent_ClassTraining_Insight",
            item_grants=[{'templateId': 'Reagent:Reagent_ClassTraining_Insight', 'quantity': 1},
                         {'templateId': 'Currency:Gold', 'quantity': 10000}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="FD57DC54925E43438479D208009D51AA",
            dev_name="Workshop.L01.Page01.BuildWCHero.02",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_WC_Hero_TripleCombo',
                     'regularPrice': 100, 'dynamicRegularPrice': -1, 'finalPrice': 100,
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 100}],
            meta_info=[{'key': 'WorkshopLevel', 'value': '1'}, {'key': 'AffordOnly', 'value': 'true'}],
            sort_priority=4,
            item_grants=[{'templateId': 'Character:MartialArtist_SR2_Nature_TripleCombo_T04', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="3BC0F14708134510B1061401D580EDD8",
            dev_name="Workshop.L14.Page01.BuildRandomItem.07",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'Other', 'currencySubType': 'LaborPoints', 'regularPrice': 50,
                     'dynamicRegularPrice': -1, 'finalPrice': 50, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 50}],
            daily_limit=6,
            meta_info=[{'key': 'WorkshopLevel', 'value': '14'}, {'key': 'MaxWorkshopLevel', 'value': '15'}],
            sort_priority=20,
            title="Build Random Item",
            description="Construct a random item, with a chance to get a hero!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="B7896D4E2028431DA84ED1CAFF60B282",
            dev_name="Workshop.Page01.ClassTraining.27",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Misc_ShadowEssence', 'regularPrice': 3,
                 'dynamicRegularPrice': -1, 'finalPrice': 3, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                 'basePrice': 3}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '689616B946BB3263CDD4F99952A3A666',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '814943904E314407D9148283C9E2F844',
                           'minQuantity': 1}],
            meta_info=[{'key': 'WorkshopLevel', 'value': '0'}, {'key': 'ForceShowFirstItemInGrant', 'value': 'true'}],
            display_asset_path="/Game/Loot/AccountItems/Reagents/Reagent_ClassTraining_Strength"
                               ".Reagent_ClassTraining_Strength",
            item_grants=[{'templateId': 'Reagent:Reagent_ClassTraining_Strength', 'quantity': 1},
                         {'templateId': 'Currency:Gold', 'quantity': 10000}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="83D99E84967645AB81A03B99684C8F81",
            dev_name="Workshop.L26.Page01.BuildRandomItem.13",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'Other', 'currencySubType': 'LaborPoints', 'regularPrice': 50,
                     'dynamicRegularPrice': -1, 'finalPrice': 50, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 50}],
            daily_limit=12,
            meta_info=[{'key': 'WorkshopLevel', 'value': '26'}, {'key': 'MaxWorkshopLevel', 'value': '27'}],
            sort_priority=20,
            title="Build Random Item",
            description="Construct a random item, with a chance to get a hero!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="D7FDE1D864D2492A80098D0F94D4347F",
            dev_name="Workshop.Page01.ClassTraining.18",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Misc_ShadowEssence', 'regularPrice': 2,
                 'dynamicRegularPrice': -1, 'finalPrice': 2, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                 'basePrice': 2}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '8550273E418A227A2CCFE7B8825472FF',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '689616B946BB3263CDD4F99952A3A666',
                           'minQuantity': 1}],
            meta_info=[{'key': 'WorkshopLevel', 'value': '0'}, {'key': 'ForceShowFirstItemInGrant', 'value': 'true'}],
            display_asset_path="/Game/Loot/AccountItems/Reagents/Reagent_ClassTraining_Insight"
                               ".Reagent_ClassTraining_Insight",
            item_grants=[{'templateId': 'Reagent:Reagent_ClassTraining_Insight', 'quantity': 1},
                         {'templateId': 'Currency:Gold', 'quantity': 10000}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="FD72465BF9C7450995D11CA951ED14CA",
            dev_name="Workshop.L28.Page01.BuildRandomItem.14",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'Other', 'currencySubType': 'LaborPoints', 'regularPrice': 50,
                     'dynamicRegularPrice': -1, 'finalPrice': 50, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 50}],
            daily_limit=13,
            meta_info=[{'key': 'WorkshopLevel', 'value': '28'}, {'key': 'MaxWorkshopLevel', 'value': '29'}],
            sort_priority=20,
            title="Build Random Item",
            description="Construct a random item, with a chance to get a hero!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="CE9B09D0BB6E44B5BF25CE8A0A375014",
            dev_name="Workshop.L01.Page01.BuildRandomGear.03",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Shard_Gear', 'regularPrice': 20,
                     'dynamicRegularPrice': -1, 'finalPrice': 20, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 20}],
            daily_limit=1,
            meta_info=[{'key': 'WorkshopLevel', 'value': '1'}],
            sort_priority=11,
            title="Build Random Weapon  (VeryRare)",
            description="Construct a random Very Rare weapon!",
            display_asset_path="/Game/UMG/Textures/HeroGear/T_Gear_Weapon_Random_03_VeryRare"
                               ".T_Gear_Weapon_Random_03_VeryRare",
        ))
        self.catalog_entries.append(Offer(
            offer_id="A322035FE49443A198939406F96417DE",
            dev_name="Workshop.Page01.ClassTraining.09",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Misc_ShadowEssence', 'regularPrice': 1,
                 'dynamicRegularPrice': -1, 'finalPrice': 1, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                 'basePrice': 1}],
            daily_limit=1,
            requirements=[{'requirementType': 'DenyOnFulfillment', 'requiredId': '8550273E418A227A2CCFE7B8825472FF',
                           'minQuantity': 1}],
            meta_info=[{'key': 'WorkshopLevel', 'value': '0'}, {'key': 'AffordOnly', 'value': 'true'},
                       {'key': 'ForceShowFirstItemInGrant', 'value': 'true'}],
            sort_priority=19,
            display_asset_path="/Game/Loot/AccountItems/Reagents/Reagent_ClassTraining_Endurance"
                               ".Reagent_ClassTraining_Endurance",
            item_grants=[{'templateId': 'Reagent:Reagent_ClassTraining_Endurance', 'quantity': 1},
                         {'templateId': 'Currency:Gold', 'quantity': 10000}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="927CE6F9076143E2BBFEAAB341EBF3D9",
            dev_name="Workshop.Page01.ClassTraining.15",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Misc_ShadowEssence', 'regularPrice': 5,
                 'dynamicRegularPrice': -1, 'finalPrice': 5, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                 'basePrice': 5}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '38278D54469AA644404255919ABC67CF',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': 'E7EEA718452DEDED4574BD9D51CE23A1',
                           'minQuantity': 1}],
            meta_info=[{'key': 'WorkshopLevel', 'value': '0'}, {'key': 'ForceShowFirstItemInGrant', 'value': 'true'}],
            display_asset_path="/Game/Loot/AccountItems/Reagents/Reagent_ClassTraining_Endurance"
                               ".Reagent_ClassTraining_Endurance",
            item_grants=[{'templateId': 'Reagent:Reagent_ClassTraining_Endurance', 'quantity': 1},
                         {'templateId': 'Currency:Gold', 'quantity': 10000}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="C51FD14F091B47A88D2743D2AE3A49FA",
            dev_name="Workshop.Page01.ClassTraining.28",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Misc_ShadowEssence', 'regularPrice': 4,
                 'dynamicRegularPrice': -1, 'finalPrice': 4, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                 'basePrice': 4}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '814943904E314407D9148283C9E2F844',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': 'D98E59024D2A05BB8E7773BD4951B36F',
                           'minQuantity': 1}],
            meta_info=[{'key': 'WorkshopLevel', 'value': '0'}, {'key': 'ForceShowFirstItemInGrant', 'value': 'true'}],
            display_asset_path="/Game/Loot/AccountItems/Reagents/Reagent_ClassTraining_Strength"
                               ".Reagent_ClassTraining_Strength",
            item_grants=[{'templateId': 'Reagent:Reagent_ClassTraining_Strength', 'quantity': 1},
                         {'templateId': 'Currency:Gold', 'quantity': 10000}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="96C2B3F56549429CAE5862D122B97102",
            dev_name="Workshop.L01.Page01.BuildWCHero.03",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_WC_Hero_TripleCombo',
                     'regularPrice': 100, 'dynamicRegularPrice': -1, 'finalPrice': 100,
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 100}],
            meta_info=[{'key': 'WorkshopLevel', 'value': '1'}, {'key': 'AffordOnly', 'value': 'true'}],
            sort_priority=4,
            item_grants=[{'templateId': 'Character:MartialArtist_SR2_Water_TripleCombo_T04', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="D80B13049A804C3FBA56C6C9C589F60C",
            dev_name="Workshop.L30.Page01.BuildRandomItem.15",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'Other', 'currencySubType': 'LaborPoints', 'regularPrice': 50,
                     'dynamicRegularPrice': -1, 'finalPrice': 50, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 50}],
            daily_limit=14,
            meta_info=[{'key': 'WorkshopLevel', 'value': '30'}],
            sort_priority=20,
            title="Build Random Item",
            description="Construct a random item, with a chance to get a hero!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="2B6943D5F2C5450EBB015025D336077B",
            dev_name="Workshop.L07.Page01.BuildRandomItem.04",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'Other', 'currencySubType': 'LaborPoints', 'regularPrice': 50,
                     'dynamicRegularPrice': -1, 'finalPrice': 50, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 50}],
            daily_limit=3,
            meta_info=[{'key': 'WorkshopLevel', 'value': '7'}, {'key': 'MaxWorkshopLevel', 'value': '9'}],
            sort_priority=20,
            title="Build Random Item",
            description="Construct a random item, with a chance to get a hero!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="8A509646F7D24171A36D05C5F924CEA3",
            dev_name="Workshop.L10.Page01.BuildRandomItem.05",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'Other', 'currencySubType': 'LaborPoints', 'regularPrice': 50,
                     'dynamicRegularPrice': -1, 'finalPrice': 50, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 50}],
            daily_limit=4,
            meta_info=[{'key': 'WorkshopLevel', 'value': '10'}, {'key': 'MaxWorkshopLevel', 'value': '11'}],
            sort_priority=20,
            title="Build Random Item",
            description="Construct a random item, with a chance to get a hero!",
        ))
        self.catalog_entries.append(Offer(
            offer_id="5D6C4EE12C844BC59ABB107D88DA5C6A",
            dev_name="Workshop.Page01.ClassTraining.19",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Misc_ShadowEssence', 'regularPrice': 3,
                 'dynamicRegularPrice': -1, 'finalPrice': 3, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                 'basePrice': 3}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '689616B946BB3263CDD4F99952A3A666',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '814943904E314407D9148283C9E2F844',
                           'minQuantity': 1}],
            meta_info=[{'key': 'WorkshopLevel', 'value': '0'}, {'key': 'ForceShowFirstItemInGrant', 'value': 'true'}],
            display_asset_path="/Game/Loot/AccountItems/Reagents/Reagent_ClassTraining_Insight"
                               ".Reagent_ClassTraining_Insight",
            item_grants=[{'templateId': 'Reagent:Reagent_ClassTraining_Insight', 'quantity': 1},
                         {'templateId': 'Currency:Gold', 'quantity': 10000}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="2965FC95A8A84C51B7980CADD027A731",
            dev_name="Workshop.Page01.ClassTraining.21",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Misc_ShadowEssence', 'regularPrice': 4,
                 'dynamicRegularPrice': -1, 'finalPrice': 4, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                 'basePrice': 4}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': 'D98E59024D2A05BB8E7773BD4951B36F',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': 'CF03EC6145560777C8E2D58CD8588386',
                           'minQuantity': 1}],
            meta_info=[{'key': 'WorkshopLevel', 'value': '0'}, {'key': 'ForceShowFirstItemInGrant', 'value': 'true'}],
            display_asset_path="/Game/Loot/AccountItems/Reagents/Reagent_ClassTraining_Insight"
                               ".Reagent_ClassTraining_Insight",
            item_grants=[{'templateId': 'Reagent:Reagent_ClassTraining_Insight', 'quantity': 1},
                         {'templateId': 'Currency:Gold', 'quantity': 10000}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="524F0F7663CF41F7B10E1719BE9E0D0C",
            dev_name="Workshop.Page01.ClassTraining.22",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Misc_ShadowEssence', 'regularPrice': 4,
                 'dynamicRegularPrice': -1, 'finalPrice': 4, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                 'basePrice': 4}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': 'CF03EC6145560777C8E2D58CD8588386',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '38278D54469AA644404255919ABC67CF',
                           'minQuantity': 1}],
            meta_info=[{'key': 'WorkshopLevel', 'value': '0'}, {'key': 'ForceShowFirstItemInGrant', 'value': 'true'}],
            display_asset_path="/Game/Loot/AccountItems/Reagents/Reagent_ClassTraining_Insight"
                               ".Reagent_ClassTraining_Insight",
            item_grants=[{'templateId': 'Reagent:Reagent_ClassTraining_Insight', 'quantity': 1},
                         {'templateId': 'Currency:Gold', 'quantity': 10000}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="39343131B8CC409D83781CD03FF8BE93",
            dev_name="Workshop.Page01.ClassTraining.06",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Misc_ShadowEssence', 'regularPrice': 4,
                 'dynamicRegularPrice': -1, 'finalPrice': 4, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                 'basePrice': 4}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': 'CF03EC6145560777C8E2D58CD8588386',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '38278D54469AA644404255919ABC67CF',
                           'minQuantity': 1}],
            meta_info=[{'key': 'WorkshopLevel', 'value': '0'}, {'key': 'ForceShowFirstItemInGrant', 'value': 'true'}],
            display_asset_path="/Game/Loot/AccountItems/Reagents/Reagent_ClassTraining_Agility"
                               ".Reagent_ClassTraining_Agility",
            item_grants=[{'templateId': 'Reagent:Reagent_ClassTraining_Agility', 'quantity': 1},
                         {'templateId': 'Currency:Gold', 'quantity': 10000}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="3462326DE9BC4C40AB6F9842C7CD0CC1",
            dev_name="Workshop.L07.Page01.BuildingMaterials.03",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'Other', 'currencySubType': 'LaborPoints', 'regularPrice': 200,
                     'dynamicRegularPrice': -1, 'finalPrice': 100, 'saleType': 'AmountOff',
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 100}],
            daily_limit=1,
            meta_info=[{'key': 'WorkshopLevel', 'value': '7'}, {'key': 'MaxWorkshopLevel', 'value': '7'}],
            sort_priority=14,
            item_grants=[{'templateId': 'Reagent:Reagent_SupplyPoints_BuildingUpgrade', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="C2BFCE1B94FC43E09FEEAB703A1020B1",
            dev_name="Workshop.Page01.ClassTraining.32",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Misc_ShadowEssence', 'regularPrice': 5,
                 'dynamicRegularPrice': -1, 'finalPrice': 5, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                 'basePrice': 5}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': 'E7EEA718452DEDED4574BD9D51CE23A1',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': 'EBDAA0DC4684721269F4F29A5494519E',
                           'minQuantity': 1}],
            meta_info=[{'key': 'WorkshopLevel', 'value': '0'}, {'key': 'ForceShowFirstItemInGrant', 'value': 'true'}],
            display_asset_path="/Game/Loot/AccountItems/Reagents/Reagent_ClassTraining_Strength"
                               ".Reagent_ClassTraining_Strength",
            item_grants=[{'templateId': 'Reagent:Reagent_ClassTraining_Strength', 'quantity': 1},
                         {'templateId': 'Currency:Gold', 'quantity': 10000}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="8EA392B3527244AB92C81A6E5A0B1418",
            dev_name="Workshop.Page01.ClassTraining.02",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Misc_ShadowEssence', 'regularPrice': 2,
                 'dynamicRegularPrice': -1, 'finalPrice': 2, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                 'basePrice': 2}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '8550273E418A227A2CCFE7B8825472FF',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '689616B946BB3263CDD4F99952A3A666',
                           'minQuantity': 1}],
            meta_info=[{'key': 'WorkshopLevel', 'value': '0'}, {'key': 'ForceShowFirstItemInGrant', 'value': 'true'}],
            display_asset_path="/Game/Loot/AccountItems/Reagents/Reagent_ClassTraining_Agility"
                               ".Reagent_ClassTraining_Agility",
            item_grants=[{'templateId': 'Reagent:Reagent_ClassTraining_Agility', 'quantity': 1},
                         {'templateId': 'Currency:Gold', 'quantity': 10000}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="CB2331F8D2C04FC08ED86C1CA9F60ABC",
            dev_name="Workshop.Page01.ClassTraining.01",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Misc_ShadowEssence', 'regularPrice': 1,
                 'dynamicRegularPrice': -1, 'finalPrice': 1, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                 'basePrice': 1}],
            daily_limit=1,
            requirements=[{'requirementType': 'DenyOnFulfillment', 'requiredId': '8550273E418A227A2CCFE7B8825472FF',
                           'minQuantity': 1}],
            meta_info=[{'key': 'WorkshopLevel', 'value': '0'}, {'key': 'AffordOnly', 'value': 'true'},
                       {'key': 'ForceShowFirstItemInGrant', 'value': 'true'}],
            sort_priority=19,
            display_asset_path="/Game/Loot/AccountItems/Reagents/Reagent_ClassTraining_Agility"
                               ".Reagent_ClassTraining_Agility",
            item_grants=[{'templateId': 'Reagent:Reagent_ClassTraining_Agility', 'quantity': 1},
                         {'templateId': 'Currency:Gold', 'quantity': 10000}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="67874B020E8949A29A1B4EE00FFE5B2B",
            dev_name="Workshop.L01.Page01.BuildRandomGear.02",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Shard_Gear', 'regularPrice': 10,
                     'dynamicRegularPrice': -1, 'finalPrice': 10, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 10}],
            daily_limit=1,
            meta_info=[{'key': 'WorkshopLevel', 'value': '1'}],
            sort_priority=12,
            title="Build Random Weapon  (Rare)",
            description="Construct a random Rare weapon!",
            display_asset_path="/Game/UMG/Textures/HeroGear/T_Gear_Weapon_Random_02_Rare.T_Gear_Weapon_Random_02_Rare",
        ))
        self.catalog_entries.append(Offer(
            offer_id="8EA48D2163DE42D394B3AE2E192FD4D1",
            dev_name="Workshop.Page01.ClassTraining.26",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Misc_ShadowEssence', 'regularPrice': 2,
                 'dynamicRegularPrice': -1, 'finalPrice': 2, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                 'basePrice': 2}],
            daily_limit=1,
            requirements=[{'requirementType': 'RequireFulfillment', 'requiredId': '8550273E418A227A2CCFE7B8825472FF',
                           'minQuantity': 1},
                          {'requirementType': 'DenyOnFulfillment', 'requiredId': '689616B946BB3263CDD4F99952A3A666',
                           'minQuantity': 1}],
            meta_info=[{'key': 'WorkshopLevel', 'value': '0'}, {'key': 'ForceShowFirstItemInGrant', 'value': 'true'}],
            display_asset_path="/Game/Loot/AccountItems/Reagents/Reagent_ClassTraining_Strength"
                               ".Reagent_ClassTraining_Strength",
            item_grants=[{'templateId': 'Reagent:Reagent_ClassTraining_Strength', 'quantity': 1},
                         {'templateId': 'Currency:Gold', 'quantity': 10000}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="F3C70C0BDCDF4AD6B5CC49703466F2DB",
            dev_name="Workshop.L01.Page01.BuildWCHero.01",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_WC_Hero_TripleCombo',
                     'regularPrice': 100, 'dynamicRegularPrice': -1, 'finalPrice': 100,
                     'saleExpiration': '9999-12-31T23:59:59.999Z', 'basePrice': 100}],
            meta_info=[{'key': 'WorkshopLevel', 'value': '1'}, {'key': 'AffordOnly', 'value': 'true'}],
            sort_priority=4,
            item_grants=[{'templateId': 'Character:MartialArtist_SR2_Fire_TripleCombo_T04', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="FE1764674550435EA71F95C4DE11AC32",
            dev_name="Workshop.L01.Page01.BuildRxT.03",
            offer_type="StaticPrice",
            prices=[
                {'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_RXT_Parts_Small', 'regularPrice': 100,
                 'dynamicRegularPrice': -1, 'finalPrice': 100, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                 'basePrice': 100}],
            meta_info=[{'key': 'WorkshopLevel', 'value': '1'}, {'key': 'AffordOnly', 'value': 'true'}],
            sort_priority=5,
            item_grants=[{'templateId': 'Character:Warrior_SR2_Light_RoboGuy_T05', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="CB1B6DE6B938471392033377C59D07A1",
            dev_name="Workshop.L24.Page01.BuildRandomItem.12",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'Other', 'currencySubType': 'LaborPoints', 'regularPrice': 50,
                     'dynamicRegularPrice': -1, 'finalPrice': 50, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 50}],
            daily_limit=11,
            meta_info=[{'key': 'WorkshopLevel', 'value': '24'}, {'key': 'MaxWorkshopLevel', 'value': '25'}],
            sort_priority=20,
            title="Build Random Item",
            description="Construct a random item, with a chance to get a hero!",
        ))

    @classmethod
    async def init_storefront(cls) -> Self:
        """
        Initialise the Workshop storefront
        :return: The initialised Workshop storefront class
        """
        self: Workshop = cls()
        self.name = "Workshop"
        self.catalog_entries = []
        return self


class Loyalty(Storefront):
    """
    Class based system to handle the Loyalty storefront for the storefront catalog service
    """

    def __init__(self) -> None:
        """
        Initialise the Loyalty storefront class.
        This will setup the variables for the Loyalty storefront
        """
        super().__init__()

    async def update_storefront(self) -> None:
        """
        Update the storefront for the Loyalty storefront class with the latest data
        This rotation never changed
        :return: None
        """
        # temporary implementation
        self.catalog_entries.append(Offer(
            offer_id="AA3FFA0E094C458288F767E35252F9EF",
            dev_name="Loyalty.Core.07",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Loyalty', 'regularPrice': 1,
                     'dynamicRegularPrice': -1, 'finalPrice': 1, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 1}],
            sort_priority=108,
            item_grants=[{'templateId': 'Currency:Hammer', 'quantity': 10}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="056554B3FF0F418BB3552D4F5DB7492C",
            dev_name="Loyalty.Core.01",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Loyalty', 'regularPrice': 1,
                     'dynamicRegularPrice': -1, 'finalPrice': 1, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 1}],
            sort_priority=105,
            item_grants=[{'templateId': 'Reagent:Reagent_Shard_Dark', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="2D61B2E4BEC54B0C868AB5F4B6AB5DC2",
            dev_name="Loyalty.Core.11",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Loyalty', 'regularPrice': 5,
                     'dynamicRegularPrice': -1, 'finalPrice': 5, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 5}],
            sort_priority=124,
            item_grants=[{'templateId': 'Voucher:Voucher_Chest_Gold', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="EF704CF0A84043BCB11AD8F9ABA7CC7F",
            dev_name="Loyalty.Core.10",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Loyalty', 'regularPrice': 1,
                     'dynamicRegularPrice': -1, 'finalPrice': 1, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 1}],
            sort_priority=109,
            item_grants=[{'templateId': 'UpgradePotion:UpgradeMana', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="D3CB18AB960D498D96989D8B90269023",
            dev_name="Loyalty.Core.02",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Loyalty', 'regularPrice': 1,
                     'dynamicRegularPrice': -1, 'finalPrice': 1, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 1}],
            sort_priority=104,
            item_grants=[{'templateId': 'Reagent:Reagent_Shard_Fire', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="79E8E5F67DA7444D922FAFCD75DCEEF9",
            dev_name="Loyalty.Core.24",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Loyalty', 'regularPrice': 1,
                     'dynamicRegularPrice': -1, 'finalPrice': 1, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 1}],
            sort_priority=112,
            item_grants=[{'templateId': 'Reagent:Reagent_Foil', 'quantity': 10}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="E21DB557AA3944158DE9B1FDFCF26E7A",
            dev_name="Loyalty.Core.23",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Loyalty', 'regularPrice': 1,
                     'dynamicRegularPrice': -1, 'finalPrice': 1, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 1}],
            sort_priority=113,
            item_grants=[{'templateId': 'Currency:SkillXP', 'quantity': 1000}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="8D71F61D65704ADFB0AC44E632B1B0B4",
            dev_name="Loyalty.Core.09",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Loyalty', 'regularPrice': 1,
                     'dynamicRegularPrice': -1, 'finalPrice': 1, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 1}],
            sort_priority=107,
            item_grants=[{'templateId': 'Ore:Ore_Magicite', 'quantity': 10}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="DA55598A71C946CDBB5E06BC5D70B7B9",
            dev_name="Loyalty.Core.13",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Loyalty', 'regularPrice': 1,
                     'dynamicRegularPrice': -1, 'finalPrice': 1, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 1}],
            sort_priority=122,
            item_grants=[{'templateId': 'Reagent:Reagent_HeroMap_Elemental', 'quantity': 40}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="061580998D7E4B169085B020B158C76E",
            dev_name="Loyalty.Core.05",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Loyalty', 'regularPrice': 1,
                     'dynamicRegularPrice': -1, 'finalPrice': 1, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 1}],
            sort_priority=101,
            item_grants=[{'templateId': 'Reagent:Reagent_Shard_Water', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="DDB177DDFA4D41CE8E8C9F709D1C2A09",
            dev_name="Loyalty.Core.14",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Loyalty', 'regularPrice': 3,
                     'dynamicRegularPrice': -1, 'finalPrice': 3, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 3}],
            sort_priority=123,
            item_grants=[{'templateId': 'Reagent:Reagent_HeroMap_SuperRare', 'quantity': 4}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="5A897D6674364002915EDD91769EDE4A",
            dev_name="Loyalty.Core.19",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Loyalty', 'regularPrice': 10,
                     'dynamicRegularPrice': -1, 'finalPrice': 10, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 10}],
            sort_priority=115,
            item_grants=[{'templateId': 'Reagent:Reagent_RXT_Parts_Large', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="A09EFF312ACC4C0A9D8F137709879751",
            dev_name="Loyalty.Core.15",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Loyalty', 'regularPrice': 25,
                     'dynamicRegularPrice': -1, 'finalPrice': 25, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 25}],
            sort_priority=119,
            item_grants=[{'templateId': 'Reagent:Reagent_Misc_CeremonialArmor', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="42CEF781441C458E9E79E18DF15E7440",
            dev_name="Loyalty.Core.04",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Loyalty', 'regularPrice': 1,
                     'dynamicRegularPrice': -1, 'finalPrice': 1, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 1}],
            sort_priority=102,
            item_grants=[{'templateId': 'Reagent:Reagent_Shard_Nature', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="CED30C36836C4FFFACAC5034DDFBDFDC",
            dev_name="Loyalty.Core.22",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Loyalty', 'regularPrice': 1,
                     'dynamicRegularPrice': -1, 'finalPrice': 1, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 1}],
            sort_priority=106,
            item_grants=[{'templateId': 'Currency:Gold', 'quantity': 1000000}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="5965E83FA8984B46BB636994F7B0D604",
            dev_name="Loyalty.Core.20",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Loyalty', 'regularPrice': 1,
                     'dynamicRegularPrice': -1, 'finalPrice': 1, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 1}],
            sort_priority=114,
            item_grants=[{'templateId': 'Reagent:Reagent_RXT_Parts_Small', 'quantity': 10}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="87366DCFB6634722BEDD55AB3BE2959D",
            dev_name="Loyalty.Core.21",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Loyalty', 'regularPrice': 1,
                     'dynamicRegularPrice': -1, 'finalPrice': 1, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 1}],
            sort_priority=108,
            item_grants=[{'templateId': 'Reagent:Reagent_SupplyPoints_BuildingUpgrade', 'quantity': 5}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="A249D316D4C0451B84DD6ACB01B4B228",
            dev_name="Loyalty.Core.03",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Loyalty', 'regularPrice': 1,
                     'dynamicRegularPrice': -1, 'finalPrice': 1, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 1}],
            sort_priority=103,
            item_grants=[{'templateId': 'Reagent:Reagent_Shard_Light', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="8B2CE0BC32A94FBE877B47F1A74A405F",
            dev_name="Loyalty.Core.25",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Loyalty', 'regularPrice': 1,
                     'dynamicRegularPrice': -1, 'finalPrice': 1, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 1}],
            sort_priority=120,
            item_grants=[{'templateId': 'Reagent:Reagent_SupplyPoints_Elite', 'quantity': 20}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="F6B435AE52DD422CB67B43526BB5D4C7",
            dev_name="Loyalty.Core.16",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Loyalty', 'regularPrice': 7,
                     'dynamicRegularPrice': -1, 'finalPrice': 7, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 7}],
            sort_priority=118,
            item_grants=[{'templateId': 'Reagent:Reagent_Misc_CeremonialShield', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="CF0BEDCD785546FC899B910F34461ADC",
            dev_name="Loyalty.Core.17",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Loyalty', 'regularPrice': 2,
                     'dynamicRegularPrice': -1, 'finalPrice': 2, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 2}],
            sort_priority=117,
            item_grants=[{'templateId': 'Reagent:Reagent_Misc_CeremonialSword', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="84FD0A89046A457D8514EE88A0F6C4DD",
            dev_name="Loyalty.Core.12",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Loyalty', 'regularPrice': 3,
                     'dynamicRegularPrice': -1, 'finalPrice': 3, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 3}],
            sort_priority=121,
            item_grants=[{'templateId': 'Reagent:Reagent_HeroMap_Bronze', 'quantity': 2}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="5FB082AF85044E4198618888C61D2D09",
            dev_name="Loyalty.Core.06",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Loyalty', 'regularPrice': 1,
                     'dynamicRegularPrice': -1, 'finalPrice': 1, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 1}],
            sort_priority=100,
            item_grants=[{'templateId': 'Reagent:Reagent_Shared_T02', 'quantity': 75}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="29F46B6355AC4BFE832F178E6F9527F2",
            dev_name="Loyalty.Core.18",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Loyalty', 'regularPrice': 15,
                     'dynamicRegularPrice': -1, 'finalPrice': 15, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 15}],
            sort_priority=116,
            item_grants=[{'templateId': 'Reagent:Reagent_Shared_MysteryGoo', 'quantity': 1}],
        ))
        self.catalog_entries.append(Offer(
            offer_id="C27AAA587BF0405C9E4836E9F4D5F056",
            dev_name="Loyalty.Core.08",
            offer_type="StaticPrice",
            prices=[{'currencyType': 'GameItem', 'currencySubType': 'Reagent:Reagent_Loyalty', 'regularPrice': 1,
                     'dynamicRegularPrice': -1, 'finalPrice': 1, 'saleExpiration': '9999-12-31T23:59:59.999Z',
                     'basePrice': 1}],
            sort_priority=125,
            item_grants=[{'templateId': 'Currency:MtxGiveaway', 'quantity': 100}],
        ))

    @classmethod
    async def init_storefront(cls) -> Self:
        """
        Initialise the Loyalty storefront
        :return: The initialised Loyalty storefront class
        """
        self: Loyalty = cls()
        self.name = "Loyalty"
        self.catalog_entries = []
        return self
