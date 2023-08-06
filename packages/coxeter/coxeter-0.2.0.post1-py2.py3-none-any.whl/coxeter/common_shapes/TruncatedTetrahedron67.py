from numpy import sqrt
import numpy
from coxeter.shape_classes.convex_polyhedron import ConvexPolyhedron

points = [
    (0, -1, -sqrt(3 / 2) / 2),
    (0, 1, -sqrt(3 / 2) / 2),
    (-(1 / sqrt(3)), -1, 1 / (2 * sqrt(6))),
    (-(1 / sqrt(3)), 1, 1 / (2 * sqrt(6))),
    (-1 / (2 * sqrt(3)), -1 / 2, 5 / (2 * sqrt(6))),
    (-1 / (2 * sqrt(3)), 1 / 2, 5 / (2 * sqrt(6))),
    (1 / sqrt(3), 0, 5 / (2 * sqrt(6))),
    (2 / sqrt(3), 0, 1 / (2 * sqrt(6))),
    (-sqrt(3) / 2, -1 / 2, -sqrt(3 / 2) / 2),
    (-sqrt(3) / 2, 1 / 2, -sqrt(3 / 2) / 2),
    (sqrt(3) / 2, -1 / 2, -sqrt(3 / 2) / 2),
    (sqrt(3) / 2, 1 / 2, -sqrt(3 / 2) / 2),
]

shape = ConvexPolyhedron(numpy.array(points))
