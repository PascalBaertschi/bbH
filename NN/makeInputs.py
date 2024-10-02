import ROOT
from ROOT import TChain, TFile, TH1F, TCanvas
import numpy as np
from array import array
import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from plotting.utils import getJSON
from xsections import xsection
from argparse import ArgumentParser
from samplenames import getsamples

parser = ArgumentParser()

parser.add_argument('-y', '--year',    dest='year', type=str, default='2018', action='store')
parser.add_argument('-p', '--preVFP',  dest='preVFP', action='store_const', const="_preVFP",default="")
parser.add_argument('-t', '--comb',  dest='UL2016comb', action='store_true',default=False)
args = parser.parse_args()

year = args.year
UL2016comb = args.UL2016comb
preVFP = args.preVFP
outdir = "/work/pbaertsc/bbh/NanoTreeProducer/NN/root/"


if UL2016comb:
    preVFP="_comb"

#mc_samples = ['bbH_M80','bbH_M100','bbH_M120','bbH_M125','bbH_M130','bbH_M140','bbH_M160','bbH_M180','bbH_M200','bbH_M250','bbH_M300'] #powheg
mc_samples = ['bbH_M-80','bbH_M-90','bbH_M-100','bbH_M-110','bbH_M-120','bbH_M-125','bbH_M-130','bbH_M-140','bbH_M-160','bbH_M-180','bbH_M-200','bbH_M-250','bbH_M-300'] #amcatnlo

selection_train = '(isHtoMuTau || isHtoETau) && EventNumber%10<=7' #use Events with endnumber 0 1 2 3 4 5 6 7 for training NN
selection_test = '(isHtoMuTau || isHtoETau) && EventNumber%10>=8'  #use Events with endnumber 8 9 for testing NN





def BDTinput(sample_shortname,filetype,year,preVFP):
    filedir = "/pnfs/psi.ch/cms/trivcat/store/user/pbaertsc/bbh/samples_UL%s%s"%(year,preVFP)
    if filetype=="train":
        selection = selection_train
    else:
        selection = selection_test
    sample = getsamples("mutau","UL",year,preVFP)[sample_shortname]
    infile = TFile(filedir+"/"+sample+".root")
    intree = infile.Get("tree")
    outfile = TFile("%s%s_%s_UL%s%s.root"%(outdir,sample_shortname,filetype,year,preVFP),"RECREATE")
    skimmed_tree=intree.CopyTree(selection)
    infile.Close()
    outfile.Write()
    outfile.Close()


for sample_shortname in mc_samples:
    print "sample:",sample_shortname
    for filetype in ["train","test"]:
        BDTinput(sample_shortname,filetype,year,preVFP)

