from serial.tools import list_ports


class ComScanner:

    def is_available(self, name):
        """Check if a serial port is available."""
        ports = self.scan()
        for port in ports:
            if port.device == name:
                return True
        return False

    def find_serial(self, name):
        """Check if a serial port is available."""
        ports = self.scan()
        for port in ports:
            if port.device == name:
                return port
        return None

    def scan(self):
        """Check if a serial port is available."""
        return list_ports.comports()