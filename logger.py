import matplotlib.pyplot as plt 

class Logger:
    def __init__(self, file_name):
        
        self.log_file = open(file_name, 'w')

    def write_metadata(self, pop_size, vacc_percentage, virus_name, mortality_rate, basic_repro_num):
        outputString =  'Population Size: ' + str(pop_size) + '\n'
        outputString += "% of people vaccinated: " + str(vacc_percentage) + '\n'
        outputString += "Virus: " + virus_name + '\n'
        outputString += 'Mortality Rate: ' + str(mortality_rate) + '\n'
        self.log_file.write(outputString)

    def log_interaction(self, person1, person2, did_infect=None):
        data = (person1.uid,
                'infected' if did_infect[0] else 'did not infect',
                person2.uid, person2.uid, did_infect[1])
        log = '%s %s %s because %s %s' % data
        self.log_file.write(log + '\n')

    def log_infection_survival(self, person, did_die_from_infection):
        data = (person.uid, 'died' if did_die_from_infection else 'did not die')
        log = '%s %s from the infection.' % data
        self.log_file.write(log + '\n')

    def log_time_step(self, number_of_dead, time_step_number):
        log = 'End of itteration %i. Number of people who died: %d' % (time_step_number, number_of_dead)
        self.log_file.write(log + '\n')

        