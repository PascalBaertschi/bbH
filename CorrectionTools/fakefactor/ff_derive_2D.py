import plotting as plot
from analysis import *
import ROOT
import argparse
import json
import os
import fnmatch
from copy import deepcopy
from array import array
import numpy as np
from ROOT import gStyle,TCanvas,TH1D, TLatex, TH2D


parser = argparse.ArgumentParser()
parser.add_argument('--input', '-i', help='File with histograms to plot')
parser.add_argument('--output', '-o', default='./plots', help='top level output directory')
args = parser.parse_args()

filename = args.input
file = ROOT.TFile("root/"+filename)

node = TDirToNode(file)

made_dirs = set()
year = filename.split("_")[2].split(".")[0]
if "preVFP" in filename:
  year=year+"_preVFP"
elif "comb" in filename:
  year=year+"_comb"
channel=filename.split("_")[1]

outfile = ROOT.TFile('root/fakefactors_%s_%s_2D.root'%(channel,year), 'RECREATE')


#path = "Tau1_pt"
#path = "transverse_mass_lepmet"
path = "2D"
selections_prong = ['1prong', '3prong']

#subnode = node["Tau1_pt"]
#subnode = node["transverse_mass_lepmet"]
subnode = node["2D"]
split_path = path.split('/')[:-1]
name = path.split('/')[-1]
target_dir = os.path.join(args.output, *split_path)
if target_dir not in made_dirs:
  os.system('mkdir -p %s' % target_dir)
  made_dirs.add(target_dir)

hists = {}
for opath,objname, obj in subnode.ListObjects(depth=0):
  hists[objname] = obj

#nBins = 10
#binning = np.array([30.,40.,50.,60.,70.,80.,100.,130.])
#nBins = len(binning)-1
#remove variable bin width: replace binning with 30,130

for prong in selections_prong:
  #ff_qcd = TH2D("ff_qcd_%s"%prong,"ff DR QCD %s"%prong,7,array('d',[30,40,50,60,70,80,100,130]),6,array('d',[20,60,100,140,180,240,300]))
  ff_qcd = TH2D("ff_qcd_%s"%prong,"ff DR QCD %s"%prong,6,array('d',[30,40,50,60,75,90,130]),5,array('d',[20,60,100,140,200,300]))
  ff_qcd.Divide(hists["DR_QCD_%s"%prong],hists["DR_QCD_AR_%s"%prong])
  ff_qcd.GetXaxis().SetTitle("Tau p_{T} (GeV)")
  ff_qcd.GetYaxis().SetTitle("visible mass (GeV)")
  #ff_w = TH2D("ff_w_%s"%prong,"ff DR W %s"%prong,7,array('d',[30,40,50,60,70,80,100,130]),6,array('d',[20,60,100,140,180,240,300]))
  ff_w = TH2D("ff_w_%s"%prong,"ff DR W %s"%prong,6,array('d',[30,40,50,60,75,90,130]),5,array('d',[20,60,100,140,200,300]))
  ff_w.Divide(hists["DR_W_%s"%prong],hists["DR_W_AR_%s"%prong])
  ff_w.GetXaxis().SetTitle("Tau p_{T} (GeV)")
  ff_w.GetYaxis().SetTitle("visible mass (GeV)")
  #ff_tt = TH2D("ff_tt_%s"%prong,"ff DR tt %s"%prong,7,array('d',[30,40,50,60,70,80,100,130]),6,array('d',[20,60,100,140,180,240,300]))
  ff_tt = TH2D("ff_tt_%s"%prong,"ff DR tt %s"%prong,6,array('d',[30,40,50,60,75,90,130]),5,array('d',[20,60,100,140,200,300]))
  ff_tt.Divide(hists["DR_TT_%s"%prong],hists["DR_TT_AR_%s"%prong])
  #mean_ff_tt = ff_tt.Integral()/ff_tt.GetNbinsX()
  ff_tt.GetXaxis().SetTitle("Tau p_{T} (GeV)")
  ff_tt.GetYaxis().SetTitle("visible mass (GeV)")

  
  ff_qcd.Write()
  ff_w.Write()
  ff_tt.Write()
  # FF QCD
  
  canv1 = TCanvas("ff_qcd_%s"%prong,"ff_qcd_%s"%prong,600,400)
  gStyle.SetOptStat(0)
  ff_qcd.SetMarkerStyle(8)
  ff_qcd.SetLineColor(1)
  ff_qcd.GetYaxis().SetRangeUser(0.,1.)
  ff_qcd.Draw("PE")
  latex = TLatex()
  latex.SetNDC()
  latex.SetTextFont(42)
  latex.DrawLatex(0.6, 0.8,"%s  %s"%(channel, year))
  canv1.SaveAs("plots/%s_%s/ff_qcd_%s_2D.pdf"%(channel,year,prong))
  # FF W
  canv4 = TCanvas("ff_w_%s"%prong,"ff_w_%s"%prong,600,400)
  gStyle.SetOptStat(0)
  ff_w.SetMarkerStyle(8)
  ff_w.SetLineColor(1)
  ff_w.GetYaxis().SetRangeUser(0.,1.)
  ff_w.Draw("PE")
  latex = TLatex()
  latex.SetNDC()
  latex.SetTextFont(42)
  latex.DrawLatex(0.6, 0.8,"%s  %s"%(channel, year))
  canv4.SaveAs("plots/%s_%s/ff_w_%s_2D.pdf"%(channel,year,prong))
  # FF TT
  canv7 = TCanvas("ff_tt%s"%prong,"ff_tt_%s"%prong,600,400)
  gStyle.SetOptStat(0)
  ff_tt.SetMarkerStyle(8)
  ff_tt.SetLineColor(1)
  ff_tt.GetYaxis().SetRangeUser(0.,1.)
  ff_tt.Draw("PE")
  latex = TLatex()
  latex.SetNDC()
  latex.SetTextFont(42)
  latex.DrawLatex(0.6, 0.8,"%s  %s"%(channel, year))
  canv7.SaveAs("plots/%s_%s/ff_tt_%s_2D.pdf"%(channel,year,prong))


outfile.Close()
print("Done")
