import time
import serial

class MotionSystem:
    def __init__(self, serial_port, baud):
        self.serial_port_info = serial_port
        self.baud = baud

        self.serial_port = serial.Serial(self.serial_port_info, self.baud, timeout=1)
        time.sleep(4)
        if not self.serial_port.is_open:
            self.restart_serial()

        self.sendGCode(
        "M84 S36000"
    )  # tells it not to turn off motors for S seconds (default 60 grr)
        self.sendGCode("M302 P1", wait=True)  # prevents errors from 'cold' extrusion
        self.sendGCode("M203 Z5", wait=True)  # lets z go a bit faster. disabled if using weak nano motor
        self.sendGCode("M17", wait=True)  # engage steppers

        while self.has_data_waiting():
            self.serial_port.readline()

    def sendGCode(self, command, wait=False):
        if not self.serial_port.is_open:
            self.restart_serial()

        command += " /r\n"
        bytes_gcode = command.encode("utf-8")
        self.serial_port.write(bytes_gcode)

        if wait:
            self.waitForOk()

    def setFan(self, speed:int = 0) -> None:
        self.sendGCode(f"M106 S{speed}", True)

    def moveX(self, distance_mm):
        pass

    def moveY(self, distance_mm):
        pass

    def moveZ(self, distance_mm):
        pass

    def homeX(self):
        self.sendGCode("G28 X;")

    def homeY(self):
        self.sendGCode("G28 Y;")

    def homeZ(self):
        self.sendGCode("G28 Z;")

    def homeAxes(self):
        self.sendGCode("G28;")

    def close_serial(self):
        self.serial_port.close()

    def waitForOk(self) -> None:
        """Experimental stub to permit blocking calls in other parts of the code
        rather than arbitrary code calls.  In theory, all calls to Marlin should
        return an 'ok\n' when done."""
        while True:
            time.sleep(0.01)
            temp_string = self.serial_port.readline()
            print(temp_string)
            if "ok" in temp_string.decode("utf-8").strip():
                break

    def has_data_waiting(self) -> bool:
        return self.serial_port.in_waiting > 0

    def restart_serial(self):
        PossibleBauds = [115200]  # expand as more options are known
        try:
            self.close_serial()  # will pass if no port by ladybug name open
        except AttributeError:  # if LadyBug turned out to be a nonetype
            pass

        if self.port != -1 and self.baud != -1:  # try given parameters first
            while True:
                time.sleep(0.01)
                try:
                    self.serial_port = serial.Serial(
                        self.serial_port_info, self.baud, timeout=1
                    )
                    print("trying to connect with serial module.")
                    time.sleep(
                        5
                    )  # this 5 instead of 1 represents 3 hours of frustration
                    if self.serial_port.isOpen():
                        return

                except:
                    pass
