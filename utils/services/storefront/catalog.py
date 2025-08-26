"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Class based system to handle the storefronts
"""
import datetime
import uuid
from typing_extensions import Any, Optional, Self

import utils.services.storefront.storefronts as storefronts
from utils.utils import get_nearest_12_hour_interval, format_time, get_current_12_hour_interval


class StoreCatalogue:
    """
    Class based system to handle the storefronts
    """

    def __init__(self) -> None:
        """
        Initialise the store catalogue class.
        This will setup the variables for the store catalogue
        """
        self.entity_tag: str = ""
        self.expiration: Optional[datetime.datetime] = None
        self.secret_shop_page_3: Optional[storefronts.SecretShopPage3] = None
        self.secret_shop_page_4: Optional[storefronts.SecretShopPage4] = None
        self.gem_store: Optional[storefronts.GemStore] = None
        self.secret_shop_page_2: Optional[storefronts.SecretShopPage2] = None
        self.weekly_challenge: Optional[storefronts.WeeklyChallenge] = None
        self.hero_store: Optional[storefronts.HeroStore] = None
        self.featured: Optional[storefronts.Featured] = None
        self.secret_shop: Optional[storefronts.SecretShop] = None
        self.magic_ticket: Optional[storefronts.MagicTicket] = None
        self.services: Optional[storefronts.Services] = None
        self.marketplace: Optional[storefronts.Marketplace] = None
        self.marketplace_page_3: Optional[storefronts.MarketplacePage3] = None
        self.marketplace_page_2: Optional[storefronts.MarketplacePage2] = None
        self.events: Optional[storefronts.Events] = None
        self.workshop: Optional[storefronts.Workshop] = None
        self.loyalty: Optional[storefronts.Loyalty] = None

    def __repr__(self) -> str:
        """
        Get the representation of the store catalogue class
        :return: The representation of the store catalogue class
        """
        return f"<ScheduledEvents>"

    def __str__(self) -> str:
        """
        Get the string of the store catalogue class
        :return: The string of the store catalogue class
        """
        return self.__repr__()

    def __dict__(self) -> dict[str, Any]:
        """
        Get the dictionary of the store catalogue class
        :return: The dictionary of the store catalogue class
        """
        # return dict or if the item is None, then an empty dict for that item
        return {
            "SecretShopPage3": self.secret_shop_page_3.__dict__() if self.secret_shop_page_3 is not None else {},
            "SecretShopPage4": self.secret_shop_page_4.__dict__() if self.secret_shop_page_4 is not None else {},
            "GemStore": self.gem_store.__dict__() if self.gem_store is not None else {},
            "SecretShopPage2": self.secret_shop_page_2.__dict__() if self.secret_shop_page_2 is not None else {},
            "WeeklyChalllenge": self.weekly_challenge.__dict__() if self.weekly_challenge is not None else {},
            "HeroStore": self.hero_store.__dict__() if self.hero_store is not None else {},
            "Featured": self.featured.__dict__() if self.featured is not None else {},
            "SecretShop": self.secret_shop.__dict__() if self.secret_shop is not None else {},
            "MagicTicket": self.magic_ticket.__dict__() if self.magic_ticket is not None else {},
            "Services": self.services.__dict__() if self.services is not None else {},
            "Marketplace": self.marketplace.__dict__() if self.marketplace is not None else {},
            "MarketplacePage3": self.marketplace_page_3.__dict__() if self.marketplace_page_3 is not None else {},
            "MarketplacePage2": self.marketplace_page_2.__dict__() if self.marketplace_page_2 is not None else {},
            "Events": self.events.__dict__() if self.events is not None else {},
            "Workshop": self.workshop.__dict__() if self.workshop is not None else {},
            "Loyalty": self.loyalty.__dict__() if self.loyalty is not None else {},
        }

    def __getitem__(self, key: str) -> Any:
        """
        Get the value of the key in the store catalogue class
        :param key: The key to get the value of
        :return: The value of the key in the store catalogue class
        """
        return getattr(self, key)

    def __setitem__(self, key: str, value: Any) -> None:
        """
        Set the value of the key in the store catalogue class
        :param key: The key to set the value of
        :param value: The value to set the key to
        :return: The value of the key in the store catalogue class
        """
        setattr(self, key, value)

    def __delitem__(self, key: str) -> None:
        """
        Delete the key in the store catalogue class
        :param key: The key to delete
        :return: The value of the key in the store catalogue class
        """
        delattr(self, key)

    def __len__(self) -> int:
        """
        Get the length of the store catalogue
        :return: The length of the store catalogue
        """
        return len(self.__dict__())

    @classmethod
    async def init_storefront(cls) -> Self:
        """
        Initialise the store catalogue
        :return: The initialised store catalogue class
        """
        self: StoreCatalogue = cls()
        self.secret_shop_page_3 = await storefronts.SecretShopPage3.init_storefront()
        self.secret_shop_page_4 = await storefronts.SecretShopPage4.init_storefront()
        self.gem_store = await storefronts.GemStore.init_storefront()
        self.secret_shop_page_2 = await storefronts.SecretShopPage2.init_storefront()
        self.weekly_challenge = await storefronts.WeeklyChallenge.init_storefront()
        self.hero_store = await storefronts.HeroStore.init_storefront()
        self.featured = await storefronts.Featured.init_storefront()
        self.secret_shop = await storefronts.SecretShop.init_storefront()
        self.magic_ticket = await storefronts.MagicTicket.init_storefront()
        self.services = await storefronts.Services.init_storefront()
        self.marketplace = await storefronts.Marketplace.init_storefront()
        self.marketplace_page_3 = await storefronts.MarketplacePage3.init_storefront()
        self.marketplace_page_2 = await storefronts.MarketplacePage2.init_storefront()
        self.events = await storefronts.Events.init_storefront()
        self.workshop = await storefronts.Workshop.init_storefront()
        self.loyalty = await storefronts.Loyalty.init_storefront()
        await self.update_storefronts()
        return self

    async def update_storefronts(self) -> dict[str, Any]:
        """
        Update the storefronts in the store catalogue class if expired
        :return: The storefronts in the store catalogue class
        """
        if self.expiration is None or self.expiration < datetime.datetime.now(datetime.UTC):
            # The ETag having double quotes is intentional
            self.entity_tag = f'"{str(uuid.uuid4().hex).upper()}|{await format_time(await get_current_12_hour_interval())}"'
            self.expiration = await get_nearest_12_hour_interval()
            await self.secret_shop_page_3.update_storefront()
            await self.secret_shop_page_4.update_storefront()
            await self.gem_store.update_storefront()
            await self.secret_shop_page_2.update_storefront()
            await self.weekly_challenge.update_storefront()
            await self.hero_store.update_storefront()
            await self.featured.update_storefront()
            await self.secret_shop.update_storefront()
            await self.magic_ticket.update_storefront()
            await self.services.update_storefront()
            await self.marketplace.update_storefront()
            await self.marketplace_page_3.update_storefront()
            await self.marketplace_page_2.update_storefront()
            await self.events.update_storefront()
            await self.workshop.update_storefront()
            await self.loyalty.update_storefront()
        return self.__dict__()

    async def get_offer_by_id(self, offer_id: str) -> Optional[storefronts.Offer]:
        """
        Get an offer by its ID from the store catalogue
        :param offer_id: The ID of the offer to get
        :return: The offer with the given ID or None if not found
        """
        storefronts_list = [
            self.secret_shop_page_3, self.secret_shop_page_4, self.gem_store, self.secret_shop_page_2,
            self.weekly_challenge, self.hero_store, self.featured, self.secret_shop, self.magic_ticket,
            self.services, self.marketplace, self.marketplace_page_3, self.marketplace_page_2, self.events,
            self.workshop, self.loyalty
        ]
        for storefront in storefronts_list:
            if storefront is not None:
                offer = await storefront.get_offer_by_id(offer_id)
                if offer is not None:
                    return offer
        return None
