#! /usr/bin/env python

import os, glob, sys, shlex, re
from argparse import ArgumentParser
import submit, checkFiles
from checkFiles import matchSampleToPattern, header
from submit import args, bcolors, createJobs, getFileListLocal, submitJobs, split_seq, saveFileListLocal
import itertools
import subprocess
from ROOT import TFile

parser = ArgumentParser()
parser.add_argument('-f', '--force',   dest='force', action='store_true', default=False,
                                       help="submit jobs without asking confirmation" )
parser.add_argument('-y', '--year',    dest='years', choices=[2016,2017,2018], type=int, nargs='+', default=[2018], action='store',
                                       help="select year" )
parser.add_argument('-c', '--channel', dest='channels', choices=['mutau','etau'], type=str, nargs='+', default=['mutau'], action='store',
                                       help="channels to submit" )
parser.add_argument('-s', '--sample',  dest='samples', type=str, nargs='+', default=[ ], action='store',
                                       help="filter these samples, glob patterns (wildcards * and ?) are allowed." )
parser.add_argument('-x', '--veto',    dest='vetos', type=str, nargs='+', default=[ ], action='store',
                                       help="veto this sample" )
parser.add_argument('-t', '--type',    dest='type', choices=['data','mc'], type=str, default=None, action='store',
                                       help="filter data or MC to submit" )
parser.add_argument('-T', '--tes',     dest='tes', type=str, default="", action='store',choices=["","scale_t_1prongUp","scale_t_1prongDown","scale_t_1prong1piUp","scale_t_1prong1piDown","scale_t_3prongUp","scale_t_3prongDown"],
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
parser.add_argument('-m', '--mock',    dest='mock', action='store_true', default=False,
                                       help="mock-submit jobs for debugging purposes" )
parser.add_argument('-v', '--verbose', dest='verbose', default=False, action='store_true',
                                       help="set verbose" )
parser.add_argument('-u', '--UL',      dest='ULtag', action='store_const', const="UL",default="UL")
parser.add_argument('-p', '--preVFP',  dest='preVFP', action='store_const', const="_preVFP",default="")
parser.add_argument('--skipSVFit',     dest='doSVFit', action='store_false', default=True)
parser.add_argument('-j', '--JECvar', dest='JECvar', action='store', type=str, default="",choices=["","jesTotalUp","jesTotalDown","jerUp","jerDown","met_unclusteredUp","met_unclusteredDown","jesAbsoluteUp","jesAbsoluteDown","jesAbsolute_2018Up","jesAbsolute_2018Down","jesAbsolute_2017Up","jesAbsolute_2017Down","jesAbsolute_2016Up","jesAbsolute_2016Down","jesBBEC1Up","jesBBEC1Down","jesBBEC1_2018Up","jesBBEC1_2018Down","jesBBEC1_2017Up","jesBBEC1_2017Down","jesBBEC1_2016Up","jesBBEC1_2016Down","jesEC2Up","jesEC2Down","jesEC2_2018Up","jesEC2_2018Down","jesEC2_2017Up","jesEC2_2017Down","jesEC2_2016Up","jesEC2_2016Down","jesFlavorQCDUp","jesFlavorQCDDown","jesHFUp","jesHFDown","jesHF_2018Up","jesHF_2018Down","jesHF_2017Up","jesHF_2017Down","jesHF_2016Up","jesHF_2016Down","jesRelativeBalUp","jesRelativeBalDown","jesRelativeSample_2018Up","jesRelativeSample_2018Down","jesRelativeSample_2017Up","jesRelativeSample_2017Down","jesRelativeSample_2016Up","jesRelativeSample_2016Down"])
args = parser.parse_args()
checkFiles.args = args
submit.args = args

def main():
    
    channels     = args.channels
    years        = args.years
    tes          = args.tes
    ltf          = args.ltf
    jtf          = args.jtf
    ULtag        = args.ULtag
    preVFP       = args.preVFP
    doSVFit      = args.doSVFit
    JECvar       = args.JECvar
    batchSystem  = 'slurm_runner.sh'    
    chunkpattern = re.compile(r".*_(\d+)_[a-z]+(?:_[A-Z]+\dp\d+)?\.root")
    tag          = ""
    
    #if tes!=1.:
    #  tag += "_TES%.3f"%(tes)
    if ltf!=1.:
      tag += "_LTF%.3f"%(ltf)
    if jtf!=1.:
      tag += "_JTF%.3f"%(jtf)
    tag = tag.replace('.','p')
    
    for year in years:
      
      # GET LIST
      samplelist = [ ]
      if JECvar!="":
          outdir     = "/pnfs/psi.ch/cms/trivcat/store/user/pbaertsc/bbh/samples/%s%s%s_%s/"%(ULtag,year,preVFP,JECvar)
      else:
          if tes!="":
              outdir     = "/pnfs/psi.ch/cms/trivcat/store/user/pbaertsc/bbh/samples/%s%s%s_%s/"%(ULtag,year,preVFP,tes)
          else:
              outdir     = "/pnfs/psi.ch/cms/trivcat/store/user/pbaertsc/bbh/samples/%s%s%s/"%(ULtag,year,preVFP)
      for directory in sorted(os.listdir(outdir)):
          if not os.path.isdir(outdir+directory): continue
          if args.samples and not matchSampleToPattern(directory,args.samples): continue
          if args.vetos and matchSampleToPattern(directory,args.vetos): continue
          if args.type=='mc' and any(s in directory[:len(s)+2] for s in ['SingleMuon','SingleElectron','EGamma','MuonEG','Tau']): continue
          if args.type=='data' and not any(s in directory[:len(s)+2] for s in ['SingleMuon','SingleElectron','EGamma','MuonEG','Tau']): continue
          samplelist.append(directory)
      if not samplelist:
        print("No samples found in %s!"%(outdir))
      if args.verbose:
        print(samplelist)
      
      # RESUBMIT samples
      for channel in channels:
        print(header(year,preVFP,JECvar,tes,channel,tag))
        
        for directory in samplelist:
            if JECvar!="":
                outdir       = "/pnfs/psi.ch/cms/trivcat/store/user/pbaertsc/bbh/samples/%s%s%s_%s/%s"%(ULtag,year,preVFP,JECvar,directory)
            else:
                if tes!="":
                   outdir       = "/pnfs/psi.ch/cms/trivcat/store/user/pbaertsc/bbh/samples/%s%s%s_%s/%s"%(ULtag,year,preVFP,tes,directory) 
                else:
                   outdir       = "/pnfs/psi.ch/cms/trivcat/store/user/pbaertsc/bbh/samples/%s%s%s/%s"%(ULtag,year,preVFP,directory)
            if JECvar!="" and tes!="" and directory.find("Run")>0: #run JEC variations only for MC samples
              print("skipping data sample for JEC variation")
              continue
            #outdir       = '/pnfs/psi.ch/cms/trivcat/store/user/pbaertsc/bbh/samples/%s%s%s/%s'%(ULtag,year,preVFP,directory)
            #outfilelist  = glob.glob("%s/*_%s%s.root"%(outdir,channel,tag))
            outfilelist  = glob.glob("%s/*.root"%(outdir))
            nFilesPerJob = args.nFilesPerJob
            jobName      = directory
            if JECvar!="":
                jobName     += "_%s_%s%s%s_%s"%(channel,ULtag,year,preVFP,JECvar)+tag
                if tes!="":
                    jobName     += "_%s_%s%s%s_%s"%(channel,ULtag,year,preVFP,tes)+tag 
                else:
                    jobName     += "_%s_%s%s%s"%(channel,ULtag,year,preVFP)+tag
            #if not outfilelist: continue            
            
            # FILE LIST
            infiles = [ ]
            infiles = getFileListLocal(year,directory,preVFP,JECvar,tes)
            
           
            if not infiles:
              print(bcolors.BOLD + bcolors.WARNING + "Warning!!! FILELIST empty" + bcolors.ENDC)
              continue
            elif args.verbose:
              print("FILELIST = "+infiles[0])
              for file in infiles[1:]:
                print("           "+file)
            
            # NFILESPERJOBS
            nFilesPerJob = 1
            if args.verbose:
              print("nFilesPerJob = %s"%nFilesPerJob)
            infilelists = list(split_seq(infiles,nFilesPerJob))
            #print("infilelists:",infilelists)
            # JOB LIST
            badchunks   = [ ]
            misschunks  = list(range(0,len(infilelists)))
            if JECvar!="":
                jobList      = 'joblist/joblist_%s%s%s_%s_%s_%s%s.txt'%(ULtag,year,preVFP,JECvar,directory,channel,tag)
            else:
                if tes!="":
                    jobList      = 'joblist/joblist_%s%s%s_%s_%s_%s%s.txt'%(ULtag,year,preVFP,tes,directory,channel,tag)   
                else:
                    jobList      = 'joblist/joblist_%s%s%s_%s_%s%s.txt'%(ULtag,year,preVFP,directory,channel,tag)
            with open(jobList, 'w') as jobslog:
              for filename in outfilelist:
                  #match = chunkpattern.search(filename)
                  #if match:
                  #  chunk = int(match.group(1))
                  #else:
                  #  print bcolors.BOLD + bcolors.FAIL + '[NG] did not recognize output file %s !'%(filename) + bcolors.ENDC
                  #  exit(1)
                  chunk = int(filename.split("/")[-1].split("_")[-1].split(".")[0])
                  if chunk in misschunks:
                    misschunks.remove(chunk)
                  elif chunk >= len(infilelists):
                    print(bcolors.BOLD + bcolors.FAIL + '[WN] %s: found chunk %s >= total number of chunks %s ! Please make sure you have chosen the correct number of files per job (-n=%s), check DAS, or resubmit everything!'%(filename,chunk,len(infilelists),nFilesPerJob) + bcolors.ENDC)
                  else:
                    print(bcolors.BOLD + bcolors.FAIL + '[WN] %s: found weird chunk %s ! Please check if there is any overcounting !'%(filename,chunk) + bcolors.ENDC)
                  file = TFile(filename,'READ')
                  #if not file.IsZombie() and (file.GetListOfKeys().Contains('tree') and file.GetListOfKeys().Contains('pileup') and file.GetListOfKeys().Contains('Events')):
                  if not file.IsZombie() and file.GetListOfKeys().Contains('tree'):
                    continue
                  infiles = infilelists[chunk]
                  createJobs(jobslog,infiles,outdir,directory,chunk,channel,ULtag,preVFP,year=year,tes=tes,ltf=ltf,jtf=jtf,doSVFit=doSVFit,JECvar=JECvar)
                  badchunks.append(chunk)


              # BAD CHUNKS
              if len(badchunks)>0:
                badchunks.sort()
                chunktext = ('chunks ' if len(badchunks)>1 else 'chunk ') + ', '.join(str(ch) for ch in badchunks)
                print(bcolors.BOLD + bcolors.WARNING + '[NG] %s, %d/%d failed! Resubmitting %s...'%(directory,len(badchunks),len(outfilelist),chunktext) + bcolors.ENDC)
              
              # MISSING CHUNKS
              if len(misschunks)>0:
                chunktext = ('chunks ' if len(misschunks)>1 else 'chunk ') + ', '.join(str(i) for i in misschunks)
                print(bcolors.BOLD + bcolors.WARNING + "[WN] %s missing %d/%d files ! Resubmitting %s..."%(directory,len(misschunks),len(outfilelist)+len(misschunks),chunktext) + bcolors.ENDC)
                for chunk in misschunks:
                  infiles = infilelists[chunk]
                  createJobs(jobslog,infiles,outdir,directory,chunk,channel,ULtag,preVFP,year=year,tes=tes,ltf=ltf,jtf=jtf,doSVFit=doSVFit,JECvar=JECvar)
            
            # RESUBMIT
            nChunks = len(badchunks)+len(misschunks)
            if nChunks==0:
                print(bcolors.BOLD + bcolors.OKBLUE + '[OK] ' + directory + bcolors.ENDC)
            elif args.force:
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
            print
      
    
#    if flag:
#        print bcolors.FAIL + "[NG]" + directory + bcolors.ENDC
#        print '\t', len(files), ' out of ', str(total) + ' files are corrupted ... skip this sample (consider to resubmit the job)'
#
#    else:
#        print bcolors.BOLD + bcolors.OKBLUE + '[OK] ' + directory + bcolors.ENDC


if __name__ == '__main__':
    print()
main()
