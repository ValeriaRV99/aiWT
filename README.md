Kinetic Energy Density Functional aiwt 
==============================
Package implementing aiWT for hackaton 2023.

This repository is currently under development.
To do a develempment install, clone this repository and type

'pip intall -e .'

in the repository directory.

### Implementation of the package
The KEDF implemented in this package needs to load the training data (https://github.com/ValeriaRV99/aiWT) in the following way

'import hd5py'

'file = h5py.File('data.hdf5', 'r')'

'X = file["Descripotor"]'

'Y = file["rho0"]'

'aiwt=aiWT.airho0(X=X,Y=Y,nat=65,ns=180) # initialize the machine learning fitting'

'path_pp='.../ofpp/EAC/upf/blps/''

'file='si.lda.upf''
'PP_list = {'Si': path_pp+file}'

'ions = bulk('Si', 'diamond', a=5.43, cubic=True)'

'energy = aiWT.airho0.get_energy(ions=ions, PP_list=PP_list, aiwt=aiwt) # predict rho0 and calculate the orbital free energy'

### Theory

In KS-DFFT the kinetic energy of non-interacting electrons $T_{s}$ is  described by the one-electron KS orbitals $\phi (\mathbf{r})$. 

$T_{s}[n]=\sum_{i}\langle \phi_i|-\frac{1}{2}\nabla^2|\phi_i\rangle$

The Kinetic energy depends on the one-electron orbital that scales the computational cost  like $\mathcal{O}(N^3)$. On the other hand, Orbital free Density Functional Theory (OFDFT) is an alternative to KSDFT. However, not just the Exchange-Correlation term needs to be approximated; it is also necessary to approximate the Kinetic energy as a functional of the electronic density (Kenetic energy density functional).

The KEDFT contains the local, semilocal and non-local contribution. Wang and Teter proposed a non-local approximation for $T_{s}$

$T_{WT}[n]=T_{TF}[n]+T_{vW}[n]+\int d\mathbf{r} \int d\mathbf{r}' n^{5/6}(\mathbf{r}) \omega (k_{F},|\mathbf{r} -\mathbf{r}'|)n^{5/6}(\mathbf{r}')$

where $k_{F} = [3\pi^{2}\bar{n}]^{1/3}$ is the fermi wave vector. However, the WT KEDF does not abey the scaling relations.

This code apply the ai, which refers to the machine learning implementation into the Wang-Teter kernel, we named this functional as aiWT Kinetic Energy Density Functional (KEDF).

$T_{NL}[n]=\int d\mathbf{r} d{\mathbf{r}^\prime} n^{5/6}(\mathbf{r}) \omega (k_{TF}^{\alpha}|{\mathbf{r} -\mathbf{r}^\prime}|)n^{5/6}(\mathbf{r}^\prime)$

The aiWT KEDF depends on a new parameter, $\rho_{0}$, which varies with the size of the system. To learn this dependence, we created a database of six phases of silicon, for each phase we decrese and increase the unit cell in thirty points and apply Gaussian process regresion to predict $\rho_{0}$. Additionally, the code performs full OF DFT calculation using the predicted $\rho_{0}$, and returns the $\rho_{0}$ parameter, kinetic energy, and the total energy of the system.   
