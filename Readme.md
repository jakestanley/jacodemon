# Jake's Doom Launcher & Stream Manager

## Running

Sensible defaults are chosen for recording and streaming

- `music` enables music which is disabled by default for copyright concerns
- `--no-demo` disables demo recording
- `--no-obs` disables OBS control
- `--no-gui` disables the options screen on launch
- `--no-mods` disables additional mods
- `--no-auto_record`

## Configuration

### Script variables

- Update `config.json` accordingly. Currently the script is not resilient to missing values.

### Playlist format (CSV)

I worked with ChatGPT to come up with a format that works for mods where a list of maps is provided and when one is not.

```
ModName,MapId,MapName,Author,CompLevel,Files,Merge,Port,Notes
Fava Beans,E1M1,Gaspra Armory,Sean Birkel,2,FAVA.WAD,,,
Fava Beans,E1M2,Hangar 18,Sean Birkel,2,FAVA.WAD,,,
Fava Beans,E1M3,Impalement Station,Sean Birkel,2,FAVA.WAD,,,Exit to secret level
The Final Gathering,,,Stormin,2,GATHER.WAD,,,From original release. Maps unnamed. Mod test
The Final Gathering (Bonus),MAP04,,Stormin,9,GATHER2.WAD|NEW.WAD,,,Bonus level added in 2005. Using Boom to be safe
The Final Gathering (Bonus),MAP05,,Stormin,9,GATHER2.WAD|NEW.WAD,,,Bonus level added in 2005. Using Boom to be safe
```

The following values _MUST_ currently be present in the map CSV for the script to work:

- `ModName`
- `MapId` (optional*)
	- Expected formats are 'E1M1' (Doom) or 'MAP01' (Doom 2)
- `MapName` (optional)
    - MAY be displayed on the stream
- `Author` (optional)
    - MAY be displayed on the stream
    - If no MapIds provided for this ModName, this will be used for all maps in the mod
- `CompLevel` (optional)
	- If empty, `default_complevel` from `config.json` is used
- `Files` determines the files that need to be loaded. 
	- Currently DEH and WAD are supported. 
	- Multiple files MUST be separated by a pipe character. 
	- This can be empty.
- `Merge` (optional)
    - For use with chocolate doom to specify which files require the `-merge` parameter
	- See [WAD merging capability](https://www.chocolate-doom.org/wiki/index.php/WAD_merging_capability)
- `Port` (optional)
    - Use this port to use, i.e `chocolate` for chocolate doom.
	- Defaults to dsda-doom
    - Overridden with `--source-port` flag
- `Notes` (optional)

*If ModName is provided without MapId, then a tool will be used to infer the maps from files. Note: if further maps are provided with the same name, they will be appended to the list for that mod. Handling this behaviour is not planned yet.

## Configure OBS

### Enable WebSocket server

- Menu -> Tools -> WebSocket Server Settings
- Check "Enable WebSocket server"
- Uncheck "Enable Authentication"
- Keep the default port, should be 4455

## Python

### Install dependencies

```
pip install -r requirements.txt
```

## Testing

- Uses `unittest` package
- Run `run_tests.py`

### Regression

TBC

## Scripting OBS

I'm referencing my bass stream from the past year when writing OBS commands: https://github.com/jakestanley/midi-obs-ws-thing/blob/main/app.js


# Optional functionality

- [maghoff/wad](https://github.com/maghoff/wad) for reading wad data (requires [rust](https://doc.rust-lang.org/cargo/getting-started/installation.html))

## Macros

### Windows
- ahk
- ahk (python)

### macOS
- [hammerspoon](http://www.hammerspoon.org/go/)
- hammerspoon-bridge [github](https://github.com/AaronC81/hammerspoon_bridge), [pypi](https://pypi.org/project/hammerspoon-bridge/)
- Hammerspoon must be running
- `~/.hammerspoon/init.lua` must contain the line: `local ipc = require('hs.ipc')`

## Notifications

### Windows
Ensure Python notifications are high priority so toast notifications will be visible when you are playing a game

# Thanks

## ChatGPT
For when my patience was wearing thin with PowerShell, and because I'm lazy.

## Doom Text Generator
Thanks to https://c.eev.ee/doom-text-generator for the rendered stream overlay text

## Doom Wiki
I've nicked so much data used in my streams from here. You can visit them at: https://doomwiki.org/

## id Software
For Doom of course

## Doomworld
For their contributions and support for this now 30 year old community