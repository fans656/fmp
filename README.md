Requirements:
- [lib/libmpv-2.dll](https://mpv.io/installation/)

Notes:
- use double quote for filename with spaces

## [mpv properties](https://mpv.io/manual/master/#properties)

To access a property (e.g. "wdith"), do `mpv.width` or `mpv._get_property('width')`

- `width` / `height` - video width/height
- `dwidth` / `dheight` - video width/height with scaling applied
- `display-width` / `display-height` - video width/height of display
- `time-pos` / `time-pos/full`
- `playback-abort`
- `user-data`
- `menu-data`
- `working-directory`
- `property-list`
- `command-list`
- `input-bindings`
