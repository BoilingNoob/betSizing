import pandas as pd
import numpy as np
import sympy as sy
import random as rd
import matplotlib.pyplot as plt

result_df = pd.read_csv("portion_sim_results.csv")

print_df = result_df[["portion_param","median_payout"]].copy()



print(print_df.to_string())

print_df["slope"]=(print_df["median_payout"] - print_df["median_payout"].shift(1)) / (print_df["portion_param"] - print_df["portion_param"].shift(1))
print_df["slope_abs"] = print_df["slope"].abs()

print_df.plot(x="portion_param",y=["median_payout","slope"],title="Median Payout vs Portion Size",xlabel="Portion Size",ylabel="Median Payout",grid=True,legend=False)

best_criteria = print_df.sort_values(by=["slope_abs"],ascending=[True]).head(1)
print(best_criteria.to_string())

plt.show()
