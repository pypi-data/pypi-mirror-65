"""Mass Memory subsystem"""
import array
import pathlib
import time
from rsfsup.common import Subsystem, validate


class MassMemory(Subsystem, kind="Mass Memory"):
    """Mass memory subsystem

    Attributes:
        instr (Fsup)
    """

    @staticmethod
    def process_catalog(cat):
        """Process comma separated q-string files into a list

        Parameters:
            cat (str): comma separated q-string files
        """
        cat = cat.replace("'", "")
        return cat.split(",")

    @property
    def drive(self):
        """value (str): {D, F}"""
        res = self._visa.query("MMEMORY:MSIS?")
        return res.replace("'", "")

    @drive.setter
    @validate
    def drive(self, value):
        self._visa.write(f"MMEMORY:MSIS '{value}:'")

    @property
    def directory(self):
        """value (str): directory, e.g. 'D:\\USER'"""
        res = self._visa.query("MMEMORY:CDIRECTORY?")
        return res.replace("'", "")

    @directory.setter
    @validate
    def directory(self, value):
        self._visa.write(f"MMEMORY:CDIRECTORY '{value}'")

    @property
    def file_listing(self):
        """(list): list of files in current directory"""
        cat = self._visa.query("MMEMORY:CATALOG?")
        return MassMemory.process_catalog(cat)

    def get(self, source, destination=None):
        """Get the source file and save at destination

        Transfers the source file raw bytes to the control computer as unsigned
        8-bit integers.

        Parameters:
            source (str): file to retrieve from the instrument
            destination (str): path and file name to save on control computer
        """
        qstr = f"MMEMORY:DATA? '{source}'"
        raw_bytes = self._visa.query_binary_values(qstr, datatype="B")
        if destination is None:
            return raw_bytes
        with open(destination, "wb") as f:
            raw_array = array.array("B")
            raw_array.fromlist(raw_bytes)
            f.write(raw_array)
        return None

    def put(self, source, destination):
        """Put the source file on the instrument at destination

        Parameters:
            source (str): file on control computer
            destination (str): path and file name to save on the instrument
        """
        with open(source, "rb") as f:
            file_bytes = f.read()
        destination = pathlib.PurePath(destination)
        if destination.is_absolute():
            self.drive = destination.drive
            self.directory = str(destination.parent)
        else:
            self.drive = "D:"
        prefix = f"MMEMORY:DATA '{destination}',#{len(str(len(file_bytes)))}{len(file_bytes)}"
        prefix = prefix.encode("utf-8")
        suffix = "; *OPC".encode("utf-8")
        self._visa.write("*CLS")
        self._visa.write_raw(prefix + file_bytes + suffix)
        while not self._visa.stb & 32:
            time.sleep(1)
        if self._visa.stb & 4:
            err = self._visa.query("SYSTEM:ERROR?")
            raise ValueError(err)

    def delete(self, file):
        """Delete file

        Parameters:
            file (str): file to delete
        """
        self._visa.write("*CLS")
        self._visa.write(f"MMEMORY:DELETE '{file}'; *OPC")
        while not self._visa.stb & 32:
            time.sleep(1)
        if self._visa.stb & 4:
            err = self._visa.query("SYSTEM:ERROR?")
            raise ValueError(err)
