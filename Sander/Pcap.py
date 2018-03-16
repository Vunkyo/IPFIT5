from __future__ import absolute_import, print_function, unicode_literals
import dpkt
import socket
import sys
import datetime
import time
import hashlib
import os.path
from tkinter import *
from pathlib import Path

#Transform a int ip address to a human readable ip address (ipv4)
def ip_to_str(address):
    return socket.inet_ntoa(address)


#transform a int mac address to a human readable mac address (EUI-48)
def mac_addr(mac_string):
    return ':'.join('%02x' % ord(b) for b in mac_string)


def hashfile(inputfile):
    read_size = 1024  # =You can make this bigger
    checksummd5 = hashlib.md5()
    checksumsha1 = hashlib.sha1()
    checksumsha256 = hashlib.sha256()

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

    #This writes the hashes to a file
    print("\n")
    print("Make ChecksumLog.txt...")
    with open("ChecksumLog.txt", "a") as myfile: 
        myfile.write("Current date & time " + time.strftime("%c") + "\n")
        myfile.write("File Name:" + inputfile + "\n")
        myfile.write("MD5:" + checksummd5 + "\n")
        myfile.write("SHA1:" + checksumsha1 + "\n")
        myfile.write("SHA256:" + checksumsha256 + "\n")
        myfile.write("\n")


#Clear the log file
def clearfile(): 
    open("ChecksumLog.txt", 'w').close()
    open("IpsLog.txt", 'w').close()
    open("CompareLog.txt", 'w').close()
    open("TimeLineLog.txt", 'w').close()
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
                ip_info = ("ip src:" , src , " ip dst:" , dst , "protocol:" , protocolCorrect , "Bytes captured:" , framesize)
                
                #Put the exact date time of the ip adress
                date_time = str(datetime.datetime.utcfromtimestamp(timestamp))
                
                # "src port:" , tcp.sport , "dst port:" , tcp.dport
                print("No.:" , counter , "Timestamp: ", date_time , ip_info , "Port number:", tcp.sport)

                #Put the source and destination in the list ips
                ips.append("Source:")
                ips.append(src)
                ips.append("Destination:")
                ips.append(dst)

                if src in testIps:

                    ips2.append(date_time)
                    ips2.append("\n")
                    ips2.append("Source:")
                    ips2.append(" ")
                    ips2.append(src)
                    ips2.append(" ")
                    ips2.append(protocolCorrect)
                    ips2.append("\n")

                if dst in testIps:

                    ips2.append(date_time)
                    ips2.append("\n")
                    ips2.append("Destination:")
                    ips2.append(" ")
                    ips2.append(dst)
                    ips2.append(" ")
                    ips2.append(protocolCorrect)
                    ips2.append("\n")

                output = []
                seen = set()
                for value in ips:
                    if value not in seen:
                        output.append(value)
                        seen.add(value)

                new = []
                for item in output:
                    if item in testIps:
                        new.append(item)

        #Make a file called IpsLog.txt with the source and destination ip adresses
        print("Make IpsLog.txt...")
        with open("IpsLog.txt", "a") as myfile:
            myfile.write("Current date & time " + time.strftime("%c") + "\n")
            myfile.write("File Name:" + cap_file + "\n")
            for item in ips:
                myfile.write("%s\n" % item)

        output = []
        seen = set()
        for value in testIps:
            if value not in seen:
                output.append(value)
                seen.add(value)

        #Make a file called CompareLog.txt with the results of the compare
        print("Make CompareLog.txt...")
        with open("CompareLog.txt", "a") as myfile2:
            myfile2.write("Current date & time " + time.strftime("%c") + "\n")
            myfile2.write("File Name:" + cap_file + "\n")
            for line in new:
                myfile2.write("\n" + line)

        #Make a file called TimeLineLog.txt with the source and destinations ip with the date time
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
        answer = input("Do u want to analyse a Pcap file? Y/N ")             
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
            #root.destroy()

start()


'''
#Stopt het programma van de GUI
def stop():
    print("Stopt GUI...")
    root.destroy()

#Wat die uitvoert als je op random klikt
def random():
    print("Dit doet niks! XD")

#Wat die uitvoert als je op hash klikt
def hash():
    print("Dit moet gaan hashen LMAO")

#De GUI
root = Tk()

label1 = Label(root, text="Pcap File Analyzer")
label1.pack()
label2 = Label(root, text="File:")
label2.pack()
entry2 = Entry(root)
entry2.pack(fill=X)

button1 = Button(root, text ="Start", bg = "red" , fg="white", command = start)
button1.pack(fill=X)
button2 = Button(root, text ="Close", bg = "purple" , fg="white", command = stop)
button2.pack(fill=X)
button3 = Button(root, text ="Hash", bg = "green" , fg="white", command = hash)
button3.pack(fill=X)
button4 = Button(root, text ="?", bg = "blue" , fg="white", command = random)
button4.pack(fill=X)

root.mainloop()
'''



