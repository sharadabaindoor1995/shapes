# `shapes`

## Requirements Specification

A program is required that displays shapes in a canvas. The user will exploit a command line interface (CLI) to invoke
commands. There should be four types of commands:

* <ins>**draw**</ins> a particular shape optionally providing the shape parameters (size, location, stroke colour, fill
  colour) e.g.
  `prog draw [options]`
* <ins>**eval**</ins>uate properties of shapes e.g. `prog eval [options]`
* <ins>**save**</ins> shapes to a file with a particular format e.g. `prog save [options]`
* <ins>**read**</ins> shapes from a file e.g. `prog read [options]`

It should support the following shapes

* polygons (3, 4, 5, 6, ... sides)
* ellipsoids (ovals, circles, conic sections)
* points
* lines

In addition to the above it should allow <ins>display of text</ins> at any point of the canvas. Furthermore, it should be
able to
<ins>insert images</ins> at any point in the canvas.

## Decomposition

We cannot solve this problem all at once. We need to decompose it sensibly to make meaningful progress. Here is a
suggestion:

* shape representation
* canvas representation
* drawing shapes on the canvas
* shape serialisation and deserialisation into some format
* handling user commands

The above decomposition is not set in stone but is my first best guess at what will be needed to solve the problem. It
might later turn out that this decomposition is not satisfactory but we have to start somewhere.

## Shape Representation

Let's think of the user. What do we expect users to know?

* users are familiar with basic shapes e.g. circle, square, rectangle, triangle; we could start with the most basic
  shapes and work our way towards more complex shapes;
* each shape is defined by some parameterisation e.g. circles may be defined in terms of their radius or diameter;
  typically, there will be multiple parameterisations so we have to choose the most obvious and straightforward;
* parameterisations imply derived properties e.g. if a circle has a radius then it follows that it has an area and
  circumference;
* shapes may have visual properties such as fill and stroke

From the preceeding we can define the following interfaces:

```python
# define a circle
circle = Circle(radius=3.0, fill='red', stroke='black')
# compute some properties
circle.area
circle.circumference

# square
square = Square(width=3.0, fill='blue', stroke='#298374')
square.area
square.perimeter

# rectangle
rect = Rectangle(width=4.0, height=2.0, fill='#932093')  # default stroke
rect.area
rect.perimeter
rect.diagonal

```

## Canvas Representation

Now that we have some shapes, we need to think about where to place them. This will be some 2D plane. Again, we must
consult our imaginary user and ask what they know about canvases in order to sythesize some notion of a canvas.

* a canvas has dimensions: a width and height e.g. width=600, height=400
* the position at any point in the canvas is represented by a 2-tuple for which we need to specify an origin e.g. the
  origin is in the center
* the most natural coordinate systems is the cartesian plane with x increasing from left to right and y increasing from
  bottom to top; the point of intersection of the principal axes gives the origin

Again, let's write some pseudocode for this:

```python
from shapes.canvas import Canvas
canvas = Canvas(width=600, height=400, origin='center')
canvas.width
canvas.height
```

We would like to provide some handy behaviour to our canvas, which we will provide in the form of methods

```python
# display the axes
canvas.draw_axes()  # to display axes
# label axes
canvas.label_axes() # or it could be part of the `draw_axes()` method
# display ticks
canvas.draw_grid()
```

## Drawing Shapes on the Canvas

Now we come to the point when we can begin to see how our entities can interact. We want to draw shapes in the plane.
Once again, we want to meet the user where they are by presenting natural interfaces. Since our task is to draw the
shapes on the plane, we should mimic these semantics in the interaction i.e. the word 'draw' should feature somewhere in
this interaction. Here is one way we could do this.

```python
circle = Circle(radius=3.0, fill='red', stroke='black')
canvas = Canvas(width=600, height=400, origin='center')
canvas.draw(circle)
```

Something is missing! We need to specify where to draw the circle otherwise we should have a sensible default. Again, we
are doing everything we can to advance the user without having to force them to venture out of their comfort zone. So,
we could draw at the center by default while providing a warning about this.

```shell
~$ python shapes.py
warning: default location for shape 'circle' used; explicit location not provided
```

We have many options on how to specify location; we will only mention two:

* make location an attribute of the circle

```python
# during initialisation
circle = Circle(radius=3.0, fill='red', stroke='black', at=(60, 20))
# after initialisation
circle.location = (60, 20)
```

* alternatively, we could ask the user to provide this when drawing

```python
canvas.draw(cirle, at=(60, 20))
```

We have used the `at` keyword because it reads naturally.

## Shape Serialisation/Deserialisation

The words 'serialisation' and 'deserialisation' may sound big, but they are just fancy ways of describing how we capture
data and render it in a standard way. By standard way we typically refer to file formats or binary structures. We will
eschew the latter and pay attention to textual file formats.

One of the most widely used and legible textual file formats is YAML. You can find out more about YAML at https://yaml.org/. Here is an example of a serialisation of some
shapes in YAML.

```yaml
# shapes
- shapes:
    - circle:
        - radius: 3.0
        - fill: red
        - stroke: '#328023'
        - at: (60,20)
```

YAML is human-readable as well as machine friendly given its clear structure. Additionally, it is easily convertible to
JSON, another very popular format used predominantly in front-end web development. Here is the equivalent JSON converted
using https://www.json2yaml.com/:

```json
[
  {
    "shapes": [
      {
        "circle": [
          {
            "radius": 3.0
          },
          {
            "fill": "red"
          },
          {
            "stroke": "#328023"
          },
          {
            "at": "(60,20)"
          }
        ]
      }
    ]
  }
]
```

There is a very sane one-to-one relationship between JSON and Python dictionaries (the only exceptions are the `null`
for `None` swap and the string form of the tuple).

There are several reasons why we should prefer YAML over JSON:

* compact yet legible
* allows comments
* can host multiple documents in a single file

On the flip side, YAML does not yet have a Python standard library so you have to install `PyYAML` to work with it.

```shell
~$ pip install PyYAML
```

Deserialisation is the opposite - converting the standard form (e.g. YAML) into executable objects.

Again, thinking from the perspective of the user, we can perform serialisation using one of several ways:

* a `serialise()` method (though it is unlikely most users will know what this means);
* a simple `to_yaml()` method
* casting it to string e.g. `str(circle)` is perhaps the easiest way to do this since the user can do this in the
  process of writing to a file

```python
circle = Circle(...)
str(circle)
"""
# circle.yml
- circle:
    - radius: 3.0
    - fill: red
    - stroke: '#328023'
    - at: (60,20)
"""
```

In the opposite direction:

```python
circle = Circle.from_file('circle.yml')
```

We have covered all the parts of our decomposition. Let us now explore how we can realise this using Python. Remember, all we have done is simulate the user facing parts of the code. In effect, we are acting as if the code will appear on its own. This approach has been aptly described as *coding in the language of the domain* because the user environment provides the vocabulary by which the code is expressed. 

We can now loosely refer to the set of classes and the respective attributes and methods as our design. In summary, we have:
* the `Circle` class with attributes `radius`, `fill`, `stroke`, `location` and methods `from_file` as well its ability to be serialised to YAML;
* the `Canvas` class with attribues `width`, `height`, `origin` and `draw` method;

To realise this design we will take a tour of Python's object-oriented features. 

## Object-oriented Python
* defining classes
* defining class initialisation
* instantiating objects
* defining methods
* public vs. private attributes
* properties
* static methods
* decorators
* special methods
* operator overloading

## Applying Object-oriented Concepts
* actual drawing using turtle
* more shapes
* implementing serialisation/deserialisation
* displaying text
* inserting images

## Tools and Techniques
* CLIs
* modules/packages
* Unit testing
* Debugging

## What else is out there?

