Package implementing aiWT for hackaton 2023.

This repository is currently under development.
To do a develempment install, clone this repository and type

'pip intall -e .'

in the repository directory.

The KEDF implemented in this package needs to load the training data in the following way

'import hd5py
file = h5py.File('Data.hdf5', 'r')
X = file["Descripotor"]
Y = file["rho0"]

aiwt=aiWT.airho0(X=X,Y=Y,nat=65,ns=180) # initialize the machine learning fitting

path_pp='.../ofpp/EAC/upf/blps/'
file='si.lda.upf'
PP_list = {'Si': path_pp+file}


ions = bulk('Si', 'diamond', a=5.43, cubic=True)
energy = aiWT.airho0.get_energy(ions=ions, PP_list=PP_list, aiwt=aiwt) # predict rho0 and calculate the orbital free energy'
