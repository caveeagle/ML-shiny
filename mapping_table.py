import numpy as np
import pandas as pd

BASE_DATASET_PATH = "./data/cleaned_dataset_v4.csv"
df = pd.read_csv(BASE_DATASET_PATH, delimiter=",")

#######################################

# List of valid localities
valid_localities = [
    "antwerp",
    "braine-l-alleud",
    "brussels",
    "gent",
    "laken",
    "liege",
    "lier",
    "mons",
    "mouscron",
    "namur",
    "nivelles",
    "oostende",
    "other",
    "pont-a-celles",
    "roeselare",
    "seraing",
    "tournai",
    "tubize",
    "turnhout",
    "wavre"
]


# Keep only rows where locality is in the valid list
df_filtered = df[df['locality'].isin(valid_localities)]

# Count how many unique valid localities correspond to each postal_code
check = df_filtered.groupby('postal_code')['locality'].nunique().reset_index(name='unique_localities')

# Find postal_codes that map to more than one valid locality
problems = check[check['unique_localities'] > 1]

if not problems.empty:
    print("Inconsistencies found (postal_code maps to MULTIPLE valid localities):")
    print(problems)
else:
    print("All postal_code map to exactly one valid locality or none (OK).")

# For each postal_code, take the first matching locality (there is guaranteed at most one)
mapping = df_filtered.groupby('postal_code')['locality'].first().reset_index()

# Add postal_codes that had no matching locality > assign "None"
all_postal = df[['postal_code']].drop_duplicates()

# Merge to ensure full list of postal codes
mapping_full = all_postal.merge(mapping, on='postal_code', how='left')

# Replace NaN with "None"
mapping_full['locality'] = mapping_full['locality'].fillna("None")

# -------------------------------------------------------------------
# Compute median cadastral_income for each postal_code
# -------------------------------------------------------------------

median_income = (
    df.groupby('postal_code')['cadastral_income']
    .median()
    .reset_index(name='median_cadastral_income')
)

# Merge median income into the final mapping table
mapping_full = mapping_full.merge(median_income, on='postal_code', how='left')

mapping_full.to_csv("./data/postal_code_mapping.csv", index=False, encoding="utf-8")

#######################################

print('Job finished')
