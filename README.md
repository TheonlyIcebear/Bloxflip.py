# Bloxflip.py
An API Wrapper for bloxflip
https://bloxflippy.readthedocs.io/en/latest/

# Usage
There are 7 main bloxflip attributes
 - Authorization
 - Crash
 - Currency
 - Mines
 - Towers
 - Jackpot
 - Errors
 Each with their own example showing how to use them in the examples folder

# Examples

Simple Crash joiner:
```py
from bloxflip import Currency, Crash
import bloxflip, time

auth = ""
betamount = 1
multiplier = 2

crash = bloxflip.Crash(auth)
websocket = crash.Websocket()
websocket.connect()

for games in crash.crashpoints(amount=30, interval=0.01):
	current = games[0]
	history = games[1]

	time.sleep(2) # Make sure bet isn't placed before game starts
	balance = round(Currency.balance(auth), 2)
	print(f"Balance: {balance}")
	print(f"Games: {current.crashpoint}")
	websocket.join(betamount=betamount, multiplier=multiplier)
```
For more detailed examples check the examples folder

# Extra

read-the-docs: https://bloxflippy.readthedocs.io/en/latest/

Discord: https://discord.gg/wbh8eFGKAm

Crypto:

XMR: 49Gwzrmm5irYKmURJgnEVajVnHo1mRMymMR8UykbGCSELCzh3q3BUBPJ4RSEho8K4c4WHvUR7LUtFcFyhXCJ11eLNt3QWoc

BTC: bc1qwxytxk6cqyhd9rj0707mmyn44ez0m85nmce8uw

ETH: 0xC52491F8Aa367F69DD4224009fE279b34279E6C7
