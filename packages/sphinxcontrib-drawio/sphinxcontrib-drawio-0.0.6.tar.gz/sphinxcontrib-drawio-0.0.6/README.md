# sphinxcontrib-drawio
Sphinx Extension to add the ``drawio`` directive to include draw.io diagrams.

**Important:** This extension is in development and not all features will work as advertised or at all.

The drawio-desktop package does not run without an x-server (e.g. when in a CI
environment), see
[this issue](https://github.com/jgraph/drawio-desktop/issues/146).
The workaround is to install `xvfb` and set the `drawio_headless` config to `auto`.

If any other of the `draw.io` CLI tool's options are wanted, please file an issue.

## Installation

1. `python3 -m pip install sphinxcontrib-drawio`
2. In your sphinx config:
```python
extensions = [
    "sphinxcontrib.drawio"
]
```
3. Add the binary to `$PATH`. For Windows add `C:\Program Files\draw.io` and on
Linux add `/opt/draw.io/`. 
4. (if running headless), `sudo apt install xvfb`

## Options
These values are placed in the `conf.py` of your sphinx project.

### Output Format
- *Formal Name*: `drawio_output_format`
- *Default Value*: `"png"`
- *Possible Values*: `"png"`, `"jpg"`, or `"svg"`

This config option controls the output file format which will be placed inside
the generated HTML. More file formats are available but not exposed, please
file an issue if you wish to add another file format.

### Binary Path
- *Formal Name*: `drawio_binary_path`
- *Default Value*: `None`

This allows for a specific override for the binary location. By default, this
gets chosen depending on the OS (Linux, Mac, or Windows) to the default
install path of the draw.io program.

### Headless Mode
- *Formal Name*: `drawio_headless`
- *Default Value*: `"auto"`
- *Possible Values*: `True`, `False`, or `"auto"`

This config option controls the behaviour of running the Xvfb server. It is
necessary because `draw.io` will not work without an X-server, see
[this issue](https://github.com/jgraph/drawio-desktop/issues/146).

The `auto` mode (on unix-like systems) will detect whether the program is
running in a headless environment through the `$DISPLAY` environment variable,
and act as if it were set to `True`. If running on Windows, or the `$DISPLAY`
environment variable contains some value (i.e. run in an X-server on a
developer's machine).

Setting the value to `True` will start a virtual X framebuffer through the
`Xvfb` command before running any `draw.io` commands, and stop it afterwards.

Setting the value to `False` will run the `draw.io` binary as normal.

## Usage
The extension can be used through the `drawio` directive, as per below:
```
.. drawio:: example.drawio
```

The directive can also be configured with a variety of options.

### Format
- *Formal Name*: `:format:`
- *Default Value*: `"png"`
- *Possible Values*: `"png"`, `"jpg"`, or `"svg"`

This option controls the output file format of *this specific* directive. It
provides similar functionality to that of the `drawio_output_format` config
option but at a more granular level.

### Alt Text
- *Formal Name*: `:alt:`

This option sets the img tag's `alt` attribute. For more information on its
functionality, see [the Mozilla web documentation](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/img#attr-alt).

### Format
- *Formal Name*: `:format:`
- *Default Value*: `"png"`
- *Possible Values*: `"png"`, `"jpg"`, or `"svg"`

This option controls the output file format of *this specific* directive. It
provides similar functionality to that of the `drawio_output_format` config
option but at a more granular level.

### Alignment
- *Formal Name*: `:align:`
- *Possible Values*: `"left"`, `"center"`, or `"right"`

This option allows control over the alignment of the image on the page.

### Page Index
- *Formal Name*: `:page-index:`
- *Default Value*: `0`
- *Possible Values*: any integer

This option allows you to select a particular page from a draw.io file to
create the image from.