#!/usr/bin/python3

from sonar import Sonar
from threading import Thread, Condition
from copy import deepcopy
from sys import stderr
from time import sleep
from enum import Enum
import dual_mc33926

class Obstacle_Avoidance:
    """
    A class for performing obstacle avoidance by running a sonar thread and a motor control thread
    in parallel.

    Attributes:
        turn_time (float):      How long (in seconds) the rover should turn left or right.
        reverse_time (float):   How long (in seconds) the rover should reverse.
        turn_dist (int):        How close an obstacle must be (in mm) before the rover turns.
        reverse_dist (int):     How close an obstacle must be (in mm) before the rover reverses.
        offset (float):         Since the wheels aren't straight, one wheel will turn slower.
        flip (bool):            Flag that allows the class to account for reverse wheel wiring.
    """

    class Direction(Enum):
        """This enumerates the possible directions the rover can move/turn."""
        FORWARD  = 1
        BACKWARD = 2
        RIGHT    = 3
        LEFT     = 4

    def __init__(self, threshold=0.1, buffer_size=5, turn_time=1, reverse_time=1, turn_dist=1000,
                 reverse_dist=500, offset=0.8, flip=False):
        """
        Constructs an Obstacle_Avoidance object using a series of overridable default parameters.

        Keyword Arguments:
            threshold (float):      What threshold value to pass to the Sonar object.
            buffer_size (int):      What buffer_size value to pass to the Sonar object.
            turn_time (float):      Refer to the turn_time class attribute.
            reverse_time (float):   Refer to the reverse_time class attribute.
            turn_dist (int):        Refer to the turn_dist class attribute.
            reverse_dist (int):     Refer to the reverse_dist class attribute.
            offset (float):         Refer to the offset class attribute.
            flip (bool):            Refer to the flip class attribute.
        """
        self.turn_time    = turn_time
        self.reverse_time = reverse_time
        self.turn_dist    = turn_dist
        self.reverse_dist = reverse_dist
        self.offset       = offset
        self.flip         = flip
        self._sonar_data  = (0, b'')
        self._condition   = Condition()
        self._stop_flag   = False
        self._sonar       = Sonar(threshold=threshold, buffer_size=buffer_size)
        self._motor       = dual_mc33926.MotorDriver()
        self._running     = False

    def _run_sonar(self):
        """Continously runs the sonars and notifies the motor thread whenever an object is close."""
        while True:
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
        max = 480   # The motor's max speed.
        flip = self.flip

        def move(direction=Direction.FORWARD, duration=None):
            """
            Helper method which simply moves/turns the rover in a given direction.

            Keyword Arguments:
                direction (Direction):  The direction the rover should turn/move.
                duration (float):       How long the rover should move in this direction.
            """
            # First, stop whatever the motors were doing before.
            self._motor.disable()

            # If the flip flag is set, movement is reversed.
            if flip:
                if direction == Direction.FORWARD:
                    motor_driver.set_speeds(max, 1, max * offset, 1)
                elif direction == Direction.BACKWARD:
                    motor_driver.set_speeds(max, 0, max * offset, 0)
                elif direction == Direction.RIGHT:
                    motor_driver.set_speeds(0, 1, max * offset, 1)
                else:
                    motor_driver.set_speeds(max, 1, 0, 1)

            # Otherwise, perform standard movement.
            else:
                if direction == Direction.FORWARD:
                    motor_driver.set_speeds(max, 1, max * offset, 1)
                elif direction == Direction.BACKWARD:
                    motor_driver.set_speeds(max, 0, max * offset, 0)
                elif direction == Direction.RIGHT:
                    motor_driver.set_speeds(max, 1, 0, 1)
                else:
                    motor_driver.set_speeds(0, 1, max * offset, 1)

            # Start moving.
            self._motor.enable()

            # Wait for a duration (if specified) before accepting another move command.
            if (type(duration) in [int, float]) and (duration >= 0):
                sleep(duration)
            else:
                raise ValueError("Invalid duration")

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

    def start(self):
        """This method starts the obstacle avoidance algorithm."""
        if not self._running:
            self._sonar_thread = Thread(target=self._run_sonar, daemon=True)
            self._motor_thread = Thread(target=self._run_motor, daemon=True)
            self._sonar_thread.start()
            self._motor_thread.start()
            self._running = True
            print("Obstacle avoidance is now running.", file=stderr)
        else:
            print("Obstacle avoidance is already running.", file=stderr)

    def stop(self):
        """This method stops the obstacle avoidance algorithm."""
        if self._running:
            self._condition.acquire()
            self._stop_flag = True
            self._condition.notify_all()
            self._condition.release()
            self._sonar_thread.join()
            self._motor_thread.join()
            self._running = False
            print("Obstacle avoidance has stopped.", file=stderr)
        else:
            print("Obstacle avoidance is not currently running.", file=stderr)

if __name__ == "__main__":
    """The main method simply runs obstacle avoidance with the default class parameters."""
    algorithm = Obstacle_Avoidance()
    algorithm.start()

    # Continue running until we recieve a keyboard interrupt (Ctrl+C).
    try:
        while True:
            pass
    except KeyboardInterrupt:
        algorithm.stop()
