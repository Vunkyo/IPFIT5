from __future__ import print_function
import re
import extract_file_type
import os
import mailbox
import HashChecksum
from pprint import pprint
import itertools
import base64

listadres = []
listmail = []
listgraph = []


def main(image, image_type, part_type):
    extract_file_type.main(image, image_type, "inbox, trash, sent items", "../Extracted", part_type)

    try:
        read_mbox_files()
        removeduplicates("email_adres.txt")
    except IOError:
        print("There where no mbox files found")

    menu()


# Removes duplicate addresses from file and places it in a list
def removeduplicates(inputfile):
    lines_seen = set()  # holds lines already seen
    for line in open(inputfile, "r"):
        if line not in lines_seen:  # not a duplicate
            listadres.append(line)
            lines_seen.add(line)
    os.remove(inputfile)


def tabel():
    print(":                   Date                    :                                      From                   "
          "                      :                                        To                                         "
          ":                                       Subject                                     :       Deleted      :")
    for item in listmail:
        if "\n" not in item[2]:
            print(":", item[0].replace("\n", ""), " "*(40-len(item[0])),
                  ":", item[1].replace("\n", ""), " "*(80-len(item[1])),
                  ":", item[2].replace("\n", ""), " "*(80-len(item[2])),
                  ":", item[3].replace("\n", ""), " "*(80-len(item[3])),
                  ":", item[5], " "*(20-len(str(item[5]))), ":")
        elif "\n" in item[2]:
            print(":", item[0].replace("\n", ""), " "*(40-len(item[0])),
                  ":", item[1].replace("\n", ""), " "*(80-len(item[1])),
                  ":", item[2].split("\n")[0], " "*(80-len(item[2])),
                  ":", item[3].replace("\n", ""), " "*(80-len(item[3])),
                  ":", item[5], " "*(20-len(str(item[5]))), ":")


def graph():
    templist = []
    for item in listmail:
        templist.append(item[1])
        templist.append(item[2])
        listgraph.append(templist)
        templist = []

    output = []
    seen = set()
    for value in listgraph:
        # If value has not been encountered yet,
        # ... add it to both list and set.
        if str(value) not in seen:
            output.append(value)
            seen.add(str(value))

    for item in output:
        if ',' not in item[1]:
            print("{}{}----->{}{}".format(item[0].replace('\n', '\ '),
                                          (" "*(100-len(item[0].replace('\n', '\ ')))), (" "*20), item[1]))
        else:
            print("{}{}----->{}{}".format(item[0].replace('\n', '\ '),
                                          (" "*(100-len(item[0].replace('\n', '\ ')))),
                                          (" "*20), item[1].split(",")[0]))


# writes date, from, to, subject and attachments to a list
# then adds that list to another list so it becomes a nested list
def emails(inputfolder, trashornot):
    mbox = mailbox.mbox(inputfolder)
    templist = []
    for message in mbox:
        templist.append(message['Date'])
        templist.append(message['From'])
        if message['To'] is None:
            templist.append("N.V.T")
        else:
            templist.append(message['To'])
        templist.append(message['subject'])
        templist.append(message.get_payload())  # if you say message.get_payload(decode=True) it gets decode beforehand
        templist.append(trashornot)
        listmail.append(templist)
        templist = []


# prints de desired email or all of them. can not be used before the emails() function
def printemail():
    print("there are %s" % len(listmail) + " emails found")
    print("If you put in 0 or a negative number then all emails will be shown ")
    print("The body will not be shown when you select 0")
    mail = input("which mail do you want to see? ") - 1
    print("")
    if mail < 0:
        i = 1
        for item in listmail:
            print("This is mail nr. %s" % i)
            print("Deleted: %s" % item[5])
            print("Date: %s" % item[0])
            print("From: %s" % item[1])
            print("To: %s" % item[2])
            print("Subject: %s" % item[3])
            # print("Body: \n %s" % item[4])
            # This shows the body. but when there are a lot of emails it can get confusing to look at
            # So the solution is when you want to see all emals they are without body and when you select a mail
            # The body will be shown and you will get the option to decode base64
            print("")
            i += 1
    else:
        print("Deleted: %s" % listmail[mail][5])
        print("Date: %s" % listmail[mail][0])
        print("From: %s" % listmail[mail][1])
        print("To: %s" % listmail[mail][2])
        print("Subject: %s" % listmail[mail][3])
        print("Body: \n %s" % listmail[mail][4])

        choice = raw_input("Do you want to decode base64? Y/n ")
        try:
            if choice == "Y":
                print(base64.b64decode(listmail[mail][4]))
        except TypeError:
            print("Oops it failed")


# Locates email addresses in text files
def find_aders(fileloc):
    in_file = open(fileloc, "rt")
    for line in in_file:
        match = re.search(r'[\w\-][\w\-\.]+@[\w\-][\w\-\.]+[a-zA-Z]{1,4}', line)
        if match is not None:
            with open("email_adres.txt", "a") as myfile:
                myfile.write(match.group(0) + "\n")


# reads .mbox files and then searches for email addresses
def read_mbox_files():
    for root, dirs, files in os.walk("..\Extracted"):
        for filename in files:
            if filename.endswith(""):  # this was endswith(".mbox") but they dont use that extension
                fileloc = os.path.join(root, filename)
                print(fileloc)
                HashChecksum.hashfile(fileloc)
                # This hashes all files that are processed.

                find_aders(fileloc)
                if filename.lower() == "trash":
                    emails(fileloc, True)
                else:
                    emails(fileloc, False)


def show_del_mails():
    i = 1
    for item in listmail:
        if item[5] is True:
            print("This is mail nr. %s" % i)
            print("Date: %s" % item[0])
            print("From: %s" % item[1])
            print("To: %s" % item[2])
            print("Subject: %s" % item[3])
            print("")
        i += 1


def print_menu1():
    print("")
    print(34 * "-", "MENU", 34 * "-")
    print("1. Print all emails")
    print("2. Print deleted emails")
    print("3. List all email addresses")
    print("4. Show table with all emails without body")
    print("5. Show a Graph of the Form & To")
    print("6. Exit")
    print(75 * "-")
    print("")


def menu():
    loop = True
    while loop:  # While loop which will keep going until loop = False
        print_menu1()  # Displays menu
        choice = raw_input("Enter your choice [1-6]: ")
        if choice == '1':
            print("Menu 1 has been selected")
            printemail()
        elif choice == '2':
            print("Menu 2 has been selected")
            show_del_mails()
        elif choice == '3':
            print("Menu 3 has been selected")
            i = 1
            for item in listadres:
                print("{}. {}".format(i, item))
                i += 1
        elif choice == '4':
            print("Menu 4 has been selected")
            tabel()
        elif choice == '5':
            print("Menu 5 has been selected")
            graph()
        elif choice == '6':
            print("Exit")
            # You can add your code or functions here
            loop = False  # This will make the while loop to end as not value of loop is set to False
        else:
            # Any integer inputs other than values 1-4 we print an error message
            raw_input("Wrong option selection. Press ENTER to try again..")


if __name__ == '__main__':
    main('..\TestImage\RawImage.dd', 'raw', 'DOS')


