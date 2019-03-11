#!/usr/bin/env python3

from threading import Thread
from multiprocessing import Process
from observable import Observable
import time
import cozmo
import web
import robot

obs = Observable()

def robot_starter(cozmo: cozmo.robot.Robot):
    print("################################################################")
    print ("Start Robot")
    print("################################################################")
    r = robot.Robot(cozmo, obs)
    r.main()

def web_starter():
    print("################################################################")
    print ("Start web")
    print("################################################################")
    web.run(obs)

web_thread = Thread(target = web_starter)
web_thread.start()
cozmo.robot.Robot.drive_off_charger_on_connect = True  # If Cozmo can stay on charger to start, set the value to False.
cozmo.run_program(robot_starter, use_viewer=True, force_viewer_on_top=False)
print("Robot stopped!!!")
#requests.get("http://127.0.0.1:5000/shutdown")  #kein Shutdown anschauen
