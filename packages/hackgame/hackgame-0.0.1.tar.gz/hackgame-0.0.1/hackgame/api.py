from datetime import datetime
from json import JSONDecodeError
from typing import List, Type, TypeVar, Generic, Optional

import requests

from hackgame.models import (
    World, AccessToken, Player,
    Account, Network, Connection,
    Program, Ice, ActionResult, ActionError,
    ErrorCode)


class BearerAuth(requests.auth.AuthBase):

    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["Authorization"] = f"Token {self.token}"
        return r


# HACKGAME_SERVER = "https://hackgame.dev.rachsharp.co.uk"
HACKGAME_SERVER = "http://localhost:8000"
API_BASE = "/api"

Resource = TypeVar("Resource")


class ObjectEndpoint(Generic[Resource]):

    def __init__(self, endpoint: str, object_class: Type[Resource], client):
        self.endpoint = endpoint
        self._class = object_class
        self._client = client

    @property
    def url(self) -> str:
        return f"{HACKGAME_SERVER}{API_BASE}/{self.endpoint}/"

    def create(self, data) -> Resource:
        response = self._client.session.post(self.url, data=data)
        response.raise_for_status()
        response = self._client.session.get(
            f"{self.url}{response.json()['public_uuid']}/"
        )
        return self._class(**response.json())

    def get(self, public_uuid) -> Resource:
        try:
            response = self._client.session.get(f"{self.url}{public_uuid}/")
            response.raise_for_status()
            obj = self._class(**response.json())
        except requests.exceptions.HTTPError as e:
            print(e)
            obj = None
        return obj

    def list(self) -> List[Resource]:
        response = self._client.session.get(self.url)
        response.raise_for_status()
        try:
            return [self._class(**item) for item in response.json()]
        except Exception:
            print(response.json())
            raise

    def proxy(self, public_uuid) -> ActionResult:
        response = self._client.session.post(
            f"{self.url}{public_uuid}/proxy/"
        )
        try:
            action_result = ActionResult(
                status_code=response.status_code, **response.json()
            )
        except (TypeError, JSONDecodeError) as e:
            action_result = ActionResult(
                success=False, status_code=response.status_code,
                errors=[ActionError(code=ErrorCode.generic, message=response.text)]
            )
        return action_result

    def post(self, public_uuid, data) -> ActionResult:
        response = self._client.session.post(
            f"{self.url}{public_uuid}/post/", json=data
        )

        # todo how to handle 500s but not 4XXs
        # todo also handle invalid player tokens
        try:
            action_result = ActionResult(
                status_code=response.status_code, **response.json()
            )
        except TypeError:
            action_result = ActionResult(
                success=False, status_code=response.status_code,
                errors=[ActionError(code=ErrorCode.generic, message=response.text)]
            )
        return action_result

    def transfer(self, public_uuid, data) -> ActionResult:
        response = self._client.session.post(
            f"{self.url}{public_uuid}/transfer/", json=data,
        )
        try:
            action_result = ActionResult(
                status_code=response.status_code, **response.json()
            )
        except TypeError:
            action_result = ActionResult(
                success=False, status_code=response.status_code,
                errors=[ActionError(code=ErrorCode.generic, message=response.text)]
            )
        return action_result


class HackgameClient(object):

    def __init__(self, player_token: str, token: Optional[str] = None):
        """
        :param player_token:
            Actual Secure Authentication Token, to determine which real
            person is playing the game.
        :param token:
            Insecure Token to determine what Object this Hackgame
            Client will be acting as.
        """
        session = requests.Session()

        self.game_token = token
        if self.game_token is not None:
            session.headers.update({"Access-Token": self.game_token})

        session.auth = BearerAuth(token=player_token)
        self.session = session

        self.players = ObjectEndpoint[Player]("players", Player, client=self)
        self.accounts = ObjectEndpoint[Account]("accounts", Account,
                                                client=self)
        self.tokens = ObjectEndpoint[AccessToken]("tokens", AccessToken,
                                                  client=self)
        self.worlds = ObjectEndpoint[World](
            "worlds", World,
            client=self
        )
        self.networks = ObjectEndpoint[Network](
            "networks", Network, client=self
        )
        self.connections = ObjectEndpoint[Connection](
            "connections", Connection, client=self
        )
        self.programs = ObjectEndpoint[Program](
            "programs", Program, client=self
        )

        self.ice = ObjectEndpoint[Ice](
            "ice", Ice, client=self
        )

        self.registry = {
            Player: self.players,
            Account: self.accounts,
            AccessToken: self.tokens,
            World: self.worlds,
            Network: self.networks,
            Connection: self.connections,
            Program: self.programs,
            Ice: self.ice,
        }

    def __getitem__(self, item) -> ObjectEndpoint:
        return self.registry[item]

    def messages(self, after: datetime = None) -> List[str]:
        url = f"{self.tokens.url}{self.game_token}/messages/"
        params = {}
        if after is not None:
            params["after"] = after.isoformat()
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()["messages"]
