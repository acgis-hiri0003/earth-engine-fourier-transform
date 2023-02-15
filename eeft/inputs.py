from __future__ import annotations

import math
from abc import ABC, abstractstaticmethod
from dataclasses import dataclass, field, InitVar
from typing import Union, Callable, List

import ee

@dataclass(frozen=True)
class _BaseData(ABC):
    ASSET_ID: str = field(default=None)
    NIR: str = field(default=None)
    RED: str = field(default=None)
    START_Y: int = field(default=None)
    END_Y: int = field(default=None)

    def cloud_mask(element: ee.Image):
        raise NotImplementedError


@dataclass(frozen=True)
class LandSAT8SR(_BaseData):
    ASSET_ID: str = field(default="LANDSAT/LC08/C02/T1_L2")
    NIR: str = field(default=None)
    RED: str = field(default=None)
    START_Y: int = field(default=None)
    END_Y: int = field(default=None)


@dataclass
class Sentinel2(_BaseData):
    NIR: str = field(default='B8')
    RED: str = field(default='B4')

    def cloud_mask(element: ee.Image):
        qa = element.select('QA60')
        cloudBitMask = 1 << 10
        cirrusBitMask = 1 << 11
        mask = qa.bitwiseAnd(cloudBitMask).eq(0).And(qa.bitwiseAnd(cirrusBitMask).eq(0))
        return element.updateMask(mask)
 

@dataclass(frozen=True)
class Sentinel2TOA(_BaseData):
    ASSET_ID: str =field(default="COPERNICUS/S2_HARMONIZED")
    START_Y: int = field(default=2015)
    END_Y: int = field(default=2023)



@dataclass(frozen=True)
class Sentinel2SR(_BaseData):
    ASSET_ID: str =field(default="COPERNICUS/S2_SR_HARMONIZED")
    START_Y: int = field(default=2017)
    END_Y: int = field(default=2023)

