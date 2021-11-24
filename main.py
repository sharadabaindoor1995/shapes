import sys
import os
from math import pi
import yaml
import turtle

turtle.tracer(False)


class Circle:
    def __init__(self, radius, fill='red', stroke='black', at=(0, 0)):
        self._radius = radius
        self._fill = fill
        self._stroke = stroke
        self._at = at

    @property
    def radius(self):
        return self._radius

    def draw(self, pen, *args, **kwargs):
        pen.up()
        pen.goto(self._at)
        pen.down()
        pen.circle(self._radius, *args, **kwargs)
        pen.up()

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
    def __init__(self, height, width, fill='red', stroke='black', at=(0, 0)):
        self._height = height
        self._width = width
        self._fill = fill
        self._stroke = stroke
        self._at = at

    def area(self):
        return self._width * self._height

    @property
    def left(self):
        return self._at[0] - self._width / 2

    @property
    def right(self):
        return self._at[0] + self._width / 2

    @property
    def top(self):
        return self._at[1] + self._height / 2

    @property
    def bottom(self):
        return self._at[1] - self._height / 2

    @property
    def vertices(self):
        """ Starting from top-left and going counter-clockwise"""
        return [
            (self.left, self.top),
            (self.left, self.bottom),
            (self.right, self.bottom),
            (self.right, self.top)
        ]

    def draw(self, pen, *args, **kwargs):
        pen.up()
        pen.goto(self.left, self.top)
        pen.down()
        pen.goto(self.left, self.bottom)
        pen.goto(self.right, self.bottom)
        pen.goto(self.right, self.top)
        pen.goto(self.left, self.top)
        pen.up()


class Canvas(turtle.TurtleScreen):
    def __init__(self, width, height, background_color='grey'):
        self._cv = turtle.getcanvas()
        super().__init__(self._cv)
        self.screensize(width, height, bg=background_color)
        self._width = width
        self._height = height
        self._pen = turtle.Turtle()
        self._pen.hideturtle()

    def draw_axes(self, pen):
        self._pen.up()
        self._pen.goto(-self._width / 2, 0)
        self._pen.down()
        self._pen.goto(self._width / 2, 0)
        self._pen.up()
        self._pen.goto(0, -self._height / 2)
        self._pen.down()
        self._pen.goto(0, self._height / 2)
        self._pen.up()
        self._pen.goto(self._width / 2, self._height / 2)

    def draw(self, shape):
        """Draw the given shape"""
        shape.draw(self._pen)

    def write(self, text, *args, **kwargs):
        text.write(self._pen, *args, **kwargs)


class Text:
    def __init__(self, text, at=(0, 0)):
        self._text = text
        self._at = at

    def write(self, pen, *args, **kwargs):
        pen.up()
        pen.goto(self._at)
        pen.down()
        pen.write(self._text, *args, **kwargs)
        pen.up()

def main():
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

    pen = turtle.Turtle()
    text = Text("This was written by turtle",at=(-50,50))
    # text.write(pen,font=("Arial", 30, "bold"))

    # circle = Circle(50)
    # circle.draw(pen)

    # quad = Quadrilateral(10, 10, at=(15, -5))
    # print(f"vertices={quad.vertices}")
    # quad.draw(pen)

    canvas = Canvas(1000, 700)
    #canvas.draw_axes(pen)
    #canvas.write(text)
    # canvas.write(text,align='center',font=('Arial',60,'bold'))
    gquad=Quadrilateral(200,300,fill='#009a44',stroke='white',at=(-200,0))
    wquad=Quadrilateral(200,300,fill='white',stroke='#dddddd',at=(0,0))
    oquad=Quadrilateral(200,300,fill='#ff8200',stroke='white',at=(200,0))
    canvas.draw(gquad)
    canvas.draw(wquad)
    canvas.draw(oquad)
    turtle.done()
    return 0


if __name__ == "__main__":
    sys.exit(main())
