import numpy as np

class Shake:
    def __init__(self, **kwargs):
       self.rules = [] 

    def update_rule(**kwargs):
        pass

    def apply(self, current, neighbors):
        # 0 = 0
        # 1 = 1
        # 2 = L
        # 4 = R
		self.rules.apply(current)
        new = self.margolus(current)
        self.margolus

   def margolus(self, current):
        odd = current[1::2]
        even = current[::2]
        
        #0L
        lstate0 = (odd==0)
        rstateL = (even==2)
        state0L = np.logical_and(lstate0, rstateL).astype(int)

        #R0
        lstateR = (odd==4) 
        rstate0 = (even==0) 
        stateR0 = np.logical_and(lstateR, rstate0).astype(int)

        #R1
        lstateR = (odd==4)
        rstate1 = (even==1)
        stateR1 = np.logical_and(lstateR, rstate1).astype(int)

        #1L
        lstate1 = (odd==1) 
        rstateL = (even==2) 
        state1L = np.logical_and(lstate1, rstateL).astype(int)

        #RL
        lstateR = (odd==4)
        rstateL = (even==2)
        stateRL = np.logical_and(lstateR, rstateL).astype(int)


class state0L:
    def apply(self, odd, even, elasticity):
        #0L
        lstate0 = (odd==0)
        rstateL = (even==2)
        state0L = np.logical_and(lstate0, rstateL).astype(int)

	

        return lstate

class stateR0:
    def apply(self, odd, even, elasticity):
 
        #R0
        lstateR = (odd==4) 
        rstate0 = (even==0) 
        stateR0 = np.logical_and(lstateR, rstate0).astype(int)

class stateR1:
    def apply(self, odd, even, elasticity):
 
        #R1
        lstateR = (odd==4)
        rstate1 = (even==1)
        1 	

class state1L:
    def apply(self, odd, even, elasticity):
 
        #1L
        lstate1 = (odd==1) 
        rstateL = (even==2) 
        state1L = np.logical_and(lstate1, rstateL).astype(int)

class stateRL:
    def apply(self, odd, even, elasticity):
        #RL
        lstateR = (odd==4)
        rstateL = (even==2)
        stateRL = np.logical_and(lstateR, rstateL).astype(int)


