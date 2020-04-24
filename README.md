# pytermvis
Python Terminal Audio Visualizer

## Requirements

Required:

* numpy
* scipy
* [pyalsaaudio](https://github.com/larsimmisch/pyalsaaudio) or [SoundCard](https://github.com/bastibe/SoundCard)


Optional:

* [asciimatics](https://github.com/peterbrittain/asciimatics)
* [pygame](https://www.pygame.org/)


## How to install

```sh
$ git clone https://github.com/bharris6/pytermvis.git
$ cd pytermvis
$ pip install .
```

Once installed, you need to set up the appropriate sampler for your machine.

### ALSA

ALSA support relies on the `pyalsaaudio` package and a loopback module `snd-aloop` being loaded.  Then your ALSA configuration needs to support splitting sound output to the loopback interface as well as to your normal speakers.

```sh
$ pip install --user pyalsaaudio
```

Some resources for ALSA loopback configuration can be found below:

* [Playing with ALSA Loopback Devices](https://sysplay.in/blog/linux/2019/06/playing-with-alsa-loopback-devices/)
* [Building and Installing ALSA Loopback](http://confoundedtech.blogspot.com/2012/08/building-installing-alsa-loopback.html)

NOTE: There's also the [alsaloop](http://manpages.ubuntu.com/manpages/bionic/man1/alsaloop.1.html) command, but I have not played with that.  

#### How to run

ALSA requires specification of the right sampler:

```sh
$ pytermvis -b alsa
```

### SoundCard

`SoundCard` supports Linux/pulseaudio, Mac/coreaudio, and Windows/WASAPI.

```sh
$ pip install --user soundcard
```

#### How to run

`SoundCard` is the default sampler, but can be specified as well:

```sh
$ pytermvis -b soundcard
```

## General How to Run

The install method will put a command `pytermvis` on your path that you can execute.  Once you've installed `pytermvis` itself and installed an appropriate sampler, you can run it using that command:

```sh
$ pytermvis -r text
```

You can also run `pytermvis` using python's `-m` flag instead:

```sh
$ python -m pytermvis.run -r text
```

### Extra Renderers

A basic install will only support a text-based renderer.  To use the `asciimatics` or `pygame` renderers, you'll need to install their respective packages.

#### Asciimatics

```sh
$ pip install --user asciimatics
```

Once installed, `asciimatics` can be selected as the renderer by using the `-r` flag:

```sh
$ pytermvis -r asciimatics
```

#### Pygame

```sh
pip install --user pygame
``` 

Once installed, `pygame` can be selected as the renderer by using the `-r` flag:

```sh
$ pytermvis -r pygame
```

It will show the same prompt for selection of sound device as the other renderers.  The difference is, a new window will be created in which the visualizer output is drawn.  

### Options

| Shortcode | Long Code | Description |
|:----------|:----------|:------------|
| -c        | --char    | What character to draw with.  One-character string. Default "\*" |
| -s        | --sample-rate | What rate to sample at.  Integer.  Default 44100. |
| -r        | --renderer | Renderer to use.  "text", "asciimatics", or "pygame".  Default "text" |
| -b        | --backend | Which backend sampler to use.  "alsa" or "soundcard".  Default "soundcard" |
| -t        | --type | Which waveform to use.  "audio" or "spectrum".  Default "spectrum" |

## What does it do?

`pytermvis` uses `SoundCard`'s or `pyalsaaudio`'s ability to record from "loopback" devices.  This means it is basically catching the audio output of your speaker and passing those raw frames through `numpy`'s/`scipy`'s FFT to get the frequency domain representation.  Then, that FFT data is split into buckets based on the terminal width and each bucket's amplitude is printed as vertical lines using one of the renderers: `asciimatics`, `pygame`, or a printline output.

## Issues 

Requires Python 3.x, preferable 3.6+.

ALSA support isn't really configurable.  
