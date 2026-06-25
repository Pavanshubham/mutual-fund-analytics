import pandas as pd
import os

# main folder path
DATA_PATH = "data/raw"

# get all csv filesfrom raw folder and make list of csv files 
csv_files = [f for f in os.listdir(DATA_PATH)
             if f.endswith(".csv")]

# calculate how many csv files in raw folder
print(f"\nFound {len(csv_files)} files\n")

for file in csv_files:

    path = os.path.join(DATA_PATH,file)

    print("="*80)
    # print csv file name
    print(f"Dataset : {file}")
    
    # load csv file in  
    df = pd.read_csv(path)
    
    # dataset shape
    print("\nShape:")
    print(df.shape)

    # dataset data type
    print("\nData Types:")
    print(df.dtypes)

    # dataset top 5 rows
    print("\nFirst 5 Rows:")
    print(df.head())

    # check missing values in dataset
    print("\nMissing Values:")
    print(df.isnull().sum().sum())

    print("="*80)