import numpy as np


class Class1(object):
    """
    A test class to check basic functionality
    """
    def __init__(self, x: int):
        self.x = x

    def info(self):
        """
        test method to return the only parameter

        Returns
        -------

        """
        print(f'The value entered is {self.x}')

    def square_root(self):
        """
        Return the square-root of the initial parameter
        Used to test the requirements

        Returns
        -------

        """
        return np.sqrt(self.x)
