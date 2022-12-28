import cloudscraper, websocket, requests, base64, json, time
from websocket import create_connection
from random import randbytes
from .utils.errors import errors

scraper = cloudscraper.create_scraper()


class Round:
    """A wrapper for a Crash game"""

    def __init__(self, game: dict) -> None:
        self.crashpoint = game["crashPoint"]
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
        }) -> websocket.WebSocket:
            """Connects to websocket and returns websocket object
            
            Parameters:
            headers (dict): Headers to be used to connect to websocket (Optional)

            Returns:
            websocket.WebSocket: A websocket connection connected and already logged in
            """

            self._connection = create_connection(
                "wss://ws.bloxflip.com/socket.io/?EIO=3&transport=websocket",
                suppress_origin=True,
                header=headers
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
    def crashpoints(amount: int = 35, interval: float = 0.01, on_game_start: type(print) = None) -> list:
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
            raise errors.InvalidParameter("Amount cannot be above 35.")

        elif not callable(on_game_start) and on_game_start:
            raise errors.InvalidParameter("'on_game_start' must be a callable object.")

        while True:
            try:
                games = scraper.get("https://api.bloxflip.com/games/crash").json()
            except ValueError:
                continue

            if history != games["history"]:
                history = games["history"]

                data = [Round(_crashpoint) for _crashpoint in history]

                if not sent:
                    sent = True
                    continue

                if on_game_start:
                    on_game_start(data)
                yield data

            time.sleep(interval)

    @property
    def history(self, amount: int = 35) -> list:
        """Returns the last N games, 35 by default
        
        Parameter:
        amount (int): Amount of games returned
        
        Returns:
        list: Recent games"""

        try:
            games = scraper.get("https://api.bloxflip.com/games/crash").json()
        except json.decoder.JSONDecodeError:
            raise errors.NetworkError("A Network Error has occurred.")

        history = games["history"]

        return [[Round(_crashpoint) for _crashpoint in history[:amount]]]
