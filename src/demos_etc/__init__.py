def CalculateStepSize(
    PixelsPerStep=370, XOverlap=40, YOverlap=40, XWidth=640, YHeight=480
):
    # returns correct amount to move X and Y for desired amount of overlap and pixel size.
    # Step in PixelsPerStep can refer to literal steps or just mm. mm easier
    # overlap in percent

    XSteps = round(
        XWidth / PixelsPerStep - (((XOverlap / 100) * XWidth) / PixelsPerStep), 3
    )
    YSteps = round(
        YHeight / PixelsPerStep - (((YOverlap / 100) * YHeight) / PixelsPerStep), 3
    )

    return XSteps, YSteps


def FocusDemo(cap):
    # Tinyscopecap is first camera with built in autofocus
    # turns out it's really easy to alter with opencv
    # this is just so I don't forget the commands

    cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)

    for i in range(5):
        for i in range(0, 255, 5):
            cap.set(cv2.CAP_PROP_FOCUS, i)
        for i in range(255, 0, -5):
            cap.set(cv2.CAP_PROP_FOCUS, i)
