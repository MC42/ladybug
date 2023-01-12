def RemoveBlank(image):
    # https://stackoverflow.com/questions/13538748/crop-black-edges-with-opencv
    # Expensively removes black/blank boundaries of large image

    if len(image.shape) == 2:  # quick fix for 2D images
        y_nonzero, x_nonzero = np.nonzero(image)
    else:
        y_nonzero, x_nonzero, _ = np.nonzero(image)
    return image[
        np.min(y_nonzero) : np.max(y_nonzero), np.min(x_nonzero) : np.max(x_nonzero)
    ]


def coin_CalculateBlur(frame):
    blur = cv2.Laplacian(frame, cv2.CV_64F).var()
    return blur


def ConvertPixelToXY(XPix, YPix, PixelsPerMM=370, debug=True):
    # convert pixel to NEAREST 0.1 XY locations.
    # Returns XY location and REAL XPix and YPix gone to
    RawXPos = XPix / PixelsPerMM
    RawYPos = YPix / PixelsPerMM

    NearestXPos = round(RawXPos, 1)  # round to 0.1 MM
    NearestYPos = round(RawYPos, 1)

    NearestXPix = round(NearestXPos * PixelsPerMM, 2)  # will be float
    NearestYPix = round(NearestYPos * PixelsPerMM, 2)

    if debug:
        print(
            """At desired XPix {} and desired YPix {},
    The closest X mm is: {} and the Closest Y mm is: {},
    which corresponds to XPixel {} and YPixel {}""".format(
                XPix, YPix, NearestXPos, NearestYPos, NearestXPix, NearestYPix
            )
        )
    return (NearestXPos, NearestYPos, NearestXPix, NearestYPix)
