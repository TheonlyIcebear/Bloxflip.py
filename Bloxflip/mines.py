import cloudscraper, json, time
from .utils.errors import errors

scraper = cloudscraper.create_scraper()


class Mine:
    """A class for a Mines game"""

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


class Mines:
    def __init__(self, auth: str) -> None:
        self.auth = auth

    def create(self, betamount: float, mines: int) -> None:
        """Creates a mines game"""

        response = scraper.post("https://api.bloxflip.com/games/mines/create", headers={
                        "x-auth-token": self.auth
                    },
                    json={
                        "betAmount": betamount,
                        "mines": mines
                    }
                )

        if betamount < 5:
            raise errors.InvalidParameter("Bet amount must be greater than 5")

        if response.status_code == 429:
            raise errors.Ratelimited("Ratelimited: Too many requests")

        if not response.status_code == 200:
            try:
                response.json()
            except json.decoder.JSONDecodeError:
                raise errors.NetworkError("Network error.", "error")
            if response.json()["msg"] == "You already have an active mines game!":
                raise errors.GameAlreadyStarted("You already have an active mines game. End it then try again.")
            if response.json()["msg"] == "You can not afford to start this game!":
                raise errors.InsufficientFunds("You cannot afford to start this game.")

            raise errors.GeneralError("Failed to create game")

    def choose(self, choice: int) -> bool:
        """Chooses a tile to bet on"""

        response = scraper.post("https://api.bloxflip.com/games/mines/action", headers={
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

        response = scraper.post("https://api.bloxflip.com/games/mines/action", headers={
                            "x-auth-token": self.auth
                        },
                        json={
                            "cashout": True
                        }
                    )

        if response.status_code == 200:
            return response

        if not "msg" in list(response.json()):
            raise errors.InvalidAuthorization("Invalid authorization provided.")

        elif response.json()["msg"] == "You do not have an active mines game!":
            raise errors.GameNotStarted("You do not have an active mines game.")

        elif response.json()["msg"] == "You cannot cash out yet! You must uncover at least one tile!":
            raise errors.GeneralError("You cannot cash out yet! You must uncover at least one tile!")

        return False

    @property
    def current(self) -> Mine:
        request = scraper.get("https://api.bloxflip.com/games/towers", headers={
                        "x-auth-token": self.auth
                    }
                ).json()

        try:
            return Mine(request)
        except (KeyError, Exception):
            raise errors.InvalidAuthorization("Invalid authorization provided.")
