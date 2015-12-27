
from motor import Motor
from wifi import WifiInterface

wifi_interface = None

def init():
  # set up the wifi interface
  global wifi_interface
  wifi_interface = WifiInterface(115200, "CLIENT", '192.168.2.1', 8888)
  wifi_interface.init_interface()

  # set up the motors
  global motor_fr
  motor_fr = Motor(17)
  motor_fr.setup()
  global motor_fl
  motor_fl = Motor(18)
  motor_fl.setup()
  global motor_br
  motor_br = Motor(19)
  motor_br.setup()
  global motor_bl
  motor_bl = Motor(20)
  motor_bl.setup()


def loop():
  global wifi_interface

  while(True):
    # read cmd
    wifi_cmd = wifi_interface.get_cmd()
    # set cmd to motors
    if(wifi_cmd == 'up'):
      motor_fr.inc_speed()
      motor_fl.inc_speed()
      motor_br.inc_speed()
      motor_bl.inc_speed()
    elif (wifi_cmd == 'down'):
      motor_fr.dec_speed()
      motor_fl.dec_speed()
      motor_br.dec_speed()
      motor_bl.dec_speed()
    elif (wifi_cmd == 'config_esc'):
      motor_fr.set_speed(0)
      motor_fl.set_speed(0)
      motor_br.set_speed(0)
      motor_bl.set_speed(0)
    elif (wifi_cmd == 'stop'):
      motor_fr.set_speed(0)
      motor_fl.set_speed(0)
      motor_br.set_speed(0)
      motor_bl.set_speed(0)

init()
loop()
# class Picopter:

#   def __init__:


#  def __main__:

#   # set up the motors
#   motor_fr = Motor()
#   motor_fl = Motor()
#   motor_br = Motor()
#   motor_bl = Motor()
