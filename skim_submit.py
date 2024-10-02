#! /usr/bin/env python

import os, re, glob
from fnmatch import fnmatch
import itertools
from argparse import ArgumentParser
import checkFiles
from checkFiles import matchSampleToPattern, header, ensureDirectory

if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument('-f', '--force',   dest='force', action='store_true', default=False,
                                         help="submit jobs without asking confirmation" )
  parser.add_argument('-y', '--year',    dest='years', choices=[2016,2017,2018], type=int, nargs='+', default=[2018], action='store',
                                         help="select year" )
  parser.add_argument('-c', '--channel', dest='channels', choices=['mutau','etau'], type=str, nargs='+', default=['mutau'], action='store',
                                         help="channels to submit" )
  parser.add_argument('-s', '--sample',  dest='sample', type=str, default="", action='store',
                                         help="filter these samples, glob patterns (wildcards * and ?) are allowed." )
  parser.add_argument('-x', '--veto',    dest='vetos', nargs='+', default=[ ], action='store',
                                         help="veto this sample" )
  parser.add_argument('-t', '--type',    dest='type', choices=['data','mc'], type=str, default=None, action='store',
                                         help="filter data or MC to submit" )
  parser.add_argument('-T', '--tes',     dest='tes', type=str, action='store', default="no",choices=["yes","no"],
                                         help="tau energy scale" )
  parser.add_argument('-L', '--ltf',     dest='ltf', type=float, default=1.0, action='store',
                                         help="lepton to tau fake energy scale" )
  parser.add_argument('-J', '--jtf',     dest='jtf', type=float, default=1.0, action='store',
                                         help="jet to tau fake energy scale" )
  parser.add_argument('-d', '--das',     dest='useDAS', action='store_true', default=False,
                                         help="get file list from DAS" )
  parser.add_argument('-n', '--njob',    dest='nFilesPerJob', action='store', type=int, default=-1,
                                         help="number of files per job" )
  parser.add_argument('-q', '--queue',   dest='queue', choices=['all.q','short.q','long.q'], type=str, default=None, action='store',
                                         help="select queue for submission" )
  parser.add_argument('-u', '--UL',      dest='ULtag', action='store_const', const="UL",default="UL")
  parser.add_argument('-p', '--preVFP',  dest='preVFP', action='store_const', const="_preVFP",default="")
  parser.add_argument('-j', '--JECvar', dest='JECvar', action='store', type=str, default="no",choices=["yes","no"])
  args = parser.parse_args()
  checkFiles.args = args
else:
  args = None

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'



def checkExistingFiles(outdir,channel,njob):
    filelist = glob.glob("%s/*%s.root"%(outdir,channel))
    nfiles = len(filelist)
    if nfiles>njob:
      print(bcolors.BOLD + bcolors.WARNING + "Warning! There already exist %d files, while the requested number of files per job is %d"%(nfiles,njob) + bcolors.ENDC)
      remove = input("Do you want to remove the extra files? [y/n] ")
      if remove.lower()=='y':
        for filename in sorted(filelist):
          matches = re.findall(r"_(\d+)_%s.root"%(channel),filename)
          if matches and int(matches[0])>njob:
            print("Removing %s..."%(filename))
            os.remove(filename)
      else:
        print("Not removing extra files. Please make sure to delete the %d last files before hadd'ing."%(nfiles-njob))
    

def split_seq(iterable, size):
    it = iter(iterable)
    item = list(itertools.islice(it, size))
    while item:
        yield item
        item = list(itertools.islice(it, size))
    

def getFileListLocal(year,sample,preVFP):
    """Get list of files from local directory."""
    filename = "./sampleslist/UL%s%s/%s.txt"%(year,preVFP,sample)
    filelist = [ ]
    if os.path.exists(filename):
      with open(filename,'r') as file:
        for line in file:
          if '#' not in line:
            filelist.append(line.rstrip('\n'))
    return filelist
    

def saveFileListLocal(dataset,filelist):
    """Save a list of files to a local directory."""
    filename = "filelist/filelist_%s.txt"%dataset.replace('/','__')
    with open(filename,'w+') as file:
      for line in filelist:
        file.write(line+'\n')
    return filename
    
    

def createJobs(jobsfile, infiles, outdir, name, nchunks, channel, ULtag, preVFP, year, JECvar, tes):
    cmd = 'python3 skim_job.py -i %s -o %s -N %s -n %i -c %s -y %s -j %s -T %s'%(','.join(infiles),outdir,name,nchunks,channel,year,JECvar,tes)
    if ULtag=="UL":
      cmd += " -u"  
    if preVFP=="_preVFP":
      cmd += " -p"
    #if args.verbose:
    #  print(cmd)
    jobsfile.write(cmd+'\n')
    return 1
    

def submitJobs(jobName, jobList, nchunks, outdir, batchSystem):
    """Submit job."""
    extraopts = "--array=1-%s --job-name=%s" %(nchunks,jobName)
    #extraopts = "--array=1-%s --job-name=%s" %(nchunks,jobName)
    subCmd = 'sbatch %s %s %s' %(extraopts,batchSystem,jobList)
    subCmd = subCmd.rstrip()
    print(bcolors.BOLD + bcolors.OKBLUE + "Submitting %d jobs with \n  %s"%(nchunks,subCmd) + bcolors.ENDC)
    os.system(subCmd)
    return 1
    

def main():
    
    channels    = args.channels
    years       = args.years
    tes         = args.tes
    ltf         = args.ltf
    jtf         = args.jtf
    preVFP      = args.preVFP
    ULtag       = args.ULtag
    JECvar      = args.JECvar
    batchSystem = 'slurm_runner_skim.sh'
    tag         = ""

    #if tes!=1.:
    #  tag += "_TES%.3f"%(tes)
    if ltf!=1.:
      tag += "_LTF%.3f"%(ltf)
    if jtf!=1.:
      tag += "_JTF%.3f"%(jtf)
    tag = tag.replace('.','p')
    
    for year in years:
      
      # READ SAMPLES
      samplesdir = "./sampleslist/UL%s%s"%(year,preVFP)
      
      for channel in channels:
        print(header(year,preVFP,JECvar,tes,channel,tag))
        
        # SUBMIT SAMPLES
        for directory in os.listdir(samplesdir):
            directory = directory.split(".")[0]
            if args.sample!="" and args.sample not in directory:
              continue
            # FILTER
    
            print(bcolors.BOLD + bcolors.OKGREEN + directory + bcolors.ENDC)
            
            # FILE LIST
            files = [ ]
            #name  = directory.split('/')[-3].replace('/','') + '__' + directory.split('/')[-2].replace('/','') + '__' + directory.split('/')[-1].replace('/','')
            name = directory
            files = getFileListLocal(year,directory,preVFP)
            if not files:
              print(bcolors.BOLD + bcolors.WARNING + "Warning!!! FILELIST empty" + bcolors.ENDC)
              continue
            if directory.find("Run")>0:
              print("skipping data samples")
              continue
            # JOB LIST
            ensureDirectory('joblist')
            
            if JECvar=="yes":
              jobList      = 'joblist_skim/joblistJECvar_UL%s%s_%s_%s%s.txt'%(year,preVFP,name,channel,tag)
            elif tes=="yes":
              jobList      = 'joblist_skim/joblistTES_UL%s%s_%s_%s%s.txt'%(year,preVFP,name,channel,tag)
            print("Creating job file %s..."%(jobList))
            jobName      = name
            jobName     += "_%s_%s%s%s"%(channel,ULtag,year,preVFP)+tag
            jobs         = open(jobList,'w')
            if JECvar=="yes":
              outdir       = ensureDirectory('/pnfs/psi.ch/cms/trivcat/store/user/pbaertsc/bbh/samples_skim/UL%s%s_JEC/%s'%(year,preVFP,name)) 
            elif tes=="yes":
              outdir       = ensureDirectory('/pnfs/psi.ch/cms/trivcat/store/user/pbaertsc/bbh/samples_skim/UL%s%s_TES/%s'%(year,preVFP,name)) 
            # NFILESPERJOBS
            nFilesPerJob = 1
            if nFilesPerJob<1:
              for default, patterns in nFilesPerJob_defaults:
                if matchSampleToPattern(directory,patterns):
                  nFilesPerJob = default
                  break
              else:
                nFilesPerJob = 4 # default
            filelists = list(split_seq(files,nFilesPerJob))
            
            # CREATE JOBS
            nChunks = 0
            checkExistingFiles(outdir,channel,len(filelists))
            #filelists = list(split_seq(files,1))
            for file in filelists:
            #print "FILES = ",f
                createJobs(jobs,file,outdir,name,nChunks,channel,"UL",preVFP,year,JECvar,tes)
                nChunks = nChunks+1
            jobs.close()
            
            # SUBMIT
            if args.force:
              submitJobs(jobName,jobList,nChunks,outdir,batchSystem)
            else:
              submit = input("Do you also want to submit %d jobs to the batch system? [y/n] "%(nChunks))
              if submit.lower()=='force':
                submit = 'y'
                args.force = True
              if submit.lower()=='quit':
                exit(0)
              if submit.lower()=='y':
                submitJobs(jobName,jobList,nChunks,outdir,batchSystem)
              else:
                print("Not submitting jobs")
            print()



if __name__ == "__main__":
    print()
    main()
print("Done\n")
