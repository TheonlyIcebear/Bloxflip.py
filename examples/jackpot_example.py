from bloxflip import Currency, Jackpot, Authorization

auth = ""
jackpot = Jackpot(auth)

websocket = jackpot.Websocket()
websocket.connect()

# example 1

for pot in jackpot.sniper(snipe_at=0.5, interval=0.01):

    balance = round(Currency.balance(auth), 2)
    print(f"Balance: {balance}")
    print(f"Pot value: {pot.value}")

    websocket.join(betamount=pot.value*2)  # Join the game with a 50% of winning
