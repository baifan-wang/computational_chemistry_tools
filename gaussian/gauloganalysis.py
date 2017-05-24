#!/usr/bin/env python3

"""
A script to extrat data from Gaussian calculated log file.

Usage:  python gauloganalysis.py -[-h] [-i gaussian log file] [-e] [-p] [-f] [-t] [-a]
"""
__author__='Baifan Wang'

def read_input(gaulog):
    pass

def read_gaulog(gaulog):
    try:
        with open(gaulog) as f:
            lines = f.readlines()
    except:
        print('Could not open gaussian log file!')
        raise
    return lines

def extract_energy(gaulog):
    energy = []
    for line in read_gaulog(gaulog):
        if line[:9] == ' SCF Done':
            energy.append(float(line.split()[4]))
            title = line.split()[2]
    return energy, title

def extract_frequeny(gaulog):
    freq = []
    for line in read_gaulog(gaulog):
        if line[:12] == ' Frequencies':
            freq.append(line.split()[2])
            freq.append(line.split()[3])
            freq.append(line.split()[4])
    return freq[0], freq[1], freq[2]

def extract_thermal(gaulog):
    thermal, final= [], []
    energy_term = ['ZPE', 'Thermal correction to E(elec)', 'Thermal correction to H', \
    'Thermal correction to G','E0(E(elec)+ZPE)', 'E(E0 +E(vib)+E(rol)+E(transl))',\
     'H(E+RT)', 'G(H-TS)']
    lines = read_gaulog(gaulog)
    for i in range(len(lines)):
        if lines[i][:22]== ' Zero-point correction':
            thermal.append(lines[i].split()[2])
            break
    for l in lines[i+1:i+8]:
        thermal.append(l.split()[-1])
    return [(i,l) for i,l in zip(energy_term, thermal)]

def plot_energy(energy, title):
    import numpy as np
    import matplotlib as mpl
    import matplotlib.pyplot as plt
    mpl.rcParams['axes.formatter.useoffset'] = False
    plt.style.use('ggplot')
    data = np.asarray(energy)
    fig = plt.figure(figsize=(6, 4))
    fig.subplots_adjust(wspace=0.5, bottom=0.2)
    plt.plot(data, color = 'maroon', linestyle = '-', marker = 'o')
    plt.title(title)
    plt.xlabel('Steps', fontsize = 14)
    plt.ylabel('Energy/Hatree', fontsize = 14)
    plt.tight_layout()
    plt.show()


if __name__=='__main__':
    import argparse
    parser = argparse.ArgumentParser(description='''Perfrom data extraction for the Gaussian log file.''')
    parser.add_argument('-i', help='the input file define the base pair')
    parser.add_argument('-e', action="store_true", help='output energy values')
    parser.add_argument('-p', action="store_true", help='plot the energy values')
    parser.add_argument('-f', action="store_true", help='output frequency values')
    parser.add_argument('-t', action="store_true", help='output thermal energy values')
    parser.add_argument('-a', action="store_true", help='perform all of the actions above')
    args = parser.parse_args()
    gaulog =args.i
    if args.e:
        energy, title = extract_energy(gaulog)
        print('The erergy values are: ',energy)
    elif args.p:
        energy, title = extract_energy(gaulog)
        plot_energy(energy, title)
    elif args.f:
        print('The first 3 frequency values are: ',extract_frequeny(gaulog)[:3])
    elif args.t:
        e = extract_thermal(gaulog)
        print('The thermal energy values are:')
        for i in e:
            print(i[0]+': '+i[1])
    elif args.a:
        energy, title = extract_energy(gaulog)
        print('The erergy values are: ', energy)
        print('The first 3 frequency values are: ', extract_frequeny(gaulog)[:3])
        e = extract_thermal(gaulog)
        print('The thermal energy values are:')
        for i in e:
            print(i[0]+': '+i[1])
        plot_energy(energy, title)
