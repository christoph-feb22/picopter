
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
    self.set_speed(100)

    # now plug esc power on
    # send command config_esc over udp to finish setup


  def inc_speed(self, step = 1):
    if(self.__speed < self.__max_speed):
      self.set_speed(self.__speed + step)

  def dec_speed(self, step = 1):
    if(self.__speed > 0):
      self.set_speed(self.__speed - step)

  def set_speed(self, value):
    self.__speed = value
    calc_value = (1000 + value * 10)
    if( calc_value >= 1000 and calc_value <= 2000):
      self.__servo.set_servo(self.__pin, calc_value)

