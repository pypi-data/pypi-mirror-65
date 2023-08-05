# pylaunch
Simple library for working with the DIAL Protocol.

DIAL -- "DIscovery And Launch" is a simple protocol that second-screen devices can use to discover and launch apps on first-screen devices.

[Dial Protocol Specification](https://sites.google.com/a/dial-multiscreen.org/dial/dial-protocol-specification "DIAL Protocol Specifcation")

## Installation
`python3 -m pip install pylaunch`

## Usage
### Discover and Launch roku application
```python
from pylaunch.roku import Roku
d = Roku.discover()[0]

disney_plus = d.apps.get('Disney Plus')
disney_plus.launch()
```

### Basic Remote Control
```python
from pylaunch.roku import Roku
d = Roku('192.168.0.3')
d.power()
d.key_press('Right')
d.key_press('Down')
d.key_press('Select')
```

### Discover DIAL devices and launch YouTube to specific video
```python
from pylaunch.dial import Dial
d = Dial.discover()[0]

d.launch_app('YouTube', v='6tNS--WetLI')
```

## License
The MIT License (MIT)

Copyright (c) 2020 Steffen Andersland

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
