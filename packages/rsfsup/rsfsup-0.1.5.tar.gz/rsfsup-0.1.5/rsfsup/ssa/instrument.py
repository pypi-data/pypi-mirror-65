"""Signal Source Analyzer mode (PNO)"""
import sys
import itertools
import asyncio
from dataclasses import dataclass
import pyvisa
from unyt import unyt_array
from rsfsup.common import Subsystem
from rsfsup.ssa.display import Display
from rsfsup.ssa.configure import Configure
from rsfsup.ssa.traces import Trace


@dataclass
class State:
    """Signal for controlling asyncio tasks"""

    running: bool = False


class SSA(Subsystem, kind="SSA"):
    """Signal Source Analyzer subsystem for phase noise measurements

    Steps to measure phase noise of a CW signal source (PLL, CCORrelation):
    - Set center frequency, amplitude and bandwidth in SPECTRUM mode
    - Switch to SSA mode
    - Configure measurement (PLL, CCORrelation)
    - Configure expected RF power ('auto', float dBm)
    - Configure TSETup {INT1, INT3}

    Attributes:
        instr (Fsup)
    """

    def __init__(self, instr):
        super().__init__(instr)
        self.display = Display(instr)
        self.configure = Configure(instr)
        self._traces = [Trace(instr, 1)]
        trace = self._traces[0]
        trace.state = "ON"
        setattr(self, trace._name, trace)
        self._state = State()

    async def _show_spinner(self):
        """Show an in-progress spinner during phase noise measurement"""
        spinner = itertools.cycle(["-", "/", "|", "\\"])
        try:
            while self._state.running:
                sys.stdout.write(next(spinner))
                sys.stdout.flush()
                sys.stdout.write("\b")
                await asyncio.sleep(0.5)
            return 0
        except asyncio.CancelledError:
            pass
        finally:
            sys.stdout.write("\b \b")

    async def _measure_phase_noise(self, premeasure):
        """Perform phase noise measurement"""
        sweep = "NEW" if premeasure else "IMMEDIATE"
        try:
            self._visa.write("*CLS")
            self._visa.write("SYSTEM:ERROR:CLEAR:ALL")
            self._visa.query("STATUS:OPERATION:EVENT?")
            self._visa.query("STATUS:QUESTIONABLE:EVENT?")
            self._visa.write("*SRE 191")
            self._visa.write("*ESE 63")
            self._visa.write("STATUS:OPERATION:PTRANSITION 16")
            self._visa.write("STATUS:QUESTIONABLE:PTRANSITION 24744")
            original_continuous = self._visa.query("INIT:CONT?")
            self._visa.write("INIT:CONT OFF")
            self._visa.write(f"INIT:{sweep}; *OPC")
            # poll the ESB bit for an event occurance indicating completion or error
            while not self._visa.stb & 32:
                await asyncio.sleep(1)
            esr = int(self._visa.query("*ESR?"))
            op_complete = bool(esr & 1)
            self._visa.write(f"INIT:CONT {original_continuous}")
            return 0 if op_complete else 1
        except asyncio.CancelledError:
            pass
        except pyvisa.VisaIOError as exc:
            if exc.abbreviation == "VI_ERROR_TMO":
                raise TimeoutError(
                    "Acquisition timed out due to loss of communication"
                ) from None
            raise
        finally:
            self._state.running = False

    async def _start_task(self, premeasure, timeout):
        self._state.running = True
        task = asyncio.gather(
            self._show_spinner(), self._measure_phase_noise(premeasure)
        )
        try:
            ret_value = await asyncio.wait_for(task, timeout)
        except asyncio.TimeoutError:
            raise TimeoutError("Phase noise measurement timed out") from None
        else:
            return ret_value

    def read(self, premeasure=True, timeout=None):
        """Measure the phase noise and return (X, Y) tuple

        Parameters:
            premeasure (bool): perform premeasurement
            timeout (int): timeout in seconds or None
        """
        ret_value = asyncio.run(self._start_task(premeasure, timeout))
        if ret_value is None:
            return None
        if ret_value[1] > 0:
            print(self._instr.status.event_status)
            return None
        x_values, y_values = self._traces[0].data
        x = unyt_array(x_values, "Hz")
        x.name = "$f$"
        y = unyt_array(y_values, "dBc/Hz")
        y.name = "$N$"
        return (x, y)
