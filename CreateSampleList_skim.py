import os, math,sys
import ROOT
import copy
from optparse import OptionParser
from argparse import ArgumentParser
ROOT.gROOT.SetBatch(True)


parser = ArgumentParser()
parser.add_argument('-y','--year', dest='year', action='store', type=str)
parser.add_argument('-T', '--tes',      dest='tes', type=str, default="no", action='store',choices=["yes","no"])
parser.add_argument('-j', '--JECvar', dest='JECvar', action='store', type=str, default="no",choices=["yes","no"])
args = parser.parse_args()
year = args.year
JECvar = args.JECvar
tes = args.tes
 
samplelist = {'UL2018':
              ["TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8",
              "TTToHadronic_TuneCP5_13TeV-powheg-pythia8",
              "TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8",
              "ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8",
              "ST_t-channel_top_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8",
              "ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-amcatnlo-pythia8",
              "ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8",
              "ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8",
              "bbHToTauTau_M-125_4FS_TuneCP5_yb2_13TeV-amcatnlo-pythia8",
              "bbHToTauTau_M-125_4FS_TuneCP5_yt2_13TeV-amcatnlo-pythia8",
              "jjHToTauTau_M-125_4FS_TuneCP5_yb2_13TeV-amcatnlo-pythia8",
              "jjHToTauTau_M-125_4FS_TuneCP5_yt2_13TeV-amcatnlo-pythia8",
              "GluGluHToTauTau_M-125_TuneCP5_13TeV-amcatnloFXFX-pythia8", 
              "GluGlujjHToTauTau_M-125_TuneCP5_13TeV-amcatnloFXFX-pythia8",
              "bbHToTauTau_M-125_4FS_ybyt_TuneCP5-13TeV-amcatnlo-pythia8",
              "jjHToTauTau_M-125_4FS_ybyt_TuneCP5-13TeV-amcatnlo-pythia8",
              "VBFHToTauTau_M125_TuneCP5_13TeV-powheg-pythia8",
              "ttHToTauTau_M125_TuneCP5_13TeV-powheg-pythia8",
              "ZHToTauTau_M125_CP5_13TeV-powheg-pythia8_ext1",
              "WplusHToTauTau_M125_TuneCP5_13TeV-powheg-pythia8",
              "WminusHToTauTau_M125_TuneCP5_13TeV-powheg-pythia8",
              "WWTo2L2Nu_TuneCP5_13TeV-powheg-pythia8",
              "WWTo1L1Nu2Q_4f_TuneCP5_13TeV-amcatnloFXFX-pythia8",
              "WWTo4Q_4f_TuneCP5_13TeV-amcatnloFXFX-pythia8",
              "WZTo3LNu_TuneCP5_13TeV-amcatnloFXFX-pythia8",
              "WZTo2Q2L_mllmin4p0_TuneCP5_13TeV-amcatnloFXFX-pythia8",
              "WZTo1L3Nu_4f_TuneCP5_13TeV-amcatnloFXFX-pythia8",
              "WZTo1L1Nu2Q_4f_TuneCP5_13TeV-amcatnloFXFX-pythia8",
              "ZZTo4L_TuneCP5_13TeV_powheg_pythia8",
              "ZZTo2Q2L_mllmin4p0_TuneCP5_13TeV-amcatnloFXFX-pythia8",
              "ZZTo2Nu2Q_5f_TuneCP5_13TeV-amcatnloFXFX-pythia8", 
              "ZZTo2L2Nu_TuneCP5_13TeV_powheg_pythia8",
              "DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8",
              "DYJetsToLL_0J_TuneCP5_13TeV-amcatnloFXFX-pythia8",
              "DYJetsToLL_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8",
              "DYJetsToLL_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8",
              "WJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-pythia8",
              "WJetsToLNu_0J_TuneCP5_13TeV-amcatnloFXFX-pythia8",
              "WJetsToLNu_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8",
              "WJetsToLNu_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8",
              ],
              'UL2017':
              ["TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8",
              "TTToHadronic_TuneCP5_13TeV-powheg-pythia8",
              "TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8",
              "ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8",
              "ST_t-channel_top_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8",
              "ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-amcatnlo-pythia8",
              "ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8",
              "ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8",
              "bbHToTauTau_M-125_4FS_TuneCP5_yb2_13TeV-amcatnlo-pythia8",
              "bbHToTauTau_M-125_4FS_TuneCP5_yt2_13TeV-amcatnlo-pythia8",
              "jjHToTauTau_M-125_4FS_TuneCP5_yb2_13TeV-amcatnlo-pythia8",
              "jjHToTauTau_M-125_4FS_TuneCP5_yt2_13TeV-amcatnlo-pythia8",
              "GluGluHToTauTau_M-125_TuneCP5_13TeV-amcatnloFXFX-pythia8", 
              "GluGlujjHToTauTau_M-125_TuneCP5_13TeV-amcatnloFXFX-pythia8",
              "bbHToTauTau_M-125_4FS_ybyt_TuneCP5-13TeV-amcatnlo-pythia8",
              "jjHToTauTau_M-125_4FS_ybyt_TuneCP5-13TeV-amcatnlo-pythia8",
              "VBFHToTauTau_M125_TuneCP5_13TeV-powheg-pythia8",
              "ttHToTauTau_M125_TuneCP5_13TeV-powheg-pythia8",
              "ZHToTauTau_M125_CP5_13TeV-powheg-pythia8_ext1",
              "WplusHToTauTau_M125_TuneCP5_13TeV-powheg-pythia8",
              "WminusHToTauTau_M125_TuneCP5_13TeV-powheg-pythia8",
              "WWTo2L2Nu_TuneCP5_13TeV-powheg-pythia8",
              "WWTo1L1Nu2Q_4f_TuneCP5_13TeV-amcatnloFXFX-pythia8",
              "WWTo4Q_4f_TuneCP5_13TeV-amcatnloFXFX-pythia8",
              "WZTo3LNu_TuneCP5_13TeV-amcatnloFXFX-pythia8",
              "WZTo2Q2L_mllmin4p0_TuneCP5_13TeV-amcatnloFXFX-pythia8",
              "WZTo1L3Nu_4f_TuneCP5_13TeV-amcatnloFXFX-pythia8",
              "WZTo1L1Nu2Q_4f_TuneCP5_13TeV-amcatnloFXFX-pythia8",
              "ZZTo4L_TuneCP5_13TeV_powheg_pythia8",
              "ZZTo2Q2L_mllmin4p0_TuneCP5_13TeV-amcatnloFXFX-pythia8",
              "ZZTo2Nu2Q_5f_TuneCP5_13TeV-amcatnloFXFX-pythia8",
              "ZZTo2L2Nu_TuneCP5_13TeV_powheg_pythia8",
              #"DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8",
              "DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8",
              "DYJetsToLL_0J_TuneCP5_13TeV-amcatnloFXFX-pythia8",
              "DYJetsToLL_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8",
              "DYJetsToLL_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8",
              "WJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-pythia8",
              "WJetsToLNu_0J_TuneCP5_13TeV-amcatnloFXFX-pythia8",
              "WJetsToLNu_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8",
              "WJetsToLNu_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8",
                ],
              'UL2016':
              ["TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8",
              "TTToHadronic_TuneCP5_13TeV-powheg-pythia8",
              "TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8",
              "ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8",
              "ST_t-channel_top_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8",
              "ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-amcatnlo-pythia8",
              "ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8",
              "ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8",
              "bbHToTauTau_M-125_4FS_TuneCP5_yb2_13TeV-amcatnlo-pythia8",
              "bbHToTauTau_M-125_4FS_TuneCP5_yt2_13TeV-amcatnlo-pythia8",
              "jjHToTauTau_M-125_4FS_TuneCP5_yb2_13TeV-amcatnlo-pythia8",
              "jjHToTauTau_M-125_4FS_TuneCP5_yt2_13TeV-amcatnlo-pythia8",
              "GluGluHToTauTau_M-125_TuneCP5_13TeV-amcatnloFXFX-pythia8", 
              "GluGlujjHToTauTau_M-125_TuneCP5_13TeV-amcatnloFXFX-pythia8",
              "bbHToTauTau_M-125_4FS_ybyt_TuneCP5-13TeV-amcatnlo-pythia8",
              "jjHToTauTau_M-125_4FS_ybyt_TuneCP5-13TeV-amcatnlo-pythia8",
              "VBFHToTauTau_M125_TuneCP5_13TeV-powheg-pythia8",
              "ttHToTauTau_M125_TuneCP5_13TeV-powheg-pythia8",
              "ZHToTauTau_M125_CP5_13TeV-powheg-pythia8_ext1",
              "WplusHToTauTau_M125_TuneCP5_13TeV-powheg-pythia8",
              "WminusHToTauTau_M125_TuneCP5_13TeV-powheg-pythia8",
              "WWTo2L2Nu_TuneCP5_13TeV-powheg-pythia8",
              "WWTo1L1Nu2Q_4f_TuneCP5_13TeV-amcatnloFXFX-pythia8",
              "WWTo4Q_4f_TuneCP5_13TeV-amcatnloFXFX-pythia8",
              "WZTo3LNu_TuneCP5_13TeV-amcatnloFXFX-pythia8",
              "WZTo2Q2L_mllmin4p0_TuneCP5_13TeV-amcatnloFXFX-pythia8",
              "WZTo1L3Nu_4f_TuneCP5_13TeV-amcatnloFXFX-pythia8",
              "WZTo1L1Nu2Q_4f_TuneCP5_13TeV-amcatnloFXFX-pythia8",
              "ZZTo4L_TuneCP5_13TeV_powheg_pythia8",
              "ZZTo2Q2L_mllmin4p0_TuneCP5_13TeV-amcatnloFXFX-pythia8",
              "ZZTo2Nu2Q_5f_TuneCP5_13TeV-amcatnloFXFX-pythia8",
              "ZZTo2L2Nu_TuneCP5_13TeV_powheg_pythia8",
              "DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8",
              "DYJetsToLL_0J_TuneCP5_13TeV-amcatnloFXFX-pythia8",
              "DYJetsToLL_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8",
              "DYJetsToLL_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8",
              "WJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-pythia8",
              "WJetsToLNu_0J_TuneCP5_13TeV-amcatnloFXFX-pythia8",
              "WJetsToLNu_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8",
              "WJetsToLNu_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8",
              ],
              'UL2016_preVFP':
              ["TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8",
              "TTToHadronic_TuneCP5_13TeV-powheg-pythia8",
              "TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8",
              "ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8",
              "ST_t-channel_top_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8",
              "ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-amcatnlo-pythia8",
              "ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8",
              "ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8",
              "bbHToTauTau_M-125_4FS_TuneCP5_yb2_13TeV-amcatnlo-pythia8",
              "bbHToTauTau_M-125_4FS_TuneCP5_yt2_13TeV-amcatnlo-pythia8",
              "jjHToTauTau_M-125_4FS_TuneCP5_yb2_13TeV-amcatnlo-pythia8",
              "jjHToTauTau_M-125_4FS_TuneCP5_yt2_13TeV-amcatnlo-pythia8",
              "GluGluHToTauTau_M-125_TuneCP5_13TeV-amcatnloFXFX-pythia8", 
              "GluGlujjHToTauTau_M-125_TuneCP5_13TeV-amcatnloFXFX-pythia8",
              "bbHToTauTau_M-125_4FS_ybyt_TuneCP5-13TeV-amcatnlo-pythia8",
              "jjHToTauTau_M-125_4FS_ybyt_TuneCP5-13TeV-amcatnlo-pythia8",
              "VBFHToTauTau_M125_TuneCP5_13TeV-powheg-pythia8",
              "ttHToTauTau_M125_TuneCP5_13TeV-powheg-pythia8",
              "ZHToTauTau_M125_CP5_13TeV-powheg-pythia8_ext1",
              "WplusHToTauTau_M125_TuneCP5_13TeV-powheg-pythia8",
              "WminusHToTauTau_M125_TuneCP5_13TeV-powheg-pythia8",
              "WWTo2L2Nu_TuneCP5_13TeV-powheg-pythia8",
              "WWTo1L1Nu2Q_4f_TuneCP5_13TeV-amcatnloFXFX-pythia8",
              "WWTo4Q_4f_TuneCP5_13TeV-amcatnloFXFX-pythia8",
              "WZTo3LNu_TuneCP5_13TeV-amcatnloFXFX-pythia8",
              "WZTo2Q2L_mllmin4p0_TuneCP5_13TeV-amcatnloFXFX-pythia8",
              "WZTo1L3Nu_4f_TuneCP5_13TeV-amcatnloFXFX-pythia8",
              "WZTo1L1Nu2Q_4f_TuneCP5_13TeV-amcatnloFXFX-pythia8",
              "ZZTo4L_TuneCP5_13TeV_powheg_pythia8",
              "ZZTo2Q2L_mllmin4p0_TuneCP5_13TeV-amcatnloFXFX-pythia8",
              "ZZTo2Nu2Q_5f_TuneCP5_13TeV-amcatnloFXFX-pythia8",
              "ZZTo2L2Nu_TuneCP5_13TeV_powheg_pythia8",
              "DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8",
              "DYJetsToLL_0J_TuneCP5_13TeV-amcatnloFXFX-pythia8",
              "DYJetsToLL_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8",
              "DYJetsToLL_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8",
              "WJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-pythia8",
              "WJetsToLNu_0J_TuneCP5_13TeV-amcatnloFXFX-pythia8",
              "WJetsToLNu_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8",
              "WJetsToLNu_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8",
              ],
}


pre_path = '/pnfs/psi.ch/cms/trivcat/store/user/pbaertsc/bbh/samples_skim'

if JECvar=="yes":
    outputdir = "sampleslist/%s_skimJEC"%year
elif tes=="yes":
    outputdir = "sampleslist/%s_skimTES"%year

for sample in samplelist[year]:
    files = []
    if JECvar=="yes":
        path = "%s/%s_JEC/%s"%(pre_path,year,sample)
    elif tes=="yes":
        path = "%s/%s_TES/%s"%(pre_path,year,sample)
    if os.path.isdir(path)==False:
        print(sample,"doesn't exist")
        continue
    for root, dirs, fs in os.walk(path):
        for f in fs:
            if '.root' in f:
                #print(pre_path+ os.path.join(root,f))
                files.append(os.path.join(root,f))
    with open(os.path.join(outputdir,sample)+".txt",'w') as out:
        for f in files:
            out.write("{}\n".format(f))

print("done")
        
