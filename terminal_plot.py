#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys

__author__="Baifan Wang"
'''usage: python terminal_plot.py xxx.dat 1'''

def check_argv():
    if len(sys.argv) != 3 or sys.argv[1] =='--help':
        print("Usage: ./terminal_plot.py data.dat data_line")
        sys.exit() 
    else:
        pass
    if os.path.isfile(sys.argv[1]) == False:
        print("Please provide a valid data file.")
        sys.exit()
    else:
        pass

x_range, y_range = os.get_terminal_size()
x_range -=8
y_range -=6

colors = {'purple':'\033[95m','blue':'\033[94m','green':'\033[92m','yellow':'\033[93m','red':'\033[91m','end':'\033[0m'}

def data_import(data_file, data_line = 1):
    '''import the data from data_file, using the columm of data_line.
    reduce the data size to appropriate size for text based plot.
    return: the reduced x and y data, y_axis, title and label for x'''
    x, y, y_axis= [],[],[]
    with open(data_file, 'r') as file: 
        header = file.readline()
        data = file.readlines()
    for line in data[::(len(data)//x_range+1)]:
        y.append(float(line.split()[int(data_line)]))
        x.append(float(line.split()[0]))
    max_y = max(y)*1.4
    min_y = min(y)*0.6
    inter = (max_y - min_y)/(y_range - 1)
    while min_y <= max_y:
        y_axis.append(min_y)
        min_y += inter
    y_axis.sort(reverse = True)
    x_titles = header.split()
    return x, y, y_axis, x_titles

def matrix_plot(y, y_axis):
    a_matrix = ([[' ']* len(y) for i in range(len(y_axis))])
    for b in range(len(y)):
        a_matrix[len(y_axis)-1][b] = "-"
    a_matrix[len(y_axis)-1][0] = colors['blue']+'-'
    a_matrix[len(y_axis)-1][-1] = '-' +colors['end']  #make x axis blue.
    for i in range(len(y)):
        for l in range(len(y_axis)-1):
            if y[i] <= y_axis[l] and y[i] >= y_axis[l+1]:
                a_matrix[l][i] = "o"
    return a_matrix

def plot(y, y_axis, maxtrix_for_plot, x, x_title, data_line):
    plot_body = ''
    for i in range(0, len(y_axis)-1):
        for l in range(0, len(y)):
            plot_body = plot_body + maxtrix_for_plot[i][l]
        plot_body = plot_body +"\n"
        plot_body = plot_body + " " + colors['yellow']+str(round(y_axis[i],1)) + '-|'+colors['end']

    #generate x axis
    for l in range(0, len(y)):
        plot_body = plot_body + maxtrix_for_plot[len(y_axis)-1][l]

    #generate x axis ticks
    x_axis_ticks = "   " + "|".center(5)*(len(x[::5]))

    #generate x axis label
    x_axis_label = "   "
    for x in x[::5]:
       x_axis_label = x_axis_label + (str(int(x))).center(5)

    x_title = x_titles[0].center(x_range)
    title = ("Displaying the " +'"' + x_titles[int(data_line)] + '"').center(x_range)
    print('')
    print(title)
    print(colors['blue'] + plot_body + colors['end'])
    print(colors['blue'] + x_axis_ticks + colors['end'])
    print(colors['blue'] +x_axis_label + colors['end'])
    print(colors['red'] + x_title + colors['end'])

if __name__ == '__main__':
    check_argv()
    x, y, y_axis, x_titles= data_import(sys.argv[1], sys.argv[2])
    maxtrix_for_plot = matrix_plot(y, y_axis)
    plot(y, y_axis, maxtrix_for_plot, x, x_titles, sys.argv[2])
