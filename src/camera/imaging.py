import cv2


def getVarianceOfLaplacian(image):
    """Produces a variance of laplacian transform, roughly analagous to the blur
    of a given image.  We can make use of this function to confirm that the camera
    is not signigifcantly shaking."""
    return cv2.Laplacian(image, cv2.CV_64F).var()


def averageFrames(images: list):
    """Takes in a list of frames (images) and produces a single numpy.ndarray() (image) with the combined average.

    Taken from here: https://leslietj.github.io/2020/06/28/How-to-Average-Images-Using-OpenCV/"""
    if len(images) == 0:
        raise Exception(
            "The length of frames fed in to the averageFrames stub cannot be less than 1 frame."
        )

    avg_image = images[0]
    for i in range(len(images)):
        if i == 0:
            pass
        else:
            alpha = 1.0 / (i + 1)
            beta = 1.0 - alpha
            avg_image = cv2.addWeighted(images[i], alpha, avg_image, beta, 0.0)

    return avg_image


def stableFrames(images: list):

    raise NotImplementedError
