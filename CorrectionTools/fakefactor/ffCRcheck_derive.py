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

outfile = ROOT.TFile('root/ffuncertainties_%s_%s.root'%(channel,year), 'RECREATE')

paths = ["Tau1_pt"]
selections_prong = ['1prong', '3prong']

var_labels={
  "Tau1_pt":"Tau p_{T} (GeV)",
}

binning_all = {
  "Tau1_pt":np.array([30.,40.,50.,60.,70.,80.,100.,130.])}

for path in paths:
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

  if path =="Tau1_pt":
    if channel=="mutau":
      binning_qcd = np.array([30.,40.,50.,60.,70.,80.,130.])
    elif channel=="etau":
      binning_qcd = np.array([30.,40.,50.,130.])
  nBins = len(binning)-1
  nBins_qcd = len(binning_qcd)-1


  for prong in selections_prong:
    ff_qcd = TH1D("ff_qcd_%s"%prong,"ff CR QCD %s"%prong,nBins_qcd,binning_qcd)
    ff_qcd.Divide(hists["CR_QCD_%s"%prong],hists["CR_QCD_AR_%s"%prong])
    ff_qcd.GetXaxis().SetTitle("%s"%var_label)
    ff_qcd.GetYaxis().SetTitle("ff closure")
    ff_w = TH1D("ff_w_%s"%prong,"ff CR W %s"%prong,nBins,binning)
    ff_w.Divide(hists["CR_W_%s"%prong],hists["CR_W_AR_%s"%prong])
    ff_w.GetXaxis().SetTitle("%s"%var_label)
    ff_w.GetYaxis().SetTitle("ff closure")
    ff_tt = TH1D("ff_tt_%s"%prong,"ff CR tt %s"%prong,nBins,binning)
    ff_tt.Divide(hists["TT_CR_TT_%s_fakes"%prong],hists["TT_CR_TT_AR_%s_fakes"%prong])
    ff_tt.GetXaxis().SetTitle("%s"%var_label)
    ff_tt.GetYaxis().SetTitle("ff closure")
    
    ff_qcd.Write()
    ff_w.Write()
    ff_tt.Write()
    # FF QCD
    canv1 = TCanvas("ff_qcd_%s%s"%(path,prong),"ff_qcd_%s_%s"%(path,prong),600,400)
    gStyle.SetOptStat(0)
    ff_qcd.SetMarkerStyle(8)
    ff_qcd.SetLineColor(1)
    #ff_qcd.GetYaxis().SetRangeUser(0.5,1.5)
    ff_qcd.GetYaxis().SetRangeUser(0.,2.)
    ff_qcd.Draw("PE")
    plot.DrawCMSLogo(canv1, "Private work", "(CMS data/simulation)", 10, 0.045, 0.05, 1.0, '', 0.8)
    latex = TLatex()
    latex.SetNDC()
    latex.SetTextFont(42)
    latex.DrawLatex(0.6, 0.8,"%s  %s"%(channel, year))
    canv1.SaveAs("plots/%s_%s/ffCRcheck/ffCRcheck_qcd_%s_%s.pdf"%(channel,year,path,prong))
    canv1.SaveAs("plots/%s_%s/ffCRcheck/ffCRcheck_qcd_%s_%s.png"%(channel,year,path,prong))
    # FF W
    canv4 = TCanvas("ff_w_%s%s"%(path,prong),"ff_w_%s_%s"%(path,prong),600,400)
    gStyle.SetOptStat(0)
    ff_w.SetMarkerStyle(8)
    ff_w.SetLineColor(1)
    #ff_w.GetYaxis().SetRangeUser(0.5,1.5)
    ff_w.GetYaxis().SetRangeUser(0.,2.)
    ff_w.Draw("PE")
    plot.DrawCMSLogo(canv4, "Private work", "(CMS data/simulation)", 10, 0.045, 0.05, 1.0, '', 0.8)
    latex = TLatex()
    latex.SetNDC()
    latex.SetTextFont(42)
    latex.DrawLatex(0.6, 0.8,"%s  %s"%(channel, year))
    canv4.SaveAs("plots/%s_%s/ffCRcheck/ffCRcheck_w_%s_%s.pdf"%(channel,year,path,prong))
    canv4.SaveAs("plots/%s_%s/ffCRcheck/ffCRcheck_w_%s_%s.png"%(channel,year,path,prong))
    # FF TT
    canv7 = TCanvas("ff_tt%s%s"%(path,prong),"ff_tt_%s_%s"%(path,prong),600,400)
    gStyle.SetOptStat(0)
    ff_tt.SetMarkerStyle(8)
    ff_tt.SetLineColor(1)
    #ff_tt.GetYaxis().SetRangeUser(0.5,1.5)
    ff_tt.GetYaxis().SetRangeUser(0.0,2.)
    ff_tt.Draw("PE")
    plot.DrawCMSLogo(canv7, "Private work", "(CMS data/simulation)", 10, 0.045, 0.05, 1.0, '', 0.8)
    latex = TLatex()
    latex.SetNDC()
    latex.SetTextFont(42)
    latex.DrawLatex(0.6, 0.8,"%s  %s"%(channel, year))
    canv7.SaveAs("plots/%s_%s/ffCRcheck/ffCRcheck_tt_%s_%s.pdf"%(channel,year,path,prong))
    canv7.SaveAs("plots/%s_%s/ffCRcheck/ffCRcheck_tt_%s_%s.png"%(channel,year,path,prong))

    # FF QCD
    canv8 = TCanvas("CR_qcd_%s%s"%(path,prong),"CR_qcd_%s_%s"%(path,prong),600,400)
    gStyle.SetOptStat(0)
    stackhist = THStack("stack","CR QCD %s %s %s;%s;data-MC(rest)"%(prong,channel,year,var_label))
    hist_CR = hists["CR_QCD_%s"%prong]
    hist_CR.SetLineColor(4)
    hist_CR.SetFillColor(4)
    hist_CR.GetXaxis().SetTitle(var_label)
    hist_CR_AR = hists["CR_QCD_AR_%s"%prong]
    hist_CR_AR.SetLineColor(880)
    hist_CR_AR.SetFillColor(880)
    stackhist.Add(hist_CR,"HIST")
    stackhist.Add(hist_CR_AR,"HIST")
    plot.DrawCMSLogo(canv8, "Private work", "(CMS data/simulation)", 10, 0.045, 0.05, 1.0, '', 0.8)
    leg = TLegend(0.65,0.75,0.85,0.85)
    leg.SetBorderSize(0)
    leg.AddEntry(hist_CR,"DR")
    leg.AddEntry(hist_CR_AR,"AR")
    stackhist.Draw()
    leg.Draw()
    canv8.SaveAs("plots/%s_%s/CRcheck/CRcheck_qcd_%s_%s.pdf"%(channel,year,path,prong))
    canv8.SaveAs("plots/%s_%s/CRcheck/CRcheck_qcd_%s_%s.png"%(channel,year,path,prong))
    # FF W
    canv9 = TCanvas("CR_w_%s%s"%(path,prong),"CR_w_%s_%s"%(path,prong),600,400)
    gStyle.SetOptStat(0)
    stackhist = THStack("stack","CR W %s %s %s;%s;data-MC(rest)"%(prong,channel,year,var_label))
    hist_CR = hists["CR_W_%s"%prong]
    hist_CR.SetLineColor(4)
    hist_CR.SetFillColor(4)
    hist_CR.GetXaxis().SetTitle(var_label)
    hist_CR_AR = hists["CR_W_AR_%s"%prong]
    hist_CR_AR.SetLineColor(880)
    hist_CR_AR.SetFillColor(880)
    stackhist.Add(hist_CR,"HIST")
    stackhist.Add(hist_CR_AR,"HIST")
    plot.DrawCMSLogo(canv9, "Private work", "(CMS data/simulation)", 10, 0.045, 0.05, 1.0, '', 0.8)
    leg = TLegend(0.65,0.75,0.85,0.85)
    leg.SetBorderSize(0)
    leg.AddEntry(hist_CR,"CR")
    leg.AddEntry(hist_CR_AR,"AR")
    stackhist.Draw()
    leg.Draw()
    canv9.SaveAs("plots/%s_%s/CRcheck/CRcheck_w_%s_%s.pdf"%(channel,year,path,prong))
    canv9.SaveAs("plots/%s_%s/CRcheck/CRcheck_w_%s_%s.png"%(channel,year,path,prong))
    # FF TT
    canv10 = TCanvas("CR_tt_%s%s"%(path,prong),"CR_tt_%s_%s"%(path,prong),600,400)
    gStyle.SetOptStat(0)
    stackhist = THStack("stack","CR TT %s %s %s;%s;data-MC(rest)"%(prong,channel,year,var_label))
    hist_CR = hists["CR_TT_%s"%prong]
    hist_CR.SetLineColor(4)
    hist_CR.SetFillColor(4)
    hist_CR.GetXaxis().SetTitle(var_label)
    hist_CR_AR = hists["CR_TT_AR_%s"%prong]
    hist_CR_AR.SetLineColor(880)
    hist_CR_AR.SetFillColor(880)
    stackhist.Add(hist_CR,"HIST")
    stackhist.Add(hist_CR_AR,"HIST")
    plot.DrawCMSLogo(canv10, "Private work", "(CMS data/simulation)", 10, 0.045, 0.05, 1.0, '', 0.8)
    leg = TLegend(0.65,0.75,0.85,0.85)
    leg.SetBorderSize(0)
    leg.AddEntry(hist_CR,"CR")
    leg.AddEntry(hist_CR_AR,"AR")
    stackhist.Draw()
    leg.Draw()
    canv10.SaveAs("plots/%s_%s/CRcheck/CRcheck_tt_%s_%s.pdf"%(channel,year,path,prong))
    canv10.SaveAs("plots/%s_%s/CRcheck/CRcheck_tt_%s_%s.png"%(channel,year,path,prong))

outfile.Close()
print("Done")
