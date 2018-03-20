from __future__ import print_function
from argparse import ArgumentParser, FileType
import extract_file_type
import EML
import os

__authors__ = ["Chapin Bryce", "Preston Miller"]
__date__ = 20170815
__description__ = "Utility to parse text and attachments from EML files"


def main(image, image_type, part_type):
    loop = 1

    while loop <= 5:
        if loop == 1:
            extract_file_type.main(image, image_type, "eml", "../Extracted", part_type)
            loop = loop + 1
        elif loop == 2:
            extract_file_type.main(image, image_type, "msg", "../Extracted", part_type)
            loop = loop + 1
        elif loop == 3:
            extract_file_type.main(image, image_type, "mbox", "../Extracted", part_type)
            loop = loop + 1
        elif loop == 4:
            extract_file_type.main(image, image_type, "pst", "../Extracted", part_type)
            loop = loop + 1
        elif loop == 5:
            extract_file_type.main(image, image_type, "ost", "../Extracted", part_type)
            loop = loop + 1


# looped door een folder en print alle files met jpg extensies.
# moet worden aangepast naar mail extensies
# kan de mail parser uitvoeren zodra dat werkt
def recursefolder():
    for root, dirs, files in os.walk("\Extracted"):
        for filename in files:
            if filename.endswith(".jpg"):
                fileloc = os.path.join(root, filename)
                print(fileloc)


EML.main(EML.args.EML_FILE)

# recursefolder()

