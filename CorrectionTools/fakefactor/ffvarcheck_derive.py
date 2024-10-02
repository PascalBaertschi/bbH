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
from ROOT import gStyle,TCanvas,TH1D, TLatex, THStack, TLegend
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

outfile = ROOT.TFile('root/ffvarcorrection_%s_%s.root'%(channel,year), 'RECREATE')

#paths = ["Tau1_pt","H_mass","Jet1_pt","collinear_mass","TauJ_mass","Jet1_btag","Dzeta","Mu1_pt","H_pt","MET"]
paths = ["Tau1_pt","H_mass","Jet1_pt","collinear_mass","TauJ_mass"]

if year == 'UL2018':
  lumi = 59.7
elif year == 'UL2017':
  lumi = 41.5
elif year == 'UL2016':
  lumi = 36.3


selections_prong = ['1prong', '3prong']

var_labels={
  "Tau1_pt":"#tau_{h} p_{T} (GeV)",
  "vis_mass":"m_{vis} (GeV)",
  "transverse_mass_total":"m_{T} (GeV)",
  "mt":"m_{T} (GeV)",
  "TauJ_mass": "#tau_{h}+leading jet mass (GeV)",
  "vistauJ_mass":"vistauJ m (GeV)",
  "vis_pt":"visible p_{T} (GeV)",
  "MET":"MET (GeV)",
  "Dzeta":"Dzeta",
  "DPhi":"#Delta #phi",
  "DEta":"#Delta #eta",
  "H_pt":"Higgs p_{T} (GeV)",
  "H_mass":"m_{H} (GeV)",
  "collinear_mass":"collinear mass (GeV)",
  "Jet1_pt":"leading jet p_{T} (GeV)",
  "Jet1_btag":"Jet1 btag",
  "Jet2_pt":"Jet2 p_{T} (GeV)",
  "Jet2_btag":"Jet2 btag",
  "Jet3_pt":"Jet3 p_{T} (GeV)",
  "HJ_pt":"HJ p_{T} (GeV)",
  "DRHJ":"#Delta R(H,J)",
  "DEtaLepJ":"#Delta #eta(Lep,J)",
  "DPhiLepMET":"#Delta #phi(Lep,MET)",
  "Bjets_pt":"Bjets p_{T} (GeV)",
  "DEtaTauJ":"#Delta #eta(Tau,J)",
  "Mu1_pt":"#mu p_{T} (GeV)",
  "Ele1_pt":"e p_{T} (GeV)",
}

binning_all = {
  "Tau1_pt":np.array([30.,40.,50.,60.,70.,80.,100.,130.]),
  "vis_mass":np.array([0.,40.,80.,120.,160.,200.,250.,300.]),
  "transverse_mass_total":np.array([0.,40.,80.,120.,160.,200.,250.,300.]),
  "mt":np.array([0.,40.,80.,120.,160.,200.,250.,300.]),
  "collinear_mass":np.array([0.,40.,80.,120.,160.,200.,250.,300.]),
  "TauJ_mass":np.array([0.,40.,80.,120.,160.,200.,250.,300.]),
  "vistauJ_mass":np.array([0.,40.,80.,120.,160.,200.,250.,300.]),
  "vis_pt":np.array([0.,40.,80.,120.,160.,200.,250.,300.]),
  "MET":np.array([0.,20.,40.,60.,80.,110.,150.,200.]),
  "Dzeta":np.array([-100.,-70.,-30.,0.,30.,70.,100.]),
  "DPhi":np.array([-3.,-2.,-1.,0.,1.,2.,3.]),
  "DEta":np.array([0.,0.5,1.,1.5,2.,2.5,3.]),
  "H_pt":np.array([0.,40.,80.,120.,160.,200.,250.,300.]),
  "H_mass":np.array([0.,40.,80.,120.,160.,200.,250.,300.]),
  "Jet1_pt":np.array([20.,40.,60.,80.,110.,140.,200.]),
  "Jet1_btag":np.array([0.2,0.5,0.8,0.9,1.]),
  "Jet2_pt":np.array([20.,40.,60.,80.,110.,150.]),
  "Jet2_btag":np.array([0.,0.1,0.2,0.5,0.8,0.9,1.]),
  "Jet3_pt":np.array([0.,40.,80.,120.,160.,200.,250.,300.]),
  "HJ_pt":np.array([0.,40.,80.,120.,160.,200.]),
  "DRHJ":np.array([0.,1.,2.,3.,4.,5.]),
  "DEtaLepJ":np.array([0.,0.5,1.,1.5,2.,2.5,3.]),
  "DPhiLepMET":np.array([0.,0.5,1.,1.5,2.,2.5,3.]),
  "Bjets_pt":np.array([0.,40.,80.,120.,160.,200.]),
  "DEtaTauJ":np.array([0.,0.5,1.,1.5,2.,2.5,3.]),
  "Mu1_pt":np.array([30.,40.,50.,60.,70.,80.,100.,130.]),
  "Ele1_pt":np.array([30.,40.,50.,60.,70.,80.,100.,130.]),}

for path in paths:
  print("path:",path)
  subnode = node[path]
  split_path = path.split('/')[:-1]
  name = path.split('/')[-1]
  target_dir = os.path.join(args.output, *split_path)
  if target_dir not in made_dirs:
    os.system('mkdir -p %s' % target_dir)
    made_dirs.add(target_dir)

  var_label=var_labels[path]
  hists = {}
  for opath,objname, obj in subnode.ListObjects(depth=0):
    hists[objname] = obj

  binning = binning_all[path]
  binning_qcd = binning_all[path]
  if path =="Tau1_pt":
    if channel=="mutau":
      binning_qcd = np.array([30.,40.,50.,60.,70.,80.,130.])
    elif channel=="etau":
      binning_qcd = np.array([30.,40.,50.,130.])
  elif path =="H_mass":
    if channel=="mutau":
      binning_qcd = np.array([0.,80.,120.,160.,200.,300.])
    elif channel=="etau":
      binning_qcd = np.array([0.,120.,300.])
  elif path =="Jet1_pt":
    if channel=="mutau":
      binning_qcd = np.array([20.,40.,60.,80.,200.])
    elif channel=="etau":
      binning_qcd = np.array([20.,50.,200.])
  elif path =="collinear_mass":
    if channel=="mutau":
      binning_qcd = np.array([0.,120.,160.,200.,250.,300.])
    elif channel=="etau":
      binning_qcd = np.array([0.,120.,200.,300.])
  elif path =="TauJ_mass":
    if channel=="mutau":
      binning_qcd = np.array([0.,80.,120.,160.,200.,300.])
    elif channel=="etau":
      binning_qcd = np.array([0.,120.,300.])
  nBins = len(binning)-1
  nBins_qcd = len(binning_qcd)-1

  for prong in selections_prong:
    if channel == "mutau":
      channel_text = "#mu#tau_{h}, %s"%prong
    elif channel == "etau":
      channel_text = "e#tau_{h}, %s"%prong

    ff_qcd = TH1D("ff_qcd_%s_%s"%(prong,path),"",nBins_qcd,binning_qcd)
    ff_qcd.Divide(hists["DR_QCD_%s"%prong],hists["DR_QCD_AR_%s"%prong])
    ff_qcd.GetXaxis().SetTitle("%s"%var_label)
    ff_qcd.GetYaxis().SetTitle("fake factor closure")
    ff_qcd.GetXaxis().SetTitleSize(0.05)
    ff_qcd.GetYaxis().SetTitleSize(0.05)
    ff_qcd.GetYaxis().SetTitleOffset(0.92)
    ff_qcd.GetXaxis().SetLabelSize(0.05)
    ff_qcd.GetYaxis().SetLabelSize(0.05)
    ff_w = TH1D("ff_w_%s_%s"%(prong,path),"",nBins,binning)
    ff_w.Divide(hists["DR_W_%s"%prong],hists["DR_W_AR_%s"%prong])
    ff_w.GetXaxis().SetTitle("%s"%var_label)
    ff_w.GetYaxis().SetTitle("fake factor closure")
    ff_w.GetXaxis().SetTitleSize(0.05)
    ff_w.GetYaxis().SetTitleSize(0.05)
    ff_w.GetYaxis().SetTitleOffset(0.92)
    ff_w.GetXaxis().SetLabelSize(0.05)
    ff_w.GetYaxis().SetLabelSize(0.05)
    ff_tt = TH1D("ff_tt_%s_%s"%(prong,path),"",nBins,binning)
    #ff_tt.Divide(hists["DR_TT_%s"%prong],hists["DR_TT_AR_%s"%prong])
    ff_tt.Divide(hists["TT_DR_TT_%s_fakes"%prong],hists["TT_DR_TT_AR_%s_fakes"%prong])
    ff_tt.GetXaxis().SetTitle("%s"%var_label)
    ff_tt.GetYaxis().SetTitle("fake factor closure")
    ff_tt.GetXaxis().SetTitleSize(0.05)
    ff_tt.GetYaxis().SetTitleSize(0.05)
    ff_tt.GetYaxis().SetTitleOffset(0.92)
    ff_tt.GetXaxis().SetLabelSize(0.05)
    ff_tt.GetYaxis().SetLabelSize(0.05)
    ff_qcd.Write()
    ff_w.Write()
    ff_tt.Write()
    # FF QCD
    canv1 = TCanvas("ff_qcd_%s%s"%(path,prong),"ff_qcd_%s_%s"%(path,prong),600,400)
    canv1.SetBottomMargin(0.12)
    gStyle.SetOptStat(0)
    ff_qcd.SetMarkerStyle(8)
    ff_qcd.SetLineColor(1)
    #ff_qcd.GetYaxis().SetRangeUser(0.5,1.5)
    ff_qcd.GetYaxis().SetRangeUser(0.,3.)
    ff_qcd.Draw("PE")
    plot.DrawCMSLogo(canv1, "Private work", "(CMS data/simulation)", 10, 0.045, 0.05, 1.0, '', 0.8)
    latex = TLatex()
    latex.SetNDC()
    latex.SetTextFont(42)
    latex.DrawLatex(0.15, 0.68,channel_text+", QCD DR")
    latex.DrawLatex(0.6, 0.91, "%s %s fb^{-1} (13 TeV)"%(year[2:],lumi))
    canv1.SaveAs("plots/%s_%s/varcheck/varcheck_qcd_%s_%s.pdf"%(channel,year,path,prong))
    canv1.SaveAs("plots/%s_%s/varcheck/varcheck_qcd_%s_%s.png"%(channel,year,path,prong))
    canv1.SaveAs("plots/thesis/ff_varcheck_qcd_%s_%s_%s_%s.pdf"%(path,prong,channel,year))
    # FF W
    canv4 = TCanvas("ff_w_%s%s"%(path,prong),"ff_w_%s_%s"%(path,prong),600,400)
    canv4.SetBottomMargin(0.12)
    gStyle.SetOptStat(0)
    ff_w.SetMarkerStyle(8)
    ff_w.SetLineColor(1)
    #ff_w.GetYaxis().SetRangeUser(0.5,1.5)
    ff_w.GetYaxis().SetRangeUser(0.,3.)
    ff_w.Draw("PE")
    plot.DrawCMSLogo(canv4, "Private work", "(CMS data/simulation)", 10, 0.045, 0.05, 1.0, '', 0.8)
    latex = TLatex()
    latex.SetNDC()
    latex.SetTextFont(42)
    latex.DrawLatex(0.15, 0.68, channel_text+", W+jets DR") 
    latex.DrawLatex(0.6, 0.91, "%s %s fb^{-1} (13 TeV)"%(year[2:],lumi))
    canv4.SaveAs("plots/%s_%s/varcheck/varcheck_w_%s_%s.pdf"%(channel,year,path,prong))
    canv4.SaveAs("plots/%s_%s/varcheck/varcheck_w_%s_%s.png"%(channel,year,path,prong))
    canv4.SaveAs("plots/thesis/ff_varcheck_w_%s_%s_%s_%s.pdf"%(path,prong,channel,year))
    # FF TT
    canv7 = TCanvas("ff_tt%s%s"%(path,prong),"ff_tt_%s_%s"%(path,prong),600,400)
    canv7.SetBottomMargin(0.12)
    gStyle.SetOptStat(0)
    ff_tt.SetMarkerStyle(8)
    ff_tt.SetLineColor(1)
    #ff_tt.GetYaxis().SetRangeUser(0.5,1.5)
    ff_tt.GetYaxis().SetRangeUser(0.0,3.)
    ff_tt.Draw("PE")
    plot.DrawCMSLogo(canv7, "Private work", "(CMS data/simulation)", 10, 0.045, 0.05, 1.0, '', 0.8)
    latex = TLatex()
    latex.SetNDC()
    latex.SetTextFont(42)
    latex.DrawLatex(0.15, 0.68, channel_text+", t#bar{t} DR")            
    latex.DrawLatex(0.6, 0.91, "%s %s fb^{-1} (13 TeV)"%(year[2:],lumi))
    canv7.SaveAs("plots/%s_%s/varcheck/varcheck_tt_%s_%s.pdf"%(channel,year,path,prong))
    canv7.SaveAs("plots/%s_%s/varcheck/varcheck_tt_%s_%s.png"%(channel,year,path,prong))
    canv7.SaveAs("plots/thesis/ff_varcheck_tt_%s_%s_%s_%s.pdf"%(path,prong,channel,year))

    # FF QCD
    canv8 = TCanvas("DR_qcd_%s%s"%(path,prong),"DR_qcd_%s_%s"%(path,prong),600,400)
    canv8.SetBottomMargin(0.12)
    gStyle.SetOptStat(0)
    stackhist = THStack("stack","DR QCD %s %s %s;%s;data-MC(rest)"%(prong,channel,year,var_label))
    hist_DR = hists["DR_QCD_%s"%prong]
    hist_DR.SetLineColor(4)
    hist_DR.SetFillColor(4)
    hist_DR.GetXaxis().SetTitle(var_label)
    hist_DR_AR = hists["DR_QCD_AR_%s"%prong]
    hist_DR_AR.SetLineColor(880)
    hist_DR_AR.SetFillColor(880)
    stackhist.Add(hist_DR,"HIST")
    stackhist.Add(hist_DR_AR,"HIST")
    plot.DrawCMSLogo(canv8, "Private work", "(CMS data/simulation)", 10, 0.045, 0.05, 1.0, '', 0.8)
    leg = TLegend(0.65,0.75,0.85,0.85)
    leg.SetBorderSize(0)
    leg.AddEntry(hist_DR,"DR")
    leg.AddEntry(hist_DR_AR,"AR")
    stackhist.Draw()
    leg.Draw()
    canv8.SaveAs("plots/%s_%s/DRcheck/DRcheck_qcd_%s_%s_%s_%s.pdf"%(channel,year,path,prong,channel,year))
    canv8.SaveAs("plots/%s_%s/DRcheck/DRcheck_qcd_%s_%s_%s_%s.png"%(channel,year,path,prong,channel,year))
    # FF W
    canv9 = TCanvas("DR_w_%s%s"%(path,prong),"DR_w_%s_%s"%(path,prong),600,400)
    canv9.SetBottomMargin(0.12)
    gStyle.SetOptStat(0)
    stackhist = THStack("stack","DR W %s %s %s;%s;data-MC(rest)"%(prong,channel,year,var_label))
    hist_DR = hists["DR_W_%s"%prong]
    hist_DR.SetLineColor(4)
    hist_DR.SetFillColor(4)
    hist_DR.GetXaxis().SetTitle(var_label)
    hist_DR_AR = hists["DR_W_AR_%s"%prong]
    hist_DR_AR.SetLineColor(880)
    hist_DR_AR.SetFillColor(880)
    stackhist.Add(hist_DR,"HIST")
    stackhist.Add(hist_DR_AR,"HIST")
    plot.DrawCMSLogo(canv9, "Private work", "(CMS data/simulation)", 10, 0.045, 0.05, 1.0, '', 0.8)
    leg = TLegend(0.65,0.75,0.85,0.85)
    leg.SetBorderSize(0)
    leg.AddEntry(hist_DR,"DR")
    leg.AddEntry(hist_DR_AR,"AR")
    stackhist.Draw()
    leg.Draw()
    canv9.SaveAs("plots/%s_%s/DRcheck/DRcheck_w_%s_%s_%s_%s.pdf"%(channel,year,path,prong,channel,year))
    canv9.SaveAs("plots/%s_%s/DRcheck/DRcheck_w_%s_%s_%s_%s.png"%(channel,year,path,prong,channel,year))
    # FF TT
    canv10 = TCanvas("DR_tt_%s%s"%(path,prong),"DR_tt_%s_%s"%(path,prong),600,400)
    canv10.SetBottomMargin(0.12)
    gStyle.SetOptStat(0)
    stackhist = THStack("stack","DR TT %s %s %s;%s;data-MC(rest)"%(prong,channel,year,var_label))
    hist_DR = hists["DR_TT_%s"%prong]
    hist_DR.SetLineColor(4)
    hist_DR.SetFillColor(4)
    hist_DR.GetXaxis().SetTitle(var_label)
    hist_DR_AR = hists["DR_TT_AR_%s"%prong]
    hist_DR_AR.SetLineColor(880)
    hist_DR_AR.SetFillColor(880)
    stackhist.Add(hist_DR,"HIST")
    stackhist.Add(hist_DR_AR,"HIST")
    plot.DrawCMSLogo(canv10, "Private work", "(CMS data/simulation)", 10, 0.045, 0.05, 1.0, '', 0.8)
    latex.DrawLatex(0.15, 0.68, channel_text)
    leg = TLegend(0.65,0.75,0.85,0.85)
    leg.SetBorderSize(0)
    leg.AddEntry(hist_DR,"DR")
    leg.AddEntry(hist_DR_AR,"AR")
    stackhist.Draw()
    leg.Draw()
    canv10.SaveAs("plots/%s_%s/DRcheck/DRcheck_tt_%s_%s_%s_%s.pdf"%(channel,year,path,prong,channel,year))
    canv10.SaveAs("plots/%s_%s/DRcheck/DRcheck_tt_%s_%s_%s_%s.png"%(channel,year,path,prong,channel,year))
outfile.Close()
print("Done")
