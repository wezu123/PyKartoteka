import pandas as pd

zgony = pd.read_csv("zgony.csv", sep=",", dtype="str", header=None)
print(zgony[0][10])