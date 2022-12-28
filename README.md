# Bloxflip.py
An API Wrapper for bloxflip

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
import time

auth = ""
betamount = 1
multiplier = 2

crash = bloxflip.Crash(auth)
websocket = crash.Websocket()
websocket.connect()

for games in crash.crashPoints(amount=30, interval=0.01):
	current = games[0]
	history = games[1]

	time.sleep(2) # Make sure bet isn't placed before game starts
        balance = round(Currency.balance(auth), 2)
	print(f"Balance: {balance}")
	print(f"Games: {current.crash_point}")
	websocket.join(betamount=betamount, multiplier=multiplier)
```
For more detailed examples check the examples folder
