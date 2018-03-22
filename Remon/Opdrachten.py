from __future__ import print_function
import re
import extract_file_type
import os
import readMsgFiles


__authors__ = ["Chapin Bryce", "Preston Miller"]
__date__ = 20170815
__description__ = "Utility to parse text and attachments from EML files"


def main(image, image_type, part_type):
    extract_file_type.main(image, image_type, "eml", "../Extracted", part_type)
    extract_file_type.main(image, image_type, "msg", "../Extracted", part_type)
    extract_file_type.main(image, image_type, "mbox", "../Extracted", part_type)
    extract_file_type.main(image, image_type, "ost", "../Extracted", part_type)


# Removes duplicate addresses from file
def removeduplicates(inputfile, outputfile):
    os.remove(outputfile)
    lines_seen = set()  # holds lines already seen
    outfile = open(outputfile, "a")
    for line in open(inputfile, "r"):
        if line not in lines_seen:  # not a duplicate
            outfile.write(line)
            lines_seen.add(line)
    outfile.close()
    os.remove(inputfile)


# Locates email addresses in text files
def find_aders(fileloc):
    in_file = open(fileloc, "rt")
    for line in in_file:
        match = re.search(r'[\w\-][\w\-\.]+@[\w\-][\w\-\.]+[a-zA-Z]{1,4}', line)
        if match is not None:
            with open("email_adres.txt", "a") as myfile:
                myfile.write(match.group(0) + "\n")


# reads .msg files and then searches for email addresses
def read_msg_files():
    for root, dirs, files in os.walk("..\Extracted"):
        for filename in files:
            if filename.endswith(".msg"):
                fileloc = os.path.join(root, filename)
                print(fileloc)
                readMsgFiles.main(fileloc, "..\Extracted")

                find_aders("msgmail.txt")


# reads .mbox files and then searches for email addresses
def read_mbox_files():
    for root, dirs, files in os.walk("..\Extracted"):
        for filename in files:
            if filename.endswith(".mbox"):
                fileloc = os.path.join(root, filename)
                print(fileloc)

                find_aders(fileloc)


# reads .eml files and then searches for email addresses
def read_eml_file():
    for root, dirs, files in os.walk("..\Extracted"):
        for filename in files:
            if filename.endswith(".eml"):
                fileloc = os.path.join(root, filename)
                print(fileloc)

                find_aders(fileloc)


read_eml_file()
read_msg_files()
read_mbox_files()
removeduplicates("email_adres.txt", "email_adres_non_dup.txt")



