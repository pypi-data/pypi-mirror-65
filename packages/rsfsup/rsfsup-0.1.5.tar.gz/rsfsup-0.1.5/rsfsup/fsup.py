"""Fsup class"""
from datetime import datetime
from rsfsup.common import RSBase, get_idn, validate
from rsfsup.status import Status
from rsfsup.spectrum_analyzer.instrument import SpecAn
from rsfsup.ssa.instrument import SSA


class Fsup(RSBase):
    """Fsup class

    Attributes:
        visa (pyvisa.resources.Resource): pyvisa resource
    """

    _modes = {"SAN": "SPECTRUM", "PNO": "SSA"}
    _options = {
        "B4": "Low-aging OCXO",
        "B10": "External Generator Control",
        "B18": "Removable Hard Disk",
        "B19": "Second Hard Disk",
        "B21": "LO/IF Ports for External Mixers",
        "B23": "20 dB Preamplifier",
        "B25": "Electronic Attenuator",
        "B28": "Trigger Port",
        "B60": "Low Phase Noise",
        "B61": "Correlation Extension",
        "K5": "GSM/EDGE",
        "K8": "Bluetooth",
        "K9": "Power Sensor Measurements",
        "K30": "Noise Figure and Gain Measurements",
        "K70": "Vector Signal Analysis",
    }

    def __init__(self, visa):
        super().__init__(visa)
        self._visa.write("*CLS")
        self._visa.write("SYSTEM:ERROR:CLEAR:ALL")
        self._visa.write("*ESE 255")
        self._visa.write("FORMAT ASCII")
        self._idn = get_idn(visa)
        self._currentmode = self.mode
        if self._currentmode == "SPECTRUM":
            self.spectrum = SpecAn(self)
        else:
            self.ssa = SSA(self)
        self.status = Status(self)

    @property
    def model(self):
        """(str): the model number"""
        return self._idn.model

    @property
    def serial_number(self):
        """(str): the serial number"""
        return self._idn.serial_number

    @property
    def firmware_version(self):
        """(str): the firmware version"""
        return self._idn.firmware_version

    @property
    def mode(self):
        """value (str): {SPECTRUM, SSA}"""
        result = self._visa.query("INSTRUMENT?")
        return Fsup._modes.get(result, result)

    @mode.setter
    @validate
    def mode(self, value):
        modes = dict((v, k) for k, v in Fsup._modes.items())
        if value in modes and value != self._currentmode:
            original_timeout = self._visa.timeout
            self._visa.timeout = 5000  # ms
            if self._currentmode == "SPECTRUM":
                del self.spectrum
            else:
                del self.ssa
            self._currentmode = value
            new_mode = modes[value]
            self._visa.write(f"INSTRUMENT:SELECT {new_mode}")
            if self._currentmode == "SPECTRUM":
                self.spectrum = SpecAn(self)
            else:
                self.ssa = SSA(self)
            self._visa.timeout = original_timeout

    def reset(self):
        """Reset the instrument to the factory default settings"""
        self._visa.write("*RST")

    def set_clock(self):
        """Set the date and time to local machine's time"""
        self._visa.write(f"SYSTEM:DATE {datetime.now().strftime('%Y,%m,%d')}")
        self._visa.write(f"SYSTEM:TIME {datetime.now().strftime('%H,%M,%S')}")

    @property
    def time(self):
        """Return system time"""
        get = lambda x: [int(s) for s in self._visa.query(f"SYSTEM:{x}?").split(",")]
        return datetime(*(get("DATE") + get("TIME"))).isoformat()

    def lock_frontpanel(self):
        """Lock the front panel"""
        self._visa.write("SYSTEM:DISPLAY:FPANEL OFF")
        self._visa.write("SYSTEM:KLOCK ON")

    def unlock_frontpanel(self):
        """Unlock the front panel"""
        self._visa.write("SYSTEM:KLOCK OFF")
        self._visa.write("SYSTEM:DISPLAY:FPANEL ON")

    @property
    def options(self):
        """List the installed options"""
        codes = self._visa.query("*OPT?").split(",")
        installed_codes = [code for code in codes if not code.startswith("0")]
        return [Fsup._options.get(code, code) for code in installed_codes]

    @property
    def impedance(self):
        """value (int): RF input impedance {50, 75} Ω"""
        return int(self._visa.query("INPUT:IMPEDANCE?"))

    @impedance.setter
    @validate
    def impedance(self, value):
        self._visa.write(f"INPUT:IMPEDANCE {value}")

    def __repr__(self):
        return f"<R&S {self.model} at {self._visa.resource_name}>"
