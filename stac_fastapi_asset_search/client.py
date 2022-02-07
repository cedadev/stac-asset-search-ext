
"""Base clients."""
import abc
from datetime import datetime
from typing import List, Optional, Union

import attr
from .types import AssetCollection, AssetSearchPostRequest
from stac_fastapi.types.extension import ApiExtension

NumType = Union[float, int]


@attr.s  # type:ignore
class BaseAssetSearchClient(abc.ABC):
    """Defines a pattern for implementing STAC asset search endpoint."""

    extensions: List[ApiExtension] = attr.ib(default=attr.Factory(list))

    def extension_is_enabled(self, extension: str) -> bool:
        """Check if an api extension is enabled."""
        return any([type(ext).__name__ == extension for ext in self.extensions])

    @abc.abstractmethod
    def post_asset_search(
        self, search_request: AssetSearchPostRequest, **kwargs
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
        ids: Optional[List[str]] = None,
        items: Optional[List[str]] = None,
        collection: Optional[str] = None,
        bbox: Optional[List[NumType]] = None,
        datetime: Optional[Union[str, datetime]] = None,
        role: Optional[str] = None,
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

    extensions: List[ApiExtension] = attr.ib(default=attr.Factory(list))

    def extension_is_enabled(self, extension: str) -> bool:
        """Check if an api extension is enabled."""
        return any([type(ext).__name__ == extension for ext in self.extensions])

    @abc.abstractmethod
    def post_asset_search(
        self, search_request: AssetSearchPostRequest, **kwargs
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
        ids: Optional[List[str]] = None,
        items: Optional[List[str]] = None,
        collection: Optional[str] = None,
        bbox: Optional[List[NumType]] = None,
        datetime: Optional[Union[str, datetime]] = None,
        role: Optional[str] = None,
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

    @abc.abstractmethod
    def get_assets(self, item_id: str, collection_id: str, **kwargs,) -> AssetCollection:
        """asset search (GET).
        Called with `GET /collection/{collection_id}/items/{item_id}/assets`.
        Returns:
            AssetCollection containing assets for given item.
        """
        ...
