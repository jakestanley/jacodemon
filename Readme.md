# JACODEMON

Jacodemon is a Doom launcher focused on managing your WADs, recording demos and with support for managing OBS recordings. It also includes a rudimentary achievement system when DSDA Doom is used. This was created to aid streaming and recording my journey through [Doomworld's "Top 100 WADs of All Time"](https://doomwiki.org/wiki/Top_100_WADs_of_All_Time). I stream almost all of my gameplay on [Twitch](https://www.twitch.tv/madstanners) and I occasionally edit and upload videos to [YouTube](https://www.youtube.com/user/madstanners).

The recommended source port to use with Jacodemon is DSDA Doom

## Features

### MapSets

Create a map set, with the WADs and DEH patches needed and Jacodemon will handle the rest

### MapSelect

Once you've opened a MapSet, you can see the following for each map if the information is available:
- Map ID
- Map name*
- Map author*
- "Badge"

*Supports UMAPINFO and ZMAPINFO currently

### OBS recording, scene, and overlay management

Configure for streaming and recording. Recorded videos will be named automatically. Can add level name overlay to stream automatically if your scene is set up right.

_need to expand on this wrt how to get OBS set up right_

### Demo and stats recording

By default a demo will be recorded for every run. 

If you complete the level, statistics will be saved for that run (for best results, exit the game on the "Kills, Secrets, Items" screen)

### Achievements & Badges

If you complete a map, when you next view the map select screen you'll see a little badge next to that map.

_need to explain the badges_

## Getting started

[Poetry](https://python-poetry.org/) is used for dependency management system and running. 

For more information, see the [development](#development) section

### Install

```
poetry install
```

### Run

```
poetry run jacodemon <args>
```

Sensible defaults are chosen for recording and streaming

- `--music` enables music which is disabled by default for copyright concerns
- `--last` plays the last chosen map and skips the GUI
- `--no-demo` disables demo recording
- `--no-obs` disables OBS control
- `--no-gui` disables the options screen on launch
- `--no-mods` disables additional mods
- `--no-auto-record`
- `--stdout-log-level <DEBUG,INFO,WARNING>` or `-sll` to set the logging levels that will print to the console

## Configure OBS

### Enable WebSocket server

- Menu -> Tools -> WebSocket Server Settings
- Check "Enable WebSocket server"
- Uncheck "Enable Authentication"
- Keep the default port, should be 4455

## Development

Preferred "IDE" is VSCode as it provides pretty clever Python and test integration.

### Testing

Testing leverages the the `unittest` framework

_please explain how to run tests_

## Roadmap

- More achievements/badges
- Show your time vs. par time
- Display WADINFO or accompanying text file if detected
- Migrate your config/stats/demos/cheevos, etc for backup
- View stats from map select
- Auto setup OBS scenes with "sensible defaults"
- Support more ports out of the box
- Big code cleanup
- All those TODOs I've left lying around
- Compile to a distributable and release
- Test coverage and UI regression plan for future releases
- Promote experimental features to actual features
- PEP compliance
- Plenty of bug fixes

## Experimental features

Don't rely on any of these to work, they're a bit rubbish. Actually, don't rely on anything in this app working properly but I digress...

### Macros

Currently hardcoded and for Windows only:
- Numpad 0: Capture replay buffer
- Numpad dot/delete: Cancel recording
- Numpad 3: Switch to browser scene and open doom wiki in a Qt web view (need to make this pop up)

#### Windows
- ahk
- ahk (python)

#### macOS
- [hammerspoon](http://www.hammerspoon.org/go/)
- hammerspoon-bridge [github](https://github.com/AaronC81/hammerspoon_bridge), [pypi](https://pypi.org/project/hammerspoon-bridge/)
- Hammerspoon must be running
- `~/.hammerspoon/init.lua` must contain the line: `local ipc = require('hs.ipc')`

### Notifications

#### Windows 11
Set these settings in Windows Settings to ensure notifications are visible when you are playing a game:
- In System -> Notifications, uncheck "When using an app in full-screen mode" under "Turn on do not disturb automatically"
- In System -> Notifications -> Set priority notifications, add "Python" under "Apps"

## Thanks

### Package maintainers
_please list Jake_

### ChatGPT
For when my patience was wearing thin, and because I'm lazy

### Doom Text Generator
Thanks to https://c.eev.ee/doom-text-generator for the rendered stream overlay text

### Doom Wiki
I've nicked so much data used in my streams from here. You can visit them at: https://doomwiki.org/

### id Software
For Doom of course

### Doomworld
For their contributions and support for this now 30 year old community