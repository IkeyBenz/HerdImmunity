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
        self.itterations = 0
        self.currentlyAlive = populationSize
        self.virus = virus
        self.vacc_percentage = vaccPercentage
        self.currentlyAlive = populationSize
        self.currentlyInfected = 0
        self.currentlyVaccinated = 0
        self.popSize = populationSize
        self.initializePopulation(initialInfected)

    def initializePopulation(self, initialInfected):
        for i in range(self.popSize):
            uid = i
            isVaccinated, isInfected, personsVirus = None, None, None
            if self.currentlyVaccinated < (self.popSize * self.vacc_percentage):
                isVaccinated = True
                self.currentlyVaccinated += 1
            else:
                if self.currentlyInfected < initialInfected:
                    isInfected = True
                    personsVirus = self.virus
                    self.currentlyInfected += 1
                else:
                    isInfected = False
                    isVaccinated = False
                    personsVirus = None
            
            self.population.append(Person(uid, isVaccinated, personsVirus, isInfected))
        print(self.currentlyInfected)

    def runItteration(self):
        self.itterations += 1
        print('Starting itteration #' + str(self.itterations), 
              'Currenly Alive: ' + str(self.currentlyAlive), 
              'Currently Vaccinated: ' + str(self.currentlyVaccinated),
              'Currently Infected: ' + str(self.currentlyInfected), sep="\n")
        alivePeople = []
        sickPeople = []
        for person in self.population:
            if person.is_infected:
                sickPeople.append(person)
            else:
                alivePeople.append(person)

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
                    self.population.pop(person.uid) 
                    deadPeople += 1
                self.logger.log_infection_survival(person, not person.is_alive)
        self.currentlyAlive -= deadPeople
        self.currentlyVaccinated = len([p for p in self.population if p.is_vaccinated])
        self.currentlyInfected = len([p for p in self.population if p.is_infected])
        return deadPeople

    def simulate(self):
        self.logger.write_metadata(len(self.population), self.vacc_percentage, self.virus.name, self.virus.mortalityRate, self.virus.reproductionRate)
        print(self.currentlyAlive, self.currentlyInfected)
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