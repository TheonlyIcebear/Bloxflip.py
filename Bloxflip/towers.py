import cloudscraper, json, time
from .utils.errors import errors

scraper = cloudscraper.create_scraper()


class Tower:
    """A class for a Towers game"""

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


class Towers:
    def __init__(self, auth):
        self.auth = auth

    def create(self, betamount: float, difficulty: str) -> dict:
        """Creates a towers game"""

        if not difficulty in ["easy", "normal", "hard"]:
            raise errors.InvalidParameter("Invalid difficulty provided.")

        response = scraper.post("https://rest-bf.blox.land/games/towers/create", headers={
                        "x-auth-token": self.auth
                    },
                    json={
                        "betAmount": str(betamount),
                        "difficulty": difficulty
                    }
                )

        if betamount < 5:
            raise errors.InvalidParameter("Bet amount must be greater than 5")

        if response.status_code == 429:
            raise errors.Ratelimited("Ratelimited: Too many requests")

        if not response.status_code == 200:
            try:
                response.json()
            except ValueError:
                raise errors.NetworkError("Network error.", "error")

            if response.json()["msg"] == "You already have an active towers game!":
                raise errors.GameAlreadyStarted("You already have an active towers game. End it then try again.")

            elif response.json()["msg"] == "You can not afford to start this game!":
                raise errors.InsufficientFunds("You cannot afford to start this game.")

            raise errors.GeneralError("Failed to create game")

        return response.json()

    def choose(self, choice: int) -> bool:
        """Chooses a tile to uncover"""

        response = scraper.post("https://rest-bf.blox.land/games/towers/action", headers={
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

    def cashout(self) -> object:
        """Cashes out the winnings from the current game"""

        response = scraper.post("https://rest-bf.blox.land/games/towers/action", headers={
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

            raise errors.InsufficientFunds("Insuffecient funds")

        return response.json()

    @property
    def current(self) -> Tower:
        request = scraper.get("https://api.bloxflip.com/games/mines", headers={
                        "x-auth-token": self.auth
                    }
                ).json()

        try:
            return Tower(request)
        except (KeyError, Exception):
            raise errors.InvalidAuthorization("Invalid authorization provided.")
