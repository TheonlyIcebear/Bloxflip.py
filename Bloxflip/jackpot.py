import cloudscraper, websocket, requests, base64, json, time
from websocket import create_connection
from random import randbytes
from .utils.errors import errors

scraper = cloudscraper.create_scraper()


class Game:
    def __init__(self, info):
        self.value = sum([player["betAmount"] for player in info["players"]])
        self.time = info["timeLeft"]
        self.status = info["status"]
        self.winner = info["winner"]
        self.winningColor = info["winningColor"]
        self.id = info["_id"]


class Jackpot:
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
            ws.send("40/jackpot,")
            ws.send(f'42/jackpot,["auth","{self.auth}"]')

            return self._connection

        @property
        def connection(self) -> websocket.WebSocket:
            return self._connection

        def join(self, betamount: float, multiplier: float) -> None:
            """Joins Crash game with the betamount as well as multiplier"""

            json = str(
                {
                    "betAmount": betamount
                }
            ).replace("'", '"').replace(" ", "")
            self._connection.send(f'42/jackpot,["join-game",{str(json)}]')

    def Websocket(self):
        return self._Websocket(self.auth)

    @staticmethod
    def sniper(snipe_at: int = 0.05, interval: float = 0.01, on_game_start: type(print) = None) -> float:
        """Indefinitely yields the pot's value N seconds before wheel spins

        Parameters:
        amount (int): Amount of games to return each time
        interval (float): Time to wait in between each api request

        Returns:
        list: Recent games

        """

        if snipe_at > 29:
            raise errors.InvalidParameter("'snipe_at' cannot be above greater than 29")

        elif not callable(on_game_start) and on_game_start:
            raise errors.InvalidParameter("'on_game_start' must be a callable object.")

        while True:
            try:
                current = scraper.get("https://api.bloxflip.com/games/jackpot").json()["current"]
            except Exception as e:
                print(e)

            if len(current["players"]) == 2:
                time.sleep(30 - snipe_at)

                current = scraper.get("https://api.bloxflip.com/games/jackpot").json()["current"]

                pot_value = sum([player["betAmount"] for player in current["players"]])
                on_game_start(pot_value)

                yield Game(current)

            time.sleep(interval)

    @property
    def current(self) -> float:
        """Returns the current game's pot value

        Returns:
        int: Current game's value
        """

        try:
            current = scraper.get("https://api.bloxflip.com/games/jackpot").json()["current"]
        except json.decoder.JSONDecodeError:
            raise errors.NetworkError("A Network Error has occurred")

        return Game(current)
