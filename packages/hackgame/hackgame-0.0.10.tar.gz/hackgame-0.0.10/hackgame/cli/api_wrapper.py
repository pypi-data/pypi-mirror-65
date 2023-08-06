from typing import List, Generic

from click import ClickException
from requests import HTTPError

from hackgame.api import ObjectEndpoint, Resource


def pretty_hackgame_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except HTTPError as e:
            status_code = e.response.status_code
            if status_code == 401:
                raise ClickException(
                    "401 unauthorized! have you logged in with `hackgame login`?"
                ) from e
            elif status_code == 403:
                detail = e.response.json().get("detail")
                if detail == "token is required to do this":
                    raise ClickException(
                        "403 forbidden! you need to set a valid token with "
                        "`hackgame use token`"
                    )
                elif detail == "Invalid token.":
                    raise ClickException(
                        "403 forbidden! have you logged in with `hackgame login`?"
                    )
                else:
                    raise
            else:
                raise

    return wrapper


class ClickRaisingObjectEndpoint(ObjectEndpoint, Generic[Resource]):
    """
    Wrapper around ObjectEndpoint that returns a prettier error when we know that
    a HTTP 401, 403, etc., is due to something that the user can fix themselves.
    """

    @pretty_hackgame_error
    def get(self, public_uuid) -> Resource:
        return super().get(public_uuid)

    @pretty_hackgame_error
    def create(self, data) -> Resource:
        return super().create(data)

    @pretty_hackgame_error
    def list(self) -> List[Resource]:
        return super().list()
