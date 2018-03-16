from serial import Serial
from time   import time

class Sonar:
    """
    A class used to obtain measurements from two sonar devices over serial.

    Attributes:
        timeout (int):      Number of seconds to wait for sonar data
        buffer_size (int):  Number of data samples to buffer and average
        unit (str):         The desired unit of the outputted measurements
        upper_bound (int):  Any sample above this (in mm) is discarded
        threshold (float):  In a buffer of samples, only samples within this
                            proportion of their average are kept
    """

    def __init__(self, device="/dev/ttyAMA0", timeout=3, buffer_size=3,
                 unit="mm", upper_bound=4500, threshold=0.2):
        """
        Constructs a Sonar object using a series of overridable default params.

        Keyword Arguments:
            device (str):       Name of the serial device being read.
            timeout (int):      Number of seconds to wait for sonar data
            buffer_size (int):  Number of data samples to buffer and average
            unit (str):         The desired unit of the outputted measurements
            upper_bound (int):  Any sample above this (in mm) is discarded
            threshold (float):  In a buffer of samples, only samples within this
                                proportion of their average are kept
        """

        # Open port at 9600 Baud, 8 data bits, no parity bit, and one stop bit.
        self._serial = Serial(device, 9600, 8, 'N', 1, timeout=timeout)

        # Initialize class attributes.
        self.timeout = timeout
        self._l_start = b'L'
        self._r_start = b'R'
        self.buffer_size = 3
        if unit.lower() in ["mm", "millimeter", "millimeters"]:
            self.unit = "mm"
        elif unit.lower() in ["cm", "centimeter", "centimeters"]:
            self.unit = "cm"
        elif unit.lower() in ["m", "meter", "meters"]:
            self.unit = "m"
        elif unit.lower() in ["in", "in.", "inch", "inches"]:
            self.unit = "in"
        elif unit.lower() in ["ft", "ft.", "foot", "feet"]:
            self.unit = "ft"
        else:
            raise Exception("Invalid unit")
        self.upper_bound = upper_bound
        self.threshold = threshold
        self._next_sonar = b''
        self._read_first = False

        # Creates two buffers, one for each sonar.
        self._buffers = {self._l_start: [], self._r_start: []}

        # Holds conversion ratios from millimeters to other units.
        self._conversions = { "mm": 1.0,
                              "cm": 10.0,
                               "m": 1000.0,
                              "in": 25.4,
                              "ft": 304.8 }

    def sample(self):
        """
        Gets a single sample from one of the sonars without averaging.

        Returns:
            sample (int):       Measurement in millimeters
            which_sonar (str):  Indicator string for the sample's sonar
        """

        end_time = time() + self.timeout

        # Tries to acquire serial data until timeout is reached.
        while time() < end_time:
            # Initialize loop variables.
            bytes = b''
            which_sonar = self._next_sonar
  
            # Keep reading bytes until we see a sonar indicator.
            byte = self._serial.read()
            while byte not in [self._l_start, self._r_start]:
                bytes += byte
                byte = self._serial.read()

            # The read sonar indicator is for the next value.
            self._next_sonar = byte

            # First sample may be malformed, skip it.
            if not self._read_first:
                self._read_first = True
                continue

            # Decode and convert the bytes, skip the sample if we can't.
            try:
                sample = int(bytes.decode())
            except:
                continue

            # Return measurement and sonar indicator if within threshold.
            if sample > self.upper_bound:
                continue
            return sample, which_sonar

        # Closes the serial port and raises exception if timeout is reached.
        self._serial.close()
        raise RuntimeError("Expected serial data not received")

    def _convert(self, value):
        """Converts a value in millimeters to the Sonar's specified unit."""
        return value / self._conversions[self.unit]

    def measure(self):
        """
        Get an averaged measurement from a sonar with outliers removed.

        Returns:
            result (float):     Measurement in desired unit
            which_sonar (str):  Indicator string for the measurement's sonar
        """

        # Reads samples until a measurement is generated.
        while True:
            # Get a sample and add it to the corresponding buffer.
            sample, which_sonar = self.sample()
            self._buffers[which_sonar].append(sample)

            # If the buffer is full, try to generate a measurement.
            buffer_len = len(self._buffers[which_sonar])
            if buffer_len >= self.buffer_size:
                avg = sum(self._buffers[which_sonar]) / float(buffer_len)

                # Discard outliers.
                for x in self._buffers[which_sonar]:
                    if abs(x - avg) > (avg * self.threshold):
                        self._buffers[which_sonar].remove(x)
                        buffer_len -= 1

                # Average the remaining samples and convert the result.
                if buffer_len > 0:
                    result = sum(self._buffers[which_sonar]) / float(buffer_len)
                    if self.unit != "mm":
                        result = self._convert(result)
                    self._buffers[which_sonar] = [] # Clear buffer
                    return result, which_sonar

    def _pretty_print(self, value, which_sonar):
        """
        Pretty prints a value/sonar pair.

        Arguments:
            value (float):          The measurement to be printed
            which_sonar (bytes):    Bytestring indicator for the sonar device
        """
        print(which_sonar.decode() + ":", "{0:.2f}".format(value).rjust(7))

    def pretty_sample(self):
        """Pretty prints a sample."""
        self._pretty_print(*self.sample())

    def pretty_measure(self):
        """Pretty prints a measurement."""
        self._pretty_print(*self.measure())

    def __del__(self):
        """Destructor for Sonar simply closes its serial port if open."""
        if hasattr(self, "_serial") and self._serial.is_open:
            self._serial.close()
