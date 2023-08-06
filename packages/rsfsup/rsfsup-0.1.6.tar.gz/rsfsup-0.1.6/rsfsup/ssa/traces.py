"""Traces subsystem"""
from rsfsup.common import Subsystem, validate

_MODES = {"WRIT": "WRITE", "AVER": "AVERAGE", "MAXH": "MAXHOLD"}


class Trace(Subsystem, kind="Trace"):
    """Trace subsystem

    Attributes:
        instr (Fsup)
        num (int): trace number {1, 2, 3}
    """

    def __init__(self, instr, num):
        super().__init__(instr)
        self._num = num
        self._name = f"trace_{num}"

    @property
    def mode(self):
        """value (str): {WRITE, AVERAGE, MAXHOLD}"""
        value = self._visa.query(f"DISP:WIND1:TRAC{self._num}:MODE?")
        return _MODES[value]

    @mode.setter
    @validate
    def mode(self, value):
        self._visa.write(f"DISP:WIND1:TRAC{self._num}:MODE {value}")

    @property
    def state(self):
        """value (str): {ON , OFF}"""
        value = int(self._visa.query(f"DISP:WIND1:TRAC{self._num}:STATE?"))
        return "ON" if value else "OFF"

    @state.setter
    @validate
    def state(self, value):
        self._visa.write(f"DISP:WIND1:TRAC{self._num}:STATE {value}")

    @property
    def y_unit(self):
        """(str) Y axis unit"""
        result = self._visa.query(f"DISP:WIND1:TRAC:Y:UNIT?")
        noise_units = {
            "DBC/HZ": "dBc/Hz",
        }
        return noise_units.get(result, result)

    @property
    def data(self):
        """(tuple): (X, Y) values"""
        # In SSA mode, trace data is both x and y interleaved
        data = self._visa.query_ascii_values(f"TRACE? TRACE{self._num}")
        x = data[::2]
        y = data[1::2]
        return (x, y)
