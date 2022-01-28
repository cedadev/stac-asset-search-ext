
"""Base clients."""
import abc
from datetime import datetime
from typing import List, Optional, Union

import attr
from .asset_search import AssetSearch
from .types import AssetCollection

NumType = Union[float, int]


@attr.s  # type:ignore
class BaseAssetSearchClient(abc.ABC):
    """Defines a pattern for implementing STAC asset search endpoint."""

    @abc.abstractmethod
    def post_asset_search(
        self, search_request: AssetSearch, **kwargs
    ) -> AssetCollection:
        """Cross catalog asset search (POST).
        Called with `POST /asset/search`.
        Args:
            search_request: search request parameters.
        Returns:
            AssetCollection containing assets which match the search criteria.
        """
        ...

    @abc.abstractmethod
    def get_asset_search(
        self,
        collections: Optional[List[str]] = None,
        itemIds: Optional[List[str]] = None,
        ids: Optional[List[str]] = None,
        bbox: Optional[List[NumType]] = None,
        datetime: Optional[Union[str, datetime]] = None,
        limit: Optional[int] = 10,
        query: Optional[str] = None,
        token: Optional[str] = None,
        fields: Optional[List[str]] = None,
        sortby: Optional[str] = None,
        **kwargs,
    ) -> AssetCollection:
        """Cross catalog asset search (GET).
        Called with `GET /asset/search`.
        Returns:
            AssetCollection containing assets which match the search criteria.
        """
        ...


@attr.s  # type:ignore
class AsyncBaseAssetSearchClient(abc.ABC):
    """Defines a pattern for implementing STAC asset search endpoint."""

    @abc.abstractmethod
    def post_asset_search(
        self, search_request: AssetSearch, **kwargs
    ) -> AssetCollection:
        """Cross catalog asset search (POST).
        Called with `POST /asset/search`.
        Args:
            search_request: search request parameters.
        Returns:
            AssetCollection containing assets which match the search criteria.
        """
        ...

    @abc.abstractmethod
    def get_asset_search(
        self,
        collections: Optional[List[str]] = None,
        itemIds: Optional[List[str]] = None,
        ids: Optional[List[str]] = None,
        bbox: Optional[List[NumType]] = None,
        datetime: Optional[Union[str, datetime]] = None,
        limit: Optional[int] = 10,
        query: Optional[str] = None,
        token: Optional[str] = None,
        fields: Optional[List[str]] = None,
        sortby: Optional[str] = None,
        **kwargs,
    ) -> AssetCollection:
        """Cross catalog asset search (GET).
        Called with `GET /asset/search`.
        Returns:
            AssetCollection containing assets which match the search criteria.
        """
        ...
