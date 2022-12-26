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

The auth arguement is optional for many of the functions
Instead you can use the ``bloxflip.Login(auth)`` function once and the functions will automatically use that auth provided. 

You can always change the auth by running ``bloxflip.Login()`` with a different authorization

Authorization
--------------
- generate: Will generate a valid bloxflip authorization token in exchange for a roblox cookie
- validate: Will return ``True`` or ``False`` wether or not the provided bloxflip auth is valid or not

Crash
-----
- websocket: 

  - connect: Returns a websocket object and automatically connects, read the `websocket-client documentation <https://websocket-client.readthedocs.io/en/latest/>`_ for examples on how to use this
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
