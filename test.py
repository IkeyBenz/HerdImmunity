from simulation import Simulation
from virus import Virus

def testNewSimDefault():
    simVirus = Virus('Ebola', 0.5, 0.3)
    sim = Simulation(100, 0.4, simVirus)
    assert sim.currentlyInfected == 1

def testNewSimProps():
    simVirus = Virus('Ebola', 0.5, 0.3)
    sim = Simulation(100, 0.4, simVirus, 50)
    assert sim.currentlyInfected == 50
    assert sim.currentlyAlive == 100
    assert sim.currentlyVaccinated == 40
    assert sim.virus.name == 'Ebola'

def testSimAfterComplete():
    simVirus = Virus('Ebola', 0.5, 0.3)
    sim = Simulation(100, 0.4, simVirus, 50)
    sim.simulate()
    # Make sure they either all died and were removed from population
    # Or that they all go vaccinated and they're no longer infected
    assert len([person for person in sim.population if person.is_infected]) == 0