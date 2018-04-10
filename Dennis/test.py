from __future__ import print_function
import exifread
import os
import extract_file_type


fotolist = []
cameralist = []


def main(image, image_type, part_type):
    extract_file_type.main(image, image_type, "jpg", "../Extracted/foto", part_type)
    for root, dirs, files in os.walk('../Extracted/foto'):
        for filename in files:
            fileloc = os.path.join(root, filename)
            if filename.endswith('.jpg'):
                print(fileloc)
                extract_exif(fileloc, "output.txt")
                print("")
    printtabel()


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

    # pprint(fotolist)


def printtabel():
    print(":", " "*37, "Model", " "*37, ":", " "*37, "Foto", " "*37, ":")
    for item in fotolist:
        if "model" in item[0].lower():
            print(":", item[1], " "*(80-len(item[1])),
                  ":", item[2], " "*(79-len(item[2])), ":")


if __name__ == "__main__":
    main()
