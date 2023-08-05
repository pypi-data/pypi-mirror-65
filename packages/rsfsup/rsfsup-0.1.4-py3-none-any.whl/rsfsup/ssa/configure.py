"""Phase noise measurement configuration"""
from rsfsup.common import Subsystem, validate, scale_frequency


class Configure(Subsystem, kind="Phase Noise Configuration"):
    """Phase noise configuration

    Constraints:
        Automatic preamplifier and attenuator control turned ON
        Automatic Frequency Control (AFC) turned OFF
        Automatic frequency and level verification turned ON
        Optimize cross-correlation if option present
        Automatic configuration of the internal VCO & PLL settings
        Suppress all spurs

    Attributes:
        instr (Fsup)
    """

    _testsetups = {
        "INT1": "Default PLL mode using internal generator, phase detector and control",
        "INT3": "Cross-correlation using internal generator, phase detector and control",
    }
    _search_bands = [
        "1 MHz to 10 MHz",
        "10 MHz to 50 MHz",
        "50 MHz to 8 GHz",
        "8 GHz to 26.5 GHz",
        "26.5 GHz to 50 GHz",
    ]

    def __init__(self, instr):
        super().__init__(instr)
        self._visa.write("INPUT:GAIN:AUTO ON")
        self._visa.write("FREQUENCY:TRACK OFF")
        self._visa.write("FREQUENCY:VERIFY:STATE ON")
        self._visa.write("SWEEP:XOPTIMIZE ON")
        self._visa.write("VCO:CSEARCH:AUTO ON")
        self._visa.write("VCO:LOOP:BWIDTH:AUTO ON")
        self._visa.write("VCO:PDETECTOR:PREMEAS:STATE ON")
        self._visa.write("VCO:PREMEAS:STATE ON")
        self._visa.write("SPURS:HIGHLIGHT:STATE OFF")
        self._visa.write("SPURS:SUPPRESS ALL")

    @property
    def test_setup(self):
        """value (str): {INT1, INT3}"""
        ts = self._visa.query("CONFIGURE:TSETUP?")
        return f"{ts}: {Configure._testsetups[ts]}"

    @test_setup.setter
    @validate
    def test_setup(self, value):
        self._visa.write(f"CONFIGURE:TSETUP {value}")

    @property
    def rf_level_detection(self):
        """value (str): {AUTO, MANUAL}"""
        auto_result = int(self._visa.query("CONFIGURE:POWER:AUTO?"))
        if auto_result:
            detection_mode = "AUTO"
        else:
            detection_mode = "MANUAL"
        return detection_mode

    @rf_level_detection.setter
    @validate
    def rf_level_detection(self, value):
        if value == "MANUAL":
            self._visa.write("CONFIGURE:POWER:AUTO OFF")
        else:
            self._visa.write("CONFIGURE:POWER:AUTO ON")

    @property
    def expected_rf_level(self):
        """value (float, str): -100 dBm to 30 dBm"""
        return float(self._visa.query("CONFIGURE:POWER:EXPECTED:RF?"))

    @expected_rf_level.setter
    @validate
    def expected_rf_level(self, value):
        self._visa.write(f"CONFIGURE:POWER:EXPECTED:RF {value}")

    @property
    def start_frequency(self):
        """value (int, str): start frequency in hertz in discrete 1, 3 steps"""
        value = int(self._visa.query("FREQUENCY:START?"))
        return scale_frequency(value)

    @start_frequency.setter
    @validate
    def start_frequency(self, value):
        self._visa.write(f"FREQUENCY:START {value}")

    @property
    def stop_frequency(self):
        """value (int, str): stop frequency in hertz in discrete 1, 3 steps"""
        value = int(self._visa.query("FREQUENCY:STOP?"))
        return scale_frequency(value)

    @stop_frequency.setter
    @validate
    def stop_frequency(self, value):
        self._visa.write(f"FREQUENCY:STOP {value}")

    @property
    def yaxis_autoscale(self):
        """value (str): {ON, OFF, ONCE}"""
        return self._visa.query("DISPLAY:TRACE:Y:SCALE:AUTO?")

    @yaxis_autoscale.setter
    @validate
    def yaxis_autoscale(self, value):
        self._visa.write(f"DISPLAY:TRACE:Y:SCALE:AUTO {value}")

    @property
    def yaxis_top(self):
        """value (int, str): y-axis top in dBc/Hz"""
        return int(self._visa.query("DISPLAY:TRACE:Y:SCALE:RLEVEL?"))

    @yaxis_top.setter
    @validate
    def yaxis_top(self, value):
        self._visa.write(f"DISPLAY:TRACE:Y:SCALE:RLEVEL {value}")

    @property
    def yaxis_range(self):
        """value (int, str): y-axis top in dBc/Hz"""
        return int(self._visa.query("DISPLAY:TRACE:Y:SCALE?"))

    @yaxis_range.setter
    @validate
    def yaxis_range(self, value):
        self._visa.write(f"DISPLAY:TRACE:Y:SCALE {value}")

    @property
    def sweep_mode(self):
        """value (str): {FAST, NORMAL, AVERAGED}"""
        return self._visa.query("SWEEP:MODE?")

    @sweep_mode.setter
    @validate
    def sweep_mode(self, value):
        self._visa.write(f"SWEEP:MODE {value}")

    @property
    def sweep_count(self):
        """value (int): number of measurement sweeps"""
        return int(self._visa.query("SWEEP:COUNT?"))

    @sweep_count.setter
    @validate
    def sweep_count(self, value):
        self._visa.write(f"SWEEP:COUNT {value}")

    @property
    def measurement_time(self):
        """(float): estimated total measurement time in seconds"""
        return float(self._visa.query("SWEEP:TIME?"))

    @property
    def dut_type(self):
        """value (str): {AUTO, FRLP, SYNT, OCXO, XTAL}"""
        return self._visa.query("VCO:TYPE?")

    @dut_type.setter
    @validate
    def dut_type(self, value):
        self._visa.write(f"VCO:TYPE {value}")

    @property
    def frequency_search_bands(self):
        """value (int, str): {ALL, 2 to 4}"""
        bands = []
        for band in range(2, 5):
            state = int(self._visa.query(f"VCO:BAND{band}?"))
            if state:
                bands.append((band, Configure._search_bands[band - 1]))
        return bands

    @frequency_search_bands.setter
    @validate
    def frequency_search_bands(self, value):
        for band in range(2, 5):
            if value in (band, "ALL"):
                self._visa.write(f"VCO:BAND{band} ON")
            else:
                self._visa.write(f"VCO:BAND{band} OFF")
