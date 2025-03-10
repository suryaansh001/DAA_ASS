import pandas as pd
import numpy as np
import networkx as nx

df = pd.read_csv('moddelhivery2.csv')
# print(df.info())
# null values
print("null values", df.isnull().sum())
# fill null values in source_name and destination_name randomly with 'Rajasthan' and 'Uttar Pradesh'
df['source_name'].fillna('Rajasthan', inplace=True)
df['destination_name'].fillna('Uttar Pradesh', inplace=True)
print("null values after filling", df.isnull().sum())

# List of replacement values
replacement_values = ['Delhi', 'Karnataka', 'Bihar']

# Replace destination_name with a random value from the list if source_name == destination_name
df.loc[df['source_name'] == df['destination_name'], 'destination_name'] = np.random.choice(replacement_values, df[df['source_name'] == df['destination_name']].shape[0])

print(df.head(10))
# print the unique values in source_name and destination_name
print("unique values in source_name", df['source_name'].unique())
#create a new columns named efficiency that is equals to actualtime/osrmtime
df['efficiency'] = df['actual_time'] / df['osrm_time']
print(df.isnull().sum())
df.drop(['actual_time', 'osrm_time'], axis=1, inplace=True)

df.to_csv('final2_delhivery.csv', index=False)