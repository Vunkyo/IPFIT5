from __future__ import absolute_import, print_function, unicode_literals
import dpkt
import socket
import datetime
import hashlib
import os.path
from ipwhois import IPWhois
import re
import sqlite3
import pandas as pd
import warnings
import time


# Transform a int ip address to a human readable ip address (ipv4)
def ip_to_str(address):
    return socket.inet_ntoa(address)


# Function to Hash the context of the PCAP file
def hashfile(inputfile):
    read_size = 1024  # =You can make this bigger
    checksummd5 = hashlib.md5()  # MD5
    checksumsha1 = hashlib.sha1()  # SHA1
    checksumsha256 = hashlib.sha256()  # SHA256

    # Opens the file and hash the context
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

    # Put the hashes from the PCAP files in the database called PCAP.db
    print("")
    print("Putting the Hashes in the database...")
    conn = sqlite3.connect("PCAP.db")
    c = conn.cursor()
    # Make table with 4 columns: File, MD5, SHA1 and SHA256
    c.execute("CREATE TABLE IF NOT EXISTS Hash(File TEXT, MD5 TEXT, SHA1 TEXT, SHA256 TEXT)")
    c.execute('INSERT INTO Hash VALUES(?,?,?,?)', (inputfile, checksummd5, checksumsha1, checksumsha256))
    conn.commit()
    conn2 = sqlite3.connect("Hash.db")
    c2 = conn2.cursor()
    c2.execute("CREATE TABLE IF NOT EXISTS Hash(File TEXT, SHA256 TEXT)")
    c2.execute('INSERT INTO Hash VALUES(?,?)', (inputfile, checksumsha256))
    conn2.commit()
    print("Done!")

    # Writes to the log file what happens
    with open("Log.txt", "a") as myfile:
        myfile.write("Creating table Hash for PCAP.db and Hash.db finished" + "\n")


# Clear the database tables that were created by this program
def clearfile():
    print("")
    print("Claering Database")
    conn = sqlite3.connect("PCAP.db")
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS Ips")
    c.execute("DROP TABLE IF EXISTS Compare")
    c.execute("DROP TABLE IF EXISTS TimeLine")
    c.execute("DROP TABLE IF EXISTS Hash")
    print("Database cleared.....")
    print("")


# Read the PCAP file and write the information to the database
def compute(cap_file, test_file):

    # Create lists that will be used furter in this function
    sourcelist = []
    destinationlist = []
    timelinelist1 = []
    timelinelist2 = []
    timelinelist3 = []
    timelinelist4 = []
    dnslist = []
    whoislist = []
    compare = []

    # Put the ip adresses of test.txt in a list called testIps
    with open(test_file, 'r') as f:
        testips = [line.strip() for line in f]

    # Will look in the list testips if a ip is a Private IP address or not
    for item in testips:
        if re.match("^(?:10|127|172\.(?:1[6-9]|2[0-9]|3[01])|192\.168)\..*", item):
            ipwhois = "Is een private IP Address"
            dnscorrect = "Geen DNS info"
        # If the IP address is not a private IP address calculate the Whois and the DNS
        else:
            with warnings.catch_warnings():
                # Ignore the error UserWarning, because the error is a common error in the ipwhois library
                warnings.filterwarnings("ignore", category=UserWarning)
                obj = IPWhois(item)  # Enter IP
                dns = obj.lookup_whois()
                ipwhois = dns['nets'][0]['name']
                dnscorrect = dns['nets'][0]['country']
        # Put the WHOIS and the DNS in the lists called: whoislist and dnslist
        whoislist.append(ipwhois)
        dnslist.append(dnscorrect)

    # Opens the pcap file with rb that stands for bytes read
    with open(cap_file, 'rb') as f:

        # Special PCAP reader from the dpkt library
        pcap = dpkt.pcap.Reader(f)

        for timestamp, buf in pcap:
            eth = dpkt.ethernet.Ethernet(buf)
            if eth.type == dpkt.ethernet.ETH_TYPE_IP:
                ip = eth.data

                # src are the ip adresses of the source
                src = ip_to_str(ip.src)
                # dst are the ip adresses of the destination
                dst = ip_to_str(ip.dst)
                # protocol is the number of protocol that can be: 1, 6, 17, 58 or 132
                protocol = ip.p

                # Protocol 1 stands for ICMP
                if protocol == 1:
                    protocolcorrect = "ICMP"
                # Protocol 6 stands for TCP
                if protocol == 6:
                    protocolcorrect = "TCP"
                # Protocol 17, 58 and 132 stands for UDP
                if protocol == 17 or protocol == 58 or protocol == 132:
                    protocolcorrect = "UDP"

                # Put the exact date time of the ip adress to the variable called date_time
                date_time = str(datetime.datetime.utcfromtimestamp(timestamp))

                # Add the source and destination IP addresses to the lists called: sourcelist and destinationlist
                sourcelist.append(src)
                destinationlist.append(dst)

                # If source or destination are in the list testips (test.txt)
                # put them in the timelinelists
                # Put them in the compare list
                if src in testips:
                    timelinelist1.append(date_time)
                    compare.append(src)
                    timelinelist2.append(src)
                    timelinelist3.append(dst)
                    timelinelist4.append(protocolcorrect)

                if dst in testips:
                    timelinelist1.append(date_time)
                    compare.append(dst)
                    timelinelist2.append(src)
                    timelinelist3.append(dst)
                    timelinelist4.append(protocolcorrect)

        # Putting all the variables of the lists: sourcelist and destinationlist in the table called Ips
        print("Putting all IP's in the database...")
        conn = sqlite3.connect("PCAP.db")
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS Ips(Source TEXT, Destination TEXT)")
        for i in range(len(sourcelist)):
            source = sourcelist[i]
            destination = destinationlist[i]
            c.execute('INSERT INTO Ips VALUES(?,?)', (source, destination))
            conn.commit()
        print("Done!")
        with open("Log.txt", "a") as myfile:
            myfile.write("Creating table Ips for PCAP.db finished" + "\n")

        # Make a list called output that compares the ip adresses with the list called testIps
        output = []
        seen = set()
        for value in compare:
            if value not in seen:
                output.append(value)
                seen.add(value)

        # Make a list called new with the variables of the list called output
        new = []
        for item in output:
            if item in compare:
                new.append(item)

        # Putting all the variables of the lists testips, new, whoislist and dnslist in the table called Compare
        print("Putting the compared IP's in the database...")
        conn = sqlite3.connect("PCAP.db")
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS Compare(TestfileTEXT, Pcapfile TEXT, WHOIS TEXT, DNS TEXT)")
        for i in range(len(new)):
            textfile_column = testips[i]
            pcapfile_column = new[i]
            whois_column = whoislist[i]
            dns_column = dnslist[i]
            c.execute('INSERT INTO Compare VALUES(?,?,?,?)', (textfile_column, pcapfile_column, whois_column,
                                                              dns_column))
            conn.commit()
        print("Done!")
        with open("Log.txt", "a") as myfile:
            myfile.write("Creating table Compare for PCAP.db finished" + "\n")

        # Putting all the variables of the timeline lists  in the table called DateTime
        print("Putting the TimeLine in the database...")
        conn = sqlite3.connect("PCAP.db")
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS TimeLine(DateTime TEXT, Source TEXT, Destination TEXT, Protocol TEXT)")
        for i in range(len(timelinelist1)):
            datetime_column = timelinelist1[i]
            source_column = timelinelist2[i]
            destination_column = timelinelist3[i]
            protocol_column = timelinelist4[i]
            c.execute('INSERT INTO TimeLine VALUES(?,?,?,?)', (datetime_column, source_column, destination_column,
                                                               protocol_column))
            conn.commit()
        print("Done!")
        with open("Log.txt", "a") as myfile:
            myfile.write("Creating table TimeLine for PCAP.db finished" + "\n")


# Starts the terminal interface
def start():
    conn = sqlite3.connect("PCAP.db")
    answer = "Y"
    pd.set_option('display.height', 2000)
    pd.set_option('display.max_rows', 2000)
    pd.set_option('display.max_columns', 2000)
    pd.set_option('display.width', 2000)
    pd.set_option('display.max_colwidth', 1000)

    while answer == "Y":
        loop3 = True
        print("----------------------------------- PCAP ----------------------------------- ")
        answer = raw_input("Do you want to analyse a Pcap file? Y/N ")
        if answer == "Y":
            answer2 = raw_input("Do you want to delete the information of the old database? Y or press a button for no ")
            if answer2 == "Y":
                with open("Log.txt", "a") as myfile:
                    myfile.write("Current date & time " + time.strftime("%c") + "\n")
                    myfile.write("PCAP function" + "\n")
                    myfile.write("Deleted context of old database" + "\n")
                clearfile()

            inputfile = raw_input("Enter the path of the PCAP-file: ")
            filename = inputfile
            with open("Log.txt", "a") as myfile:
                myfile.write("Analyse PCAP  called: " + filename + "\n")

            if os.path.exists(filename) and filename.endswith(".pcap"):
                inputfile2 = raw_input("Enter the path of the test.txt file: ")
                filename2 = inputfile2
                with open("Log.txt", "a") as myfile:
                    myfile.write("Compare PCAP file with txt file called : " + filename2 + "\n")
                if os.path.exists(filename2) and filename2.endswith(".txt"):
                    hashfile(filename)
                    compute(filename, filename2)
                # If file doesn't exist or is not a .txt file give the following error
                else:
                    print("This file doesn't exist! or is not a .txt file")
                    loop3 = False
            # If file doesn't exist or is not a .pcap file give the following error
            else:
                print("This file doesn't exist! or is not a .pcap file")
                loop3 = False

            while loop3 is True:
                print("")
                print("----------------------------------- MENU ----------------------------------- ")
                answer3 = raw_input("1: Show Hashes from the PCAP-Files" + "\n" +
                                "2: Show all IP-addresses from the PCAP-Files" + "\n" +
                                "3: Show the compared IP-addresses from the PCAP-Files" + "\n" +
                                "4: Show the Time line from the PCAP-Files" + "\n" +
                                "5: Go to main menu" + "\n" +
                                "Your option: ")
                # If option is 1 show table with all the hashes
                if answer3 == "1":
                    print(pd.read_sql_query("SELECT * FROM Hash", conn))
                    with open("Log.txt", "a") as myfile:
                        myfile.write("Showed hashes from the PCAP file " + "\n")
                # If option is 2 show table with all the IP addresses
                if answer3 == "2":
                    print(pd.read_sql_query("SELECT * FROM Ips", conn))
                    with open("Log.txt", "a") as myfile:
                        myfile.write("Showed all ip addresses from the PCAP file " + "\n")
                # If option is 3 show all IP addresses that are in the test.txt and in the .pcap file aswell
                if answer3 == "3":
                    print(pd.read_sql_query("SELECT * FROM Compare", conn))
                    with open("Log.txt", "a") as myfile:
                        myfile.write("Showed all compared ip addresses from the PCAP file " + "\n")
                # If option is 4 show table with the timeline
                if answer3 == "4":
                    print(pd.read_sql_query("SELECT * FROM TimeLine", conn))
                    with open("Log.txt", "a") as myfile:
                        myfile.write("Showed the timeline from the PCAP file " + "\n")
                # If option is 5 go back to the begin of the interface
                if answer3 == "5":
                    loop3 = False
                # If option is not one of the options give a error the options is not an option

                if answer3 != "1" and answer3 != "2" and answer3 != "3" and answer3 != "4" and answer3 != "5":
                    print(answer3 + " is not an option")

        # If the option is N stop the program
        if answer == "N":
            print("Stopping program...")
            with open("Log.txt", "a") as myfile:
                myfile.write("PCAP reseaerch done at " + time.strftime("%c") + "\n")
                myfile.write("\n")
            # Moet geen exit worden maar ervoor zorgen dat die terug naar de main gaat
            break
        # If the option is not N or Y give the error that option is not an option
        if answer != "Y" and answer != "N":
            print(answer + " is not an option")
            start()


if __name__ == '__main__':
    start()
