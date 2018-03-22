from __future__ import print_function
import re
import extract_file_type
import os
import readMsgFiles

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


def removeduplicates(inputfile, outputfile):
    lines_seen = set()  # holds lines already seen
    outfile = open(outputfile, "a")
    for line in open(inputfile, "r"):
        if line not in lines_seen:  # not a duplicate
            outfile.write(line)
            lines_seen.add(line)
    outfile.close()
    os.remove(inputfile)


def find_aders(fileloc):
    in_file = open(fileloc, "rt")
    for line in in_file:
        match = re.search(r'[\w\.-]+@[\w\.-]+', line)
        if match is not None:
            with open("email_adres.txt", "a") as myfile:
                myfile.write(match.group(0) + "\n")


def read_msg_files():
    for root, dirs, files in os.walk("..\Extracted"):
        for filename in files:
            if filename.endswith(".msg"):
                fileloc = os.path.join(root, filename)
                print(fileloc)
                readMsgFiles.main(fileloc, "..\Extracted")

                find_aders("msgmail.txt")
    removeduplicates("email_adres.txt", "email_adres_non_dup.txt")


# looped door een folder en print alle files met jpg extensies.
# moet worden aangepast naar mail extensies
# kan de mail parser uitvoeren zodra dat werkt
def read_eml_file():
    for root, dirs, files in os.walk("..\Extracted"):
        for filename in files:
            if filename.endswith(".eml"):
                fileloc = os.path.join(root, filename)
                print(fileloc)

                find_aders(fileloc)
    removeduplicates("email_adres.txt", "email_adres_non_dup.txt")


read_eml_file()
read_msg_files()

