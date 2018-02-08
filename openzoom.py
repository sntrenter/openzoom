#!/usr/local/env python
import subprocess
import time 
import postgresql
import webbrowser
import os
import socket
import urllib.request
import pyautogui
import getpass

#this command will help you test on a computer without an attached 
#drive named zoom
#subst Z: C:\zoom
#
#if your having trouble with a string having invisible chars .rstrip() might help
#test

def config():
    '''Reads the config.zoom file, containing server names, length for 
    shutdown and ports for pgsql and web services

    returns a tuple of the contents of config.zoom
    and is ment to passed to a tuple'''
    config = readfile("z:\zoom\config.zoom")
    server1 = config[0].split(';')[0]
    server2 = config[1].split(';')[0]
    server3 = config[2].split(';')[0]
    server4 = config[3].split(';')[0]
    timeout = config[4].split(';')[0]
    pgSQLpt = config[5].split(';')[0]
    webport = config[6].split(';')[0]
    return server1,server2,server3,server4,timeout,pgSQLpt,webport
    

def hostname():
    '''reads the hostname file, containing whatever thsi computer
    is identified as.

    returns a string containing the hostname'''
    hostname = "failed"
    try:
        hostname = readfile("z:\zoom\hostname.txt")[0]
    except:
        pass
    print(hostname)
    return hostname



def netstat():
    '''executes the netstat command(finding which zoom server we are hiting)
    the global variable conn in a temporary fix, it tells if the connection with
    the zoom server is ESTABLISHED, if the netstat command fails conn and netstat = 'failed'

    conn is global and does not need to be returned, netstat is returned with the unresolved(
    resolving takes to long in production) ip address. '''

    #TODO: make this function return a tuple so conn isn't global
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




def tasklist():
    '''this finds the zoom process running using the tasklist command and if it fails, ps is 
    returned as 'failed' 

     returns Zoom when process is running correctly'''
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



def sendtodb(host,task,time,date,net,conn,server,port):
    '''send to db uses postgresql to send the values that were colected 
    into a database, host=hostname,task=tasklist,time and date=time and date, 
    conn is gotten during the netstat function, the server and port are from 
    the config file'''
    try:
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
    except:
        print('the database deposite failed')





def gettime():
    '''gets time in military format, no colons
    returns that time'''
    t = time.strftime("%H%M")
    print(t)
    return t



def getdate():
    '''gets date with dd/mm/yy format and chops of the first two characters 
    of the year
    returns the date'''
    d = time.strftime("%d/%m/%Y") 
    #cuts the first 2 characters in the year area
    d = d.split('/')
    d[2] = d[2][2:]
    d = '/'.join(d)
    
    print(d)
    return d




def getmeetingid():
    '''grabs the meeting id from the attached z drive 
    and returns it as a string'''
    try:
        meetingid = readfile("z:\zoom\meetingid")[0]
    except:
        pass
    print(meetingid)
    return meetingid



def shutdown(time = 60):
    '''default time is set to 60 seconds, can pass any number of seconds,
    to cancel a shutdown enter 'shutdown /a' '''

    #TODO: make this show minutes left instead of seconds, the large 
        #numbers are scaring people 
    sd = "shutdown /s /c \"your meeting will end in "+\
         str(time)+" seconds\" /t "+str(time)
    print(sd)
    os.system(sd) 




def is_connected(link,port):
    '''this will return true if a link is accsesable and is used here 
    to check if a server can be reached. can only be given www.domain.com
    format, or it will break.

    returns true and false based on the connection status'''

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





def readfile(location):
    '''the one argument given is the file location

    returns a list containing the lines of the file, 
    ex: foo = readfile(bar)[0] returns only the first line in the file'''
    with open(location) as f:
        lines = f.readlines()
    return lines





def clicks():
    '''writes click.zoom to the z drive, letting the linux 
    host system know it is time to cycle monitors'''
    file = open('z:/zoom/click.zoom','w')
    file.close()


def networkfailure():\
    '''
    TODO:
    -implement in main
    -find out if database needs to be used
    -reorginize code
    -make a bigger commit    
    '''
    file = open('z:/zoom/FAILED.txt','w')
    file.write()
    file.close()    
    pass


def main():
    USER = getpass.getuser()
    #delete what is left in trash folder
    try:
        os.system("del /f /q c:/users/"+USER+"/downloads/*.*")
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
        clicks()
    except:
        print('failed to notify host to cycle monitors')
    time.sleep(10)#give time for the monitor cycle to happen


    try:
        os.startfile("z:\zoom\\base.ahk")
    except:
        print("failed to start base.ahk")
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



    

    #preparing for initail database deposite
    print("hostname:",end=" ")  
    host = hostname()

    print("netstat:",end=" ")
    net = netstat()

    print("connection:",end=" ")
    print(conn)

    print("tasklist:",end=" ")
    task = tasklist()

    print("time:",end=" ")
    t = gettime()

    print("date:",end=" ")
    date = getdate()

    #the data base deposite
    sendtodb(host,task,t,date,net,conn,server3,pgSQLpt)


    status = True 
    print(server1,server2)
    while(True):
        print('in while state, checking to see if meeting is over')
        oshost = 'Z:/Zoom/'+host

        if os.path.exists(oshost.rstrip()) == False:
            shutdown(timeout)

        print('Checking to make sure meeting connection is in ok state')
        netstat()
        if conn == 'ESTABLISHED' and status == False:
            status = True


            t = gettime()
            date = getdate()
            sendtodb(host,task,t,date,net,conn,server3,pgSQLpt) 
        if conn != 'ESTABLISHED' and status == True:
            status = False
            print('connection is not ESTABLISHED')
            t = gettime()
            date = getdate()
            sendtodb(host,task,t,date,net,conn,server3,pgSQLpt)

        time.sleep(10)    
main()
