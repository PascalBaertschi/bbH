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
parser.add_argument('-T', '--tes',      dest='tes', action='store', type=float, default=1.0)
parser.add_argument('-L', '--ltf',      dest='ltf', action='store', type=float, default=1.0)
parser.add_argument('-J', '--jtf',      dest='jtf', action='store', type=float, default=1.0)
parser.add_argument('-l', '--tag',      dest='tag', action='store', type=str, default="")
parser.add_argument('-u', '--UL',      dest='ULtag', action='store_const', const="UL",default="UL")
parser.add_argument('-p', '--preVFP',  dest='preVFP', action='store_const', const="_preVFP",default="")
parser.add_argument('--skipSVFit',     dest='doSVFit', action='store_false', default=True)
parser.add_argument('-j', '--JECvar', dest='JECvar', action='store', type=str, default="")
args = parser.parse_args()

year     = args.year
ULtag    = args.ULtag
preVFP   = args.preVFP
dataType = args.type
infiles  = args.infiles
JECvar   = args.JECvar
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
        #filelist = ['/pnfs/psi.ch/cms/trivcat/store/user/pbaertsc/bbh/SingleElectron/SingleElectron_Run2016G-UL2016_trigger__UL2016/220610_195946/0000/tree_4.root']
        filelist = ['/pnfs/psi.ch/cms/trivcat/store/user/pbaertsc/bbh/SingleElectron/SingleElectron_Run2016F-UL2016_trigger__UL2016/220610_195830/0000/tree_3.root']
        #filelist =['/pnfs/psi.ch/cms/trivcat/store/user/pbaertsc/bbh/SingleElectron/SingleElectron_Run2016F-HIPM_UL2016_trigger__UL2016/220610_195717/0000/tree_5.root']
    else:
        if preVFP=='_preVFP':
            filelist = ['/pnfs/psi.ch/cms/trivcat/store/user/pbaertsc/bbh/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8__UL2016_preVFP/211221_220256/0000/tree_21.root']
        else:
            filelist = ['/pnfs/psi.ch/cms/trivcat/store/user/pbaertsc/bbh/bbHToTauTau_M-125_4FS_TuneCP5_yb2_13TeV-amcatnlo-pythia8/bbHToTauTau_M-125_4FS_TuneCP5_yb2_13TeV-amcatnlo-pythia8__UL2016/210930_063921/0000/tree_2.root']
elif year == 2017:
    if dataType=='data':
        #filelist = ['/pnfs/psi.ch/cms/trivcat/store/user/pbaertsc/bbh/SingleElectron/SingleElectron_Run2017C-UL2017_MiniAODv1_NanoAODv2-v1__UL2017/210521_182427/0000/tree_44.root']
        filelist = ['/pnfs/psi.ch/cms/trivcat/store/user/pbaertsc/bbh/SingleMuon/SingleMuon_Run2017C-UL2017_trigger__UL2017/220726_104046/0000/tree_4.root']
    else:
        #filelist = ['/pnfs/psi.ch/cms/trivcat/store/user/pbaertsc/bbh/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8_trigger__UL2017_newerOLD/220726_103833/0000/tree_21.root']
        filelist = ['/pnfs/psi.ch/cms/trivcat/store/user/pbaertsc/bbh/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8_trigger__UL2017/220803_083629/0000/tree_21.root']
elif year == 2018:
    if dataType=='data':
        filelist = ['/pnfs/psi.ch/cms/trivcat/store/user/pbaertsc/bbh/SingleMuon/SingleMuon_Run2018B-UL2018_MiniAODv1_NanoAODv2-v1__UL2018/210225_132044/0000/tree_14.root']
    else:
        #filelist = ['/pnfs/psi.ch/cms/trivcat/store/user/pbaertsc/bbh/WJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-pythia8/WJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-pythia8__UL2018/211221_194455/0000/tree_12.root']
        #filelist = ['/pnfs/psi.ch/cms/trivcat/store/user/pbaertsc/bbh/bbHToTauTau_M-125_4FS_ybyt_TuneCP5-13TeV-amcatnlo-pythia8/bbHToTauTau_M-125_4FS_ybyt_TuneCP5-13TeV-amcatnlo-pythia8__UL2018/220428_125132/0000/tree_2.root']
        #filelist = ['/pnfs/psi.ch/cms/trivcat/store/user/pbaertsc/bbh/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8_trigger__UL2018/220530_141733/0000/tree_4.root']
        filelist = ['/pnfs/psi.ch/cms/trivcat/store/user/pbaertsc/bbh/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8__UL2018/210903_163213/0000/tree_96.root']
   
       
infiles = filelist


branchsel = "keep_and_drop.txt"
_postfix = 'localrun.root'

from Module_deriveSF import *
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

