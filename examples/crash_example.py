from bloxflip import Currency, Crash, Authorization
import bloxflip, time

failed = False
auth = ""

if not Authorization.validate(auth):
    print("Invalid authorization")
    exit()

crash = bloxflip.Crash(auth)


try:
    websocket = crash.Websocket()
    websocket.connect()
except:
    failed = True

# example 1

for history in crash.crashpoints(amount=35, interval=0.01):
    current = history[0]

    """Attributes: 
     - crash_point
     - private_hash
     - private_seed
     - public_seed
     - game_id
    """

    time.sleep(2)  # Make sure bet isn't placed before game starts
    balance = round(Currency.balance(auth), 2)
    print(f"Balance: {balance}")
    print(f"Games: {current.crashpoint}")
    if not failed:
        websocket.join(betamount=1, multiplier=1.5)  # Join the game

# example 2


def func(history):
    current = history[0]

    time.sleep(2)  # Make sure bet isn't placed before game starts
    balance = round(Currency.balance(auth), 2)
    print(f"Balance: {balance}")
    print(f"Games: {current.crashpoint}")
    if not failed:
        websocket.join(betamount=1, multiplier=1.5)  # Join the game


crash.crashpoints(on_game_start=func)
