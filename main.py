import sys
import os
from math import pi
import yaml


class Circle:
    def __init__(self, radius, fill='red', stroke='black', at=(0, 0)):
        self._radius = radius
        self._fill = fill
        self._stroke = stroke
        self._at = at

    @property
    def radius(self):
        return self._radius

    def calculate_area(self):
        """Calculates the area"""
        return pi * self._radius ** 2

    def __len__(self):
        return int(2 * pi * self.radius)

    def __str__(self):
        string = yaml.dump({
            'circle': {
                'radius': self._radius,
                'fill': self._fill,
                'stroke': self._stroke,
                'at': self._at
            }
        })
        return string

    def __repr__(self):
        return f"Circle({self._radius},fill={self._fill})"

    @classmethod
    def from_yaml(cls, string):
        """ Create a circle from a YAML string"""
        circle_dict = yaml.load(string, Loader=yaml.Loader)['circle']
        print(circle_dict)
        obj = cls(circle_dict['radius'], fill=circle_dict['fill'], stroke=circle_dict['stroke'], at=circle_dict['at'])
        return obj


class Quadrilateral:
    def __init__(self, height, width, fill='red', stroke='black'):
        self._height = height
        self._width = width
        self._fill = fill
        self._stroke = stroke

    def area(self):
        return self._width * self._height


class Canvas:
    def __init__(self, width, height, background_color='grey'):
        self._width = width
        self._height = height
        self._backgroundColor = background_color


class Text:
    def __init__(self, text, color='black', size=20, font='Arial'):
        self._text = text
        self._color = color
        self._size = size
        self._font = font


def main():
    circle = Circle(5.0, fill='blue', stroke='white')
    print(f"area = {circle.calculate_area()}")
    print(circle.radius)
    print(f"circumference is {len(circle)}")
    print(str(circle))
    print(repr(circle))

    my_yaml = str(circle)
    print(my_yaml)

    yaml_circle = """\
circle:
  radius: 5.0
  at: !!python/tuple
  - 0
  - 0
  fill: blue
  stroke: white
"""
    my_circle = Circle.from_yaml(yaml_circle)
    return 0


if __name__ == "__main__":
    sys.exit(main())
