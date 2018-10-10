from person import Person
from random import randint, random, seed
seed(42)
from logger import Logger
from virus import Virus
import sys

class Simulation:
    def __init__(self, populationSize, vaccPercentage, virus, initialInfected = 1):
        self.population = []
        self.logger = Logger('log.txt')
        self.currentlyInfected = 0
        self.currentlyVaccinated = 0
        for i in range(populationSize):
            uid = '0'*(7-len(str(i))) + str(i)
            isVaccinated = random() <= vaccPercentage
            if isVaccinated: self.currentlyVaccinated += 1
            isInfected = not isVaccinated and self.currentlyInfected < initialInfected
            if isInfected: self.currentlyInfected += 1
            personsVirus = virus if isInfected else None
            self.population.append(Person(uid, isVaccinated, personsVirus, isInfected))
        self.itterations = 0
        self.currentlyAlive = populationSize

    def runItteration(self):
        self.itterations += 1
        print('Starting itteration #' + str(self.itterations), 
              'Currenly Alive: ' + str(self.currentlyAlive), 
              'Currently Vaccinated: ' + str(self.currentlyVaccinated),
              'Currently Infected: ' + str(self.currentlyInfected), sep="\n")
        alivePeople = [person for person in self.population if person.is_alive]
        sickPeople = [person for person in self.population if person.is_infected and person.is_alive]

        for sickPerson in sickPeople:
            for _ in range(100):
                victim = alivePeople[randint(0, len(alivePeople)-1)]
                while victim is sickPerson:
                    victim = alivePeople[randint(0, len(alivePeople)-1)]
                didInfect = sickPerson.interactWith(victim)
                if not didInfect: self.currentlyVaccinated += 1
                self.logger.log_interaction(sickPerson, victim, didInfect)

    def surveyDamage(self):
        deadPeople = 0
        for person in self.population:
            if person.is_infected:
                person.checkForDeath()
                if not person.is_alive: 
                    deadPeople += 1
                self.logger.log_infection_survival(person, not person.is_alive)
        self.currentlyAlive -= deadPeople
        self.currentlyVaccinated = len([p for p in self.population if p.is_vaccinated])
        self.currentlyInfected = len([p for p in self.population if p.is_infected])
        return deadPeople

    def simulate(self):
        while self.currentlyAlive > 0 and self.currentlyInfected > 0:
            self.runItteration()
            deadPeople = self.surveyDamage()
            self.logger.log_time_step(deadPeople, self.itterations)
        self.logger.log_file.close()

def main():
    params = sys.argv[1:]
    pop_size = int(params[0])
    vacc_percentage = float(params[1])
    virus_name = str(params[2])
    mortality_rate = float(params[3])
    basic_repro_num = float(params[4])
    virus = Virus(virus_name, basic_repro_num, mortality_rate)
    if len(params) == 6:
        initial_infected = int(params[5])
    else:
        initial_infected = 1
    simulation = Simulation(pop_size, vacc_percentage, virus, initial_infected)
    simulation.simulate()

main()