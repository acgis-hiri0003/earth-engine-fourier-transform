import ee
import funcs
import harm
import inputs


def fourier_transform(time_series: inputs._BaseData, omega: float = 1.5, num_harmonics: int = 3) -> harm.HarmonicRegression:

    return 


class FourierTransform:
    
    def __init__(self, time_series: inputs._BaseData, omega: float = 1.5, modes: int = 3) -> None:
        self.ts = time_series
        self.omega = omega
        self.modes = modes
        self._ft = None
        self._sample = None
    
        
    def run(self) -> None:
        input_col = inputs.InputCollection(data=self.time_series)
        
        hcfg = harm.HarmonicCFG(
            omega=self.omega,
            harmonics=self.modes
        )

        harm_col = harm.HarmonicsCollection(
            config=hcfg,
            input_collection=input_col
        )
        
        self._ft = harm.HarmonicRegression(harm_col)

        return None
    
    def transformation(self) -> harm.HarmonicRegression:
        if self._ft is not None:
            return self._ft
        else:
            return None
    
    def sample(self, collection, on: str = 'fitted'):
        pass
    
    def plot(self, samples: ee.FeatureCollection = None):
        pass