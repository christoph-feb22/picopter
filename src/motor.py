
from RPIO import PWM
import time

class Motor(object):

  def __init__(self, pin):
    self.__pin = pin
    self.__servo = PWM.Servo()

    # set default values
    self.__speed = 0
    self.__max_speed  = 100

  def setup(self):
    # set speed to max
    set_speed(100)

    # wait 1 second
    time.sleep(1)

    set_speed(0)


  def inc_speed(self, step = 1):
    if(self.__speed < self.__max_speed):
      set_speed(self.__speed + step)

  def dec_speed(self, step = 1):
    if(self.__speed > 0):
      set_speed(self.__speed + step)

  def set_speed(self, value):
    self.__servo.add_channel_pulse()

