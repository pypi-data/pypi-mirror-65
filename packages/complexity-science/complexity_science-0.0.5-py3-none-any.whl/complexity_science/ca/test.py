import complexity_science.ca as cs
import numpy as np
import time

def test_wolfram():
    N = 128
    
    a = cs.wolfram(N, [54,20])
    a.initialize_index([64])
    a.run(100)

    #b = cs.CA_nt(100)
    #print(b)
    #TEST FOR MULTIPLE WOLFRAM RULES

def test_brians():
    a = cs.brians_brain([128,128])
    a.animate()

def test_game():
    a = cs.game([128,128])
    a.animate()

def test_brians_and_game_nt():
    a = cs.brians_brain([32,32], toroidal=False)
    b = cs.game([32,32], toroidal=False)
    c = cs.applause([32,32])
    a.animate()
    b.animate()
    c.animate()

def test_applause():
    ca = cs.applause([128,128])
    ca.animate()
    ca.modify_rule(b=1)
    ca.initialize_random_bin(0.9)
    ca.animate()

def test_mpa():
    mpa = cs.mpa([128,128], percent_mpa=0.8)
    mpa.animate()

    mpa.initialize_random()
    mpa.modify_rule(percent_mpa=0.5)
    mpa.animate()

def test_run_collect():
    mpa = cs.mpa([8,8], percent_mpa=0)
    df = mpa.run_collect(200000, collector={'max':np.amax})
    print(df)

if __name__ == '__main__':
    #test_wolfram()
    #test_brians()
    #test_game()
    #test_brians_and_game_nt()
    #test_applause()
    test_mpa()
    #start = time.time()
    #test_run_collect()
    #end = time.time()
    #print(end-start)
