import cv2


class Camera:
    def __init__(self, camera_index):
        self.cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
        # We use cv2.CAP_DSHOW to remove this oddball warning when iterating resolutions.
        # https://answers.opencv.org/question/234933/opencv-440modulesvideoiosrccap_msmfcpp-682-cvcapture_msmfinitstream-failed-to-set-mediatype-stream-0-640x480-30-mfvideoformat_rgb24unsupported-media/
        self.setResolution()
        self.takePicture()

    def setResolution(self, resolution=(640, 480)) -> bool:
        if self.cap is not None:
            self.cap.set(3, resolution[0])
            self.cap.set(4, resolution[1])
            return True
        return False

    def getHighestResolution(self, setResolution=False) -> tuple:
        """
        This function uses the highest resolution example for OpenCV that seems to
        work somewhat reliably and wraps it into a single doohickey to use.  Should be pretty ok?

        https://stackoverflow.com/a/64444072
        """
        HIGH_VALUE = 10000
        WIDTH = HIGH_VALUE
        HEIGHT = HIGH_VALUE

        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
        width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # We only set resolution if it's used.  It is not intended to be used.
        if setResolution:
            self.setResolution((width, height))

        return (width, height)

    # This is to mirror the equivalent stub in the singlefile.
    def takePicture(self):
        ret, frame = self.cap.read()
        return frame

    def closeCamera(self):
        self.cap.release()
