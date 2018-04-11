from __future__ import print_function  # Used for features from newer versions whith an older release of Python.
import exifread  # Used for extracting EXIF information from .JPG's
import os  # Used for file location on the host-system
import HashChecksum  # Calculates the SHA256 for every extracted file
import extract_file_type  # Extracts a given filetype from a previously selected image file
import sqlite3  # Used for database related tasks
from pprint import pprint  # 'Pretty Printer'. Used for data represantation


# Used for putting in all the extracted EXIF information from the extracted .JPGS's
fotolist = []


# Extracts every .JPG from the images writes them to  ../Extracted/foto
def main(image, image_type, part_type):
    try:
        os.remove("log_foto's.txt")
        os.remove("Exif Information.txt")
    except OSError:
        pass
    # Writing output to 'log_foto's
    with open("log_foto's.txt", "a") as log:
        log.write("Extracting .JPG's from previously selected image file..." + "\n")
    extract_file_type.main(image, image_type, "jpg", "../Extracted/foto", part_type)
    # Writing output to 'log_foto's
    with open("log_foto's.txt", "a") as log:
        log.write("Succesfully extracted .JPG's from image file." + "\n")
    menu()


# Extracts all EXIF information from the extracted .JPG's and prints the EXIF information on screen.
# Every .JPG will be hashed using SHA256
def show_exif():
    # Checks every file in ../Extracted/foto
    for root, dirs, files in os.walk('../Extracted/foto'):
        for filename in files:
            # Defines the location and filename
            fileloc = os.path.join(root, filename)
            # Filters every .JPG from ../Extracted/foto
            if filename.endswith('.jpg'):
                print(fileloc)
                # Hashes every extracted .JPG using SHA256 and writes it to the database
                HashChecksum.hashfile(fileloc)
                extract_exif(fileloc, "Exif Information.txt")
                print("")


# Used by show_exif to extract all the EXIF information
def extract_exif(fileloc, output):
    with open(fileloc, 'rb') as f:
        exif = exifread.process_file(f)
    # Filters certain EXIF Tags like MakerNote which contain very long hexadecimal strings
    for k in sorted(exif.keys()):
        if k not in ['JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote']:
            # Prints the EXIF information on screen by Tag and Value
            print('%s = %s' % (k, exif[k]))
            with open(output, "a") as myfile:
                myfile.write('%s = %s %s \n' % (k, str(exif[k]).strip(), fileloc))

            # Temp list used for appending to fotolist in the format Tag, Value and File Location
            templist1 = []
            templist1.append(k)
            templist1.append(str(exif[k]))
            templist1.append(fileloc)
            fotolist.append(templist1)


# Prints the content of fotolist, containing every extracted EXIF Tag from the extracted .JPGS's
def show_list():
    pprint(fotolist)


# Sorts the extracted EXIF information from the extracted .JPGS
# by used camera model in the format Model and File Location
def show_camera():
    print(":", " " * 37, "Model", " " * 37, ":", " " * 37, "Foto", " " * 37, ":")
    for item in fotolist:
        if "model" in item[0].lower():
            print(":", item[1], " " * (80 - len(item[1])),
                  ":", item[2], " " * (79 - len(item[2])), ":")


# Writes the content of fotolist to a .db file
def listtodb():
    # Connects to Photo.db
    conn = sqlite3.connect("Photo.db")
    # Writes the content as a string
    conn.text_factory = str
    c = conn.cursor()
    # Creating a table with the name Photos with 3 columns:
    c.execute("CREATE TABLE IF NOT EXISTS Photos('Tag' TEXT, 'Value' TEXT, 'Location' TEXT)")
    # Inserts every item in fotolist to the table Photos
    for item in fotolist:
        c.execute('INSERT INTO Photos VALUES(?,?,?)', (item[0], item[1], item[2],))

    conn.commit()


# Prints the different menu options on screen
def print_menu():
    print("")
    print(34 * "-", "MENU", 34 * "-")
    print("Note: In order to use every option, mode 1 has to be chosen first.")
    print("1. Show EXIF information and SHA256 for every extracted .JPG file")
    print("2. Show list with every extracted .JPG file and extraced EXIF information")
    print("3. Show used camera model for every extracted .JPEG file")
    print("4. Write the list to the database")
    print("5. Exit")
    print(75 * "-")
    print("")


# Defines every menu option and executes the corresponding def
def menu():
    loop = True
    while loop:  # While loop which will keep going until loop = False
        print_menu()  # Displays menu
        choice = raw_input("Enter your choice [1-5]: ")
        if choice == '1':
            # Exif information will be extracted and every extracted .JPG will be hashed using SHA256.
            # Hashes will be written to Hash.db
            print("Menu 1 has been selected")
            print("")
            print("This option will also create a log file called 'Exif Information.txt',"
                  " containing the extracted EXIF information from every .JPEG file.")
            option = raw_input("Continue? [y/n]: ")
            if option.lower() == "y":
                print("Extracting EXIF information...")
                # Writing output to 'log_foto's
                with open("log_foto's.txt", "a") as log:
                    log.write("Extracting EXIF information from previously extracted .JPG's..." + "\n")
                show_exif()
                # Writing output to 'log_foto's
                with open("log_foto's.txt", "a") as log:
                    log.write("Writing extracted EXIF information to 'log_foto's'..." + "\n")
                    log.write("Done!" + "\n")
                print("Done!")
                # Writing output to 'log_foto's
                with open("log_foto's.txt", "a") as log:
                    log.write("Succesfully extracted EXIF information from previously extracted .JPG's." + "\n")
            elif option.lower() == "n":
                print("")
                print("Returning to menu...")
            else:
                print("")
                print("Unknown argument. Returning to menu...")
        elif choice == '2':
            # Prints the content of fotolist, containing every extracted EXIF Tag from the extracted .JPGS's
            print("Menu 2 has been selected")
            print("")
            print("Getting list with EXIF Information from extracted .JPG's...")
            # Writing output to 'log_foto's
            with open("log_foto's.txt", "a") as log:
                log.write("Getting list with EXIF information from extracted .JPG's..." + "\n")
            show_list()
            print("")
            print("Done!")
            # Writing output to 'log_foto's
            with open("log_foto's.txt", "a") as log:
                log.write("Succesfully printed list with EXIF information from extracted .JPG's." + "\n")
        elif choice == '3':
            # Sorts the extracted EXIF information from the extracted .JPGS
            # by used camera model in the format Model and File Location
            print("Menu 3 has been selected")
            print("Getting used camera's from extracted .JPGS's...")
            # Writing output to 'log_foto's
            with open("log_foto's.txt", "a") as log:
                log.write("Getting used camera's from extracted .JPG's..." + "\n")
            show_camera()
            print("")
            print("Done!")
            # Writing output to 'log_foto's
            with open("log_foto's.txt", "a") as log:
                log.write("Succesfully found used camera's from extracted .JPG's." + "\n")
        elif choice == '4':
            # Writes the content of fotolist to a .db file
            print("Menu 4 has been selected")
            print("")
            option = raw_input("Do you want to drop the previous extracted .JPG table? [Y/n]: ")
            if option.lower() == "y":
                print("Dropping table...")
                # Writing output to 'log_foto's
                with open("log_foto's.txt", "a") as log:
                    log.write("Dropping table from the previous extracted .JPG table..." + "\n")
                conn = sqlite3.connect("Photo.db")
                c = conn.cursor()
                c.execute("DROP TABLE IF EXISTS Photos")
                print("Table has succesfully been dropped.")
                # Writing output to 'log_foto's
                with open("log_foto's.txt", "a") as log:
                    log.write("Table has succesfully been dropped." + "\n")
                print("")
                print("Writing table to database...")
                # Writing output to 'log_foto's
                with open("log_foto's.txt", "a") as log:
                    log.write("Writing table to the database..." + "\n")
                listtodb()
                print("Done!")
                # Writing output to 'log_foto's
                with open("log_foto's.txt", "a") as log:
                    log.write("Table has succesfully been written to the database." + "\n")
            elif option.lower() == "n":
                print("")
                print("Writing table to database...")
                # Writing output to 'log_foto's
                with open("log_foto's.txt", "a") as log:
                    log.write("Writing table to the database..." + "\n")
                listtodb()
                print("Done!")
                # Writing output to 'log_foto's
                with open("log_foto's.txt", "a") as log:
                    log.write("Table has succesfully been written to the database." + "\n")
            else:
                print("Unknown argument. Returning to menu...")
        elif choice == '5':
            # Exits the menu and returns to the main
            print("Returning to main menu...")
            # Writing output to 'log_foto's
            with open("log_foto's.txt", "a") as log:
                log.write("Returning to main menu..." + "\n")
            loop = False  # This will make the while loop to end as not value of loop is set to False
        else:
            # Any integer inputs other than values 1-5 will print an error message
            raw_input("Wrong option selection. Press ENTER to try again..")


# Only used when running the file directly from the terminal
if __name__ == "__main__":
    main()
