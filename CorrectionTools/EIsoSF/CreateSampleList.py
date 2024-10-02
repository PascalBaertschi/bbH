import os, math,sys
import ROOT
import copy
from optparse import OptionParser
from argparse import ArgumentParser
ROOT.gROOT.SetBatch(True)


parser = ArgumentParser()
parser.add_argument('-y','--year', dest='year', action='store', type=str,default='UL2018')
args = parser.parse_args()
year = args.year
 
samplelist = {'UL2018':
              ["DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8",
               "SingleMuon_Run2018ABCD-UL2018",
               "EGamma_Run2018ABCD-UL2018",
              ],
              'UL2017':
              ["DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8",
               "DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8_OLD",
               "SingleElectron_Run2017B-UL2017",
               "SingleElectron_Run2017C-UL2017",
               "SingleElectron_Run2017D-UL2017",
               "SingleElectron_Run2017E-UL2017",
               "SingleElectron_Run2017F-UL2017",
               "SingleMuon_Run2017B-UL2017",
               "SingleMuon_Run2017C-UL2017",
               "SingleMuon_Run2017D-UL2017",
               "SingleMuon_Run2017E-UL2017",
               "SingleMuon_Run2017F-UL2017",
                ],
              'UL2016':
              ["DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8",
               "SingleElectron_Run2016B-HIPM_UL2016",
               "SingleElectron_Run2016C-HIPM_UL2016",
               "SingleElectron_Run2016D-HIPM_UL2016",
               "SingleElectron_Run2016E-HIPM_UL2016",
               "SingleElectron_Run2016F-HIPM_UL2016",
               "SingleElectron_Run2016F-UL2016",
               "SingleElectron_Run2016G-UL2016",
               "SingleElectron_Run2016H-UL2016",
               "SingleMuon_Run2016B-HIPM_UL2016",
               "SingleMuon_Run2016C-HIPM_UL2016",
               "SingleMuon_Run2016D-HIPM_UL2016",
               "SingleMuon_Run2016E-HIPM_UL2016",
               "SingleMuon_Run2016F-HIPM_UL2016",
               "SingleMuon_Run2016F-UL2016",
               "SingleMuon_Run2016G-UL2016",
               "SingleMuon_Run2016H-UL2016"
              ],
              'UL2016_preVFP':
              ["DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8",
              ],
}


pre_path = '/pnfs/psi.ch/cms/trivcat/store/user/pbaertsc/bbh'

outputdir = "sampleslist/%s"%year

for sample in samplelist[year]:
    files = []
    if sample.split("_")[0] in ["Tau","MuonEG","SingleElectron","EGamma","SingleMuon"]:
        path ="%s/%s/%s_trigger__%s"%(pre_path,sample.split("_")[0],sample,year)
    elif sample.split("_")[0]=="MET":
        path = "%s/%s/%s__%s"%(pre_path,sample.split("_")[0],sample,year)
    elif sample.split("_")[0]=="TTTo2L2Nu":
        path = "%s/%s/%s__%s"%(pre_path,sample,sample,year)   
    elif "_ext" in sample and year=="2018":
        path = "%s/%s/%s__%s"%(pre_path,sample[:-5],sample,year)
    #elif "SUSY" in sample:
    #   path = "%s/%s/%s__2018"%(pre_path,sample,sample) 
    else:
        path = "%s/%s/%s_trigger__%s"%(pre_path,sample,sample,year)
    if os.path.isdir(path)==False:
        print("path:",path)
        print(sample,"doesn't exist")
        continue
    if len([i for i in os.listdir(path)])>1:
        print("WARNING: more than 1 directory found for",sample,"!")
    for root, dirs, fs in os.walk(path):
        for f in fs:
            if '.root' in f:
                #print(pre_path+ os.path.join(root,f))
                files.append(os.path.join(root,f))
    with open(os.path.join(outputdir,sample)+".txt",'w') as out:
        for f in files:
            out.write("{}\n".format(f))

print("done")
        
