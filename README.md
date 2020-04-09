# pytermvis
Terminal Audio Visualizer

## Requirements

* asciimatics
* numpy
* scipy
* [SoundCard](https://github.com/bastibe/SoundCard)

## How to install

```
$ git clone https://github.com/bharris6/pytermvis.git
$ cd pytermvis
$ pip install --user -r requirements.txt
```

## How to run

```
$ python pytermvis.py
```

This will query your local system to determine what sound devices exist, and prompt you to choose one.  All visualizer output is in the same terminal.  

### Options

| Shortcode | Long Code | Description |
|:----------|:----------|:------------|
| -c        | --char    | What character to draw with.  One-character string. Default "\*" |
| -s        | --sample-rate | What rate to sample at.  Integer.  Default 44100. |
| -r        | --renderer | Renderer to use.  "asciimatics" or "pygame".  Default "asciimatics" |

## What does it do?

`pytermvis` uses `SoundCard`'s ability to record from "loopback" devices.  This means it is basically catching the audio output of your speaker and passing those raw frames through `numpy`'s/`scipy`'s FFT to get the frequency domain representation.  Then, that FFT data is split into buckets based on the terminal width and each bucket's amplitude is printed as vertical lines using `asciimatics`.

## Issues

Requires PulseAudio for now on Linux.  Should work fine on Windows, and with both Python 2.x and Python3.x versions.  

## Extras

If you want to try out the `pygame` version, just `pip install pygame` and then

```
$ python pytermvis -r pygame
```

It will show the same prompt for selection of sound device.  The difference is, a new window will be created which has the visualizer output.  

