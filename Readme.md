# Jake's Doom Launcher & Stream Manager

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

*If ModName is provided without MapId, then a tool will be used to infer the maps from files. Note: if further maps are provided with the same name, they will be appended to the list for that mod. Handling this behaviour is not planned yet.

## Configure OBS

### Enable WebSocket server

- Menu -> Tools -> WebSocket Server Settings
- Check "Enable WebSocket server"
- Uncheck "Enable Authentication"
- Keep the default port, should be 4455

### Scenes and inputs

The `start.ps1` script is expecting the following scenes and inputs:
- Input "Text" for the map title, displayed at the top of the screen
- Scenes "Waiting" and "Playing" for switching between the map selection and game in progress states

These are subject to change.

## PowerShell

I'm not that sharp with PowerShell and Windows package management but here's my best attempt.

### Upgrade PowerShell

```
winget install --id Microsoft.Powershell --source winget
```

Close PowerShell and launch PowerShell 7. You may wish to set this as the default Windows Terminal profile.

### Install OBSWebSocket

- Documentation: https://github.com/onyx-and-iris/OBSWebSocket-Powershell
- Requests: https://github.com/obsproject/obs-websocket/blob/master/docs/generated/protocol.md#requests
- PowerShell Gallery: https://www.powershellgallery.com/packages/OBSWebSocket/0.0.4

```
Install-Module -Name OBSWebSocket -Scope CurrentUser
```

## Python

### Install dependencies

```
pip install -r requirements.txt
```

## Testing

Run any scripts in `lib/py` or `lib/ps` with the `test_` prefix
I intend to add more tests later excepting UI tests.

```
lib/py/test_*.py
```

## Scripting OBS

I'm referencing my bass stream from the past year when writing OBS commands: https://github.com/jakestanley/midi-obs-ws-thing/blob/main/app.js

# Post-processing

## Extract audio tracks

Assuming that you have the OBS audio channels set up like I do in the format:

- All
- Desktop
- Microphone

Then you can use the following PowerShell snippet to separate the audio tracks for easier editing later:
```
foreach ($file in (Get-ChildItem "." -Filter *.mkv)) {

    $streams = ffprobe -v error -select_streams a $file.FullName -show_entries stream=index:stream_tags=title -of csv=p=0 | ConvertFrom-Csv -Header Index,Title
    $desktopStream = $streams | Where-Object {$_.Title -eq "Desktop"}
    $microphoneStream = $streams | Where-Object {$_.Title -eq "Microphone"}

    $desktopStreamIndex = $desktopStream.Index
    $microphoneStreamIndex = $microphoneStream.Index
    $desktopStreamIndex = [int]$desktopStreamIndex - 1
    $microphoneStreamIndex = [int]$microphoneStreamIndex - 1

    Write-Host $desktopStreamIndex
    Write-Host $microphoneStreamIndex

    # Use ffmpeg to extract the "Desktop" and "Microphone" audio streams
    ffmpeg -i $file.FullName -map 0:a:$desktopStreamIndex -c:a copy ("{0}_Desktop.m4a" -f $file.BaseName)
    ffmpeg -i $file.FullName -map 0:a:$microphoneStreamIndex -c:a copy ("{0}_Microphone.m4a" -f $file.BaseName)
}
```

## Convert to format supported by iMovie (sorry, it's what I like)

I'm assuming you are doing this on an Nvidia card with CUDA support.

```
Get-ChildItem -Path "." -Filter *.mkv | ForEach-Object { ffmpeg.exe -hwaccel cuvid -i $_.FullName -c:v h264_nvenc -cq:v 20 -b:v 4M -maxrate:v 8M -bufsize:v 16M -c:a copy $($_.FullName -replace '.mkv','.mp4') }
```

## Use SSH to copy to your editing machine

## Or you could do all of the above in one loop

I also added a bit on archiving

```
if (-not (Test-Path -Path ".\Originals" -PathType Container)) {
    New-Item -ItemType Directory -Path ".\Originals"
}

foreach ($file in (Get-ChildItem "." -Filter *.mkv)) {

    $streams = ffprobe -v error -select_streams a $file.FullName -show_entries stream=index:stream_tags=title -of csv=p=0 | ConvertFrom-Csv -Header Index,Title
    $desktopStream = $streams | Where-Object {$_.Title -eq "Desktop"}
    $microphoneStream = $streams | Where-Object {$_.Title -eq "Microphone"}

    $desktopStreamIndex = $desktopStream.Index
    $microphoneStreamIndex = $microphoneStream.Index
    $desktopStreamIndex = [int]$desktopStreamIndex - 1
    $microphoneStreamIndex = [int]$microphoneStreamIndex - 1

    Write-Host $desktopStreamIndex
    Write-Host $microphoneStreamIndex

    # Use ffmpeg to extract the "Desktop" and "Microphone" audio streams
    ffmpeg -i $file.FullName -map 0:a:$desktopStreamIndex -c:a copy ("{0}_Desktop.m4a" -f $file.BaseName)
    ffmpeg -i $file.FullName -map 0:a:$microphoneStreamIndex -c:a copy ("{0}_Microphone.m4a" -f $file.BaseName)
    ffmpeg -hwaccel cuvid -i $file.FullName -c:v h264_nvenc -cq:v 20 -b:v 4M -maxrate:v 8M -bufsize:v 16M -c:a copy $($file.FullName -replace '.mkv','.mp4')
    Move-Item -Path $file.FullName -Destination ".\Originals\"
}
```

# Optional functionality

- [maghoff/wad](https://github.com/maghoff/wad) for reading wad data (requires [rust](https://doc.rust-lang.org/cargo/getting-started/installation.html))

# Thanks

## ChatGPT
For when my patience was wearing thin with PowerShell, and because I'm lazy.

## Doom Text Generator
Thanks to https://c.eev.ee/doom-text-generator for the rendered stream overlay text

## Doom Wiki
Wanted to include their logo as I am using their resource. I'm not affiliated with the Doom Wiki but they are a great bunch. You can visit them here: https://doomwiki.org/
