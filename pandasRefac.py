import pandas as pd
import numpy as np
import sympy as sy
import random as rd

def test_portion_pd(start_amt,portion,odds,flips):
    portion_pass = 1+portion
    portion_lost = 1-portion

    rng = np.random.default_rng()
    rand_array = rng.random(flips)
    flip_frame = pd.DataFrame(rand_array, columns=["flips_result"])
    flip_frame["portion_result"]  = flip_frame["flips_result"] < odds

    grouped = pd.DataFrame.groupby(flip_frame,by="portion_result").count()
    grouped["per_mult"] = grouped.apply(lambda x: portion_pass**x.flips_result if x.name == True else portion_lost**x.flips_result, axis=1)
    total_mult = grouped["per_mult"].prod()
    result_amt = start_amt*total_mult

    return result_amt

def re_test_portioning_median(start,portion,odds,flips,simcount):
    simcount = int(simcount)
    sims = np.empty(simcount)
    for i in range(0,simcount):
        sims[i] = test_portion_pd(start,portion,odds,flips)
    return np.median(sims)

def test_diff_portions_pd(start,portion_start,portion_ends,step,odds,flips,simcount):
    sim_frame = pd.DataFrame(np.arange(portion_start,portion_ends,step),columns=["portion_param"])
    sim_frame["start_amt"] = start
    sim_frame["odds"] = odds
    sim_frame["sim_flips"] = flips
    sim_frame["sim_count"] = simcount

    sim_frame["sim_count"] = sim_frame["sim_count"].astype(int)
    sim_frame["sim_flips"] = sim_frame["sim_flips"].astype(int)

    sim_frame["median_payout"] = sim_frame.apply(lambda x: re_test_portioning_median(x["start_amt"],x["portion_param"],x["odds"],x["sim_flips"].astype(int),x["sim_count"].astype(int)), axis=1)
    sim_frame["median_payout"] = sim_frame["median_payout"].round(0)

    return sim_frame

start = 0.005
step = 0.005
end = 0.6 + step
starting_amt = 100
odds = 0.6
sim_flips = 100
sim_count = 2000

result_frame = test_diff_portions_pd(starting_amt,start,end,step,odds,sim_flips,sim_count)

print("organized:")
print(result_frame.to_string())

print("sorted by median payout:")
print(result_frame.sort_values(by=["median_payout","portion_param"],ascending=[False,True]).to_string())

result_frame.to_csv("portion_sim_results.csv",index=False)