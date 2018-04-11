from __future__ import print_function
import exifread
import os
import HashChecksum
import extract_file_type
import sqlite3
from pprint import pprint


fotolist = []


def main(image, image_type, part_type):
    extract_file_type.main(image, image_type, "jpg", "../Extracted/foto", part_type)
    menu()


def show_exif():
    for root, dirs, files in os.walk('../Extracted/foto'):
        for filename in files:
            fileloc = os.path.join(root, filename)
            if filename.endswith('.jpg'):
                print(fileloc)
                HashChecksum.hashfile(fileloc)
                extract_exif(fileloc, "output.txt")
                print("")


def extract_exif(fileloc, output):
    with open(fileloc, 'rb') as f:
        exif = exifread.process_file(f)
    for k in sorted(exif.keys()):
        if k not in ['JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote']:
            print('%s = %s' % (k, exif[k]))
            # with open(output, "a") as myfile:
            #     myfile.write('%s,%s,%s \n' % (k, str(exif[k]).strip(), fileloc))

            templist1 = []
            templist1.append(k)
            templist1.append(str(exif[k]))
            templist1.append(fileloc)
            fotolist.append(templist1)


def show_list():
    pprint(fotolist)


def show_camera():
    print(":", " " * 37, "Model", " " * 37, ":", " " * 37, "Foto", " " * 37, ":")
    for item in fotolist:
        if "model" in item[0].lower():
            print(":", item[1], " " * (80 - len(item[1])),
                  ":", item[2], " " * (79 - len(item[2])), ":")


def listtodb():
    # try:
    conn = sqlite3.connect("Photo.db")
    conn.text_factory = str
    c = conn.cursor()
    # Make table with 1 column:
    c.execute("CREATE TABLE IF NOT EXISTS Photos('Tag' TEXT, 'Value' TEXT, 'Location' TEXT)")
    for item in fotolist:
        c.execute('INSERT INTO Photos VALUES(?,?,?)', (item[0], item[1], item[2],))

    conn.commit()


def print_menu():
    print("")
    print(34 * "-", "MENU", 34 * "-")
    print("Note: In order to use every option, mode 1 has to be chosen first.")
    print("1. Show EXIF information and SHA256 for every extracted .JPG file")
    print("2. Show list with every extracted .JPG file and extraced EXIF information")
    print("3. Show used camera model for every extracted .JPEG file")
    print("4. Write the list to the database")
    print("5. Show GEO")
    print("6. Exit")
    print(75 * "-")
    print("")


def menu():
    loop = True
    while loop:  # While loop which will keep going until loop = False
        print_menu()  # Displays menu
        choice = raw_input("Enter your choice [1-6]: ")
        if choice == '1':
            print("Menu 1 has been selected")
            show_exif()
        elif choice == '2':
            print("Menu 3 has been selected")
            show_list()
        elif choice == '3':
            print("Menu 3 has been selected")
            show_camera()
        elif choice == '4':
            print("Menu 4 has been selected")
            listtodb()
        elif choice == '5':
            print("Menu 5 has been selected")
            print("Hoi")
        elif choice == '6':
            print("Exit")
            # You can add your code or functions here
            loop = False  # This will make the while loop to end as not value of loop is set to False
        else:
            # Any integer inputs other than values 1-4 we print an error message
            raw_input("Wrong option selection. Press ENTER to try again..")


if __name__ == "__main__":
    main()
