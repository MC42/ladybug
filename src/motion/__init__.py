class MotionSystem:
    def __init__(self):
        pass

    def sendGCode(self, command):
        pass

    def moveX(self, distance_mm):
        pass

    def moveY(self, distance_mm):
        pass

    def moveZ(self, distance_mm):
        pass

    def homeX(self):
        pass

    def homeY(self):
        pass

    def homeZ(self):
        pass

    def homeAxes(self):
        self.homeX()
        self.homeY()
        self.homeZ()