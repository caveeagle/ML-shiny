import numpy as np
import pandas as pd

#BASE_DATASET_PATH = "../service_data/cleaned_dataset_v4.csv"
BASE_DATASET_PATH = "../service_data/base_dataset.csv"

df = pd.read_csv(BASE_DATASET_PATH, delimiter=",")

#######################################

#count_gent = (df['locality'] == 'gent').sum()
#print(count_gent)  # 328 | 262

#print( df.info() )

col = 'running_water'

fraction = df[col].value_counts(normalize=True).iloc[0]

print(fraction)
 

#######################################

print('Job finished')
