from bloxflip import Currency, Mines, Authorization

cookie = ""
auth = ""


if Authorization.validate(auth):
    balance = Currency.balance(auth)
    affiliate = Currency.affiliate(auth)
    user = Authorization.get_info(auth)

    print(f"User balance: {balance}")
    print(f"Affiliate balance: {affiliate}")
    print(f"Amount wagered: {user.total_wagered}")

    """Attributes: user
     - account_verified
     - total_wagered
     - total_deposited
     - total_withdrawn
     - games_played
     - games_won
     - username
     - roblox_id
     - rank
     
    """