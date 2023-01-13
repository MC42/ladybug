from src.camera import Camera
from src.storage import FileStore
from src.motion import MarlinMotion

fs = FileStore()
fs.loadConfigFile()

motion = MarlinMotion(fs.config_file["serial_port"], fs.config_file["baud_rate"])
camera = Camera(0)

motion.homeAxes()
motion.waitForOk()

# It seems that M211 doesn't properly report the bed area,
# as that can be changed at runtime.  The commit from 2017
# for Marlin shows it as DOA in essence.  Drats.

# The bodge is to have the machine go to it's limits ,and use
#  what it says it's position is once it's there.  Great.

motion.deriveDimensions()
import time

# Calibration Steps
# Get Machine Dimensions -> Store in config.json
# verify camera ID -> store in config.json
# place object under lens / move to / around
# Autofocus to find focal areas / stacked (like we already do)
# Capture more frames than we normally need to try and improve quality of calibration stuff and producing the watermark.
# Produce "watermark" to remove lens dirt, etc.
# SIFT / RANSAC to undistort camera lens (hopefully?)
# Store camera lens calibration
# Also produce MM/px with known size object(s).

time.sleep(60)
