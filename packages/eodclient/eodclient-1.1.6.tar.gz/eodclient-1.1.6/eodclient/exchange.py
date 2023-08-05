from json.decoder import JSONDecodeError
from .errors import InvalidExchangeCodeError, ExchangeCodeRequiredError

from . import session

__all__ = ['Exchange']

EXCHANGE_CODES = [
    {'code': 'US', 'name': 'USA Stocks'},
    {'code': 'LSE', 'name': 'London Exchange'},
    {'code': 'TO', 'name': 'Toronto Exchange'},
    {'code': 'V', 'name': 'TSX Venture Exchange'},
    {'code': 'BE', 'name': 'Berlin Exchange'},
    {'code': 'HM', 'name': 'Hamburg Exchange'},
    {'code': 'XETRA', 'name': 'XETRA Exchange'},
    {'code': 'DU', 'name': 'Dusseldorf Exchange'},
    {'code': 'MU', 'name': 'Munich Exchange'},
    {'code': 'HA', 'name': 'Hanover Exchange'},
    {'code': 'STU', 'name': 'Stuttgart Exchange'},
    {'code': 'F', 'name': 'Frankfurt Exchange'},
    {'code': 'VI', 'name': 'Vienna Exchange'},
    {'code': 'MI', 'name': 'Borsa Italiana'},
    {'code': 'PA', 'name': 'Euronext Paris'},
    {'code': 'BR', 'name': 'Euronext Brussels'},
    {'code': 'MC', 'name': 'Madrid Exchange'},
    {'code': 'AS', 'name': 'Euronext Amsterdam'},
    {'code': 'VX', 'name': 'Swiss Exchange'},
    {'code': 'LS', 'name': 'Euronext Lisbon'},
    {'code': 'SW', 'name': 'SIX Swiss Exchange'},
    {'code': 'ST', 'name': 'Stockholm Exchange'},
    {'code': 'OL', 'name': 'Oslo Stock Exchange'},
    {'code': 'CO', 'name': 'Coppenhagen Exchange'},
    {'code': 'NB', 'name': 'Nasdaq Baltic'},
    {'code': 'NFN', 'name': 'Nasdaq First North'},
    {'code': 'IS', 'name': 'Iceland Exchange'},
    {'code': 'HE', 'name': 'Helsinki Exchange'},
    {'code': 'IR', 'name': 'Irish Exchange'},
    {'code': 'TA', 'name': 'Tel Aviv Exchange'},
    {'code': 'HK', 'name': 'Hong Kong Exchange'},
    {'code': 'MCX', 'name': 'MICEX Russia'},
    {'code': 'AU', 'name': 'Australian Exchange'},
    {'code': 'KO', 'name': 'Korea Stock Exchange'},
    {'code': 'NZ', 'name': 'New Zealand Exchange'},
    {'code': 'NX', 'name': 'ETF-Euronext'},
    {'code': 'SG', 'name': 'Singapore Exchange'},
    {'code': 'BSE', 'name': 'Bombay Exchange'},
    {'code': 'NSE', 'name': 'NSE (India)'},
    {'code': 'SR', 'name': 'Saudi Arabia Exchange'},
    {'code': 'BK', 'name': 'Thailand Exchange'},
    {'code': 'TSE', 'name': 'Tokyo Stock Exchange'},
    {'code': 'JSE', 'name': 'Johannesburg Exchange'},
    {'code': 'KAR', 'name': 'Karachi Stock Exchange'},
    {'code': 'JK', 'name': 'Jakarta Exchange'},
    {'code': 'SHG', 'name': 'Shanghai Exchange'},
    {'code': 'SHE', 'name': 'Shenzhen Exchange'},
    {'code': 'KLSE', 'name': 'Kuala Lumpur Exchange'},
    {'code': 'SA', 'name': 'Sao Paolo Exchange'},
    {'code': 'MX', 'name': 'Mexican Exchange'},
    {'code': 'IL', 'name': 'London IL'},
    {'code': 'FOREX', 'name': 'FOREX'},
    {'code': 'COMM', 'name': 'Commodities'},
    {'code': 'INDX', 'name': 'Indexes'},
    {'code': 'CC', 'name': 'Cryptocurrencies'},
    {'code': 'TW', 'name': 'Taiwan Exchange'},
    {'code': 'SN', 'name': 'Chilean Stock Exchange'},
    {'code': 'BOND', 'name': 'Bond Virtual Exchange'},
    {'code': 'EUFUND', 'name': 'Europe Fund Virtual Exchange'},
    {'code': 'RUFUND', 'name': 'Russsia Fund Virtual Exchange'},
    {'code': 'BA', 'name': 'Buenos Aires Exchange'},
    {'code': 'BUD', 'name': 'Budapest Stock Exchange'},
    {'code': 'KQ', 'name': 'KOSDAQ'},
    {'code': 'IC', 'name': 'Iceland Exchange'},
    {'code': 'PSE', 'name': 'Philippine Stock Exchange'},
    {'code': 'WAR', 'name': 'Warsaw Stock Exchange'},
    {'code': 'AT', 'name': 'Athens Exchange'},
    {'code': 'TWO', 'name': 'Taiwan OTC Exchange'},
    {'code': 'VN', 'name': 'Vietnam Stocks'},
    {'code': 'LU', 'name': 'Luxembourg Stock Exchange'}
]


class Exchange(object):
    '''Exchange object for interacting with the EOD exchange'''
    def __init__(self, exchange_code=None):
        '''The exchange code from
        https://eodhistoricaldata.com/knowledgebase/list-supported-exchanges/
        is required'''
        if exchange_code is None:
            raise ExchangeCodeRequiredError(
                message='An exchange code is required to initiatile an exchange'
            )
        codes = [exchange['code'] for exchange in EXCHANGE_CODES]
        if exchange_code not in codes:
            codes = ', '.join(codes)
            raise InvalidExchangeCodeError(
                expression=exchange_code,
                message=f'Ensure exchange code is in: { codes }'
            )
        self.exchange_code = exchange_code

    def get_symbols(self):
        '''Get all the symbols in the exchange'''
        path = f'https://eodhistoricaldata.com/api/exchanges/{self.exchange_code}'
        response = session.get(
            path,
            params={'fmt': 'json'}
        )
        try:
            return response.json()
        except JSONDecodeError:
            return {'message': response.content.decode("utf-8")}

