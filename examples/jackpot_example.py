from bloxflip import Currency, Jackpot, Authorization
import bloxflip, time

failed = False
auth = ""

if not Authorization.validate(auth):
    print("Invalid authorization")
    exit()

jackpot = Jackpot(auth)


try:
    websocket = jackpot.Websocket()
    websocket.connect()
except:
    failed = True

# example 1

for pot in jackpot.sniper(snipe_at=0.5, interval=0.01):

    balance = round(Currency.balance(auth), 2)
    print(f"Balance: {balance}")
    print(f"Pot value: {pot.value}")

    """"Attributes: pot
         - value
         - time
         - status
         - winner
         - winningColor
         - id
        """

    if not failed:
        websocket.join(betamount=pot.value*2)  # Join the game with a 50% of winning

# example 2


def func(pot):
    balance = round(Currency.balance(auth), 2)
    print(f"Balance: {balance}")
    print(f"Pot value: {pot.value}")

    if not failed:
        websocket.join(betamount=pot.value * 2, multiplier=1.5)  # Join the game with a 50% of winning

jackpot.sniper(on_game_start=func)
