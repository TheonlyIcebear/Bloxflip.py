import cloudscraper, requests, base64, json, time, os
from websocket import create_connection

from random import randbytes

scraper = cloudscraper.create_scraper()
auth = None

def Login(a):
	global auth
	if Authorization.validate(a):
		auth = a
	else:
		raise Exception("KeyError: Invalid authorization provided.")

class Crash:
	def __init__(self, auth):
		self.auth = auth

	class Websocket:
		def __init__ (self):
			pass

		def Connect(auth=auth, headers=None):
			global ws
			if not headers:
				headers = {
						"GET": "/socket.io/?EIO=3&transport=websocket HTTP/1.1",
						"Host": "sio-bf.blox.land",
						"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0",
						"Accept": "*/*",
						"Accept-Language": "en-US,en;q=0.5",
						"Accept-Encoding": "gzip, deflate, br",
						"Sec-WebSocket-Version": "13",
						"Origin": "https://www.piesocket.com",
						"Sec-WebSocket-Extensions": "permessage-deflate",
						"Sec-WebSocket-Key": str(base64.b64encode(randbytes(16)).decode('utf-8')),
						"Connection": "keep-alive, Upgrade",
						"Sec-Fetch-Dest": "websocket",
						"Sec-Fetch-Mode": "websocket",
						"Sec-Fetch-Site": "cross-site",
						"Pragma": "no-cache",
						"Cache-Control": "no-cache",
						"Upgrade": "websocket"
				}
			ws = create_connection("wss://ws.bloxflip.com/socket.io/?EIO=3&transport=websocket",
									suppress_origin=True,  
									headers=headers
								)

			ws.send("40/crash,")
			if not Authorization.validate(auth):
				ws.close()
				raise Exception("KeyError: Invalid authorization provided.")
			ws.send(f'42/crash,["auth","{auth}"]')

			return ws

		def Join(betamount, multiplier):
			try:
				ws
			except:
				raise NameError("ws is not defined. You haven't connected to the websocket yet.")
			try:
				json = str({"autoCashoutPoint":int(multiplier*100),"betAmount":betamount}).replace("'", '"').replace(" ", "")
				ws.send(f'42/crash,["join-game",{str(json)}]')
			except:
				return False

			return True


	def Crashpoints(amount=10, interval=0.01):
		history = None
		sent = False

		if amount > 35:
			raise KeyError("amount cannot be above 35")

		while True:
			try:
				games = scraper.get("https://rest-bf.blox.land/games/crash").json()
			except:
				continue

			if not history == games["history"]:
				history = games["history"]
				yield [float(crashpoint["crashPoint"]) for crashpoint in history][::-1][-amount:]
			time.sleep(interval)

class Towers:
	def __init__(self):
		pass

	def Create(betamount, difficulty, auth=None):
		if not difficulty in ["easy", "normal", "hard"]:
			raise KeyError("Invalid difficulty provided.")
		response = scraper.post("https://rest-bf.blox.land/games/towers/create", 
								headers={
									"x-auth-token": auth
								}, 
								json={
									"betAmount": str(betamount),
									"difficulty": difficulty
								}
						)

		if betamount < 5:
			raise Exception("Bet amount must be greater than 5")

		if response.status_code == 429:
			raise KeyError("Ratelimited: Too many requests")


		if not response.status_code == 200:
			try:
				response.json()
			except:
				raise Exception("Network error.", "error")

			if response.json()["msg"] == "You already have an active towers game!":
				raise Exception("You already have an active towers game. End it then try again.")
			
			else:
				raise Exception("Insuffecient funds.")

			return response
		return True

	def Choose(choice, auth=None):
		response = scraper.post("https://rest-bf.blox.land/games/towers/action", 
								headers={
									"x-auth-token": auth
								},
								json={
									"cashout": False,
									"tile": choice
								}
						)
				

		if response.status_code == 429:
			raise KeyError("Ratelimited: Too many requests")

		if not response.status_code == 200:
			if response.json()["msg"] == "You do not have an active towers game!":
				raise Exception("There is currently no active towers game")

		return not response.json()["exploded"]


	def Cashout(auth):
		response = scraper.post("https://rest-bf.blox.land/games/towers/action", 
							headers={
								"x-auth-token": auth
							},
							json={
								"cashout": True,

							}
					)

		if response.status_code == 429:
			raise KeyError("Ratelimited: Too many requests")

		if not response.status_code == 200:
			if not "msg" in list(response.json()):
				raise KeyError("Invalid authorization provided.")

			elif response.json()["msg"] == "You do not have an active towers game!":
				raise Exception("You do not have an active towers game.")

			elif response.json()["msg"] == "You cannot cash out yet! You must uncover at least one tile!":
				raise Exception("You cannot cash out yet! You must uncover at least one tile!")

			raise Exception("Insuffecient funds")

		return True


class Mines:
	def __init__(self):
		pass

	def Create(betamount, mines, auth=None):
		response = scraper.post("https://rest-bf.blox.land/games/mines/create", 
								headers={
									"x-auth-token": auth
								}, 
								json={
									"betAmount": betamount,
									"mines": mines
								}
						)

		if betamount < 5:
			raise Exception("Bet amount must be greater than 5")


		if response.status_code == 429:
			raise KeyError("Ratelimited: Too many requests")

		if not response.status_code == 200:
			try:
				response.json()
			except:
				raise Exception("Network error.", "error")
			if response.json()["msg"] == "You already have an active mines game!":
				raise Exception("You already have an active mines game. End it then try again.")

		return response

	def Choose(choice, auth=None):
		response = scraper.post("https://rest-bf.blox.land/games/mines/action", 
								headers={
									"x-auth-token": auth
								},
								json={
									"cashout": False,
									"mine": choice
								}
						)
				

		if response.status_code == 429:
			raise KeyError("Ratelimited: Too many requests")

		if not response.status_code == 200:
			if response.json()["msg"] == "You do not have an active mines game!":
				raise Exception("There is currently no active mines game")
		return not response.json()["exploded"]

	def Cashout(auth):
		response = scraper.post("https://rest-bf.blox.land/games/mines/action", 
							headers={
								"x-auth-token": auth
							},
							json={
								"cashout": True,

							}
					)

		if not response.status_code == 200:
			if not "msg" in list(response.json()):
				raise KeyError("Invalid authorization provided.")

			elif response.json()["msg"] == "You do not have an active mines game!":
				raise Exception("You do not have an active mines game.")

			elif response.json()["msg"] == "You cannot cash out yet! You must uncover at least one tile!":
				raise Exception("You cannot cash out yet! You must uncover at least one tile!")

			return False

		return response

class Authorization:
	def __init__(self):
		pass

	def Generate(cookie):
		request = scraper.post("https://rest-bf.blox.land/user/login", json={
			"affiliateCode": "BFSB",
			"cookie": cookie
		}).json()
		if not "jwt" in list(request):
			raise KeyError("Either cookie is invalid or cookie is ip locked.")

		return request.json()["jwt"]

	def validate(auth):
		request = scraper.get("https://rest-bf.blox.land/user", headers={
						"x-auth-token": auth
				}).json()

		return request["success"]


class Currency:
	def __init__(self):
		pass

	def Balance(auth):
		request = scraper.get("https://rest-bf.blox.land/user", headers={
						"x-auth-token": auth
				}).json()
		if not "user" in list(request):
			raise KeyError("Invalid authorization provided.")
		return request["user"]["wallet"]

	def Affiliate(auth):
		request = scraper.get("https://rest-bf.blox.land/user/affiliates", headers={
				"x-auth-token": auth
			}).json()
		if not "affiliateMoneyAvailable" in list(request):
			raise KeyError("Invalid authorization provided.")
		return request["affiliateMoneyAvailable"]

	def ClaimAfiliate(auth, amount):
		response = scraper.post("https://rest-bf.blox.land/user/affiliates/claim", headers={
									"x-auth-token": auth
								}, json={
									"amount": str(amount)
								})

		if response.status_code == 200:
			return True

		elif response.status_code == 429:
			raise Exception("Network error: Ratelimited, too many requests.")

		elif Curreny.Affiliate(auth) < 100:
			raise Exception("Not enough funds to withdraw")

		else:
			raise KeyError("Invalid authorization provided.")

	def Withdraw(auth, amount):
		response = scraper.post("https://rest-bf.blox.land/user/withdrawTarget", headers={
								"x-auth-token": auth
							}, json={
								"amount": str(int(amount))
							})

		if not response.status_code == 200:
			raise Exception("Either you're withdrawing more than your balance or your auth is not connected to a valid cookie.")
