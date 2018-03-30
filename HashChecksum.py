import hashlib


def hashfile(inputfile):
    read_size = 1024  # You can make this bigger
    checksumsha256 = hashlib.sha256()

    try:
        with open(inputfile, 'rb') as f:
            data = f.read(read_size)
            while data:
                checksumsha256.update(data)
                data = f.read(read_size)
        checksumsha256 = checksumsha256.hexdigest()

        # shows de hashes in the terminal
        print("File Name: %s" % inputfile)
        print("SHA256: %r" % checksumsha256)
        print("")

        with open("ChecksumLog.txt", "a") as myfile:  # This writes the hashes to a file
            myfile.write("File Name: %s" % inputfile + "\n")
            myfile.write("SHA256: %r" % checksumsha256 + "\n")
            myfile.write("\n")
    except IOError:
        print("There is no such file")


def clearfile():  # Clear the log file
    open("ChecksumLog.txt", 'w').close()
    print("")
    print("Log file cleared")
