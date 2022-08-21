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

Every function requires you to pass a valid bloxflip authorization, Besides ``bloxflip.Authorization.Generate``
With the Generate function you must pass a roblox valid roblox cookie and it will return you a valid bloxflip authorization.


Authorization
--------------
- Generate: Will generate a valid bloxflip authorization token in exchange for a roblox cookie
- validate: Will return ``True`` or ``False`` wether or not the provided bloxflip auth is valid or not

Crash
-----
- Websocket: 

  - Connect: Returns a websocket object and automatically connects, read the `websocket-client documentation <https://websocket-client.readthedocs.io/en/latest/examples.html/>`_ for examples on how to use this
  - Join: Joins the crash game

