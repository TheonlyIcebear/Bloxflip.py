import cloudscraper, websocket, requests, base64, json, time, ssl, os
from websocket import create_connection
from random import randbytes
from typing import Union

scraper = cloudscraper.create_scraper()

class errors:
	def __init__() -> None:
		pass

	class InsuffecientFunds(Exception):
		"""Raised if user lacks the funds to do a certain action"""

		pass

	class InvalidAuthorization(Exception):
		"""Raised if a invalid Authorization Token is passed"""

		pass

	class GameAlreadyStarted(Exception):
		"""Raised if there is an already active game"""

		pass

	class GameNotStarted(Exception):
		"""Raised if there is no active game"""

		pass

	class Ratelimited(Exception):
		"""Raised if user is ratelimited"""

		pass

	class InvalidParamater(Exception):
		"""Raised if a invalid paramater is passed"""

		pass

	class GeneralError(Exception):
		"""Raisedd on a general failures"""

		pass

	class NetworkError(Exception):
		"""Raised on cloudflare or other network errors"""

		pass

class Round:
	"""A wrapper for the api response"""

	def __init__(self, game: dict) -> None:
		self.crash_point = game["crashPoint"]
		self.public_seed = game["publicSeed"]
		self.private_seed = game["privateSeed"]
		self.private_hash = game["privateHash"]
		self.gameid = game["_id"]


class Tower:
	"""A wrapper for a Towers game"""

	def __init__(self, info: dict) -> None:
		if not info["hasGame"]:

			game = info["game"]
			self.competed_levels = info["completedLevels"]
			self.difficulty = info["difficulty"]
			self.exploded = info["exploded"]

			self.timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(info["created"]))
			self.client_seed = info["clientSeed"]
			self.user_id = info["userId"]
			self.nonce = info["nonce"]
			self.uuid = info["uuid"]


			self.bet_amount = info["betAmount"]
			self.payout = info["payout"]
			

			self.active = True
		else:
			self.active = False

class Mine:
	"""A wrapper for a Mines game"""

	def __init__(self, game: dict) -> None:
		if game["hasGame"]:

			info = game["game"]
			self.competed_levels = info["uncoveredLocations"]
			self.client_seed = info["clientSeed"]
			self.multiplier = game["multiplier"]
			self.exploded = info["exploded"]
			
			self.timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(info["created"]))
			self.user_id = info["userId"]
			self.nonce = info["nonce"]
			self.uuid = info["uuid"]

			self.mines = info["minesAmount"]
			self.bet_amount = info["betAmount"]
			self.payout = info["payout"]


			self.active = True
		else:
			self.active = False

class Crash:
	def __init__(self, auth) -> None:
		self.auth = auth

	class _websocket:
		def __init__ (self, auth: str) -> None:
			self.auth = auth
			self._connection = None

		def connect(self, headers=None) -> websocket.WebSocket:
			"""Connects to websocket and returns websocket object"""

			self._connection = create_connection("wss://ws.bloxflip.com/socket.io/?EIO=3&transport=websocket", header={
					"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0",
					"Accept": "*/*",
					"Accept-Language": "en-US,en;q=0.5",
					"Accept-Encoding": "gzip, deflate, br",
					"Sec-WebSocket-Version": "13",
					"Host": "ws.bloxflip.com",
					"Origin": "https://bloxflip.com",
					"Sec-WebSocket-Key": str(base64.b64encode(randbytes(16)).decode('utf-8')),
					"Connection": "keep-alive, Upgrade",
					"Sec-Fetch-Dest": "websocket",
					"Sec-Fetch-Mode": "websocket",
					"Sec-Fetch-Site": "cross-site",
					"Pragma": "no-cache",
					"Cache-Control": "no-cache",
					"Upgrade": "websocket",
					"x-auth-token": self.auth
				},
				suppress_origin=True
			)

			ws = self._connection
			ws.send("40/crash,")
			ws.send(f'42/crash,["auth","{self.auth}"]')

			return self._connection

		@property
		def connection(self) -> websocket.WebSocket:
			return self._connection

		def join(self, betamount: float, multiplier: float) -> None:
			"""Joins Crash game with the betamount as well as multiplier"""

			json = str(
					{
						"autoCashoutPoint": int( multiplier * 100 ),
						"betAmount": betamount	
					}
				).replace("'", '"').replace(" ", "")
			ws.send(f'42/crash,["join-game",{str(json)}]')

	def Websocket(self):
		return self._websocket(self.auth)

	def crashPoints(self, amount=10, interval=0.01):
		"""Yields the last games results as well as the previous results"""

		history = None
		sent = False

		if amount > 35:
			raise errors.InvalidParamater("amount cannot be above 35")

		while True:
			try:
				games = scraper.get("https://rest-bf.blox.land/games/crash").json()
			except:
				continue

			if not history == games["history"]:
				history = games["history"]
				yield [Round(games["history"][0]), [Round(crashpoint) for crashpoint in history]]
			time.sleep(interval)

class Towers:
	def __init__(self, auth):
		self.auth = auth

	def create(self, betamount: int, difficulty: str) -> dict:
		"""Creates a towers game"""
		
		if not difficulty in ["easy", "normal", "hard"]:
			raise errors.InvalidParamater("Invalid difficulty provided.")
		response = scraper.post("https://rest-bf.blox.land/games/towers/create", 
			headers={
				"x-auth-token": self.auth
			}, 
			json={
				"betAmount": str(betamount),
				"difficulty": difficulty
			}
		)

		if betamount < 5:
			raise errors.InvalidParamater("Bet amount must be greater than 5")

		if response.status_code == 429:
			raise errors.Ratelimited("Ratelimited: Too many requests")


		if not response.status_code == 200:
			try:
				response.json()
			except:
				raise errors.NetworkError("Network error.", "error")

			if response.json()["msg"] == "You already have an active towers game!":
				raise errors.GameAlreadyStarted("You already have an active towers game. End it then try again.")

			elif response.json()["msg"] == "You can not afford to start this game!":
				raise errors.InsuffecientFunds("You cannot afford to start this game.")

			raise errors.GeneralError("Failed to create game")

		return response.json()

	def choose(self, choice: int) -> bool:
		"""Chooses a tile to uncover"""

		response = scraper.post("https://rest-bf.blox.land/games/towers/action", 
							headers={
								"x-auth-token": self.auth
							},
							json={
								"cashout": False,
								"tile": choice
							}
						)
				

		if response.status_code == 429:
			raise errors.Ratelimited("Ratelimited: Too many requests")

		if not response.status_code == 200:
			if response.json()["msg"] == "You do not have an active towers game!":
				raise errors.GameNotStarted("There is currently no active towers game")

		return not response.json()["exploded"]


	def cashout(self):
		"""Cashes out the winnings from the current game"""

		response = scraper.post("https://rest-bf.blox.land/games/towers/action", 
						headers={
							"x-auth-token": self.auth
						},
						json={
							"cashout": True,

						}
					)

		if response.status_code == 429:
			raise errors.Ratelimited("Ratelimited: Too many requests")

		if not response.status_code == 200:
			if not "msg" in list(response.json()):
				raise errors.InvalidAuthorization("Invalid authorization provided.")

			elif response.json()["msg"] == "You do not have an active towers game!":
				raise errors.GameNotStarted("You do not have an active towers game.")

			elif response.json()["msg"] == "You cannot cash out yet! You must uncover at least one tile!":
				raise errors.GeneralError("You cannot cash out yet! You must uncover at least one tile!")

			raise errors.InsuffecientFunds("Insuffecient funds")

		return True

	@property
	def current(self) -> Tower:
		if not Authorization.validate(self.auth):
			raise errors.InvalidAuthorization("Invalid authorization provided.")

		request = scraper.get("https://api.bloxflip.com/games/mines", 
					headers={
						"x-auth-token": self.auth
					}
				).json()
		
		return Tower(request)


class Mines:
	def __init__(self, auth: str) -> None:
		self.auth = auth

	def create(self, betamount: int, mines: int) -> None:
		"""Creates a mines game"""

		response = scraper.post("https://rest-bf.blox.land/games/mines/create", 
							headers={
								"x-auth-token": self.auth
							}, 
							json={
								"betAmount": betamount,
								"mines": mines
							}
						)

		if betamount < 5:
			raise errors.InvalidParamater("Bet amount must be greater than 5")


		if response.status_code == 429:
			raise erros.Ratelimited("Ratelimited: Too many requests")

		if not response.status_code == 200:
			try:
				response.json()
			except:
				raise errors.NetworkError("Network error.", "error")
			if response.json()["msg"] == "You already have an active mines game!":
				raise errors.GameAlreadyStarted("You already have an active mines game. End it then try again.")
			if response.json()["msg"] == "You can not afford to start this game!":
				raise errors.InsuffecientFunds("You cannot afford to start this game.")

			raise errors.GeneralError("Failed to create game")

	def choose(self, choice: int) -> bool:
		"""Chooses a tile to bet on"""

		response = scraper.post("https://rest-bf.blox.land/games/mines/action", 
							headers={
								"x-auth-token": self.auth
							},
							json={
								"cashout": False,
								"mine": choice
							}
						)
				

		if response.status_code == 429:
			raise errors.Ratelimited("Ratelimited: Too many requests")

		if not response.status_code == 200:
			if response.json()["msg"] == "You do not have an active mines game!":
				raise errors.GameNotStarted("There is currently no active mines game")

		return not response.json()["exploded"]

	def cashout(self) -> bool:
		"""Cashouts the winnings from the current Mines game"""

		response = scraper.post("https://rest-bf.blox.land/games/mines/action", 
						headers={
							"x-auth-token": self.auth
						},
						json={
							"cashout": True,

						}
					)

		if not response.status_code == 200:
			if not "msg" in list(response.json()):
				raise errors.InvalidAuthorization("Invalid authorization provided.")

			elif response.json()["msg"] == "You do not have an active mines game!":
				raise errors.GameNotStarted("You do not have an active mines game.")

			elif response.json()["msg"] == "You cannot cash out yet! You must uncover at least one tile!":
				raise errors.GeneralError("You cannot cash out yet! You must uncover at least one tile!")

			return False

		return response

	@property
	def current(self) -> Mine:
		if not Authorization.validate(self.auth):
			raise errors.InvalidAuthorization("Invalid authorization provided.")

		request = scraper.get("https://api.bloxflip.com/games/towers", 
					headers={
						"x-auth-token": self.auth
					}
				).json()
		
		return Mine(request)

class Authorization:
	def __init__(self) -> None:
		pass

	def generate(cookie: str) -> str:

		"""Generate a Bloxflip Auth Token from a Roblox Cookie"""
		request = scraper.post("https://rest-bf.blox.land/user/login", json={
			"affiliateCode": "BFSB",
			"cookie": cookie
		}).json()

		if not "jwt" in list(request):
			raise errors.GeneralError("Either cookie is invalid or cookie is ip locked.")

		return request["jwt"]

	def validate(auth: str) -> bool:
		"""Validates that the Authorization Token works"""

		request = scraper.get("https://rest-bf.blox.land/user", headers={
						"x-auth-token": auth
				}).json()

		if request["success"] == True:
			return True

		return False


class Currency:
	def __init__(self) -> None:
		pass

	def balance(auth: str) -> int:
		"""Get user's balance from their auth token"""

		request = scraper.get("https://rest-bf.blox.land/user", headers={
						"x-auth-token": auth
				}).json()
		if not "user" in list(request):
			raise errors.InvalidAuthorization("Invalid authorization provided.")

		return request["user"]["wallet"]

	def affiliate(auth: str) -> int:
		"""Get the amount of currency available on their affiliate"""

		request = scraper.get("https://rest-bf.blox.land/user/affiliates", headers={
				"x-auth-token": auth
			}).json()
		if not "affiliateMoneyAvailable" in list(request):
			raise errors.InvalidAuthorization("Invalid authorization provided.")

		return request["affiliateMoneyAvailable"]

	def claimAfiliate(auth: str, amount: int) -> dict:
		"""Claim the currency insied the user's affiliate balance"""

		response = scraper.post("https://rest-bf.blox.land/user/affiliates/claim", headers={
									"x-auth-token": auth
								}, json={
									"amount": str(amount)
								})

		if response.status_code == 200:
			return response.json()

		elif response.status_code == 429: 
			raise errors.Ratelimited("Ratelimited, too many requests.")

		elif Curreny.Affiliate(auth) < 100:
			raise errors.InsuffecientFunds("Not enough funds to withdraw")

		else:
			raise errors.InvalidAuthorization("Invalid authorization provided.")

	def Wwthdraw(auth: str, amount: int) -> None:
		"""Withdraw Bloxflip currency into Roblox"""

		response = scraper.post("https://rest-bf.blox.land/user/withdrawTarget", headers={
								"x-auth-token": auth
							}, json={
								"amount": str(int(amount))
							})

		if not response.status_code == 200:
			raise errrors.GeneralError("Either you're withdrawing more than your balance or your auth is not connected to a valid cookie.")