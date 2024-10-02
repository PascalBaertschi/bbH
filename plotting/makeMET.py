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
from ROOT import gStyle,TCanvas,TH1D,TH2D, TLatex, TLegend


parser = argparse.ArgumentParser()
parser.add_argument('--input', '-i', help='File with histograms to plot')
parser.add_argument('--output', '-o', default='./plots', help='top level output directory')
args = parser.parse_args()

filename = args.input
file = ROOT.TFile("root/"+filename)


node = TDirToNode(file)

made_dirs = set()
year = filename.split("_")[1].split(".")[0]
if "preVFP" in filename:
  year=year+"_preVFP"
elif "comb" in filename:
  year=year+"_comb"
channel=filename.split("_")[0]


hists_taupt = {}
hists_mupt = {}
hists_2d = {}


for path, subnode in node.ListNodes(withObjects=True):
  if path not in ["Tau1_pt","Mu1_pt","2D"]:
    continue
  split_path = path.split('/')[:-1]
  name = path.split('/')[-1]
  for opath,objname, obj in subnode.ListObjects(depth=0):
    if path=="Tau1_pt":
      hists_taupt[objname] = obj
    elif path=="Mu1_pt":
      hists_mupt[objname] = obj
    elif path=="2D":
      hists_2d[objname]  = obj

tau_pt = [30., 31., 32., 33., 34., 35., 40., 45., 50. ,75., 100.,200.]
mutau_eta = [0., 0.9, 1.2, 2.1]
etau_eta = [0., 0.8, 1.444, 1.566, 2., 2.1]

if channel=="METmutau":
    lep_eta = mutau_eta
elif channel=="METetau":
    lep_eta = etau_etau

for selection_prong in ["1prong","3prong"]:
  for j in range(len(lep_eta)-1):
    #2D
    canv_2d_data = TCanvas("2D","Tau pt vs mu pt checks",600,400)
    gStyle.SetOptStat(0)
    data = TH2D("MET_data","cross trigger eff with MET trigger DATA",16,np.array([21., 22., 23., 24., 25., 26., 27., 28., 29., 30., 35., 40., 45., 50. ,75., 100., 200.]),11,np.array([30., 31., 32., 33., 34., 35., 40., 45., 50. ,75., 100., 200.]))
    data.Divide(hists_2d["data_obs_fired_%s_lepeta%s"%(selection_prong,lep_eta[j])],hists_2d["data_obs_%s_lepeta%s"%(selection_prong,lep_eta[j])])
    data.GetXaxis().SetTitle("#mu p_{T} (GeV)")
    data.GetYaxis().SetTitle("#tau p_{T} (GeV)")
    data.Draw("COLZ")
    canv_2d_data.SaveAs("plots/METchecks/%s/2D_data_%s_lepeta%s.pdf"%(year,selection_prong,lep_eta[j]))

    canv_2d_mc = TCanvas("2D","Tau pt vs mu pt checks",600,400)
    gStyle.SetOptStat(0)
    mc = TH2D("MET_mc","cross trigger eff with MET trigger MC",16,np.array([21., 22., 23., 24., 25., 26., 27., 28., 29., 30., 35., 40., 45., 50. ,75., 100., 200.]),11,np.array([30., 31., 32., 33., 34., 35., 40., 45., 50. ,75., 100., 200.]))
    mc.GetXaxis().SetTitle("#mu p_{T} (GeV)")
    mc.GetYaxis().SetTitle("#tau p_{T} (GeV)")
    mc.Divide(hists_2d["TTTo2L2Nu_fired_%s_lepeta%s"%(selection_prong,lep_eta[j])],hists_2d["TTTo2L2Nu_%s_lepeta%s"%(selection_prong,lep_eta[j])])
    mc.Draw("COLZ")
    canv_2d_mc.SaveAs("plots/METchecks/%s/2D_mc_%s_lepeta%s.pdf"%(year,selection_prong,lep_eta[j]))

    canv_muonpt = TCanvas("Muon_pt","Muon pt checks",600,400)
    gStyle.SetOptStat(0)
    mu_pt_data = TH1D("MET_muon_pt","cross trigger eff with MET trigger",16,np.array([21., 22., 23., 24., 25., 26., 27., 28., 29., 30., 35., 40., 45., 50. ,75., 100., 200.]))
    mu_pt_data.Divide(hists_mupt["data_obs_fired_%s_lepeta%s"%(selection_prong,lep_eta[j])],hists_mupt["data_obs_%s_lepeta%s"%(selection_prong,lep_eta[j])])
    mu_pt_data.GetXaxis().SetTitle("#mu p_{T} (GeV)")
    mu_pt_data.GetYaxis().SetTitle("efficiency")
    mu_pt_mc = TH1D("MET_muon_pt_mc","",16,np.array([21., 22., 23., 24., 25., 26., 27., 28., 29., 30., 35., 40., 45., 50. ,75., 100., 200.]))
    mu_pt_mc.Divide(hists_mupt["TTTo2L2Nu_fired_%s_lepeta%s"%(selection_prong,lep_eta[j])],hists_mupt["TTTo2L2Nu_%s_lepeta%s"%(selection_prong,lep_eta[j])])
    mu_pt_data.SetMarkerStyle(21)
    mu_pt_data.SetMarkerColor(1)
    mu_pt_data.SetLineColor(1)
    mu_pt_mc.SetMarkerStyle(20)
    mu_pt_mc.SetMarkerColor(2)
    mu_pt_mc.SetLineColor(2)
    mu_pt_data.GetYaxis().SetRangeUser(0.,1.1)
    leg = TLegend(0.7,0.2,0.85,0.35)
    leg.AddEntry(mu_pt_data,"data","p")
    leg.AddEntry(mu_pt_mc,"mc","p")
    leg.SetBorderSize(0)
    mu_pt_data.Draw("P0")
    mu_pt_mc.Draw("P0 SAME")
    leg.Draw("SAME")
    latex = TLatex()
    latex.SetNDC()
    latex.SetTextSize(0.04)
    latex.SetTextColor(1)
    latex.SetTextFont(42)
    latex.DrawLatex(0.3, 0.30, "#mu #eta: [%s-%s]"%(lep_eta[j],lep_eta[j+1]))
    latex.DrawLatex(0.3, 0.20, "#tau dm: %s"%selection_prong)
    canv_muonpt.SaveAs("plots/METchecks/%s/muon_pt_%s_lepeta%s.pdf"%(year,selection_prong,lep_eta[j]))
    for i in range(len(tau_pt)-1):
      canv_muonpt = TCanvas("Muon_pt","Muon pt checks",600,400)
      gStyle.SetOptStat(0)
      mu_pt_data = TH1D("MET_muon_pt","cross trigger eff with MET trigger",16,np.array([21., 22., 23., 24., 25., 26., 27., 28., 29., 30., 35., 40., 45., 50. ,75., 100., 200.]))
      mu_pt_data.Divide(hists_mupt["data_obs_fired_%s_taupt%s_lepeta%s"%(selection_prong,tau_pt[i],lep_eta[j])],hists_mupt["data_obs_%s_taupt%s_lepeta%s"%(selection_prong,tau_pt[i],lep_eta[j])])
      mu_pt_data.GetXaxis().SetTitle("#mu p_{T} (GeV)")
      mu_pt_data.GetYaxis().SetTitle("efficiency")
      mu_pt_mc = TH1D("MET_muon_pt_mc","",16,np.array([21., 22., 23., 24., 25., 26., 27., 28., 29., 30., 35., 40., 45., 50. ,75., 100., 200.]))
      mu_pt_mc.Divide(hists_mupt["TTTo2L2Nu_fired_%s_taupt%s_lepeta%s"%(selection_prong,tau_pt[i],lep_eta[j])],hists_mupt["TTTo2L2Nu_%s_taupt%s_lepeta%s"%(selection_prong,tau_pt[i],lep_eta[j])])
      mu_pt_data.SetMarkerStyle(21)
      mu_pt_data.SetMarkerColor(1)
      mu_pt_data.SetLineColor(1)
      mu_pt_mc.SetMarkerStyle(20)
      mu_pt_mc.SetMarkerColor(2)
      mu_pt_mc.SetLineColor(2)
      mu_pt_data.GetYaxis().SetRangeUser(0.,1.1)
      leg = TLegend(0.7,0.2,0.85,0.35)
      leg.AddEntry(mu_pt_data,"data","p")
      leg.AddEntry(mu_pt_mc,"mc","p")
      leg.SetBorderSize(0)
      mu_pt_data.Draw("P0")
      mu_pt_mc.Draw("P0 SAME")
      leg.Draw("SAME")
      latex = TLatex()
      latex.SetNDC()
      latex.SetTextSize(0.04)
      latex.SetTextColor(1)
      latex.SetTextFont(42)
      latex.DrawLatex(0.3, 0.30, "#mu #eta: [%s-%s]"%(lep_eta[j],lep_eta[j+1]))
      latex.DrawLatex(0.3, 0.25, "#tau p_{T}: [%s-%s]"%(tau_pt[i],tau_pt[i+1]))
      latex.DrawLatex(0.3, 0.20, "#tau dm: %s"%selection_prong)
      canv_muonpt.SaveAs("plots/METchecks/%s/muon_pt_%s_taupt%s_lepeta%s.pdf"%(year,selection_prong,tau_pt[i],lep_eta[j]))

print("Done")
