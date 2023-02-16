from __future__ import annotations

import math
from dataclasses import dataclass, field, InitVar
from typing import List, Union, Any, Dict

import ee

import ts


@dataclass
class HarmonicCFG:
    dependent: str = field(default='NDVI')
    independents: list = field(default_factory= lambda: ['constant', 't'])
    harmonics: int = 2
    omega: float = 1.5
    
    def __post_init__(self):
        self.harmonic_freq = list(range(1, self.harmonics + 1))
        self.cos_names = [f'cos_{ _ }' for _ in self.harmonic_freq]
        self.sin_names = [f'sin_{ _ }' for _ in self.harmonic_freq]
        self.independents = [*self.independents, *self.cos_names, *self.sin_names]



class HarmonicModel:
    def __init__(self, col: ts.TimeSeries, cfg: HarmonicCFG) -> None:
        self.config = col.config
        self.time_series = col
        self.harmonic_trend = self.time_series.select([*self.config.independents, 
                                                           self.config.dependent]).\
            reduce(ee.Reducer.linearRegression(**{
                'numX': len(self.config.independents),
                'numY': 1
            }))
        
        self.harmonic_coeff = self.harmonic_trend.select('coefficients').\
            arrayProject([0]).\
            arrayFlatten([self.config.independents])

    @property
    def phase(self) -> ee.Image:
        def mk_phase_inner(b1, b2):
            return self.harmonic_coeff.select(b1).atan2(self.harmonic_coeff.select(b2))\
                .unitScale(-math.pi, math.pi)
        
        stack = ee.Image.cat(*[mk_phase_inner(x,y) for x,y in zip(self.config.sin_names, 
                                                                 self.config.cos_names)])
    
        old_names: ee.List = stack.bandNames()
        new_names = [f'phase_{idx}' for idx, _ in enumerate(self.config.sin_names, start=1)]
        return stack.select(old_names, new_names)

    @property
    def amplitude(self) -> ee.Image:
        
        def mk_amp_inner(numerator, denominator) -> ee.Image:
            return self.harmonic_coeff.select(numerator)\
                .hypot(self.harmonic_coeff.select(denominator)).multiply(5)
        
        stack = ee.Image.cat(*[mk_amp_inner(x,y) for x,y in zip(self.config.sin_names, 
                                                                self.config.cos_names)])
        
        band_names: ee.List = stack.bandNames()
        new_names = [f'amp_{idx}' for idx, _ in enumerate(self.config.sin_names, start=1)]
        return stack.select(band_names, new_names)

    @property
    def mean_dependent(self) -> ee.Image:
        return self.time_series.select(self.config.dependent).mean()\
            .rename(f'{self.config.dependent}_mean')
    
    def fit_harmonics(self, collection: bool = True) -> Union[ee.ImageCollection, List[ee.Image]]:
        #TODO need to make it so that we can take a list of images and not a collection

        def fit_inner(element: ee.Image):
            return element.addBands(element.select(self.config.independents).\
                multiply(self.harmonic_coeff).\
                reduce('sum').\
                rename('fitted')
            )

        return self.time_series.map(fit_inner)
    