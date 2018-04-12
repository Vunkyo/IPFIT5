from __future__ import print_function
import HashChecksum
import AskStuf
import open_evidence
from Sander import Pcap
from Remon import Mail
from Dennis import foto
import os


def ascii():
    # SDR Stands for Sander, Dennis & Remon
    print("###########################################################################")
    print("#                                                                         #")
    print("#    _________________            ______                       _          #")
    print("#   /  ___|  _  \ ___ \           |  ___|                     (_)         #")
    print("#   \ `--.| | | | |_/ /           | |_ ___  _ __ ___ _ __  ___ _  ___     #")
    print("#    `--. \ | | |    /            |  _/ _ \| '__/ _ \ '_ \/ __| |/ __|    #")
    print("#   /\__/ / |/ /| |\ \            | || (_) | | |  __/ | | \__ \ | (__     #")
    print("#   \____/|___/ \_| \_|           \_| \___/|_|  \___|_| |_|___/_|\___|    #")
    print("#                                                                         #")
    print("#                                                                         #")
    print("#   ______                               _          _____           _     #")
    print("#   | ___ \                             | |        |_   _|         | |    #")
    print("#   | |_/ /___  ___  ___  __ _ _ __ ___ | |__        | | ___   ___ | |    #")
    print("#   |    // _ \/ __|/ _ \/ _` | '__/ __|| '_ \       | |/ _ \ / _ \| |    #")
    print("#   | |\ \  __/\__ \  __/ (_| | | | (__ | | | |      | | (_) | (_) | |    #")
    print("#   \_| \_\___||___/\___|\__,_|_|  \___||_| |_|      \_/\___/ \___/|_|    #")
    print("#                                                                         #")
    print("#                                                                         #")
    print("###########################################################################")
    print("")
    # Just a nice ASCII for the astatics


var = 0


def clearhashfile():
    HashChecksum.clearfile()
    # this drops the hash table in the database hash


def loadimagefile():
    # this could also write it to a database if that is needed
    with open("Log.txt", "a") as log:
        log.write("Asking info" + "\n")

    print("---------------------------------------------------------------------------")

    global imagefile        # makes this variable global so it can be used everywhere
    global imagetype        # makes this variable global so it can be used everywhere
    global imageoffset      # makes this variable global so it can be used everywhere

    imagefile = raw_input("Choose your image file: ")                                   # ask user for imagefile
    imagetype = raw_input("Is your image raw of ewf? ")                                 # ask user for imagetype
    imageoffset = input("What is your image offset? (if you are unsure try 32256) ")    # ask user for imageoffset
    # the offset will be "32256" for alot of images

    print("---------------------------------------------------------------------------")
    print("")

    HashChecksum.hashfile(imagefile)  # hashes the imagefile given by the user

    open_evidence.main(imagefile, imagetype, imageoffset)  # shows a general overview of the image given by the user

    global var
    var = 1  # set var to 1 so the menu knows it can go to the next menu


# shows the menu options of menu 1
def print_menu1():
    print("")
    print("----------------------------------- MENU ----------------------------------- ")
    print("1. Load Image file")
    print("2. Load PCAP file")
    print("3. Clear Hash.db")
    print("4. Exit")
    print(75 * "-")
    print("")
    with open("Log.txt", "a") as log:
        log.write("Printing menu" + "\n")
# dit is een test. een beter optie menu word later toegevoegd


# shows the menu options of menu 2
def print_menu2():
    print("")
    print(34 * "-", "MENU", 34 * "-")
    print("1. Foto's")
    print("2. Mail")
    print("3. Back")
    print("4. Exit")
    print(75 * "-")
    print("")
    with open("Log.txt", "a") as log:
        log.write("Printing menu" + "\n")


# main script. runs the menu which will call other functions
def main():
    AskStuf.ask()  # asks the user for info like researcher and case nr.
    AskStuf.save("Log.txt")  # writes the given info to a file in this case checksumlog.txt

    try:
        os.remove("Log.txt")
    except OSError:
        pass
    ascii()
    loop = True
    global var
    with open("Log.txt", "a") as log:
        log.write("Printing menu" + "\n")

    while loop:  # While loop which will keep going until loop = False
        if var == 0:  # if var is 0 run this menu if it is 1 run the other menu
            print_menu1()  # Displays menu
            choice = raw_input("Enter your choice [1-4]: ")
            if choice == '1':
                print("Menu 1 has been selected")
                with open("Log.txt", "a") as log:
                    log.write("loading image file" + "\n")
                loadimagefile()
            elif choice == '2':
                print("Menu 2 has been selected")
                with open("Log.txt", "a") as log:
                    log.write("staring Pcap.py" + "\n")
                Pcap.start()  # runs the main function from Pcap.py
            elif choice == '3':
                print("Menu 3 has been selected")
                with open("Log.txt", "a") as log:
                    log.write("clearing the hash database" + "\n")
                clearhashfile()  # clears the hash db
            elif choice == '4':
                print("Exit")
                with open("Log.txt", "a") as log:
                    log.write("Stopping script" + "\n")
                loop = False  # This will make the while loop to end as not value of loop is set to False
            else:
                # Any integer inputs other than values 1-4 we print an error message
                input("Wrong option selection. Press ENTER to try again..")
        elif var == 1:  # if var is 1 run this menu if it is 0 run the other menu
            print_menu2()  # Displays menu
            choice = raw_input("Enter your choice [1-4]: ")
            if choice == '1':
                print("Menu 1 has been selected")
                with open("Log.txt", "a") as log:
                    log.write("Starting foto.py" + "\n")
                global imagefile  # tells this function to take the imagefile previously defined
                global imagetype  # tells this function to take the imagetype previously defined
                part_type = raw_input("What is the partition type? (When unsure try DOS) ")  # ask part_type
                foto.main(imagefile, imagetype, part_type)  # runs the main function in foto.py
            elif choice == '2':
                print("Menu 2 has been selected")
                with open("Log.txt", "a") as log:
                    log.write("Starting Mail.py" + "\n")
                part_type = raw_input("What is the partition type? (When unsure try DOS) ")  # ask part_type
                Mail.main(imagefile, imagetype, part_type)  # runs the main function in Mail.py
            elif choice == '3':
                print("Menu 3 has been selected")
                print("Going back")
                var = 0  # makes var 0 again so you can either select an img again or select pcap
            elif choice == '4':
                print("Exit")
                with open("Log.txt", "a") as log:
                    log.write("Stopping script" + "\n")
                loop = False  # This will make the while loop to end as not value of loop is set to False
            else:
                # Any integer inputs other than values 1-4 we print an error message
                input("Wrong option selection. Press ENTER to try again..")


if __name__ == "__main__":
    main()  # starts everything
