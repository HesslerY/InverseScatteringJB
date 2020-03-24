'''
Changes Dataset1 from ellipsoid radii to voxels
'''
import numpy as np
import os
import pandas as pd


def insideEllipsoid(radii, point):

    '''
    Calculates whether a voxel midpoint is inside or 
    outside an ellipsoid

    radii - an array of 3 radii defining an ellipsoid 
            in the order (x, y, z)
    point - (x, y, z) of midpoint of voxel
    '''

    a = radii[0]
    b = radii[1]
    c = radii[2]

    x = point[0]
    y = point[1]
    z = point[2]

    return (x/a)**2 + (y/b)**2 + (z/c)**2 < 1

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

def generateEllipsoidVoxels(filename):


    df = pd.read_csv(filename)

    X = df.iloc[:,:400]
    Y = df.iloc[:,400:]

    gridpoints = generateGridPoints()

    y_voxels = pd.DataFrame([[insideEllipsoid(Y.iloc[j], gridpoint) for gridpoint in gridpoints] for j in range(len(Y))])

    df_vox = pd.concat([X.reset_index(drop=True), y_voxels],axis=1, ignore_index=True)

    df_vox.columns = list(range(400)) + [str(i) for i in gridpoints]

    filename1 = 'VoxelsDataset/ellipsoidVoxels/'+os.path.basename(filename)+'.csv'

    return df_vox.to_csv(filename1, index=False)


files =  os.listdir('Dataset1')
files.sort()

for filename in files:
    generateEllipsoidVoxels('Dataset1/'+filename)



