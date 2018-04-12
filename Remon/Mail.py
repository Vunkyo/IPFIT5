from __future__ import print_function
import re
import extract_file_type
import os
import mailbox
import HashChecksum
import sqlite3
from graphviz import Digraph
from multiprocessing import Process

# Defines the list so they can be used in all functions
listadres = []
listmail = []
listgraph = []

loop1 = False
loop2 = False


def main(image, image_type, part_type):
    extract_file_type.main(image, image_type, "inbox, trash, sent", "../Extracted/mail", part_type)
    with open("Log.txt", "a") as log:
        log.write("Succesfully extracted MBOX files from image file." + "\n")
    # Extracts the inbox, trash and sent mbox's from the image that is given in the main.py
    # extracts them to ../Extracted/mail/

    try:
        read_mbox_files()  # researches the files
        removeduplicates("email_adres.txt")  # deletes duplicate email adresses
    except IOError:
        print("There where no mbox files found")
        with open("Log.txt", "a") as log:
            log.write("There where no MBOX files" + "\n")
        # if the file it wants to open is not found return this string

    menu()  # starts the menu function defined below


# Removes duplicate addresses from file and places it in a list
def removeduplicates(inputfile):
    lines_seen = set()  # holds lines already seen
    for line in open(inputfile, "r"):  # loops trough files
        if line not in lines_seen:  # not a duplicate
            listadres.append(line)  # if not seen add to this list
            lines_seen.add(line)  # after add it to the list with seen lines
    os.remove(inputfile)  # removes the file with emails so it doesnt get a mess
    with open("Log.txt", "a") as log:
        log.write("email address duplicates removed" + "\n")


def tabel():
    print(":                   Date                    :                                      From                   "
          "                      :                                        To                                         "
          ":                                       Subject                                     :       Deleted      :")
    #  prints the collumn names

    # For each item in the nested list listmail print the date, from, to, subject and deleted
    for item in listmail:
        if "\n" not in item[2]:  # if there is a enter in the to it means there are multiple people in the To
            # if thats the cae only print the first person of that list
            print(":", item[0].replace("\n", ""), " " * (40 - len(item[0])),  # prints the item in the same format
                  ":", item[1].replace("\n", ""), " " * (80 - len(item[1])),  # as the collumn names
                  ":", item[2].replace("\n", ""), " " * (80 - len(item[2])),
                  ":", item[3].replace("\n", ""), " " * (80 - len(item[3])),
                  ":", item[5], " " * (20 - len(str(item[5]))), ":")
        elif "\n" in item[2]:
            print(":", item[0].replace("\n", ""), " " * (40 - len(item[0])),
                  ":", item[1].replace("\n", ""), " " * (80 - len(item[1])),
                  ":", item[2].split("\n")[0], " " * (80 - len(item[2])),
                  ":", item[3].replace("\n", ""), " " * (80 - len(item[3])),
                  ":", item[5], " " * (20 - len(str(item[5]))), ":")


def graph():
    templist = []  # creates a temporary list
    for item in listmail:  # goes trough all items in the nested list listmail
        templist.append(item[1])  # appends the From to the templist
        templist.append(item[2])  # appends the To to the templist
        listgraph.append(templist)  # appends the templist to the graphlist to create a nested list
        templist = []  # clears the templist so data does not get duplicated

    output = []  # creates a temporary list
    seen = set()

    # this code removes duplicates form the graphlist and places them in the output list
    for value in listgraph:
        # If value has not been encountered yet,
        # ... add it to both list and set.
        if str(value) not in seen:
            output.append(value)
            seen.add(str(value))
    with open("Log.txt", "a") as log:
        log.write("removing graph duplicats" + "\n")

    # next piece of code is for creating and displaying graphs.
    # this is done with the lib Graphviz
    # for this to work 100% graphviz als has to be installed on the system and added to the systems PATH
    g = Digraph('unix', filename='unix.gv')  # sets g. also defines filename for the graph
    g.attr(size='6,6')  # gives some attributes to the graph in this case the size
    g.node_attr.update(color='lightblue2', style='filled')  # gives some attributes to the nodes
    # in this case the nodes are supposed to be lightblue and the background filled

    # loops through all items in the output list and places them in the graph
    for item in output:
        g.edge(item[0], item[1])  # this basicly says that item[0] goes to item[1]
    with open("Log.txt", "a") as log:
        log.write("Constructing graph" + "\n")
    try:
        g.view()
        with open("Log.txt", "a") as log:
            log.write("graph made" + "\n")
        # this is the part that makes the graph into a pdf format so it can be seen          ###WARNING###
        # this also opens the pdf file in the users pdf reader                               ###WARNING###
        # this one line is the cause of a warning. but the script still functions            ###WARNING###
    except RuntimeError:
        print("Graphviz is not installed on the system or is not in the systems PATH")
        with open("Log.txt", "a") as log:
            log.write("making graph failed" + "\n")
        # if graphviz is not installed or is not correctly added to system PATH this string will be shown


# writes date, from, to, subject and attachments to a list
# then adds that list to another list so it becomes a nested list
def emails(inputfolder, trashornot):  # the trash or not is True if the file is from the trash mbox and false if not
    mbox = mailbox.mbox(inputfolder)  # defines what the mail is
    templist = []  # creates a temporary list
    templist2 = []  # creates a temporary list
    with open("Log.txt", "a") as log:
        log.write("Adding mbox messages to a list" + "\n")
    for message in mbox:  # loops through all messages in an mbox
        templist.append(message['Date'])
        templist.append(message['From'])
        if message['To'] is None:  # because python cant do some thing with NoneType objects
            # if this item is none it makes is so it becomes the string "N.V.T"
            # this could potentialy happen in the other message parts aswell
            # but while testing it only appeared int the To so thats why this line is only
            # added here
            templist.append("N.V.T")
        else:
            templist.append(message['To'])
        templist.append(message['subject'])
        if message.is_multipart():  # checks if the body is multipart. if so it adds both parts as body to the list
            for part in message.get_payload():
                templist2.append(part.get_payload(decode=True))
            templist.append(templist2)
        else:
            templist.append(message.get_payload(decode=True))
        templist.append(trashornot)
        listmail.append(templist)  # appends the templist to the listmail to create a nested list
        templist = []   # clears the templist so data does not get duplicated
        templist2 = []  # clears the templist so data does not get duplicated
    with open("Log.txt", "a") as log:
        log.write("Added mbox messages to a list" + "\n")


# prints de desired email or all of them. can not be used before the emails() function
def printemail():
    print("there are %s" % len(listmail) + " emails found")  # tells the user how many emails
    print("If you put in 0 or a negative number then all emails will be shown ")
    print("The body will not be shown when you select 0")
    mail = input("which mail do you want to see? ") - 1  # -1 because a list begins at 0
    print("")
    with open("Log.txt", "a") as log:
        log.write("trying to print 1 or more emails" + "\n")
    try:
        if mail < 0:
            i = 1
            with open("Log.txt", "a") as log:
                log.write("Printing all emails without body" + "\n")
            for item in listmail:
                print("This is mail nr. %s" % i)  # this is to keep track of what number an
                print("Deleted: %s" % item[5])  # email is for if you want to view it with body
                print("Date: %s" % item[0])
                print("From: %s" % item[1])
                print("To: %s" % item[2])
                print("Subject: %s" % item[3])
                # print("Body: \n %s" % item[4])
                # This shows the body. but when there are a lot of emails it can get confusing to look at
                # So the solution is when you want to see all emals they are without body and when you select a mail
                # The body will be shown
                print("")
                i += 1  # this is to keep track of what number an email is for if you want to view it with body
        else:  # this one prints the specific email you want with body
            with open("Log.txt", "a") as log:
                log.write("printing mail {} with body to terminal".format(mail) + "\n")
            print("Deleted: %s" % listmail[mail][5])
            print("Date: %s" % listmail[mail][0])
            print("From: %s" % listmail[mail][1])
            print("To: %s" % listmail[mail][2])
            print("Subject: %s" % listmail[mail][3])
            print("Body: \n %s" % listmail[mail][4])
    except IndexError:
        print("Mail not found")
        with open("Log", "a") as log:
            log.write("choosen email not found" + "\n")
        # if the user selects an email number that is not in the list.
        # for example the list has 300 emails and the user searchers for mail 539


# Locates email addresses in text files
def find_aders(fileloc):
    in_file = open(fileloc, "rt")
    with open("Log.txt", "a") as log:
        log.write("Searching for email addresses" + "\n")
    for line in in_file:  # searches each file lin by line
        match = re.search(r'[\w\-][\w\-\.]+@[\w\-][\w\-\.]+[a-zA-Z]', line)  # regular expression detects addresses
        if match is not None: # if there is a match write it to a file
            with open("email_adres.txt", "a") as myfile:
                myfile.write(match.group(0) + "\n")  # writes an email address and then places an Enter
    with open("Log.txt", "a") as log:
        log.write("writing emailaddresses to email_adres.txt" + "\n")


# reads .mbox files and then searches for email addresses
def read_mbox_files():
    with open("Log.txt", "a") as log:
        log.write("Walking through folder" + "\n")
        log.write("Reasearching folder" + "\n")
    for root, dirs, files in os.walk("..\Extracted\mail"):              # This part of the script walks through
        for filename in files:                                          # all the files in the specified folder
            if filename.endswith(""):  # this was endswith(".mbox") the extracted files dont have that extension
                fileloc = os.path.join(root, filename)  # creates a variable fileloc wicht basicly is the location of
                print(fileloc)                          # a file
                HashChecksum.hashfile(fileloc)          # This hashes each file it finds in the specified folder

                find_aders(fileloc)  # runs the script that finds email addresses
                if filename.lower() == "trash":             # if that file is trash then the trashornot is True
                    emails(fileloc, True)                   # otherwise the trashornot is false
                else:                                       # this is for recognising deleted emails
                    emails(fileloc, False)


def show_del_mails():
    i = 1
    with open("Log.txt", "a") as log:
        log.write("searching and printing deleted emails" + "\n")
    for item in listmail:                                           # This script goes through all items in listmail
        if item[5] is True:                                         # and if item[5] (trashornot) is true
            print("This is mail nr. %s" % i)                        # it prints the email without body
            print("Date: %s" % item[0])
            print("From: %s" % item[1])
            print("To: %s" % item[2])
            print("Subject: %s" % item[3])
            print("")
        i += 1
        # all emails get counted so the email nr. is same as in the printemail function
        # the reason for this is that if you want to see the body you can use that function (menu option 1)


def table1(c):  # this adds data in a database table
    # this is in a seperate function because then they can be ran multithreaded
    print("Adding to table Addresses")
    for item in listadres:
        c.execute('INSERT INTO Addresses VALUES(?)', (item,))  # add all items from listaddres to the table addresses

    print("Table Addresses Done")
    global loop1
    loop1 = True  # if set a variabele to True to check if the script is done
    with open("Log.txt", "a") as log:
        log.write("Adding data to table Addresses" + "\n")


def table2(c):
    print("Adding to table Emails")
    for item in listmail:
        c.execute('INSERT INTO Emails VALUES(?,?,?,?,?,?)', (item[0], item[1], item[2], item[3],
                                                             str(item[4]), str(item[5]),))
        # add all items from listmail to the table emails

    print("Table Emails Done")
    global loop2
    loop2 = True  # if set a variabele to True to check if the script is done
    with open("Log.txt", "a") as log:
        log.write("Adding data to table Emails" + "\n")


def listtodb():
    print("Writing to Database")
    conn = sqlite3.connect("Mail.db")  # opens the database
    conn.text_factory = str  # makes it so you can use strings or something
    c = conn.cursor()  # makes the cursor so you can add things
    # Make table with 1 column:
    c.execute("CREATE TABLE IF NOT EXISTS Addresses(Addres TEXT)")
    # Make table with 6 columns
    c.execute("CREATE TABLE IF NOT EXISTS Emails('Datum' TEXT, 'From' TEXT, 'To' TEXT,"
              " 'Subject' TEXT, 'Body' TEXT, 'Deleted' TEXT)")
    with open("Log.txt", "a") as log:
        log.write("creating tables if they did not exist" + "\n")

    Process(target=table2(c)).start()  # runs this line alogside the one below it
    Process(target=table1(c)).start()  # runs this line alogside the one above it

    if (loop1 is True) and (loop2 is True):  # if both loop1 and loop2 are done contineu the script
        conn.commit()
        print("Added to Database")


# def that prints the menu options
def print_menu1():
    with open("Log.txt", "a") as log:
        log.write("Printing menu" + "\n")
    print("")
    print(34 * "-", "MENU", 34 * "-")
    print("1. Print all emails")
    print("2. Print deleted emails")
    print("3. List all email addresses")
    print("4. Show table with all emails without body")
    print("5. Show a Graph of the Form & To")
    print("6. Write to lists Database")
    print("7. Exit")
    print(75 * "-")
    print("")


# runs the menu
def menu():
    loop = True
    while loop:  # While loop which will keep going until loop = False
        print_menu1()  # Displays menu
        choice = raw_input("Enter your choice [1-7]: ")
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
                print("{}. {}".format(i, item))  # prints the list with numbers in front of it
                i += 1
        elif choice == '4':
            print("Menu 4 has been selected")
            tabel()
        elif choice == '5':
            print("Menu 5 has been selected")
            print("Making Graph")
            graph()
            print("Done")
        elif choice == '6':
            print("Menu 6 has been selected")
            yesorno = raw_input("Do you want to drop the previous email table? (Y/n) ")  # gives the option
            if yesorno.lower() == "y":                                                   # to drop tables
                print("Dropping tables")
                conn = sqlite3.connect("Mail.db")
                c = conn.cursor()
                c.execute("DROP TABLE IF EXISTS Emails")     # drops table emails
                print("Dropped table Emails")
                c.execute("DROP TABLE IF EXISTS Addresses")  # drops table addresses
                print("Dropped table Addresses")
                conn.commit()
                print("Dropped all tables")
                with open("Log.txt", "a") as log:
                    log.write("Dropped existing tables" + "\n")
                listtodb()
            elif yesorno.lower() == "n":
                listtodb()
            else:
                print("Invalid entry")
        elif choice == '7':
            print("Exit")
            loop = False  # This will make the while loop to end as not value of loop is set to False
        else:
            # Any integer inputs other than values 1-4 we print an error message
            raw_input("Wrong option selection. Press ENTER to try again..")


if __name__ == '__main__':
    main('..\TestImage\RawImage.dd', 'raw', 'DOS')
    # Just for testing. will be user input if run from main.py
