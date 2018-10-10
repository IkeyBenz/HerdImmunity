from random import random

class Person:
    def __init__(self, uid, is_vaccinated, virus, infected=None):
        self.uid = uid
        self.is_vaccinated = is_vaccinated
        self.is_alive = True
        self.is_infected = infected
        self.virus = virus

    def interactWith(self, otherPerson):
        if otherPerson.is_infected:
            return (False, 'is already infected')
        return self.virus.attack(otherPerson)

    # Assumes self is infected
    def checkForDeath(self):
        if self.is_infected:
            if self.virus.mortalityRate > random():
                self.is_alive = False
            else:
                self.is_vaccinated = True
                self.is_infected = False