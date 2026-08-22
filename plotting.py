import pandas as pd
import numpy as np
import sympy as sy
import random as rd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.differentiate import derivative

result_df = pd.read_csv("portion_sim_results.csv")

print_df = result_df[["portion_param","median_payout"]].copy()

def normal_dist_func(x,mu,sigma,a):
    return a*np.exp(-((x-mu)**2)/(2*sigma**2))


initial_guesses = [1,1,1]

popt, pcov = curve_fit(normal_dist_func, print_df["portion_param"], print_df["median_payout"], p0=initial_guesses)

my_derivative_y = derivative(normal_dist_func, print_df["portion_param"], args=tuple(popt),preserve_shape=True).df #.values()

functionilzed = pd.DataFrame({"portion_param":print_df["portion_param"],"median_payout":normal_dist_func(print_df["portion_param"], *popt)})
best_one = functionilzed.sort_values(by="median_payout",ascending=False).head(1)

print("best value:")
print(best_one.to_string())


plt.scatter(print_df["portion_param"], print_df["median_payout"], color='red', label='Noisy Data')
plt.plot(print_df["portion_param"], normal_dist_func(print_df["portion_param"], *popt), color='blue', label='Fitted Curve', linewidth=2)
plt.plot(print_df["portion_param"], my_derivative_y, color='green', label='derivative Curve', linewidth=2)
plt.plot(best_one["portion_param"], best_one["median_payout"], marker='o', markersize=5, color='orange', label='Best Point')

plt.legend()
plt.show()
