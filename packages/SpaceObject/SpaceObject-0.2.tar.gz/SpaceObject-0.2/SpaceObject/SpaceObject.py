class SpaceObject:
    def __init__ (self, age=0):
        self.age = age        

    def pass_time(self, time):
        self.age += time