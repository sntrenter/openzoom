#!/usr/bin/python3
import subprocess
import time 
import webbrowser
import os
import socket
import urllib.request
#subst Z: C:\zoom

server = "svr2.missouristate.edu"

#======-----------------=============================================
#====- reads config.zoom -===========================================
#======-----------------=============================================

def config():
    #set all variables subject to change using config.zoom
    config = readfile("z:\zoom\config.zoom")
    server1 = config[0].split(';')[0]
    server2 = config[1].split(';')[0]
    server3 = config[2].split(';')[0]
    server4 = config[3].split(';')[0]
    timeout = config[4].split(';')[0]
    pgSQLpt = config[5].split(';')[0]
    webport = config[6].split(';')[0]
    return server1,server2,server3,server4,timeout,pgSQLpt,webport
    

#======-----------------=============================================
#====- gets the hostname -===========================================
#======-----------------=============================================


def hostname():
    hostname = "failed"
    try:
        hostname = readfile("z:\zoom\hostname.txt")[0]
    except:
        pass
    print(hostname)
    return hostname




#======-----------------------------------===========================
#====- grabs zoom from the netstat command -=========================
#======-----------------------------------===========================

def netstat():
    global conn
    netstat = "failed"
    conn = "failed"
    try:
        netstat = subprocess.check_output("netstat -an | findstr 8801",
                                          shell=True)
        netstat = netstat.split()
        conn = netstat[3].decode('ascii')
        netstat = netstat[2].decode('ascii').split(':')[0]


    except:
        #couldn"t find the zoom connection
        pass
    print(netstat)
    return netstat


#======------------------------------================================
#====- grabs zoom from the ps command -==============================
#======------------------------------================================

def tasklist():
    ps = "failed"
    try:
        ps = subprocess.check_output("tasklist | findstr Zoom",
                                     shell=True).decode('ascii')
        ps = ps.split()
        ps = ps[0]
    except:
        #couldn"t find the zoom process running
        pass
    print(ps)
    return ps


#======-------------------===========================================
#====- send to to database -=========================================
#======-------------------===========================================


def sendtodb(host,task,time,date,net,conn,server,port):
    db = postgresql.open(
        user = 'zoomclient',
        password = '$#P$$w0rd',
        database = 'zoomstats',
        host = server,
        port = port)
    #table is clientstats
    insertstatment = "INSERT INTO clientstats VALUES\
(\'"+host+"\',\'"+task+"\',"+time+",\'"+date+"\',\'"+net+"\',\'"+conn+"\');"
    insertstatment = insertstatment[0:-1]
    print(insertstatment)
    db.execute(insertstatment)



#======--------======================================================
#====- get time -====================================================
#======--------======================================================

def gettime():
    t = time.strftime("%H%M")
    print(t)
    return t

#======--------======================================================
#====- get date -====================================================
#======--------======================================================

def getdate():
    d = time.strftime("%d/%m/%Y")
    
    #cuts the first 2 characters in the year area
    d = d.split('/')
    d[2] = d[2][2:]
    d = '/'.join(d)
    
    print(d)
    return d

#======--------------================================================
#====- get meeting id -==============================================
#======--------------================================================

def getmeetingid():
    meetingid = "http://www.google.com"
    try:
        meetingid = readfile("z:\zoom\meetingid")[0]
    except:
        pass
    print(meetingid)
    return meetingid

#======-----------------=============================================
#====- shutdown computer -===========================================
#======-----------------=============================================

def shutdown(time = 60):
    sd = "shutdown /s /c \"your meeting will end in "+\
         str(time)+" seconds\" /t "+str(time)
    print(sd)
    os.system(sd) 

#======------------==================================================
#====- is_connected -================================================
#======------------==================================================



def is_connected(link,port):
  try:
    # see if we can resolve the host name -- tells us if there is
    # a DNS listening
    host = socket.gethostbyname(link)
    # connect to the host -- tells us if the host is actually
    # reachable
    s = socket.create_connection((host, port), 2)
    return True
  except:
     return False




#======--------======================================================
#====- readfile -====================================================
#======--------======================================================

def readfile(location):
    with open(location) as f:
        lines = f.readlines()
    return lines

#======---------=====================================================
#====- clickfile -===================================================
#======---------=====================================================

def click():
    #write to a file that activates click.py in the GNU linux host system
    file = open('z:/zoom/click.zoom','w')
    file.write('1')
    file.close()
    pass


#################################remove beep in final version########
def beep():
    freq = 440
    dur = 1000
    winsound.Beep(freq,dur)



def main():


    try:
        os.system("del /f /q c:/users/msudirect/downloads/*.*")
        print("trash deleted")
    except:
        print("couldn't delete trash")

        
    #attaches z drive incase of earlier failure
    try:
        os.system('net use z: "\\vmware-host\Shared Folders"')
        print('net use z drive called')
    except:
        print("couldn't attach the z drive") 


    try:    
        server1,server2,server3,server4,timeout,pgSQLpt,webport = config()
        print("server1:",server1)
        print("server2:",server2)
        print("server3:",server3)
        print("server4:",server4)
        print("timeout:",timeout)
        print("pgSQLpt:",pgSQLpt)
        print("webport:",webport)
    except:
        print('failed to get config.zoom')


    #click the cycle monitors button
    click()





    print('before while')
    status = True 
    while(True):
        print('beginning of while')
        print(server1,server2)
        time.sleep(3)

        
        #try server 1
        if is_connected(server1[7:-7],webport) == True:
            try:
                print("try 1")
                ret = urllib.request.urlopen(server1+host)
                print(ret)
                shutdown(timeout)
            except: 
                pass
        #try server 2  
        if is_connected(server2[7:-7],webport) == True:
            try:
                print("try 2")
                ret = urllib.request.urlopen(server2+host)
                print(ret)
                shutdown(timeout)
            except:
                pass

    
        
        print('end of while')

                
    print('after while')


    print("end of main")

    
main()

