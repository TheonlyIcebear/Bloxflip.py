import cloudscraper, requests, json, time, os
from websocket import create_connection

scraper = cloudscraper.create_scraper()

class Crash:
	def __init__(self, auth):
		self.auth = auth

	class Websocket:
		def __init__ (self):
			pass

		def Connect(auth=None):
			global ws
			ws = create_connection("wss://sio-bf.blox.land/socket.io/?EIO=3&transport=websocket", header={
					"Accept-Encoding": "gzip, deflate, br",
					"Accept-Language": "en-US,en;q=0.9",
					"Cache-Control": "no-cache",
					"Connection": "Upgrade",
					"Host": "sio-bf.blox.land",
					"Origin": "https://bloxflip.com",
					"Pragma": "no-cache",
					"Sec-WebSocket-Extensions": "permessage-deflate; client_max_window_bits",
					"Sec-WebSocket-Key": "dTCC7XK7OBweEv1kVAUycQ==",
					"Sec-WebSocket-Version": "13",
					"Upgrade": "websocket",
					"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
			})

			ws.send("40/crash,")
			if not Authorization.validate(auth):
				raise Exception("KeyError: Invalid authorization provided.")
			ws.send(f'42/crash,["auth","{auth}"]')

			return ws

		def Join(betamount, multiplier):
			json = str({"autoCashoutPoint":int(multiplier*100),"betAmount":betamount}).replace("'", '"').replace(" ", "")
			ws.send(f'42/crash,["join-game",{str(json)}]')


	def Crashpoints(amount=10, interval=0.01):
		history = None
		sent = False

		if amount > 35:
			raise KeyError("amount cannot be above 35")

		while True:
			try:
				games = scraper.get("https://rest-bf.blox.land/games/crash").json()
			except:
				games = scraper.get("https://rest-bf.blox.land/games/crash").json()

			if not history == games["history"]:
				history = games["history"]
				yield [float(crashpoint["crashPoint"]) for crashpoint in history][::-1][-amount:]
			time.sleep(interval)

class Authorization:
	def __init__(self):
		pass

	def generate(cookie):
		request = scraper.post("https://rest-bf.blox.land/user/login", json={
			"affiliateCode": "BFSB",
			"cookie": cookie
		}).json()
		if not "jwt" in list(request):
			raise KeyError("Either cookie is invalid or cookie is ip locked.")

	def validate(auth):
		request = scraper.get("https://rest-bf.blox.land/user", headers={
						"x-auth-token": auth
				}).json()
		if not "user" in list(request):
			return False
		return True


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
		if not "affiliateMoneyAvailable" in list(j):
			raise KeyError("Invalid authorization provided.")
		yield affiliate

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