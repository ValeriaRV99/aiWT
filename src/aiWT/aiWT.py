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
    def __init__(ions,fileX,fileY,nat=None,ns=None):

        if nat is not None:
            if nat < len(ions):
                raise Exception ("nat in airho0 should be larger than the number of atoms")
            self.nat=nat
        
        if ns is not None:
            if ns==0:
                raise Exception ("you must have at least one sample in airho0!")
            self.ns=ns

        kernel = ConstantKernel(constant_value=1.0, constant_value_bounds=(1.e-09, 1.e+08)) * Exponentiation(RationalQuadratic(), exponent=1) + WhiteKernel(
         noise_level=1e-2, noise_level_bounds=(1e-25, 1e1)
))
        model = GaussianProcessRegressor(kernel=kernel, random_state=0)
        X_ref = np.load(fileX)
        y_ref = np.load(fileY)
        model.fit(X_ref, y_ref)
        self.model = model
 

    def rho0(self,ions):
        ions = Ions.from_ase(ions)
        sine = SineMatrix(n_atoms_max=self.nat)
        sine_matrices = sine.create(ions)
        X_pol = np.asarray(sine_matrices)
        y_pred = self.model.predict(X_pol.reshape(1, -1))
        pred_rho0 = np.zeros(y_pred.shape[0])
        return pred_rho0[0][0]

                
# %%
def ml_model():
    kernel = ConstantKernel(constant_value=1.0, constant_value_bounds=(1.e-09, 1.e+08)) * Exponentiation(RationalQuadratic(), exponent=1) + WhiteKernel(
    noise_level=1e-2, noise_level_bounds=(1e-25, 1e1)
)
    model = GaussianProcessRegressor(kernel=kernel, random_state=0)
    X_ref = np.load('/home/valeria/Documents/DFTPY/cWT-KEDF/Phases/Model_ML_function/training_set_data/organize_data/SM_Btin_fcc_bcc_8cd_dhcp_Btin-hd_65.npy')
    y_ref = np.load('/home/valeria/Documents/DFTPY/cWT-KEDF/Phases/Model_ML_function/training_set_data/organize_data/rho0_Btin_fcc_bcc_8cd_dhcp_Btin-hd_65.npy')
    X = X_ref
    y = y_ref
    model.fit(X, y)
    return model


# %%
def get_energy(material, PP_list, aiwt):
    import copy
    ml_material = copy.deepcopy(material)
    of_material = copy.deepcopy(material)
    charge = int(charge)
    phase = phase
    PP_list = PP_list
    XC = Functional(type='XC',name='LDA')
    HARTREE = Functional(type='HARTREE')
    pred_KE = Functional(type='KEDF',name='WT', rho0=aiwt.rho0(ions))
    ions = Ions.from_ase(of_material)
    cell = ions.get_cell()
    ions.set_charges(charge)

    nr = ecut2nr(ecut=25, lattice=ions.cell)
    grid = DirectGrid(lattice=ions.cell, nr=nr)
    rho_ini = DirectField(grid=grid)
    rho_ini[:] = ions.get_ncharges()/ions.cell.volume
    PSEUDO = LocalPseudo(grid = grid, ions=ions, PP_list=PP_list, rcut=20)
    predevaluator = TotalFunctional(KE=pred_KE, XC=XC, HARTREE=HARTREE, PSEUDO=PSEUDO)
    optimization_options = {'econv' : 1e-5*ions.nat}
    optpred = Optimization(EnergyEvaluator=predevaluator, optimization_options = optimization_options, 
                       optimization_method = 'TN')
    predrho = optpred.optimize_rho(guess_rho=rho_ini)
    predenergy = predevaluator.Energy(rho=predrho, ions=ions)
    predke = pred_KE(predrho).energy
    vol = ions.get_volume()
    return np.asarray(vol), np.asarray(predenergy), np.asarray(predke)



## Your code in Jupyter Notebook:

fileX='/home/valeria/Documents/DFTPY/cWT-KEDF/Phases/Model_ML_function/training_set_data/organize_data/SM_Btin_fcc_bcc_8cd_dhcp_Btin-hd_65.npy'
fileY='/home/valeria/Documents/DFTPY/cWT-KEDF/Phases/Model_ML_function/training_set_data/organize_data/rho0_Btin_fcc_bcc_8cd_dhcp_Btin-hd_65.npy'
aiwt=airho0(ions=ions,fileX=fileX,fileY=fileY,nat=65,ns=180)

# or define your calculator
get_energy(bla bla bla)




