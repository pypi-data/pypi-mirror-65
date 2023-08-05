# `rsfsup`
Python interface to the Rohde & Schwarz FSUP Signal Source Analyzer

## Installation
```linux
$ pip install rsfsup
```  

## Usage
It is possible to configure the instrument and read the trace data with this library.
The first example shows reading the spectrum analyzer trace in a context manager.

```python
>>> from rsfsup import CommChannel
>>> with CommChannel("<ip address>") as fsup:
...     data = fsup.spectrum.read()
>>> import matplotlib.pyplot as plt
>>> plt.plot(*data)
[<matplotlib.lines.Line2D at ...>]
>>> plt.show()
```  

The next example shows switching to SSA mode to measure phase noise. This one also shows
using the CommChannel directly, which is useful in interactive sessions where features
of the instrument can be accessed using tab completion.

```python
>>> from rsfsup import CommChannel
>>> cc = CommChannel("<ip address>")
>>> fsup = cc.get_instrument()
>>> fsup.mode = "SSA"
>>> data = fsup.ssa.read()
>>> import matplotlib.pyplot as plt
>>> plt.semilogx(*data)
>>> plt.show()
>>> cc.close()
```

## Documentation