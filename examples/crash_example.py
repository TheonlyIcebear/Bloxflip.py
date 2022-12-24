from bloxflip import Currency, Mines, Authorization
import bloxflip, time

failed = False
auth = ""

if not Authorization.validate(auth):
	print("Inavlid authorization")
	exit()

crash = bloxflip.Crash(auth)


try:
    websocket = crash.Websocket()
    websocket.connect()
except:
    failed = True

for games in crash.crashPoints(amount=30, interval=0.01):
    current = games[0]
    history = games[1]

    """Attributes: 
     - crash_point
     - private_hash
     - private_seed
     - public_seed
     - gameid
    """

    time.sleep(2) # Make sure bet isn't placed before game starts
    balance = round(Currency.balance(auth), 2)
	print(f"Balance: {balance}")
	print(f"Games: {current.crash_point}")
    if not failed:
        websocket.join(betamount=1, multiplier=1.5) # Join the game