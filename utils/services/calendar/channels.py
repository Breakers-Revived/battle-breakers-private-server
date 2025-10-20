"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Class based systems for each of the channels in the calendar service
"""
from typing_extensions import Any
import datetime

import aiofiles
import icalendar
import orjson
import recurring_ical_events
import sanic.log

from utils.utils import load_datatable, format_time


class State:
    """
    Class based system to handle states of a channel for the calendar service
    """

    def __init__(self) -> None:
        """
        Initialise the states class.
        This will set up the variables for the state
        """
        self.valid_from: str = ""
        self.active_events: list[str] = []
        self.state: dict[str, str | int | float | list | dict | bool] = {}

    def __repr__(self) -> str:
        """
        Get the representation of the state class
        :return: The representation of the state class
        """
        return f"<State>"

    def __str__(self) -> str:
        """
        Get the string of the state class
        :return: The string of the state class
        """
        return self.__repr__()

    def __dict__(self) -> dict[str, Any]:
        """
        Get the dictionary of the state class
        :return: The dictionary of the state class
        """
        return {
            "validFrom": self.valid_from,
            "activeEvents": self.active_events,
            "state": self.state
        }

    def __getitem__(self, key: str) -> Any:
        """
        Get the value of the key in the state class
        :param key: The key to get the value of
        :return: The value of the key in the state class
        """
        return getattr(self, key)

    def __setitem__(self, key: str, value: Any) -> None:
        """
        Set the value of the key in the state class
        :param key: The key to set the value of
        :param value: The value to set the key to
        :return: The value of the key in the state class
        """
        setattr(self, key, value)

    def __delitem__(self, key: str) -> None:
        """
        Delete the key in the state class
        :param key: The key to delete
        :return: The value of the key in the state class
        """
        delattr(self, key)

    def __len__(self) -> int:
        """
        Get the length of the state
        :return: The length of the state
        """
        return len(self.__dict__())


class Channel:
    """
    Class based system to handle a channel for the calendar service
    """

    def __init__(self) -> None:
        """
        Initialise the channel class.
        This will set up the variables for the channel
        """
        self.states: list[State] = [State()]
        self.cache_expire: str = "0021-01-01T00:00:000Z"

    def __repr__(self) -> str:
        """
        Get the representation of the channel class
        :return: The representation of the channel class
        """
        return f"<Channel>"

    def __str__(self) -> str:
        """
        Get the string of the channel class
        :return: The string of the channel class
        """
        return self.__repr__()

    def __dict__(self) -> dict[str, Any]:
        """
        Get the dictionary of the channel class
        :return: The dictionary of the channel class
        """
        return {
            "states": [self.states[0].__dict__()],  # states is a list of states, but there is only ever one state
            "cacheExpire": self.cache_expire
        }

    def __getitem__(self, key: str) -> Any:
        """
        Get the value of the key in the channel class
        :param key: The key to get the value of
        :return: The value of the key in the channel class
        """
        return getattr(self, key)

    def __setitem__(self, key: str, value: Any) -> None:
        """
        Set the value of the key in the channel class
        :param key: The key to set the value of
        :param value: The value to set the key to
        :return: The value of the key in the channel class
        """
        setattr(self, key, value)

    def __delitem__(self, key: str) -> None:
        """
        Delete the key in the channel class
        :param key: The key to delete
        :return: The value of the key in the channel class
        """
        delattr(self, key)

    def __len__(self) -> int:
        """
        Get the length of the channel
        :return: The length of the channel
        """
        return len(self.__dict__())

    def cache_expired(self) -> bool:
        """
        Determines if the cache is expired
        :return: True if the cache is expired
        """
        return datetime.datetime.now(datetime.UTC) > datetime.datetime.strptime(self.cache_expire,
                                                                                "%Y-%m-%dT%H:%M:%S.%fZ").replace(
            tzinfo=datetime.UTC)


class News(Channel):
    """
    Class based system to handle the news channel for the calendar service
    """

    def __init__(self) -> None:
        """
        Initialise the news channel class.
        This will set up the variables for the news channel
        """
        super().__init__()

    async def update_events(self) -> None:
        """
        Update the events for the news channel
        :return: None
        """
        sanic.log.logger.debug("Reading news ical file")
        async with aiofiles.open("res/wex/api/calendar/news.ics", "rb") as f:
            events = recurring_ical_events.of(icalendar.Calendar.from_ical(await f.read())).at(
                datetime.datetime.now(datetime.UTC)
            )
        self.states[0].state["activeNews"] = []
        for event in events:
            news_data = orjson.loads(event.get("DESCRIPTION"))
            sanic.log.logger.debug(f"Adding news data {news_data} to news channel")
            self.states[0].state["activeNews"].append({
                "uniqueId": f"{event.get('UID', '0@').split('@')[0]}[0]0",
                "widget": news_data.get("widget", ""),  # TODO: figure out the format
                "newsType": news_data.get("newsType", 0),
                "widgetParams": {
                    "titleText": news_data.get("titleText", {"en": ""}),
                    "bodyText": news_data.get("bodyText", {"en": ""}),
                    "foundInText": news_data.get("foundInText", {"en": ""}),
                    "linkMenu": news_data.get("linkMenu", ""),  # TODO: figure out the format
                    "linkSubMenuClass": news_data.get("linkSubMenuClass", ""),
                    "backgroundImageURL": news_data.get("backgroundImageURL", ""),
                }
            })
        self.states[0].valid_from = await format_time()
        self.cache_expire = await format_time(datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=2))
        sanic.log.logger.debug(f"Finished updating news channel, cache expires at {self.cache_expire}")


class LimitedTimeMode(Channel):
    """
    Class based system to handle the limited time mode channel for the calendar service
    """

    def __init__(self) -> None:
        """
        Initialise the limited time mode channel class.
        This will set up the variables for the limited time mode channel
        """
        super().__init__()

    async def update_events(self) -> None:
        """
        Update the events for the limited time mode channel
        :return: None
        """
        begin = await format_time(
            datetime.datetime.now(datetime.UTC).replace(hour=0, minute=0, second=0, microsecond=0) +
            datetime.timedelta(days=-datetime.datetime.now(datetime.UTC).weekday() + 2))
        end = await format_time(datetime.datetime.now(datetime.UTC).replace(hour=0, minute=0, second=0, microsecond=0) +
                                datetime.timedelta(days=7 - datetime.datetime.now(datetime.UTC).weekday() + 2))
        sanic.log.logger.debug(f"Populating LTM channel with weekly modes from {begin} to {end}")
        self.states[0].valid_from = await format_time()
        self.states[0].state = {
            "activeLTMs": [{
                "LTM_Event_ID": "Week1_LTM",
                "LTM_ID": "Endless_01",
                "PlayMode": {
                    "Mode": "DeepDungeons",
                    "Rules": [{
                        "Rule": "AllBosses",
                        "RuleDataValue": 0
                    }, {
                        "Rule": "StrongSpecial",
                        "RuleDataValue": 0
                    }, {
                        "Rule": "InsightHeroBonus",
                        "RuleDataValue": 0
                    }],
                    "Zones": [{
                        "ZoneId": "Zone.HauntedWoods.Map1",
                        "Difficulty": "Easy",
                        "completionLoot": "LTG.LTM.Endless.Completion.VeryLow"
                    }, {
                        "ZoneId": "Zone.EndlessDesert.Map2",
                        "Difficulty": "Easy",
                        "firstCompletionLoot": "LTG.LTM.Battlepass5_Week1.FirstCompletion",
                        "completionLoot": "LTG.LTM.Battlepass5_Week1.Endless.Low.Gear"
                    }, {
                        "ZoneId": "Zone.CollapsedSpire.Map3",
                        "Difficulty": "Easy",
                        "completionLoot": "LTG.LTM.Endless.Completion.Low"
                    }, {
                        "ZoneId": "Zone.BlessedPlains.Map1",
                        "Difficulty": "Easy",
                        "firstCompletionLoot": "LTG.LTM.Battlepass5_Week1.FirstCompletion",
                        "completionLoot": "LTG.LTM.Battlepass5_Week1.Endless.Low.Gear"
                    }, {
                        "ZoneId": "Zone.OasisOfLife.Map3",
                        "Difficulty": "Medium",
                        "completionLoot": "LTG.LTM.Endless.Completion.Medium"
                    }, {
                        "ZoneId": "Zone.MoltenCaverns.Map1",
                        "Difficulty": "Medium",
                        "firstCompletionLoot": "LTG.LTM.Battlepass5_Week1.FirstCompletion",
                        "completionLoot": "LTG.LTM.Battlepass5_Week1.Endless.Medium.Gear"
                    }, {
                        "ZoneId": "Zone.LeafyTreeland.Map5",
                        "Difficulty": "Hard",
                        "completionLoot": "LTG.LTM.Endless.Completion.High"
                    }, {
                        "ZoneId": "Zone.BurnyVolcano.Map2",
                        "Difficulty": "Hard",
                        "firstCompletionLoot": "LTG.LTM.Battlepass5_Week1.FirstCompletion",
                        "completionLoot": "LTG.LTM.Battlepass5_Week1.Endless.High.Gear"
                    }, {
                        "ZoneId": "Zone.FieldsOfDespair.Map1",
                        "Difficulty": "Nightmare",
                        "completionLoot": "LTG.LTM.Endless.Completion.VeryHigh"
                    }, {
                        "ZoneId": "Zone.AbyssalPrecipice.Map1",
                        "Difficulty": "Nightmare",
                        "firstCompletionLoot": "LTG.LTM.Battlepass5_Week1.FirstCompletion",
                        "completionLoot": "LTG.LTM.Battlepass5_Week1.Endless.VeryHigh.Gear"
                    }],
                    "ModeDataValue": 0,
                    "ImageIndex": 151
                },
                "modeNamedWeight": "Modes_Weekly",
                "ruleNamedWeights": ["Rules_AllBosses", "Rules_StrongSpecial", "Rules_InsightHeroBonus"],
                "availabilityBegin": begin,
                "availabilityEnd": end
            }, {
                "LTM_Event_ID": "Week1_LTM",
                "LTM_ID": "TimeAttack_01",
                "PlayMode": {
                    "Mode": "TimeAttack",
                    "Rules": [{
                        "Rule": "InsightHeroBonus",
                        "RuleDataValue": 0
                    }, {
                        "Rule": "MightyMinions",
                        "RuleDataValue": 0
                    }, {
                        "Rule": "AgilityHeroBonus",
                        "RuleDataValue": 0
                    }],
                    "Zones": [{
                        "ZoneId": "Zone.BurnyVolcano.Map1",
                        "Difficulty": "Nightmare",
                        "firstCompletionLoot": "LTG.LTM.Battlepass5_Week1.FirstCompletion",
                        "completionLoot": "LTG.LTM.Battlepass5_Week1.Completion",
                        "playBonusLoot": "LTG.LTM.TimeAttack.Completion.Bonus"
                    }],
                    "ModeDataValue": 70,
                    "ImageIndex": 58
                },
                "modeNamedWeight": "Modes_DuelsDoubleCommander",
                "ruleNamedWeights": ["Rules_InsightHeroBonus", "Rules_MightyMinions", "Rules_AgilityHeroBonus"],
                "availabilityBegin": begin,
                "availabilityEnd": end
            }, {
                "LTM_Event_ID": "Week1_LTM",
                "LTM_ID": "TurnAttack_01",
                "PlayMode": {
                    "Mode": "TurnAttack",
                    "Rules": [{
                        "Rule": "FullClearRooms",
                        "RuleDataValue": 0
                    }, {
                        "Rule": "EnduranceHeroBonus",
                        "RuleDataValue": 0
                    }, {
                        "Rule": "StrengthHeroBonus",
                        "RuleDataValue": 0
                    }],
                    "Zones": [{
                        "ZoneId": "Zone.HauntedWoods.Map3",
                        "Difficulty": "Nightmare",
                        "firstCompletionLoot": "LTG.LTM.Battlepass5_Week1.FirstCompletion",
                        "completionLoot": "LTG.LTM.Battlepass5_Week1.Completion"
                    }],
                    "ModeDataValue": 175,
                    "ImageIndex": 162
                },
                "modeNamedWeight": "Modes_Duels3v3",
                "ruleNamedWeights": ["Rules_FullClearRooms", "Rules_EnduranceHeroBonus", "Rules_StrengthHeroBonus"],
                "availabilityBegin": begin,
                "availabilityEnd": end
            }, {
                "LTM_Event_ID": "Week1_LTM",
                "LTM_ID": "PvP_Duels",
                "PlayMode": {
                    "Mode": "PvP",
                    "Rules": [{
                        "Rule": "AgilityHeroBonus",
                        "RuleDataValue": 0
                    }, {
                        "Rule": "EnduranceHeroBonus",
                        "RuleDataValue": 0
                    }, {
                        "Rule": "EnemyManaBonus",
                        "RuleDataValue": 0
                    }],
                    "Zones": [{
                        "ZoneId": "Zone.Event.GrandArena.Aux.Battleford.Map1",
                        "Difficulty": "Easy",
                        "firstCompletionLoot": "LTG.LTM.PvP.FirstCompletion",
                        "completionLoot": "LTG.LTM.PvP.Completion"
                    }],
                    "ModeDataValue": 0,
                    "ImageIndex": 97
                },
                "ruleNamedWeights": ["Rules_AgilityHeroBonus", "Rules_EnduranceHeroBonus", "Rules_EnemyManaBonus"],
                "availabilityBegin": begin,
                "availabilityEnd": end
            }, {
                "LTM_Event_ID": "Week1_LTM",
                "LTM_ID": "Campaign01",
                "PlayMode": {
                    "Mode": "Campaign01",
                    "Rules": [{
                        "Rule": "EnemyManaBonus",
                        "RuleDataValue": 0
                    }, {
                        "Rule": "StrongSpecial",
                        "RuleDataValue": 0
                    }, {
                        "Rule": "FastCoolDown",
                        "RuleDataValue": 0
                    }, {
                        "Rule": "BlockSummonPets",
                        "RuleDataValue": 0
                    }],
                    "Zones": [],
                    "ModeDataValue": 0,
                    "ImageIndex": 0
                },
                "modeNamedWeight": "Modes_Campaign",
                "ruleNamedWeights": ["Rules_EnemyManaBonus", "Rules_StrongSpecial", "Rules_FastCoolDown",
                                     "Rules_Pets_BlockSummon"]
            }, {
                "LTM_Event_ID": "Week1_LTM",
                "LTM_ID": "Campaign02",
                "PlayMode": {
                    "Mode": "Campaign02",
                    "Rules": [{
                        "Rule": "AllBosses",
                        "RuleDataValue": 0
                    }, {
                        "Rule": "StrongEnemyATK",
                        "RuleDataValue": 0
                    }, {
                        "Rule": "StrongSpecial",
                        "RuleDataValue": 0
                    }, {
                        "Rule": "ItemSlots",
                        "RuleDataValue": 0
                    }],
                    "Zones": [],
                    "ModeDataValue": 0,
                    "ImageIndex": 0
                },
                "modeNamedWeight": "Modes_Campaign",
                "ruleNamedWeights": ["Rules_AllBosses", "Rules_StrongEnemyATK", "Rules_StrongSpecial",
                                     "Rules_ItemSlots"]
            }, {
                "LTM_Event_ID": "Week1_LTM",
                "LTM_ID": "Campaign03",
                "PlayMode": {
                    "Mode": "Campaign03",
                    "Rules": [{
                        "Rule": "ItemSlots",
                        "RuleDataValue": 0
                    }, {
                        "Rule": "InsightHeroBonus",
                        "RuleDataValue": 0
                    }, {
                        "Rule": "StrengthHeroBonus",
                        "RuleDataValue": 0
                    }, {
                        "Rule": "FastCoolDown",
                        "RuleDataValue": 0
                    }, {
                        "Rule": "EnemyManaBonus",
                        "RuleDataValue": 0
                    }],
                    "Zones": [],
                    "ModeDataValue": 0,
                    "ImageIndex": 0
                },
                "modeNamedWeight": "Modes_Campaign",
                "ruleNamedWeights": ["Rules_ItemSlots", "Rules_InsightHeroBonus", "Rules_StrengthHeroBonus",
                                     "Rules_FastCoolDown", "Rules_EnemyManaBonus"]
            }, {
                "LTM_Event_ID": "Week1_LTM",
                "LTM_ID": "Campaign04",
                "PlayMode": {
                    "Mode": "Campaign04",
                    "Rules": [{
                        "Rule": "StrengthHeroBonus",
                        "RuleDataValue": 0
                    }, {
                        "Rule": "StrongSpecial",
                        "RuleDataValue": 0
                    }],
                    "Zones": [],
                    "ModeDataValue": 0,
                    "ImageIndex": 0
                },
                "modeNamedWeight": "Modes_Campaign",
                "ruleNamedWeights": ["Rules_StrengthHeroBonus", "Rules_StrongSpecial"]
            }, {
                "LTM_Event_ID": "Week1_LTM",
                "LTM_ID": "Campaign05",
                "PlayMode": {
                    "Mode": "Campaign05",
                    "Rules": [{
                        "Rule": "AgilityHeroBonus",
                        "RuleDataValue": 0
                    }, {
                        "Rule": "StrongEnemyATK",
                        "RuleDataValue": 0
                    }, {
                        "Rule": "DoubleCommander",
                        "RuleDataValue": 0
                    }],
                    "Zones": [],
                    "ModeDataValue": 0,
                    "ImageIndex": 0
                },
                "modeNamedWeight": "Modes_Campaign",
                "ruleNamedWeights": ["Rules_AgilityHeroBonus", "Rules_StrongEnemyATK", "Rules_Commander_Double"]
            }, {
                "LTM_Event_ID": "Week1_LTM",
                "LTM_ID": "Campaign06",
                "PlayMode": {
                    "Mode": "Campaign06",
                    "Rules": [{
                        "Rule": "StrongEnemyATK",
                        "RuleDataValue": 0
                    }, {
                        "Rule": "FastCoolDown",
                        "RuleDataValue": 0
                    }, {
                        "Rule": "StrengthHeroBonus",
                        "RuleDataValue": 0
                    }, {
                        "Rule": "ItemSlots",
                        "RuleDataValue": 0
                    }],
                    "Zones": [],
                    "ModeDataValue": 0,
                    "ImageIndex": 0
                },
                "modeNamedWeight": "Modes_Campaign",
                "ruleNamedWeights": ["Rules_StrongEnemyATK", "Rules_FastCoolDown", "Rules_StrengthHeroBonus",
                                     "Rules_ItemSlots"]
            }, {
                "LTM_Event_ID": "Week1_LTM",
                "LTM_ID": "Campaign07",
                "PlayMode": {
                    "Mode": "Campaign07",
                    "Rules": [{
                        "Rule": "MightyMinions",
                        "RuleDataValue": 0
                    }, {
                        "Rule": "FullClearRooms",
                        "RuleDataValue": 0
                    }, {
                        "Rule": "ItemSlots",
                        "RuleDataValue": 0
                    }, {
                        "Rule": "EnduranceHeroBonus",
                        "RuleDataValue": 0
                    }],
                    "Zones": [],
                    "ModeDataValue": 0,
                    "ImageIndex": 0
                },
                "modeNamedWeight": "Modes_Campaign",
                "ruleNamedWeights": ["Rules_MightyMinions", "Rules_FullClearRooms", "Rules_ItemSlots",
                                     "Rules_EnduranceHeroBonus"]
            }, {
                "LTM_Event_ID": "Week1_LTM",
                "LTM_ID": "Campaign08",
                "PlayMode": {
                    "Mode": "Campaign08",
                    "Rules": [{
                        "Rule": "ItemSlots",
                        "RuleDataValue": 0
                    }, {
                        "Rule": "EnemyManaBonus",
                        "RuleDataValue": 0
                    }, {
                        "Rule": "AgilityHeroBonus",
                        "RuleDataValue": 0
                    }],
                    "Zones": [],
                    "ModeDataValue": 0,
                    "ImageIndex": 0
                },
                "modeNamedWeight": "Modes_Campaign",
                "ruleNamedWeights": ["Rules_ItemSlots", "Rules_EnemyManaBonus", "Rules_AgilityHeroBonus"]
            }, {
                "LTM_Event_ID": "Week1_LTM",
                "LTM_ID": "Campaign09",
                "PlayMode": {
                    "Mode": "Campaign09",
                    "Rules": [{
                        "Rule": "StrongSpecial",
                        "RuleDataValue": 0
                    }, {
                        "Rule": "StrongEnemyATK",
                        "RuleDataValue": 0
                    }, {
                        "Rule": "MightyMinions",
                        "RuleDataValue": 0
                    }, {
                        "Rule": "DoubleCommander",
                        "RuleDataValue": 0
                    }],
                    "Zones": [],
                    "ModeDataValue": 0,
                    "ImageIndex": 0
                },
                "modeNamedWeight": "Modes_Campaign",
                "ruleNamedWeights": ["Rules_StrongSpecial", "Rules_StrongEnemyATK", "Rules_MightyMinions",
                                     "Rules_Commander_Double"]
            }, {
                "LTM_Event_ID": "Week1_LTM",
                "LTM_ID": "Campaign10",
                "PlayMode": {
                    "Mode": "Campaign10",
                    "Rules": [{
                        "Rule": "StrengthHeroBonus",
                        "RuleDataValue": 0
                    }, {
                        "Rule": "StrongSpecial",
                        "RuleDataValue": 0
                    }],
                    "Zones": [],
                    "ModeDataValue": 0,
                    "ImageIndex": 0
                },
                "modeNamedWeight": "Modes_Campaign",
                "ruleNamedWeights": ["Rules_StrengthHeroBonus", "Rules_StrongSpecial"]
            }, {
                "LTM_Event_ID": "Week1_LTM",
                "LTM_ID": "Campaign11",
                "PlayMode": {
                    "Mode": "Campaign11",
                    "Rules": [{
                        "Rule": "ItemSlots",
                        "RuleDataValue": 0
                    }, {
                        "Rule": "AgilityHeroBonus",
                        "RuleDataValue": 0
                    }],
                    "Zones": [],
                    "ModeDataValue": 0,
                    "ImageIndex": 0
                },
                "modeNamedWeight": "Modes_Campaign",
                "ruleNamedWeights": ["Rules_ItemSlots", "Rules_AgilityHeroBonus"]
            }, {
                "LTM_Event_ID": "Week1_LTM",
                "LTM_ID": "Campaign12",
                "PlayMode": {
                    "Mode": "Campaign12",
                    "Rules": [{
                        "Rule": "MightyMinions",
                        "RuleDataValue": 0
                    }, {
                        "Rule": "AgilityHeroBonus",
                        "RuleDataValue": 0
                    }, {
                        "Rule": "StrongEnemyATK",
                        "RuleDataValue": 0
                    }, {
                        "Rule": "ItemSlots",
                        "RuleDataValue": 0
                    }],
                    "Zones": [],
                    "ModeDataValue": 0,
                    "ImageIndex": 0
                },
                "modeNamedWeight": "Modes_Campaign",
                "ruleNamedWeights": ["Rules_MightyMinions", "Rules_AgilityHeroBonus", "Rules_StrongEnemyATK",
                                     "Rules_ItemSlots"]
            }, {
                "LTM_Event_ID": "Week1_LTM",
                "LTM_ID": "Campaign13",
                "PlayMode": {
                    "Mode": "Campaign13",
                    "Rules": [{
                        "Rule": "StrongEnemyATK",
                        "RuleDataValue": 0
                    }, {
                        "Rule": "ItemSlots",
                        "RuleDataValue": 0
                    }, {
                        "Rule": "AllBosses",
                        "RuleDataValue": 0
                    }, {
                        "Rule": "EnemyManaBonus",
                        "RuleDataValue": 0
                    }],
                    "Zones": [],
                    "ModeDataValue": 0,
                    "ImageIndex": 0
                },
                "modeNamedWeight": "Modes_Campaign",
                "ruleNamedWeights": ["Rules_StrongEnemyATK", "Rules_ItemSlots", "Rules_AllBosses",
                                     "Rules_EnemyManaBonus"]
            }, {
                "LTM_Event_ID": "Week1_LTM",
                "LTM_ID": "Campaign14",
                "PlayMode": {
                    "Mode": "Campaign14",
                    "Rules": [{
                        "Rule": "StrongSpecial",
                        "RuleDataValue": 0
                    }, {
                        "Rule": "StrongEnemyATK",
                        "RuleDataValue": 0
                    }, {
                        "Rule": "FullClearRooms",
                        "RuleDataValue": 0
                    }],
                    "Zones": [],
                    "ModeDataValue": 0,
                    "ImageIndex": 0
                },
                "modeNamedWeight": "Modes_Campaign",
                "ruleNamedWeights": ["Rules_StrongSpecial", "Rules_StrongEnemyATK", "Rules_FullClearRooms"]
            }, {
                "LTM_Event_ID": "Week1_LTM",
                "LTM_ID": "Campaign15",
                "PlayMode": {
                    "Mode": "Campaign15",
                    "Rules": [{
                        "Rule": "EnemyManaBonus",
                        "RuleDataValue": 0
                    }, {
                        "Rule": "StrengthHeroBonus",
                        "RuleDataValue": 0
                    }, {
                        "Rule": "AllBosses",
                        "RuleDataValue": 0
                    }, {
                        "Rule": "StrongEnemyATK",
                        "RuleDataValue": 0
                    }],
                    "Zones": [],
                    "ModeDataValue": 0,
                    "ImageIndex": 0
                },
                "modeNamedWeight": "Modes_Campaign",
                "ruleNamedWeights": ["Rules_EnemyManaBonus", "Rules_StrengthHeroBonus", "Rules_AllBosses",
                                     "Rules_StrongEnemyATK"]
            }, {
                "LTM_Event_ID": "Week1_LTM",
                "LTM_ID": "Campaign16",
                "PlayMode": {
                    "Mode": "Campaign16",
                    "Rules": [{
                        "Rule": "EnemyManaBonus",
                        "RuleDataValue": 0
                    }, {
                        "Rule": "ItemSlots",
                        "RuleDataValue": 0
                    }, {
                        "Rule": "EnduranceHeroBonus",
                        "RuleDataValue": 0
                    }],
                    "Zones": [],
                    "ModeDataValue": 0,
                    "ImageIndex": 0
                },
                "modeNamedWeight": "Modes_Campaign",
                "ruleNamedWeights": ["Rules_EnemyManaBonus", "Rules_ItemSlots", "Rules_EnduranceHeroBonus"]
            }, {
                "LTM_Event_ID": "Week1_LTM",
                "LTM_ID": "Campaign17",
                "PlayMode": {
                    "Mode": "Campaign17",
                    "Rules": [{
                        "Rule": "EnduranceHeroBonus",
                        "RuleDataValue": 0
                    }, {
                        "Rule": "MightyMinions",
                        "RuleDataValue": 0
                    }],
                    "Zones": [],
                    "ModeDataValue": 0,
                    "ImageIndex": 0
                },
                "modeNamedWeight": "Modes_Campaign",
                "ruleNamedWeights": ["Rules_EnduranceHeroBonus", "Rules_MightyMinions"]
            }, {
                "LTM_Event_ID": "Week1_LTM",
                "LTM_ID": "Campaign18",
                "PlayMode": {
                    "Mode": "Campaign18",
                    "Rules": [{
                        "Rule": "ItemSlots",
                        "RuleDataValue": 0
                    }, {
                        "Rule": "EnemyManaBonus",
                        "RuleDataValue": 0
                    }, {
                        "Rule": "DoubleCommander",
                        "RuleDataValue": 0
                    }],
                    "Zones": [],
                    "ModeDataValue": 0,
                    "ImageIndex": 0
                },
                "modeNamedWeight": "Modes_Campaign",
                "ruleNamedWeights": ["Rules_ItemSlots", "Rules_EnemyManaBonus", "Rules_Commander_Double"]
            }, {
                "LTM_Event_ID": "Week1_LTM",
                "LTM_ID": "Campaign19",
                "PlayMode": {
                    "Mode": "Campaign19",
                    "Rules": [{
                        "Rule": "ItemSlots",
                        "RuleDataValue": 0
                    }, {
                        "Rule": "EnduranceHeroBonus",
                        "RuleDataValue": 0
                    }, {
                        "Rule": "AllCommander",
                        "RuleDataValue": 0
                    }],
                    "Zones": [],
                    "ModeDataValue": 0,
                    "ImageIndex": 0
                },
                "modeNamedWeight": "Modes_Campaign",
                "ruleNamedWeights": ["Rules_ItemSlots", "Rules_EnduranceHeroBonus", "Rules_Commander_All"]
            }, {
                "LTM_Event_ID": "Week1_LTM",
                "LTM_ID": "Campaign20",
                "PlayMode": {
                    "Mode": "Campaign20",
                    "Rules": [{
                        "Rule": "FullClearRooms",
                        "RuleDataValue": 0
                    }, {
                        "Rule": "EnemyManaBonus",
                        "RuleDataValue": 0
                    }, {
                        "Rule": "FastCoolDown",
                        "RuleDataValue": 0
                    }, {
                        "Rule": "MightyMinions",
                        "RuleDataValue": 0
                    }, {
                        "Rule": "AllBosses",
                        "RuleDataValue": 0
                    }],
                    "Zones": [],
                    "ModeDataValue": 0,
                    "ImageIndex": 0
                },
                "modeNamedWeight": "Modes_Campaign",
                "ruleNamedWeights": ["Rules_FullClearRooms", "Rules_EnemyManaBonus", "Rules_FastCoolDown",
                                     "Rules_MightyMinions", "Rules_AllBosses"]
            }, {
                "LTM_Event_ID": "Week1_LTM",
                "LTM_ID": "Campaign21",
                "PlayMode": {
                    "Mode": "Campaign21",
                    "Rules": [{
                        "Rule": "FullClearRooms",
                        "RuleDataValue": 0
                    }, {
                        "Rule": "ItemSlots",
                        "RuleDataValue": 0
                    }, {
                        "Rule": "MightyMinions",
                        "RuleDataValue": 0
                    }, {
                        "Rule": "AgilityHeroBonus",
                        "RuleDataValue": 0
                    }],
                    "Zones": [],
                    "ModeDataValue": 0,
                    "ImageIndex": 0
                },
                "modeNamedWeight": "Modes_Campaign",
                "ruleNamedWeights": ["Rules_FullClearRooms", "Rules_ItemSlots", "Rules_MightyMinions",
                                     "Rules_AgilityHeroBonus"]
            }, {
                "LTM_Event_ID": "Week1_LTM",
                "LTM_ID": "Campaign22",
                "PlayMode": {
                    "Mode": "Campaign22",
                    "Rules": [{
                        "Rule": "FullClearRooms",
                        "RuleDataValue": 0
                    }, {
                        "Rule": "StrongEnemyATK",
                        "RuleDataValue": 0
                    }, {
                        "Rule": "MightyMinions",
                        "RuleDataValue": 0
                    }, {
                        "Rule": "FastCoolDown",
                        "RuleDataValue": 0
                    }],
                    "Zones": [],
                    "ModeDataValue": 0,
                    "ImageIndex": 0
                },
                "modeNamedWeight": "Modes_Campaign",
                "ruleNamedWeights": ["Rules_FullClearRooms", "Rules_StrongEnemyATK", "Rules_MightyMinions",
                                     "Rules_FastCoolDown"]
            }],
            "eventInstanceId": "$EVENT_INSTANCE_ID"
        }
        self.cache_expire = await format_time(datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=2))
        sanic.log.logger.debug(f"Finished updating LTM channel, cache expires at {self.cache_expire}")


class Marketing(Channel):
    """
    Class based system to handle the marketing channel for the calendar service
    """

    def __init__(self) -> None:
        """
        Initialise the marketing channel class.
        This will set up the variables for the marketing channel
        """
        super().__init__()

    async def update_events(self) -> None:
        """
        Update the events for the marketing channel
        :return: None
        """
        self.states[0].valid_from = await format_time()
        self.states[0].state = {
            "affiliateSelectionEndDate": "9999-12-31T23:59:59.999Z"
        }
        self.cache_expire = await format_time(datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=2))
        sanic.log.logger.debug(f"Finished updating marketing channel, cache expires at {self.cache_expire}")


class RotationalContent(Channel):
    """
    Class based system to handle the rotational content channel for the calendar service
    """

    def __init__(self) -> None:
        """
        Initialise the rotational content channel class.
        This will set up the variables for the rotational content channel
        """
        super().__init__()

    async def update_events(self) -> None:
        """
        Update the events for the rotational content channel
        :return: None
        """
        self.states[0].valid_from = await format_time()
        # noinspection PyDictCreation
        self.states[0].state = {
            "activeZones": [],
            "activeEvents": [],
            "preregRewardZones": [],
            "heroStoreEnd": await format_time(
                datetime.datetime.now(datetime.UTC).replace(hour=0, minute=0, second=0,
                                                            microsecond=0) + datetime.timedelta(
                    days=-datetime.datetime.now(datetime.UTC).weekday(), weeks=1)),
            "purchasingEventId": ""
        }
        self.states[0].state["activeZones"] = [{
            "sortPriority": 800,
            "zoneId": "Zone.Event.GrandArena.Aux.Battleford.Map1",
            "maxRuns": -1,
            "resetCostMtx": 0,
            "flags": ["IsSpecialEvent"],
            "eventId": "Event.GrandArena",
            "dynamicTier": 1,
            "dynamicGoldTier": 1,
            "dynamicWorldLevel": -1,
            "expiresAt": "2026-01-01T00:00:00Z",
            "eventKey": "37m008vr790voua5ie1g0s0pqg[0]0+0"
        }, {
            "sortPriority": 800,
            "zoneId": "Zone.Pvp.Sparring1.Map1",
            "maxRuns": -1,
            "resetCostMtx": 0,
            "flags": ["IsSpecialEvent"],
            "eventId": "Event.GrandArena",
            "dynamicTier": -1,
            "dynamicGoldTier": -1,
            "dynamicWorldLevel": -1,
            "expiresAt": "2026-01-01T00:00:00Z",
            "eventKey": "37m008vr790voua5ie1g0s0pqg[1]0+0"
        }, {
            "sortPriority": -100,
            "zoneId": "Zone.Event.WK.TKVoucher1.Light.Map1",
            "maxRuns": 8,
            "resetCostMtx": 500,
            "flags": [],
            "dynamicTier": -1,
            "dynamicGoldTier": -1,
            "dynamicWorldLevel": -1,
            "expiresAt": "2026-12-31T00:00:00Z",
            "eventKey": "021lv6t1k5dmuuokgcr3cr1m0s[0]199+0"
        }, {
            "sortPriority": 0,
            "zoneId": "Zone.HallsOfFadedGlory.MapDark1",
            "maxRuns": 1,
            "resetCostMtx": 0,
            "flags": [],
            "dynamicTier": -1,
            "dynamicGoldTier": -1,
            "dynamicWorldLevel": -1,
            "expiresAt": "2026-12-31T00:00:00Z",
            "eventKey": "90661350-C3AE-475C-99C3-877CA7930AA1[0]173+0"
        }, {
            "sortPriority": 0,
            "zoneId": "Zone.HallsOfFadedGlory.MapGold1",
            "maxRuns": 1,
            "resetCostMtx": 0,
            "flags": [],
            "dynamicTier": 1,
            "dynamicGoldTier": 3,
            "dynamicWorldLevel": -1,
            "expiresAt": "2026-12-31T00:00:00Z",
            "eventKey": "6tojdi2dqvmqbeo0st5bvr919m[0]9999+0"
        }]
        sanic.log.logger.debug("Reading battle pass ical file")
        async with aiofiles.open("res/wex/api/calendar/battlepass.ics", "rb") as f:
            events = recurring_ical_events.of(icalendar.Calendar.from_ical(await f.read())).at(
                datetime.datetime.now(datetime.UTC)
            )
        end_date = events[-1].get("DTEND").dt
        event_data = await load_datatable(events[-1].get("DESCRIPTION")[1:])
        self.states[0].state["activeEvents"] = [{
            "sortPriority": 999,
            "eventAsset": f"{events[-1].get('DESCRIPTION').replace('/Content', '/Game')}."
                          f"{events[-1].get('DESCRIPTION').split('/')[-1]}",
            "eventId": event_data[0].get("Properties").get("EventId"),
            "expiresAt": await format_time(end_date)
        }]
        self.states[0].state["purchasingEventId"] = f"Event.{event_data[0].get('Name').split('_')[-1]}"
        sanic.log.logger.info(
            f"Current battle pass event set to {self.states[0].state['activeEvents'][0]['eventId']} (Currency {self.states[0].state['purchasingEventId']}), ending at {self.states[0].state['activeEvents'][0]['expiresAt']}")
        self.cache_expire = await format_time(datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=2))
        sanic.log.logger.debug(f"Finished updating rotational content channel, cache expires at {self.cache_expire}")


class FeaturedStoresMcp(Channel):
    """
    Class based system to handle the featured stores mcp channel for the calendar service
    """

    def __init__(self) -> None:
        """
        Initialise the featured stores mcp channel class.
        This will set up the variables for the featured stores mcp channel
        """
        super().__init__()

    async def update_events(self) -> None:
        """
        Update the events for the featured stores mcp channel
        :return: None
        """
        # This channel is not used by any version of the game
        self.states[0].valid_from = await format_time()
        self.states[0].state = {
            "activePurchaseLimitingEventIds": [],
            "storefront": {}
        }
        self.cache_expire = await format_time(datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=2))
        sanic.log.logger.debug(f"Finished updating featured stores mcp channel, cache expires at {self.cache_expire}")


class WeeklyChallenge(Channel):
    """
    Class based system to handle the weekly challenge mcp channel for the calendar service
    """

    def __init__(self) -> None:
        """
        Initialise the weekly challenge mcp channel class.
        This will set up the variables for the weekly challenge mcp channel
        """
        super().__init__()

    async def update_events(self) -> None:
        """
        Update the events for the weekly challenge channel
        :return: None
        """
        # {
        #     "zoneId": "Zone.Event.WC.Daily.BossTrio.Map1",
        #     "availabilityBegin": "2022-12-26T00:00:00.000Z",
        #     "availabilityEnd": "2023-01-02T00:00:00.000Z",
        #     "minAccountLevel": 1,
        #     "maxAccountLevel": 2147483647,
        #     "requirements": {
        #         "maxPartySize": 5,
        #         "minPartySize": 1,
        #         "requirements": [{
        #             "count": 1,
        #             "heroClass": "Archer",
        #             "heroElement": "None"
        #         }],
        #         "excludeClasses": [],
        #         "excludeElements": []
        #     }
        # }
        # {
        #     "zoneId": "Zone.Event.WC.Weekend.BossSuper.1.Blackguard.Map1",
        #     "availabilityBegin": "2022-12-26T00:00:00.000Z",
        #     "availabilityEnd": "2023-01-02T00:00:00.000Z",
        #     "minAccountLevel": 1,
        #     "maxAccountLevel": 2147483647,
        #     "runLimit": 1
        # }
        end_date: datetime.datetime | None = None
        self.states[0].valid_from = await format_time()
        # noinspection PyDictCreation
        self.states[0].state = {
            "phases": [],
            "activePhases": ["Weekend", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
            "eventInstanceId": "70ruue8l0oma4lm9egb3o9koga[0]170",
            "bossZone": {},
            "namedWeights": ""
        }
        # TODO: Implement phases + boss zone + named weights + event instance id into the calendar, then the state
        self.states[0].state["phases"] = [{
            "zoneId": "Zone.Event.WC.Daily.BossTrio.Map1",
            "availabilityBegin": "2022-12-26T00:00:00.000Z",
            "availabilityEnd": "9999-12-31T23:59:59.999Z",
            "minAccountLevel": 1,
            "maxAccountLevel": 2147483647,
            "requirements": {
                "maxPartySize": 5,
                "minPartySize": 1,
                "requirements": [{
                    "count": 1,
                    "heroClass": "Archer",
                    "heroElement": "None"
                }],
                "excludeClasses": [],
                "excludeElements": []
            }
        }, {
            "zoneId": "Zone.Event.WC.Daily.SuperBoss.Map1",
            "availabilityBegin": "2022-12-26T00:00:00.000Z",
            "availabilityEnd": "9999-12-31T23:59:59.999Z",
            "minAccountLevel": 1,
            "maxAccountLevel": 2147483647,
            "requirements": {
                "maxPartySize": 5,
                "minPartySize": 1,
                "requirements": [{
                    "count": 1,
                    "heroClass": "Ninja",
                    "heroElement": "None"
                }, {
                    "count": 1,
                    "heroClass": "AnyClass",
                    "heroElement": "Dark"
                }],
                "excludeClasses": [],
                "excludeElements": []
            }
        }, {
            "zoneId": "Zone.Event.WC.Daily.BossTrio.Map1",
            "availabilityBegin": "2022-12-26T00:00:00.000Z",
            "availabilityEnd": "9999-12-31T23:59:59.999Z",
            "minAccountLevel": 1,
            "maxAccountLevel": 2147483647,
            "requirements": {
                "maxPartySize": 5,
                "minPartySize": 1,
                "requirements": [{
                    "count": 1,
                    "heroClass": "AnyClass",
                    "heroElement": "Dark"
                }],
                "excludeClasses": [],
                "excludeElements": []
            }
        }, {
            "zoneId": "Zone.Event.WC.Daily.BossTrio.Map1",
            "availabilityBegin": "2022-12-26T00:00:00.000Z",
            "availabilityEnd": "9999-12-31T23:59:59.999Z",
            "minAccountLevel": 1,
            "maxAccountLevel": 2147483647,
            "requirements": {
                "maxPartySize": 5,
                "minPartySize": 1,
                "requirements": [{
                    "count": 1,
                    "heroClass": "Archer",
                    "heroElement": "None"
                }],
                "excludeClasses": [],
                "excludeElements": []
            }
        }, {
            "zoneId": "Zone.Event.WC.Daily.SuperBoss.Map1",
            "availabilityBegin": "2022-12-26T00:00:00.000Z",
            "availabilityEnd": "9999-12-31T23:59:59.999Z",
            "minAccountLevel": 1,
            "maxAccountLevel": 2147483647,
            "requirements": {
                "maxPartySize": 5,
                "minPartySize": 1,
                "requirements": [{
                    "count": 2,
                    "heroClass": "AnyClass",
                    "heroElement": "Dark"
                }],
                "excludeClasses": [],
                "excludeElements": []
            }
        }]
        self.states[0].state["bossZone"] = {
            "zoneId": "Zone.Event.WC.Weekend.BossSuper.1.Blackguard.Map1",
            "availabilityBegin": "2022-12-26T00:00:00.000Z",
            "availabilityEnd": "9999-12-31T23:59:59.999Z",
            "minAccountLevel": 1,
            "maxAccountLevel": 2147483647,
            "runLimit": 1000
        }
        if end_date is None:
            end_date = datetime.datetime.strptime(self.states[0].state["bossZone"]["availabilityEnd"],
                                                  "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=datetime.UTC)
        else:
            end_date = min(end_date, datetime.datetime.strptime(self.states[0].state["bossZone"]["availabilityEnd"],
                                                                "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=datetime.UTC))
        sanic.log.logger.debug(f"Weekly challenge end date set to {end_date.isoformat()}")
        self.states[0].state["namedWeights"] = "Blackguard=1"
        if end_date is None:
            self.cache_expire = await format_time(datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=2))
        else:
            self.cache_expire = await format_time(
                min(datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=2), end_date)
            )
        sanic.log.logger.debug(f"Finished updating weekly challenge channel, cache expires at {self.cache_expire}")


class BattlePass(Channel):
    """
    Class based system to handle the battle pass channel for the calendar service
    """

    def __init__(self) -> None:
        """
        Initialise the battle pass channel class.
        This will set up the variables for the battle pass channel
        """
        super().__init__()

    async def update_events(self) -> None:
        """
        Update the events for the battle pass channel
        :return: None
        """
        sanic.log.logger.debug(f"Reading battle pass ical file")
        async with aiofiles.open("res/wex/api/calendar/battlepass.ics", "rb") as f:
            events = recurring_ical_events.of(icalendar.Calendar.from_ical(await f.read())).at(
                datetime.datetime.now(datetime.UTC)
            )
        end_date = events[-1].get("DTEND").dt.replace(tzinfo=datetime.UTC)
        event_data = await load_datatable(events[-1].get("DESCRIPTION")[1:])
        self.states[0].valid_from = await format_time()
        self.states[0].state = {
            "seasonId": event_data[0].get("Properties", {}).get("EventId", "None"),
            "seasonEndDate": await format_time(end_date),
        }
        sanic.log.logger.debug(
            f"Current battle pass event set to {self.states[0].state['seasonId']}, ending at {self.states[0].state['seasonEndDate']}")
        self.cache_expire = await format_time(
            min(datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=2), end_date)
        )
        sanic.log.logger.debug(f"Finished updating battle pass channel, cache expires at {self.cache_expire}")
