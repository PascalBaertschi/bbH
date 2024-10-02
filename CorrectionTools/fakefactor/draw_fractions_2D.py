import os, sys
import copy, math, pickle, numpy
from array import array
import argparse
from ROOT import gROOT, gSystem, gStyle, gRandom
from ROOT import TMath, TFile, TChain, TTree, TCut, TH1F, TH2F, THStack, TGraph, TGaxis
from ROOT import TStyle, TCanvas, TPad, TLegend, TLatex, TText, TColor, TPaveText
from ROOT import TH1, TF1, TGraph, TGraphErrors, TGraphAsymmErrors, TVirtualFitter



parser = argparse.ArgumentParser()
parser.add_argument('--input', '-i', help='File with histograms to plot')
parser.add_argument('--output', '-o', default='./plots', help='top level output directory')
args = parser.parse_args()
selections_prong = ['1prong','3prong']
filename = args.input
outdir = args.output
year = filename.split("_")[2].split(".")[0]
if "preVFP" in filename:
    year=year+"_preVFP"
elif "comb" in filename:
    year=year+"_comb"
channel=filename.split("_")[1]

file = TFile("root/"+filename,"READ")
tau_pt = file.Get("Tau1_pt")
for prong in selections_prong:
    hist_data = tau_pt.Get("data_obs_AR_%s"%prong)
    data_integral = hist_data.Integral()
    hist_DY=tau_pt.Get("DYJetscomb_AR_%s"%prong)
    hist_DY.SetFillColor(600)
    hist_W=tau_pt.Get("WJetscomb_AR_%s"%prong)
    hist_W.SetFillColor(632)
    hist_TT=tau_pt.Get("TT_AR_%s"%prong)
    hist_TT.SetFillColor(416)
    hist_Multijet = tau_pt.Get("Multijet_AR_%s"%prong)
    hist_Multijet.SetFillColor(432)
    hist_true = tau_pt.Get("MC_ARtrue_%s"%prong)
    hist_true.SetFillColor(616)
    for bin in range(1,14):
        data=hist_data.GetBinContent(bin)
        if data==0:
            continue
        hist_DY.SetBinContent(bin,hist_DY.GetBinContent(bin)/data)
        hist_W.SetBinContent(bin,hist_W.GetBinContent(bin)/data)
        hist_TT.SetBinContent(bin,hist_TT.GetBinContent(bin)/data)
        hist_Multijet.SetBinContent(bin,hist_Multijet.GetBinContent(bin)/data)
        hist_true.SetBinContent(bin,hist_true.GetBinContent(bin)/data)
    hist_DY.GetYaxis().SetTitle("Fractions")
    stack = THStack()
    stack.Add(hist_W)
    stack.Add(hist_DY)
    stack.Add(hist_true)
    stack.Add(hist_Multijet)
    stack.Add(hist_TT)
    #save histograms in root file
    outfile = TFile("root/fractions_%s_%s_%s.root"%(channel,year,prong),'Recreate')
    hist_W.Write()
    hist_Multijet.Write()
    hist_DY.Write()
    hist_TT.Write()
    outfile.Close()
    canv = TCanvas(prong,prong,600,400)
    gStyle.SetOptStat(0)
    stack.Draw('HIST')
    stack.SetTitle("Fractions AR %s"%prong)
    stack.GetXaxis().SetTitle("Tau p_{T}")
    stack.GetYaxis().SetTitle("Fractions")
    leg = TLegend(0.7, 0.57, 0.8, 0.77)#0.15 0.12 0.3 0.32
    leg.AddEntry(hist_TT,"TT","F")
    leg.AddEntry(hist_Multijet,"QCD","F")
    leg.AddEntry(hist_true,"true #tau","F")
    leg.AddEntry(hist_DY,"DYJets","F")
    leg.AddEntry(hist_W,"WJets","F")
    leg.Draw("SAME")
    latex = TLatex()
    latex.SetNDC()
    latex.SetTextFont(42)
    latex.DrawLatex(0.7, 0.8,"%s  %s"%(channel, year))
    canv.SetLogx()
    canv.SaveAs(outdir+"/%s_%s/fractions_%s.pdf"%(channel,year,prong))

###save fractions for TT DR

for prong in selections_prong:
    hist_data = tau_pt.Get("data_obs_ARTT_%s"%prong)
    data_integral = hist_data.Integral()
    hist_DY=tau_pt.Get("DYJetscomb_ARTT_%s"%prong)
    hist_DY.SetFillColor(600)
    hist_W=tau_pt.Get("WJetscomb_ARTT_%s"%prong)
    hist_W.SetFillColor(632)
    hist_TT=tau_pt.Get("TT_ARTT_%s"%prong)
    hist_TT.SetFillColor(416)
    hist_Multijet = tau_pt.Get("Multijet_ARTT_%s"%prong)
    hist_Multijet.SetFillColor(432)
    hist_true = tau_pt.Get("MC_ARTTtrue_%s"%prong)
    hist_true.SetFillColor(616)
    for bin in range(1,14):
        data=hist_data.GetBinContent(bin)
        if data==0:
            continue
        hist_DY.SetBinContent(bin,hist_DY.GetBinContent(bin)/data)
        hist_W.SetBinContent(bin,hist_W.GetBinContent(bin)/data)
        hist_TT.SetBinContent(bin,hist_TT.GetBinContent(bin)/data)
        hist_Multijet.SetBinContent(bin,hist_Multijet.GetBinContent(bin)/data)
        hist_true.SetBinContent(bin,hist_true.GetBinContent(bin)/data)
    hist_DY.GetYaxis().SetTitle("Fractions")
    stack = THStack()
    stack.Add(hist_W)
    stack.Add(hist_DY)
    stack.Add(hist_true)
    stack.Add(hist_Multijet)
    stack.Add(hist_TT)
    #save histograms in root file
    outfile = TFile("root/fractions_TTDR_%s_%s_%s.root"%(channel,year,prong),'Recreate')
    hist_W.Write()
    hist_Multijet.Write()
    hist_DY.Write()
    hist_TT.Write()
    outfile.Close()
    canv = TCanvas(prong,prong,600,400)
    gStyle.SetOptStat(0)
    stack.Draw('HIST')
    stack.SetTitle("Fractions AR %s"%prong)
    stack.GetXaxis().SetTitle("Tau p_{T}")
    stack.GetYaxis().SetTitle("Fractions")
    leg = TLegend(0.15, 0.12, 0.3, 0.32)
    leg.AddEntry(hist_TT,"TT","F")
    leg.AddEntry(hist_Multijet,"QCD","F")
    leg.AddEntry(hist_true,"true #tau","F")
    leg.AddEntry(hist_DY,"DYJets","F")
    leg.AddEntry(hist_W,"WJets","F")
    leg.Draw("SAME")
    latex = TLatex()
    latex.SetNDC()
    latex.SetTextFont(42)
    latex.DrawLatex(0.6, 0.8,"%s  %s"%(channel, year))
    canv.SetLogx()
    canv.SaveAs(outdir+"/%s_%s/fractions_TTDR_%s.pdf"%(channel,year,prong))
