[![Build Status](https://travis-ci.org/Moguri/panda3d-eventmapper.svg?branch=master)](https://travis-ci.org/Moguri/panda3d-eventmapper)
[![Package Versions](https://img.shields.io/pypi/pyversions/panda3d-eventmapper.svg)](https://pypi.org/project/panda3d-eventmapper/)
[![Panda3D Versions](https://img.shields.io/badge/panda3d-1.9%2C%201.10-blue.svg)](https://www.panda3d.org/)
[![License](https://img.shields.io/github/license/Moguri/panda3d-eventmapper.svg)](https://choosealicense.com/licenses/bsd-3-clause/)

# Panda3D Event Mapper
A simple utility to remap Panda3D events.

## Features

* Remap events
* Configure via PRC variables or an API
* Handle keyboards, mice, and gamepads

## Installation

Use [pip](https://pypi.org/project/pip/) to install the `panda3d-eventmapper` package:

```bash
pip install panda3d-eventmapper
```

## Example

```python
import sys

from direct.showbase.ShowBase import ShowBase
import panda3d.core as p3d

import eventmapper


p3d.load_prc_file_data(
    '',
    'event-map-item-quit escape q\n'
    'event-map-item-move-forward raw-w\n'
    'event-map-item-move-backward raw-s\n'
    'event-map-item-move-left raw-a\n'
    'event-map-item-move-right raw-d\n'
)


class GameApp(ShowBase):
    def __init__(self):
        super().__init__()

        self.eventmapper = eventmapper.EventMapper()
        self.accept('quit', sys.exit)
        self.accept('move-forward', print, ['move forward'])
        self.accept('move-backward', print, ['move backward'])
        self.accept('move-left', print, ['move left'])
        self.accept('move-right', print, ['move right'])

GameApp().run()
```

## License

[BSD](https://choosealicense.com/licenses/bsd-3-clause/)
