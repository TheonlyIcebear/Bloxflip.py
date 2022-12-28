They're are 5 main attributes inside the bloxflip module

- Authorization
- Crash
- Currency
- Mines
- Towers

Example of how you would call the the ``Currency.Balance`` attribute:

>>> from bloxflip import Currency
>>> auth = ""
>>> Currency.Balance(auth)

To begin, for the classess, crash, towers, mines and jackpot, you need to create a instance of the class with the authorization token

>>> from bloxflip import Crash
>>> crash = Crash('Auth-Token-Here')
>>> crash.crashpoints()


authorization
--------------
- generate: Will generate a valid bloxflip authorization token in exchange for a roblox cookie
- validate: Will return ``True`` or ``False`` wether or not the provided bloxflip auth is valid or not

crash
-----
- websocket: 

  - connect: Returns a websocket object and automatically connects, read the `websocket-client documentation <https://websocket-client.readthedocs.io/en/latest/>`_ for examples on how to use this
  - join: Joins the crash game
- crashpoints: Will ``yield`` the past n'th crash games

towers
-------
- create: Starts a towers game
- choose: Chooses a tile; must be from 0 to 2, returns False if tile exploded
- cashout: Exits the towers game with your earnings

mines
-------
- create: Starts a mines game
- choose: Chooses a tile; must be from 0 to 24, returns False if tile exploded
- cashout: Exits the mines game with your earnings
