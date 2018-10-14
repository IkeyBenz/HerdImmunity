import matplotlib.pyplot as plt

class Grapher:
    def __init__(self, params, virus):
        self.plots = {}
        self.itterations = 0
        self.virusName = virus
        for param in params:
            self.plots[param] = []
    
    def recordPointsForItteration(self, values):
        self.itterations += 1
        for param, value in values.items():
            self.plots[param].append(value)
    
    def show(self):
        xCoords = [i for i in range(self.itterations)]
        for param, yCoords in self.plots.items():
            plt.plot(xCoords, yCoords, label=param)

        plt.title("Herd Immunity Stats For " + self.virusName)
        plt.xlabel('Itteration Number')
        plt.ylabel('Number of People')

        plt.legend()
        plt.show()