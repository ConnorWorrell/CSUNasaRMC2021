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

            self.FRSpeed = 0
            self.FLSpeed = 0

            self.WormLSpeed = 0
            self.WormRSpeed = 0

            self.BucketSpeed = 0

            self.ActuatorLSpeed = 0

            self.BeltSpeed = 0


            # Arduinos must be flashed with Standard Firmata
            try:
                self.ard0 = PyMata3(arduino_wait=2, com_port='COM4')  # Lattepanda onboard arduino
                self.ard1 = PyMata3(arduino_wait=2, com_port='COM7')  # External Arduino Uno
                # self.ard1 = PyMata3(arduino_wait=2, com_port='/dev/ttyACM1')  # Additional arduino micro
            except:
                print("On Board Arduino Connection Failed")
                self.status = "FAIL"
                return
            # try:
            #     pass
            #     # self.ard1 = PyMata3(arduino_wait=2, com_port='COM5')  # External Arduino Uno
            # except:
            #     print("Arduino Connection Failed")
            #     self.status = "FAIL"
            #     return

            # Front Left
            self.FL = 6
            self.ard0.servo_config(self.FL, 1000, 2000)

            # Front Right
            self.FR = 5
            self.ard0.servo_config(self.FR, 1000, 2000)

            # Left Worm screw
            self.WormL = 10
            self.ard0.servo_config(self.WormL, 1000, 2000)

            # Right Worm screw
            self.WormR = 11
            self.ard0.servo_config(self.WormR, 1000, 2000)

            # Bucket Motor
            self.Bucket = 9
            self.ard0.servo_config(self.Bucket, 1000, 2000)

            # Left Linear Actuator
            self.ActuatorL = 3
            self.ard0.servo_config(self.ActuatorL, 1000, 2000)

            # Belt Motor
            self.Belt = 13
            self.ard0.set_pin_mode(self.Belt, Constants.PWM)

            self.stop()

            self.status = "OK"  # TODO: real status check (arduinos present, etc)

        # Wheel FL
        def SetMotorFL(self, speed):
            print("MotorFL",speed)
            speed = map_sabertooth(speed * 1)
            print("MotorFL", speed)
            self.ard0.analog_write(self.FL, speed)
            return

        # Wheel FR
        def SetMotorFR(self, speed):
            print("MotorFR", speed)
            speed = map_sabertooth(speed * 1)
            self.ard0.analog_write(self.FR, speed)
            return

        # Left Worm Screw
        def SetMotorWormL(self, speed):
            print("MotorWormL", speed)
            speed = map_sabertooth(speed * 1)
            self.ard0.analog_write(self.WormL, speed)
            return

        # Right Worm Screw
        def SetMotorWormR(self, speed):
            print("MotorWormR", speed)
            speed = map_sabertooth(speed * 1)
            self.ard0.analog_write(self.WormR, speed)
            return

        # Bucket
        def SetMotorBucket(self, speed):
            print("MotorBucket", speed)
            speed = map_syren(speed * 1)
            self.ard0.analog_write(self.Bucket, speed)
            return

        # Left Linear Actuator
        def SetMotorActuatorL(self, speed):
            print("MotorActuatorL", speed)
            speed = map_sabertooth(speed * 1)
            self.ard0.analog_write(self.ActuatorL, speed)
            return

        # Belt Motor
        def SetMotorBelt(self, speed):
            print("MotorBelt", speed)
            # speed = map_sabertooth(speed * 1)
            self.ard0.analog_write(self.Belt, speed*255)
            return

        def stop(self, smooth=False):
            # TODO smooth stop
            logging.info("Stopping motors")
            self.SetMotorFR(0)
            self.SetMotorFL(0)
            self.SetMotorWormL(0)
            self.SetMotorWormR(0)
            self.SetMotorBucket(0)
            self.SetMotorActuatorL(0)
            self.SetMotorBelt(0)
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
            motors.SetMotorFR(self.FRSpeed)
            motors.SetMotorFL(self.FLSpeed)
            motors.SetMotorWormL(self.WormLSpeed)
            motors.SetMotorWormR(self.WormRSpeed)
            motors.SetMotorBucket(self.BucketSpeed)
            motors.SetMotorActuatorL(self.ActuatorLSpeed)
            motors.SetMotorBelt(self.BeltSpeed)

    motors = motors()
    while (1):
        lock.acquire()
        if "FRSpeed" in sharedMotorSpeedData.keys():
            motors.FRSpeed = sharedMotorSpeedData["FRSpeed"]
        if "FLSpeed" in sharedMotorSpeedData.keys():
            motors.FLSpeed = sharedMotorSpeedData["FLSpeed"]
        if "WormLSpeed" in sharedMotorSpeedData.keys():
            motors.WormLSpeed = sharedMotorSpeedData["WormLSpeed"]
        if "WormRSpeed" in sharedMotorSpeedData.keys():
            motors.WormRSpeed = sharedMotorSpeedData["WormRSpeed"]
        if "BucketSpeed" in sharedMotorSpeedData.keys():
            motors.BucketSpeed = sharedMotorSpeedData["BucketSpeed"]
        if "ActuatorLSpeed" in sharedMotorSpeedData.keys():
            motors.ActuatorLSpeed = sharedMotorSpeedData["ActuatorLSpeed"]
        if "BeltSpeed" in sharedMotorSpeedData.keys():
            motors.BeltSpeed = sharedMotorSpeedData["BeltSpeed"]
        lock.release()
        motors.updateMotors()
        time.sleep(.1)

if __name__ == "__main__":
    from multiprocessing import Lock
    ThreadLock = Lock()
    motorSpeedControl({"RRSpeed": 0, "RLSpeed": 0, "FRSpeed": 0, "FLSpeed": 0, "WormLSpeed": 0, "WormRSpeed": 0, "BucketSpeed": 0, "ActuatorLSpeed": 0, "ActuatorRSpeed": 0, "BeltSpeed": 0},ThreadLock)
    # motors = motors()
    # motors.stop(False)
    # for i in range(-1000, 1000, 1):
    #     motors.RRSpeed = i / 1000
    #     motors.RLSpeed = i / 1000
    #     motors.updateMotors()
    #     print(i / 1000)
    #     time.sleep(0.01)
    # motors.stop()