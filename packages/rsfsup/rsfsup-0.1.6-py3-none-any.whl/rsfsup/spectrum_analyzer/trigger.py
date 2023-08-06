"""Trigger subsystem for spectrum analyzer mode"""
from rsfsup.common import Subsystem, validate


class Trigger(Subsystem, kind="Trigger"):
    """Trigger subsystem for spectrum analyzer mode

    Specifically supports screen A immediate and external triggering.

    Attributes:
        instr (Fsup)
    """

    _sources = {"IMM": "FREE RUN", "EXT": "EXTERNAL"}
    _slopes = {"POS": "POSITIVE", "NEG": "NEGATIVE"}

    @property
    def source(self):
        """value (str): {IMMEDIATE, EXTERNAL}"""
        src = self._visa.query("TRIGGER1:SEQUENCE:SOURCE?")
        return Trigger._sources.get(src, src)

    @source.setter
    @validate
    def source(self, value):
        sources = {v: k for k, v in Trigger._sources.items()}
        src = sources.get(value, value)
        self._visa.write(f"TRIGGER1:SEQUENCE:SOURCE {src}")

    @property
    def level(self):
        """value (float, str): external trigger level in volts"""
        res = self._visa.query("TRIGGER1:SEQUENCE:LEVEL:EXTERNAL?")
        return f"{res} V"

    @level.setter
    @validate
    def level(self, value):
        self._visa.write(f"TRIGGER1:SEQUENCE:LEVEL:EXTERNAL {value}")

    @property
    def slope(self):
        """value (str): {POSITIVE, NEGATIVE}"""
        res = self._visa.query("TRIGGER1:SEQUENCE:SLOPE?")
        return Trigger._slopes[res]

    @slope.setter
    @validate
    def slope(self, value):
        self._visa.write(f"TRIGGER1:SEQUENCE:SLOPE {value}")

    @property
    def offset(self):
        """value (float, str): -100 s to 100 s, negative means pretrigger for zero span"""
        res = self._visa.query("TRIGGER1:SEQUENCE:HOLDOFF?")
        return f"{res} s"

    @offset.setter
    @validate
    def offset(self, value):
        self._visa.write(f"TRIGGER1:SEQUENCE:HOLDOFF {value}")
