They're are 7 main attributes inside the bloxflip module

- Authorization
- Crash
- Currency
- Mines
- Jackpot
- Towers
- Errors

Example of how you would call the the ``Currency.Balance`` attribute:

>>> from bloxflip import Currency
>>> auth = ""
>>> Currency.balance(auth)

For the classess, crash, towers, mines and jackpot, you need to create a instance of the class with the authorization token

>>> from bloxflip import Crash
>>> crash = Crash('Auth-Token-Here')
>>> for game in crash.crashpoints():
>>>     print(game)


Authorization
--------------
- generate: Will generate a valid bloxflip authorization token in exchange for a roblox cookie
- validate: Will return ``True`` or ``False`` wether or not the provided bloxflip auth is valid or not

Crash
-----
- Websocket: Returns a websocket object and automatically connects, Reread the `websocket-client documentation <https://websocket-client.readthedocs.io/en/latest/>`_ for examples on how to use this

  - connect: logs into to websocket and begins listening on the Crash channel
  - join: Joins the crash game
- crashpoints: Will ``yield`` the past n'th crash games

Towers
-------
- create: Starts a towers game
- choose: Chooses a tile; must be from 0 to 2, returns False if tile exploded
- cashout: Exits the towers game with your earnings

Mines
-------
- create: Starts a mines game
- choose: Chooses a tile; must be from 0 to 24, returns False if tile exploded
- cashout: Exits the mines game with your earnings

Jackpot
------
- Websocket: Creates websocket object connected to bloxflip websocket

  - connect: logs into Websocket, same as crash websocket except it's listening in on the Jackpot channel
  - join: Will join the current Jackpot game
- sniper: Yields the current jackpot's game's current value N seconds before it ends

>>> from bloxflip import Currency, Jackpot, Authorization
>>> jackpot = Jackpot('Auth-Token-Here')
>>>
>>> for pot in jackpot.sniper(snipe_at=0.5, interval=0.01): # Snipes game 0.5 seconds before it starts
>>>     balance = round(Currency.balance(auth), 2)
>>>     print(f"Balance: {balance}")
>>>     print(f"Pot value: {pot.value}")

Errors
-------



.. list-table:: Errors is a exception raising and catching class
   :widths: 25 25 50
   :header-rows: 1

   * - Error Type
     - Raised when
     - Exception
   * - InsufficientFunds
     - User attempts to do an action that requires more credits than they have
     - bloxflip.errors.InsufficientFunds
   * - InvalidAuthorization
     - User passes an invalid authorization token for action that requires a valid token 
     - bloxflip.errors.InvalidAuthorization
   * - GameAlreadyStarted
     - User attempts to create a new game when a game is already active
     - bloxflip.errors.GameAlreadyStarted
   * - GameNotStarted
     - User attempts an action that requires a game to be started when there isn't
     - bloxflip.errors.GameNotStarted
   * - Ratelimited
     - User is sending too many messages and bloxflip begings blocking their requests
     - bloxflip.errors.Ratelimited
   * - InvalidParamater
     - User passes a paramter than cannot be evaluated
     - bloxflip.errors.InvalidParameter
   * - GeneralError
     - General Failure
     - bloxflip.errors.GeneralError
   * - NetworkError
     - General network, ussually fails when user is being blocked by cloudflare
     - bloxflip.errors.NetworkError
