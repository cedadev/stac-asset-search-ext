# encoding: utf-8
"""Asset Search Extension"""

__author__ = 'Rhys Evans'
__date__ = '27 Jan 2022'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'rhys.r.evans@stfc.ac.uk'

from typing import List, Dict, Optional, Union

import attr
from fastapi import FastAPI
from pydantic import BaseModel

from stac_fastapi.types.extension import ApiExtension
from stac_fastapi.extensions.core import FieldsExtension
from stac_fastapi.api.models import SearchGetRequest, _create_request_model

from .types import AssetCollection, STACAssetSearch
from .client import AsyncBaseAssetSearchClient, BaseAssetSearchClient

CONFORMANCE_CLASSES = [
    'https://api.stacspec.org/v1.0.0-beta.2/asset-search'
]


@attr.s
class AssetSearchExtensionGetRequest(SearchGetRequest):
    """GET search request."""

    items: Optional[str] = attr.ib(default=None)

    def kwargs(self) -> Dict:
        """kwargs."""
        kwargs = super().kwargs()
        kwargs["items"] = self.items.split(",") if self.items else self.items
        return kwargs


class AssetSearchExtensionPostRequest(BaseModel):
    """Asset search extension POST request model."""
    q: Optional[str] = None


@attr.s
class AssetSearchExtension(ApiExtension):
    """Asset search extension


    The asset search extension adds the `asset/search` endpoint
    and allows the caller perform queries against asset properties.

    https://github.com/cedadev/stac-asset-search

    Attributes:
        conformance_classes (list): Defines the list of conformance classes
                                    for the extension.
    """

    client: Union[AsyncBaseAssetSearchClient, BaseAssetSearchClient] = attr.ib()

    conformance_classes: List[str] = attr.ib(
        default=CONFORMANCE_CLASSES
    )

    def register_get_asset_search(self):
        """Register search endpoint (GET /search).
        Returns:
            None
        """
        fields_ext = self.get_extension(FieldsExtension)
        self.router.add_api_route(
            name="Asset Search",
            path="/asset/search",
            response_model=(AssetCollection if not fields_ext else None)
            if self.settings.enable_response_models
            else None,
            response_class=self.response_class,
            response_model_exclude_unset=True,
            response_model_exclude_none=True,
            methods=["GET"],
            endpoint=self._create_endpoint(self.client.get_asset_search, AssetSearchExtensionGetRequest),
        )

    def register_post_asset_search(self):
        """Register search endpoint (POST /search).
        Returns:
            None
        """
        search_request_model = _create_request_model(attr.ib(STACAssetSearch))
        fields_ext = self.get_extension(FieldsExtension)
        self.router.add_api_route(
            name="Asset Search",
            path="/asset/search",
            response_model=(AssetCollection if not fields_ext else None)
            if self.settings.enable_response_models
            else None,
            response_class=self.response_class,
            response_model_exclude_unset=True,
            response_model_exclude_none=True,
            methods=["POST"],
            endpoint=self._create_endpoint(
                self.client.post_asset_search, search_request_model
            ),
        )

    def register(self, app: FastAPI) -> None:
        self.register_get_asset_search()
        self.register_post_asset_search()
        app.include_router(self.router, tags=["Asset Search Extension"])
