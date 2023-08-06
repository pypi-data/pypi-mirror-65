"""
Mr. Market - your servant in the Philippine financial market

Features & Benefits
* Get the latest market price of a stock in the Philippine Stock Exchange

Usage
> from mistermarket import MrMarket
> jfc = MrMarket('jfc') # accepts stock ticker
> meg = MrMarket('meg')
> jfc.price
119.32
> meg.price
3.75

"""

__version__ = '0.1.2'

import bs4
import requests


class MrMarket:

    def __init__(self, ticker, market=None):

        self.ticker = ticker
        self.market = market
        self.company = None
        self.price = None
        self.price_change = None
        self._status_code = None
        self._json = None
        self._search_equity()

    def _search_equity(self):
        """ Using the Phisix API URL """

        phisix_url = f'http://phisix-api2.appspot.com/stocks/{self.ticker}.json'
        response = requests.get(phisix_url)
        quote = response.json()
        self._status_code = response.status_code
        self._json = response.json()
        self.company = quote['stock'][0]['name']
        self.price = quote['stock'][0]['price']['amount']
        self.price_change = quote['stock'][0]['percent_change']
