"""Spectrum analyzer mode"""
import sys
import asyncio
import itertools
from dataclasses import dataclass
import numpy as np
from unyt import unyt_quantity, unyt_array
from rsfsup.common import Subsystem
from rsfsup.spectrum_analyzer.display import Display
from rsfsup.spectrum_analyzer.frequency import Frequency
from rsfsup.spectrum_analyzer.amplitude import Amplitude
from rsfsup.spectrum_analyzer.bandwidth import Bandwidth
from rsfsup.spectrum_analyzer.sweep import Sweep
from rsfsup.spectrum_analyzer.markers import Marker, DeltaMarker
from rsfsup.spectrum_analyzer.traces import Trace


@dataclass
class State:
    """Signal for controlling asyncio tasks"""

    running: bool = False


class SpecAn(Subsystem, kind="Spectrum Analyzer"):
    """Spectrum analyzer mode

    Attributes:
        instr (Fsup)
    """

    def __init__(self, instr):
        super().__init__(instr)
        self.display = Display(instr)
        self.frequency = Frequency(instr)
        self.amplitude = Amplitude(instr)
        self.bandwidth = Bandwidth(instr)
        self.sweep = Sweep(instr)
        self._markers = [Marker(instr, num) for num in range(1, 5)]
        self._deltamarkers = [DeltaMarker(instr, num) for num in range(1, 5)]
        self._traces = [Trace(instr, 1)]
        trace = self._traces[0]
        trace.state = "ON"
        setattr(self, trace._name, trace)
        self._state = State()

    def reference_fixed(self, state="ON"):
        """state (str): {ON, OFF}
            Turn on markers 1 and 2, if necessary, and set markers 2 to 4 as delta
            markers fixed to marker 1
        """
        self.enable_marker(1)
        self.enable_marker(2, as_delta=True)
        self._visa.write(f"CALC{self._screen()}:DELT2:FUNC:FIX {state}")

    def enable_marker(self, num, as_delta=False):
        """num (int): marker/deltamarker number {1, 2, 3, 4}
        as_delta (bool): True if deltamarker"""
        i = num - 1
        marker = self._markers[i]
        deltamarker = self._deltamarkers[i]
        # pylint: disable=protected-access
        if as_delta:
            deltamarker.state = "ON"
            try:
                setattr(self, deltamarker._name, deltamarker)
            except AttributeError:
                pass
            marker.state = "OFF"
            try:
                delattr(self, marker._name)
            except AttributeError:
                pass
        else:
            deltamarker.state = "OFF"
            try:
                delattr(self, deltamarker._name)
            except AttributeError:
                pass
            marker.state = "ON"
            try:
                setattr(self, marker._name, marker)
            except AttributeError:
                pass

    def turnoff_markers(self):
        """Turn off all markers in the active screen"""
        for marker in self._markers + self._deltamarkers:
            marker.state = "OFF"

    def clear_traces(self):
        """Clear all traces"""
        self._visa.write(f"DISP:WIND{self._screen()}:TRACE:CLEAR")

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

    async def _measure_spectrum(self):
        """Measure spectrum"""
        try:
            self._visa.write("*CLS")
            self._visa.write("SYSTEM:ERROR:CLEAR:ALL")
            self._visa.query("STATUS:OPERATION:EVENT?")
            self._visa.query("STATUS:QUESTIONABLE:EVENT?")
            self._visa.write("*SRE 191")
            self._visa.write("*ESE 63")
            self._visa.write("STATUS:OPERATION:PTRANSITION 0")
            self._visa.write("STATUS:QUESTIONABLE:PTRANSITION 296")
            original_continuous = self._visa.query("INIT:CONT?")
            self._visa.write("INIT:CONT OFF")
            self._visa.write(f"INIT; *OPC")
            # poll the ESB bit for an event occurance indicating completion or error
            while not self._visa.stb & 32:
                await asyncio.sleep(1)
            self._state.running = False
            esr = int(self._visa.query("*ESR?"))
            op_complete = bool(esr & 1)
            return 0 if op_complete else 1
        except asyncio.CancelledError:
            pass
        finally:
            self._visa.write(f"INIT:CONT {original_continuous}")

    async def _start_task(self, timeout):
        self._state.running = True
        task = asyncio.gather(self._show_spinner(), self._measure_spectrum())
        try:
            ret_value = await asyncio.wait_for(task, timeout)
        except asyncio.TimeoutError:
            raise TimeoutError("Phase noise measurement timed out") from None
        else:
            return ret_value

    def read(self, trace=1, timeout=None):
        """Read trace data and return tuple (X, Y)

        Parameters:
            trace (int): {1, 2, 3}
            timeout (int): timeout in seconds or None
        """
        ret_value = asyncio.run(self._start_task(timeout))
        if ret_value is None:
            return None
        if ret_value[1] > 0:
            print(self._instr.status.event_status)
            return None
        num = self.sweep.points
        start_str = self.frequency.start
        value, unit = start_str.split(" ")
        start = unyt_quantity(float(value), unit)
        stop_str = self.frequency.stop
        value, unit = stop_str.split(" ")
        stop = unyt_quantity(float(value), unit)
        x = np.linspace(start, stop, num=num, endpoint=True)
        x.name = "$f$"
        i = trace - 1
        data = self._traces[i].data
        unit = self._traces[i].y_unit
        y = unyt_array(data, unit)
        y.name = "$P$"
        return (x, y)

    def __dir__(self):
        for marker in self._markers + self._deltamarkers:
            if marker.state == "OFF":
                try:
                    delattr(self, marker._name)
                except AttributeError:
                    pass
        return super().__dir__()
