from random import random

class Virus:
    def __init__(self, name, reproductionRate, mortalityRate):
        self.name = name
        self.reproductionRate = reproductionRate
        self.mortalityRate = mortalityRate

    def attack(self, person):
        if person.is_vaccinated:
            return (False, 'was vaccinated')
        if self.reproductionRate > random():
            person.infected = True
            person.virus = self
            return (True, 'is weak')
        return (False, 'got lucky')

