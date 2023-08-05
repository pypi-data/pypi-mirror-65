'''Initialise the eod client with api tokem in session'''

import os
import requests

from .errors import APIKeyMissingError

__all__ = []

EOD_API_KEY = os.environ.get('EOD_API_KEY', None)

if EOD_API_KEY is None:
    raise APIKeyMissingError(
        "All methods require an EOD_API_KEY env variable from "
        "https://eodhistoricaldata.com/"
    )

session = requests.Session()
session.params = {}
session.params['api_token'] = EOD_API_KEY

from .symbol import *
__all__ += symbol.__all__
from .exchange import *
__all__ += exchange.__all__