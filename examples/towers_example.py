from bloxflip import Currency, Towers, Authorization
import bloxflip, random, time

auth = ""

if not Authorization.validate(auth):
    print("Invalid authorization")
    exit()

bet_amount = 5
towers_amount = 3

towers = bloxflip.Towers(auth)

while True:
    towers.create(bet_amount, towers_amount)
    time.sleep(0.5)

    choice = random.choice(list(range(0, 2)))
    balance = round(Currency.Balance(auth), 2)

    current = towers.current
    result = towers.choose(choice)

    time.sleep(1)
    if current.active:  # Check if there is an active game
        print(current.payout)  # print how much you'd get if you withdraw

    print(current)
        
    """Attributes: current
     - payout
     - bet_amount
     - difficulty
     - uuid
     - nonce
     - user_id
     - timestamp
     - exploded
     - client_seed
     - competed_levels
     - active
    """

    

    print(f"Balance: {balance}")
    print(f"Choosing tile {choice}")
    if result:
        print("Cashing out")
        towers.cashout()
    else:
        print("Mine exploded")