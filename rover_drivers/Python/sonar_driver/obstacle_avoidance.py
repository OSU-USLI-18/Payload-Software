#!/usr/bin/python3

from sonar import Sonar
from threading import Thread, Condition
from copy import deepcopy
from sys import stderr
from time import sleep
from enum import Enum
import dual_mc33926
import ptvsd

class Obstacle_Avoidance:
    """
    A class for performing obstacle avoidance by running a sonar thread and a motor control thread
    in parallel.

    Attributes:
        max_speed (int):        The maximum speed value for the motor driver.
        decel_rate (float):     How quickly (from 0 to 1) the rover should decelerate.
        turn_time (float):      How long (in seconds) the rover should turn left or right.
        reverse_time (float):   How long (in seconds) the rover should reverse.
        turn_dist (int):        How close an obstacle must be (in mm) before the rover turns.
        reverse_dist (int):     How close an obstacle must be (in mm) before the rover reverses.
        offset (float):         Since the wheels aren't straight, one wheel will turn slower.
    """

    class Direction(Enum):
        """This enumerates the possible directions the rover can move/turn."""
        FORWARD  = 0
        BACKWARD = 1
        RIGHT    = 2
        LEFT     = 3

    def __init__(self, threshold=0.1, buffer_size=5, max_speed=480, decel_rate=0.05, turn_time=1,
                 reverse_time=1, turn_dist=1000, reverse_dist=500, offset=0.8, debug=False):
        """
        Constructs an Obstacle_Avoidance object using a series of overridable default parameters.

        Keyword Arguments:
            threshold (float):      What threshold value to pass to the Sonar object.
            buffer_size (int):      What buffer_size value to pass to the Sonar object.
            max_speed (int):        Refer to the max_speed class attribute.
            decel_rate (float):     Refer to the decel_rate class attribute.
            turn_time (float):      Refer to the turn_time class attribute.
            reverse_time (float):   Refer to the reverse_time class attribute.
            turn_dist (int):        Refer to the turn_dist class attribute.
            reverse_dist (int):     Refer to the reverse_dist class attribute.
            offset (float):         Refer to the offset class attribute.
            debug (bool):           Flag that controls whether or not to allow remote debugging.
        """
        # If debug is enabled, wait for the remote debugger to attach before continuing.
        if debug:
            ptvsd.enable_attach("rover_senpai")
            print("Waiting for debugger to attach...", file=stderr)
            ptvsd.wait_for_attach()
            print("Debugger attached, continuing...", file=stderr)

        dual_mc33926.io_init_motor_drive()  # Initializes the motor driver.
        self.max_speed     = max_speed
        self.decel_rate    = decel_rate
        self.turn_time     = turn_time
        self.reverse_time  = reverse_time
        self.turn_dist     = turn_dist
        self.reverse_dist  = reverse_dist
        self.offset        = offset
        self._sonar_data   = (0, b'')       # Distance and the sonar indicator (b'L' or b'R').
        self._stop_flag    = False          # Causes the threads to stop when set to true.
        self._condition    = Condition()    # Condition object protects _sonar_data and _stop_flag.
        self._sonar        = Sonar(threshold=threshold, buffer_size=buffer_size)
        self._motor        = dual_mc33926.MotorDriver()
        self._sonar_thread = Thread(target=self._run_sonar, daemon=True)
        self._motor_thread = Thread(target=self._run_motor, daemon=True)

    def _run_sonar(self):
        """Continously runs the sonars and notifies the motor thread whenever an object is close."""
        while True:
            # Gets a measurement from the sonars.
            dist, dir = self._sonar.measure()

            # If the measured sonar distance is less than our turning threshold...
            if dist < self.turn_dist:
                self._condition.acquire()

                # If the stop flag has been set by stop(), release the lock and break out.
                if self._stop_flag:
                    self._condition.release()
                    break

                # Otherwise, publish the distance and which sonar detected it.
                self._sonar_data = (dist, dir)
                self._condition.notify_all()
                self._condition.release()

    def _run_motor(self):
        """Continuously runs the motors and turns away from any obstacles deteced by the sonars."""
        self._motor.enable()

        def move(direction=Direction.FORWARD, duration=None):
            """
            Helper method which simply moves/turns the rover in a given direction.

            Keyword Arguments:
                direction (Direction):  The direction the rover should turn/move.
                duration (float):       How long the rover should move in this direction.
            """
            # First, gradually stop whatever the motors were doing before.
            for i in range(1 - self.decel_rate, 0, -self.decel_rate):
                self._motor.set_speeds(self._spd1 * i, self._dir1, self._spd2 * i, self._dir2)
                sleep(0.05)

            # Determine speed and direction of motors based on the desired direction.
            if direction == Direction.FORWARD:
                self._spd1 = self.max_speed
                self._spd2 = self.max_speed * self.offset
                self._dir1 = 1
                self._dir2 = 1
            elif direction == Direction.BACKWARD:
                self._spd1 = self.max_speed
                self._spd2 = self.max_speed * self.offset
                self._dir1 = 0
                self._dir2 = 0
            elif direction == Direction.RIGHT:
                self._spd1 = 0
                self._spd2 = self.max_speed * self.offset
                self._dir1 = 1
                self._dir2 = 1
            else:
                self._spd1 = self.max_speed
                self._spd2 = 0
                self._dir1 = 1
                self._dir2 = 1

            # Start moving.
            self._motor.set_speeds(self._spd1, self._dir1, self._spd2, self._dir2)

            # Wait for a duration (if specified) before accepting another move command.
            if (type(duration) in [int, float]) and (duration > 0):
                sleep(duration)

        # The rover continuously moves forward, reversing and turning away from detected obstacles.
        while True:
            # Move forward until sonar publishes data about a detected obstacle.
            move()
            self._condition.acquire()
            self._condition.wait()

            # If the stop flag has been set by stop(), release the lock and break out.
            if self._stop_flag:
                self._condition.release()
                break

            # Otherwise, save the distance from the obstacle (in mm) and which sonar detected it.
            dist, dir = self._sonar_data.deepcopy()
            self._condition.release()

            # If the object is very close, first reverse from it.
            if dist < self.reverse_dist:
                move(direction=Direction.BACKWARD, duration=self.reverse_time)
            
            # Turn right away from objects detected by the left sonar.
            if dir == b'R':
                move(direction=Direction.LEFT, duration=self.turn_time)
            
            # Turn left away from objects detected by the right sonar.
            elif dir == b'L':
                move(direction=Direction.RIGHT, duration=self.turn_time)

            # Raise an exception if we see an unrecognized sonar label.
            else:
                raise ValueError("Invalid sonar label")

        # Disable the motors once we break out of the loop.
        self._motor.disable()

    def start(self):
        """This method starts the obstacle avoidance algorithm."""
        if not (self._motor_thread.is_alive() and self._sonar_thread.is_alive()):
            self._stop_flag = False
            self._sonar_thread.start()
            self._motor_thread.start()
            print("Obstacle avoidance is now running.", file=stderr)
        else:
            print("Obstacle avoidance is already running.", file=stderr)

    def stop(self):
        """This method stops the obstacle avoidance algorithm."""
        if self._motor_thread.is_alive() and self._sonar_thread.is_alive():
            self._condition.acquire()
            self._stop_flag = True
            self._condition.notify_all()
            self._condition.release()
            self._sonar_thread.join()
            self._motor_thread.join()
            print("Obstacle avoidance has stopped.", file=stderr)
        else:
            print("Obstacle avoidance is not currently running.", file=stderr)

if __name__ == "__main__":
    """The main method simply runs obstacle avoidance with the default class parameters."""
    algorithm = Obstacle_Avoidance(debug=True)
    algorithm.start()

    # Continue running until we receive a keyboard interrupt (Ctrl+C).
    try:
        while True:
            pass
    finally:
        algorithm.stop()
