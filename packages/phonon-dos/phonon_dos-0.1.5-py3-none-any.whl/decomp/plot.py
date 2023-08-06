#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 13:56:19 2019

@author: gabriele
"""
import numpy as np
def figsize(scale):

    fig_width_pt = 469.755                          # Get this from LaTeX using \the\textwidth

    inches_per_pt = 1.0/72.27                       # Convert pt to inch

    golden_mean = (np.sqrt(5.0)-1)/2.0              # Aesthetic ratio (you could change this)

    fig_width = fig_width_pt*inches_per_pt*scale    # width in inches

    fig_height = fig_width*golden_mean              # height in inches

    fig_size = [fig_width,fig_height]               # reverse widht and height for horizontal plots

    return fig_size

import matplotlib as mpl
mpl.use('pgf')
#import warnings
#warnings.filterwarnings('ignore') 
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import animation
from scipy import interpolate
import os








def lorentzian(x, x0, A, gamma):
    y = 1/np.pi *  A * 1/2*gamma / ((x - x0)**2 + (1/2*gamma)**2)
    return y

def from_band(ks):
    Points = {'$\Gamma$':[0,0,0],'X':[0.5,0,0],'M':[0.5,0.5,0],'R':[0.5,0.5,0.5],'boh':[0,0.5,0], 'Z':[0,0,0.5]}
    x_labels = []
    for kpoint in ks:
        a = 0
        for element in Points.items():
            a = a + 1
            if (np.array_equal(kpoint , element[1])):
                x_labels.append(element[0])
                break
            if (a==len(Points.items())):
                x_labels.append(' ')
    return x_labels


def animate(frames,plot):
    plot.collections = []
    
#    Baiimag, Tiiimag, Oiimag = frame_BaTiO3[0:8*3], frame_BaTiO3[8*3:9*3], frame_BaTiO3[9*3::]
    plot._offsets3d = (frames[0::3], frames[1::3], frames[2::3])

#    plotBaimag._offsets3d = (Baiimag[0::3],Baiimag[1::3],Baiimag[2::3])
#    plotTiimag._offsets3d = (Tiiimag[0::3],Tiiimag[1::3],Tiiimag[2::3])
#    plotOimag._offsets3d = (Oiimag[0::3],Oiimag[1::3],Oiimag[2::3])
    return

def plot_eigvec(Ruc, n_uc, k,eigvec,freq, ax, fig):
    t = np.arange(0,100,1)
    
    Rucxyz = np.repeat(Ruc,3,axis=0)
    EIGs = eigvec
    
    exp1 = np.exp(1j*np.sum(np.multiply(k,Rucxyz),axis=1)) #this multiplies by the phase factor exp(i k.R)
    #exp2 = np.exp(1j*freq*t).reshape(1,len(t))
    exp2 = np.sin(t).reshape(1,len(t))
    EIG_exp = np.multiply(EIGs,exp1)
    ut = np.dot(EIG_exp.reshape(len(EIGs),1),exp2)
        
    Rt = Ruc.flatten().reshape(len(EIGs),1) + np.real(ut)
    Rt2 = Ruc.flatten().reshape(len(EIGs),1) + np.imag(ut)

    plot = ax.scatter(Rt[0::3,0], Rt[1::3,0], Rt[2::3,0], s=100)
    ani = animation.FuncAnimation(fig,animate,frames=Rt.T,fargs=(plot,))
    return ani

def plot(x,y,title):
    fig,ax = plt.subplots()
    ax.plot(x,y)
    ax.set_xlabel('Frequency [Thz]')
    ax.set_title(title)
    plt.show()
    return

def plot_eigvec_noani(Ruc, n_uc, k,eigvec,freq, ax,fig):
    t = np.arange(0,100,1)
    
    Rucxyz = np.repeat(Ruc,3,axis=0)
    
    eigvec = eigvec.real
    Ruc = Ruc.flatten()
    
    ax.scatter(Ruc[0::3], Ruc[1::3], Ruc[2::3], alpha=0.5, s=100)
    ax.quiver(Ruc[0::3], Ruc[1::3], Ruc[2::3], eigvec[0::3], eigvec[1::3], eigvec[2::3], color='black')
    return 

def plot_with_ani(x,y,ytot, k,eigvec,freq,n,Ruc,eigname,masses):
    fig,ax = plt.subplots()
    graph2, = ax.plot(x,ytot,'--',label='total DOS', color='orangered')
    graph1, = ax.plot(x,y,label='mode-projected DOS', color='blue')
    ax.set_xlim(left=-1,right=30)
    ax.set_xlabel('Frequency [Thz]')
    ax.set_title('Spectrum of mode n. '+str(n)+' kpoint '+str(k))
    
    ax1 = ax.twiny()
    ax1.set_xlabel('Frequency [cm$^{-1}$]')
    ax1.plot(x*33.35641,-np.ones(len(x)),c='white',linewidth=0,label='')
    ax1.set_xlim(-1*33.35641,30*33.35641)

    
    
    graph3, = ax.plot(np.repeat(freq,100),np.linspace(0,ytot.max(),100),':' ,c='r', label='freq from dispersion')
    plt.legend(handles=[graph1, graph2, graph3], loc=2)
    
    
    ax2 = fig.add_axes([0.5, .5, .3, .3],projection='3d')
    ax2.set_title(str(eigname)+'\nfrequency: '+str(freq))
    ampl = 10
    eigvec = eigvec/np.sqrt(masses)*ampl
    ani = plot_eigvec(Ruc, 1, [0,0,0],eigvec,freq,ax2,fig)
    
    
    print('Mode frequency: ', freq, '\n')
    print('Eigenvector components:')
    print(np.round(np.reshape(np.real(eigvec),np.shape(Ruc)),2))
    print()
    print('Imaginary part:')
    print(np.round(np.reshape(np.imag(eigvec),np.shape(Ruc)),2))
    print()
    
    plt.show()
    return ani

def save_proj(x,y,ytot, k,Ruc, eigvec,freq,n,namedir,masses, params, max_Z):
    pgf_with_latex = {                      # setup matplotlib to use latex for output

    "pgf.texsystem": "pdflatex",        # change this if using xetex or lautex

    "text.usetex": True,                # use LaTeX to write all text

    "font.family": "serif",

    "font.serif": [],                   # blank entries should cause plots to inherit fonts from the document

    "font.sans-serif": [],

    "font.monospace": [],

    "axes.labelsize": 16,                # LaTeX default is 10pt font.     "text.fontsize": 10,

    "legend.fontsize": 12,               # Make the legend/label fonts a little smaller

    "xtick.labelsize": 16,

    "ytick.labelsize": 16,

    "figure.figsize": figsize(1.4),       # default fig size of 0.9 textwidth

    "pgf.preamble": [

        r"\usepackage[utf8x]{inputenc}",    # use utf8 fonts becasue your computer can handle it :)

        r"\usepackage[T1]{fontenc}",        # plots will be generated using this preamble

        ]

    }
    
    name_current_dir = namedir+'/'+str(k)
    try:
        os.mkdir(name_current_dir)
    except FileExistsError:
        a = 1

    mpl.rcParams.update(pgf_with_latex)
    plt.ioff()
    fig,ax = plt.subplots()
    #graph2, = ax.plot(x,ytot,'--',label='k-point DOS', color='grey')
    graph1, = ax.plot(x,y,label='mode-projected DOS', color='blue', alpha=0.7)
    ax.set_xlabel('Frequency [Thz]')
    ax.set_ylabel('DOS [kB T * ps]')
#    fig.suptitle('Spectrum of mode n. '+str(n)+' kpoint '+str(k))
    
    ax1 = ax.twiny()
    ax1.set_xlabel('Frequency [cm$^{-1}$]')
    ax1.plot(x*33.35641,-0.0001*np.ones(len(x)),c='white',linewidth=0,label='')
    ax1.set_xlim(-1*33.35641,25*33.35641)
    ax.set_xlim(left=-1,right=25)

    
    if(max_Z > np.max(ytot.max()) or max_Z < 0.0):
        a=1
    else:
        ax.set_ylim(bottom=-max_Z/10,top=max_Z)
    
    
#    print('Mode frequency: ', freq, '\n')
#    print('Eigenvector components:')
#    print(np.round(np.reshape(np.real(eigvec),(5,3)),2))
#    print()
#    print('Imaginary part:')
#    print(np.round(np.reshape(np.imag(eigvec),(5,3)),2))
#    print()
#    print()

    
    xx = np.arange(x.min(), x.max(), 0.01)
    graph4, = ax.plot(xx,lorentzian(xx,*params), linewidth=3, color='orange', label='Lorentzian')
    omega0 = params[0]
    gamma = params[2]
    y_max = np.max(lorentzian(x,*params))
    if not(np.isnan(y_max)): #exclude acoustic at Gamma
        ax.text(omega0+gamma, y_max/2, 'width='+str(np.round(gamma,2)))
        ax.axvline(x=omega0, linestyle=':', color='black')
        #vline1 = ax.plot(np.repeat(omega0,100),np.linspace(0,y_max/2,100),':' ,c='grey')
#        vline1 = ax.plot(np.repeat(omega0+gamma/2,100),np.linspace(0,y_max/2,100) ,c='orangered')
        ax.axvspan(omega0-gamma/2, omega0+gamma/2, ymin=0, ymax=1, color='grey', alpha=0.2)
    

    
      
    graph3, = ax.plot(np.repeat(freq,100),np.linspace(0,y.max(),100), c='red', label='freq from dispersion')
    plt.legend(handles=[graph1, graph3, graph4])
    
#    plt.subplots_adjust(top=0.85)
#    if(np.allclose(k,[0,0,0])):
#        ax2 = fig.add_axes([0.7, 0.4, .2, .2],projection='3d')
#        ax2.set_xticks([])
#        ax2.set_yticks([])
#        ax2.set_zticks([])
#        ax2.set_title('frequency: '+str(freq))
#        ampl = 10
#        eigvec = eigvec/np.sqrt(masses)*ampl
#        ggraph = plot_eigvec_noani(Ruc, 1 ,[0,0,0],eigvec,freq, ax2, fig)

    plt.tight_layout()
    fig.savefig(name_current_dir+'/proj_'+str(k)+'mode'+str(n)+'.pdf')
    plt.close(fig)
#    plt.show()
    return 
    
def plot_k(f, data, data_projected, ks,freqs, max_Z, branches,  title=''):
    """
    Plotting the dispersion from MD and from phonon theory.
    
    Variables:
        f = array of the frequencies [Thz] 
        data = matrix with spectra from all k points: shape = (timesteps,N)
        indexes = list of all kpoints
        freqs = frequencies from phonopy
    """
    fig,ax = plt.subplots()
    plt.suptitle('Spectrum via MD and phonon theory')
    #ax.set_title(title)
    ax.set_ylabel('[Thz]')
    N = len(data[0,:])
    offset = np.zeros(N) + f[0]
    df = f[1]-f[0]
    tot_branches = int(len(freqs[0][0,:]))
    
    kk = np.linspace(0,1,N)
    dk = kk[1] - kk[0]
    


    indexes = from_band(ks)

    #norm = [plt.cm.colors.Normalize(vmax=abs(data[0::1,l]).max(), vmin=-abs(data[0::1,l]).min()) for l in range(len(data[0,:]))]
    if(max_Z > np.max(data) or max_Z < 0.0):
        max_Z = np.max(data)
    
    norm = plt.cm.colors.Normalize(vmax=max_Z, vmin=0)
    cmps = [plt.cm.Purples, plt.cm.Reds, plt.cm.Greens]
    
    if(branches[1]- branches[0] > 3): #plot whole spectrum
        print('Drawing the whole spectrum...')
        for j in range(len(data[0::1,0])):  
            # this is the whole spectrum
            ax.bar(kk, np.repeat(df,N), bottom=offset-df/2,  color=plt.cm.Blues(norm(data[j,:])), tick_label=indexes, align='center', width=dk, alpha=None)
            offset = offset + df
            
    else:   #print only those branches 
        print('Drawing spectrum branches from ', branches[0], 'to ', branches[1])
        for j in range(len(data[0::1,0])):      
            if(np.size(data_projected) != 0):
                for mm in range(len(data_projected[0,:,0])):
                    if(np.max(data_projected[j,mm,:]) == np.max(data_projected[:,mm,:])): #this is just for the legend
                        ax.bar(kk, np.repeat(df,N), bottom=offset-df/2,  color=cmps[mm](norm(data_projected[j,mm,:])), tick_label=indexes, align='center', width=dk, alpha=.5)
                        kpoint_of_max = np.argwhere(data_projected[j,mm,:] == np.max(data_projected[j,mm,:]))[0,0]
                        bar = ax.bar(kk[kpoint_of_max], df, bottom=offset[0]-df/2,  color=cmps[mm](norm(data_projected[j,mm,kpoint_of_max])),  align='center', width=dk, alpha=.5, label='mode '+str(branches[0]+mm))
                    else:
                        ax.bar(kk, np.repeat(df,N), bottom=offset-df/2,  color=cmps[mm](norm(data_projected[j,mm,:])), tick_label=indexes, align='center', width=dk, alpha=.5)
    
            offset = offset + df
   
    
    ax2 = plt.twinx()
    ax2.set_ylabel('[Thz]')
    num_dispersions = len(freqs)
    colours = ['blue', 'red']
    for l in range(num_dispersions):
        for j in range(tot_branches):
            ax2.scatter(kk,freqs[l][:,j], marker='x', c=colours[l], s=100)
            
        ax2.scatter(kk,freqs[l][:,tot_branches-1],  marker='x', s=100, c=colours[l], label=title[l])
    ax2.get_shared_y_axes().join(ax, ax2)
    
    
    handles, labels = ax.get_legend_handles_labels()

    plt.ylim([f[0], f[-1]])
    plt.legend(handles=handles, labels=labels)
    plt.show()
    fig.savefig('spectrum_branches_'+str(branches[0])+'_to_'+str(branches[1])+'.pdf')
    fig.savefig('spectrum_branches_'+str(branches[0])+'_to_'+str(branches[1])+'.png')
    return
    



def plot1(freq,ZQS, labels):
    pgf_with_latex = {                      # setup matplotlib to use latex for output

    "pgf.texsystem": "pdflatex",        # change this if using xetex or lautex

    "text.usetex": True,                # use LaTeX to write all text

    "font.family": "serif",

    "font.serif": [],                   # blank entries should cause plots to inherit fonts from the document

    "font.sans-serif": [],

    "font.monospace": [],

    "axes.labelsize": 16,                # LaTeX default is 10pt font.     "text.fontsize": 10,

    "legend.fontsize": 12,               # Make the legend/label fonts a little smaller

    "xtick.labelsize": 16,

    "ytick.labelsize": 16,

    "figure.figsize": figsize(1.4)[::-1],       # default fig size of 0.9 textwidth

    "pgf.preamble": [

        r"\usepackage[utf8x]{inputenc}",    # use utf8 fonts becasue your computer can handle it :)

        r"\usepackage[T1]{fontenc}",        # plots will be generated using this preamble

        ]

    }

    mpl.rcParams.update(pgf_with_latex)
    n = len(ZQS[0])-1

    fig, axs = plt.subplots(n, sharex=True, sharey=True, gridspec_kw={'hspace': 0})
    for i in range(n):
        axs[i].plot(freq,ZQS[:,0], ':', color='grey')
        axs[i].text(.75,.75,labels[i],fontsize=12,horizontalalignment='center', verticalalignment='center',transform=axs[i].transAxes)
        axs[i].plot(freq, ZQS[:,i+1])
    
    axs[0].tick_params(axis='x', which='major', labelsize=15, width=2 , length=6, direction='in', top = True, bottom=False)
    axs[-1].tick_params(axis='x', which='major', labelsize=15, width=2 , length=6, direction='in', bottom = True)
    plt.rcParams['axes.linewidth'] = 2
    plt.yticks([])
    plt.yticks([])
#    fig.add_subplot(111, frameon=False)
#    plt.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
#    plt.ylabel('K-point DOS [kB T * ps]')
    plt.xlabel('Frequency [Thz]')
    plt.tight_layout()
#    plt.show() 
    fig.savefig('plot1.pdf')
    return

def plot2(freq,ZQS,modes, labels, freqs_from_disp):
    pgf_with_latex = {                      # setup matplotlib to use latex for output

    "pgf.texsystem": "pdflatex",        # change this if using xetex or lautex

    "text.usetex": True,                # use LaTeX to write all text

    "font.family": "serif",

    "font.serif": [],                   # blank entries should cause plots to inherit fonts from the document

    "font.sans-serif": [],

    "font.monospace": [],

    "axes.labelsize": 16,                # LaTeX default is 10pt font.     "text.fontsize": 10,

    "legend.fontsize": 12,               # Make the legend/label fonts a little smaller

    "xtick.labelsize": 16,

    "ytick.labelsize": 16,

    "figure.figsize": figsize(1.4)[::-1],       # default fig size of 0.9 textwidth

    "pgf.preamble": [

        r"\usepackage[utf8x]{inputenc}",    # use utf8 fonts becasue your computer can handle it :)

        r"\usepackage[T1]{fontenc}",        # plots will be generated using this preamble

        ]

    }

    mpl.rcParams.update(pgf_with_latex)
    n_modes = len(modes)
    n_kpoints = len(ZQS[0,0,:])-1
    for n in range(n_kpoints): #iterating over the k points
        fig, axs = plt.subplots(n_modes, sharex=True, sharey=True, gridspec_kw={'hspace': 0})
        
        for i in range(n_modes): #iterating over the modes
            mode = modes[i]
            axs[i].plot(np.repeat(freqs_from_disp[mode,n],100),np.linspace(0,ZQS[:,0,n].max(),100),c='r', label='freq from dispersion')
            axs[i].plot(freq,ZQS[:,0,n], ':', color='grey')
            axs[i].text(.75,.75,labels[n]+str('\n mode')+str(mode),fontsize=12,horizontalalignment='center', verticalalignment='center',transform=axs[i].transAxes)
            axs[i].plot(freq, ZQS[:,mode+1,n])

        axs[0].tick_params(axis='x', which='major', labelsize=15, width=2 , length=6, direction='in', top = True, bottom=False)
        axs[-1].tick_params(axis='x', which='major', labelsize=15, width=2 , length=6, direction='in', bottom = True)
        plt.rcParams['axes.linewidth'] = 2
        plt.yticks([])
#        fig.add_subplot(111, frameon=False)
#        plt.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
#        plt.ylabel('K-point DOS [kB T * ps]')
        plt.xlabel('Frequency [Thz]')
#        plt.tight_layout()
        
#    plt.show() 
    fig.savefig('plot2.pdf')
    return


def plot3(Ts, frequencies, modes, labels):
    pgf_with_latex = {                      # setup matplotlib to use latex for output

    "pgf.texsystem": "pdflatex",        # change this if using xetex or lautex

    "text.usetex": True,                # use LaTeX to write all text

    "font.family": "serif",

    "font.serif": [],                   # blank entries should cause plots to inherit fonts from the document

    "font.sans-serif": [],

    "font.monospace": [],

    "axes.labelsize": 16,                # LaTeX default is 10pt font.     "text.fontsize": 10,

    "legend.fontsize": 12,               # Make the legend/label fonts a little smaller

    "xtick.labelsize": 16,

    "ytick.labelsize": 16,

    "figure.figsize": figsize(1.4),       # default fig size of 0.9 textwidth

    "pgf.preamble": [

        r"\usepackage[utf8x]{inputenc}",    # use utf8 fonts becasue your computer can handle it :)

        r"\usepackage[T1]{fontenc}",        # plots will be generated using this preamble

        ]

    }

    mpl.rcParams.update(pgf_with_latex)
    n_kpoints = len(frequencies[0,0,:,0])
    markers = ['s','o','v','X','+','.','^','<','>','*','s','o','v','X','+','.','^','<','>','*']
    for i in range(n_kpoints):
        fig, ax = plt.subplots()
        for mode in modes:
            freq = frequencies[0,mode,i,:] - frequencies[0,mode,i,0]
            gamma = frequencies[1,mode,i,:]
            ax.errorbar(Ts, freq, gamma/2, marker=markers[mode], fmt='o', label='mode '+str(mode))
        ax.text(.1,.1,labels[i],fontsize=12,horizontalalignment='center', verticalalignment='center',transform=ax.transAxes)

        ax.set_xlabel('Temperature [K]')
        ax.set_ylabel('$\omega(T) - \omega(T='+str(Ts[0])+')$ [Thz]')
        ax.tick_params(axis='x', which='both', labelsize=15, width=2 , length=6, direction='in', top = True, bottom=True, left=True, right=True)
        ax.legend()  
        fig.savefig('plot3_'+str(labels[i])+'.pdf')
    plt.rcParams['axes.linewidth'] = 2
#    plt.show()
    return


def plot4(kk, frequencies, frequencies_disp, qpoints, x_labels):
    pgf_with_latex = {                      # setup matplotlib to use latex for output

    "pgf.texsystem": "pdflatex",        # change this if using xetex or lautex

    "text.usetex": True,                # use LaTeX to write all text

    "font.family": "serif",

    "font.serif": [],                   # blank entries should cause plots to inherit fonts from the document

    "font.sans-serif": [],

    "font.monospace": [],

    "axes.labelsize": 16,                # LaTeX default is 10pt font.     "text.fontsize": 10,

    "legend.fontsize": 12,               # Make the legend/label fonts a little smaller

    "xtick.labelsize": 16,

    "ytick.labelsize": 16,

    "figure.figsize": figsize(1.4),       # default fig size of 0.9 textwidth

    "pgf.preamble": [

        r"\usepackage[utf8x]{inputenc}",    # use utf8 fonts becasue your computer can handle it :)

        r"\usepackage[T1]{fontenc}",        # plots will be generated using this preamble

        ]

    }

    mpl.rcParams.update(pgf_with_latex)
    fig, ax = plt.subplots()
    n_branches = len(frequencies[0,:,0])
    
    
    
    gamma_pos = []
    for c in range(len(qpoints)):
        qpoint = qpoints[c]
        if(np.allclose(qpoint,[0,0,0])):
            gamma_pos.append(c)
    if(gamma_pos[0] != 0):
        gamma_pos.insert(0,0)
    if(gamma_pos[-1] != len(kk)):
        gamma_pos.insert(len(kk),len(kk))
    for j in range(3):
        ax.scatter(kk,frequencies_disp[0,j,:], marker='x', color='black', label='0K dispersion')
        ax.scatter(kk,frequencies[0,j,:], marker='x', color='red')
        for d in range(len(gamma_pos)-1):
            this_gamma = gamma_pos[d]
            next_gamma = gamma_pos[d+1]+1
            kk_div = kk[this_gamma:next_gamma]
            f = interpolate.interp1d(kk_div, frequencies[0,j,this_gamma:next_gamma], kind=1)
            x = np.arange(kk_div.min(), kk_div.max(), 0.01)
#            ax.plot(x, f(x), color='red')
            f_gamma = interpolate.interp1d(kk_div, frequencies[1,j,this_gamma:next_gamma], kind=1)
            y1, y2 = f(x)+f_gamma(x)/2, f(x)-f_gamma(x)/2
            ax.fill_between(x, y1, y2, color='red', alpha=0.3)

    for j in range(3,n_branches):
        f = interpolate.interp1d(kk, frequencies[0,j,:], kind=1)
        x = np.arange(kk.min(), kk_div.max(), 0.01)
#        ax.plot(x, f(x), color='red')
        f_gamma = interpolate.interp1d(kk, frequencies[1,j,:], kind=1)
        y1, y2 = f(x)+f_gamma(x)/2, f(x)-f_gamma(x)/2
        ax.fill_between(x, y1, y2, color='red', alpha=0.3)
        graph_disp = ax.scatter(kk,frequencies_disp[0,j,:], marker='x', color='black', label='0K dispersion')
        graph_ft = ax.scatter(kk,frequencies[0,j,:], marker='x', color='red', label='finite T dispersion')
    ax.set_ylabel('Frequency [Thz]')
    ax.tick_params(axis='both', which='major', labelsize=15, width=2 , length=6, direction='in', top=True, right=True)
    ax.axhline(0, linestyle='--', color='b')
    plt.rcParams['axes.linewidth'] = 2
    plt.xticks(kk, x_labels)
    plt.legend(handles=[graph_disp, graph_ft])
#    plt.show()
    fig.savefig('plot4.pdf')
    return



































def corr_j(tcorr,X,dt,masses):
    Nsteps = len(tcorr)
    N = np.size(X[0])
    sigma2 = np.var(X,axis=0)
    C = []
    for i in range(Nsteps):
        X_i = X[i::,:]
        Xjj = np.concatenate((X[i::,:],X[0:i,:]))#[i::,:]
        a = np.multiply(np.conjugate(X),Xjj)
        b = 1/(Nsteps) * np.sum(a,axis=0)#/sigma2
        c = np.multiply(b,masses)
        d = 1/N*np.sum(c)
        C.append(d)
    C = np.array(C)
    freq = np.fft.fftfreq(Nsteps,d=dt)
    Z = np.fft.fft(C,axis=0)
    return C, freq, Z

def corr_jaa(tall,X,dt,masses):
    M = len(tall)
    tau = 1000
    tmax = M - tau
    t = np.arange(0,tau)*dt
    N = np.size(X[0])   
    X0 = X[0:tau,:]
    C = []
    for n in range(tau):
        A = []
        for m in range(tmax):
            xj = X[m,:]
            xjj = X[m+n,:]
            a = np.multiply(xj,xjj)
            A.append(a*masses)
        A = np.array(A)
        Cn = np.average(A,axis=0)
        C.append(np.average(Cn))
    C = np.array(C)
    freq = np.fft.fftfreq(tau,d=dt)
    Z = np.fft.fft(C,axis=0)
    return t, C, freq, Z
    
    

def create_folder(system,prefix=''):
    flag = ''
    try:
        namedir = prefix+'phonDOS'+system
        os.mkdir(namedir)
        flag = 'created'
    except FileExistsError:
        if(flag=='created'):
            bbb = 1
        else:
            number_of_folders = len(np.sort([x[1] for x in os.walk(prefix+'.')][0]))
            print('Folder '+namedir+' already exists. Creating phonDOS_'+str(system)+'_'+str(number_of_folders))
            namedir = namedir+'_'+str(number_of_folders)
            os.mkdir(namedir)
    return namedir
    
    
#this is if you have the velocities instead of positions    
#Vt = np.loadtxt(file_trajectory)[:,1:]*np.sqrt(masses)/np.sqrt(3*N)#/(2.418884254*1e-05)
#Num_timesteps = int(len(Vt[:,0]))
#print(' Number of timesteps of simulation: ', Num_timesteps, '\n')
#tall = np.arange(Num_timesteps)*DT*2.418884254*1e-05 #conversion to picoseconds
#dt_ps = tall[1]-tall[0] 

#eigvec_exp = np.array([0,0,0,0,0,0.5,0,0,-0.9,0,0,-0.6,0,0,0.6])
#a = np.array([0,0,1,0,0,-1,0,0,-1,0,0,-1,0,0,-1])  

#    print('\t\t sum of projected: ',1/2*np.sum(C_proj[0].real)*cH, ' Hartree')
