#!/usr/bin/env python3
import cozmo
import time
import asyncio
import subprocess
from cozmo.util import degrees, distance_mm, speed_mmps

class Robot:

    _robot = None

    @staticmethod
    def drive(mm):
        print("Drive")
        _robot.drive_straight(distance_mm(mm), speed_mmps(50)).wait_for_completed()

    @staticmethod
    def command1(method, argument):
        print("command1")
        getattr(_robot, method)(argument).wait_for_completed()

    def __init__(self, robot: cozmo.robot.Robot, obs: Observable):
        global _robot
        _robot = robot
        _obs = obs
        obs.on("drive", Robot.drive)

    def main(self):
        cozmo.logger.info("Press CTRL-C to quit")
        self.get_in_position()
        cozmo.logger.info("RObot: %s", _robot.pose)

        while True:
            print("COZMO is waiting")
            time.sleep(60.0 - time.time() % 60.0)

    def get_in_position(self):
        _robot.set_lift_height(1, in_parallel = True)
        _robot.set_head_angle(degrees(0), in_parallel = True)
        _robot.wait_for_all_actions_completed()
        _robot.say_text("Ich bin bereit!").wait_for_completed()

    def wait_for_cube(self):
        cozmo.logger.info("Wait for Cube")
        cube = _robot.world.wait_for_observed_light_cube(timeout=3600)
        cozmo.logger.info("Found cube %s", cube.cube_id)

        cube.set_lights(cozmo.lights.green_light.flash())
        _robot.set_all_backpack_lights(cozmo.lights.blue_light)
        cozmo.logger.info("Found cube: %s", cube)
        return cube

    def pick_up(self, cube: cozmo.objects.LightCube):
        cozmo.logger.info("pickup cube: %s", cube.cube_id)
        current_action = _robot.pickup_object(cube, num_retries=3)
        current_action.wait_for_completed()

        if current_action.has_failed:
            code, reason = current_action.failure_reason
            result = current_action.result
            print("Pickup Cube failed: code=%s reason='%s' result=%s" % (code, reason, result))

        cube.set_light_corners(None, None, None, None)
        _robot.say_text("Würfel {:d} geladen.".format(cube.cube_id)).wait_for_completed()

    def go_back(self):
        charger = None

        look_around = _robot.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)
        try:
            charger = _robot.world.wait_for_observed_charger(timeout=60)
            cozmo.logger.info("Found charger: %s", charger)
        except asyncio.TimeoutError:
            cozmo.logger.info("Didn't see the charger")
        finally:
            look_around.stop()

        if charger:
            # Attempt to drive near to the charger, and then stop.
            action = _robot.go_to_object(charger, distance_mm(50))
            action.wait_for_completed()
            _robot.set_lift_height(1).wait_for_completed()

            _robot.turn_in_place(degrees(185)).wait_for_completed()
            _robot.drive_straight(action.distance_from_object * -1, speed_mmps(50)).wait_for_completed()

            _robot.backup_onto_charger(10)
            cozmo.logger.info("Done.")

        while not _robot.is_on_charger:
            cozmo.logger.info("Not on charger")
            _robot.drive_straight(distance_mm(-10), speed_mmps(50)).wait_for_completed()

