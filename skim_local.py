#!/usr/bin/env python
import os, sys
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetHelperRun2 import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.PrefireCorr import *
from argparse import ArgumentParser
from shutil import copyfile, rmtree


parser = ArgumentParser()
parser.add_argument('-i', '--infiles',  dest='infiles', action='store', type=str, default=[ ])
parser.add_argument('-t', '--type', dest='type', action='store', choices=['data','mc'], default='mc')
parser.add_argument('-y', '--year',     dest='year', action='store', choices=[2016,2017,2018], type=int, default=2018)
parser.add_argument('-T', '--tes',      dest='tes', action='store', choices=["yes","no"], type=str, default="no")
parser.add_argument('-L', '--ltf',      dest='ltf', action='store', type=float, default=1.0)
parser.add_argument('-J', '--jtf',      dest='jtf', action='store', type=float, default=1.0)
parser.add_argument('-l', '--tag',      dest='tag', action='store', type=str, default="")
parser.add_argument('-u', '--UL',      dest='ULtag', action='store_const', const="UL",default="UL")
parser.add_argument('-p', '--preVFP',  dest='preVFP', action='store_const', const="_preVFP",default="")
parser.add_argument('--skipSVFit',     dest='doSVFit', action='store_false', default=True)
parser.add_argument('-j', '--JECvar', dest='JECvar', action='store', type=str, default="no", choices=["yes","no"])
args = parser.parse_args()

year     = args.year
ULtag    = args.ULtag
preVFP   = args.preVFP
dataType = args.type
infiles  = args.infiles
JECvar   = args.JECvar
tes      = args.tes
if args.tag and args.tag[0]!='_': args.tag = '_'+args.tag

kwargs = {
  'year':        args.year,
  'ULtag':       args.ULtag,
  'preVFP':      args.preVFP,
  'tes':         args.tes,
  'ltf':         args.ltf,
  'jtf':         args.jtf,
  'doSVFit':     args.doSVFit,
  'JECvar':      args.JECvar}

print('DataType = ', dataType)
print('year =', year)

#access directly via
#root://cms-xrd-global.cern.ch/

if year == 2016:
    if dataType =='data':
        filelist = ['/pnfs/psi.ch/cms/trivcat/store/user/pbaertsc/bbh/SingleElectron/SingleElectron_Run2016B-ver2_HIPM_UL2016_MiniAODv2_NanoAODv9-v2__UL2016/220301_164402/0000/tree_10.root']
    else:
        if preVFP=='_preVFP':
            #filelist = ['/pnfs/psi.ch/cms/trivcat/store/user/pbaertsc/bbh/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8__UL2016_preVFP/211221_220256/0000/tree_21.root']
            filelist = ['/pnfs/psi.ch/cms/trivcat/store/user/pbaertsc/bbh/WminusHToTauTau_M125_TuneCP5_13TeV-powheg-pythia8/WminusHToTauTau_M125_TuneCP5_13TeV-powheg-pythia8__UL2016_preVFP/230919_162501/0000/tree_15.root']
        else:
            filelist = ['/pnfs/psi.ch/cms/trivcat/store/user/pbaertsc/bbh/DYJetsToLL_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8/DYJetsToLL_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8__UL2016/220301_145038/0000/tree_10.root']
elif year == 2017:
    if dataType=='data':
        filelist = ['/pnfs/psi.ch/cms/trivcat/store/user/pbaertsc/bbh/SingleElectron/SingleElectron_Run2017C-UL2017_MiniAODv2_NanoAODv9-v1__UL2017/220301_162600/0000/tree_44.root']
    else:
        filelist = ['/pnfs/psi.ch/cms/trivcat/store/user/pbaertsc/bbh/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8__UL2017/211221_212736/0000/tree_9.root']
            
elif year == 2018:
    if dataType=='data':
        filelist = ['/pnfs/psi.ch/cms/trivcat/store/user/pbaertsc/bbh/EGamma/EGamma_Run2018B-UL2018_MiniAODv2_NanoAODv9-v1__UL2018/220301_161427/0000/tree_15.root']
    else:
        filelist = ['/pnfs/psi.ch/cms/trivcat/store/user/pbaertsc/bbh/samples_skim/UL2018_TES/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/tree_95.root']
        #filelist = ['/pnfs/psi.ch/cms/trivcat/store/user/pbaertsc/bbh/VBFHToTauTau_M125_TuneCP5_13TeV-powheg-pythia8/VBFHToTauTau_M125_TuneCP5_13TeV-powheg-pythia8__UL2018/210819_145748/0000/tree_31.root']
        #filelist = ['/pnfs/psi.ch/cms/trivcat/store/user/pbaertsc/bbh/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8__UL2018/210903_163213/0000/tree_7.root']
        #filelist = ['/pnfs/psi.ch/cms/trivcat/store/user/pbaertsc/bbh/bbHToTauTau_M-125_4FS_TuneCP5_yb2_13TeV-amcatnlo-pythia8/bbHToTauTau_M-125_4FS_TuneCP5_yb2_13TeV-amcatnlo-pythia8__UL2018/220201_163706/0000/tree_3.root']
infiles = filelist


branchsel = "keep_and_drop.txt"
_postfix = 'localrun.root'

if JECvar=="yes":
    from skim_Module import *
elif tes=="yes":
    from skimTES_Module import *
prefirecorr = lambda : PrefCorr()
PrefireCorr2016 = lambda : PrefCorr('L1prefiring_jetpt_2016BtoH.root', 'L1prefiring_jetpt_2016BtoH', 'L1prefiring_photonpt_2016BtoH.root', 'L1prefiring_photonpt_2016BtoH')
PrefireCorr2017 = lambda : PrefCorr('L1prefiring_jetpt_2017BtoF.root', 'L1prefiring_jetpt_2017BtoF', 'L1prefiring_photonpt_2017BtoF.root', 'L1prefiring_photonpt_2017BtoF')
module2run = lambda : Producer(_postfix, dataType, filelist, **kwargs)



if dataType == 'data':
    p=PostProcessor(".",filelist,None,branchsel,noOut=False, modules=[module2run()],provenance=False)
else:
    if year==2018:
        p = PostProcessor(".", filelist, None, branchsel, outputbranchsel=branchsel, noOut=False,
                          modules=[module2run()], provenance=False, fwkJobReport=False)
    elif year==2017:
        p = PostProcessor(".", filelist, None, branchsel, outputbranchsel=branchsel, noOut=False,
                          modules=[module2run()], provenance=False, fwkJobReport=False)
    elif year==2016:
        p = PostProcessor(".", filelist, None, branchsel, outputbranchsel=branchsel, noOut=False,
                          modules=[module2run()], provenance=False, fwkJobReport=False)


p.run()
outFileName = os.path.join('.', os.path.basename(infiles[0]))
filename = os.path.basename(infiles[0])

print("deleting root file with name:",outFileName)
os.remove(outFileName)

