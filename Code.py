#%%
import pandas as pd

# Load the uploaded CSV file
file_path = "/Users/bhumikamallikarjunhorapet/Documents/GWU/Capstone project/coronavirus-data-master/trends/caserate-by-modzcta.csv"
df = pd.read_csv(file_path)

# Display the first few rows to understand the structure
df.head()

# %%
# Convert week_ending to datetime format
df["week_ending"] = pd.to_datetime(df["week_ending"])

# Filter for the range: December 1, 2020 to April 30, 2021
mask = (df["week_ending"] >= "2020-12-01") & (df["week_ending"] <= "2021-04-30")
filtered_df = df.loc[mask]

#%%
# Sum case rates over time for each borough and ZCTA
summed_case_rates = filtered_df.sum(numeric_only=True).to_frame(name="Total_Case_Rate")
summed_case_rates.index.name = "Region"

# Separate boroughs and ZCTAs
borough_case_rates = summed_case_rates.loc[
    summed_case_rates.index.str.startswith("CASERATE_") &
    summed_case_rates.index.str.match(r"CASERATE_(BX|BK|MN|QN|SI)$")
]

#%%
zcta_case_rates = summed_case_rates.loc[
    summed_case_rates.index.str.match(r"CASERATE_\d{5}$")
]

# Rename borough index values for clarity
borough_case_rates.index = borough_case_rates.index.str.replace("CASERATE_", "")
borough_case_rates.index.name = "Borough"

print(zcta_case_rates.head())

zcta_case_rates.reset_index(inplace=True)
zcta_case_rates["ZCTA"] = zcta_case_rates["Region"].str.replace("CASERATE_", "")
zcta_case_rates = zcta_case_rates[["ZCTA", "Total_Case_Rate"]]

# %%
zcta_case_rates.to_csv("zcta_case_rates_dec2020_apr2021.csv", index=False)

# %%
import pandas as pd

# Step 1: Load the income and case rate datasets
income_df = pd.read_csv("/Users/bhumikamallikarjunhorapet/Documents/GWU/Capstone project/coronavirus-data-master/Population_den _edit.csv")
case_rate_df = pd.read_csv("/Users/bhumikamallikarjunhorapet/Documents/GWU/Capstone project/coronavirus-data-master/zcta_case_rates_dec2020_apr2021.csv")

# Step 2: Clean ZCTA codes (remove 'ZCTA5 ' if present)
income_df['ZCTA'] = income_df['ZCTA'].astype(str).str.replace('ZCTA5 ', '')
case_rate_df['ZCTA'] = case_rate_df['ZCTA'].astype(str)

# Step 3: Filter income_df to include only ZCTAs in the case_rate_df
filtered_income_df = income_df[income_df['ZCTA'].isin(case_rate_df['ZCTA'])]
filtered_income_df.to_csv("filtered_median_income_zctas.csv", index=False)

#%%
# Step 4: Optional – merge to see both together
merged_df = pd.merge(case_rate_df, filtered_income_df, on='ZCTA', how='left')

# Step 5: Save to CSV
merged_df.to_csv("filtered_Pop_Den.csv", index=False)

# Preview result
print(merged_df.head())

# %%
