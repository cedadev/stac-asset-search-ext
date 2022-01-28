from typing import List, Optional

from geojson_pydantic.features import Feature, FeatureCollection
from pydantic import AnyUrl, Field, constr

from stac_pydantic.api.extensions.context import ContextExtension
from stac_pydantic.links import Links
from stac_pydantic.item import Item, ItemProperties
from stac_pydantic.shared import BBox
from stac_pydantic.version import STAC_VERSION

from stac_fastapi.types.search import STACSearch


class AssetProperties(ItemProperties):
    ...


class Asset(Feature):

    id: constr(min_length=1)
    stac_version: constr(min_length=1) = Field(STAC_VERSION, const=True)
    properties: AssetProperties
    assets: List[str, Item]
    links: Links
    bbox: BBox
    stac_extensions: Optional[List[AnyUrl]]
    collection: Optional[str]

    def to_dict(self, **kwargs):
        return self.dict(by_alias=True, exclude_unset=True, **kwargs)

    def to_json(self, **kwargs):
        return self.json(by_alias=True, exclude_unset=True, **kwargs)


class AssetCollection(FeatureCollection):

    stac_version: constr(min_length=1) = Field(STAC_VERSION, const=True)
    features: List[Asset]
    stac_extensions: Optional[List[AnyUrl]]
    links: Links
    context: Optional[ContextExtension]

    def to_dict(self, **kwargs):
        return self.dict(by_alias=True, exclude_unset=True, **kwargs)

    def to_json(self, **kwargs):
        return self.json(by_alias=True, exclude_unset=True, **kwargs)


class STACAssetSearch(STACSearch):
    """Asset search model."""

    # Make items optional, default to searching all items if none are provided
    items: Optional[List[str]] = None