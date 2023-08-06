# Mr. Market
 Mr. Market - your servant in the Philippine financial market
 
Features & Benefits
--- 
* Get the latest market price of a stock in the Philippine Stock Exchange

Installation
---
```python
> pip install mistermarket
```

Usage
---
```python
> from mistermarket import MrMarket
> jfc = MrMarket('jfc') # Jollibee's stock ticker
> meg = MrMarket('meg') # Megaworld's stock ticker
> jfc.price
119.32
> meg.price
3.75
```

Software Requirements and Dependencies
---
* [Requests](https://github.com/psf/requests)
* [Phisix API](http://phisix-api4.appspot.com/)
