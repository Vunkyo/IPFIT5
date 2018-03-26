from __future__ import absolute_import, print_function, unicode_literals
import dpkt
import socket
import datetime
import time
import hashlib
import os.path
import csv
from ipwhois import IPWhois
import re
import warnings

#Transform a int ip address to a human readable ip address (ipv4)
def ip_to_str(address):
    return socket.inet_ntoa(address)


#transform a int mac address to a human readable mac address (EUI-48)
def mac_addr(mac_string):
    return ':'.join('%02x' % ord(b) for b in mac_string)


def hashfile(inputfile):
    read_size = 1024  # =You can make this bigger
    checksummd5 = hashlib.md5() #MD5
    checksumsha1 = hashlib.sha1() #SHA1
    checksumsha256 = hashlib.sha256() #SHA256

    #Opens the file
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

    #This writes the hashes to a file called CheksumLog.txt
    print("\n")
    print("Make ChecksumLog.txt...")
    with open("ChecksumLog.txt", "a") as myfile: 
        myfile.write("Current date & time " + time.strftime("%c") + "\n")
        myfile.write("File Name:" + inputfile + "\n")
        myfile.write("MD5:" + checksummd5 + "\n")
        myfile.write("SHA1:" + checksumsha1 + "\n")
        myfile.write("SHA256:" + checksumsha256 + "\n")
        myfile.write("\n")


#Clear the log files that were created by this program
def clearfile(): 
    open("ChecksumLog.txt", 'w').close()
    open("IpsLog.txt", 'w').close()
    open("CompareLog.txt", 'w').close()
    open("TimeLineLog.txt", 'w').close()
    open("Nieuw.csv", 'wb').close()
    print("")
    print("Log files cleared....")
    print("")


#Read the PCAP file and shows the information in the Terminal
def compute(cap_file):
    #Opens the pcap file with rb that stands for bytes read
    with open(cap_file, 'rb') as f:
        
        #Special PCAP reader from the dpkt library
        pcap = dpkt.pcap.Reader(f)

        #Counter of the packages start at 0
        counter = 0
        #Make a list called ips
        ips = []
        #Make a list called ips2
        ips2 = []

        testIps = []

        #Put the ip adresses of test.txt in a list called testIps
        with open('test.txt', 'r') as f:
            testIps = [line.strip() for line in f]

        for timestamp, buf in pcap:
            
            #counter counts how many packages there are in the PCAP file
            counter = counter + 1
            
            eth = dpkt.ethernet.Ethernet(buf)
            if eth.type == dpkt.ethernet.ETH_TYPE_IP:
                ip = eth.data
                
                #framsize are how many bytes are captured in the ip adress
                framesize = len(buf)
                #src are the ip adresses of the source 
                src=ip_to_str(ip.src)
                #dst are the ip adresses of the destination
                dst=ip_to_str(ip.dst)
                #protocol is the number of protocol that can be: 1, 6, 17, 58 or 132
                protocol=ip.p

                if ip.p == dpkt.ip.IP_PROTO_TCP:
                    tcp = ip.data
                    
                    #payloadsize 
                    payloadsize = len(tcp.data) 

                #Protocol 1 stands for ICMP
                if protocol == 1:
                    protocolCorrect = "ICMP"
                #Protocol 6 stands for TCP
                if protocol == 6:
                    protocolCorrect = "TCP"
                #Protocol 17, 58 and 132 stands for UDP
                if protocol == 17 or protocol == 58 or protocol == 132:
                    protocolCorrect = "UDP"

                #ip_info contains ip source, destination, protocol and how many bytes captured
                ip_info = ("ip source:" , src , " ip destination:" , dst , "protocol:" , protocolCorrect)
                
                #Put the exact date time of the ip adress
                date_time = str(datetime.datetime.utcfromtimestamp(timestamp))

                if re.match("^(?:10|127|172\.(?:1[6-9]|2[0-9]|3[01])|192\.168)\..*", src):
                    sander = "Is een private IP Address"
                else:
                    obj = IPWhois(src)  # Enter IP
                    DNS = obj.lookup_whois()
                    sander = (DNS['nets'][0]['name']) , (DNS['nets'][0]['country']) , (DNS['nets'][0]['city'])

                #"src port:" , tcp.sport , "dst port:" , tcp.dport
                print("No.:" , counter , "Timestamp: ", date_time , ip_info , "Port number:", tcp.sport , "DNS info:", sander)


                #Put the source and destination in the list ips
                ips.append("Source:")
                ips.append(src)
                ips.append("Destination:")
                ips.append(dst)

                #If src is in the list testIps put date time source and protocol in the list called ips2
                if src in testIps:

                    ips2.append(date_time)
                    ips2.append("\n")
                    ips2.append("Source:")
                    ips2.append(" ")
                    ips2.append(src)
                    ips2.append(" ")
                    ips2.append(protocolCorrect)
                    ips2.append("\n")

                # If destination is in the list testIps put date time destination and protocol in the list called ips2
                if dst in testIps:

                    ips2.append(date_time)
                    ips2.append("\n")
                    ips2.append("Destination:")
                    ips2.append(" ")
                    ips2.append(dst)
                    ips2.append(" ")
                    ips2.append(protocolCorrect)
                    ips2.append("\n")

        #Make a file called IpsLog.txt with the source and destination from the list called ips
        print("Make IpsLog.txt...")
        with open("IpsLog.txt", "a") as myfile:
            myfile.write("Current date & time " + time.strftime("%c") + "\n")
            myfile.write("File Name:" + cap_file + "\n")
            for item in ips:
                myfile.write("%s\n" % item)


        #Make a file called Nieuw.csv with the source and destionation from the list called ips
        with open("Nieuw.csv", "a") as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=' ',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow("Current date & time: " + time.strftime("%c"))
            spamwriter.writerow("File Name: " + cap_file)
            for item in ips:
                spamwriter.writerow(item)

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

        #Make a file called CompareLog.txt with the results of the compare that put out the variables of the list called
        # new
        print("Make CompareLog.txt...")
        with open("CompareLog.txt", "a") as myfile2:
            myfile2.write("Current date & time " + time.strftime("%c") + "\n")
            myfile2.write("File Name:" + cap_file + "\n")
            for line in new:
                myfile2.write("\n" + line)

        #Make a file called TimeLineLog.txt with the source, destination and date time from the list called ips2
        print("Make TimeLineLog.txt...")
        with open("TimeLineLog.txt", "a") as myfile3:
            myfile3.write("Current date & time " + time.strftime("%c") + "\n")
            myfile3.write("File Name:" + cap_file + "\n")
            for item in ips2:
                myfile3.write(item)

#Starts the terminal interface
def start():
   
    answer = "Y"
    while answer == "Y":
        answer = input("Do you want to analyse a Pcap file? Y/N ")
        if answer == "Y":
            
            answer2 = input("Do you want to delete the information of the old log files? Y/N ")
            if answer2 == "Y":
                clearfile()
            
            inputFile = input("Enter the name of the file:")
            filename = inputFile

            if os.path.exists(filename):
                hashfile(filename)
                compute(filename)
            #If file doesn't exist give the following error
            else:
                print("This file doesn't exist!")
        
        else:
            print("Stopping program...")
            answer = ""

start()
