from src.camera import Camera
from src.storage import FileStore
from src.motion import MotionSystem

fs = FileStore()
fs.loadConfigFile()

motion = MotionSystem(fs.config_file["serial_port"], fs.config_file["baud_rate"])
camera = Camera(0)

motion.homeAxes()

# It seems that M211 doesn't properly report the bed area,
# as that can be changed at runtime.  The commit from 2017
# for Marlin shows it as DOA in essence.  Drats.

# The bodge is to have the machine go to it's limits ,and use
#  what it says it's position is once it's there.  Great.

import time
time.sleep(60)
