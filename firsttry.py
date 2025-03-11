import pandas as pd
import numpy as np
import networkx as nx

df = pd.read_csv('delhivery.csv')
print(df.columns)
print(df.head(10))

# Dropping irrelevant columns
df.drop(['route_schedule_uuid', 'route_type', 'trip_uuid', 'source_center', 'destination_center', 'start_scan_to_end_scan', 'is_cutoff', 'cutoff_factor', 'cutoff_timestamp',   'osrm_distance', 'factor', 'data', 'trip_creation_time','segment_actual_time', 'segment_osrm_time', 'segment_osrm_distance', 'segment_factor', 'od_start_time', 'od_end_time'], axis=1, inplace=True)
# Extracting the names inside the brackets in the 'source_name' and 'destination_name' columns
# df['source_name'] = df['source_name'].str.extract(r'\((.*?)\)')
# df['destination_name'] = df['destination_name'].str.extract(r'\((.*?)\)')


print(df.columns)
print(df.head(10))
print(df.shape)
#remove duplicate rows from the dataframe
df.drop_duplicates(inplace=False)

# Saving the modified DataFrame to a new CSV file
df.to_csv('moddelhivery4.csv', index=False)
