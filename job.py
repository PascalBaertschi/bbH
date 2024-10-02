#! /usr/bin/env python
import os,sys
import PhysicsTools
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetHelperRun2 import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.PrefireCorr import *
from argparse import ArgumentParser
from checkFiles import ensureDirectory
from shutil import copyfile, rmtree

infiles = "root://cms-xrd-global.cern.ch//store/user/arizzi/Nano01Fall17/DY1JetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAOD-94X-Nano01Fall17/180205_160029/0000/test94X_NANO_70.root"

parser = ArgumentParser()
parser.add_argument('-i', '--infiles', dest='infiles', action='store', type=str, default=infiles)
parser.add_argument('-o', '--outdir',  dest='outdir', action='store', type=str, default="outdir")
parser.add_argument('-N', '--outfile', dest='outfile', action='store', type=str, default="noname")
parser.add_argument('-n', '--nchunck', dest='nchunck', action='store', type=int, default='test')
parser.add_argument('-c', '--channel', dest='channel', action='store', choices=['mutau','etau'], type=str, default='mutau')
parser.add_argument('-t', '--type',    dest='type', action='store', choices=['data','mc'], default='mc')
parser.add_argument('-y', '--year',    dest='year', action='store', choices=[2016,2017,2018], type=int, default=2018)
parser.add_argument('-T', '--tes',     dest='tes', action='store', type=str, default="",choices=["","scale_t_1prongUp","scale_t_1prong1piUp","scale_t_3prongUp","scale_t_1prongDown","scale_t_1prong1piDown","scale_t_3prongDown"],)
parser.add_argument('-L', '--ltf',     dest='ltf', action='store', type=float, default=1.0)
parser.add_argument('-J', '--jtf',     dest='jtf', action='store', type=float, default=1.0)
parser.add_argument('-u', '--UL',      dest='ULtag', action='store_const', const="UL",default="")
parser.add_argument('-p', '--preVFP',  dest='preVFP', action='store_const', const="_preVFP",default="")
parser.add_argument('--doSVFit',        dest='doSVFit', action='store_true', default=False)
parser.add_argument('-j', '--JECvar', dest='JECvar', action='store', type=str, default="")
args = parser.parse_args()

channel  = args.channel
dataType = args.type
infiles  = args.infiles
outdir   = args.outdir
outfile  = args.outfile
nchunck  = args.nchunck
year     = args.year
ULtag    = args.ULtag
preVFP   = args.preVFP
JECvar   = args.JECvar
tes      = args.tes
ltf      = args.ltf
jtf      = args.jtf
kwargs   = {
  'year':  year,
  'ULtag': ULtag,
  'preVFP': preVFP,
  'tes':   tes,
  'ltf':   ltf,
  'jtf':   jtf,
  'doSVFit':args.doSVFit,
  'JECvar':args.JECvar,
}

if isinstance(infiles,str):
  infiles = infiles.split(',')

#ensureDirectory(outdir)

runJEC = False   ## jet met corrections are already applied to the preskimmed samples

dataType = 'mc'
if infiles[0].find("/Tau/")>0 or infiles[0].find("/SingleMuon/")>0 or infiles[0].find("/MuonEG/")>0 or infiles[0].find("/EGamma/")>0 or infiles[0].find("/SingleElectron/")>0 or infiles[0].find("TauEmbedding")>0 or infiles[0].find("/MET/")>0:
  dataType = 'data'            


JSON = '/work/pbaertsc/bbh/NanoTreeProducer/json/'
if year==2016:
  if ULtag=="UL":
    if preVFP=="_preVFP":
      json = JSON+'UL2016_preVFP/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt'
    else:
      json = JSON+'UL2016/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt'
  else:
    json = JSON+'Cert_271036-284044_13TeV_PromptReco_Collisions16_JSON.txt'
elif year==2017:
  if ULtag=="UL":
    json = JSON+'UL2017/Cert_294927-306462_13TeV_UL2017_Collisions17_GoldenJSON.txt'
  else:
    json = JSON+'Cert_294927-306462_13TeV_PromptReco_Collisions17_JSON.txt'
elif year==2018:
  if ULtag=="UL":
    json = JSON+'UL2018/Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt'
  else:
    json = JSON+'2018NanoAODv7/Cert_314472-325175_13TeV_PromptReco_Collisions18_JSON.txt'
  


##Function parameters
##isMC=True, dataYear=2016, runPeriod="B", jesUncert="Total", redojec=False, jetType = "AK8PFPuppi", noGroom=False, metBranchName="PuppiMET", applySmearing=True, isFastSim=False)
##All other parameters will be set in the helper module

#jmeCorrections only needed for MC
if runJEC:
  if year==2016:
    jmeCorrections = createJMECorrector(True, "2016", "B", "Total", False, "AK4PFchs", False,'PuppiMET', True, False)
  elif year==2017:
    jmeCorrections = createJMECorrector(True, "2017", "B", "Total", False, "AK4PFchs", False,'PuppiMET', True, False)
  else:
    jmeCorrections = createJMECorrector(True, "2018", "B", "Total", False, "AK4PFchs", False,'PuppiMET', True, False)
  
tag = ""
#if tes!=1: tag +="_TES%.3f"%(tes)
if ltf!=1: tag +="_LTF%.3f"%(ltf)
if jtf!=1: tag +="_JTF%.3f"%(jtf)
#outfile = "%s_%s_%s%s.root"%(outfile,nchunck,channel,tag.replace('.','p'))
#fname = "%s/%s_%i.root"%(outdir,outfile,args.nchunck)

fname = "%s/tree_%i.root"%(outdir,args.nchunck)
outdir_scratch = '/scratch/pbaertsc/bbh/%s/%s_%i'%(year,outfile,args.nchunck)
if JECvar!="":
  outdir_scratch = '/scratch/pbaertsc/bbh/%s_%s/%s_%i'%(year,JECvar,outfile,args.nchunck)
elif tes!="":
  outdir_scratch = '/scratch/pbaertsc/bbh/%s_%s/%s_%i'%(year,tes,outfile,args.nchunck)
fname_scratch = "%s/%s_%i.root"%(outdir_scratch,outfile,args.nchunck)
ensureDirectory(outdir_scratch)

print('-'*80)
print("%-12s = %s"%('input files',infiles))
print("%-12s = %s"%('output directory',outdir))
print("%-12s = %s"%('output file',outfile))
print("%-12s = %s"%('chunck',nchunck))
print("%-12s = %s"%('channel',channel))
print("%-12s = %s"%('dataType',dataType))
print("%-12s = %s"%('year',kwargs['year']))
print("%-12s = %s"%('tes',kwargs['tes']))
print("%-12s = %s"%('ltf',kwargs['ltf']))
print("%-12s = %s"%('jtf',kwargs['jtf']))
print('-'*80)


from Module import *
PrefireCorr2016 = lambda : PrefCorr('L1prefiring_jetpt_2016BtoH.root', 'L1prefiring_jetpt_2016BtoH', 'L1prefiring_photonpt_2016BtoH.root', 'L1prefiring_photonpt_2016BtoH')
PrefireCorr2017 = lambda : PrefCorr('L1prefiring_jetpt_2017BtoF.root', 'L1prefiring_jetpt_2017BtoF', 'L1prefiring_photonpt_2017BtoF.root', 'L1prefiring_photonpt_2017BtoF')
#module2run = lambda : Producer(fname, dataType, infiles, **kwargs)
module2run = lambda : Producer(fname_scratch, dataType, infiles, **kwargs)
branchsel = "keep_and_drop.txt"

print("job.py: creating PostProcessor...")

if dataType=='data':
    p = PostProcessor(outdir_scratch, infiles, None, branchsel, outputbranchsel=branchsel, noOut=False, 
                      modules=[module2run()], provenance=False, fwkJobReport=False, jsonInput=json)
else:
  if runJEC:
    if year==2018:
        p = PostProcessor(outdir_scratch, infiles, None, branchsel, outputbranchsel=branchsel, noOut=False,
                          modules=[jmeCorrections(),module2run()], provenance=False, fwkJobReport=False)
    elif year==2017:
        p = PostProcessor(outdir_scratch, infiles, None, branchsel, outputbranchsel=branchsel, noOut=False,
                          modules=[PrefireCorr2017,jmeCorrections(),module2run()], provenance=False, fwkJobReport=False)
    elif year==2016:
        p = PostProcessor(outdir_scratch, infiles, None, branchsel, outputbranchsel=branchsel, noOut=False,
                          modules=[PrefireCorr2016,jmeCorrections(),module2run()], provenance=False, fwkJobReport=False)

  else:
    if year==2018:
        p = PostProcessor(outdir_scratch, infiles, None, branchsel, outputbranchsel=branchsel, noOut=False,
                          modules=[module2run()], provenance=False, fwkJobReport=False)
    elif year==2017:
        p = PostProcessor(outdir_scratch, infiles, None, branchsel, outputbranchsel=branchsel, noOut=False,
                          modules=[module2run()], provenance=False, fwkJobReport=False)#removed PrefireCorr2017
    elif year==2016:
        p = PostProcessor(outdir_scratch, infiles, None, branchsel, outputbranchsel=branchsel, noOut=False,
                          modules=[module2run()], provenance=False, fwkJobReport=False)#removed PrefireCorr2016


print("job.py: going to run PostProcessor...")
p.run()
copyfile_from=fname_scratch
copyfile_to=fname
print("copying ",copyfile_from,"to ",copyfile_to)
#copyfile(copyfile_from,copyfile_to)
os.system("xrdcp -f %s root://t3dcachedb.psi.ch:1094/%s"%(copyfile_from,copyfile_to))
print("deleting scratch directory:",outdir_scratch)
rmtree(outdir_scratch,ignore_errors=True)

#copyfile_from = "/work/pbaertsc/bbh/NanoTreeProducer/localrun.root"
#copyfile(copyfile_from,copyfile_to)
#basename=os.path.basename(infiles[0])
#outFileName = os.path.join(outdir, basename)
#print "deleting root file with name:",outFileName
#os.remove(outFileName)

print("DONE")
