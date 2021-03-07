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

def motorSpeedControl(sharedMotorSpeedData,lock):
    class motors:
        def __init__(self):
            self.status = "Initializing"
            logging.info("Initializing motor drivers")
            self.RRSpeed = 0
            self.RLSpeed = 0
            self.FRSpeed = 0
            self.FLSpeed = 0
            # Arduinos must be flashed with Standard Firmata
            try:
                self.ard0 = PyMata3(arduino_wait=2, com_port='COM6')  # Lattepanda onboard arduino
                # self.ard1 = PyMata3(arduino_wait=2, com_port='/dev/ttyACM1')  # Additional arduino micro
            except:
                logging.error("Motor fail")
                self.status = "FAIL"
                return

            # FL
            self.FL = 3
            self.ard0.servo_config(self.FL, 1000, 2000)

            # FR
            self.FR = 5
            self.ard0.servo_config(self.FR, 1000, 2000)

            # RL
            self.RL = 6
            self.ard0.servo_config(self.RL, 1000, 2000)

            # RR
            self.RR = 9
            self.ard0.servo_config(self.RR, 1000, 2000)

            # Auger
            # self.m4 = 5
            # self.ard1.servo_config(self.m4, 1000, 2000)

            # Slider
            # self.m5 = 3
            # self.ard1.servo_config(self.m5, 1000, 2000)

            # Tilt-mining
            # self.m6 = 10
            # self.ard0.servo_config(self.m6, 1000, 2000)

            # Deposit bucket
            # self.m7 = 11
            # self.ard0.servo_config(self.m7, 1000, 2000)

            self.stop()

            self.status = "OK"  # TODO: real status check (arduinos present, etc)

        # Wheel FL
        def SetMotorFL(self, speed):
            speed = map_sabertooth(speed * -1)
            self.ard0.analog_write(self.FL, speed)
            return

        # Wheel FR
        def SetMotorFR(self, speed):
            speed = map_sabertooth(speed * -1)
            self.ard0.analog_write(self.FR, speed)
            return

        # Wheel RL
        def SetMotorRL(self, speed):
            speed = map_sabertooth(speed * -1)
            self.ard0.analog_write(self.RL, speed)
            return

        # Wheel RR
        def SetMotorRR(self, speed):
            speed = map_sabertooth(speed * -1)
            self.ard0.analog_write(self.RR, speed)
            return

        # # Auger
        # def aug(self, speed):
        #     speed = map_syren(speed)
        #     self.ard1.analog_write(self.m4, speed)
        #     return
        #
        # # Slider
        # def sld(self, speed):
        #     speed = map_syren(speed - 0.12)  # Zero speed is slightly off
        #     self.ard1.analog_write(self.m5, speed)
        #     return
        #
        # # Tilt-mining
        # def tlt(self, speed):
        #     speed = map_sabertooth(speed)
        #     self.ard0.analog_write(self.m6, speed)
        #     return
        #
        # # Deposit bucket
        # def bkt(self, speed):
        #     speed = map_sabertooth(speed)
        #     self.ard0.analog_write(self.m7, speed)
        #     return

        def stop(self, smooth=False):
            # TODO smooth stop
            logging.info("Stopping motors")
            self.SetMotorRR(0)
            self.SetMotorRL(0)
            self.SetMotorFR(0)
            self.SetMotorFL(0)
            return self.status

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

        def updateMotors(self):
            motors.SetMotorRR(self.RRSpeed)
            motors.SetMotorRL(self.RLSpeed)
            motors.SetMotorFR(self.FRSpeed)
            motors.SetMotorFL(self.FLSpeed)

    motors = motors()
    while (1):
        lock.acquire()
        if "RRSpeed" in sharedMotorSpeedData.keys():
            motors.RRSpeed = sharedMotorSpeedData["RRSpeed"]
        if "RLSpeed" in sharedMotorSpeedData.keys():
            motors.RLSpeed = sharedMotorSpeedData["RLSpeed"]
        if "FRSpeed" in sharedMotorSpeedData.keys():
            motors.FRSpeed = sharedMotorSpeedData["FRSpeed"]
        if "FLSpeed" in sharedMotorSpeedData.keys():
            motors.FLSpeed = sharedMotorSpeedData["FLSpeed"]
        lock.release()
        motors.updateMotors()
        time.sleep(.1)

if __name__ == "__main__":
    from multiprocessing import Lock
    ThreadLock = Lock()
    motorSpeedControl({"RRSpeed": 0, "RLSpeed": 0, "FRSpeed": 0, "FLSpeed": 0},ThreadLock)
    # motors = motors()
    # motors.stop(False)
    # for i in range(-1000, 1000, 1):
    #     motors.RRSpeed = i / 1000
    #     motors.RLSpeed = i / 1000
    #     motors.updateMotors()
    #     print(i / 1000)
    #     time.sleep(0.01)
    # motors.stop()