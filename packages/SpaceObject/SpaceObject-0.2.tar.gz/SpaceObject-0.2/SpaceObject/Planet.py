from .SpaceObject import SpaceObject

class Planet(SpaceObject):
    def __init__(self, age, population, name):
        super().__init__(age)
        self.population = population
        self.name = name
    
    def add_settlers(self, new_population=1):
        self.population += new_population
        
    def check_population(self):
        return self.population
    
    def get_name(self):
        return self.name
    
    def __repr__(self):
        return 'Name: {}, Age: {}, Population: {}'.format(self.name, self.age,self.population)