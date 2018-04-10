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

#Transform a int ip address to a human readable ip address (ipv4)
def ip_to_str(address):
    return socket.inet_ntoa(address)

#Function to Hash the context of the PCAP file
def hashfile(inputfile):
    read_size = 1024  # =You can make this bigger
    checksummd5 = hashlib.md5() #MD5
    checksumsha1 = hashlib.sha1() #SHA1
    checksumsha256 = hashlib.sha256() #SHA256

    #Opens the file and hash the context
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

    #Put the hashes from the PCAP files in the database called PCAP.db
    print("Put the Hashes in the database...")
    conn = sqlite3.connect("PCAP.db")
    c = conn.cursor()
    #Make table with 3 columns: File, MD5 and SHA256
    c.execute("CREATE TABLE IF NOT EXISTS Hash(File TEXT, MD5 TEXT, SHA1 TEXT, SHA256 TEXT)")
    c.execute('INSERT INTO Hash VALUES(?,?,?,?)', (inputfile, checksummd5, checksumsha1, checksumsha256))
    conn.commit()
    print("Done!")


#Clear the database tables that were created by this program
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


#Read the PCAP file and shows the information in the Terminal
def compute(cap_file, test_file):
    SourceList = []
    DestinationList = []

    TimeLineList1 = []
    TimeLineList2 = []
    TimeLineList3 = []
    TimeLineList4 = []

    DnsList = []
    WhoIsList = []
    # Put the ip adresses of test.txt in a list called testIps
    with open(test_file, 'r') as f:
        testIps = [line.strip() for line in f]

    for item in testIps:
        if re.match("^(?:10|127|172\.(?:1[6-9]|2[0-9]|3[01])|192\.168)\..*", item):
            DnsCorrect = "Is een private IP Address"
            DnsCorrect2 = "Geen DNS info"
        else:
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=UserWarning)
                obj = IPWhois(item)  # Enter IP
                DNS = obj.lookup_whois()
                DnsCorrect = DNS['nets'][0]['name']
                DnsCorrect2 = DNS['nets'][0]['country']
        WhoIsList.append(DnsCorrect)
        DnsList.append(DnsCorrect2)

    #Opens the pcap file with rb that stands for bytes read
    with open(cap_file, 'rb') as f:
        
        #Special PCAP reader from the dpkt library
        pcap = dpkt.pcap.Reader(f)

        for timestamp, buf in pcap:
            eth = dpkt.ethernet.Ethernet(buf)
            if eth.type == dpkt.ethernet.ETH_TYPE_IP:
                ip = eth.data

                #src are the ip adresses of the source 
                src=ip_to_str(ip.src)
                #dst are the ip adresses of the destination
                dst=ip_to_str(ip.dst)
                #protocol is the number of protocol that can be: 1, 6, 17, 58 or 132
                protocol=ip.p

                #Protocol 1 stands for ICMP
                if protocol == 1:
                    protocolCorrect = "ICMP"
                #Protocol 6 stands for TCP
                if protocol == 6:
                    protocolCorrect = "TCP"
                #Protocol 17, 58 and 132 stands for UDP
                if protocol == 17 or protocol == 58 or protocol == 132:
                    protocolCorrect = "UDP"

                #Put the exact date time of the ip adress
                date_time = str(datetime.datetime.utcfromtimestamp(timestamp))

                SourceList.append(src)
                DestinationList.append(dst)

                if src in testIps:
                    TimeLineList1.append(date_time)
                    TimeLineList2.append(src)
                    TimeLineList3.append(dst)
                    TimeLineList4.append(protocolCorrect)

                if dst in testIps:
                    TimeLineList1.append(date_time)
                    TimeLineList2.append(src)
                    TimeLineList3.append(dst)
                    TimeLineList4.append(protocolCorrect)

        print("Put all IP's in the database...")
        conn = sqlite3.connect("PCAP.db")
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS Ips(Source TEXT, Destination TEXT)")
        for i in range(len(SourceList)):
            I = SourceList[i]
            II = DestinationList[i]
            c.execute('INSERT INTO Ips VALUES(?,?)', (I, II))
            conn.commit()
        print("Done!")

        #Make a list called output that compares the ip adresses with the list called testIps
        output = []
        seen = set()
        for value in testIps:
            if value not in seen:
                output.append(value)
                seen.add(value)

        #Make a list called new with the variables of the list called output
        new = []
        for item in output:
            if item in testIps:
                new.append(item)

        print("Put the compared IP's in the database...")
        conn = sqlite3.connect("PCAP.db")
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS Compare(TestBestand TEXT, PcapBestand TEXT, WHOIS TEXT, DNS TEXT)")
        for i in range(len(testIps)):
            I = testIps[i]
            II = new[i]
            III = WhoIsList[i]
            IIII = DnsList[i]
            c.execute('INSERT INTO Compare VALUES(?,?,?,?)', (I, II, III, IIII))
            conn.commit()
        print("Done!")

        print("Put the TimeLine in the database...")
        conn = sqlite3.connect("PCAP.db")
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS TimeLine(DateTime TEXT, Source TEXT, Destination TEXT, Protocol TEXT)")
        for i in range(len(TimeLineList1)):
            I = TimeLineList1[i]
            II = TimeLineList2[i]
            III = TimeLineList3[i]
            IIII = TimeLineList4[i]
            c.execute('INSERT INTO TimeLine VALUES(?,?,?,?)', (I, II, III, IIII))
            conn.commit()
        print("Done!")

#Starts the terminal interface
def start():
    conn = sqlite3.connect("PCAP.db")
    answer = "Y"

    while answer == "Y":
        loop3 = True
        answer = input("Do you want to analyse a Pcap file? Y/N ")
        if answer == "Y":
            
            answer2 = input("Do you want to delete the information of the old database? Y/N ")
            if answer2 == "Y":
                clearfile()
            
            inputFile = input("Enter the path of the PCAP-file:")
            filename = inputFile

            if os.path.exists(filename) and filename.endswith(".pcap"):
                inputFile2 = input("Enter the path of the test.txt file:")
                filename2 = inputFile2
                if os.path.exists(filename2) and filename2.endswith(".txt"):
                        hashfile(filename)
                        compute(filename, filename2)
                # If file doesn't exist or is not a .txt file give the following error
                else:
                    print("This file doesn't exist! or is not a .txt file")
                    loop3 = False
            #If file doesn't exist or is not a .pcap file give the following error
            else:
                print("This file doesn't exist! or is not a .pcap file")
                loop3 = False

            while loop3 == True:
                print("")
                answer3 = input ("1: Show Hashes from the PCAP-Files" + "\n" +
                                 "2: Show all IP-addresses from the PCAP-Files" + "\n" +
                                 "3: Show the compared IP-addresses from the PCAP-Files" + "\n" +
                                 "4: Show the Time line from the PCAP-Files" + "\n" +
                                 "5: Go to main menu" + "\n")
                if answer3 == "1":
                    print(pd.read_sql_query("SELECT * FROM Hash", conn))
                if answer3 == "2":
                    print(pd.read_sql_query("SELECT * FROM Ips", conn))
                if answer3 == "3":
                    print(pd.read_sql_query("SELECT * FROM Compare", conn))
                if answer3 == "4":
                    print(pd.read_sql_query("SELECT * FROM TimeLine", conn))
                if answer3 == "5":
                    loop3 = False
                if answer3 != "1" and answer3 != "2" and answer3 != "3" and answer3 != "4" and answer3 != "5":
                    print(answer3 + " is not an option")

        else:
            print("Stopping program...")
            exit()

if __name__ == '__main__':
    pd.set_option('display.height', 2000)
    pd.set_option('display.max_rows', 2000)
    pd.set_option('display.max_columns', 2000)
    pd.set_option('display.width', 2000)
    pd.set_option('display.max_colwidth', 1000)
    start()
