"""Display subsystem specific to SSA mode"""
from rsfsup.common import Subsystem, validate


class Display(Subsystem, kind="Display"):
    """Display subsystem

    Attributes:
        instr (Fsup)
    """

    def __init__(self, instr):
        super().__init__(instr)
        self._psave_holdoff = 0
        self._visa.write(f"DISPLAY:PSAVE:STATE OFF")

    @property
    def pwr_save(self):
        """value (int): screen-saver timeout in minutes (1 to 60), 0 disables pwr save"""
        return self._psave_holdoff

    @pwr_save.setter
    @validate
    def pwr_save(self, value):
        self._psave_holdoff = value
        if value:
            self._visa.write(f"DISPLAY:PSAVE:HOLDOFF {value}")
            self._visa.write("DISPLAY:PSAVE:STATE ON")
        else:
            self._visa.write("DISPLAY:PSAVE:STATE OFF")
