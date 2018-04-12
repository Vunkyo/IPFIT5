import hashlib
import sqlite3


def hashfile(inputfile):
    with open("log_main.txt", "a") as log:
        log.write("Hashing file %s" % inputfile + "\n")
    read_size = 1024  # You can make this bigger
    checksumsha256 = hashlib.sha256()  # simplify the function name

    try:
        with open(inputfile, 'rb') as f:  # opens a file
            data = f.read(read_size)        # read the file using the given read size. this is so
            while data:                     # you can still read really large files without memory crashes
                checksumsha256.update(data)
                data = f.read(read_size)
        checksumsha256 = checksumsha256.hexdigest()
        # generates the sha256 checksum

        # shows de hashes in the terminal
        print("File Name: %s" % inputfile)
        print("SHA256: %r" % checksumsha256)
        print("")

        # writes the hashes to a database
        conn = sqlite3.connect("Hash.db")  # opens the database
        c = conn.cursor()  # makes the cursor so you can add things
        # Make table with 2 columns: File and SHA256
        c.execute("CREATE TABLE IF NOT EXISTS Hash(File TEXT, SHA256 TEXT)")
        c.execute('INSERT INTO Hash VALUES(?,?)', (inputfile, checksumsha256))
        conn.commit()
        with open("log_main.txt", "a") as log:
            log.write("Writing hash to Database" + "\n")

    except IOError:
        print("There is no such file")
        with open("log_main.txt", "a") as log:
            log.write("Can't find %s" % inputfile + "\n")


def clearfile():  # Clear the log file
    conn = sqlite3.connect("Hash.db")
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS Hash")  # drops table Hash
    conn.commit()
