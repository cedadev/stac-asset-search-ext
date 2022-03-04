import attr
from datetime import datetime
from urllib.parse import urljoin
from geojson_pydantic.geometries import (
    LineString,
    MultiLineString,
    MultiPoint,
    MultiPolygon,
    Point,
    Polygon,
    _GeometryBase,
)

from stac_fastapi.types.search import APIRequest, str2list

from typing import Any, Dict, List, Optional, Union
from typing_extensions import TypedDict

from pydantic import BaseModel

from pydantic import BaseModel, conint, validator
from pydantic.datetime_parse import parse_datetime
from stac_pydantic.links import Relations
from stac_fastapi.types.links import BaseLinks
from stac_pydantic.shared import BBox, MimeTypes

NumType = Union[float, int]


class Asset(TypedDict, total=False):

    type: str
    stac_version: str
    stac_extensions: Optional[List[str]]
    id: str
    items: Optional[str]
    geometry: Dict[str, Any]
    bbox: List[NumType]
    properties: Dict[str, Any]
    links: List[Dict[str, Any]]
    role: Optional[str]


class AssetCollection(TypedDict, total=False):

    type: str
    stac_version: str
    features: List[Asset]
    stac_extensions: Optional[List[str]]
    links: List[Dict[str, Any]]
    context: Optional[Dict[str, int]]


@attr.s
class AssetSearchGetRequest(APIRequest):
    """Base arguments for GET  Request."""

    ids: Optional[str] = attr.ib(default=None, converter=str2list)
    items: Optional[str] = attr.ib(default=None)
    bbox: Optional[str] = attr.ib(default=None, converter=str2list)
    intersects: Optional[str] = attr.ib(default=None, converter=str2list)
    datetime: Optional[str] = attr.ib(default=None)
    role: Optional[str] = attr.ib(default=None)
    limit: Optional[int] = attr.ib(default=10)


class AssetSearchPostRequest(BaseModel):
    """Asst Search model."""

    ids: Optional[List[str]]
    items: Optional[List[str]]
    collection: Optional[str]
    bbox: Optional[BBox]
    intersects: Optional[
        Union[Point, MultiPoint, LineString, MultiLineString, Polygon, MultiPolygon]
    ]
    datetime: Optional[str]
    role: Optional[List[str]]
    limit: Optional[conint(gt=0, le=10000)] = 10

    @property
    def start_date(self) -> Optional[datetime]:
        """Extract the start date from the datetime string."""
        if not self.datetime:
            return

        values = self.datetime.split("/")
        if len(values) == 1:
            return None
        if values[0] == "..":
            return None
        return parse_datetime(values[0])

    @property
    def end_date(self) -> Optional[datetime]:
        """Extract the end date from the datetime string."""
        if not self.datetime:
            return

        values = self.datetime.split("/")
        if len(values) == 1:
            return parse_datetime(values[0])
        if values[1] == "..":
            return None
        return parse_datetime(values[1])

    @validator("intersects")
    def validate_spatial(cls, v, values):
        """Check bbox and intersects are not both supplied."""
        if v and values["bbox"]:
            raise ValueError("intersects and bbox parameters are mutually exclusive")
        return v

    @validator("bbox")
    def validate_bbox(cls, v: BBox):
        """Check order of supplied bbox coordinates."""
        if v:
            # Validate order
            if len(v) == 4:
                xmin, ymin, xmax, ymax = v
            else:
                xmin, ymin, min_elev, xmax, ymax, max_elev = v
                if max_elev < min_elev:
                    raise ValueError(
                        "Maximum elevation must greater than minimum elevation"
                    )

            if xmax < xmin:
                raise ValueError(
                    "Maximum longitude must be greater than minimum longitude"
                )

            if ymax < ymin:
                raise ValueError(
                    "Maximum longitude must be greater than minimum longitude"
                )

            # Validate against WGS84
            if xmin < -180 or ymin < -90 or xmax > 180 or ymax > 90:
                raise ValueError("Bounding box must be within (-180, -90, 180, 90)")

        return v

    @validator("datetime")
    def validate_datetime(cls, v):
        """Validate datetime."""
        if "/" in v:
            values = v.split("/")
        else:
            # Single date is interpreted as end date
            values = ["..", v]

        dates = []
        for value in values:
            if value == "..":
                dates.append(value)
                continue

            parse_datetime(value)
            dates.append(value)

        if ".." not in dates:
            if parse_datetime(dates[0]) > parse_datetime(dates[1]):
                raise ValueError(
                    "Invalid datetime range, must match format (begin_date, end_date)"
                )

        return v

    @property
    def spatial_filter(self) -> Optional[_GeometryBase]:
        """Return a geojson-pydantic object representing the spatial filter for the search request.
        Check for both because the ``bbox`` and ``intersects`` parameters are mutually exclusive.
        """
        if self.bbox:
            return Polygon(
                coordinates=[
                    [
                        [self.bbox[0], self.bbox[3]],
                        [self.bbox[2], self.bbox[3]],
                        [self.bbox[2], self.bbox[1]],
                        [self.bbox[0], self.bbox[1]],
                        [self.bbox[0], self.bbox[3]],
                    ]
                ]
            )
        if self.intersects:
            return self.intersects
        return


@attr.s
class GetAssetsRequest(APIRequest):
    """Base arguments for GET  Request."""

    collection_id: str = attr.ib()
    item_id: str = attr.ib()


@attr.s
class GetAssetRequest(APIRequest):
    """Base arguments for GET  Request."""

    collection_id: str = attr.ib()
    item_id: str = attr.ib()
    asset_id: str = attr.ib()


@attr.s
class AssetLinks(BaseLinks):
    """Create inferred links specific to assets."""

    asset_id: str = attr.ib()
    item_id: str = attr.ib()

    def root(self) -> Dict[str, Any]:
        """Return the catalog root."""
        return dict(rel=Relations.root, type=MimeTypes.json, href=self.base_url)

    def self(self) -> Dict[str, Any]:
        """Create the `self` link."""
        url = f"collections/{self.collection_id}/items/{self.item_id}/assets/{self.asset_id}" if self.collection_id else f"asset/search/?ids={self.asset_id}"
        return dict(
            rel=Relations.self,
            type=MimeTypes.geojson,
            href=urljoin(
                self.base_url,
                url,
            ),
        )

    def parent(self) -> Dict[str, Any]:
        """Create the `parent` link."""
        url = f"collections/{self.collection_id}/items/{self.item_id}" if self.collection_id else f"search/?ids={self.item_id}"
        return dict(
            rel=Relations.parent,
            type=MimeTypes.json,
            href=urljoin(self.base_url, url),
        )

    def item(self) -> Dict[str, Any]:
        """Create the `item` link."""
        url = f"collections/{self.collection_id}/items/{self.item_id}" if self.collection_id else f"search/?ids={self.item_id}"
        return dict(
            rel=Relations.item,
            type=MimeTypes.json,
            href=urljoin(self.base_url, url),
        )

    def create_links(self) -> List[Dict[str, Any]]:
        """Return all inferred links."""
        links = [
            self.self(),
            self.parent(),
            self.item(),
            self.root(),
        ]
        return links
