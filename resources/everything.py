import importlib
import os
import secrets
import sys
import turtle

import yaml
from PIL import Image as PILImage

turtle.tracer(False)


class Canvas(turtle.TurtleScreen):
    def __init__(self, width, height, bg='#ffffff'):
        self._cv = turtle.getcanvas()
        super().__init__(self._cv)
        self.screensize(width, height, bg=bg)
        self._width = width
        self._height = height
        self._pen = turtle.Turtle()
        self._pen.hideturtle()
        # self._pen.speed(0)
        # self.bgpic('funny.gif')
        # self.onclick(self._report)

    def draw_axes(self):
        # self._pen.speed(0)
        self._pen.up()
        self._pen.goto(0, self._height / 2)
        self._pen.down()
        self._pen.goto(0, -self._height / 2)
        self._pen.up()
        self._pen.goto(-self._width / 2, 0)
        self._pen.down()
        self._pen.goto(self._width / 2, 0)
        self._pen.up()
        self._pen.goto(-self._width / 2, -self._height / 2)

    def draw_grid(self, colour='#dddddd', hstep=50, vstep=50):
        # self._pen.speed(0)
        original_pen_colour = self._pen.pencolor()
        self._pen.color(colour)
        # vertical grids
        self._pen.up()
        for hpos in range(-500, 500 + hstep, hstep):
            self._pen.goto(hpos, 350)
            self._pen.down()
            self._pen.goto(hpos, -350)
            self._pen.up()
        # horizontal grids
        for vpos in range(-350, 350 + vstep, vstep):
            self._pen.goto(-500, vpos)
            self._pen.down()
            self._pen.goto(500, vpos)
            self._pen.up()
        # reset
        self._pen.pencolor(original_pen_colour)

    @property
    def pen(self):
        return self._pen

    def paint(self, image):
        self.pen.up()
        image.paint(self)
        self.pen.down()

    def draw(self, shape):
        """Draw the given shape"""
        shape.draw(self._pen)

    def write(self, text, *args, **kwargs):
        text.write(self._pen, *args, **kwargs)

    # def _report(self, arg1, arg2):
    #     print(f"something {arg1 = } and {arg2 = }")
    #     circle = Circle(20, at=(arg1, arg2))
    #     self.draw(circle)


class Image:
    def __init__(
            self, fp, mode='r', formats=None, at=(0, 0)
    ):
        self._image = PILImage.open(fp, mode, formats=formats)
        print(f"{self._image.format = }")
        print(f"{self._image.filename = }")
        self._at = at

    @property
    def name(self):
        """Guarantees we get a name"""
        if self._image.format == 'GIF':
            return self._image.filename
        return self._gif_name

    def __enter__(self):
        """create the gif if not a gif"""
        if self._image.format != 'GIF':
            self._gif_name = f"{secrets.token_urlsafe(4)}.gif"
            print(f"temporarily saving as {self._gif_name}...")
            # write a temporary GIF file
            self._image.save(self._gif_name)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """delete the gif if not a gif"""
        if hasattr(self, '_gif_name'):
            os.remove(self._gif_name)

    def paint(self, canvas):
        canvas.bgpic(self.name)
        canvas.pen.goto(*self._at)
        canvas._cv.itemconfig(canvas._bgpic, anchor="sw")  # pylint: disable=W0212


class Circle:
    shape = 'circle'

    def __init__(self, radius, fill='#ffffff', stroke='#000000', at=(0, 0)):
        self._radius = radius
        self._fill = fill
        self._stroke = stroke
        self._at = at

    def draw(self, pen):
        """Draw a circle"""
        if pen.isdown():
            pen.up()
        pen.goto(*self._at)
        pen.down()
        pen.begin_fill()
        pen.pencolor(self._stroke)
        pen.fillcolor(self._fill)
        pen.circle(self._radius)
        pen.end_fill()
        pen.up()

    @property
    def yaml(self):
        return {
            self.shape: {
                'radius': self._radius,
                'fill': self._fill,
                'stroke': self._stroke,
                'at': self._at
            }
        }

    @classmethod
    def from_string(cls, string):
        print(f"{string = }")
        d = yaml.load(string, Loader=yaml.Loader)['circle']
        print(d)
        return cls(d['radius'], fill=d['fill'], stroke=d['stroke'], at=d['at'])

    def __str__(self):
        """Serialise to YAML

        circle:
            radius: 3.0
            fill: red
            stroke: '#328023'
            at: (60,20)
        """
        return yaml.dump(self.yaml, default_flow_style=False, canonical=False)

    def __repr__(self):
        """the representational string"""
        return f"{self.__class__.__qualname__}({self._radius}, fill='{self._fill}, stroke='{self._stroke}', at={self._at})"


class Quadrilateral:
    shape = 'quadrilateral'

    def __init__(self, width, height, fill='red', stroke='#000000', at=(0, 0)):
        self._width = width
        self._height = height
        self._fill = fill
        self._stroke = stroke
        self._at = at

    def draw(self, pen):
        fg, bg = pen.color()
        pen.pencolor(self._stroke)
        pen.fillcolor(self._fill)
        pen.begin_fill()
        pen.up()
        for vertex in self.vertices + [self.vertices[0]]:
            pen.goto(*vertex)
            pen.down()
        pen.end_fill()
        # reset
        pen.up()
        pen.color(fg, bg)

    @property
    def vertices(self):
        return [
            (self.xpos - self._width / 2, self.ypos + self._height / 2),
            (self.xpos + self._width / 2, self.ypos + self._height / 2),
            (self.xpos + self._width / 2, self.ypos - self._height / 2),
            (self.xpos - self._width / 2, self.ypos - self._height / 2),
        ]

    @property
    def xpos(self):
        return self._at[0]

    @property
    def ypos(self):
        return self._at[1]


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
    print(sys.argv)
    if sys.argv[1] == 'draw':
        importlib.import_module(sys.argv[2], package='..drawings')

    turtle.done()
    return os.EX_OK


if __name__ == "__main__":
    sys.exit(main())
