__all__ = [
    "BaseResource",
    "Date",
    "DateTime",
    "list_all_resources",
]

from dataclasses import dataclass
from datetime import date as Date
from datetime import datetime as DateTime
from typing import Any, ClassVar, Dict, Iterable, List, Type, TypeVar

from pydantic import BaseModel

from decaf.api.client.machinery import Client
from decaf.api.client._internal import ProgrammingError


@dataclass(frozen=True)
class APIMeta:
    """
    Provides a model for API metadata information.
    """

    #: Path segment for the API endpoint.
    endpoint: str

    #: Indicates whether the resource is accessible by pagination or exposed as a single bulk collection.
    paged: bool


class BaseResource(BaseModel):
    """
    Provides a base class for standard DECAF resource models.
    """

    #: API metadata information.
    APIMeta: ClassVar[APIMeta]

    def __init_subclass__(cls, **kwargs: Any) -> None:
        """
        Compiles endpoint call machinery parameters for the resource.

        :param endpoint: Path segment for the resource listing endpoint.
        :param kwargs: Further keyword arguments to be passed the super method.
        """

        ## Check if the endpoint is provided:
        if "endpoint" not in kwargs:
            raise ProgrammingError(f"No endpoint specified for class {cls}.")

        ## Prepare and attach (override) the API metadata information class:
        cls.APIMeta = APIMeta(kwargs["endpoint"], kwargs.get("paged", False))


#: Defines a type alias for :py:class:`BaseResource` implementations.
_R = TypeVar("_R", bound=BaseResource)


def list_all_resources(client: Client, rtype: Type[_R]) -> List[_R]:
    """

    :param client:
    :param rtype:
    :return:
    """

    return [rtype(**d) for d in client.get(rtype.APIMeta.endpoint, params={"page_size": "-1"})]


#: Defines a type-alias for query parameters.
Params = Dict[str, str]


@dataclass(frozen=True)
class Repository:
    """
    Provides a repository machinery.
    """

    #: Client to access repository.
    client: Client

    def list(self, rtype: Type[_R], params: Params) -> Iterable[_R]:
        """
        Lists remote resources.

        :param rtype: Remote resource type.
        :param params: Listing parameters.
        :return: An iterable of remote resources.

        .. todo:: Retrieve large payloads in pages.
        """
        return (rtype(**d) for d in self.client.get(rtype.APIMeta.endpoint, params={**params, "page_size": "-1"}))
