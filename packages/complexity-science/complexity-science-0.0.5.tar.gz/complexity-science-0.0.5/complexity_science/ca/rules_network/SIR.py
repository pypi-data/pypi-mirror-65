import numpy as np

class SIRC_Guillespie:
    def __init__(self, **kwargs):
        """
		S-I-R rule
		S - Susceptible = 0
		I - Infected = 1
		R - Recovered = 2
        ---------------
        Parameters

		---------------
		Returns : None
        """

		self.update_matrix = np.zeros([3,3])
		"""						S I R C update matrix"""
		self.update_matrix[0] = [-1,1,0,0]
		self.update_matrix[1] = [1,1,-1]
		self.update_matrix[2] = [-1,1,1] 
		self.update_matrix[3] = [-1,1,1] 

        self.default = {'alpha' : 0.2,
                        'beta' : 0.2,
                        'gamma' : 0.2,
                        }

        self.update_parameters(**kwargs)

    def update_parameters(self, **kwargs):
        for key, value in kwargs.items():
            self.default[key] = value

        self.alpha = self.default['alpha']
        self.beta = self.default['beta']
        self.gamma = self.default['gamma']

    def apply(self, current, adj):
		self.update_prob(
		choice = np.random.choice(1,2,3, p=[0.5,0.3,0.2])

		increment = (self.update_matrix[choice]*np.ones_like(current)).T
		print(increment)

		result = current+increment
		return result
