#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 14:33:25 2019

@author: gc4217
"""

import numpy as np
import os

def repeat_masses(Masses, n_atom_conventional_cell, n_atom_primitive_cell, N1, N2, N3):
    repeated_masses = np.array([])
    repeated_masses_for_ani = np.array([])
    for i in range(len(Masses)):
        mass = Masses[i]

        n = n_atom_conventional_cell[i]
        nprim = n_atom_primitive_cell[i]
        
        m = np.repeat(mass, N1*N2*N3*3*n)
        m_ani = np.repeat(mass,nprim*3)
        
        repeated_masses = np.concatenate((repeated_masses,m))
        repeated_masses_for_ani = np.concatenate((repeated_masses_for_ani,m_ani))
        
    masses = np.array(repeated_masses).flatten()
    masses_for_animation = np.array(repeated_masses_for_ani).flatten()
    
    return masses, masses_for_animation

def corr(tall,X,Y,tau,mode):
    M = len(tall)
    dt = tall[1] - tall[0]
    tmax = M - tau
    N = np.size(X[0]) 
    X0 = X[0:tmax,:]
    X2 = 1/tmax*np.sum(X[0:tmax,:]*X[0:tmax,:])
    C = []
    for n in range(tau):
        Xjj = Y[n:n+tmax,:]
        a = np.multiply(np.conjugate(X0),Xjj)
        b = 1/(tmax) * np.sum(a,axis=0)#/X2
        if (mode=='projected'):
            c = b
        else:
            c = np.sum(b)
        C.append(c)
    C = np.array(C)
    t = np.arange(0,tau)*dt
    freq = np.fft.fftfreq(tau,d=dt)
    Z = np.fft.fft(C,axis=0)
    return t, C, freq, Z

def lorentzian(x, x0, A, gamma):
    y = 1/np.pi *  A * 1/2*gamma / ((x - x0)**2 + (1/2*gamma)**2)
    return y

def save(filename, data):
    filename2 = filename
    if os.path.isfile(filename):
        n_of_files = len([name for name in os.listdir('.') if (os.path.isfile(name) and name==filename)])
        filename2 = filename+'_'+str(n_of_files)
        print(filename, ' already present. Saving it as ', filename2)
    np.savetxt(filename2,data) 
    return

def save_append(filename, data1, data2):
    filename2 = filename
    if os.path.isfile(filename):
        n_of_files = len([name for name in os.listdir('.') if (os.path.isfile(name) and name==filename)])
        filename2 = filename+'_'+str(n_of_files)
        print(filename, ' already present. Saving it as ', filename2)
        
    file = open(filename2,'ab')
    np.savetxt(filename2,data1)
    np.savetxt(filename2,data2)
    file.close()
    return

def max_freq(dt_ps, tau):
    #you want the max frequency plotted be 25 Thz
    max_freq = 0.5*1/dt_ps
    if (max_freq < 25):
        meta = int(tau/2)
    else:
        meta = int(tau/2*25/max_freq)
    return meta
