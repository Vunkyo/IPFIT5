import extract_file_type
import EML
import os


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


def recursefolder():
    for filename in os.listdir('../Extracted'):
        EML.main(filename)


recursefolder()
