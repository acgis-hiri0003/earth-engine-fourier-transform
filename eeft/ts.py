import ee

import data
import funcs
import harm

class TimeSeries:
    
    def __new__(cls, data: data._BaseData, hcfg) -> ee.ImageCollection:
        
        instance = ee.ImageCollection(data.ASSET_ID).filterBounds(data.ROI)\
            .filterDate(f'{data.START_Y}', f'{data.END_Y}')\
            .map(data.cloud_mask)\
            .map(funcs.add_ndvi(nir=data.NIR, red=data.RED))\
            .map(funcs.add_constant)\
            .map(funcs.add_time(omega=hcfg.omega))\
            .map(funcs.add_harmonics(
                freq=hcfg.harmonic_freq,
                cos_names=hcfg.cos_names,
                sin_names=hcfg.sin_names
            ))
        return instance
    
