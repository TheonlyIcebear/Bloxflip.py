from bloxflip import Currency, Mines, Authorization

cookie = ""

auth = Authorization.generate(cookie)


if Authorization.validate(auth):
    balance = Currency.balance(auth)
    affiliate = Currrency.affiliate


    print(f"User balance: {balance}")
    print(f"Affiliate balance: {affiliate}")