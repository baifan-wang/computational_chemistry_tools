#!/bin/env python3
_description__ = \
'''usage: python rem_rate_calculator.py rem.log'''
__author__='Baifan Wang'
import sys
def rem_log_reader(rem):
    try:
        with open(rem, 'r') as f:
            for line in f:
                if line[0] != '#':
                    yield line
    except IOError as e:
        print('Unable to open file, please check')
        sys.exit()

def calculate_average(remlog):
    average_rate = []
    rate_temp = []
    count = 0
    for line in remlog:
        success_rate = float(line.split()[6])
        rate_temp.append(success_rate)
        if count == 23:
            average = sum(rate_temp)/24
#            print(average)
            average_rate.append(average)
            rate_temp = []
            count = 0
        count += 1
    final_average = sum(average_rate)/len(average_rate)
    return final_average
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Please provide a validate rem.log file.')
        sys.exit()
    remlog = rem_log_reader(sys.argv[1])
    print('The average avlue of Success rate is %.3f' %calculate_average(remlog))
