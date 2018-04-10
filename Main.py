import HashChecksum
import AskStuf
import open_evidence
from Sander import Pcap
from Remon import Opdrachten
from Dennis import test

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

var = 0


def clearhashfile():
    HashChecksum.clearfile()


def loadimagefile():
    AskStuf.ask()
    AskStuf.save("ChecksumLog.txt")

    print("---------------------------------------------------------------------------")

    global imagefile
    global imagetype
    global imageoffset

    imagefile = raw_input("Choose your image file: ")
    imagetype = raw_input("Is your image raw of ewf? ")
    imageoffset = input("What is your image offset? (if you are unsure try 32256) ")
    # the offset will be "32256" for alot of images

    print("---------------------------------------------------------------------------")
    print("")

    HashChecksum.hashfile(imagefile)

    open_evidence.main(imagefile, imagetype, imageoffset)

    global var
    var = 1


def print_menu1():
    print("")
    print("----------------------------------- MENU ----------------------------------- ")
    print("1. Load Image file")
    print("2. Load PCAP file")
    print("3. Clear Hash Log")
    print("4. Exit")
    print(75 * "-")
    print("")
# dit is een test. een beter optie menu word later toegevoegd


def print_menu2():
    print("")
    print(34 * "-", "MENU", 34 * "-")
    print("1. Foto's")
    print("2. Mail")
    print("3. Back")
    print("4. Exit")
    print(75 * "-")
    print("")


def main():
    loop = True
    global var

    while loop:  # While loop which will keep going until loop = False
        if var == 0:
            print_menu1()  # Displays menu
            choice = raw_input("Enter your choice [1-4]: ")
            if choice == '1':
                print("Menu 1 has been selected")
                loadimagefile()
            elif choice == '2':
                print("Menu 2 has been selected")
                Pcap.start()
            elif choice == '3':
                print("Menu 3 has been selected")
                clearhashfile()
            elif choice == '4':
                print("Exit")
                # You can add your code or functions here
                loop = False  # This will make the while loop to end as not value of loop is set to False
            else:
                # Any integer inputs other than values 1-4 we print an error message
                input("Wrong option selection. Press ENTER to try again..")
        elif var == 1:
            print_menu2()  # Displays menu
            choice = raw_input("Enter your choice [1-4]: ")
            if choice == '1':
                print("Menu 1 has been selected")
                global imagefile
                global imagetype
                part_type = raw_input("What is the partition type? (When unsure try DOS) ")
                test.main(imagefile, imagetype, part_type)
            elif choice == '2':
                print("Menu 2 has been selected")
                part_type = raw_input("What is the partition type? (When unsure try DOS) ")
                Opdrachten.main(imagefile, imagetype, part_type)
            elif choice == '3':
                print("Menu 3 has been selected")
                print("Going back")
                var = 0
            elif choice == '4':
                print("Exit")
                # You can add your code or functions here
                loop = False  # This will make the while loop to end as not value of loop is set to False
            else:
                # Any integer inputs other than values 1-4 we print an error message
                input("Wrong option selection. Press ENTER to try again..")


if __name__ == "__main__":
    main()
