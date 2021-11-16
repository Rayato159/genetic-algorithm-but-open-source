# Created by HashTable159

import numpy as np

class ObjFunc:
    def __init__(self):
        # Set attribute here
        pass

    def function(self, x):
        # Set objective function here
        # You must return the objective value in one dimension on this function only !!!
        return (x[0]**2 + x[1] - 11)**2 + (x[0] + x[1]**2 - 7)**2

    def result(self, x):
        # Set return parameters here
        # This function will return the parameters caused by the objective function
        return (x[0], x[1])