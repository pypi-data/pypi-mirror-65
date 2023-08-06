#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  1 15:11:33 2019

@author: Gabriele Coiana
"""
import numpy as np
from scipy.optimize import curve_fit
from decomp import  read,  util
import os, sys

## =============================================================================
## Parameters
input_file = sys.argv[1]
a = read.read_parameters(input_file)[0]
Masses = read.read_parameters(input_file)[1]
n_atom_unit_cell = read.read_parameters(input_file)[2]
n_atom_conventional_cell = read.read_parameters(input_file)[3]
N1,N2,N3 = read.read_parameters(input_file)[4:7]
kinput = read.read_parameters(input_file)[7::][0]
file_eigenvectors = read.read_parameters(input_file)[8]
file_trajectory = read.read_parameters(input_file)[9]
file_initial_conf = read.read_parameters(input_file)[10]
system = read.read_parameters(input_file)[11]
DT = read.read_parameters(input_file)[12]
tau = read.read_parameters(input_file)[13]
T = read.read_parameters(input_file)[14]



tot_atoms_uc = int(np.sum(n_atom_unit_cell)) 
tot_atoms_conventional_cell = int(np.sum(n_atom_conventional_cell)) 
N1N2N3 = N1*N2*N3 # Number of cells
N = N1*N2*N3*tot_atoms_uc    # Number of atoms
masses, masses_for_animation = util.repeat_masses(Masses, n_atom_conventional_cell, n_atom_unit_cell, N1, N2, N3)
cH = 1.066*1e-6 # to [H]
cev = 2.902*1e-05 # to [ev]
kbH = 3.1668085639379003*1e-06# a.u. [H/K]
kbev = 8.617333262*1e-05 # [ev/K]
#### =============================================================================

print('\nHello, lets start!\n')
print('Getting input parameters...')
print(' System: ', system)
print(' Masses: ', Masses)
print(' Number of atoms per unit cell', n_atom_unit_cell)
print(' Supercell: ', N1, N2, N3)
print(' k path: ', [x.tolist() for x in kinput])
print(' Temperature: ', T, ' K')
print(' Number of timesteps chosen for correlation function: ', tau)
print(' Extent of timestep [ps]: ', DT*2.418884254*1e-05)
print()
print('Now calculating velocities...')

Nqpoints, qpoints_scaled, ks, freqs, eigvecs, distances, Hk = read.read_phonopy(file_eigenvectors, tot_atoms_uc)
Ruc, R0 = read.read_SPOSCAR(file_initial_conf, N1N2N3, N, n_atom_conventional_cell, n_atom_unit_cell)                       #rhombo or avg R0

Rt = np.loadtxt(file_trajectory)[:,1:]
Num_timesteps = int(len(Rt[:,0]))
print(' Number of timesteps of simulation: ', Num_timesteps, '\n')
tall = np.arange(Num_timesteps)*DT*2.418884254*1e-05 #conversion to picoseconds
dt_ps = tall[1]-tall[0]
Vt = np.diff(Rt,axis=0)/dt_ps*np.sqrt(masses)/np.sqrt(3*(N))



meta = util.max_freq(dt_ps, tau) #you want the max frequency plotted be 25 Thz
ZS = np.zeros((meta,Nqpoints+1))
Zqs = np.zeros((meta,tot_atoms_uc*3+1))



#this is for the total C(t)
t_tot, C_tot, freq_tot, G_tot = util.corr(tall,Vt,Vt,tau, ' ')
Z_tot = np.sqrt(np.conjugate(G_tot)*G_tot).real*cev/(kbev*T)
ZS[:,0] = Z_tot[0:meta]
print(' Total spectrum, average total kinetic energy per dof: ', 1/2*C_tot[0]*cH, ' Hartree')
print(' Kinetic energy per dof according to eqp thm: ', 1/2*kbH*T, ' Hartree')
print('\t\t ratio: ', np.round((1/2*C_tot[0]*cH)/(1/2*kbH*T)*100,2), ' %\n')
util.save('freq', freq_tot[0:meta])
util.save('C(t)', np.hstack((t_tot,C_tot)))


print(' Done. Performing decomposition...\n')

#namedir = plot.create_folder(system)
#anis = list(range(tot_atoms_uc*3))
#every_tot = int(tot_atoms_conventional_cell/tot_atoms_uc)
for i in range(Nqpoints):
    eigvec = eigvecs[i]
    freq_disp = freqs[i]
    k = ks[i]
    k_scal = qpoints_scaled[i]
    print('\t kpoint scaled: ', k_scal)
    print('\t kpoint ',np.round(k,3))
    
    #Creating the collective variable based on the k point
    Vcoll = np.zeros((Num_timesteps-1,tot_atoms_uc*3),dtype=complex)  
    for j,h,l in zip(range(tot_atoms_uc*3),np.repeat(range(0,N),3)*N1N2N3*3,np.tile(range(0,3),tot_atoms_uc)):
        vels = np.array(Vt[:,h+l:h+N1N2N3*3:3],dtype=complex)
        poss = R0[h:h+N1N2N3*3:3,:]
        x = np.multiply(vels,np.exp(-1j*np.dot(poss,k)))
        Vcoll[:,j] = np.sum(x,axis=1)
    Tkt = Vcoll  
    
##   this was to convert conventional into primitive
#    Tkt = np.zeros((Num_timesteps-1,tot_atoms_uc*3), dtype=complex)
#    for l,m in zip(range(0,tot_atoms_conventional_cell*3, every_tot*3),range(0,tot_atoms_uc*3,3)):
#        Tkt[:,m:m+3] = Vcoll[:,l:l+3]
    eigvecH = np.conjugate(eigvec.T)
    Qkt = np.dot(eigvecH,Tkt.T).T
    
    
    t, C, freq, G = util.corr(tall,Tkt,Tkt,tau, ' ')
    Z_q = np.sqrt(np.conjugate(G)*G).real*cev/(kbev*T)
    print('\t kinetic energy of this kpoint: ',1/2*C.real[0]*cH, ' Hartree')
    print('\t kinetic according to eqp thm: ',1/2*kbH*T, ' Hartree')
    print('\t ratio: ', np.round((1/2*C.real[0]*cH)/(1/2*kbH*T)*100,2), ' %')
    ZS[:,i+1] = Z_q[0:meta]
        
    
    t_proj, C_proj, freq_proj, G_proj = util.corr(tall,Qkt,Qkt,tau, 'projected')
    Z = np.sqrt(np.conjugate(G_proj)*G_proj).real*cev/(kbev*T)
    
    Zqs[:,0] = Z_q[0:meta]
    Zqs[:,1:] = Z[0:meta,:]
    
    Params = np.zeros((3,tot_atoms_uc*3))
    for n in range(tot_atoms_uc*3):
        x_data = freq[0:meta]
        y_data = Z[0:meta,n]

        if(n in [0,1,2] and np.allclose(k, [0,0,0])):
            popt, pcov = np.zeros(3), np.zeros((3,3))
        else:
            popt, pcov = curve_fit(util.lorentzian, x_data, y_data)
#        except RuntimeError:
#            print('Acoustic mode at Gamma (or something went wrong)')
#            continue
        perr = np.sqrt(np.diag(pcov))
        print()
        print('\t\tFitting to Lorentzian, mode '+str(n)+'...')
        print('\t\tResonant frequency omega =',np.round(popt[0],2),' +-',np.round(perr[0],3))
        print('\t\tLinewidth gamma =',np.round(popt[2],2),' +-',np.round(perr[2],3))
        print()
        Params[:,n] = popt
    
    util.save_append('Zqs', k_scal.reshape(1,3), Zqs)
    util.save_append('quasiparticles', k_scal.reshape(1,3), Params)  
#        plot.plot(freq[0:meta],Z[0:meta],'Spectrum of '+str(k))
#        anis[n] = plot.plot_with_ani(freq[0:meta],Z[0:meta,n],Z_q[0:meta], k, eigvec[:,n],freq_disp[n],n,Ruc,file_eigenvectors,masses_for_animation)
#        plot.save_proj(freq[0:meta],Z[0:meta,n],Z_q[0:meta], qpoints_scaled[i], Ruc, eigvec[:,n],freq_disp[n],n,namedir,masses_for_animation)  
    print()


util.save('ZS', ZS)

