"""
A test for module `transformations` that contains tools for manipulating affine
transformations of real plane.
"""
import numpy as np

# module `transformations` contains class `Transformation` and its children `Scaling`, `Translation`, `Rotation`
from homework.transformations import Transformation, Scaling, Translation, Rotation

# `Scaling` is a child of `Transformation`
scaling = Scaling(scale=3)
assert isinstance(scaling, Transformation)

# `scaling` acts on a point by multiplying its coordinates by the given scale x, y = p = [1, 2]
assert np.allclose(scaling(p), [3 * x, 3 * y])

# `Translation` is also a child of `Transformation`
translation = Translation(shift=[1, 2])
assert isinstance(translation, Transformation)

# `translation` acts on a point by shifting that point by given `shift`
assert np.allclose(translation(p), [x+1, y+2])

# `Rotation` is also a child of `Transformation`
rotation = Rotation(angle=np.pi / 3)
assert isinstance(rotation, Transformation)

# `rotation` acts on a point by rotation by given `angle` around the origin
assert np.allclose(rotation([1, 0]), [1/2, 3**(1/2) / 2])

# We can compose any transformations
composed = scaling @ translation
assert np.allclose(composed(p), scaling(translation(p)))

# A transformation has an attribute `matrix` that returns the corresponding affine matrix of shape `[3, 3]`
assert np.allclose(
    composed.matrix,
    np.array([[3., 0., 3.],
              [0., 3., 6.],
              [0., 0., 1.]])
)
# However the `matrix` attribute is not writeable: try:
try:
    composed.matrix = np.eye(3)
except Exception:
    pass # the code has raised an exception as expected else:
else:
    raise Exception("The code should have raised an exception but it did not!")

# transformations can be used as context managers using special function `transform` as in the following example
from homework.transformations import transform

with composed:
    p1 = transform(p)
assert np.allclose(p1, composed(p))

# the transformation-contexts can be nested as follows
with translation:
    p1 = transform(p)
    with scaling:
        p2 = transform(p)
        with rotation:
            p3 = transform(p)
    p4 = transform(p)

assert np.allclose(p1, translation(p))
assert np.allclose(p2, (scaling @ translation)(p))
assert np.allclose(p3, (rotation @ scaling @ translation)(p))
assert np.allclose(p4, translation(p))
