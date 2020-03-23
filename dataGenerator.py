import bempp.api
import csv

from scipy.special import sph_harm
import numpy as np
import scipy.io as sio
import io
import random

from scipy.linalg import lstsq
from matplotlib import pyplot as plt

import numpy as np
import matplotlib.cm as cm
from scipy.spatial import Delaunay
from functools import reduce

#defining wavenumber
k=1

@bempp.api.complex_callable
def dirichlet_fun(x, n, domain_index, result):
    result[0] = np.exp(1j * k * x[0])

@bempp.api.complex_callable
def neumann_fun(x, n, domain_index, result):
    result[0] = 1j * k * n[0] * np.exp(1j * k * x[0])

class DataGenerator:
    def __init__(self,h = 0.3, max_degree =3):
        '''
        h - meshsize
        k - wavenumber
        data - list of all data points
        dirichlet_grid_fun - dirichlet grid function
        neumann_grid_fun - neumann grid function
        '''
        self.h = h

        self.dirichlet_grid_fun = None
        self.neumann_grid_fun = None

        self.data = []
        self.theta = np.linspace(0, 2 * np.pi, 400)

    def generateData(self, n):
        '''
        Generates Data
        '''
        for i in range(n):
            lengths = np.array([random.uniform(2/3, 2) for i in range(3)])
            grid = bempp.api.shapes.ellipsoid(r1=lengths[0], r2=lengths[1], r3=lengths[2], h = self.h)
            total_field, info, it_count, space = self.calculateTotalField(grid)
            db_pattern = self.calculate_db_pattern(space, total_field)
            data1 =  db_pattern.tolist() + centres.tolist() + lengths.tolist()
            self.data.append(data1)
        return self.data

    def calculateTotalField(self, grid):
        '''Takes a wavenumber k and grid and calculates total
        field.

        Make sure grid is not too fine, otherwise it will take too long.

        Returns the total field, info, number of iterations and the
        function space (that is calculated from the grid.)
        '''
        space = bempp.api.function_space(grid, "P", 1)
        #print("The space has {0} dofs".format(space.global_dof_count))
        identity = bempp.api.operators.boundary.sparse.identity(
            space, space, space)
        dlp = bempp.api.operators.boundary.helmholtz.double_layer(
            space, space, space, k)
        hyp = bempp.api.operators.boundary.helmholtz.hypersingular(
            space, space, space, k)

        #Replacing ntd with 1/ik
        ntd = 1/1j*k

        burton_miller = .5 * identity - dlp - ntd * hyp

        self.dirichlet_grid_fun = bempp.api.GridFunction(space, fun=dirichlet_fun)
        self.neumann_grid_fun = bempp.api.GridFunction(space, fun=neumann_fun)
        rhs_fun = self.dirichlet_grid_fun - ntd * self.neumann_grid_fun

        total_field, info, it_count = bempp.api.linalg.gmres(
            burton_miller, rhs_fun, use_strong_form=True,
            return_iteration_count=True,)
        return total_field, info, it_count, space

    def calculate_db_pattern(self, space, total_field):
        '''
        Takes an argument of Space and Total Field
        Calculates Far-Field Pattern
        Returns the Far-Field Pattern and the respective
        '''
        #bempp.api.global_parameters.assembly.potential_operator_assembly_type = 'dense'
        pylab.rcParams['figure.figsize'] = (8.0, 8.0)

        points = np.array([np.cos(self.theta), np.sin(self.theta), np.zeros(len(self.theta))])
        dlp_far_field = bempp.api.operators.far_field.helmholtz.double_layer(
            space, points, k)
        far_field = dlp_far_field * total_field
        max_incident = np.abs(self.dirichlet_grid_fun.coefficients).max()
        radiation_pattern = (np.abs(far_field/max_incident)**2).ravel()
        db_pattern = 10 * np.log10(4 * np.pi * radiation_pattern)
        return db_pattern

    def writeCSV(self, filepath):
        '''
        Writes the data to a csv with column names for the first entry
        '''

        label_dim = 6
        feature_dim = len(self.theta)
        columns = ['feature_'+str(i+1) for i in range(feature_dim)] + ['label_'+str(i+1) for i in range(label_dim)]

        self.data.insert(0, columns)

        with open(filepath, 'w') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerows(self.data)
        csvFile.close()
        self.data.remove(columns)
        return self.data

for i in range(100):
    dg = DataGenerator(h=0.3)
    dg.generateData(100)
    dg.writeCSV('Ellipsoids/EllipsoidData_%d.csv' % i)
