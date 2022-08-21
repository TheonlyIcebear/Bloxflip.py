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
- Generate
Will generate a valid bloxflip authorization token in exchange for a roblox cookie
