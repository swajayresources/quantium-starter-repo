import pandas as pd
import glob

files = glob.glob("data/daily_sales_data_*.csv")
df = pd.concat([pd.read_csv(f) for f in files],ignore_index=True)

df = df[df["product"] == "pink morsel"]

df["price"] = df["price"].str.replace("$", "", regex=False).astype(float)

df["sales"] = df["quantity"] * df["price"]

result = df[["sales", "date", "region"]]

result.to_csv("data/output.csv", index=False)

print(f"Done. {len(result)} rows  written to data/output.csv")
