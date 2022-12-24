import cloudscraper, websocket, requests, base64, json, time, ssl, os
from typing import Union, Generator, Any
from websocket import create_connection
from random import randbytes
from utils.errors import errors

scraper = cloudscraper.create_scraper()

class Authorization:
    def __init__(self) -> None:
        pass

    @staticmethod
    def generate(cookie: str) -> str:

        """Generate a Bloxflip Auth Token from a Roblox Cookie"""
        request = scraper.post("https://rest-bf.blox.land/user/login", json={
            "affiliateCode": "BFSB",
            "cookie": cookie
        }).json()

        if "jwt" in list(request):
            return request["jwt"]

        raise errors.GeneralError("Either cookie is invalid or cookie is ip locked.")

    @staticmethod
    def validate(auth: str) -> bool:
        """Validates that the Authorization Token works"""

        request = scraper.get("https://rest-bf.blox.land/user", headers={
            "x-auth-token": auth
        }).json()

        if request["success"]:
            return True

        return False