[![Documentation Status](https://readthedocs.org/projects/galaxie-curses/badge/?version=latest)](http://galaxie-curses.readthedocs.io/?badge=latest)
[![pipeline status](https://gitlab.com/Tuuux/galaxie-curses/badges/master/pipeline.svg)](https://gitlab.com/Tuuux/galaxie-curses/-/commits/master)
[![coverage report](https://gitlab.com/Tuuux/galaxie-curses/badges/master/coverage.svg)](https://gitlab.com/Tuuux/galaxie-curses/-/commits/master)
[![codecov](https://codecov.io/gl/Tuuux/galaxie-curses/branch/master/graph/badge.svg)](https://codecov.io/gl/Tuuux/galaxie-curses)

Galaxie Curses, The ToolKit
===========================
<div style="text-align:center"><img src ="https://gitlab.com/Tuuux/galaxie-curses/raw/master/docs/source/images/logo_galaxie.png" /></div>

Once upon a time, this project was hosted on a ancient platform called GitHub. Then came the Buyer.
The Buyer bought GitHub, willing to rule over its community.

I was not to sell, so here is the new home of "https://github.com/Tuuux/galaxie-curses".

The Project
-----------
**Galaxie Curses** alias **Le Truc Blue** (The Blue Thing) is a free software Tool Kit for the **NCurses** API.
It can be consider as a text based implementation of the famous **GTK+** Library (Or Ultra Inspired...).

Where ``implementation`` mean: ``Devellop a project from a documentation specs``.

Originally the project have start in 2016 when the author Jérôme.O have start to learn **Python** at home.

Then the lib is write in **Python**

Installation
------------

**Pre Version**: ```pip install galaxie-curses```<BR>
**Dev Version**: ```pip install -i https://test.pypi.org/simple/ galaxie-curses```

Documentation:
-------------
* **API:** https://galaxie-curses.readthedocs.io/GLXCurses.html
* **Readthedocs link:** http://galaxie-curses.readthedocs.io


The Mission
-----------
Provide a Text Based ToolKit with powerfull high level Widget (Select Color, Printer Dialog, FileSelector).

During lot of years the main stream was to provide big computer with big GUI Toolkit,
unfortunately almost nobody have care about ultra low profile computer and we are now in a situation where no mature
ToolKit is ready to use on **pen computer**. Time's change then it's time to change the world ...

The goal of the version 1.0 will be to create a application like Midnight-Commander with **GLXCurses**.

Midnight-Commander: https://midnight-commander.org

The Lib should have no dependency , then consider Applications will come with they own dependency.

Contribute
----------
You welcome !!!

The **GTK+ v3** documentation is our model: https://developer.gnome.org/gtk3/stable/

- Issue Tracker: https://gitlab.com/Tuuux/galaxie-curses/issues
- Source Code: https://gitlab.com/Tuuux/galaxie-curses

It's almost impossible to code widget without UnitTest, that because eyes can't easily control background operations.

Screenshots
-----------
v0.3rc1
<p align="center">
<img src="https://gitlab.com/Tuuux/galaxie-curses/raw/master/docs/source/images/screen_02.png">
</p>

v0.2
<p align="center">
<img src="https://gitlab.com/Tuuux/galaxie-curses/raw/master/docs/source/images/screen_01.png">
</p>

Example
-------
 v0.2
```python
#!/usr/bin/env python
import GLXCurses

if __name__ == '__main__':

    # Create the main Application
    app = GLXCurses.Application()

    # Create a Label
    label = GLXCurses.Label()
    label.text = 'Hello World !!!'

    # Create the main Window and add our Label inside
    win = GLXCurses.Window()
    win.add(label)

    def handle_keys(self, event_signal, *event_args):
        if event_args[0] == ord('q'):
            # Everything have a end, the main loop too ...
            # Control + C work automatically
            GLXCurses.MainLoop().quit()

    # Add Everything inside the Application
    app.add_window(win)

    # Connect the application to Curses event
    app.connect('CURSES', handle_keys)

    # Main loop start
    GLXCurses.MainLoop().run()

```
More examples can be found here: https://gitlab.com/Tuuux/galaxie-curses/tree/master/examples

Features
--------
* MainLoop
* Signal
* Application Class
* Component like Button, Container, ProgressBar
* Have GTK+ design as roadmap
* Auto Rezize
* Minimize NCurses crash
* Common thing for a text based graphic interface tool kit :)

Roadmap
-------
**Galaxie-Curses** is a Text Based **GTK+** like, then the GTK+ Doc is the **roadmap**.

Yes NCurses haven't icons or pixel management :) , then chars replace pixel. Each sizes x, y , height, width are in chars value.

* 100% Test Code Coverage
* Add Image Widget
* Add Video Widget
* Ultra Low Power usage.
* Widget over SSH
* ZeroMQ integration
* Audio
* Data to Audio file for backup or long distance radio
* Build Application via YAML file (it have been report about a low TUI must have light programation style)
* Every Examples should be a small and efficient Desktop component, Calc, Config Panel, File Explorer, Panel, etc ...
* Widget capability to save information's
* Look like MC similar to GTK code

Note that actually a Curses Window Manager is not on the pipe. Everything is ready for ...

How that possible
-----------------
I don't know if one day i'll finish the lib. I do my best for that.

Unfortunately GLXCurses is not a GTK Clone it will take too mush time for one guy to make it possible.
For minimize the effort i implement ``property`` and ``Widget`` class with the same GTK+ design.

I consider haven't the enginier level to create a UI design by my self, then i have choose GTK Documentation as specs.

GTK Method's are implemented only if that really require.
The lib use massively properties getter and setter decorator, for limit the need of method. 

For be brief it take advantage of Python object where GTK use GLIBC and method's for make the same thing.

If a method is implemented, then it's a pure GTK+ implementation else the lib use a property in pure Python style.

Exemple:

```python
widget = Widget.new()
widget.set_decorated(True)
```
is replace by
```python
widget = Widget()
widget.decorated = True
```

I focus my effort to have capability to make MC clone with GLXCurses, and limit my effort to that direction. (yes i would like more too ...)





Note for GTK+ Project Developer's
---------------------------------
I'm really confuse about the big copy/past i making from the **GTK+** documentation during the creation of
the **Galaxie-Curse** documentation, that because english is not my primary language and i'm a bit limited for make a
ToolKit documentation without that ...
Consider that actual documentation of **Galaxie-Curse** as the better i can do and it
include to copy/past large parts of the **GTK+** documentation. (sorry about that)

As you probably see **Galaxie-Curses** is a Text Based **GTK+** with a hard dependency to the **GTK+** documentation.

Thanks
------
To everyone i have interrest to it project, copy it, use it, diffuse it , and have fun ...

All **Galaxie** API is develop with **pycharm** as IDE from **JetBrains** 
link: https://www.jetbrains.com

JetBrains graciously have provide to us licenses for **pycharm profesional**

License
-------
GNU GENERAL PUBLIC LICENSE Version 3
https://gitlab.com/Tuuux/galaxie-curses/blob/master/LICENSE