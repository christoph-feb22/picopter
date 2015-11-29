import serial
import time

class WifiInterface():

  __debug = True
  __serial_interface_port = "/dev/ttyAMA0"
  __last_cmd = ''
  __wifi_serial = None

  # AP
  __ap_name      = "PiCopter-Wifi"
  __ap_password  = ""
  __ap_channel   = 2
  __ap_sec       = 0

  def __init__(self, baud, server_ip, server_port):
    self.__baud_rate = baud
    self.__ip = server_ip
    self.__port = server_port

    #-------------------------------------------------------------------
    # SerialPort = "/dev/ttyAMA0"
    # SerialBaudrate = 115200
    #servIP = "74.125.225.6"      # Google's IP Number
    #servPort = 80
    servIP = "192.168.178.20"
    servPort = 8888


  def __init_serial_interface(self):
    # todo: finish

    self.__wifi_serial = serial.Serial()
    self.__wifi_serial.port = self.__serial_interface_port
    self.__wifi_serial.baudrate = self.__baud_rate
    self.__wifi_serial.timeout = 2
    self.__wifi_serial.writeTimeout = 2

    # needed ? 
    self.__wifi_serial.bytesize = serial.EIGHTBITS
    self.__wifi_serial.parity = serial.PARITY_NONE
    self.__wifi_serial.stopbits = serial.STOPBITS_ONE
    self.__wifi_serial.xonxoff = False
    self.__wifi_serial.rtscts = False

    self.__wifi_serial.open()

    return self.__wifi_serial.isOpen()



    #-------------------------------------------------------------------
    #initialization and open the port.
    #possible timeout values:
    #    1. None: wait forever, block call
    #    2. 0: non-blocking mode, return immediately
    #    3. x, x is bigger than 0, float allowed, timeout block call
    # ser = serial.Serial()
    # ser.port = SerialPort
    # ser.baudrate = SerialBaudrate
    # ser.bytesize = serial.EIGHTBITS #number of bits per bytes
    # ser.parity = serial.PARITY_NONE #set parity check: no parity
    # ser.stopbits = serial.STOPBITS_ONE #number of stop bits
    # #ser.timeout = 1        #non-block read
    # ser.timeout = 2.5      #timeout block call
    # ser.xonxoff = False    #disable software flow control
    # ser.rtscts = False     #disable hardware (RTS/CTS) flow control
    # ser.dsrdtr = False     #disable hardware (DSR/DTR) flow control
    # ser.writeTimeout = 2   #timeout for write
    #-------------------------------------------------------------------


  def init_interface(self):

    if (self.__init_serial_interface()):
      print "serial interface set up"
    else:
      print "serial interface error"

    # check if esp alive
    resp = self.send_cmd('AT')
    if (resp == 'OK'):
        print "OK"
    else:
        print "Error!!!"

    # setup server
    self.send_cmd('AT+CIPMUX=1')
    self.send_cmd("AT+CIPSERVER=1," + str(self.__port))

    # setup mode
    self.send_cmd("AT+CWMODE=3")
    self.send_cmd("AT+CWMODE?")

    # setup ap
    self.send_cmd("AT+CWSAP=\"" + self.__ap_name + "\",\"" +  self.__ap_password + "\"," + str(self.__ap_channel) + "," + str(self.__ap_sec))
    self.send_cmd("AT+CWSAP?")

    # get ip address
    self.send_cmd("AT+CIFSR")



  def send_cmd(self, cmd, timo = 1, term='OK'):
    # TODO: check flushInput cmd
    self.__wifi_serial.flushInput()

    if(self.__debug):
      print("Send command: " + cmd)

    self.__wifi_serial.write(cmd + "\r\n")
    # check response
    ret = self.__wifi_serial.readline()
    time.sleep( 0.2 )
    # TODO: add timeout
    # while( lp < waitTm ):
    while( self.__wifi_serial.inWaiting() ):
      ret = self.__wifi_serial.readline().strip( "\r\n" )
      if(self.__debug):
        print(ret)
      # lp = 0
      if( ret == term ): break
      if( ret == 'ready' ): break
      if( ret == 'ERROR' ): break
      if( ret == 'Error' ): break
      # sleep( 1 )
      # lp += 1
    return ret

  # ------------------------------------------
  # def wifiCheckRxStream():
  #     while( ser.inWaiting() ):
  #         s = ser.readline().strip( "\r\n" )
  # +IPD,0,213:POST / HTTP/1.1
  # Host: 192.168.4.1:8888
  # Connection: keep-alive
  # Accept: */*
  # User-Agent: HTTPea/1.1.1 CFNetwork/758.1.6 Darwin/15.0.0
  # Accept-Language: de-de
  # Content-Length: 0
  # Accept-Encoding: gzip, deflate

  def get_cmd(self):
    cmd = ""
    if(self.__wifi_serial.inWaiting()):
      while (self.__wifi_serial.inWaiting()):
        cmd += self.__wifi_serial.readline()
        print self.__wifi_serial.inWaiting()
        print cmd
      if(cmd.find("+IPD,") > 0):
        print "IPD gefunden"
        # Todo prufen auf gewunschte lange
        self.send_response()
    ret = self.__last_cmd
    self.__last_cmd = ''
    return ret


  def send_response(self):
    # s = wifiCommand( "AT+CIPSTART=\"TCP\",\""+servIP+"\","+str(servPort), 10, sTerm="Linked" )
    # // wifi_send_cmd("AT+CIPSTART=0,TCP,192.168.4.2,8888");
    # self.send_cmd("AT+CIPSTART=0,TCP,192.168.4.2,8888")

    response = "HTTP/1.1 200 OK\r\n"
    response += "Content-Type: text/plain\r\n\r\n"
    response += "Super!\r\n"

    resp_cmd = "AT+CIPSEND=0,"
    resp_cmd += str(len(response))

    self.send_cmd(resp_cmd)
    time.sleep(0.2)
    self.send_cmd(response)

# / HTTP Header
#   String response = "HTTP/1.1 200 OK\r\n";
#   response += "Content-Type: text/plain\r\n\r\n";

#   response += "Super!\r\n";

  
#   // setup esp 4 resp
#   // AT+CIPSEND= <id>,<length>
#   String at_cmd = "AT+CIPSEND=0,";
#   at_cmd += String(response.length());

#   Debug_Serial.print(F("Lange HTTP Response: "));
#   Debug_Serial.println(String(response.length()));
#   wifi_send_cmd(at_cmd);

#   delay(20);

#   wifi_send_cmd(response);











