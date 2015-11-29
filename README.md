# picopter
Quadcopter based on a raspberry pi implemented in python

Status: Still implementing remote control.

## Preconditions
To get the picopter run, you need to install the following python module on your raspberry pi.

```
$ sudo apt-get install python-setuptools
$ sudo easy_install -U RPIO
```

## Parts list
Part list is not complete, will be enlarged as soon as possible.
* Raspberry Pi 1 Model B+
* T-Motor AIR GEAR 350
  * 4 x Motor AIR2213 KV920
  * 4 x Plastik Prop T9545 (2XW+2CCW)
  * 4 x ESC AIR 20A 600Hz
* ~~Quadcopter Frame~~
* ESP8266 wifi module
* ~~Gyro module~~
* ~~GPS module~~

## Wiring
I will create a fritzing project with the wiring and add this to the repository.

## Open Tasks
* Remote control
* Gyro extension
* GPS extension
* Autonomous flight control with gps way points

## Links
[EPS8266 command examples](http://bbs.espressif.com/viewtopic.php?f=51&t=1022)