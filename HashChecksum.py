import hashlib


def hashfile(inputfile):
    read_size = 1024  # You can make this bigger
    checksummd5 = hashlib.md5()
    checksumsha1 = hashlib.sha1()
    checksumsha256 = hashlib.sha256()

    with open(inputfile, 'rb') as f:
        data = f.read(read_size)
        while data:
            checksummd5.update(data)
            checksumsha1.update(data)
            checksumsha256.update(data)
            data = f.read(read_size)
    checksummd5 = checksummd5.hexdigest()
    checksumsha1 = checksumsha1.hexdigest()
    checksumsha256 = checksumsha256.hexdigest()

# shows de hashes in the terminal
    print("File Name: %s" % inputfile)
    print("MD5: %r" % checksummd5)
    print("SHA1: %r" % checksumsha1)
    print("SHA256: %r" % checksumsha256)
    print("")

    with open("ChecksumLog.txt", "a") as myfile:  # This writes the hashes to a file
        myfile.write("File Name: %s" % inputfile + "\n")
        myfile.write("MD5: %r" % checksummd5 + "\n")
        myfile.write("SHA1: %r" % checksumsha1 + "\n")
        myfile.write("SHA256: %r" % checksumsha256 + "\n")
        myfile.write("\n")


def clearfile():  # Clear the log file
    open("ChecksumLog.txt", 'w').close()
    print("")
    print("Log file cleared")
