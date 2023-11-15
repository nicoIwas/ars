import pandas as pd

# Read the csv files into dataframes
brl = pd.read_csv("brasilivre.csv")
brl2 = pd.read_csv("brasilivre2.csv")

# Reset the index of the dataframes
brl = brl.reset_index(drop=True)
brl2 = brl2.reset_index(drop=True)

# Concatenate the dataframes into a single dataframe
final = pd.concat([brl, brl2], axis=1)
print(final)
final.to_csv('brasilivre_final.csv', sep=',', index=False)

# Print the resulting dataframe
