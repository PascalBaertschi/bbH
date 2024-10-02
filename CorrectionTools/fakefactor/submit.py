#! /usr/bin/env python

import os, re, glob
from fnmatch import fnmatch
import itertools
from argparse import ArgumentParser


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument('-f', '--force',   dest='force', action='store_true', default=False,
                                         help="submit jobs without asking confirmation" )
  parser.add_argument('-y', '--year',    dest='years', choices=[2016,2017,2018], type=int, nargs='+', default=[2018], action='store',
                                         help="select year" )
  parser.add_argument('-p', '--preVFP',  dest='preVFP', action='store_const', const="_preVFP",default="")
  args = parser.parse_args()
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

def ensureDirectory(dirname):
  """Make directory if it does not exist."""
  if not os.path.exists(dirname):
    #os.makedirs(dirname)
    os.system("mkdir -p %s"%dirname)
    print('>>> made directory "%s"'%(dirname))
    if not os.path.exists(dirname):
      print('>>> failed to make directory "%s"'%(dirname))
  return dirname

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
    
    

def createJobs(jobsfile, infiles, outdir, name, nchunks,year,origin):
    """Create file with commands to execute per job."""
    cmd = 'python3 job.py -i %s -o %s -N %s -n %i -y %s -f %s'%(infiles,outdir,name,nchunks,year,origin)
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
    years       = args.years
    preVFP      = args.preVFP
    batchSystem = 'slurm_runner.sh'
    mc_files = ['DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8','DYJetsToLL_0J_TuneCP5_13TeV-amcatnloFXFX-pythia8','DYJetsToLL_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8','DYJetsToLL_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8','WJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-pythia8','WJetsToLNu_0J_TuneCP5_13TeV-amcatnloFXFX-pythia8','WJetsToLNu_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8','WJetsToLNu_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8','TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8','TTToHadronic_TuneCP5_13TeV-powheg-pythia8','TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8','ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8','ST_t-channel_top_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8','ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-amcatnlo-pythia8','ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8','ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8']
    #mc_files = ['DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8','DYJetsToLL_0J_TuneCP5_13TeV-amcatnloFXFX-pythia8','DYJetsToLL_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8']
    for year in years:
      if year == 2016:
        preVFP = "_comb"
        files = ['SingleMuon_Run2016BCDEFGH','SingleElectron_Run2016BCDEFGH'] + mc_files
      elif year == 2017:
        files = ['SingleMuon_Run2017BCDEF','SingleElectron_Run2017BCDEF'] + mc_files
      elif year == 2018:
        #files = ['SingleMuon_Run2018ABCD','EGamma_Run2018ABCD'] + mc_files
        files = ['SingleMuon_Run2018A-UL2018_MiniAODv2_NanoAODv9-v2','SingleMuon_Run2018B-UL2018_MiniAODv2_NanoAODv9-v2','SingleMuon_Run2018C-UL2018_MiniAODv2_NanoAODv9-v2','SingleMuon_Run2018D-UL2018_MiniAODv2_NanoAODv9-v1','EGamma_Run2018ABCD'] + mc_files

      #ouput and input path
      outdir = '/pnfs/psi.ch/cms/trivcat/store/user/pbaertsc/bbh/ffvarcorr/samples_UL%s%s/'%(year,preVFP)  
      path = "/pnfs/psi.ch/cms/trivcat/store/user/pbaertsc/bbh/samples_UL%s%s"%(year,preVFP)
      # READ SAMPLES

      ensureDirectory('joblist')
      jobList      = 'joblist/joblist_UL%s.txt'%year
      jobName      = 'UL%s'%year
      print("Creating job file %s..."%(jobList))
      jobs         = open(jobList,'w')
      nChunks = 0
      #files = os.listdir(path)
      for file in files:
        name = file
        file = file+".root"
        createJobs(jobs,file,outdir,name,nChunks,year,path)
        nChunks = nChunks+1
      jobs.close()
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
