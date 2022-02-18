# encoding: utf-8
"""Asset Search Extension"""

__author__ = 'Rhys Evans'
__date__ = '27 Jan 2022'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'rhys.r.evans@stfc.ac.uk'

from distutils import extension
from typing import Callable, List, Union, Type

import attr
from fastapi import APIRouter, FastAPI
from starlette.responses import JSONResponse, Response
from pydantic import BaseModel

from stac_fastapi.types.extension import ApiExtension
from stac_fastapi.api.models import APIRequest
from stac_fastapi.types.config import ApiSettings
from stac_fastapi.api.routes import create_async_endpoint, create_sync_endpoint

from .types import AssetCollection, AssetSearchGetRequest, AssetSearchPostRequest, GetAssetsRequest
from .client import BaseAssetSearchClient, AsyncBaseAssetSearchClient

CONFORMANCE_CLASSES = [
    'https://api.stacspec.org/v1.0.0-beta.2/asset-search'
]


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

    client: Union[AsyncBaseAssetSearchClient, BaseAssetSearchClient] = attr.ib(default = None)
    settings: ApiSettings = attr.ib(default = None)
    conformance_classes: List[str] = attr.ib(
        default=CONFORMANCE_CLASSES
    )
    router: APIRouter = attr.ib(factory=APIRouter)
    response_class: Type[Response] = attr.ib(default=JSONResponse)
    extensions: List[ApiExtension] = attr.ib(default=attr.Factory(list))
    asset_search_get_request_model: Type[AssetSearchGetRequest] = attr.ib(
        default=AssetSearchGetRequest
    )
    asset_search_post_request_model: Type[AssetSearchPostRequest] = attr.ib(
        default=AssetSearchPostRequest
    )

    def _create_endpoint(
        self,
        func: Callable,
        request_type: Union[Type[APIRequest], Type[BaseModel],],
    ) -> Callable:
        """Create a FastAPI endpoint."""
        if isinstance(self.client, AsyncBaseAssetSearchClient):
            return create_async_endpoint(
                func, request_type, response_class=self.response_class
            )
        elif isinstance(self.client, BaseAssetSearchClient):
            return create_sync_endpoint(
                func, request_type, response_class=self.response_class
            )
        raise 

    def register_get_asset_search(self):
        """Register asset search endpoint (GET /asset/search).
        Returns:
            None
        """
        self.router.add_api_route(
            name="Asset Search",
            path="/asset/search",
            response_model=AssetCollection
            if self.settings and self.settings.enable_response_models
            else None,
            response_class=self.response_class,
            response_model_exclude_unset=True,
            response_model_exclude_none=True,
            methods=["GET"],
            endpoint=self._create_endpoint(self.client.get_asset_search, self.asset_search_get_request_model),
        )

    def register_post_asset_search(self):
        """Register asset search endpoint (POST /asset/search).
        Returns:
            None
        """
        self.router.add_api_route(
            name="Asset Search",
            path="/asset/search",
            response_model=AssetCollection
            if self.settings and self.settings.enable_response_models
            else None,
            response_class=self.response_class,
            response_model_exclude_unset=True,
            response_model_exclude_none=True,
            methods=["POST"],
            endpoint=self._create_endpoint(self.client.post_asset_search, self.asset_search_post_request_model),
        )
    
    def register_get_assets(self):
        """Register asset search endpoint (GET /collection/{collection_id}/items/{item_id}/assets).
        Returns:
            None
        """
        self.router.add_api_route(
            name="Get Assets",
            path="/collections/{collection_id}/items/{item_id}/assets",
            response_model=AssetCollection
            if self.settings and self.settings.enable_response_models
            else None,
            response_class=self.response_class,
            response_model_exclude_unset=True,
            response_model_exclude_none=True,
            methods=["GET"],
            endpoint=self._create_endpoint(self.client.get_assets, GetAssetsRequest),
        )

    def register(self, app: FastAPI) -> None:
        self.register_get_asset_search()
        self.register_post_asset_search()
        self.register_get_assets()
        app.include_router(self.router, tags=["Asset Search Extension"])
