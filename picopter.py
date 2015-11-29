#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Run 'SocketTest' Java on your PC.
# Start a Server and set servIP/servPort to your PC's one
#

import sys, serial
from time import *
import datetime, string

#-------------------------------------------------------------------
SerialPort = "/dev/ttyAMA0"
SerialBaudrate = 115200
#servIP = "74.125.225.6"      # Google's IP Number
#servPort = 80
servIP = "192.168.178.20"
servPort = 999
#-------------------------------------------------------------------
#initialization and open the port.
#possible timeout values:
#    1. None: wait forever, block call
#    2. 0: non-blocking mode, return immediately
#    3. x, x is bigger than 0, float allowed, timeout block call
ser = serial.Serial()
ser.port = SerialPort
ser.baudrate = SerialBaudrate
ser.bytesize = serial.EIGHTBITS #number of bits per bytes
ser.parity = serial.PARITY_NONE #set parity check: no parity
ser.stopbits = serial.STOPBITS_ONE #number of stop bits
#ser.timeout = 1        #non-block read
ser.timeout = 2.5      #timeout block call
ser.xonxoff = False    #disable software flow control
ser.rtscts = False     #disable hardware (RTS/CTS) flow control
ser.dsrdtr = False     #disable hardware (DSR/DTR) flow control
ser.writeTimeout = 2   #timeout for write
#-------------------------------------------------------------------

if len(sys.argv) != 3:
    print "Usage: ESP8266.py SSID Password"
    exit()
else:
    ssid = sys.argv[1]
    pwd = sys.argv[2]
    print("SSID: %s" % ssid)
    print("PWD: %s" % pwd)

# ----------------------------------------
def wifiCommand( sCmd, waitTm=1, sTerm='OK' ):
    lp = 0
    ret = ""
    print(" ")
    print("Cmd: %s" % sCmd)
    ser.flushInput()
    ser.write( sCmd + "\r\n" )
    ret = ser.readline()    # Eat echo of command.
    sleep( 0.2 )
    while( lp < waitTm ):
        while( ser.inWaiting() ):
            ret = ser.readline().strip( "\r\n" )
            print(ret)
            lp = 0
        if( ret == sTerm ): break
        if( ret == 'ready' ): break
        if( ret == 'ERROR' ): break
        if( ret == 'Error' ): break
        sleep( 1 )
        lp += 1
    return ret

# ------------------------------------------
def wifiCheckRxStream():
    while( ser.inWaiting() ):
        s = ser.readline().strip( "\r\n" )

# ------------------------------------------
def main():
    REG_OFF = True
    REG_ON = False
    # Power Cycle ESP8266 - The RTS pin is used to control the 3.3V regulator.
    #print("Pwr Off - 10s")
    #ser.setRTS(REG_OFF)    # Turn off 3.3V power.
    #sleep(10)
    #print("Pwr On - 3s")
    #ser.setRTS(REG_ON)    # Turn on 3.3V power.
    #sleep(3)        # and wait for WiFi to stabablize.
    wifiCommand( "AT" )                       # Should just return an 'OK'.
    wifiCommand( "AT+CIPCLOSE" )              # Close any open connection.
    wifiCommand( "AT+RST", 5, sTerm='ready' ) # Reset the radio. Returns with a 'ready'.
    wifiCommand( "AT+GMR" )                   # Report firmware number.
    wifiCommand( "AT+CWMODE=1" )              # Set mode to 'Sta'.
    wifiCommand( "AT+CWLAP", 10 )             # Scan for AP nodes. Returns SSID / RSSI.
    # Join Access Point given SSID and Passcode.
    wifiCommand( "AT+CWJAP=\""+ssid+"\",\""+pwd+"\"", 5 )
    wifiCommand( "AT+CWJAP?" )
    # Sometimes it takes a couple querries until we get a IP number.
    sIP = wifiCommand( "AT+CIFSR", 3, sTerm="ERROR" )
    if ( sIP == 'ERROR' ):
        i = 10    # Retry n times.
        while( (sIP == 'ERROR') and (i > 0) ):
            print(i)
            sIP = wifiCommand( "AT+CIFSR", 3, sTerm="ERROR" )
            if( sIP == 'ERROR' ): sleep( 3 )
            i -= 1
        if( i > 0 ):
            print("IP Num: %s"% sIP)
        else:
            print("Bad IP Number.")
    else:
        print("IP Num: %s"% sIP)
    wifiCommand( "AT+CIPMUX=0" )    # Setup for single connection mode.
    print("Delay - 5s")
    sleep( 5 )
    s = wifiCommand( "AT+CIPSTART=\"TCP\",\""+servIP+"\","+str(servPort), 10, sTerm="Linked" )
    if ( s == 'Linked' ):
        #cmd = 'GET / HTTP/1.0\r\n\r\n'
        cmd = "Now is the time for all good men to come to the aid of their country.\r\n"
        #cmd = "Bridgeport 30 34 31 35 31 34 41 42 43 34\r\n"
        cmdLn = str( len(cmd) )
        s = wifiCommand( "AT+CIPSEND=" + cmdLn, sTerm=">" )
        sleep( 1 )
        wifiCommand( cmd, sTerm="SEND OK" )
        #sleep( 2 )
        #wifiCommand( "+IPD" )
        i = 5
        while( i > 0 ):        # Dump whatever comes over the TCP link.
            while( ser.inWaiting() ):
                sys.stdout.write( ser.read() )
                i = 5     # Keep timeout reset as long as stuff in flowing.
            sys.stdout.flush()
            i -= 1
            sleep( 1 )
    else:
        print("Error:")
        ser.write( "\r\n" )
        sleep( 0.5 )
        i = 5
        while( (i > 0) and ser.inWaiting() ):    # Dump whatever is in the Rx buffer.
            while( ser.inWaiting() ):
                sys.stdout.write( ser.read() )
                i = 5     # Keep timeout reset as long as stuff in flowing.
            sys.stdout.flush()
            i -= 1
            sleep( 1 )

# ------------------------------------------
def _exit():
    global finished
    print("Quit")
    ser.close()
    finished = True
    exit()

# ------------------------------------------
# Custom User Input:
def Custom():
    global finished
    try:
        print(" ")
        while not finished:
            Eingabe = raw_input("Custom command to ESP8266? ")
            if Eingabe == "q":
                _exit()
            else:
                wifiCommand(Eingabe, 240)
    except:
        exit()

# ------------------------------------------
if __name__ == '__main__':
    finished = False
    try:
        ser.open()
    except Exception, e:
        print("Error open serial port: " + str(e))
        exit()
    if ser.isOpen():
        try:
            main()
            Custom()
        except Exception, e1:
            finished = True
            print("Error...: " + str(e1))
        except (KeyboardInterrupt, SystemExit):
            _exit()
    else:
        print("Cannot open serial port %s" % SerialPort)
        _exit()