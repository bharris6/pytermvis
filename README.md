# pytermvis
Python Terminal Audio Visualizer

## Requirements

Required:

* numpy
* matplotlib
* [pyalsaaudio](https://github.com/larsimmisch/pyalsaaudio) or [SoundCard](https://github.com/bastibe/SoundCard)

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
$ pytermvis -s alsaaudio
```

### SoundCard

`SoundCard` supports Linux/pulseaudio, Mac/coreaudio, and Windows/WASAPI.

```sh
$ pip install --user soundcard
```

#### How to run

`SoundCard` is the default sampler, but can be specified as well:

```sh
$ pytermvis -s soundcard
```

## General How to Run

The install method will put a command `pytermvis` on your path that you can execute.  Once you've installed `pytermvis` itself and installed an appropriate sampler, you can run it using that command:

```sh
$ pytermvis -m audio
```

You can also run `pytermvis` using python's `-m` flag instead:

```sh
$ python -m pytermvis.run -m audio
```

### Extra Renderers

A basic install only supports the matplotlib renderer. 

### Options

| Shortcode | Long Code | Description |
|:----------|:----------|:------------|
|           | --rate    | What rate to sample at.  Integer.  Default 44100. |
|           | --period  | How many chunks/frames per sample.  Integer.  Default 1024. |
| -r        | --renderer| Renderer to use.  "text" or "matplotlib".  Default "text" |
| -s        | --sampler | Which backend sampler to use.  "alsaaudio" or "soundcard".  Default "soundcard" |
| -m        | --mode    | Which visualization to display.  "audio" for the sound signal itself, or "fft"/"bfft"/"gfft" for various FFT transformations. Default "audio" |

## What does it do?

`pytermvis` uses `SoundCard`'s or `pyalsaaudio`'s ability to record from "loopback" devices.  This means it is basically catching the audio output of your speaker and passing those raw frames through `numpy`'s FFT to get the frequency domain representation.  Then, that FFT data is split into buckets based on the terminal width and each bucket's magnitude is printed as vertical lines using one of the renderers.

## Issues 

Requires Python 3.4+.

ALSA support isn't really configurable.  
