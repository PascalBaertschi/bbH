import plotting as plot
from analysis import *
import ROOT
import argparse
import json
import os
import sys
import fnmatch
from copy import deepcopy
from array import array
import numpy as np
from ROOT import gStyle,TCanvas,TH1D,TH2D, TLatex
sys.path.insert(1, os.path.join(sys.path[0], '../..')) #to get file in parent directory
from CorrectionTools.MCCorrection import *
from samplenames import getsamples
ROOT.gROOT.SetBatch(ROOT.kTRUE)

parser = argparse.ArgumentParser()
parser.add_argument('--input', '-i', help='File with histograms to plot')
parser.add_argument('--output', '-o', default='./plots', help='top level output directory')
args = parser.parse_args()

filename = args.input
file = ROOT.TFile("root/"+filename)

node = TDirToNode(file)

made_dirs = set()
year = filename.split("_")[1].split(".")[0]
preVFP = ""
if "2016" in filename:
  preVFP = "_comb"
channel=filename.split("_")[0]
if year=="UL2018":
  lumi = 59.7
elif year=="UL2017":
  lumi = 41.5
elif year=="UL2016":
  lumi = 36.3
if channel=="mumu":
  channel_text = "#mu#mu"
elif channel=="tt":
  channel_text = "e#mu"
elif channel=="mutau":
  channel_text = "#mu#tau_{h}"
elif channel=="etau":
  channel_text = "e#tau_{h}"
titleright = "%s %.1f fb^{-1} (13 TeV)"%(year,float(lumi))

hists = {}
outfilename = "./txtfiles/btagSFcorr_%s_%s.txt"%(channel,year)
outfile = open(outfilename,"w")

for path, subnode in node.ListNodes(withObjects=True):
  if path not in ["Jet1_pt"]:
    continue
  split_path = path.split('/')[:-1]
  name = path.split('/')[-1]
  for opath,objname, obj in subnode.ListObjects(depth=0):
    if path=="Jet1_pt":
      hists[objname] = obj
      

for sample in getsamples(channel,year[2:],preVFP):
  norm_btagSF = hists["%s_btagSF"%sample].Integral()
  norm_nobtagSF = hists["%s_nobtagSF"%sample].Integral()
  if norm_btagSF!=0.:
    norm_ratio = norm_nobtagSF/norm_btagSF  #before applying btag SF/after applying btag SF
  else:
    norm_ratio = 1.
  outfile.write("'%s' : %f,\n"%(getsamples(channel,year[2:],preVFP)[sample],norm_ratio))
  """
  norm_ratio_text = "norm corr: %s"%round(norm_ratio,5)
  canv = TCanvas("%s_btagSFcorr"%sample,"%s btag SF norm corr"%sample,600,400)
  gStyle.SetOptStat(0)
  btagSFcorr = TH1D("%s_btagSFcorr"%sample,"%s btag SF corr"%sample,40,0.,200.)
  btagSFcorr.Divide(hists["%s_nobtagSF"%sample],hists["%s_btagSF"%sample])
  btagSFcorr.GetXaxis().SetTitle("leading jet pt (GeV)")
  btagSFcorr.GetYaxis().SetTitle("no btag SF/btag SF")
  btagSFcorr.GetYaxis().SetRangeUser(0.9,1.1)
  btagSFcorr.Draw()
  plot.DrawCMSLogo(canv, "CMS", "Internal", 10, 0.045, 0.05, 1.0, '', 0.8)
  plot.DrawTitle(canv, titleright, 3, 0.2, 0.4)
  latex = TLatex()
  latex.SetNDC()
  latex.SetTextFont(42)
  latex.DrawLatex(0.15, 0.68, channel_text)
  latex.DrawLatex(0.6,0.75,norm_ratio_text)
  canv.SaveAs("plots/btagSFcorr/%s_%s/%s_btagSFcorr.pdf"%(channel,year,sample))
  canv.SaveAs("plots/btagSFcorr/%s_%s/%s_btagSFcorr.png"%(channel,year,sample))
  """
outfile.close()


    
print("Done")
