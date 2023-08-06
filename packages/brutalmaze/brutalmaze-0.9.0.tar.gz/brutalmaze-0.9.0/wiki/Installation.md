## Python and pip

Brutal Maze should run on any recent Python (2 or 3) version. If you're using
an Unix-like operating system, you're likely to have Python installed on your
computer. Otherwise, you can download it from [python.org](https://www.python.org/downloads/).

This game also uses [appdirs](https://pypi.org/project/appdirs/) and
[Pygame](https://pypi.org/project/Pygame/) libraries, which is recommended to
be installed using `pip`. There is a detailed documentation about getting this
package manager on [pypa.io](https://pip.pypa.io/en/latest/installing/).

**Note:** When you follow either of the instruction below, `pip` will
automatically install appdirs and Pygame as dependencies.

## Install from PyPI

For convenience reasons, every release of Brutal Maze is uploaded to the Python
Package Index. To either install or upgrade, open your terminal (on Windows:
Command Prompt or PowerShell) and run:

    pip install brutalmaze --upgrade

You might need to use `sudo` on Unix-like systems, or add the flag `--user` to
the command to use [the user scheme](https://docs.python.org/2/install/index.html#alternate-installation-the-user-scheme).
The later would require [Python scripts directory](https://docs.python.org/3/install/index.html#alternate-installation-the-user-scheme)
to be in your environmental variable `$PATH`.

## Install from Github

If you want to tweak the game or contribute, clone the Github repository:

    git clone https://github.com/McSinyx/brutalmaze.git --recursive

This will also clone the `wiki` submodules containing, well, ehm, this Wiki.

Then install it using `pip` with the `--editable` flag, like so:

    pip install --user -e ./brutalmaze

If you want to link Brutal Maze to another versions of dependencies, you will
need to install directly using `setup.py`, which additionally requires
[setuptools](https://pypi.org/project/setuptools/):

    python setup.py install --user

This is especially useful when you needs to link the game to a better updated
version of SDL (SDL 1.2 was deprecated in 2012 but it still receives downstream
patches). Simply install Pygame from your distribution's repository and the
package manager will resolve dependencies for you; or [compile the library from
source](https://www.pygame.org/wiki/Compilation). Note that Brutal Maze is
fully compatible with Pygame SDL2 port (not to be confused with
[renpy/pygame\_sdl2](https://github.com/renpy/pygame_sdl2)) which have
significantly improved performance, so if possible, try to compile Pygame with
SDL2.
