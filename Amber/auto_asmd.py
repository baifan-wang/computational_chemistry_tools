import sys, os, subprocess, time
import numpy as np

def creat_ASMD_dir(num_asmd, num_stage):
    #create the ASMD directories and write mdin in each directories:
    #asmd_2/asmd_2.3.mdin
    for i in range(1, num_asmd+1):
      asmd_dir = 'asmd_'+ str(i)
      if not os.path.exists(asmd_dir):
          os.mkdir(asmd_dir)
      for stage in range(1, num_stage+1):
          mdin = 'asmd_%s.%s.mdin' %(i, stage)
          mdin = os.path.join(asmd_dir, mdin) #nstlim = 25000
          mdin_content = '''ASMD simulation
&cntrl
 imin = 0, nstlim = 250000, dt = 0.002,
 ntx = 1, temp0 = 300.0,
 ntt = 3, gamma_ln = 5.0
 ntc = 2, ntf = 2, ntb = 1,
 ntwx =  1000, ntwr = 10000, ntpr = 1000,
 cut = 8.0, ig = -1, ioutfm = 1,
 irest = 0, jar = 1, 
/
&wt type='DUMPFREQ', istep1=1000 /
&wt type='END'   /
DISANG=dist.RST.dat.%s
DUMPAVE=asmd_%s.work.dat.%s
LISTIN=POUT
LISTOUT=POUT''' %(stage, i, stage)
          with open(mdin, 'w') as f:
              f.write(mdin_content)

def creat_RST(start_distance, dis_step, num_stage):
    # creat restraint file: dist.RST.dat.xxx
    # you need to desinate the atomic number, and initial distance.
    end_distance = start_distance + dis_step
    for stage in range(1, num_stage+1):
      dist_file = 'dist.RST.dat.'+str(stage)
      dist = ''' &rst
    iat=-1,765,
    r2=%s,
    r2a=%s,
    rk2=28.8,
    igr1 = 17,208,590,399
&end
''' %(start_distance, end_distance)
      with open(dist_file, 'w') as f:
          f.write(dist)
      start_distance += dis_step
      end_distance += dis_step

def write_job(num_asmd, coord, stage):
    '''write batch md simulation job file: job.0x.sh
    Here I use GPU accelerated pmemd. if you use other versions pmemd or sander 
    please change the pmemd.cuda, e.g., mpirun -np 16 pmemd.MPI.
    '''
    job_sh = 'job.'+str(stage)+'.sh'
    with open(job_sh,'w') as f:
        content = '''#!/bin/bash
export CUDA_VISIBLE_DEVICES=1
for ((i=1; i<%s; i++))
do
let "s=%s"
pmemd.cuda -O -p 1.top -c %s -i asmd_$i/asmd_$i.$s.mdin -o asmd_$i/asmd_$i.$s.out -x asmd_$i/asmd_$i.$s.mdcrd -r asmd_$i/asmd_$i.$s.rst -inf asmd_$i/mdinfo 
done''' %(num_asmd+1, stage, coord)
        f.write(content)
    return job_sh

def run_md(job_sh):
    '''run batch md simulation'''
    t1 = time.time()
    if "AMBERHOME" in os.environ:
        # See if we can find AMBERHOME environment variable
        amberhome = os.environ["AMBERHOME"]
    else:
        # No AMBERHOME defined
        raise("Cannot find Amber!")
    amber_bin_path = os.path.join(amberhome, "bin")
    pmemd = os.path.join(amber_bin_path, 'pmemd.cuda')
    if not os.path.exists(pmemd):
        raise("Cannot find pmemd.cuda!")
    cmd1 = "chmod +x %s" %job_sh
    subprocess.call(cmd1,shell=True)
    cmd2 = "./%s" %job_sh
    print("running MD jobs: %s" %job_sh)
    subprocess.call(cmd2, shell=True, stderr=subprocess.STDOUT)
    t2 =time.time()
    return t2-t1

def parse_asmd_workfiles(asmd_work_files):
    asmd_work      = []   #array holder for all the work
    final_Work     = []   #an array holder of all the final works. It used
    #                to determine which of the SMD sim is closest to the JA
    rec_coord      = np.array(np.loadtxt(asmd_work_files[0], skiprows=1, usecols=(0,)))
    #array holder of the Reaction Coordinates used in the SMD sim
    workskip      = len(rec_coord)  #returns the number of rows to skip to get only the final work
    for f in asmd_work_files:
        asmd_work.append(np.loadtxt(f, usecols=(3,), skiprows=1))
        final_Work.append(np.loadtxt(f, usecols=(3,), skiprows=workskip))
    return asmd_work, final_Work, rec_coord, workskip

def calc_jar(asmd_work, TEMP):
    #Calculate the Jarzynski Average
    Beta = 1/(TEMP*1.98722E-3)  #1/(TEMP*1.98722E-3) == 1/(T*kb)
    jar_avg = -np.log(np.exp(np.array(asmd_work)*-Beta).mean(axis=0))/Beta
    return jar_avg

def closest_to_jar(final_work, jar_avg, work_skip, asmd_files):
    diff_work_jar = np.abs(np.array(final_work) - jar_avg[work_skip-1])
    closest_work = diff_work_jar.min() #get the work with the smallest difference
    asmdfile = np.where(diff_work_jar == closest_work) #locates which work had the smallest diference
    asmd_files = np.array(asmd_files)
    for i in asmd_files[asmdfile]:
       filename = i
    return filename

def write_jar_output(jar_file, jar_avg, rec_coord):
  with open(jar_file, 'w') as f:
    for coords, jarval in zip(rec_coord, jar_avg):
      f.write("%s %s\n" % (coords, jarval))

def get_restart_by_asmdfile(asmd_file):
    path, stage = asmd_file.split('.')[0], asmd_file.split('.')[3]
    restart = path+'.'+stage+'.rst'
    restart =  os.path.join(path, restart)
    if os.path.exists(restart):
        return restart
    else:
        raise('Error: unable to locate the corresponding restart file')

def creat_PMF(num_stage, output):
      with open(output, "w") as f:
        addval=0.0
        for stage in range(1, num_stage+1):
            rec_coord, work=loadtxt("jar.stage%02d.dat" % stage, usecols=(0,1), unpack=True)
            for coord, workval in zip(rec_coord, work):
                f.write("%s %s\n" % (coord, workval))
            value=int(len(work))-1 
            addval=float(work[value])


def write_log(log, s):
    t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    s = "%s: "%t+s
    print(s)
    log.write(s+'\n')

def run(num_asmd, num_stage, start_distance, step, restart, TEMP=300):
    t1 = time.time()
    log = open('asmd.log','a')
    write_log(log, "ASMD simulations of %s stages with %s replicas start" %(num_stage,num_asmd))
    creat_ASMD_dir(num_asmd, num_stage)
    write_log(log, "Create ASMD directories and md inputs")
    creat_RST(start_distance, step, num_stage)
    write_log(log, "Create ASMD restraints")
    for stage in range(1, num_stage+1):
        job_sh = write_job(num_asmd, restart, stage)
        write_log(log, 'Create batch job file: %s' %job_sh)
        write_log(log, 'running batch job: %s' %job_sh)
        md_time = run_md(job_sh)
        write_log(log, 'Batch job file: %s finished, using %s s ' %(job_sh, md_time))

        asmd_work_files = ['asmd_'+str(i)+'.work.dat.'+str(stage) for i in range(1, num_asmd+1)]
        jar_file = 'jar.stage%02d.dat' %stage
        write_log(log, 'parsing ASMD work files and get restart file for next batch job')

        asmd_work, final_Work, rec_coord, workskip = parse_asmd_workfiles(asmd_work_files)
        jar_avg= calc_jar(asmd_work, TEMP)
        asmdfile = closest_to_jar(final_Work, jar_avg, workskip, asmd_work_files)
        write_log(log, "The file closest to the Jarzynski Average is: %s" %asmdfile)
        write_log(log, "Writing Jarzynski Average to %s" %jar_file)
        write_jar_output(jar_file, jar_avg, rec_coord)
        restart = get_restart_by_asmdfile(asmdfile)
        write_log(log, 'Restart file for next batch job is: %s' %restart)
        time.sleep(3000)
    creat_PMF(num_stage, 'jar.dat')
    write_log(log, 'Wrote PMF data to: jar.dat')
    t2 = time.time()
    t3=t2-t1
    write_log(log, 'ASMD simulations of %s stages successfully finished. using: %s' %(num_stage,t3))
    log.close()

if __name__=='__main__':
    num_asmd = 100
    num_stage = 5
    start_distance = 12
    step = -1
    restart = 'equil4.rst7'
    run(num_asmd, num_stage, start_distance, step, restart, TEMP=300)
