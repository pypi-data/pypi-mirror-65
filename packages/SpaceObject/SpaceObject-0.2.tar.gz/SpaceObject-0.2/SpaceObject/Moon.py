from .SpaceObject import SpaceObject

class Moon(SpaceObject):
    def __init__ (self, planet =[], age=0):
        self.age =age 
        self.planet = planet

    def pass_time(self, time):
        self.age += time
        return self.age
       
    def set_planet(self, planet):
        self.planet = planet

    def __repr__(self):
        name = 'No Planet Associated'
        if self.planet != []:
            name = self.planet.get_name()
        return 'Age: {}, Planet: {}'.format(self.age, name)
                   