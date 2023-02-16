from __future__ import annotations

from abc import ABC
from dataclasses import dataclass, field

import ee


@dataclass(frozen=False)
class _BaseData(ABC):
    ROI: ee.Geometry
    ASSET_ID: str = field(default=None)
    NIR: str = field(default=None)
    RED: str = field(default=None)
    START_Y: int = field(default=None)
    END_Y: int = field(default=None)

    def cloud_mask(element: ee.Image):
        raise NotImplementedError


@dataclass(frozen=False)
class LandSAT8SR(_BaseData):
    ASSET_ID: str = field(default="LANDSAT/LC08/C02/T1_L2")
    NIR: str = field(default=None)
    RED: str = field(default=None)
    START_Y: int = field(default=None)
    END_Y: int = field(default=None)


@dataclass(frozen=False)
class Sentinel2(_BaseData):
    NIR: str = field(default='B8')
    RED: str = field(default='B4')

    @staticmethod
    def cloud_mask(element: ee.Image):
        qa = element.select('QA60')
        cloudBitMask = 1 << 10
        cirrusBitMask = 1 << 11
        mask = qa.bitwiseAnd(cloudBitMask).eq(0).And(qa.bitwiseAnd(cirrusBitMask).eq(0))
        return element.updateMask(mask)
 

@dataclass(frozen=False)
class Sentinel2TOA(Sentinel2):
    ASSET_ID: str =field(default="COPERNICUS/S2_HARMONIZED")
    START_Y: int = field(default=2015)
    END_Y: int = field(default=2023)



@dataclass(frozen=False)
class Sentinel2SR(Sentinel2):
    ASSET_ID: str =field(default="COPERNICUS/S2_SR_HARMONIZED")
    START_Y: int = field(default=2017)
    END_Y: int = field(default=2023)

