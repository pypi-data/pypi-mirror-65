import numpy as np

class Migration:
    def __init__(self, **kwargs):
        """
		Migration rule
        ---------------
        Parameters


		---------------
		Returns:
			Population array after movement.
        """
        self.itr = 0
        self.default = {'m' : 1
                        }
        self.update_parameters(**kwargs)

    def update_parameters(self, **kwargs):
        for key, value in kwargs.items():
            self.default[key] = value

        self.m = self.default['m']

    def apply(self, current, adj):
        self.itr+=1
        result = current
        if (self.itr%10 == 0):
            result = self.move(current)

        return result
    def move(self, current):
        pass
        

