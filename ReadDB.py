from __future__ import print_function
import subprocess


def print_menu1():
    with open("Log.txt", "a") as log:
        log.write("Printing menu" + "\n")
    print("")
    print(34 * "-", "MENU", 34 * "-")
    print("1. Open Hash DB")
    print("2. Open PCAP DB")
    print("3. Open Mail DB")
    print("4. Open Photo DB")
    print("5. Exit")
    print(75 * "-")
    print("")


# runs the menu
def menu():
    loop = True
    while loop:  # While loop which will keep going until loop = False
        print_menu1()  # Displays menu
        choice = raw_input("Enter your choice [1-5]: ")
        if choice == '1':
            print("Menu 1 has been selected")
            with open("Log.txt", "a") as log:
                log.write("Opening Hash DB" + "\n")
            subprocess.Popen(["C:\Program Files\DB Browser for SQLite\DB Browser for SQLite.exe",
                              "Hash.db"])
        elif choice == '2':
            print("Menu 2 has been selected")
            with open("Log.txt", "a") as log:
                log.write("Opening PCAP DB" + "\n")
            subprocess.Popen(["C:\Program Files\DB Browser for SQLite\DB Browser for SQLite.exe",
                              "PCAP.db"])
        elif choice == '3':
            print("Menu 3 has been selected")
            with open("Log.txt", "a") as log:
                log.write("Opening Mail" + "\n")
            subprocess.Popen(["C:\Program Files\DB Browser for SQLite\DB Browser for SQLite.exe",
                              "Mail.db"])
        elif choice == '4':
            print("Menu 4 has been selected")
            with open("Log.txt", "a") as log:
                log.write("Opening Photo DB" + "\n")
            subprocess.Popen(["C:\Program Files\DB Browser for SQLite\DB Browser for SQLite.exe",
                              "Photo.db"])
        elif choice == '5':
            print("Exit")
            loop = False  # This will make the while loop to end as not value of loop is set to False
        else:
            # Any integer inputs other than values 1-4 we print an error message
            raw_input("Wrong option selection. Press ENTER to try again..")
