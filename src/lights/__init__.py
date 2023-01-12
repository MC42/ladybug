import subprocess


class DinoLite:
    def __init__(self):
        """This class is responsible for the interface to the DinoLite Camera module described in other parts of the project.

        uses dinolite windows batch file to control settings on EDGE plus model.
        FLCLevel: 1-6 brightness, if  0 convert to LED off
        FLCSwitch: control quadrants, value is 1111, 1010...
        AE on
        AE off (locks current exposure value)
        EV: sets exposure values 16-220, strange behavior
        """
        pass

    def control(self, setting):
        if "FLCLevel" in setting:
            subprocess.call(
                "DN_DS_Ctrl.exe LED ON"
            )  # can't change FLC if it's already off
            if "0" in setting:
                setting = "LED off"

        subprocess.call("DN_DS_Ctrl.exe " + setting)
