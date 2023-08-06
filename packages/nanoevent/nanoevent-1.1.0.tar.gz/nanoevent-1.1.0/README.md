# Nanoevent

Nanoevent is a terrifically small and simple event dispatching library for
Python 3.6+. It's key features:

* Easy enough to start using in *minutes*.
* Pretty feature complete.
* Designed to be super simple to use.

## Installation

`pip install nanoevent`

## User guide

```python
import nanoevent

d = nanoevent.Dispatcher()

def handler(value):
    print(value)

d.attach('event:name', handler)

# The following results in "Hi, this is a test" being printed.
d.emit('event:name', 'Hi, this is a test')
```