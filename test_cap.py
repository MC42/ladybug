from src.camera import Camera
from src.motion import MarlinMotion
from src.camera.imaging import averageFrames
from src.motion.units import marlinFormat
from numpy import round, arange as better_range
import cv2

import time
from tqdm import tqdm

cam = Camera(2)
motion = MarlinMotion("COM8", 115200)


# Parse the M503 output to try and get the Z steps per mm for height so we can request single step moves.
value = motion.sendGCode("M503;")
value = [x.decode("utf8") for x in value]
value = [x for x in value if "M92" in x]
value = value[0]
value = value.split(" ")
value = [x for x in value if x.startswith("Z")][0]
value = value.replace("Z", "")
value = float(value)

minimumMotionUnitZ = averageFrames(1 / value)

# We give the range function a more useful name here to avoid confusion and larger-scale pollution of the namespace.  Lots of named things.

### Alignment stack should probably use SIFT or FAST.
### SIFT is definitely out of patent (https://patents.google.com/patent/US6711293B1/en / 2020-03-06)
### FAST doesn't seem to be patented at all?
### Lots of papers and patents seem to cite it, but don't use it independently.  May be worth comparing down the line & benchmarking.
### ORB seems solid: https://computer-vision-talks.com/2011-07-13-comparison-of-the-opencv-feature-detection-algorithms/
### SIFT taking 450ms+ isn't ideal, soooo....

for stepcount in tqdm(better_range(0.0, 6.0, marlinFormat(minimumMotionUnitZ * 5))):
    motion.sendGCode(f"G0 Z{stepcount}")
    frames = cam.takeNPictures(12)

    frames = [averageFrames(frames[7:])]

    for frameno, framerly in enumerate(frames):
        if not cv2.imwrite(f"./temp/stp_{round(stepcount,4)}.jpg", framerly):
            print("Error, couldn't save.")

    print(f"Step height done:\t{marlinFormat(stepcount)}")
