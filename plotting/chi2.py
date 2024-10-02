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


def chisquared(path):
  hists={}
  subnode = node[path]
  for opath,objname, obj in subnode.ListObjects(depth=0):
    hists[objname] = obj
  chi2 = hists["data_obs"].Chi2Test(hists["MC"],"UW")
  print "var:",path," chi2:",chi2



if __name__=="__main__":
  var_list = ["Jet1_btag","Jet1_pt","MET","vis_mass","Dzeta","Jet2_btag","H_pt","vistauJ_mass","DRHJ","TauJ_mass","HJ_pt","DEta","Jet2_pt","dijet_pt","transverse_mass_total","DRHJ2","Jet3_pt","dijet_mass","DPhiLepMET","DPhi","DEtaTauJ2","vis_pt","DEtaLepJ","collinear_mass","vistau1_pt","vistau1_eta"]

  for var in var_list:
    chisquared(var)
