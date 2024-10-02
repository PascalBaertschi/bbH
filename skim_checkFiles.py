#! /usr/bin/env python

import os, glob, sys, shlex, re
#import time
from fnmatch import fnmatch
import subprocess
from argparse import ArgumentParser
import ROOT; ROOT.PyConfig.IgnoreCommandLineOptions = True
from ROOT import TFile, TTree, TH1
from samplenames import getMCsamples

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

if __name__ == '__main__':
    description = '''Check if the job output files are valid, compare the number of events to DAS (-d), hadd them into one file per sample (-m), and merge datasets (-a).'''
    parser = ArgumentParser(prog="checkFiles",description=description,epilog="Good luck!")
    parser.add_argument('-y', '--year',     dest='year', choices=[2016,2017,2018], type=int, nargs='+', default=[2018], action='store',
                                            help="select year" )
    parser.add_argument('-c', '--channel',  dest='channel', choices=['mutau','etau'], nargs='+', default=['mutau'], action='store' )
    parser.add_argument('-d', '--das',      dest='compareToDas', default=False, action='store_true',
                                            help="compare number of events in output to das" )
    parser.add_argument('-D', '--das-ex',   dest='compareToDasExisting', default=False, action='store_true',
                                            help="compare number of events in existing output to das" )
    parser.add_argument('-C', '--check-ex', dest='checkExisting', default=False, action='store_true',
                                            help="check existing output (e.g. 'LHE_Njets')" )
    parser.add_argument('-f', '--force',    dest='force', default=False, action='store_true',
                                            help="overwrite existing hadd'ed files" )
    parser.add_argument('-r', '--clean',    dest='cleanup', default=False, action='store_true',
                                            help="remove all output files after hadd" )
    parser.add_argument('-R', '--rm-bad',   dest='removeBadFiles', default=False, action='store_true',
                                            help="remove files that are bad" )
    parser.add_argument('-o', '--outdir',   dest='outdir', type=str, default=None, action='store' )
    parser.add_argument('-s', '--sample',   dest='samples', type=str, nargs='+', default=[ ], action='store',
                                            help="samples to run over, glob patterns (wildcards * and ?) are allowed." )
    parser.add_argument('-x', '--veto',     dest='veto', action='store', type=str, default=None,
                                            help="veto this sample" )
    parser.add_argument('-t', '--type',     dest='type', choices=['data','mc'], type=str, default=None, action='store',
                                            help="filter data or MC to submit" )
    parser.add_argument('-T', '--tes',      dest='tes', type=str, default="no", action='store',choices=["yes","no"],
                                            help="tau energy scale" )
    parser.add_argument('-L', '--ltf',      dest='ltf', type=float, default=1.0, action='store',
                                            help="lepton to tau fake energy scale" )
    parser.add_argument('-J', '--jtf',      dest='jtf', type=float, default=1.0, action='store',
                                            help="jet to tau fake energy scale" )
    parser.add_argument('-l', '--tag',      dest='tag', type=str, default="", action='store',
                                            help="add a tag to the output file" )
    parser.add_argument('-v', '--verbose',  dest='verbose', default=False, action='store_true',
                                            help="set verbose" )
    parser.add_argument('-u', '--UL',      dest='ULtag', action='store_const', const="UL",default="UL")
    parser.add_argument('-p', '--preVFP',  dest='preVFP', action='store_const', const="_preVFP",default="")
    parser.add_argument('-j', '--JECvar', dest='JECvar', action='store', type=str, default="no",choices=["yes","no"])
    args = parser.parse_args()
else:
  args = None

def main(args):
  #from checkJobs import getSubmittedJobs
  
  years      = args.year
  ULtag      = args.ULtag
  preVFP     = args.preVFP
  channels   = args.channel
  outtag     = args.tag
  intag      = ""
  tes        = args.tes
  ltf        = args.ltf
  jtf        = args.jtf
  JECvar     = args.JECvar
  #submitted  = getSubmittedJobs()


  if outtag and '_' not in outtag[0]:
    outtag = '_'+outtag
  #if tes!=1.:
  #  intag += "_TES%.3f"%(tes)
  if ltf!=1.:
    intag += "_LTF%.3f"%(ltf)
  if jtf!=1.:
    intag += "_JTF%.3f"%(jtf)
  intag  = intag.replace('.','p')
  outtag = intag+outtag
  
  for year in years:
    if JECvar == "yes":
        indir      = "/pnfs/psi.ch/cms/trivcat/store/user/pbaertsc/bbh/samples_skim/UL%s%s_JEC/"%(year,preVFP)
    elif tes == "yes":
        indir      = "/pnfs/psi.ch/cms/trivcat/store/user/pbaertsc/bbh/samples_skim/UL%s%s_TES/"%(year,preVFP)
    os.chdir(indir)
    
    # CHECK EXISTING
    if args.checkExisting:
      for channel in channels:
        infiles  = "*/*.root"
        filelist = glob.glob(infiles)
        pattern  = infiles.split('/')[-1]
        for file in filelist:
          if not isValidSample(pattern): continue
          checkFiles(file,pattern)
      continue
    
    # GET LIST
    samplelist = [ ]
    for directory in sorted(os.listdir('./')):
      if not os.path.isdir(directory): continue
      if not isValidSample(directory): continue
      samplelist.append(directory)
    if not samplelist:
      print("No samples found in %s!"%(indir))
    if args.verbose:
      print('samplelist = %s\n'%(samplelist))
    
    # CHECK samples
    for channel in channels:
      print(header(year,preVFP,JECvar,tes,channel,intag))
      for directory in samplelist:
            
        subdir = directory
        samplename = directory
        infiles = '%s/*.root'%(directory)
        filelist = glob.glob(infiles)
        if not filelist: continue
            
        if checkFiles(filelist,directory):
            print(bcolors.BOLD + bcolors.OKGREEN + '[OK] ' + directory + ' ... can be hadded ' + bcolors.ENDC)
    os.chdir('..')
     


def isValidSample(pattern):
  if args.samples and not matchSampleToPattern(pattern,args.samples): return False
  if args.veto and matchSampleToPattern(pattern,args.veto): return False
  if args.type=='mc' and any(s in pattern[:len(s)+2] for s in ['SingleMuon','SingleElectron','EGamma','MuonEG','Tau']): return False
  if args.type=='data' and not any(s in pattern[:len(s)+2] for s in ['SingleMuon','SingleElectron','EGamma','MuonEG','Tau']): return False
  return True


indexpattern = re.compile(r".*_(\d+)_[a-z]+(?:_[A-Z]+\dp\d+)?\.root")
def checkFiles(filelist,directory,clean=False):
    if args.verbose:
      print("checkFiles: %s, %s"%(filelist,directory))
    if isinstance(filelist,str):
      filelist = [filelist]
    badfiles = [ ]
    ifound   = [ ]
    for filename in filelist:
      file  = TFile(filename, 'READ')
      isbad = False
      if file.IsZombie():
        print(bcolors.FAIL + '[NG] file %s is a zombie'%(filename) + bcolors.ENDC)
        isbad = True
      else:
        tree = file.Get('Events')
        if not isinstance(tree,TTree):
          print(bcolors.FAIL + '[NG] no tree found in ' + filename + bcolors.ENDC)
          isbad = True
      if isbad:
        badfiles.append(filename)
        #rmcmd = 'rm %s' %filename
        #print rmcmd
        #os.system(rmcmd)
      file.Close()
      #match = indexpattern.search(filename)
      #if match: ifound.append(int(match.group(1)))
      ifound.append(int(filename.split("/")[-1].split("_")[-1].split(".")[0]))

    if len(badfiles)>0:
      print(bcolors.BOLD + bcolors.FAIL + "[NG] %s:   %d out of %d files %s no tree!"%(directory,len(badfiles),len(filelist),"have" if len(badfiles)>1 else "has") + bcolors.ENDC)
      if clean:
        for filename in badfiles:
          os.remove(filename)
      return False
    # TODO: check all chunks (those>imax)
    if ifound:
      imax = max(ifound)+1
      if len(filelist)<imax:
        imiss = [ i for i in range(0,max(ifound)) if i not in ifound ]
        chunktext = ('chunks ' if len(imiss)>1 else 'chunk ') + ', '.join(str(i) for i in imiss)
        print(bcolors.BOLD + bcolors.WARNING + "[WN] %s missing %d/%d files (%s) ?"%(directory,len(imiss),len(filelist)+len(imiss),chunktext) + bcolors.ENDC)
    else:
      print(bcolors.BOLD + bcolors.WARNING + "[WN] %s did not find any valid chunk pattern in file list ?"%(directory) + bcolors.ENDC)
    
    return True
    

    
  
def getSubdir(dir):
  for subdir in subdirs:
    if '*' in subdir or '?' in subdir:
      if fnmatch(dir,subdir):
        return subdir
    else:
      if subdir==dir[:len(subdir)]:
        return subdir
  return "unknown"
  
def matchSampleToPattern(sample,patterns):
  """Match sample name to some pattern."""
  sample = sample.lstrip('/')
  if not isinstance(patterns,list):
    patterns = [patterns]
  for pattern in patterns:
    if '*' in pattern or '?' in pattern:
      if fnmatch(sample,pattern+'*'):
        return True
    else:
      if pattern in sample[:len(pattern)+1]:
        return True
  return False
  
def ensureDirectory(dirname):
  """Make directory if it does not exist."""
  if not os.path.exists(dirname):
    #os.makedirs(dirname)
    os.system("mkdir -p %s"%dirname)
    print('>>> made directory "%s"'%(dirname))
    if not os.path.exists(dirname):
      print('>>> failed to make directory "%s"'%(dirname))
  return dirname
  
headeri = 0
def header(year,preVFP,JECvar,tes,channel,tag=""):
  global headeri
  if JECvar!="":
      title  = "UL%s%s, %s, %s"%(year,preVFP,JECvar,channel)
  elif tes!="":
      title  = "UL%s%s, %s, %s"%(year,preVFP,tes,channel)
  else:
      title  = "UL%s%s, %s"%(year,preVFP,channel)
  if tag: title += ", %s"%(tag.lstrip('_'))
  string = ("\n\n" if headeri>0 else "") +\
           "   ###%s\n"    % ('#'*(len(title)+3)) +\
           "   #  %s  #\n" % (title) +\
           "   ###%s\n"    % ('#'*(len(title)+3))
  headeri += 1
  return string


if __name__ == '__main__':
    
    print()
    main(args)
    print()
