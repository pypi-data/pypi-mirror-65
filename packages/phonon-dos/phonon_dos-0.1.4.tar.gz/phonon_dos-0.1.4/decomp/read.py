# -*- coding: utf-8 -*-
"""
Created on Sun Mar 11 11:05:28 2018

@author: Gabriele Coiana
"""

import numpy as np
import yaml, os
#yaml.warnings({'YAMLLoadWarning': False})

def read_parameters(input_file):
    """
    This function takes the input parameters from the file input.txt 
    and applies the right types to the variables
    """
    lista = []
    f = open(input_file, 'r')
    A = f.readlines()
    for string in A:
        index = string.find('=')+2
        lista.append(string[index:-1])
        
    lattice_param = float(lista[1])
    
    m = lista[2]
    Masses = np.fromstring(m, dtype=np.float, sep=',')
    
    ns = lista[3]
    n_atom_unit_cell = np.fromstring(ns, dtype=np.int, sep=',')
    
    ncs = lista[4]
    n_atom_conventional_cell = np.fromstring(ncs, dtype=np.int, sep=',')
    
    N = lista[5]
    n = np.fromstring(N, dtype=np.int, sep=',')
    N1,N2,N3 = n[0],n[1],n[2]
    
    band = lista[6]
    a = np.fromstring(band, dtype=np.float, sep=',')
    num = len(a)/3
    ks = np.split(a,num)
    
    file_eigenvectors = str(lista[7])
    
    file_trajectory = str(lista[8])
    
    file_initial_conf = str(lista[9])
    
    system = str(lista[10])
    
    DT = float(lista[11])
    tau = int(lista[12])
    
    T = float(lista[13])
    
    brchs = lista[14]
    branches = np.fromstring(brchs, dtype=np.int, sep=',')
    
    max_Z = float(lista[15])
    
    f.close()
    return lattice_param, Masses, n_atom_unit_cell, n_atom_conventional_cell, N1,N2,N3, ks, file_eigenvectors, file_trajectory, file_initial_conf, system, DT, tau, T, branches, max_Z





def read_post_proc(input_file):
    lista = []
    f = open(input_file, 'r')
    A = f.readlines()
    for string in A:
        index = string.find('=')+2
        lista.append(string[index:-1])
        
    mode = int(lista[1])
    
    ns = lista[2]
    n_atom_unit_cell = np.fromstring(ns, dtype=np.int, sep=',')
    
    file_eigenvectors = str(lista[3])
    
    max_Z = float(lista[4])
    
    ks = lista[5]
    a = np.fromstring(ks, dtype=np.float, sep=',')
    num = len(a)/3
    kpoints = np.split(a,num)
    
    labs = lista[6]
    labels = labs.split(',')
    
    modes = np.fromstring(lista[7], dtype=np.int, sep=',')
    
    temperature_folders = lista[8]
    
    return mode, n_atom_unit_cell, file_eigenvectors, max_Z, kpoints, labels, modes, temperature_folders








def read_phonopy(file_eigenvectors, n_atom_unit_cell):
    ## =============================================================================
    # Phonopy frequencies and eigenvectors
    data = yaml.load(open(file_eigenvectors))
    #D = data['phonon'][0]['dynamical_matrix']
    #D = np.array(D)
    #D_real, D_imag = D[:,0::2], 1j*D[:,1::2]
    #D = (D_real + D_imag)*21.49068**2#*0.964*10**(4)#
    
#    data2 = data['phonon']
#    qpoints_scaled = []
#    freqs = []
#    eigvecs = []
#    for element in data2:
#        qpoints_scaled.append(element['q-position'])
#        freq = []
#        eigvec = np.zeros((n_atom_unit_cell*3, n_atom_unit_cell*3),dtype=complex)
#        for j in range(len(element['band'])):
#            branch = element['band'][j]
#            freq.append(branch['frequency'])
#            
#            eigen = np.array(branch['eigenvector'],dtype=complex)
#            eigen_real = eigen[:,:,0]
#            eigen_imag = eigen[:,:,1]
#            eigen = eigen_real + 1j*eigen_imag
#            eigen = eigen.reshape(n_atom_unit_cell*3,)
#            eigvec[:,j] = eigen
#    
#        freqs.append(freq)
#        eigvecs.append(eigvec)
#    qpoints_scaled = np.array(qpoints_scaled)
#    freqs = np.array(freqs)
    c = 1.88973 #conversion to Bohrs
    h = np.array(data['reciprocal_lattice'])*2*np.pi*1/c
    distances = []
    qpoints_scaled = []
    dist = 0.0
    frequencies = []
    eigvecs = []
    for i in range(len(data['phonon'])):
        if(i==0):
            this_element = data['phonon'][i]
            this_qpoint_sc = this_element['q-position']
            dist = 0.0
            distances.append(dist)
        else:
            this_element = data['phonon'][i]
            previous_element = data['phonon'][i-1]
            this_qpoint_sc = this_element['q-position']
            previous_qpoint_sc =  previous_element['q-position']
            
            this_qpoint = np.dot(h,this_qpoint_sc)
            previous_qpoint = np.dot(h,previous_qpoint_sc)
            
            diff = this_qpoint - previous_qpoint
            
            dist = dist + np.linalg.norm(diff)
            distances.append(dist)
        
        prov = []
        eigvec = np.zeros((n_atom_unit_cell*3, n_atom_unit_cell*3),dtype=complex)
        for j in range(len(this_element['band'])):
            branch = this_element['band'][j]
            prov.append(branch['frequency'])
            eigen = np.array(branch['eigenvector'],dtype=complex)
            eigen_real = eigen[:,:,0]
            eigen_imag = eigen[:,:,1]
            eigen = eigen_real + 1j*eigen_imag
            eigen = eigen.reshape(n_atom_unit_cell*3,)
            eigvec[:,j] = eigen
            
        eigvecs.append(eigvec)
        frequencies.append(prov)
        qpoints_scaled.append(this_qpoint_sc)

    frequencies = np.array(frequencies)
    distances = np.array(distances)
    qpoints_scaled = np.array(qpoints_scaled)
    Nqpoints = len(qpoints_scaled[:,0])

    
    c = 1.88973 #conversion to Bohrs
    Hk = np.array(data['reciprocal_lattice'])*2*np.pi*1/c
    ks = np.dot(Hk,qpoints_scaled.T).T
    # =============================================================================
    return Nqpoints, qpoints_scaled, ks, frequencies, eigvecs, distances, Hk


def read_SPOSCAR(file,N1N2N3,N,n_atom_conventional_cell,n_atom_primitive_cell):
    conv = np.genfromtxt(file, skip_header=1, max_rows=1)
    h = np.genfromtxt(file,skip_header=2, max_rows=3)
    S = np.genfromtxt(file, skip_header=8)
    
    if (conv==1.0):
        conv_factor = 1.88973
    else:
        conv_factor = 1
            
    tot_atoms_primitive = int(np.sum(n_atom_primitive_cell))
    R0 = np.dot(h,S.T).T*conv_factor
    
    Ruc = np.zeros((tot_atoms_primitive,3))
    for i in range(len(n_atom_conventional_cell)):
        n = n_atom_conventional_cell[i]
        for j in range(n):
            Ruc[i] = R0[i*j*N1N2N3]
    R0 = np.repeat(R0,3,axis=0)
    return Ruc, R0

def read_path(kinput_scaled, Nqpoints, labels, Hk):
    Nq_input = len(kinput_scaled)
    ks = []
    x_labels = []
    distances = []
    previous_k = np.dot(Hk, kinput_scaled[0])
    distance = 0.0
    for i in range(Nq_input-1):
        this_k_input = kinput_scaled[i]
        next_k_input = kinput_scaled[i+1]
        ks.append(this_k_input)
        x_labels.append(labels[i])
        direction_input = (next_k_input - this_k_input)/np.linalg.norm(next_k_input - this_k_input)
        accepted_kinputs = []
        for j in range(Nqpoints):
            to_skip = (4)*j
            this_k = np.genfromtxt('quasiparticles',skip_header=to_skip+0, max_rows=1)
            direction = (this_k - this_k_input)/np.linalg.norm(this_k - this_k_input)
            if(np.allclose(direction, direction_input) and not np.allclose(this_k, next_k_input)):
                ks.append(this_k)
                distance = distance + np.linalg.norm(np.dot(Hk,this_k) - previous_k)
                distances.append(distance)
                previous_k = np.dot(Hk,this_k)
                x_labels.append(' ')
            elif(np.allclose(this_k, this_k_input) and not this_k.tolist() in accepted_kinputs):
                accepted_kinputs.append(this_k_input.tolist())
                this_q = np.dot(Hk, this_k_input)
                distance = distance + np.linalg.norm(this_q - previous_k)
                distances.append(distance)  
                previous_k = this_q

    ks.append(kinput_scaled[-1])
    x_labels.append(labels[-1])
    distance = distance + np.linalg.norm(np.dot(Hk,kinput_scaled[-1])-previous_k)
    distances.append(distance)
    distances = np.array(distances)
    return ks, x_labels, distances






