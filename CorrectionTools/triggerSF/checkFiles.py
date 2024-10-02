#! /usr/bin/env python

import os, glob, sys, shlex, re
#import time
from fnmatch import fnmatch
import subprocess
from argparse import ArgumentParser
import ROOT; ROOT.PyConfig.IgnoreCommandLineOptions = True
from ROOT import TFile, TTree, TH1

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
    parser.add_argument('-c', '--channel',  dest='channel', choices=['mutau','etau','tautau'], nargs='+', default=['mutau'], action='store' )
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
    parser.add_argument('-u', '--UL',      dest='ULtag', action='store_const', const="UL",default="UL")
    parser.add_argument('-p', '--preVFP',  dest='preVFP', action='store_const', const="_preVFP",default="")
    parser.add_argument('-j', '--JECvar', dest='JECvar', action='store', type=str, default="")
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
  if tes!=1.:
    intag += "_TES%.3f"%(tes)
  if ltf!=1.:
    intag += "_LTF%.3f"%(ltf)
  if jtf!=1.:
    intag += "_JTF%.3f"%(jtf)
  intag  = intag.replace('.','p')
  outtag = intag+outtag
  
  for year in years:
    indir      = "/pnfs/psi.ch/cms/trivcat/store/user/pbaertsc/bbh/samples/triggerSF/%s%s%s/"%(ULtag,year,preVFP)
    samplesdir = args.outdir if args.outdir else "/pnfs/psi.ch/cms/trivcat/store/user/pbaertsc/bbh/triggerSF/samples_%s%s%s"%(ULtag,year,preVFP)
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
      print(header(year,preVFP,JECvar,channel,intag))
      
      # HADD samples
      if not args.haddother or args.make:
        for directory in samplelist:
            if args.verbose:
              print(directory)
            
            #subdir, samplename = getSampleShortName(directory,year)
            subdir = directory
            samplename = directory
            outdir  = "/pnfs/psi.ch/cms/trivcat/store/user/pbaertsc/bbh/triggerSF/samples_%s%s%s"%(ULtag,year,preVFP)
            outfile = "%s/%s.root"%(outdir,samplename)
            infiles = '%s/*.root'%(directory)
            
            if args.verbose:
              print("directory = %s"%(directory))
              print("outdir    = %s"%(outdir))
              print("outfile   = %s"%(outfile))
              print("infiles   = %s"%(infiles))
            
            filelist = glob.glob(infiles)
            if not filelist: continue
            
            if checkFiles(filelist,directory):
              print(bcolors.BOLD + bcolors.OKGREEN + '[OK] ' + directory + ' ... can be hadded ' + bcolors.ENDC)
            
            if args.compareToDas:
                compareEventsToDAS(filelist,directory)
            if args.compareToDasExisting and os.path.isfile(outfile):
                print('   check existing file %s:'%(outfile))
                compareEventsToDAS(outfile,directory)
            
            # HADD
            if args.make:
                ensureDirectory(outdir)
                if os.path.isfile(outfile):
                  if args.force:
                    print(bcolors.BOLD + bcolors.WARNING + "   [WN] target %s already exists! Overwriting..."%(outfile) + bcolors.ENDC)
                  else:
                    print(bcolors.BOLD + bcolors.FAIL + "   [NG] target %s already exists! Use --force or -f to overwrite."%(outfile) + bcolors.ENDC)
                    continue
                haddcmd = 'hadd -f %s %s'%(outfile,infiles)
                print(haddcmd)
                os.system(haddcmd)
                # CLEAN UP
                if args.cleanup:
                  rmcmd = 'rm -rf %s'%directory
                  print(bcolors.BOLD + bcolors.OKBLUE + "   removing %d output files for %s..."%(len(infiles),directory) + bcolors.ENDC)
                  os.system(rmcmd)  
      # HADD other
      if year == 2018:
          haddsets = [
                  ('SingleMuon', 'SingleMuon_Run2018ABCD', ['SingleMuon_Run2018A-UL2018','SingleMuon_Run2018B-UL2018','SingleMuon_Run2018C-UL2018','SingleMuon_Run2018D-UL2018']),
                  ('EGamma', 'EGamma_Run2018ABCD', ['EGamma_Run2018A-UL2018','EGamma_Run2018B-UL2018','EGamma_Run2018C-UL2018','EGamma_Run2018D-UL2018'])]
      elif year==2017:
          haddsets = [
                  ('SingleMuon', 'SingleMuon_Run2017BCDEF', ['SingleMuon_Run2017B-UL2017','SingleMuon_Run2017C-UL2017','SingleMuon_Run2017D-UL2017','SingleMuon_Run2017E-UL2017','SingleMuon_Run2017F-UL2017']),
                  ('SingleElectron', 'SingleElectron_Run2017BCDEF', ['SingleElectron_Run2017B-UL2017','SingleElectron_Run2017C-UL2017','SingleElectron_Run2017D-UL2017','SingleElectron_Run2017E-UL2017','SingleElectron_Run2017F-UL2017'])]
      elif year==2016:
          haddsets = [
              ('SingleMuon', 'SingleMuon_Run2016BCDEFGH', ['SingleMuon_Run2016B-HIPM_UL2016','SingleMuon_Run2016C-HIPM_UL2016','SingleMuon_Run2016D-HIPM_UL2016','SingleMuon_Run2016E-HIPM_UL2016','SingleMuon_Run2016F-HIPM_UL2016','SingleMuon_Run2016F-UL2016','SingleMuon_Run2016G-UL2016','SingleMuon_Run2016H-UL2016']),
              ('SingleMuon', 'SingleMuon_Run2016BCDEF', ['SingleMuon_Run2016B-HIPM_UL2016','SingleMuon_Run2016C-HIPM_UL2016','SingleMuon_Run2016D-HIPM_UL2016','SingleMuon_Run2016E-HIPM_UL2016','SingleMuon_Run2016F-HIPM_UL2016']),
              ('SingleMuon', 'SingleMuon_Run2016FGH', ['SingleMuon_Run2016F-UL2016','SingleMuon_Run2016G-UL2016','SingleMuon_Run2016H-UL2016']),
              ('SingleElectron', 'SingleElectron_Run2016BCDEFGH', ['SingleElectron_Run2016B-HIPM_UL2016','SingleElectron_Run2016C-HIPM_UL2016','SingleElectron_Run2016D-HIPM_UL2016','SingleElectron_Run2016E-HIPM_UL2016','SingleElectron_Run2016F-HIPM_UL2016','SingleElectron_Run2016F-UL2016','SingleElectron_Run2016G-UL2016','SingleElectron_Run2016H-UL2016']),
              ('SingleElectron', 'SingleElectron_Run2016BCDEF', ['SingleElectron_Run2016B-HIPM_UL2016','SingleElectron_Run2016C-HIPM_UL2016','SingleElectron_Run2016D-HIPM_UL2016','SingleElectron_Run2016E-HIPM_UL2016','SingleElectron_Run2016F-HIPM_UL2016']),
              ('SingleElectron', 'SingleElectron_Run2016FGH', ['SingleElectron_Run2016F-UL2016','SingleElectron_Run2016G-UL2016','SingleElectron_Run2016H-UL2016'])]
          
      if args.haddother:
        if year==2016:
            #workdir = "/work/pbaertsc/bbh/NanoTreeProducer"
            workdir = "/pnfs/psi.ch/cms/trivcat/store/user/pbaertsc/bbh/triggerSF"
            print("hadd UL2016 MC files")
            sample = "DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8"
            haddcmd = 'hadd -f %s/samples_UL2016_comb/%s.root %s/samples_UL2016/%s.root %s/samples_UL2016_preVFP/%s.root'%(workdir,sample,workdir,sample,workdir,sample)
            os.system(haddcmd)
            if JECvar=="": #for JECvariations no need to copy data
                print("copying data samples to comb")
                for sample in ['SingleMuon_Run2016BCDEFGH','SingleElectron_Run2016BCDEFGH','SingleMuon_SingleElectron_Run2016BCDEFGH']:
                    haddcmd = 'cp -f %s/samples_UL2016/%s.root %s/samples_UL2016_comb/%s.root'%(workdir,sample,workdir,sample)
                    os.system(haddcmd)
        for subdir, samplename, sampleset in haddsets:
            if args.verbose:
              print(subdir, samplename, sampleset)
            if args.samples and not matchSampleToPattern(samplename,args.samples): continue
            if args.veto and matchSampleToPattern(directory,args.veto): continue
            if '2016' in samplename and year!=2016: continue
            if '2017' in samplename and year!=2017: continue
            if '2018' in samplename and year!=2018: continue
            #if '$RUN' in samplename:
            #  samplename = samplename.replace('$RUN','Run%d'%year)
            #  sampleset  = [s.replace('$RUN','Run%d'%year) for s in sampleset]
            
            outdir  = "%s"%(samplesdir)
            outfile = "%s/%s%s.root"%(outdir,samplename,outtag)
            #infiles = ['%s/%s.root'%(samplesdir,s) for s in sampleset] #.replace('ele','e')
            infiles = ['%s/%s/*.root'%(indir,s) for s in sampleset] #.replace('ele','e')
            ensureDirectory(outdir)
            
            # OVERWRITE ?
            if os.path.isfile(outfile):
              if args.force:
                pass
              else:
                print(bcolors.BOLD + bcolors.FAIL + "[NG] target %s already exists! Use --force or -f to overwrite."%(outfile) + bcolors.ENDC)
                continue
            
            # CHECK FILES
            allinfiles = [ ]
            for infile in infiles[:]:
              if '*' in infile or '?' in infile:
                files = glob.glob(infile)
                allinfiles += files
                if not files:
                  print(bcolors.BOLD + bcolors.FAIL + '[NG] no match for the glob pattern %s! Removing pattern from hadd list for "%s"...'%(infile,samplename) + bcolors.ENDC)
                  infiles.remove(infile)
              elif not os.path.isfile(infile):
                print(bcolors.BOLD + bcolors.FAIL + '[NG] infile %s does not exists! Removing from hadd list for "%s"...'%(infile,samplename) + bcolors.ENDC)
                infiles.remove(infile)
              else:
                allinfiles.append(infile)
            
            # HADD
            if args.verbose:
              print("infiles =", infiles)
              print("allfiles =", allinfiles)
            if len(allinfiles)==1:
              print(bcolors.BOLD + bcolors.WARNING + "[WN] found only one file (%s) to hadd to %s!"%(allinfiles[0],outfile) + bcolors.ENDC) 
            elif len(allinfiles)>1:
              print(bcolors.BOLD + bcolors.OKGREEN + '[OK] hadding %s' %(outfile) + bcolors.ENDC)
              haddcmd = 'hadd -f %s %s'%(outfile,' '.join(infiles))
              print(haddcmd)
              os.system(haddcmd)
              if year==2016:
                  copyfiles =  'cp -f %s/samples_UL2016/%s %s/samples_UL2016_comb/%s'%(workdir,outfile.split("/")[-1],workdir,outfile.split("/")[-1])
                  print(copyfiles)
                  os.system(copyfiles)
                  copyfiles_preVFP =  'cp -f %s/samples_UL2016/%s %s/samples_UL2016_preVFP/%s'%(workdir,outfile.split("/")[-1],workdir,outfile.split("/")[-1])
                  print(copyfiles_preVFP)
                  os.system(copyfiles_preVFP)
            else:
              print(bcolors.BOLD + bcolors.WARNING + "[WN] no files to hadd!" + bcolors.ENDC)
            print()
    
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
        tree = file.Get('tree')
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
    
def compareEventsToDAS(filenames,dasname):
    """Compare a number of processed events in an output file to the available number of events in DAS."""
    dasname = dasname.replace('__', '/')
    if args.verbose:
      print("compareEventsToDAS: %s, %s"%(filenames,dasname))
      #start = time.time()
    if isinstance(filenames,str):
      filenames = [filenames]
    total_processed = 0
    nfiles = len(filenames)
    for filename in filenames:
      file = TFile(filename, 'READ')
      if file.IsZombie():
        continue
      #else:
      #  print bcolors.FAIL + '[NG] compareEventsToDAS: no cutflow found in ' + filename + bcolors.ENDC
      file.Close()
    
    instance = 'prod/phys03' if 'USER' in dasname else 'prod/global'
    dascmd   = 'das_client --limit=0 --query=\"summary dataset=/%s instance=%s\"'%(dasname,instance)
    if args.verbose:
      print(dascmd)
    dasargs  = shlex.split(dascmd)
    output, error = subprocess.Popen(dasargs, stdout = subprocess.PIPE, stderr= subprocess.PIPE).communicate()
    
    if not "nevents" in output:
        print(bcolors.BOLD + bcolors.FAIL + '   [NG] Did not find nevents for "%s" in DAS. Return message:'%(dasname) + bcolors.ENDC) 
        print(bcolors.FAIL + '     ' + output + bcolors.ENDC)
        return False
    total_das = output.split('"nevents":')[1].split(',')[0]
    fraction = total_processed/total_das
    
    nfiles = ", %d files"%(nfiles) if nfiles>1 else ""
    if fraction > 1.001:
        print(bcolors.BOLD + bcolors.FAIL + '   [NG] DAS entries = %d, Processed in tree = %d (frac = %.2f > 1%s)'%(total_das,total_processed,fraction,nfiles) + bcolors.ENDC)
    elif fraction > 0.8:
        print(bcolors.BOLD + bcolors.OKBLUE + '   [OK] DAS entries = %d, Processed in tree = %d (frac = %.2f%s)'%(total_das,total_processed,fraction,nfiles) + bcolors.ENDC)
    else:
        print(bcolors.BOLD + bcolors.FAIL + '   [NG] DAS entries = %d, Processed in tree = %d (frac = %.2f < 0.8%s)'%(total_das,total_processed,fraction,nfiles) + bcolors.ENDC)
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
def header(year,preVFP,JECvar,channel,tag=""):
  global headeri
  if JECvar!="":
      title  = "UL%s%s, %s, %s"%(year,preVFP,JECvar,channel)
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
