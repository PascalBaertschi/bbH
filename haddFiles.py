#! /usr/bin/env python

import os, glob, sys, shlex, re
#import time
from fnmatch import fnmatch
import subprocess
from argparse import ArgumentParser
import ROOT; ROOT.PyConfig.IgnoreCommandLineOptions = True
from ROOT import TFile, TTree, TH1, Double

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
    parser.add_argument('-y', '--year',     dest='years', choices=[2016,2017,2018], type=int, nargs='+', default=[2017], action='store',
                                            help="select year" )
    parser.add_argument('-c', '--channel',  dest='channels', choices=['ll'], nargs='+', default=['ll'], action='store' )
    parser.add_argument('-m', '--make',     dest='make', default=False, action='store_true',
                                            help="hadd all output files" )
    parser.add_argument('-a', '--hadd',     dest='haddother', default=False, action='store_true',
                                            help="hadd some samples into one (e.g. all data sets, or the extensions)" )
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
    parser.add_argument('-T', '--tes',      dest='tes', type=float, default=1.0, action='store',
                                            help="tau energy scale" )
    parser.add_argument('-L', '--ltf',      dest='ltf', type=float, default=1.0, action='store',
                                            help="lepton to tau fake energy scale" )
    parser.add_argument('-J', '--jtf',      dest='jtf', type=float, default=1.0, action='store',
                                            help="jet to tau fake energy scale" )
    parser.add_argument('-l', '--tag',      dest='tag', type=str, default="", action='store',
                                            help="add a tag to the output file" )
    parser.add_argument('-v', '--verbose',  dest='verbose', default=False, action='store_true',
                                            help="set verbose" )
    args = parser.parse_args()
else:
  args = None

def main(args):
  #from checkJobs import getSubmittedJobs
  
  years      = args.years
  channels   = args.channels
  outtag     = args.tag
  intag      = ""
  tes        = args.tes
  ltf        = args.ltf
  jtf        = args.jtf
  #submitted  = getSubmittedJobs()
  samplesdir = '/work/pbaertsc/heavy_resonance/2017_2018'
  inputdir = '/work/pbaertsc/heavy_resonance'
  years = ['2017','2018']
  haddsets = [
     ('DY',             "DYJetsToLL_HT-70to100"            ),
     ('DY',             "DYJetsToLL_HT-100to200"           ),
     ('DY',             "DYJetsToLL_HT-200to400"           ),
     ('DY',             "DYJetsToLL_HT-400to600"           ),
     ('DY',             "DYJetsToLL_HT-600to800"           ),
     ('DY',             "DYJetsToLL_HT-800to1200"          ),
     ('DY',             "DYJetsToLL_HT-1200to2500"         ),
     ('DY',             "DYJetsToLL_HT-2500toInf"          ),
     ('ZJ',             "ZJetsToNuNu_HT-100to200"          ),
     ('ZJ',             "ZJetsToNuNu_HT-200to400"          ),
     ('ZJ',             "ZJetsToNuNu_HT-400to600"          ),
     ('ZJ',             "ZJetsToNuNu_HT-600to800"          ),
     ('ZJ',             "ZJetsToNuNu_HT-800to1200"         ),
     ('ZJ',             "ZJetsToNuNu_HT-1200to2500"        ),
     ('ZJ',             "ZJetsToNuNu_HT-2500toInf"         ),
     ('WJ',             "WJetsToLNu_HT-100to200"           ),
     ('WJ',             "WJetsToLNu_HT-200to400"           ),
     ('WJ',             "WJetsToLNu_HT-400to600"           ),
     ('WJ',             "WJetsToLNu_HT-600to800"           ),
     ('WJ',             "WJetsToLNu_HT-800to1200"          ),
     ('WJ',             "WJetsToLNu_HT-1200to2500"         ),
     ('WJ',             "WJetsToLNu_HT-2500toInf"          ),
     ('ST',             "ST_s-channel"                     ),
     ('ST',             "ST_t-channel_antitop"             ),
     ('ST',             "ST_t-channel_top"                 ),
     ('ST',             "ST_tW_antitop"                    ),
     ('ST',             "ST_tW_top"                        ),
     ('TT',             "TTTo2L2Nu"                        ),
     ('TT',             "TTToSemiLeptonic"                 ),
     ('TT',             "TTWJetsToLNu"                     ),
     ('TT',             "TTZToLLNuNu"                      ),
     ('VV',             "WWTo1L1Nu2Q"                      ),
     ('VV',             "WWTo2L2Nu"                        ),
     ('VV',             "WWTo4Q"                           ),
     ('VV',             "WZTo1L1Nu2Q"                      ),
     ('VV',             "WZTo2L2Q"                         ),
     ('VV',             "ZZTo2L2Q"                         ),
     ('VV',             "ZZTo2Q2Nu"                        ),
     ('VV',             "ZZTo2L2Nu"                        ),
     ('VV',             "ZZTo4L"                           ),
     ('VV',             "GluGluHToBB"                      ),
     ('XZH',            "ZprimeToZHToZlepHinc_narrow_M600" ),
     ('XZH',            "ZprimeToZHToZlepHinc_narrow_M800" ),
     ('XZH',            "ZprimeToZHToZlepHinc_narrow_M1000"),
     ('XZH',            "ZprimeToZHToZlepHinc_narrow_M1200"),
     ('XZH',            "ZprimeToZHToZlepHinc_narrow_M1400"),
     ('XZH',            "ZprimeToZHToZlepHinc_narrow_M1600"),
     ('XZH',            "ZprimeToZHToZlepHinc_narrow_M1800"),
     ('XZH',            "ZprimeToZHToZlepHinc_narrow_M2000"),
     ('XZH',            "ZprimeToZHToZlepHinc_narrow_M2500"),
     ('XZH',            "ZprimeToZHToZlepHinc_narrow_M3000"),
     ('XZH',            "ZprimeToZHToZlepHinc_narrow_M3500"),
     ('XZH',            "ZprimeToZHToZlepHinc_narrow_M4000"),
     ('XZH',            "ZprimeToZHToZlepHinc_narrow_M4500"),
     ('XZH',            "ZprimeToZHToZlepHinc_narrow_M5000"),
     ('XZH',            "ZprimeToZHToZlepHinc_narrow_M5500"),
     ('XZH',            "ZprimeToZHToZlepHinc_narrow_M6000"),
     ('XZH',            "ZprimeToZHToZlepHinc_narrow_M7000"),
     ('XZH',            "ZprimeToZHToZlepHinc_narrow_M8000"),
     ('XZH',            "ZprimeToZHToZinvHinc_narrow_M600" ),
     ('XZH',            "ZprimeToZHToZinvHinc_narrow_M800" ),
     ('XZH',            "ZprimeToZHToZinvHinc_narrow_M1000"),
     ('XZH',            "ZprimeToZHToZinvHinc_narrow_M1200"),
     ('XZH',            "ZprimeToZHToZinvHinc_narrow_M1400"),
     ('XZH',            "ZprimeToZHToZinvHinc_narrow_M1600"),
     ('XZH',            "ZprimeToZHToZinvHinc_narrow_M1800"),
     ('XZH',            "ZprimeToZHToZinvHinc_narrow_M2000"),
     ('XZH',            "ZprimeToZHToZinvHinc_narrow_M2500"),
     ('XZH',            "ZprimeToZHToZinvHinc_narrow_M3000"),
     ('XZH',            "ZprimeToZHToZinvHinc_narrow_M3500"),
     ('XZH',            "ZprimeToZHToZinvHinc_narrow_M4000"),
     ('XZH',            "ZprimeToZHToZinvHinc_narrow_M4500"),
     ('XZH',            "ZprimeToZHToZinvHinc_narrow_M5000"),
     ('XZH',            "ZprimeToZHToZinvHinc_narrow_M5500"),
     ('XZH',            "ZprimeToZHToZinvHinc_narrow_M6000"),
     ('XZH',            "ZprimeToZHToZinvHinc_narrow_M7000"),
     ('XZH',            "ZprimeToZHToZinvHinc_narrow_M8000"), 
     ('SingleMuon',     "SingleMuon" ),
     ('SingleElectron', "SingleElectron"),
     ('MET',            "MET"   )]
  for subdir, samplename in haddsets:
      outdir  = "%s/%s"%(samplesdir,subdir)
      outfile = "%s/%s.root"%(outdir,samplename)
      infiles = []
      for year in years:
          if subdir=='SingleElectron' and year=='2018':
              infiles.append('%s/%s/%s/%s.root'%(inputdir,year,'EGamma','EGamma'))
          else:
              infiles.append('%s/%s/%s/%s.root'%(inputdir,year,subdir,samplename))
      ensureDirectory(outdir)
      # CHECK FILES
      allinfiles = [ ]
      for infile in infiles[:]:
          if '*' in infile or '?' in infile:
              files = glob.glob(infile)
              allinfiles += files
              if not files:
                  print bcolors.BOLD + bcolors.FAIL + '[NG] no match for the glob pattern %s! Removing pattern from hadd list for "%s"...'%(infile,samplename) + bcolors.ENDC
                  infiles.remove(infile)
          elif not os.path.isfile(infile):
              print bcolors.BOLD + bcolors.FAIL + '[NG] infile %s does not exists! Removing from hadd list for "%s"...'%(infile,samplename) + bcolors.ENDC
              infiles.remove(infile)
          else:
              allinfiles.append(infile)
            
      # HADD
      if args.verbose:
          print "infiles =", infiles
          print "allfiles =", allinfiles
      if len(allinfiles)==1:
          print bcolors.BOLD + bcolors.WARNING + "[WN] found only one file (%s) to hadd to %s!"%(allinfiles[0],outfile) + bcolors.ENDC 
      elif len(allinfiles)>1:
          print bcolors.BOLD + bcolors.OKGREEN + '[OK] hadding %s' %(outfile) + bcolors.ENDC
          haddcmd = 'hadd -f %s %s'%(outfile,' '.join(infiles))
          print haddcmd
          os.system(haddcmd)
      else:
          print bcolors.BOLD + bcolors.WARNING + "[WN] no files to hadd!" + bcolors.ENDC
    
      os.chdir('..')

def ensureDirectory(dirname):
  """Make directory if it does not exist."""
  if not os.path.exists(dirname):
    os.makedirs(dirname)
    print '>>> made directory "%s"'%(dirname)
    if not os.path.exists(dirname):
      print '>>> failed to make directory "%s"'%(dirname)
  return dirname


if __name__ == '__main__':
    
    print
    main(args)
    print
