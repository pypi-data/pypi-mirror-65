Brutal Maze provides a INET (i.e. IPv4), STREAM (i.e. TCP) socket server which
can be enabled in the config file or by adding the `--server` CLI flag. After
binding to the given host and port, it will wait for a client to connect. Then,
in each cycle of the loop, the server will send current details of each object
(hero, walls, enemies and bullets), wait for the client to process the data and
return instruction for the hero to follow. Since there is no EOT (End of
Transfer) on a socket, messages sent and received between server and client
must must be strictly formatted as explained below.

## Server output

First, the game will export its data to a byte sequence (which in this case, is
simply a ASCII string without null-termination) of the length *l*. Before
sending the data to the client, the server would send the number *l* padded to
7 digits.

Below is the meta structure of the data:

```
<Map height (nh)> <Number of enemies (ne)> <Number of bullets (nb)> <Score>
<nh lines describing visible part of the maze>
<One line describing the hero>
<ne lines describing ne enemies>
<nb lines describing nb bullets>
```

### The maze

Visible parts of the maze with the width *nw* and the height *nh* are exported
as a byte map of *nh* lines and *nw* columns. Any character other than `0`
represents a blocking *cell*, i.e. a wall.

To avoid floating point number in later description of other objects, each
cell has the width (and height) of 100, which means the top left corner of
the top left cell has the coordinates of (0, 0) and the bottom right vertex of
the bottom right cell has the coordinates of (*nw*\*100, *nh*\*100).

### The hero

6 properties of the hero are exported in one line, separated by 1 space, in the
following order:

* **Hero's color** indicating the current HP of the hero, as shown in in the
  later section.
* **X-coordinate**, which will be in the range \[0, *nw* \* 100\], cast to an
  integer.
* **Y-coordinate**, which will be in the range \[0, *nh* \* 100\], cast to an
  integer. Note that the y-axis points up-side-down instead of pointing upward.
* **Angle** of the direction the hero is pointing to in degrees, cast to a
  nonnegative integer (from 0 to 360). Same note as above (the unit circle
  figure might help you understand this easier). 
* **Flag showing if the hero can strike an attack**, `0` for *no* and `1` for
  *yes*.
* **Flag showing if the hero can heal**, `0` for *no* and `1` for *yes*.

![Unit circle](pics/unitCircleDegrees.png)

### The enemies

Each enemy exports these properties:

* **Color** indicating the type and current HP of the enemy, as shown in the
  table below.
* **X-coordinate**, which will be in the range \[0, *nw* \* 100\], cast to an
  integer.
* **Y-coordinate**, which will be in the range \[0, *nh* \* 100\], cast to an
  integer.
* **Angle of the direction the hero is pointing to** in degrees, cast to a
  nonnegative integer (from 0 to 360).

To shorten the data, each color (in the Tango palette) is encoded to a
lowercase letter or number `0`. Different shades of a same color indicating
different HP of the characters.

|     HP      |           5           |           4           |           3           |           2           |           1           |           0           |
| ----------- | --------------------- | --------------------- | --------------------- | --------------------- | --------------------- | --------------------- |
| Butter      |                       |                       | ![a](pics/fce94f.png) | ![b](pics/edd400.png) | ![c](pics/c4a000.png) | ![0](pics/2e3436.png) |
| Orange      |                       |                       | ![d](pics/fcaf3e.png) | ![e](pics/f57900.png) | ![f](pics/ce5c00.png) | ![0](pics/2e3436.png) |
| Chocolate   |                       |                       | ![h](pics/e9b96e.png) | ![i](pics/c17d11.png) | ![j](pics/8f5902.png) | ![0](pics/2e3436.png) |
| Chameleon   |                       |                       | ![j](pics/8ae234.png) | ![k](pics/73d216.png) | ![l](pics/4e9a06.png) | ![0](pics/2e3436.png) |
| Sky Blue    |                       |                       | ![m](pics/729fcf.png) | ![n](pics/3465a4.png) | ![o](pics/204a87.png) | ![0](pics/2e3436.png) |
| Plum        |                       |                       | ![p](pics/ad7f8a.png) | ![q](pics/75507b.png) | ![r](pics/5c3566.png) | ![0](pics/2e3436.png) |
| Scarlet Red |                       |                       | ![s](pics/ef2929.png) | ![t](pics/cc0000.png) | ![u](pics/a40000.png) | ![0](pics/2e3436.png) |
| Aluminium   | ![v](pics/eeeeec.png) | ![w](pics/d3d7cf.png) | ![x](pics/babdb6.png) | ![y](pics/888a85.png) | ![z](pics/555753.png) | ![0](pics/2e3436.png) |

### Flying bullets

Bullets also export 4 properties like enemies:

* **Color** indicating the type and potential damage of the bullet (from 0.0 to
  1.0), encoded similarly to characters', except that Aluminium bullets only
  have 4 colors `v`, `w`, `x` and `0`.
* **X-coordinate**, which will be in the range \[0, *nw* \* 100\], cast to an
  integer.
* **Y-coordinate**, which will be in the range \[0, *nh* \* 100\], cast to an
  integer.
* **Angle of the bullet's flying direction** in degrees, cast to a
  nonnegative integer (from 0 to 360).

### Example

![Screenshot](https://raw.githubusercontent.com/McSinyx/brutalmaze/master/screenshot.png)

Above snapshot of the game is exported as:

    19 5 3 180
    00000000000000000vvvv0000
    v0000000000000000vvvv0000
    v0000000000000000vvvv0000
    v0000000000000000vvvv0000
    vvvvvvvvvvvvvvvvvvvvv0000
    vvvvvvvvvvvvvvvvvvvvv000v
    vvvvvvvvvvvvvvvvvvvvv000v
    vvvvvvvvvvvvvvvvvvvv00000
    0000000000000000000000000
    0000000000000000000000000
    0000000000000000000000000
    v000000000000000000000000
    v000000000000000000000000
    v000000000000000000000000
    v000vvvvvvv000vvv0vvv0000
    v000vvvvvvv000vvvvvvv0000
    v000vvvvvvv000vvvvvvv0000
    v000vvvvvvv000vvvvvvv0000
    v000000vvvv000000vvvv0000
    v 1267 975 47 0 1
    p 1817 1050 45
    g 1550 1217 45
    a 2250 1194 45
    p 2050 1017 45
    e 1850 950 358
    x 2126 1189 361
    e 1541 1020 167
    v 1356 1075 49

## Client output format

Every loop, the server receives no more than 7 bytes in this format:
`<Movement> <Angle> <Attack>`. Again, these values need to be specially
encoded.

### Movement

This is the most awkward one. As we can all imagine, there are 9 different
directions for the hero to move. If we represent them as two-dimensional
vector, at least 3 characters will be needed to describe such a simple thing,
e.g. `1 0` for m = (1, 0), and in the worst-case scenario m = (-1, -1), we will
need to use 5: `-1 -1`. 40 bits used to carry a 4-bit piece of data, freaking
insane, right? So instead, we decided to *slightly* encode it like this:

| Direction | Left  |  Nil  | Right |
| --------- | :---: | :---: | :---: |
| Up        |   0   |   1   |   2   |
| Nil       |   3   |   4   |   5   |
| Down      |   6   |   7   |   8   |

### Angle

Direction to point to hero to, might be useful to aim or to perform close-range
attack manually. This value should also be converted to degrees and cast to a
nonnegative integer.

### Attack

Attack can be either of the three values:

0. Do nothing
1. Long-range attack
2. Close-range attack

Simple, huh? Though be aware that this won't have any effect if the hero cannot
strike an attack yet (as described in above section about
[Server output](#the-hero)).

## Pseudo-client

1. Create INET, STREAMing socket *s*
2. Connect *s* to the address `host:port` which the server is bound to
3. Receive length *l* of data
4. If *l* > 0, close *s* and quit
5. Receive the data
6. Process the data
7. Send instruction for the hero to the server and go back to step 3

Your AI should try to not only reach the highest score possible, but also in
the smallest amount of time. For convenience purpose, the server will log these
values to stdout.

There are samples of client implementations in different languages in
[client-examples](https://github.com/McSinyx/brutalmaze/tree/master/client-examples)
directory (more are coming).
