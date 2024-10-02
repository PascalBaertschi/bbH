import plotting as plot
from analysis import *
import ROOT
import argparse
import json
import os
import fnmatch
from ROOT import RooStats
from copy import deepcopy
from array import array
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('--input', '-i', help='File with histograms to plot')
parser.add_argument('--output', '-o', default='./plots', help='top level output directory')
args = parser.parse_args()

filename = args.input
file = ROOT.TFile("./root/"+filename)

node = TDirToNode(file)

made_dirs = set()


#path = "H_mass"
#path = "BDTisSignal"
path = "BDToutput"

subnode = node[path]
split_path = path.split('/')[:-1]
name = path.split('/')[-1]
target_dir = os.path.join(args.output, *split_path)
if target_dir not in made_dirs:
  os.system('mkdir -p %s' % target_dir)
  made_dirs.add(target_dir)


significance = 0
hists = {}
for opath,objname, obj in subnode.ListObjects(depth=0):
  hists[objname] = obj


for bin in range(hists["MC"].GetNbinsX()):
  if hists["bbHtautau"].GetBinContent(bin)>0 and hists["MC"].GetBinContent(bin)>0:
    significance += RooStats.AsimovSignificance(hists["bbHtautau"].GetBinContent(bin),hists["MC"].GetBinContent(bin))**2

max_bin = hists["MC"].GetNbinsX()
significance = np.sqrt(significance)
significance_total = RooStats.AsimovSignificance(hists["bbHtautau"].Integral(),hists["MC"].Integral())

print("significance for",path,":",significance)
print("total significance for",path,":",significance_total)

