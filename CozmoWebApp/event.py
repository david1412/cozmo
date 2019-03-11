from observable import Observable

class Event:
    def __init__(self, obs):
        print("init Event")
        obs.trigger("init", "Init Event")
