# Handle the motor controllers
import logging
from pymata_aio.pymata3 import PyMata3
from pymata_aio.constants import Constants
import time


# TODO PID Control for each motor
# TODO Limit checks

# Shift range from [-1,1] to [0,180]
def map_sabertooth(speed):
    if speed == 0:
        return 90  # Stopped
    else:
        speed += 1
        speed /= 2
        speed *= 180
        speed = int(speed)
        return speed


def map_syren(speed):
    if speed == 0:
        return 90  # Stopped
    else:
        speed += 1
        speed /= 2
        speed *= 180
        speed = int(speed)
        return speed


class motors:
    def __init__(self):
        self.status = "Initializing"
        logging.info("Initializing motor drivers")

        # Arduinos must be flashed with Standard Firmata
        try:
            self.ard0 = PyMata3(arduino_wait=2, com_port='COM4')  # Lattepanda onboard arduino
            #self.ard1 = PyMata3(arduino_wait=2, com_port='/dev/ttyACM1')  # Additional arduino micro
        except:
            logging.error("Motor fail")
            self.status = "FAIL"
            return

        # FL
        self.m0 = 3
        self.ard0.servo_config(self.m0, 1000, 2000)

        # FR
        self.m1 = 5
        self.ard0.servo_config(self.m1, 1000, 2000)

        # RL
        self.m2 = 6
        self.ard0.servo_config(self.m2, 1000, 2000)

        # RR
        self.m3 = 9
        self.ard0.servo_config(self.m3, 1000, 2000)

        # Auger
        #self.m4 = 5
        #self.ard1.servo_config(self.m4, 1000, 2000)

        # Slider
        #self.m5 = 3
        #self.ard1.servo_config(self.m5, 1000, 2000)

        # Tilt-mining
        #self.m6 = 10
        #self.ard0.servo_config(self.m6, 1000, 2000)

        # Deposit bucket
        #self.m7 = 11
        #self.ard0.servo_config(self.m7, 1000, 2000)

        self.stop()

        self.status = "OK"  # TODO: real status check (arduinos present, etc)

    # Wheel FL
    def FL(self, speed):
        speed = map_sabertooth(speed * -1)
        self.ard0.analog_write(self.m0, speed)
        return

    # Wheel FR
    def FR(self, speed):
        speed = map_sabertooth(speed * -1)
        self.ard0.analog_write(self.m1, speed)
        return

    # Wheel RL
    def RL(self, speed):
        speed = map_sabertooth(speed * -1)
        self.ard0.analog_write(self.m2, speed)
        return

    # Wheel RR
    def RR(self, speed):
        speed = map_sabertooth(speed * -1)
        self.ard0.analog_write(self.m3, speed)
        return

    # Auger
    def aug(self, speed):
        speed = map_syren(speed)
        self.ard1.analog_write(self.m4, speed)
        return

    # Slider
    def sld(self, speed):
        speed = map_syren(speed - 0.12)  # Zero speed is slightly off
        self.ard1.analog_write(self.m5, speed)
        return

    # Tilt-mining
    def tlt(self, speed):
        speed = map_sabertooth(speed)
        self.ard0.analog_write(self.m6, speed)
        return

    # Deposit bucket
    def bkt(self, speed):
        speed = map_sabertooth(speed)
        self.ard0.analog_write(self.m7, speed)
        return

    def stop(self, smooth=False):
        # TODO smooth stop
        logging.info("Stopping motors")
        self.FL(0)
        self.FR(0)
        self.RL(0)
        self.RR(0)
        #self.aug(0)
        #self.sld(0)
        #self.tlt(0)
        #self.bkt(0)
        return self.status

    # Map wheel number to motors
    def wheel(self, num, speed):
        if num == 0:
            self.FL(speed)
        elif num == 1:
            self.FR(speed)
        elif num == 2:
            self.RL(speed)
        elif num == 3:
            self.RR(speed)

    # Map L,R tank drive to wheel number
    def tank(self, left, right):
        self.wheel(0, left)
        self.wheel(1, right)
        self.wheel(2, left)
        self.wheel(3, right)

    # Map X,Y from joystick to L,R tank drive
    def direction(self, speed, dir):
        # Math from http://home.kendra.com/mauser/joystick.html
        v = (1 - abs(dir)) * speed + speed
        w = (1 - abs(speed)) * dir + dir
        l = (v + w) / 2
        r = (v - w) / 2
        self.tank(l, r)

    def heartbeat(self):
        # Provide beat for watchdog to enable drivers
        while self.status == "OK":
            # TODO
            pass


# Testing
if __name__ == "__main__":
    motors = motors()
    motors.stop(False)
    for i in range(-1000, 1000, 1):
        #motors.wheel(0, i / 1000)
        #motors.wheel(1, i / 1000)
        #motors.wheel(2, i / 1000)
        motors.wheel(3, i / 1000)
        print(i / 1000)
        time.sleep(0.01)
    motors.stop()