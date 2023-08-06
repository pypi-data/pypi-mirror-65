import enum
import logging
import sys

import serial
from serial import PARITY_EVEN, STOPBITS_ONE

from pyticcom.const import ADCO_DESCRIPTION, OPTARIF_DESCRIPTION, ISOUSC_DESCRIPTION, UNIT_A, UNIT_WH, UNIT_VA, UNIT_NONE, \
    BASE_DESCRIPTION, HCHC_DESCRIPTION, HCHP_DESCRIPTION, PTEC_DESCRIPTION, IINST_DESCRIPTION, IMAX_DESCRIPTION, \
    PAPP_DESCRIPTION, HHPHC_DESCRIPTION, MOTDETAT_DESCRIPTION

LOGGER = logging.getLogger(__name__)

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

class GroupInfo(enum.Enum):
    ADCO = (ADCO_DESCRIPTION)
    OPTARIF = (OPTARIF_DESCRIPTION)
    ISOUSC = (ISOUSC_DESCRIPTION, UNIT_A)
    BASE = (BASE_DESCRIPTION, UNIT_WH)
    HCHC = (HCHC_DESCRIPTION, UNIT_WH)
    HCHP = (HCHP_DESCRIPTION, UNIT_WH)
    PTEC = (PTEC_DESCRIPTION)
    IINST = (IINST_DESCRIPTION, UNIT_WH)
    IMAX = (IMAX_DESCRIPTION, UNIT_A)
    PAPP = (PAPP_DESCRIPTION, UNIT_VA)
    HHPHC = (HHPHC_DESCRIPTION)
    MOTDETAT = (MOTDETAT_DESCRIPTION)

    def __init__(self, description, unit = UNIT_NONE):
        self._description = description
        self._unit = unit

    @property
    def description(self):
        return self._description

    @property
    def unit(self):
        return self._unit

    @classmethod
    def from_str(cls, value):
        for m, mm in GroupInfo.__members__.items():
            if m == value.upper():
                return mm


class Mode(enum.Enum):
    STANDARD = 1
    HISTORY = 2


class Group:

    def __init__(self, info, value, checksum):
        self.info = info
        self.value = value
        self.checksum = checksum

    def __repr__(self):
        return "TeleinfoGroup(name=%s, value=%s, checksum=%s)" % (self.info.name, self.value, self.checksum)


class Frame:

    def __init__(self):
        """Initialize TeleinfoFrame."""
        self.groups = []

    def get(self, group_info:GroupInfo):
        """Get group by label."""
        for group in self.groups:
            if group.info == group_info:
                return group
        return None

    def add_group(self, name, value, checksum):
        """Add group"""
        group_info = GroupInfo.from_str(name)
        self.groups.append(Group(group_info, value, checksum))

    def __repr__(self):
        return ",".join([g.__repr__() for g in self.groups])


class Teleinfo:

    reader = None

    def __init__(self, port = "/dev/ttyUSB", mode:Mode = Mode.HISTORY, timeout=5):
        """Responsible to read TIC frame on serial port."""
        self.port = port
        self.mode = mode
        self.baud_rate = 1200 if mode == Mode.HISTORY else 9600
        self.timeout = timeout

    def _readline(self):
        """Readline from serial."""
        line = self.reader.readline()
        return line.replace(b'\r', b'').replace(b'\n', b'')

    def __wait_rcv_frame_start(self):
        """Wait for frame start."""
        line = self._readline()
        FRAME_START = b'\x02'
        while FRAME_START not in line:
            line = self._readline()

    def __process_history_frame(self):
        """Process history frame."""
        STE = b'\x03'
        frame = Frame()
        LOGGER.debug(u"New frame")
        line = self._readline()
        while STE not in line:
            LOGGER.debug("New group: %s", line)
            part_size = len(line.split())
            if part_size == 2:
                name, value = line.split()
                checksum = b' '
            elif part_size == 3:
                name, value, checksum = line.split()
            else:
                self.__process_history_frame()
                break

            if self.validate_checksum(line, checksum):
                frame.add_group(name.decode(), value.decode(), checksum.hex())
            else:
                LOGGER.warning("Frame corrupted. Waiting for a new one.")
                break
            line = self._readline()
        return frame

    def __process_frame(self):
        """Process frame."""
        if self.mode == Mode.STANDARD:
            raise NotImplemented()
        return self.__process_history_frame()

    async def read_frame(self):
        """Read a frame from serial port. """
        self.__wait_rcv_frame_start()
        frame = self.__process_frame()

        LOGGER.debug("Frame: %s", frame)
        return frame

    def validate_checksum(self, frame, checksum):
        """Check if a frame is valid."""
        datas = frame[:-2]
        computed_checksum = (sum(datas) & 0x3F) + 0x20
        if computed_checksum == ord(checksum):
            return True
        LOGGER.warning(u"Invalid checksum for %s : %s != %s", frame, computed_checksum, checksum)
        return False

    def open(self):
        """Open reader."""
        if self.reader is None:
            self.reader = serial.Serial(
                self.port,
                self.baud_rate,
                bytesize=7,
                parity=PARITY_EVEN,
                stopbits=STOPBITS_ONE,
                timeout=self.timeout
            )
        if not self.reader.isOpen():
            self.reader.open()

    def close(self):
        """Close reader."""
        if self.reader is not None and self.reader.isOpen():
            self.reader.close()

    def __enter__(self):
        """Open reader."""
        self.open()
        return self

    def __exit__(self, type, value, traceback):
        """Make sure reader is closed."""
        self.close()