## Configuration files

At the time of writing, this is the default configuration file:

```ini
[Graphics]
Screen width: 640
Screen height: 480
# FPS should not be greater than refresh rate.
Maximum FPS: 60

[Sound]
Muted: no
# Volume must be between 0.0 and 1.0.
Music volume: 1.0
# Use space music background, which sounds cold and creepy.
Space theme: no

[Control]
# Touch-friendly control
Touch: no
# Input values should be either from Mouse1 to Mouse3 or a keyboard key
# and they are case-insensitively read.
# Aliases for special keys are listed here (without the K_ part):
# http://www.pygame.org/docs/ref/key.html
# Key combinations are not supported.
New game: F2
Toggle pause: p
Toggle mute: m
Move left: a
Move right: d
Move up: w
Move down: s
Long-range attack: Mouse1
Close-range attack: Mouse3

[Record]
# Directory to write record of game states, leave blank to disable.
Directory:
# Number of snapshots per second. This is preferably from 3 to 60.
Frequency: 30

[Server]
# Enabling remote control will disable control via keyboard and mouse.
Enable: no
Host: localhost
Port: 8089
# Timeout on blocking socket operations, in seconds.
Timeout: 1.0
# Disable graphics and sound (only if socket server is enabled).
Headless: no
```

By default, Brutal Maze also then tries to read site (system-wide) and user
configuration.

### Site config file location

* Apple macOS: `/Library/Application Support/brutalmaze/settings.ini`
* Other Unix-like: `$XDG_CONFIG_DIRS/brutalmaze/settings.ini` or
  `/etc/xdg/brutalmaze/settings.ini`
* Microsoft Windows:
    * XP: `C:\Documents and Settings\All Users\Application Data\brutalmaze\settings.ini`
    * Vista: Fail! (`C:\ProgramData` is a hidden *system* directory, however
      if you use Windows Vista, please file an issue telling us which error you
      receive)
    * 7 and above: `C:\ProgramData\brutalmaze\settings.ini`

### User config file location

* Apple macOS: `~/Library/Application Support/brutalmaze/settings.ini`
* Other Unix-like: `$XDG_CONFIG_HOME/brutalmaze/settings.ini` or
  `~/.config/brutalmaze/settings.ini`
* Microsoft Windows (roaming is not supported until someone requests):
    * XP: `C:\Documents and Settings\<username>\Application Data\brutalmaze\settings.ini`
    * Vista and above: `C:\Users\<username>\AppData\Local\brutalmaze\settings.ini`

## Command-line arguments

```sh
$ brutalmaze --help
usage: brutalmaze [options]

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  --write-config [PATH]
                        write default config and exit, if PATH not specified use stdout
  -c PATH, --config PATH
                        location of the configuration file
  -s X Y, --size X Y    the desired screen size
  -f FPS, --max-fps FPS
                        the desired maximum FPS
  --mute, -m            mute all sounds
  --unmute              unmute sound
  --music-volume VOL    between 0.0 and 1.0
  --space-music         use space music background
  --default-music       use default music background
  --touch               enable touch-friendly control
  --no-touch            disable touch-friendly control
  --record-dir DIR      directory to write game records
  --record-rate SPF     snapshots of game state per second
  --server              enable server
  --no-server           disable server
  --host HOST           host to bind server to
  --port PORT           port for server to listen on
  -t TIMEOUT, --timeout TIMEOUT
                        socket operations timeout in seconds
  --head                run server with graphics and sound
  --headless            run server without graphics or sound
```

First, Brutal Mazes read the default settings, then it try to read site and
user config whose locations are shown above. These files are listed as fallback
of the `--config` option and their contents are fallback for other options (if
they are absent default values are used instead). We don't support control
configuration via CLI because that is unarguably ugly.

If `--config` option is set, Brutal Maze parse it before other command-line
options. Later-read preferences will override previous ones.
