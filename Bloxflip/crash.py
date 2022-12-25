import cloudscraper, websocket, requests, base64, json, time
from typing import Union, Generator, Any
from websocket import create_connection
from random import randbytes
from utils.errors import errors

scraper = cloudscraper.create_scraper()


class Round:
    """A wrapper for a Crash game"""

    def __init__(self, game: dict) -> None:
        self.crash_point = game["crashPoint"]
        self.public_seed = game["publicSeed"]
        self.private_seed = game["privateSeed"]
        self.private_hash = game["privateHash"]
        self.game_id = game["_id"]


class Crash:
    def __init__(self, auth: str) -> None:
        self.auth = auth

    class _Websocket:
        def __init__(self, auth: str) -> None:
            self.auth = auth
            self._connection = None

        def connect(self, headers: dict = {
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
            }) -> websocket.WebSocket:
            """Connects to websocket and returns websocket object
            
            Parameters:
            headers (dict): Headers to be used to connect to websocket (Optional)

            Returns:
            websocket.WebSocket: A websocket connection connected and already logged in
            """

            self._connection = create_connection("wss://ws.bloxflip.com/socket.io/?EIO=3&transport=websocket", header=headers,
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
                    "autoCashoutPoint": int(multiplier * 100),
                    "betAmount": betamount
                }
            ).replace("'", '"').replace(" ", "")
            self._connection.send(f'42/crash,["join-game",{str(json)}]')

    def Websocket(self):
        return self._Websocket(self.auth)

    @staticmethod
    def crashpoints(amount: int = 35, interval: float = 0.01, on_game_start: =None) -> Generator[list[Union[Round, list[Round]]], Any, Any]:
        """Indefinitely yields the last game's results as well as the previous results everytime a new game starts
        
        Parameters:
        amount (int): Amount of games to return each time
        interval (float): Time to wait in between each api request

        Returns:
        list: Recent games
        
        """

        history = None
        sent = False

        if amount > 35:
            raise errors.InvalidParamater("Amount cannot be above 35.")

        elif not callable(on_game_start) and on_game_start:
            raise errors.InvalidParamater("'on_game_start' must be a callable object.")

        while True:
            try:
                games = scraper.get("https://rest-bf.blox.land/games/crash").json()
            except ValueError:
                continue
            
            data = [Round(games["history"][0]), [Round(_crashpoint) for _crashpoint in history]]

            if history != games["history"]:
                history = games["history"]
                if on_game_start:
                    on_game_start(data)
                yield data
            time.sleep(interval)

    @property
    def history(self, amount: int = 35) -> list:
        """Returns the last N games, 35 by default"""

        try:
            games = scraper.get("https://rest-bf.blox.land/games/crash").json()
        except:
            raise errors.NetworkError("A Network Error has occured")

        history = games["history"]

        return [[Round(_crashpoint) for _crashpoint in history[:amount]]]