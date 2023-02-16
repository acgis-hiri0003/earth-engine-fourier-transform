import math

from typing import List, Callable

import ee


def add_harmonics(freq: List[int], cos_names: List[str], sin_names: List[str]) -> Callable:    
    def add_harmonics_wrapper(element: ee.Image):
        frequencies = ee.Image.constant(freq)
        time = ee.Image(element).select('t')
        cosines = time.multiply(frequencies).cos().rename(cos_names)
        sines = time.multiply(frequencies).sin().rename(sin_names)
        return element.addBands(cosines).addBands(sines)
    return add_harmonics_wrapper


def add_ndvi(nir: str, red: str) -> Callable:
    def add_ndvi_wrapper(element: ee.Image):
        return element.addBands(element.normalizedDifference([nir, red]).rename('NDVI'))
    return add_ndvi_wrapper


def add_constant(element: ee.Image):
    return element.addBands(ee.Image(1))


def add_time(omega: float = 1.5) -> Callable:
        def add_time_inner(image: ee.Image):
            date = image.date()
            years = date.difference(ee.Date('1970-01-01'), 'year')
            time_radians = ee.Image(years.multiply(2 * omega * math.pi))
            return image.addBands(time_radians.rename('t').float())
        return add_time_inner


def new_collection_to_image(collection: ee.ImageCollection) -> ee.Image:
    stack = ee.Image(collection.iterate(lambda img, prev: ee.Image(prev).addBands(img), ee.Image(1)))
    stack = stack.select(ee.List.sequence(1, stack.bandNames().size().subtract(1)))
    return stack


def create_time_band(element: ee.Image) -> ee.Image:
    date = element.date().format('YYYY-MM-dd')
    return element.set('date', date).rename(date)


def add_phase_image(mode: int) -> Callable:
    sin, cos = f'sin_{mode}', f'cos_{mode}'
    def wrapper(element: ee.Image):
        return element.select(sin).atan2(element.select(cos))\
            .unitScale(-math.pi, math.pi)
    return wrapper


def add_amplitude_image(mode: int) -> Callable:
    sin, cos = f'sin_{mode}', f'cos_{mode}'
    def wrapper(element: ee.Image):
        return element.select(sin).hypot(element.select(cos))
    return wrapper