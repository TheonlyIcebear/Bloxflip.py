from bloxflip import Currency, Mines, Authorization
import bloxflip, random, time

auth = ""

if not Authorization.validate(auth):
    print("Invalid authorization")
    exit()

bet_amount = 5
mines_amount = 3

mines = Mines(auth)

while True:
    mines.create(bet_amount, mines_amount)
    time.sleep(0.5)

    choice = random.choice(list(range(0, 24)))
    balance = round(Currency.Balance(auth), 2)

    current = mines.current
    result = mines.choose(choice)

    time.sleep(5)
    if current.active:  # Check if there is an active game
        print(current.payout)  # print how much you'd get if you withdrawed

    """Attributes: current
    - payout
    - bet_amount
    - mines
    - uuid
    - nonce
    - user_id
    - timestamp
    - exploded
    - multiplier
    - client_seed
    - competed_levels
    - active

    """

    print(f"Balance: {balance}")
    print(f"Choosing tile {choice}")
    if result:
        print("Cashing out")
        mines.cashout()
    else:
        print("Mine exploded")
