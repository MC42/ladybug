import time
import serial


class MarlinMotion:
    def __init__(self, serial_port, baud):
        self.serial_port_info = serial_port
        self.baud = baud

        self.serial_port = serial.Serial(self.serial_port_info, self.baud, timeout=None)

        # Sanity saver it seems.
        # Attempting to open a port does not render it immediately
        # avalible for use.  This may be a hassle but it's far easier
        # than dealing with the cross-platform errata of just... waiting.
        time.sleep(5)  

        if not self.serial_port.is_open:
            self.restart_serial()

        self.sendGCode(
            "M84 S36000;"
        )  # tells it not to turn off motors for S seconds (default 60 grr)
        self.sendGCode("M302 P1;", wait=True)  # prevents errors from 'cold' extrusion
        # self.sendGCode("M203 Z5;", wait=True)  # lets z go a bit faster. disabled if using weak nano motor
        self.sendGCode("M17;", wait=True)  # engage steppers

        # We explicitly set our units to millimeters here to avoid any potential coordinate
        # system mishaps.  Yay!
        self.sendGCode("M21;", wait=True)

        while self.has_data_waiting():
            self.serial_port.readline()

    def stripGCodeOutput(self, input) -> list:
        """
        This helper is here to remove extraneous returns from the percieved output of the microscope apparatus
        without impeding our ability to use it or debug it.  So it's stripped after calls.  This also means that 
        the "waitForOk" code could be hooked into a logging framework fairly easily.
        """
        
        return [
            x.decode("utf-8").strip()
            for x in input
            if x.decode("utf-8").strip() not in ["ok", "", "echo:busy: processing"]
        ]

    def sendGCode(self, command, wait=False) -> list:
        if not self.serial_port.is_open:
            self.restart_serial()

        command += " /r\n"
        bytes_gcode = command.encode("utf-8")
        self.serial_port.write(bytes_gcode)

        returned_lines = []
        if wait:
            returned_lines = self.waitForOk()

        return returned_lines

    def setFan(self, speed: int = 0) -> None:
        self.sendGCode(f"M106 S{speed};", True)

    def moveX(self, distance_mm):
        pass

    def moveY(self, distance_mm):
        pass

    def moveZ(self, distance_mm):
        pass

    def homeX(self):
        self.sendGCode("G28 X;", wait=True)

    def homeY(self):
        self.sendGCode("G28 Y;", wait=True)

    def homeZ(self):
        self.sendGCode("G28 Z;", wait=True)

    def homeAxes(self):
        self.sendGCode("G28;", wait=True)

    def close_serial(self):
        self.serial_port.close()

    def waitForOk(self) -> list:
        """Experimental stub to permit blocking calls in other parts of the code
        rather than arbitrary code calls.  In theory, all calls to Marlin should
        return an 'ok\n' when done."""

        returned_lines = []

        while True:
            temp_string = self.serial_port.readline()
            print(temp_string)
            returned_lines.append(temp_string)
            if temp_string.decode("utf-8").strip() == "ok":
                return returned_lines

    def has_data_waiting(self) -> bool:
        return self.serial_port.in_waiting > 0

    def restart_serial(self):
        try:
            self.close_serial()
        except AttributeError:
            pass

        if self.port != -1 and self.baud != -1:  # try given parameters first
            while True:
                try:
                    self.serial_port = serial.Serial(
                        self.serial_port_info, self.baud, timeout=None
                    )
                    print("trying to connect with serial module.")
                    if self.serial_port.isOpen():
                        return

                except:
                    pass

    def get_location(self):
        """
        This functions tells us where we are in approximately real time
        per the Marlin docs.  It may be imperfect, and should only be used
        at stop _anyways_.

        TODO: Figure out how to detect stops.

        https://marlinfw.org/docs/gcode/M114.html"""

        returndat = self.sendGCode("M114 D;", wait=True)
        returndat = self.stripGCodeOutput(returndat)

        print(returndat)

    def deriveDimensions(self):
        """
        For the time being we can make the assumption that soft limits
        are enabled on our CNC devices and as such we can use it to infer
        the maximum movement area of the scanner and work around that.
        """

        returndat = self.stripGCodeOutput(self.sendGCode("M211;", wait=True))
        print(returndat)

        print("EOF")
