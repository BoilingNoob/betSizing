import pandas as pd
import numpy as np
import sympy as sy
import random as rd

initial_value = 100
coin_perc = 0.6
portion = 0.1
sim_flips = 1000
sim_count = 10_000

def test_portion(start_amt,portion,odds,flips):
    #print("initial conditions: start:",start_amt,"bet portion:",portion,"odds:",odds,"flips:",flips)
    rd.seed()
    for i in range(0,flips):
        if rd.random() < odds:
            start_amt += start_amt*portion
        else:
            start_amt -= start_amt*portion
    return start_amt
def re_test_portioning(start,portion,odds,flips,simcount):
    sims = np.empty(simcount)
    for i in range(0,simcount):
        sims[i] = test_portion(start,portion,odds,flips)
        #print(np.nanmean(sims),"start",start,"portion",portion,"odds",odds,"iterations",flips,i)

    return np.median(sims)
def test_diff_portions(start,portion_start,portion_ends,step,odds,flips,simcount):
    step_count = int((portion_ends - portion_start)/step)
    step_lib = {}
    for i in range(0,step_count):
        current_portion = (i*step) + portion_start
        #print("current portion:",current_portion)
        step_lib[current_portion] = re_test_portioning(start,current_portion,odds,flips,simcount)

    return step_lib

results = test_diff_portions(initial_value,0.005,0.43,0.005,coin_perc,sim_flips,sim_count)

for key, value in results.items():
    print(f"{np.round(key,4)}: {np.round(value,2)}")