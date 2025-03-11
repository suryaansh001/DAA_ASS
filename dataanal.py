import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

df=pd.read_csv('final2_delhivery.csv')
print(df.columns)

#printing the graph of high frequencyof names  in source 
# plt.figure(figsize=(10,6))
# df['source_name'].value_counts().head(10).plot(kind='bar')
# plt.title('Top 10 source names')
# plt.xlabel('source name')
# plt.ylabel('frequency')
# plt.show()


#finding the maximum distance and its corresponding source and destination
max_distance_row = df.loc[df['actual_distance_to_destination'].idxmax()]
max_distance = max_distance_row['actual_distance_to_destination']
source = max_distance_row['source_name']
destination = max_distance_row['destination_name']

print(f"The maximum distance is {max_distance} between {source} and {destination}")

#finding the minimum distance and its corresponding source and destination
min_distance_row = df.loc[df['actual_distance_to_destination'].idxmin()]
min_distance = min_distance_row['actual_distance_to_destination']
source = min_distance_row['source_name']
destination = min_distance_row['destination_name']

print(f"The minimum distance is {min_distance} between {source} and {destination}")
#findin the efficiency of the path

max_efficiency_row = df.loc[df['efficiency'].idxmax()]
max_efficiency = max_efficiency_row['efficiency']
source = max_efficiency_row['source_name']
destination = max_efficiency_row['destination_name']    

print(f"The maximum efficiency is {max_efficiency} between {source} and {destination}")

min_efficiency_row = df.loc[df['efficiency'].idxmin()]
min_efficiency = min_efficiency_row['efficiency']
source = min_efficiency_row['source_name']
destination = min_efficiency_row['destination_name']

print(f"The minimum efficiency is {min_efficiency} between {source} and {destination}")