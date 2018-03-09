import HashChecksum
import RecursingToCsv

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


def clearhashfile():
    HashChecksum.clearfile()


def loadimagefile():
    print("---------------------------------------------------------------------------")

    imagefile = input("Choose your image file: ")

    print("---------------------------------------------------------------------------")
    print("")

    HashChecksum.hashfile(imagefile)

    RecursingToCsv.openimage(imagefile)


def openpcapfile():
    print("Opening pcap")


def print_menu():  # Your menu design here
    print(34 * "-", "MENU", 34 * "-")
    print("1. Load Image file")
    print("2. Load PCAP file")
    print("3. Clear Hash Log")
    print("4. Exit")
    print(75 * "-")
    print("")
 # dit is een test

loop = True

while loop:  # While loop which will keep going until loop = False
    print_menu()  # Displays menu
    choice = input("Enter your choice [1-5]: ")

    if choice == '1':
        print("Menu 1 has been selected")
        loadimagefile()
    elif choice == '2':
        print("Menu 2 has been selected")
        openpcapfile()
    elif choice == '3':
        print("Menu 3 has been selected")
        clearhashfile()
    elif choice == '4':
        print("Exit")
        # You can add your code or functions here
        loop = False  # This will make the while loop to end as not value of loop is set to False
    else:
        # Any integer inputs other than values 1-5 we print an error message
        input("Wrong option selection. Press ENTER to try again..")
