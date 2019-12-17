from math import sqrt
class Planet:
    def __init__(self, name: str, loc: tuple, mass: int):
        self.mass = mass
        self.name = name
        self.loc = loc
        self.distance = sqrt(loc[0]**2 + loc[1]**2 + loc[2]**2)
    def __add__(self, other):
        loc = [0]*3
        for i in range(3):
            loc[i] = (self.loc[i]*self.mass + other.loc[i]*other.mass)/(self.mass + other.mass)
        loc = tuple(loc)
        return Planet(self.name + other.name, loc, self.mass + other.mass)
    def __str__(self):
        return 'Planet - ' + self.name
class PlanetSystem:
    def __init__(self, planets: list):
        self.planets = planets
        self.i = 0
    def add(self, planet):
        for i in range(len(self.planets)):
            if self.planets[i].name == planet.name: return
        self.planets.append(planet)
    def delete(self, planet):
        for i in range(len(self.planets)):
            if self.planets[i].name == planet: self.planets.remove(self.planets[i])
    def __iter__(self):
        self.distances = []
        for i in range(len(self.planets)):
            self.distances.append(self.planets[i].distance)
        self.distances.sort()
        return self
    def __next__(self):
        if self.i >= len(self.planets): 
            self.i = 0
            raise StopIteration()
        for i in range(len(self.planets)):
            if self.planets[i].distance == self.distances[self.i]:
                self.i += 1
                return self.planets[i]
if __name__ == "__main__":
    earth = Planet("Earth",(0,0,0),1)
    venus = Planet("Venus",(1,1,1),0.8)
    mercury = Planet("Mercury",(2,2,2),0.5)
    moon =  Planet("Moon",(0,0,1),0.01)
 
    new_planet = mercury + moon
    solar_system = PlanetSystem([venus,earth])
    solar_system.add(new_planet)
    for each in solar_system:
        print(each)
    solar_system.delete("MercuryMoon")
    print("===after_delete===")
    for each in solar_system:
        print(each)