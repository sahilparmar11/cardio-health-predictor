import pandas as pd

df = pd.read_csv("../../data/cardio_preprocessed.csv")
print("Columns:", df.columns)
print("ap_lo unique values (head 20):", df['ap_lo'].unique()[:20])
print("ap_lo description:")
print(df['ap_lo'].describe())
