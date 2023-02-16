import harm
import inputs


def fourier_transform(data: inputs._BaseData, omega: float = 1.5, num_harmonics: int = 3) -> harm.HarmonicRegression:
    input_col = inputs.InputCollection(data=data)
    hcfg = harm.HarmonicCFG(
        omega=omega,
        harmonics=num_harmonics
    )

    harm_col = harm.HarmonicsCollection(
        config=hcfg,
        input_collection=input_col
    )
    
    return harm.HarmonicRegression(harm_col)
