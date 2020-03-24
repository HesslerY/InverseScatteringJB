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

def insideCuboid(point, y):

    '''
    Calculates whether a voxel midpoint is inside or 
    outside an cuboid

    radii - an array of 3 lengths defining an cuboid 
            in the order (x, y, z)
    point - (x, y, z) of midpoint of voxel
    '''

    l0 = y[0]
    l1 = y[1]
    l2 = y[2]

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

def generateEllipsoidVoxels(filename):


    df = pd.read_csv(filename).reset_index()

    X = df.iloc[:,:400]
    Y = df.iloc[:,400:]

    Y.columns = ['k', 'shape', 'origin1', 'origin2', 'origin3', 'length1', 'length2', 'length3']

    gridpoints = generateGridPoints()

    Y1 = np.array([toVoxels(y, gridpoints) for index, y in Y.iterrows()])

    df_vox = pd.concat([X, Y['k'], pd.DataFrame(Y1)], axis=1)

    df_vox.columns = list(range(400)) + ['k'] + [str(i) for i in gridpoints]

    filename1 = 'VoxelsDataset/wavenumberVoxels/'+os.path.basename(filename)+'.csv'

    return df_vox.to_csv(filename1, index=False)

def toVoxels(datapoint, gridpoints):

    gridpoints = generateGridPoints()

    if datapoint['shape']=='e':
        return np.array([insideEllipsoid(datapoint[['length1', 'length2', 'length3']].values, vox)  for vox in gridpoints])

    if datapoint['shape']=='c':
        return np.array([insideCuboid(datapoint[['length1', 'length2', 'length3']].values, vox)  for vox in gridpoints])



files =  os.listdir('Wavenumber')
files.sort()

for filename in files:
    generateEllipsoidVoxels('Wavenumber/'+filename)



