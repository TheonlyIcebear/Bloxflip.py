import cloudscraper, json
from .utils.errors import errors

scraper = cloudscraper.create_scraper()

class User:
    """An Object for a user's account info"""

    def __init__(self, info: dict) -> None:
        self.games_played = info["gamesPlayed"]
        self.games_won = info["gamesWon"]
        self.account_verified = info["hasVerifiedAccount"]
        self.total_deposited = info["totalDeposited"]
        self.total_withdrawn = info["totalWithdrawn"]
        self.total_wagered = info["wager"]
        self.username = info["user"]["robloxUsername"]
        self.roblox_id = info["user"]["robloxId"]
        self.rank = info["user"]["rank"]
        self.balance = info["user"]["wallet"]


class Authorization:
    def __init__(self) -> None:
        pass

    @staticmethod
    def generate(cookie: str, affiliate: str = "BFSB") -> str:

        """Generate a Bloxflip Auth Token from a Roblox Cookie"""
        request = scraper.post("https://api.bloxflip.com/user/login", json={
            "affiliateCode": affiliate,
            "cookie": cookie
        }).json()

        if "jwt" in list(request):
            return request["jwt"]

        raise errors.GeneralError("Either cookie is invalid or cookie is ip locked.")

    @staticmethod
    def validate(auth: str) -> bool:
        """Validates that the Authorization Token works"""

        request = scraper.get("https://api.bloxflip.com/user", headers={
            "x-auth-token": auth
        }).json()

        if request["success"]:
            return True

        return False

    @staticmethod
    def get_info(auth: str) -> User:
        """Gets user's info then returns in a class"""

        try:
            request = scraper.get("https://api.bloxflip.com/user", headers={
                "x-auth-token": auth
            }).json()
        except json.decoder.JSONDecodeError:
            raise errors.NetworkError("Network Error.")

        try:
            return User(request)
        except KeyError:
            raise errors.InvalidAuthorization("Invalid Authorization provided")


