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
from ROOT import gStyle,TCanvas,TH1D, TLatex, TF1, TLine
ROOT.gROOT.SetBatch(ROOT.kTRUE)

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
#elif "comb" in filename:
#  year=year+"_comb"
channel=filename.split("_")[1]

selections_prong = ['1prong', '3prong']

if year=="UL2018":
  lumi = 59.7
elif year=="UL2017":
  lumi = 41.5
elif year=="2018":
  lumi = 59.7
else:
  lumi = 36.3
  """
  if "comb" in filename:
    lumi = 36.3
  elif "preVFP" in filename:
    lumi = 19.5
  else:
    lumi = 16.8
  """

titleright = "%s %.1f fb^{-1} (13 TeV)"%(year,float(lumi))

gStyle.SetOptStat(0)

for path, subnode in node.ListNodes(withObjects=True):
  split_path = path.split('/')[:-1]
  name = path.split('/')[-1]
  target_dir = os.path.join(args.output, *split_path)
  if target_dir not in made_dirs:
    os.system('mkdir -p %s' % target_dir)
    made_dirs.add(target_dir)
  hists = {}
  for opath, objname, obj in subnode.ListObjects(depth=0):
    hists[objname] = obj
    
  if path=="Tau1_pt":
    binning = np.array([30.,40.,50.,60.,70.,80.,100.,130.])
    if channel=="mutau":
      binning_qcd = np.array([30.,40.,50.,60.,70.,80.,130.])
    elif channel=="etau":
      binning_qcd = np.array([30.,40.,50.,130.])
  elif path=="H_mass":
    binning = np.array([0.,40.,80.,120.,160.,200.,250.,300.])
    if channel=="mutau":
      binning_qcd = np.array([0.,80.,120.,160.,200.,300.])
    elif channel=="etau":
      binning_qcd = np.array([0.,120.,300.])
  elif path=="Jet1_pt":
    binning = np.array([20.,40.,60.,80.,110.,140.,200.])
    if channel=="mutau":
      binning_qcd = np.array([20.,40.,60.,80.,200.])
    elif channel=="etau":
      binning_qcd = np.array([20.,50.,200.])
  elif path=="collinear_mass":
    binning = np.array([0.,40.,80.,120.,160.,200.,250.,300.])
    if channel=="mutau":
      binning_qcd = np.array([0.,120.,160.,200.,250.,300.])
    elif channel=="etau":
      binning_qcd = np.array([0.,120.,200.,300.])
  elif path=="TauJ_mass":
    binning = np.array([0.,40.,80.,120.,160.,200.,250.,300.])
    if channel=="mutau":
      binning_qcd = np.array([0.,80.,120.,160.,200.,300.])
    elif channel=="etau":
      binning_qcd = np.array([0.,120.,300.])


  nBins = len(binning)-1
  nBins_qcd = len(binning_qcd)-1

  if path=="Tau1_pt":
    xtitle = "Tau p_{T} (GeV)"
  elif path=="H_mass":
    xtitle = "H mass (GeV)"
  elif path=="Jet1_pt":
    xtitle = "leading Jet p_{T} (GeV)"
  elif path=="collinear_mass":
    xtitle = "collinear mass (GeV)"
  elif path=="TauJ_mass":
    xtitle = "#tau+jet1 mass (GeV)"

  for prong in selections_prong:
    if channel == "mutau":
      channel_text = "#mu#tau_{h}, %s"%prong
    elif channel == "etau":
      channel_text = "e#tau_{h}, %s"%prong
    ff_qcd = TH1D("ff_qcd_%s"%prong,"ff DR QCD %s"%prong,nBins_qcd,binning_qcd)
    ff_qcd.Divide(hists["DR_QCD_%s"%prong],hists["DR_QCD_AR_%s"%prong])
    ff_qcd.GetXaxis().SetTitle(xtitle)
    ff_qcd.GetYaxis().SetTitle("fakefactor")

    ff_w = TH1D("ff_w_%s"%prong,"ff DR W %s"%prong,nBins,binning)
    ff_w.Divide(hists["DR_W_%s"%prong],hists["DR_W_AR_%s"%prong])
    ff_w.GetXaxis().SetTitle(xtitle)
    ff_w.GetYaxis().SetTitle("fakefactor")

    ff_tt = TH1D("ff_tt_%s"%prong,"ff DR tt %s"%prong,nBins,binning)
    ff_tt.Divide(hists["TT_DR_TT_%s_fakes"%prong],hists["TT_DR_TT_AR_%s_fakes"%prong]) #using MC to derive fakefactor
    ff_tt.GetXaxis().SetTitle(xtitle)
    ff_tt.GetYaxis().SetTitle("fakefactor")
  
    canv1 = TCanvas("ff_qcd_%s"%prong,"ff_qcd_%s"%prong,600,400)
    ff_qcd.SetMarkerStyle(8)
    ff_qcd.SetLineColor(1)
    ff_qcd.GetYaxis().SetRangeUser(0.,0.5)
    ff_qcd.Draw("PE")
    latex = TLatex()
    latex.SetNDC()
    latex.SetTextFont(42)
    #latex.DrawLatex(0.6, 0.8,"%s  %s"%(channel, year))
    plot.DrawCMSLogo(canv1, "CMS", "Internal", 10, 0.045, 0.05, 1.0, '', 0.8)
    plot.DrawTitle(canv1, titleright, 3, 0.2, 0.4)
    plot.Set(latex, NDC=None, TextFont=42, TextSize=0.05)
    latex.DrawLatex(0.15, 0.68, channel_text)
    canv1.SaveAs("plots/%s_%s/othervars/ff_qcd_%s_%s.pdf"%(channel,year,path,prong))
    canv1.SaveAs("plots/%s_%s/othervars/ff_qcd_%s_%s.png"%(channel,year,path,prong))
    
    # FF W
    canv4 = TCanvas("ff_w_%s"%prong,"ff_w_%s"%prong,600,400)
    ff_w.SetMarkerStyle(8)
    ff_w.SetLineColor(1)
    ff_w.GetYaxis().SetRangeUser(0.,0.5)
    ff_w.Draw("PE")
    latex = TLatex()
    latex.SetNDC()
    latex.SetTextFont(42)
    #latex.DrawLatex(0.6, 0.8,"%s  %s"%(channel, year))
    plot.DrawCMSLogo(canv4, "CMS", "Internal", 10, 0.045, 0.05, 1.0, '', 0.8)
    plot.DrawTitle(canv4, titleright, 3, 0.2, 0.4)
    plot.Set(latex, NDC=None, TextFont=42, TextSize=0.05)
    latex.DrawLatex(0.15, 0.68, channel_text)
    canv4.SaveAs("plots/%s_%s/othervars/ff_w_%s_%s.pdf"%(channel,year,path,prong))
    canv4.SaveAs("plots/%s_%s/othervars/ff_w_%s_%s.png"%(channel,year,path,prong))

    # FF TT
    canv7 = TCanvas("ff_tt%s"%prong,"ff_tt_%s"%prong,600,400)
    ff_tt.SetMarkerStyle(8)
    ff_tt.SetLineColor(1)
    ff_tt.GetYaxis().SetRangeUser(0.,0.5)
    ff_tt.Draw("PE")
    latex = TLatex()
    latex.SetNDC()
    latex.SetTextFont(42)
    #latex.DrawLatex(0.6, 0.8,"%s  %s"%(channel, year))
    plot.DrawCMSLogo(canv7, "CMS", "Internal", 10, 0.045, 0.05, 1.0, '', 0.8)
    plot.DrawTitle(canv7, titleright, 3, 0.2, 0.4)
    plot.Set(latex, NDC=None, TextFont=42, TextSize=0.05)
    latex.DrawLatex(0.15, 0.68, channel_text)
    canv7.SaveAs("plots/%s_%s/othervars/ff_tt_%s_%s.pdf"%(channel,year,path,prong))
    canv7.SaveAs("plots/%s_%s/othervars/ff_tt_%s_%s.png"%(channel,year,path,prong))

print("Done")
