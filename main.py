import sys
import os
from math import pi

class Circle:
    def __init__(self, radius, fill='red', stroke='black'):
        self._radius=radius
        self._fill=fill
        self._stroke=stroke

    @property
    def radius(self):
        return self._radius

    def calculate_area(self):
        """Calculates the area"""
        return pi * self._radius ** 2

    def __len__(self):
        return int(2*pi*self.radius)

def main():
    circle=Circle(5.0, fill='blue', stroke='white')
    print(f"area = {circle.calculate_area()}")
    print(circle.radius)
    print(f"circumference is {len(circle)}")
    return 0

if __name__ == "__main__":
    sys.exit(main())