#!/usr/bin/env python
# coding: utf-8
# %%


import numpy as np
from matplotlib import pyplot as plt

from dftpy.ions import Ions
from dftpy.field import DirectField
from dftpy.grid import DirectGrid
from dftpy.functional import LocalPseudo, Functional, TotalFunctional, ExternalPotential
from dftpy.formats import io
from dftpy.math_utils import ecut2nr
from dftpy.optimization import Optimization

from sklearn.gaussian_process.kernels import Exponentiation, RationalQuadratic, ConstantKernel, WhiteKernel
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.kernel_ridge import KernelRidge
from dscribe.descriptors import SineMatrix
from ase import Atoms

class airho0(object):
    def __init__(self,ions,X=None, Y=None, nat=None,ns=None):
        # if X is not None:
        self.X = X
        self.Y = Y
        # else:
        #     path= get_python_lib()
        #     file = h5py.File(path+"/aiwt/data.hdf5", 'r') 
        #     self.X = file["Descriptor"] 
        #     self.Y = file["rho0"]
        #     file.close
        
        if nat is not None:
            if nat < len(ions):
                raise Exception ("nat in airho0 should be larger than the number of atoms")
            self.nat=nat
        
        if ns is not None:
            if ns==0:
                raise Exception ("you must have at least one sample in airho0!")
            self.ns=ns

        kernel = ConstantKernel(constant_value=1.0, constant_value_bounds=(1.e-09, 1.e+08)) * Exponentiation(RationalQuadratic(), exponent=1) + WhiteKernel(
         noise_level=1e-2, noise_level_bounds=(1e-25, 1e1))
        model = GaussianProcessRegressor(kernel=kernel, random_state=0)
        model.fit(self.X, self.Y)
        self.model = model
 

    def rho0(self,ions):
        sine = SineMatrix(n_atoms_max=self.nat)
        sine_matrices = sine.create(ions)
        X_pol = np.asarray(sine_matrices)
        y_pred = self.model.predict(X_pol.reshape(1, -1))
        return y_pred[0][0]
    
    def get_energy(ions, PP_list, aiwt):
        import copy
        # self.ions=ions
        PP_list = PP_list
        XC = Functional(type='XC',name='LDA')
        HARTREE = Functional(type='HARTREE')
        ions = Ions.from_ase(ions)
        rho00 = aiwt.rho0(ions)
        KE = Functional(type='KEDF',name='WT', rho0=rho00)

        nr = ecut2nr(ecut=25, lattice=ions.cell)
        grid = DirectGrid(lattice=ions.cell, nr=nr)
        PSEUDO = LocalPseudo(grid = grid, ions=ions, PP_list=PP_list, rcut=20)
        rho_ini = DirectField(grid=grid)
        rho_ini[:] = ions.get_ncharges()/ions.cell.volume
        evaluator = TotalFunctional(KE=KE, XC=XC, HARTREE=HARTREE, PSEUDO=PSEUDO)
        optimization_options = {'econv' : 1e-5*ions.nat}
        opt = Optimization(EnergyEvaluator=evaluator, optimization_options = optimization_options, 
                            optimization_method = 'TN')
        
        rho = opt.optimize_rho(guess_rho=rho_ini)
        energy = evaluator.Energy(rho=rho, ions=ions)
        ke = KE(rho).energy
        vol = ions.get_volume()
        print('Volume = ', np.asarray(vol)), print('Kinetic energy (Ha)= ', np.asarray(ke)), print('Total energy (Ha) = ', np.asarray(energy))
        return rho00, ke, np.asarray(energy)
