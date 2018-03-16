from serial import Serial
from time   import time

class Sonar:
    """
    A class used to obtain measurements from two sonar devices over serial.

    Attributes:
        timeout (int):      Number of seconds to wait for sonar data
        l_start (str):      Indicates the start of left sonar data
        r_start (str):      Indicates the start of right sonar data
        buffer_size (int):  Number of data samples to buffer and average
        unit (str):         The desired unit of the outputted measurements
        upper_bound (int):  Any sample above this (in mm) is discarded
        threshold (float):  In a buffer of samples, only samples within this
                            proportion of their average are kept
    """

    def __init__(self, device="dev/ttmyAMA0", timeout=3, l_start='L',
                 r_start='R', buffer_size=3, unit="mm", upper_bound=4500, 
                 threshold=0.1):
        """
        Constructs a Sonar object using a series of overridable default params.

        Keyword Arguments:
            device (str):       Name of the serial device being read.
            timeout (int):      Number of seconds to wait for sonar data
            l_start (str):      Indicates the start of left sonar data
            r_start (str):      Indicates the start of right sonar data
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
        self.l_start = l_start
        self.r_start = r_start
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

        # Creates two buffers, one for each sonar.
        self._buffers = {l_start: [], r_start: []}

        # Holds conversion ratios from millimeters to other units.
        self._conversions = { "mm": 1.0,
                              "cm": 10.0,
                              "m":  1000.0,
                              "in": 25.4,
                              "ft": 304.8 }

    def get_sample(self):
        """
        Gets a single sample from one of the sonars without averaging.

        Returns:
            sample (int):       Measurement in millimeters
            which_sonar (str):  Indicator string for the sample's sonar
        """

        start_time = time()

        # Tries to acquire serial data until timeout is reached.
        while time() < start_time + self.timeout:
            if self._serial.inWaiting():
                bytes_to_read = self._serial.inWaiting()

                # Read the sample and decode it, skip it if we can't.
                try:
                    sample = self._serial.read(bytes_to_read).decode()
                except:
                    continue

                # Store the indicator string, skip if none found.
                if sample.startswith(self.l_start):
                    which_sonar = self.l_start
                elif sample.startwith(self.r_start):
                    which_sonar = self.r_start
                else:
                    continue

                # Strip the indicator string and convert, skip it if we can't.
                try:
                    sample = int(sample.lstrip(which_sonar))
                except:
                    continue

                # Return measurement and sonar indicator if within threshold.
                if sample > self.upper_bound:
                    continue
                return sample, which_sonar

        # Closes the serial port and raises exception if timeout is reached.
        self._serial.close()
        raise RuntimeError("Expected serial data not received")

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
            sample, which_sonar = self.get_sample()
            self._buffers[which_sonar].append(sample)

            buffer_length = float(len(self._buffers[which_sonar]))

            # If the buffer is full, try to generate a measurement.      
            if buffer_length >= self.buffer_size:
                avg = sum(self._buffers[which_sonar]) / buffer_length

                # Discard outliers.
                for x in self._buffers[which_sonar]:
                    if abs(x - avg) > (avg * self.threshold):
                        self._buffers[which_sonar].remove(x)

                buffer_length = float(len(self._buffers[which_sonar]))

                # Average, convert, and return the remaining samples.
                if buffer_length > 0:
                    result = sum(self._buffers[which_sonar]) / buffer_length
                    if self.unit != "mm":
                        result = self._convert(result)
                    return result, which_sonar

    def _convert(self, value):
        """Converts a value in millimeters to the Sonar's specified unit."""
        return value / self._conversions[self.unit]

    def __del__(self):
        """Destructor for Sonar simply closes its serial port."""
        self._serial.close()
