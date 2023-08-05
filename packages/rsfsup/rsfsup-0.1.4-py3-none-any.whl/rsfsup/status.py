"""Status reporting system"""
from rsfsup.common import Subsystem

STB = [
    None,
    None,
    "Error queue not empty",
    "Questionable status register sum bit",
    "MAV, message available",
    "ESB, event status sum bit",
    "MSS, master status summary",
    "Operation status register sum bit",
]

ESR = [
    "Operation complete",
    None,
    "Query error",
    "Device-dependent error",
    "Execution error",
    "Command error",
    "User request (LOCAL)",
    "Power on",
]

OPER = [
    "Calibrating",
    None,
    None,
    None,
    "Measuring phase noise",
    None,
    None,
    None,
    "Hardcopy in progress",
    None,
    None,
    None,
    None,
    None,
    None,
    None,
]

QUES = [
    None,
    None,
    None,
    "RF power",
    None,
    "Frequency",
    None,
    "Low phase noise board",
    "Calibration",
    "Limit",
    "Margin",
    None,
    "Adjacent channel power",
    "Phase noise",
    "DC or phase noise board",
    None,
]

POW = [
    "RF input overload, screen A",
    "RF input underload, screen A",
    "IF path overload, screen A",
    "RF or IF overload occured during AVERAGE or MAX/MINHOLD, screen A",
    None,
    None,
    None,
    None,
    "RF input overload, screen B",
    "RF input underload, screen B",
    "IF path overload, screen B",
    "RF or IF overload occured during AVERAGE or MAX/MINHOLD, screen B",
    None,
    None,
    None,
    None,
]

LPN = 4 * [None] + ["PLL unlock"] + 11 * [None]

PNO = [
    "Invalid DC switching sequence",
    "Signal not found",
    "Verify signal failed",
    "Beat note not found",
    "Beat note level too low",
    "Reference frequency out of range",
    None,
    "Power to the DUT is disabled or disconnected",
    "No traces",
    "Automatic frequency control error",
] + 6 * [None]

DCPN = (
    [
        "Temperature of DC board too high",
        "Current Vcc1 too high",
        "Current Vcc2 too high",
        "Current Vaux too high",
        "Current Vtune1 too high",
        "Current Vtune2 too high",
        "Vtune1 above Vmax",
        "Vtune2 above Vmax",
    ]
    + 3 * [None]
    + ["PLL loop unlock"]
    + 4 * [None]
)


def decode_register(register, value):
    """Decode decimal value for register

    Attributes:
        register (list): list of bit descriptions
        value (int): 0 to 255

    Returns:
        list of descriptions of bits that are set
    """
    set_bits = []
    for bit_description in register:
        if value & 1:
            if bit_description is not None:
                set_bits.append(bit_description)
        value = value >> 1
    return set_bits


class Status(Subsystem, kind="Status"):
    """Status reporting system

    Attributes:
        instr (Fsup)
    """

    def clear(self):
        """Clear status reporting system (*CLS)"""
        self._visa.write("*CLS")
        self._visa.write("SYSTEM:ERROR:CLEAR:ALL")

    @property
    def status_byte(self):
        """Query Status Byte (*STB) register

        Returns tuple of integer value and descriptions for bits that are set
        """
        value = self._visa.stb
        set_bits = decode_register(STB, value)
        return (value, set_bits)

    @property
    def event_status(self):
        """Query Event Status register (*ESR)

        Returns tuple of integer value and descriptions for bits that are set
        """
        value = int(self._visa.query("*ESR?"))
        set_bits = decode_register(ESR, value)
        return (value, set_bits)

    @property
    def operation(self):
        """Query the Operation register - events

        Returns tuple of integer value and descriptions for bits that are set
        """
        value = int(self._visa.query("STATUS:OPERATION?"))
        set_bits = decode_register(OPER, value)
        return (value, set_bits)

    @property
    def questionable(self):
        """Query the Questionable register - events

        Returns tuple of integer value and descriptions for bits that are set
        """
        value = int(self._visa.query("STATUS:QUESTIONABLE?"))
        set_bits = decode_register(QUES, value)
        if value & 2 ** 3:
            sub_value = int(self._visa.query("STATUS:QUESTIONABLE:POWER?"))
            set_bits.append(decode_register(POW, sub_value))
        if value & 2 ** 7:
            sub_value = int(self._visa.query("STATUS:QUESTIONABLE:LPNOISE?"))
            set_bits.append(decode_register(LPN, sub_value))
        if value & 2 ** 13:
            sub_value = int(self._visa.query("STATUS:QUESTIONABLE:PNOISE?"))
            set_bits.append(decode_register(PNO, sub_value))
        if value & 2 ** 14:
            sub_value = int(self._visa.query("STATUS:QUESTIONABLE:DCPNOISE?"))
            set_bits.append(decode_register(DCPN, sub_value))
        return (value, set_bits)
