"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Main Blueprint group for the server
"""
import sanic
from .account import account
from .affiliate import affiliate
from .battlebreakers import bb_cdn
from .catalog import catalog
from .dashboard import dashboard
from .datarouter import datarouter
from .entitlement import entitlements
from .eulatracking import agreements
from .exchange import exchange
from .friends import friends
from .lightswitch import lightswitch
from .login import login
from .misc import misc
from .presence import presence
from .priceengine import priceengine
from .purchase import purchase
from .thirdpartytrackers import trackers
from .wex import wex

api = sanic.Blueprint.group(trackers, account, catalog, datarouter, entitlements, friends, lightswitch, login, misc,
                            presence, priceengine, wex, bb_cdn, affiliate, agreements, exchange, purchase, dashboard)
