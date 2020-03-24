'''
Changes Dataset1 from ellipsoid radii to voxels
'''
import numpy as np
import os
import pandas as pd


def insideCuboid(point, y):

  p0 = y[0]
  p1 = y[1]
  p2 = y[2]

  l0 = y[3]
  l1 = y[4]
  l2 = y[5]

  bool0 = (point[0]>-l0/2) & (point[0]<l0/2)
  bool1 = (point[1]>-l1/2) & (point[1]<l1/2)
  bool2 = (point[2]>-l2/2) & (point[2]<l2/2)


  return bool0 & bool1 & bool2


def generateGridPoints():

    '''
    Generates Gridpoints
    '''

    gridpoints = []
    for z in np.linspace(-2,2,11):
        for y in np.linspace(-2,2,11):
            for x in np.linspace(-2,2,11):
                gridpoints.append([np.round(i, 1) for i in (x,y,z)])

    return gridpoints

def generateCuboidVoxels(filename):


    df = pd.read_csv(filename)

    X = df.iloc[:,:400]
    Y = df.iloc[:,400:]

    gridpoints = generateGridPoints()

    y_voxels = pd.DataFrame([[insideCuboid(Y.iloc[j], gridpoint) for gridpoint in gridpoints] for j in range(len(Y))])

    df_vox = pd.concat([X.reset_index(drop=True), y_voxels],axis=1, ignore_index=True)

    df_vox.columns = list(range(400)) + [str(i) for i in gridpoints]

    filename1 = 'VoxelsDataset/cuboidVoxelsNoOrigin/'+os.path.basename(filename)+'.csv'

    return df_vox.to_csv(filename1, index=False)


files =  os.listdir('Dataset2')
files.sort()

for filename in files:
    generateCuboidVoxels('Dataset2/'+filename)



