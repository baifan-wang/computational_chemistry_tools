#!/usr/bin/env python3
def file_loader(file):
    """
    load the file and return the lines in this file.
    """
    try:
        with open(file) as f:
            lines = f.readlines()
    except:
        print('Could not open file!')
        raise
    return lines

def get_energy(file):
    lines = file_loader(file)
    EPTOT = []
    DIHE = []
    for line in lines:
        if "EPtot" in line:
            EPTOT.append(float(line.split()[8]))
        elif "DIHED" in line:
            DIHE.append(float(line.split()[8]))
    return sum(EPTOT)/len(EPTOT), sum(DIHE)/len(DIHE)

def generate_amd_input(res_num, atm_num, avg_eptot, avg_dihe, time):
    alphaP   =atm_num*0.2
    EthreshP =avg_eptot+alphaP
    EthreshD =res_num*3.5+avg_dihe
    alphaD   =0.2*3.5*res_num
    print('Input for Accelerated Molecular Dynamics simulation are:')
    print("ethreshd=%.2f, alphad=%.2f,\nethreshp=%.2f, alphap=%.2f" %(EthreshD, alphaD, EthreshP, alphaP))
    nstlim = int(int(time)/0.000002)
    s = """amd in vt
 &cntrl
  imin = 0, irest = 1, ntx = 5,
  nstlim = %s, dt = 0.002,
  ntc = 2, ntf = 2, ig = -1,
  cut = 8.0, ntb = 1, ntp = 0,
  ntpr = 1000, ntwx=1000, ntwr = 10000,
  ntt = 3, gamma_ln = 2.0, temp0 = 300.0,
  ioutfm = 1, iwrap = 1, ntxo = 2,
  iamd = 3,
  ethreshd = %.2f, alphad = %.2f,
  ethreshp = %.2f, alphap = %.2f
/
""" %(nstlim,EthreshD, alphaD, EthreshP, alphaP)
    with open('amd.in','w') as f:
        f.write(s)

if __name__ =="__main__":
    import sys
    mdout, res_num, atm_num, time = sys.argv[1:]
    res_num = float(res_num)
    atm_num = float(atm_num)
    avg_eptot, avg_dihe = get_energy(mdout)
    print("Energy potential energy is: %.3f kcal/mol" %avg_eptot)
    print("Energy dihedral energy is: %.3f kcal/mol" %avg_dihe)
    print("Number of residue is: %s, number of atoms is: %s" %(res_num, atm_num))
    generate_amd_input(res_num, atm_num, avg_eptot, avg_dihe, time)
