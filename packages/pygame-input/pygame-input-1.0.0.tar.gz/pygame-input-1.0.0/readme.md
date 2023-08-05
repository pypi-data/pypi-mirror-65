
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![](https://img.shields.io/badge/build%20system-poetry-ff69b5)](https://python-poetry.org/)
[![Pypi Version](https://img.shields.io/pypi/v/pygame-input.svg)](https://pypi.python.org/pypi/PygameGUILib)
[![Python Version](https://img.shields.io/pypi/pyversions/pygame-input.svg)](https://pypi.python.org/pypi/PygameGUILib)
[![Pypi Downloads](https://img.shields.io/pypi/dm/pygame-input.svg)](https://pypi.python.org/pypi/pygame-input)

pygame-input
========

`pygame-input` will simplify your input handling with pygame
by providing a simple way to assign callbacks to given key press
or joystick events.

Look how easy it is to use:

```python
import pygame
from pygame_input import Inputs, Button, JoyButton

inputs = Inputs()
inputs["fire"] = Button(pygame.K_SPACE, JoyButton(1))
inputs["fire"].on_press_repeated(player.fire, delay=0.1)
```

This will call your `player.fire()` function every 0.1 seconds while 
any button, whether it is the space bar or the button one on your
joystick is pressed.
    
Features
--------

- Joystick
- Boolean input values (ie. *is key pressed ?*) 
    and scalar input values (ie. *how much is the stick on the left ?*)
- Register callbacks on:
    - press,
    - release,
    - double-press 
    - or all the time
- Every function and class has a detailed docstring
    
What `pygame-input` is not (yet ?):
 - handling key modifiers
 - handling mouse input
 - recognising mouse gestures
 - doing gamepad configuration 
    (ie. you need to know which id is the "A" button)
    
Though the first two will probably be implemented quite
soon, depending on when I need them.

Installation
------------

Install `pygame-input` by running::

    pip install pygame-input

Alternativelly you can just copy `pygame_input.py` into your
game folder as the whole code is just one file. Feel free to
modify it as much as you need.

Usage
-----

#### Defining the inputs
The first step to be able to to register callbacks 
is to create an `Inputs` object, which is bacically a 
python's `dict` with a `trigger` method. We will 
come back on `trigger` later. So:

```python
from pygame_input import *
inputs = Inputs()
```
    
Then you can add all the input types in dictionary.
There are two input types: `Button` and `Axis`.

A `Button` represents anything that is either
pressed or released, like a key on your keyboard or 
a button of your joystick.

An `Axis` is for anything that takes a value between -1 and 1,
for instance, the position of a joystick, but a pair of 
keys can also be seen as an axis: if we consider the pair of 
left and right arrows, the axis would have value -1 if the left key
is pressed, 1 if it is the right and 0 if none or both are pressed. 
This is very convenient for moving a player.

Enough talking, let's add a `Button` to our `inputs`.

```python
inputs["fire"] = Button(pygame.K_SPACE, pygame.K_RETURN)
```

The `Button` takes every posible way to press it as parameters.
Here we want to trigger the fire input when we press either 
the space bar or return. Any pygame key code is a valid argument
but if we also want joystick support 

```python
inputs["fire"] = Button(pygame.K_SPACE, pygame.K_RETURN, JoyButton(1))
```
It would also trigger if the button 1 on joystick 0 is pressed. 
Note that you need to [initialise the joysticks](https://www.pygame.org/docs/ref/joystick.html) 
yourself. If you want to fire only when the button 1 on the 3rd joystick
is pressed, you would pass `JoyButton(1, 3)` instead.
 
Other parameters for buttons can be:
 - `QuitEvent()` that matches the `pygame.QUIT` event.
 - `JoyAxisTrigger(axis, threshold=0.5, above=True, joy_id=0)`
  that matches when an axis has a value above `threshold` 
  (or below if `above=False`)
  
We will also add an `Axis` so our player can move horizontally.

```python
import pygame
from pygame_input import Axis
inputs["hmove"] = Axis(
    (pygame.K_LEFT, pygame.K_a), 
    (pygame.K_RIGHT, pygame.K_d),
    JoyAxis(1),
)
```

What did you do here ? The two first arguments of `Axis`
are the negative and positive keys. Negative keys corresponds to a value
of -1 (think: left/down) and positive to a value of +1 (think: right/up).
It accepts a single key code or a list of key codes.

After that, can follow any number of `JoyAxis` that correspond 
to an axis on the joystick. The signature of `JoyAxis` is more complex
but quite explicit :

```python
@dataclass(frozen=True)
class JoyAxis:
    axis: int
    reversed: bool = False
    """Whether the positive and negative should be reversed."""
    threshold: float = 0.2
    """Any value of smaller magnitude will be considered as zero."""
    sensibility: float = 1.0
    """Multiply the value by this amount. Useful if a joystick doesn't go all the way to +/-1"""
    joy_id: int = 0
    """The id used to initialise the joystick."""
```

If you don't know about dataclasses, don't worry and consider that 
the attributes defined here are the parameters of `JoyAxis()`. Though
feel free to check [what dataclasses are](https://realpython.com/python-data-classes/),
because they're nice :)

#### Adding callbacks

Now that you know everything about defining the inputs, 
we can add callbacks to them. Those two steps are different, 
because they can happen at different places in the code. 
For instance inputs definition can be in the main in on a settings screen.
You may also want to add callbacks during the player creation
and also register a callback on the camera when the player moves.

Enough theory. There are 5 ways to add a callback `f` to a `Button`:
 - `always_call(f)`:
 - `on_press(f)`
 - `on_release(f)`
 - `on_double_press(f)`
 - `on_press_repeated(f, delay)`
 
Their names are self explanatory. `on_press_repeated` 
accepts a `delay` argument: the callback will be called every `delay` seconds.

**Each callback is always called with one argument: 
the `Button` or `Axis` that triggered it.** 
This way you can access the axis `value` or the button's `press_time`.

For an `Axis` there only `always_call(f)` is available, since the others
don't make sense. Example:

```python
inputs["fire"].on_press_repeated(player.fire, delay=0.5)
inputs["hmove"].allways_call(player.horizontal_move)
```

#### Triggering callbacks

To trigger the callbacks the only thing that is needed is 
to call `inputs.trigger` with a list of the events 
that happened since last frame.

```python
while True:
    # Event handling
    inputs.trigger(pygame.events.get())

    # Game logic
    ...

    # Draw everything
    ...

    pygame.display.update()
```

**Note**: if you also need to process the events in a different way,
you need to convert `pygame.events.get()` to a list first and use the list:

```python
events = list(pygame.events.get())
inputs.trigger(events)
for event in events:
    if event.type == ...:
        ...
```

For more, see the [examples](examples).

Contribute
----------

- Issue Tracker: https://gitlab.com/ddorn/pygame-input/issues
- Source Code: https://gitlab.com/ddorn/pygame-input

Support
-------

If you are having issues, please let me know.
You can open an issue or send me a mail, 
my email address is on my gitlab profile.
 
License
-------

The project is licensed under the MIT license.