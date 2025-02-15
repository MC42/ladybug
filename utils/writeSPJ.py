"""

Writes SPJ project files which can be opened with Microsoft ICE. This is a stopgap until (hopefully) real-time image stitching with OpenCV.

Yujie

"""

import os
import argparse


def createSPJ(folder, outputFolder):
    global SPJ
    folderAboveName = os.path.basename(os.path.dirname(folder))
    folderName = os.path.basename(os.path.normpath(folder))
    SPJ = open(
        os.path.join(outputFolder, "R" + folderAboveName + "Z" + folderName + ".spj"),
        "x",
    )


def modifySPJ(folder, outputFolder, extension=".png"):
    # TODO: fix the errors while using os.walk in high directory. It will append the file in subdir onto dir
    global SPJ
    folderAboveName = os.path.basename(os.path.dirname(folder))
    folderName = os.path.basename(os.path.normpath(folder))
    SPJ = open(
        os.path.join(outputFolder, "R" + folderAboveName + "Z" + folderName + ".spj"),
        "w",
    )
    SPJ.write('<?xml version="1.0" encoding="utf-8"?>\n')
    SPJ.write(
        '<stitchProject version="2.0" cameraMotion="rigidScale" projection="perspective">\n'
    )
    SPJ.write("  <sourceImages>\n")
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(extension):
                SPJ.write('    <sourceImage filePath="')
                SPJ.write(os.path.join(folder, file))
                SPJ.write('" />\n')
    SPJ.write("  </sourceImages>\n")
    SPJ.write("</stitchProject>")


def main(rootFolder, outputFolder, extension):
    rawFolders = [x[0] for x in os.walk(rootFolder)]
    print(rawFolders)
    # f = open("hello.aio","x")
    for folder in rawFolders:
        if any(file.endswith(extension) for file in os.listdir(folder)):
            # print(folder)
            createSPJ(folder, outputFolder)
            modifySPJ(folder, outputFolder, extension)
            # f = open(, "x")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required=True, help="input folder")
    parser.add_argument("-o", "--output", required=True, help="output folder")
    parser.add_argument(
        "-e", "--extension", required=False, help="file extension without ."
    )
    args = vars(parser.parse_args())

    extension = ".png"
    if args["extension"]:
        extension = "." + args["extension"]

    rootFolder = args["input"]
    outputFolder = args["output"]

    main(rootFolder, outputFolder, extension)
