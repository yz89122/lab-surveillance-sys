# Scripts here

`display.py` - This simple python program is used to display image from camera.

`control.sh` - A controlling script written with bash. Supports movement, zooming and set speed.

# Video Stream

Since the VLC browser plug-in is unavailable, the only way to access video stream is through it's build-in streaming interface. The interface is using [RTSP](https://en.wikipedia.org/wiki/Real_Time_Streaming_Protocol). URL `rtsp://[IP addr]/medias1` for stream 1 and `rtsp://[IP addr]/medias2` for stream 2. Some media are supporting this protocol, such as VLC Media Player.

# Web interface

## Control

### Movement

Path: `/cgi-bin/view/cammove.cgi?move=[direction]`

#### `directions`

`up`

`down`

`left`

`right`

`upleft`

`upright`

`downleft`

`downright`

`home`

### Zoom

Path: `cgi-bin/view/cammove.cgi?move=[arg]`

#### `arg`

`rZoomIn`

`rZoomOut`

### Movement Speed

Path: `/cgi-bin/view/ptzspeed.cgi?speed=[speed]`

#### `speed`

from `1` to `10`

## Snapshot

Path: `/cgi-bin/view/ss.cgi`