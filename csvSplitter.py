import pandas as pd
from pathlib import Path
import os

def csvSplitter(filename):
    df = pd.read_csv(filename)
    dir_path = os.path.dirname(os.path.realpath(filename))
    foldername = Path(filename).stem
    os.mkdir(dir_path+'/'+foldername)
    for count, i in enumerate(range(0, len(df), 100)):
        df.iloc[i:i+100,:].to_csv(dir_path+'/'+foldername+'/'+foldername+'_{}.csv'.format(count))

for filename in ['VoxelsDataset/ellipsoidVoxels.csv', 'VoxelsDataset/cuboidVoxelsNoOrigin.csv', 
'VoxelsDataset/2ellipsoids.csv', 'VoxelsDataset/wavenumberVoxels.csv']:
    csvSplitter(filename)

