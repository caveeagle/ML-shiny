import numpy as np
import pandas as pd

BASE_DATASET_PATH = "../service_data/cleaned_dataset_v4.csv"
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

###########################################################################

# Columns for which we want to compute the median per postal_code
cols_to_process = ['cadastral_income', 'area', 'rooms','number_floors',
                   'bathrooms', 'toilets','facades_number','primary_energy_consumption']   

for col in cols_to_process:
    # Median per postal_code
    median_table = (
        df.groupby('postal_code')[col]
          .median()
          .reset_index(name=f'median_{col}')
    )

    # Global median for this column
    global_median = df[col].median()

    # Replace NaN with global median
    median_table[f'median_{col}'] = median_table[f'median_{col}'].fillna(global_median)

    # Merge into the final mapping table
    mapping_full = mapping_full.merge(median_table, on='postal_code', how='left')

###########################################################################

###########################################################################
# Add synthetic region N1 with global medians
###########################################################################

# Build a dict for the new row
synthetic_row = {"postal_code": 1, "locality": "None"}

for col in cols_to_process:
    global_median = df[col].median()
    synthetic_row[f"median_{col}"] = global_median

# Append the new row
mapping_full = pd.concat(
    [mapping_full, pd.DataFrame([synthetic_row])],
    ignore_index=True
)

###########################################################################
###########################################################################


mapping_full = mapping_full.sort_values(by='postal_code')

mapping_full.to_csv("../data/postal_code_mapping.csv", index=False, encoding="utf-8")

#######################################

print('Job finished')
