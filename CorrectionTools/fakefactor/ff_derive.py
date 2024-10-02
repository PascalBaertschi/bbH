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

outfile = ROOT.TFile('root/fakefactors_%s_%s.root'%(channel,year), 'RECREATE')

path = "Tau1_pt"
selections_prong = ['1prong', '3prong']

subnode = node["Tau1_pt"]
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
binning = np.array([30.,40.,50.,60.,70.,80.,100.,130.])
nBins = len(binning)-1
if channel=="mutau":
  binning_qcd = np.array([30.,40.,50.,60.,70.,80.,130.])
elif channel=="etau":
  #binning_qcd = np.array([30.,40.,50.,60.,130.])
  binning_qcd = np.array([30.,40.,50.,130.])
nBins_qcd = len(binning_qcd)-1
#remove variable bin width: replace binning with 30,130


#also change value in fakefactor.py!
cut_values = {
  "UL2018":{
    "mutau":{
      "1prong":{
        "qcd":90.,
        "w":115.,
        "tt":115.
      },
      "3prong":{
        "qcd":90.,
        "w":115.,
        "tt":90.
      },
    },
    "etau":{
      "1prong":{
        "qcd":90.,
        "w":115.,
        "tt":115.
      },
      "3prong":{
        "qcd":90., 
        "w":115.,
        "tt":90.
      },
    },
  },
  "UL2017":{
    "mutau":{
      "1prong":{
        "qcd":105.,
        "w":115.,
        "tt":115.
      },
      "3prong":{
        "qcd":105.,
        "w":115.,
        "tt":115.
      },
    },
    "etau":{
      "1prong":{
        "qcd":45.,
        "w":115.,
        "tt":75.
      },
      "3prong":{
        "qcd":90., 
        "w":115.,
        "tt":75.
      },
    },
  },
  "UL2016":{
    "mutau":{
      "1prong":{
        "qcd":90.,
        "w":115.,
        "tt":115.
      },
      "3prong":{
        "qcd":105.,
        "w":115.,
        "tt":90.
      },
    },
    "etau":{
      "1prong":{
        "qcd":90.,
        "w":115.,
        "tt":115.
      },
      "3prong":{
        "qcd":90.,
        "w":115.,
        "tt":115.
      },
    },
  },
}

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

titleright = "%s %.1f fb^{-1} (13 TeV)"%(year[2:],float(lumi))

gStyle.SetOptStat(0)
for prong in selections_prong:
  if channel == "mutau":
    channel_text = "#mu#tau_{h}, %s"%prong
  elif channel == "etau":
    channel_text = "e#tau_{h}, %s"%prong
  ff_qcd = TH1D("ff_qcd_%s"%prong,"",nBins_qcd,binning_qcd)
  ff_qcd.Divide(hists["DR_QCD_%s"%prong],hists["DR_QCD_AR_%s"%prong])
  ff_qcd.GetXaxis().SetTitle("#tau_{h} p_{T} (GeV)")
  ff_qcd.GetYaxis().SetTitle("fakefactor")
  ff_qcd.GetXaxis().SetTitleSize(0.05)
  ff_qcd.GetYaxis().SetTitleSize(0.05)
  ff_qcd.GetYaxis().SetTitleOffset(0.92)
  ff_qcd.GetXaxis().SetLabelSize(0.05)
  ff_qcd.GetYaxis().SetLabelSize(0.05)
  cut_value_qcd = cut_values[year][channel][prong]["qcd"]
  ff_qcd.Fit("pol1","","",30.,cut_value_qcd)
  y_val = ff_qcd.GetFunction("pol1").Eval(cut_value_qcd)
  qcd_fit = ff_qcd.GetFunction("pol1")
  qcd_fit_par0 = qcd_fit.GetParameter(0)
  qcd_fit_par1 = qcd_fit.GetParameter(1)
  qcd_fit_par0_error = qcd_fit.GetParError(0)
  qcd_fit_par1_error = qcd_fit.GetParError(1)
  qcd_fit_par0_up = qcd_fit_par0 + qcd_fit_par0_error
  qcd_fit_par0_down = qcd_fit_par0 - qcd_fit_par0_error
  qcd_fit_par1_up = qcd_fit_par1 + qcd_fit_par1_error
  qcd_fit_par1_down = qcd_fit_par1 - qcd_fit_par1_error
  qcd_func_par0_up = TF1("qcd_func_%s_par0_up"%prong,"%s*x+%s"%(qcd_fit_par1,qcd_fit_par0_up),30.,130.)
  qcd_func_par0_down = TF1("qcd_func_%s_par0_down"%prong,"%s*x+%s"%(qcd_fit_par1,qcd_fit_par0_down),30.,130.)
  qcd_func_par1_up = TF1("qcd_func_%s_par1_up"%prong,"%s*x+%s"%(qcd_fit_par1_up,qcd_fit_par0),30.,130.)
  qcd_func_par1_down = TF1("qcd_func_%s_par1_down"%prong,"%s*x+%s"%(qcd_fit_par1_down,qcd_fit_par0),30.,130.)
  #### flat fit #####
  ff_qcd_flat = TH1D("ff_qcd_flat_%s"%prong,"",nBins_qcd,binning_qcd)
  ff_qcd_flat.Divide(hists["DR_QCD_%s"%prong],hists["DR_QCD_AR_%s"%prong])
  ff_qcd_flat.GetXaxis().SetTitle("#tau_{h} p_{T} (GeV)")
  ff_qcd_flat.GetYaxis().SetTitle("fakefactor")
  ff_qcd_flat.Fit("pol0","","",30.,130.)
  qcd_flatfit = ff_qcd_flat.GetFunction("pol0")
  qcd_flatfit_par0 = qcd_flatfit.GetParameter(0)
  qcd_flatfit_par0_error = qcd_flatfit.GetParError(0)
  qcd_flatfit_par0_up = qcd_flatfit_par0 + qcd_flatfit_par0_error
  qcd_flatfit_par0_down = qcd_flatfit_par0 - qcd_flatfit_par0_error
  qcd_flatfunc_par0_up = TF1("qcd_flatfunc_%s_par0_up"%prong,"%s"%(qcd_flatfit_par0_up),30.,130.)
  qcd_flatfunc_par0_down = TF1("qcd_flatfunc_%s_par0_down"%prong,"%s"%(qcd_flatfit_par0_down),30.,130.)
  ###################
  line_qcd = TLine(cut_value_qcd,y_val,130.,y_val)
  ff_cr_qcd = TH1D("ff_cr_qcd_%s"%prong,"ff CR QCD %s"%prong,nBins_qcd,binning_qcd)
  ff_cr_qcd.Divide(hists["CR_QCD_%s"%prong],hists["CR_QCD_AR_%s"%prong])
  ff_cr_qcd.GetXaxis().SetTitle("#tau_{h} p_{T} (GeV)")
  ff_cr_qcd.GetYaxis().SetTitle("fakefactor")
  ff_comp_qcd = TH1D("ff_comp_qcd_%s"%prong,"ff DR/CR QCD %s"%prong,nBins_qcd,binning_qcd)
  ff_comp_qcd.Divide(ff_qcd,ff_cr_qcd)
  ff_comp_qcd.GetXaxis().SetTitle("#tau_{h} p_{T} (GeV)")
  ff_comp_qcd.GetYaxis().SetTitle("ff DR/CR")
  ff_w = TH1D("ff_w_%s"%prong,"",nBins,binning)
  ff_w.Divide(hists["DR_W_%s"%prong],hists["DR_W_AR_%s"%prong])
  ff_w.GetXaxis().SetTitle("#tau_{h} p_{T} (GeV)")
  ff_w.GetYaxis().SetTitle("fakefactor")
  ff_w.GetXaxis().SetTitleSize(0.05)
  ff_w.GetYaxis().SetTitleSize(0.05)
  ff_w.GetYaxis().SetTitleOffset(0.92)
  ff_w.GetXaxis().SetLabelSize(0.05)
  ff_w.GetYaxis().SetLabelSize(0.05)
  cut_value_w = cut_values[year][channel][prong]["w"]
  ff_w.Fit("pol2","","",30.,cut_value_w)
  y_val = ff_w.GetFunction("pol2").Eval(cut_value_w)
  w_fit = ff_w.GetFunction("pol2")
  w_fit_par0 = w_fit.GetParameter(0)
  w_fit_par1 = w_fit.GetParameter(1)
  w_fit_par2 = w_fit.GetParameter(2)
  w_fit_par0_error = w_fit.GetParError(0)
  w_fit_par1_error = w_fit.GetParError(1)
  w_fit_par2_error = w_fit.GetParError(2)
  w_fit_par0_up = w_fit_par0 + w_fit_par0_error
  w_fit_par0_down = w_fit_par0 - w_fit_par0_error
  w_fit_par1_up = w_fit_par1 + w_fit_par1_error
  w_fit_par1_down = w_fit_par1 - w_fit_par1_error
  w_fit_par2_up = w_fit_par2 + w_fit_par2_error
  w_fit_par2_down = w_fit_par2 - w_fit_par2_error
  w_func_par0_up = TF1("w_func_%s_par0_up"%prong,"%s*x*x+%s*x+%s"%(w_fit_par2,w_fit_par1,w_fit_par0_up),30.,130.)
  w_func_par0_down = TF1("w_func_%s_par0_down"%prong,"%s*x*x+%s*x+%s"%(w_fit_par2,w_fit_par1,w_fit_par0_down),30.,130.)
  w_func_par1_up = TF1("w_func_%s_par1_up"%prong,"%s*x*x+%s*x+%s"%(w_fit_par2,w_fit_par1_up,w_fit_par0),30.,130.)
  w_func_par1_down = TF1("w_func_%s_par1_down"%prong,"%s*x*x+%s*x+%s"%(w_fit_par2,w_fit_par1_down,w_fit_par0),30.,130.)
  w_func_par2_up = TF1("w_func_%s_par2_up"%prong,"%s*x*x+%s*x+%s"%(w_fit_par2_up,w_fit_par1,w_fit_par0),30.,130.)
  w_func_par2_down = TF1("w_func_%s_par2_down"%prong,"%s*x*x+%s*x+%s"%(w_fit_par2_down,w_fit_par1,w_fit_par0),30.,130.)
  line_w = TLine(cut_value_w,y_val,130.,y_val)
  ff_cr_w = TH1D("ff_cr_w_%s"%prong,"ff CR W %s"%prong,nBins,binning)
  ff_cr_w.Divide(hists["CR_W_%s"%prong],hists["CR_W_AR_%s"%prong])
  ff_cr_w.GetXaxis().SetTitle("#tau_{h} p_{T} (GeV)")
  ff_cr_w.GetYaxis().SetTitle("fakefactor")
  ff_comp_w = TH1D("ff_comp_w_%s"%prong,"ff DR/CR W %s"%prong,nBins,binning)
  ff_comp_w.Divide(ff_w,ff_cr_w)
  ff_comp_w.GetXaxis().SetTitle("#tau_{h} p_{T} (GeV)")
  ff_comp_w.GetYaxis().SetTitle("ff DR/CR")
  ff_tt = TH1D("ff_tt_%s"%prong,"",nBins,binning)
  #ff_tt.Divide(hists["DR_TT_%s"%prong],hists["DR_TT_AR_%s"%prong])
  ff_tt.Divide(hists["TT_DR_TT_%s_fakes"%prong],hists["TT_DR_TT_AR_%s_fakes"%prong]) #using MC to derive fakefactor
  cut_value_tt = cut_values[year][channel][prong]["tt"]
  #ff_tt.Fit("pol3","","",30.,cut_value_tt)
  #y_val = ff_tt.GetFunction("pol3").Eval(cut_value_tt)
  ff_tt.Fit("pol1","","",30.,cut_value_tt)
  y_val = ff_tt.GetFunction("pol1").Eval(cut_value_tt)
  tt_fit = ff_tt.GetFunction("pol1")
  tt_fit_par0 = tt_fit.GetParameter(0)
  tt_fit_par1 = tt_fit.GetParameter(1)
  tt_fit_par0_error = tt_fit.GetParError(0)
  tt_fit_par1_error = tt_fit.GetParError(1)
  tt_fit_par0_up = tt_fit_par0 + tt_fit_par0_error
  tt_fit_par0_down = tt_fit_par0 - tt_fit_par0_error
  tt_fit_par1_up = tt_fit_par1 + tt_fit_par1_error
  tt_fit_par1_down = tt_fit_par1 - tt_fit_par1_error
  tt_func_par0_up = TF1("tt_func_%s_par0_up"%prong,"%s*x+%s"%(tt_fit_par1,tt_fit_par0_up),30.,130.)
  tt_func_par0_down = TF1("tt_func_%s_par0_down"%prong,"%s*x+%s"%(tt_fit_par1,tt_fit_par0_down),30.,130.)
  tt_func_par1_up = TF1("tt_func_%s_par1_up"%prong,"%s*x+%s"%(tt_fit_par1_up,tt_fit_par0),30.,130.)
  tt_func_par1_down = TF1("tt_func_%s_par1_down"%prong,"%s*x+%s"%(tt_fit_par1_down,tt_fit_par0),30.,130.)
  line_tt = TLine(cut_value_tt,y_val,130.,y_val)
  #mean_ff_tt = ff_tt.Integral()/ff_tt.GetNbinsX()
  ff_tt.GetXaxis().SetTitle("#tau_{h} p_{T} (GeV)")
  ff_tt.GetYaxis().SetTitle("fakefactor")
  ff_tt.GetXaxis().SetTitleSize(0.05)
  ff_tt.GetYaxis().SetTitleSize(0.05)
  ff_tt.GetYaxis().SetTitleOffset(0.92)
  ff_tt.GetXaxis().SetLabelSize(0.05)
  ff_tt.GetYaxis().SetLabelSize(0.05)
  ff_lcr_data_tt = TH1D("ff_lcr_data_tt_%s"%prong,"ff LCR data tt %s"%prong,nBins,binning)
  ff_lcr_data_tt.Divide(hists["LCR_TT_%s"%prong],hists["LCR_TT_AR_%s"%prong])
  ff_lcr_data_tt.GetXaxis().SetTitle("#tau_{h} p_{T} (GeV)")
  ff_lcr_data_tt.GetYaxis().SetTitle("fakefactor")
  ff_lcr_mc_tt = TH1D("ff_lcr_mc_tt_%s"%prong,"ff LCR MC tt %s"%prong,nBins,binning)
  ff_lcr_mc_tt.Divide(hists["TT_LCR_TT_%s_fakes"%prong],hists["TT_LCR_TT_AR_%s_fakes"%prong])
  ff_lcr_mc_tt.GetXaxis().SetTitle("#tau_{h} p_{T} (GeV)")
  ff_lcr_mc_tt.GetYaxis().SetTitle("fakefactor MC")
  ff_cr_tt = TH1D("ff_cr_tt_%s"%prong,"ff CR tt %s"%prong,nBins,binning)
  ff_cr_tt.Divide(hists["CR_TT_%s"%prong],hists["CR_TT_AR_%s"%prong])
  #mean_ff_cr_tt = ff_cr_tt.Integral()/ff_cr_tt.GetNbinsX()
  ff_cr_tt.GetXaxis().SetTitle("#tau_{h} p_{T} (GeV)")
  ff_cr_tt.GetYaxis().SetTitle("fakefactor")
  ff_comp_tt = TH1D("ff_comp_tt_%s"%prong,"ff DR/CR tt %s"%prong,nBins,binning)
  ff_comp_tt.Divide(ff_tt,ff_cr_tt)
  ff_comp_tt.GetXaxis().SetTitle("#tau_{h} p_{T} (GeV)")
  ff_comp_tt.GetYaxis().SetTitle("ff DR/CR")
  #ff_tt.Scale(mean_ff_cr_tt/mean_ff_tt)
  #### MC checks   ####
  w_sr = TH1D("w_sr_%s"%prong,"iso/anti-iso %s"%prong,nBins,binning)
  w_sr.Divide(hists["WJetscomb_SR_W_%s"%prong],hists["WJetscomb_SR_W_AR_%s"%prong])
  w_sr.GetXaxis().SetTitle("#tau_{h} p_{T} (GeV)")
  w_sr.GetYaxis().SetTitle("fakefactor")
  w_dr = TH1D("w_dr_%s"%prong,"iso/anti-iso %s"%prong,nBins,binning)
  w_dr.Divide(hists["WJetscomb_DR_W_%s"%prong],hists["WJetscomb_DR_W_AR_%s"%prong])
  w_dr.GetXaxis().SetTitle("#tau_{h} p_{T} (GeV)")
  w_dr.GetYaxis().SetTitle("fakefactor")
  w_cr = TH1D("w_cr_%s"%prong,"iso/anti-iso %s"%prong,nBins,binning)
  w_cr.Divide(hists["WJetscomb_CR_W_%s"%prong],hists["WJetscomb_CR_W_AR_%s"%prong])
  w_cr.GetXaxis().SetTitle("#tau_{h} p_{T} (GeV)")
  w_cr.GetYaxis().SetTitle("fakefactor")
  w_sr_dr = TH1D("w_sr_dr_%s"%prong,"iso/anti-iso in SR/DR %s"%prong,nBins,binning)
  w_sr_dr.Divide(w_sr,w_dr)
  w_sr_dr.GetXaxis().SetTitle("#tau_{h} p_{T} (GeV)")
  w_sr_dr.GetYaxis().SetTitle("SR/DR")
  w_sr_cr = TH1D("w_sr_cr_%s"%prong,"iso/anti-iso in SR/CR %s"%prong,nBins,binning)
  w_sr_cr.Divide(w_sr,w_cr)
  w_sr_cr.GetXaxis().SetTitle("#tau_{h} p_{T} (GeV)")
  w_sr_cr.GetYaxis().SetTitle("SR/CR")
  tt_sr = TH1D("tt_sr_%s"%prong,"iso/anti-iso %s"%prong,nBins,binning)
  tt_sr.Divide(hists["TT_SR_TT_%s"%prong],hists["TT_SR_TT_AR_%s"%prong])
  tt_sr.GetXaxis().SetTitle("#tau_{h} p_{T} (GeV)")
  tt_sr.GetYaxis().SetTitle("fakefactor")
  tt_dr = TH1D("tt_dr_%s"%prong,"iso/anti-iso %s"%prong,nBins,binning)
  tt_dr.Divide(hists["TT_DR_TT_%s"%prong],hists["TT_DR_TT_AR_%s"%prong])
  tt_dr.GetXaxis().SetTitle("#tau_{h} p_{T} (GeV)")
  tt_dr.GetYaxis().SetTitle("fakefactor")
  tt_sr_dr = TH1D("tt_sr_dr_%s"%prong,"iso/anti-iso in SR/DR %s"%prong,nBins,binning)
  tt_sr_dr.Divide(tt_sr,tt_dr)
  tt_sr_dr.GetXaxis().SetTitle("#tau_{h} p_{T} (GeV)")
  tt_sr_dr.GetYaxis().SetTitle("SR/DR")
  tt_cr = TH1D("tt_cr_%s"%prong,"iso/anti-iso %s"%prong,nBins,binning)
  tt_cr.Divide(hists["TT_CR_TT_%s"%prong],hists["TT_CR_TT_AR_%s"%prong])
  tt_cr.GetXaxis().SetTitle("#tau_{h} p_{T} (GeV)")
  tt_cr.GetYaxis().SetTitle("fakefactor")
  tt_sr_cr = TH1D("tt_sr_cr_%s"%prong,"iso/anti-iso in SR/CR %s"%prong,nBins,binning)
  tt_sr_cr.Divide(tt_sr,tt_cr)
  tt_sr_cr.GetXaxis().SetTitle("#tau_{h} p_{T} (GeV)")
  tt_sr_cr.GetYaxis().SetTitle("SR/CR")
  qcd_sr = TH1D("qcd_sr_%s"%prong,"iso/anti-iso %s"%prong,nBins,binning)
  qcd_sr.Divide(hists["TT_SR_TT_%s"%prong],hists["TT_SR_TT_AR_%s"%prong])
  qcd_sr.GetXaxis().SetTitle("#tau_{h} p_{T} (GeV)")
  qcd_sr.GetYaxis().SetTitle("fakefactor")
  qcd_dr = TH1D("tt_dr_%s"%prong,"iso/anti-iso %s"%prong,nBins,binning)
  qcd_dr.Divide(hists["TT_DR_TT_%s"%prong],hists["TT_DR_TT_AR_%s"%prong])
  qcd_dr.GetXaxis().SetTitle("#tau_{h} p_{T} (GeV)")
  qcd_dr.GetYaxis().SetTitle("fakefactor")
  qcd_sr_dr = TH1D("tt_sr_dr_%s"%prong,"iso/anti-iso in SR/DR %s"%prong,nBins,binning)
  qcd_sr_dr.Divide(tt_sr,tt_dr)
  qcd_sr_dr.GetXaxis().SetTitle("#tau_{h} p_{T} (GeV)")
  qcd_sr_dr.GetYaxis().SetTitle("SR/DR")
  ####################
  ff_qcd.Write()
  qcd_func_par0_up.Write()
  qcd_func_par0_down.Write()
  qcd_func_par1_up.Write()
  qcd_func_par1_down.Write()
  ff_qcd_flat.Write()
  qcd_flatfunc_par0_up.Write()
  qcd_flatfunc_par0_down.Write()
  ff_w.Write()
  w_func_par0_up.Write()
  w_func_par0_down.Write()
  w_func_par1_up.Write()
  w_func_par1_down.Write()
  w_func_par2_up.Write()
  w_func_par2_down.Write()
  ff_tt.Write()
  tt_func_par0_up.Write()
  tt_func_par0_down.Write()
  tt_func_par1_up.Write()
  tt_func_par1_down.Write()
  # FF QCD
  canv1 = TCanvas("ff_qcd_%s"%prong,"ff_qcd_%s"%prong,600,400)
  canv1.SetBottomMargin(0.12)
  ff_qcd.SetMarkerStyle(8)
  ff_qcd.SetLineColor(1)
  ff_qcd.GetYaxis().SetRangeUser(0.,0.5)
  ff_qcd.Draw("PE")
  line_qcd.SetLineWidth(2)
  line_qcd.SetLineColor(2)
  line_qcd.Draw("SAME")
  qcd_func_par0_up.SetLineStyle(2)
  qcd_func_par0_up.SetLineColorAlpha(2,0.4)
  qcd_func_par0_down.SetLineStyle(2)
  qcd_func_par0_down.SetLineColorAlpha(2,0.4)
  qcd_func_par0_up.Draw("SAME")
  qcd_func_par0_down.Draw("SAME")
  qcd_func_par1_up.SetLineStyle(2)
  qcd_func_par1_up.SetLineColorAlpha(2,0.4)
  qcd_func_par1_down.SetLineStyle(2)
  qcd_func_par1_down.SetLineColorAlpha(2,0.4)
  qcd_func_par1_up.Draw("SAME")
  qcd_func_par1_down.Draw("SAME")
  latex = TLatex()
  latex.SetNDC()
  latex.SetTextFont(42)
  #latex.DrawLatex(0.6, 0.8,"%s  %s"%(channel, year))
  #plot.DrawCMSLogo(canv1, "CMS", "Internal", 10, 0.045, 0.05, 1.0, '', 0.8)
  plot.DrawCMSLogo(canv1, "Private work", "(CMS data/simulation)", 10, 0.045, 0.05, 1.0, '', 0.8)
  plot.DrawTitle(canv1, titleright, 3, 0.2, 0.5)
  plot.Set(latex, NDC=None, TextFont=42, TextSize=0.05)
  latex.DrawLatex(0.15, 0.68, channel_text+", QCD DR")
  canv1.SaveAs("plots/%s_%s/ff_qcd_%s.pdf"%(channel,year,prong))
  canv1.SaveAs("plots/%s_%s/ff_qcd_%s.png"%(channel,year,prong))
  canv1.SaveAs("plots/thesis/ff_qcd_%s_%s_%s.pdf"%(prong,channel,year))
  ## flat fit
  canv111 = TCanvas("ff_qcd_flat_%s"%prong,"ff_qcd_flat_%s"%prong,600,400)
  ff_qcd_flat.SetMarkerStyle(8)
  ff_qcd_flat.SetLineColor(1)
  ff_qcd_flat.GetYaxis().SetRangeUser(0.,0.5)
  ff_qcd_flat.Draw("PE")
  qcd_flatfunc_par0_up.SetLineStyle(2)
  qcd_flatfunc_par0_up.SetLineColorAlpha(2,0.4)
  qcd_flatfunc_par0_down.SetLineStyle(2)
  qcd_flatfunc_par0_down.SetLineColorAlpha(2,0.4)
  qcd_flatfunc_par0_up.Draw("SAME")
  qcd_flatfunc_par0_down.Draw("SAME")
  latex = TLatex()
  latex.SetNDC()
  latex.SetTextFont(42)
  #plot.DrawCMSLogo(canv111, "CMS", "Internal", 10, 0.045, 0.05, 1.0, '', 0.8)
  plot.DrawCMSLogo(canv111, "Private work", "(CMS data/simulation)", 10, 0.045, 0.05, 1.0, '', 0.8)
  plot.DrawTitle(canv111, titleright, 3, 0.2, 0.5)
  plot.Set(latex, NDC=None, TextFont=42, TextSize=0.05)
  latex.DrawLatex(0.15, 0.68, channel_text)
  canv111.SaveAs("plots/%s_%s/ff_qcd_flat_%s.pdf"%(channel,year,prong))
  canv111.SaveAs("plots/%s_%s/ff_qcd_flat_%s.png"%(channel,year,prong))
  ####
  canv2 = TCanvas("ff_cr_qcd%s"%prong,"ff_cr_qcd_%s"%prong,600,400)
  ff_cr_qcd.SetMarkerStyle(8)
  ff_cr_qcd.SetLineColor(1)
  ff_cr_qcd.GetYaxis().SetRangeUser(0.,1.)
  ff_cr_qcd.Draw("PE")
  latex = TLatex()
  latex.SetNDC()
  latex.SetTextFont(42)
  #plot.DrawCMSLogo(canv2, "CMS", "Internal", 10, 0.045, 0.05, 1.0, '', 0.8)
  plot.DrawCMSLogo(canv2, "Private work", "(CMS data/simulation)", 10, 0.045, 0.05, 1.0, '', 0.8)
  plot.DrawTitle(canv2, titleright, 3, 0.2, 0.4)
  plot.Set(latex, NDC=None, TextFont=42, TextSize=0.05)
  latex.DrawLatex(0.15, 0.68, channel_text)
  #latex.DrawLatex(0.6, 0.8,"%s  %s"%(channel, year))
  canv2.SaveAs("plots/%s_%s/ff_cr_qcd_%s.pdf"%(channel,year,prong))
  canv2.SaveAs("plots/%s_%s/ff_cr_qcd_%s.png"%(channel,year,prong))
  canv3 = TCanvas("ff_comp_qcd%s"%prong,"ff_comp_qcd_%s"%prong,600,400)
  ff_comp_qcd.SetMarkerStyle(8)
  ff_comp_qcd.SetLineColor(1)
  ff_comp_qcd.GetYaxis().SetRangeUser(0.5,1.5)
  ff_comp_qcd.Draw("PE")
  latex = TLatex()
  latex.SetNDC()
  latex.SetTextFont(42)
  #latex.DrawLatex(0.6, 0.8,"%s  %s"%(channel, year))
  #plot.DrawCMSLogo(canv3, "CMS", "Internal", 10, 0.045, 0.05, 1.0, '', 0.8)
  plot.DrawCMSLogo(canv3, "Private work", "(CMS data/simulation)", 10, 0.045, 0.05, 1.0, '', 0.8)
  plot.DrawTitle(canv3, titleright, 3, 0.2, 0.4)
  plot.Set(latex, NDC=None, TextFont=42, TextSize=0.05)
  latex.DrawLatex(0.15, 0.68, channel_text)
  canv3.SaveAs("plots/%s_%s/ff_comp_qcd_%s.pdf"%(channel,year,prong))
  canv3.SaveAs("plots/%s_%s/ff_comp_qcd_%s.png"%(channel,year,prong))
  # FF W
  canv4 = TCanvas("ff_w_%s"%prong,"ff_w_%s"%prong,600,400)
  canv4.SetBottomMargin(0.12)
  ff_w.SetMarkerStyle(8)
  ff_w.SetLineColor(1)
  ff_w.GetYaxis().SetRangeUser(0.,0.5)
  ff_w.Draw("PE")
  line_w.SetLineWidth(2)
  line_w.SetLineColor(2)
  line_w.Draw("SAME")
  w_func_par0_up.SetLineStyle(2)
  w_func_par0_up.SetLineColorAlpha(2,0.4)
  w_func_par0_down.SetLineStyle(2)
  w_func_par0_down.SetLineColorAlpha(2,0.4)
  w_func_par0_up.Draw("SAME")
  w_func_par0_down.Draw("SAME")
  w_func_par1_up.SetLineStyle(2)
  w_func_par1_up.SetLineColorAlpha(2,0.4)
  w_func_par1_down.SetLineStyle(2)
  w_func_par1_down.SetLineColorAlpha(2,0.4)
  w_func_par1_up.Draw("SAME")
  w_func_par1_down.Draw("SAME")
  w_func_par2_up.SetLineStyle(2)
  w_func_par2_up.SetLineColorAlpha(2,0.4)
  w_func_par2_down.SetLineStyle(2)
  w_func_par2_down.SetLineColorAlpha(2,0.4)
  w_func_par2_up.Draw("SAME")
  w_func_par2_down.Draw("SAME")
  #w_func_par3_up.SetLineStyle(2)
  #w_func_par3_up.SetLineColorAlpha(2,0.4)
  #w_func_par3_down.SetLineStyle(2)
  #w_func_par3_down.SetLineColorAlpha(2,0.4)
  #w_func_par3_up.Draw("SAME")
  #w_func_par3_down.Draw("SAME")
  latex = TLatex()
  latex.SetNDC()
  latex.SetTextFont(42)
  #latex.DrawLatex(0.6, 0.8,"%s  %s"%(channel, year))
  #plot.DrawCMSLogo(canv4, "CMS", "Internal", 10, 0.045, 0.05, 1.0, '', 0.8)
  plot.DrawCMSLogo(canv4, "Private work", "(CMS data/simulation)", 10, 0.045, 0.05, 1.0, '', 0.8)
  plot.DrawTitle(canv4, titleright, 3, 0.2, 0.5)
  plot.Set(latex, NDC=None, TextFont=42, TextSize=0.05)
  latex.DrawLatex(0.15, 0.68, channel_text+", W+jets DR")
  canv4.SaveAs("plots/%s_%s/ff_w_%s.pdf"%(channel,year,prong))
  canv4.SaveAs("plots/%s_%s/ff_w_%s.png"%(channel,year,prong))
  canv4.SaveAs("plots/thesis/ff_w_%s_%s_%s.pdf"%(prong,channel,year))
  canv5 = TCanvas("ff_cr_w_%s"%prong,"ff_cr_w_%s"%prong,600,400)
  ff_cr_w.SetMarkerStyle(8)
  ff_cr_w.SetLineColor(1)
  ff_cr_w.GetYaxis().SetRangeUser(0.,1.)
  ff_cr_w.Draw("PE")
  latex = TLatex()
  latex.SetNDC()
  latex.SetTextFont(42)
  #latex.DrawLatex(0.6, 0.8,"%s  %s"%(channel, year))
  #plot.DrawCMSLogo(canv5, "CMS", "Internal", 10, 0.045, 0.05, 1.0, '', 0.8)
  plot.DrawCMSLogo(canv5, "Private work", "(CMS data/simulation)", 10, 0.045, 0.05, 1.0, '', 0.8)
  plot.DrawTitle(canv5, titleright, 3, 0.2, 0.4)
  plot.Set(latex, NDC=None, TextFont=42, TextSize=0.05)
  latex.DrawLatex(0.15, 0.68, channel_text)
  canv5.SaveAs("plots/%s_%s/ff_cr_w_%s.pdf"%(channel,year,prong))
  canv5.SaveAs("plots/%s_%s/ff_cr_w_%s.png"%(channel,year,prong))
  canv6 = TCanvas("ff_comp_w_%s"%prong,"ff_comp_w_%s"%prong,600,400)
  ff_comp_w.SetMarkerStyle(8)
  ff_comp_w.SetLineColor(1)
  ff_comp_w.GetYaxis().SetRangeUser(0.5,1.5)
  ff_comp_w.Draw("PE")
  latex = TLatex()
  latex.SetNDC()
  latex.SetTextFont(42)
  #latex.DrawLatex(0.6, 0.8,"%s  %s"%(channel, year))
  #plot.DrawCMSLogo(canv6, "CMS", "Internal", 10, 0.045, 0.05, 1.0, '', 0.8)
  plot.DrawCMSLogo(canv6, "Private work", "(CMS data/simulation)", 10, 0.045, 0.05, 1.0, '', 0.8)
  plot.DrawTitle(canv6, titleright, 3, 0.2, 0.4)
  plot.Set(latex, NDC=None, TextFont=42, TextSize=0.05)
  latex.DrawLatex(0.15, 0.68, channel_text)
  canv6.SaveAs("plots/%s_%s/ff_comp_w_%s.pdf"%(channel,year,prong)) 
  canv6.SaveAs("plots/%s_%s/ff_comp_w_%s.png"%(channel,year,prong)) 
  # FF TT
  canv7 = TCanvas("ff_tt%s"%prong,"ff_tt_%s"%prong,600,400)
  canv7.SetBottomMargin(0.12)
  ff_tt.SetMarkerStyle(8)
  ff_tt.SetLineColor(1)
  ff_tt.GetYaxis().SetRangeUser(0.,0.5)
  ff_tt.Draw("PE")
  line_tt.SetLineWidth(2)
  line_tt.SetLineColor(2)
  line_tt.Draw("SAME")
  tt_func_par0_up.SetLineStyle(2)
  tt_func_par0_up.SetLineColorAlpha(2,0.4)
  tt_func_par0_down.SetLineStyle(2)
  tt_func_par0_down.SetLineColorAlpha(2,0.4)
  tt_func_par0_up.Draw("SAME")
  tt_func_par0_down.Draw("SAME")
  tt_func_par1_up.SetLineStyle(2)
  tt_func_par1_up.SetLineColorAlpha(2,0.4)
  tt_func_par1_down.SetLineStyle(2)
  tt_func_par1_down.SetLineColorAlpha(2,0.4)
  tt_func_par1_up.Draw("SAME")
  tt_func_par1_down.Draw("SAME")
  latex = TLatex()
  latex.SetNDC()
  latex.SetTextFont(42)
  #latex.DrawLatex(0.6, 0.8,"%s  %s"%(channel, year))
  #plot.DrawCMSLogo(canv7, "CMS", "Internal", 10, 0.045, 0.05, 1.0, '', 0.8)
  plot.DrawCMSLogo(canv7, "Private work", "(CMS data/simulation)", 10, 0.045, 0.05, 1.0, '', 0.8)
  plot.DrawTitle(canv7, titleright, 3, 0.2, 0.5)
  plot.Set(latex, NDC=None, TextFont=42, TextSize=0.05)
  latex.DrawLatex(0.15, 0.68, channel_text+", t#bar{t} DR")
  canv7.SaveAs("plots/%s_%s/ff_tt_%s.pdf"%(channel,year,prong))
  canv7.SaveAs("plots/%s_%s/ff_tt_%s.png"%(channel,year,prong))
  canv7.SaveAs("plots/thesis/ff_tt_%s_%s_%s.pdf"%(prong,channel,year))

  canv71 = TCanvas("ff_lcr_data_tt%s"%prong,"ff_lcr_data_tt_%s"%prong,600,400)
  ff_lcr_data_tt.SetMarkerStyle(8)
  ff_lcr_data_tt.SetLineColor(1)
  ff_lcr_data_tt.GetYaxis().SetRangeUser(0.,0.5)
  ff_lcr_data_tt.Draw("PE")
  latex = TLatex()
  latex.SetNDC()
  latex.SetTextFont(42)
  #latex.DrawLatex(0.6, 0.8,"%s  %s"%(channel, year))
  #plot.DrawCMSLogo(canv71, "CMS", "Internal", 10, 0.045, 0.05, 1.0, '', 0.8)
  plot.DrawCMSLogo(canv71, "Private work", "(CMS data/simulation)", 10, 0.045, 0.05, 1.0, '', 0.8)
  plot.DrawTitle(canv71, titleright, 3, 0.2, 0.4)
  plot.Set(latex, NDC=None, TextFont=42, TextSize=0.05)
  latex.DrawLatex(0.15, 0.68, channel_text)
  canv71.SaveAs("plots/%s_%s/ff_lcr_data_tt_%s.pdf"%(channel,year,prong))
  canv71.SaveAs("plots/%s_%s/ff_lcr_data_tt_%s.png"%(channel,year,prong))

  canv72 = TCanvas("ff_lcr_mc_tt%s"%prong,"ff_lcr_mc_tt_%s"%prong,600,400)
  ff_lcr_mc_tt.SetMarkerStyle(8)
  ff_lcr_mc_tt.SetLineColor(1)
  ff_lcr_mc_tt.GetYaxis().SetRangeUser(0.,0.5)
  ff_lcr_mc_tt.Draw("PE")
  latex = TLatex()
  latex.SetNDC()
  latex.SetTextFont(42)
  #latex.DrawLatex(0.6, 0.8,"%s  %s"%(channel, year))
  #plot.DrawCMSLogo(canv72, "CMS", "Internal", 10, 0.045, 0.05, 1.0, '', 0.8)
  plot.DrawCMSLogo(canv72, "Private work", "(CMS data/simulation)", 10, 0.045, 0.05, 1.0, '', 0.8)
  plot.DrawTitle(canv72, titleright, 3, 0.2, 0.4)
  plot.Set(latex, NDC=None, TextFont=42, TextSize=0.05)
  latex.DrawLatex(0.15, 0.68, channel_text)
  canv72.SaveAs("plots/%s_%s/ff_lcr_mc_tt_%s.pdf"%(channel,year,prong))
  canv72.SaveAs("plots/%s_%s/ff_lcr_mc_tt_%s.png"%(channel,year,prong))

  canv8 = TCanvas("ff_cr_tt%s"%prong,"ff_cr_tt_%s"%prong,600,400)
  ff_cr_tt.SetMarkerStyle(8)
  ff_cr_tt.SetLineColor(1)
  ff_cr_tt.GetYaxis().SetRangeUser(0.,1.)
  ff_cr_tt.Draw("PE")
  latex = TLatex()
  latex.SetNDC()
  latex.SetTextFont(42)
  #latex.DrawLatex(0.6, 0.8,"%s  %s"%(channel, year))
  #plot.DrawCMSLogo(canv8, "CMS", "Internal", 10, 0.045, 0.05, 1.0, '', 0.8)
  plot.DrawCMSLogo(canv8, "Private work", "(CMS data/simulation)", 10, 0.045, 0.05, 1.0, '', 0.8)
  plot.DrawTitle(canv8, titleright, 3, 0.2, 0.4)
  plot.Set(latex, NDC=None, TextFont=42, TextSize=0.05)
  latex.DrawLatex(0.15, 0.68, channel_text)
  canv8.SaveAs("plots/%s_%s/ff_cr_tt_%s.pdf"%(channel,year,prong))
  canv8.SaveAs("plots/%s_%s/ff_cr_tt_%s.png"%(channel,year,prong))
  canv9 = TCanvas("ff_comp_tt%s"%prong,"ff_comp_tt_%s"%prong,600,400)
  ff_comp_tt.SetMarkerStyle(8)
  ff_comp_tt.SetLineColor(1)
  ff_comp_tt.GetYaxis().SetRangeUser(0.5,1.5)
  ff_comp_tt.Draw("PE")
  latex = TLatex()
  latex.SetNDC()
  latex.SetTextFont(42)
  #latex.DrawLatex(0.6, 0.8,"%s  %s"%(channel, year))
  #plot.DrawCMSLogo(canv9, "CMS", "Internal", 10, 0.045, 0.05, 1.0, '', 0.8)
  plot.DrawCMSLogo(canv9, "Private work", "(CMS data/simulation)", 10, 0.045, 0.05, 1.0, '', 0.8)
  plot.DrawTitle(canv9, titleright, 3, 0.2, 0.4)
  plot.Set(latex, NDC=None, TextFont=42, TextSize=0.05)
  latex.DrawLatex(0.15, 0.68, channel_text)
  canv9.SaveAs("plots/%s_%s/ff_comp_tt_%s.pdf"%(channel,year,prong))
  canv9.SaveAs("plots/%s_%s/ff_comp_tt_%s.png"%(channel,year,prong))
  #MC Checks
  canv10 = TCanvas("w_sr_%s"%prong,"w_sr_%s"%prong,600,400)
  w_sr.SetMarkerStyle(8)
  w_sr.SetLineColor(1)
  w_sr.GetYaxis().SetRangeUser(0.,1.)
  w_sr.Draw("PE")
  latex = TLatex()
  latex.SetNDC()
  latex.SetTextFont(42)
  #latex.DrawLatex(0.6, 0.8,"%s  %s"%(channel, year))
  #plot.DrawCMSLogo(canv10, "CMS", "Internal", 10, 0.045, 0.05, 1.0, '', 0.8)
  plot.DrawCMSLogo(canv10, "Private work", "(CMS data/simulation)", 10, 0.045, 0.05, 1.0, '', 0.8)
  plot.DrawTitle(canv10, titleright, 3, 0.2, 0.4)
  plot.Set(latex, NDC=None, TextFont=42, TextSize=0.05)
  latex.DrawLatex(0.15, 0.68, channel_text)
  canv10.SaveAs("plots/%s_%s/w_sr_%s.pdf"%(channel,year,prong))
  canv10.SaveAs("plots/%s_%s/w_sr_%s.png"%(channel,year,prong))
  canv11 = TCanvas("w_dr_%s"%prong,"w_dr_%s"%prong,600,400)
  w_dr.SetMarkerStyle(8)
  w_dr.SetLineColor(1)
  w_dr.GetYaxis().SetRangeUser(0.,1.)
  w_dr.Draw("PE")
  latex = TLatex()
  latex.SetNDC()
  latex.SetTextFont(42)
  #latex.DrawLatex(0.6, 0.8,"%s  %s"%(channel, year))
  #plot.DrawCMSLogo(canv11, "CMS", "Internal", 10, 0.045, 0.05, 1.0, '', 0.8)
  plot.DrawCMSLogo(canv11, "Private work", "(CMS data/simulation)", 10, 0.045, 0.05, 1.0, '', 0.8)
  plot.DrawTitle(canv11, titleright, 3, 0.2, 0.4)
  plot.Set(latex, NDC=None, TextFont=42, TextSize=0.05)
  latex.DrawLatex(0.15, 0.68, channel_text)
  canv11.SaveAs("plots/%s_%s/w_dr_%s.pdf"%(channel,year,prong))
  canv11.SaveAs("plots/%s_%s/w_dr_%s.png"%(channel,year,prong))
  canv12 = TCanvas("w_sr_dr_%s"%prong,"w_sr_dr_%s"%prong,600,400)
  w_sr_dr.SetMarkerStyle(8)
  w_sr_dr.SetLineColor(1)
  w_sr_dr.GetYaxis().SetRangeUser(0.,2.)
  w_sr_dr.Draw("PE")
  canv12.SaveAs("plots/%s_%s/w_sr_dr_%s.pdf"%(channel,year,prong))
  canv12.SaveAs("plots/%s_%s/w_sr_dr_%s.png"%(channel,year,prong))
  canv13 = TCanvas("w_sr_cr_%s"%prong,"w_sr_cr_%s"%prong,600,400)
  w_sr_cr.SetMarkerStyle(8)
  w_sr_cr.SetLineColor(1)
  w_sr_cr.GetYaxis().SetRangeUser(0.,2.)
  w_sr_cr.Draw("PE")
  latex = TLatex()
  latex.SetNDC()
  latex.SetTextFont(42)
  #latex.DrawLatex(0.6, 0.8,"%s  %s"%(channel, year))
  #plot.DrawCMSLogo(canv13, "CMS", "Internal", 10, 0.045, 0.05, 1.0, '', 0.8)
  plot.DrawCMSLogo(canv13, "Private work", "(CMS data/simulation)", 10, 0.045, 0.05, 1.0, '', 0.8)
  plot.DrawTitle(canv13, titleright, 3, 0.2, 0.4)
  plot.Set(latex, NDC=None, TextFont=42, TextSize=0.05)
  latex.DrawLatex(0.15, 0.68, channel_text)
  canv13.SaveAs("plots/%s_%s/w_sr_cr_%s.pdf"%(channel,year,prong))
  canv13.SaveAs("plots/%s_%s/w_sr_cr_%s.png"%(channel,year,prong))
  canv14 = TCanvas("tt_sr_%s"%prong,"tt_sr_%s"%prong,600,400)
  tt_sr.SetMarkerStyle(8)
  tt_sr.SetLineColor(1)
  tt_sr.GetYaxis().SetRangeUser(0.,1.)
  tt_sr.Draw("PE")
  latex = TLatex()
  latex.SetNDC()
  latex.SetTextFont(42)
  #latex.DrawLatex(0.6, 0.8,"%s  %s"%(channel, year))
  #plot.DrawCMSLogo(canv14, "CMS", "Internal", 10, 0.045, 0.05, 1.0, '', 0.8)
  plot.DrawCMSLogo(canv14, "Private work", "(CMS data/simulation)", 10, 0.045, 0.05, 1.0, '', 0.8)
  plot.DrawTitle(canv14, titleright, 3, 0.2, 0.4)
  plot.Set(latex, NDC=None, TextFont=42, TextSize=0.05)
  latex.DrawLatex(0.15, 0.68, channel_text)
  canv14.SaveAs("plots/%s_%s/tt_sr_%s.pdf"%(channel,year,prong))
  canv14.SaveAs("plots/%s_%s/tt_sr_%s.png"%(channel,year,prong))
  canv15 = TCanvas("tt_dr_%s"%prong,"tt_dr_%s"%prong,600,400)
  tt_dr.SetMarkerStyle(8)
  tt_dr.SetLineColor(1)
  tt_dr.GetYaxis().SetRangeUser(0.,1.)
  tt_dr.Draw("PE")
  latex = TLatex()
  latex.SetNDC()
  latex.SetTextFont(42)
  #latex.DrawLatex(0.6, 0.8,"%s  %s"%(channel, year))
  #plot.DrawCMSLogo(canv15, "CMS", "Internal", 10, 0.045, 0.05, 1.0, '', 0.8)
  plot.DrawCMSLogo(canv15, "Private work", "(CMS data/simulation)", 10, 0.045, 0.05, 1.0, '', 0.8)
  plot.DrawTitle(canv15, titleright, 3, 0.2, 0.4)
  plot.Set(latex, NDC=None, TextFont=42, TextSize=0.05)
  latex.DrawLatex(0.15, 0.68, channel_text)
  canv15.SaveAs("plots/%s_%s/tt_dr_%s.pdf"%(channel,year,prong))
  canv15.SaveAs("plots/%s_%s/tt_dr_%s.png"%(channel,year,prong))
  canv16 = TCanvas("tt_sr_dr_%s"%prong,"tt_sr_dr_%s"%prong,600,400)
  tt_sr_dr.SetMarkerStyle(8)
  tt_sr_dr.SetLineColor(1)
  tt_sr_dr.GetYaxis().SetRangeUser(0.8,1.2)
  tt_sr_dr.Draw("PE")
  latex = TLatex()
  latex.SetNDC()
  latex.SetTextFont(42)
  #latex.DrawLatex(0.6, 0.8,"%s  %s"%(channel, year))
  #plot.DrawCMSLogo(canv16, "CMS", "Internal", 10, 0.045, 0.05, 1.0, '', 0.8)
  plot.DrawCMSLogo(canv16, "Private work", "(CMS data/simulation)", 10, 0.045, 0.05, 1.0, '', 0.8)
  plot.DrawTitle(canv16, titleright, 3, 0.2, 0.4)
  plot.Set(latex, NDC=None, TextFont=42, TextSize=0.05)
  latex.DrawLatex(0.15, 0.68, channel_text)
  canv16.SaveAs("plots/%s_%s/tt_sr_dr_%s.pdf"%(channel,year,prong))
  canv16.SaveAs("plots/%s_%s/tt_sr_dr_%s.png"%(channel,year,prong))
  canv17 = TCanvas("tt_sr_cr_%s"%prong,"tt_sr_cr_%s"%prong,600,400)
  tt_sr_cr.SetMarkerStyle(8)
  tt_sr_cr.SetLineColor(1)
  tt_sr_cr.GetYaxis().SetRangeUser(0.8,1.2)
  tt_sr_cr.Draw("PE")
  latex = TLatex()
  latex.SetNDC()
  latex.SetTextFont(42)
  #latex.DrawLatex(0.6, 0.8,"%s  %s"%(channel, year))
  #plot.DrawCMSLogo(canv17, "CMS", "Internal", 10, 0.045, 0.05, 1.0, '', 0.8)
  plot.DrawCMSLogo(canv17, "Private work", "(CMS data/simulation)", 10, 0.045, 0.05, 1.0, '', 0.8)
  plot.DrawTitle(canv17, titleright, 3, 0.2, 0.4)
  plot.Set(latex, NDC=None, TextFont=42, TextSize=0.05)
  latex.DrawLatex(0.15, 0.68, channel_text)
  canv17.SaveAs("plots/%s_%s/tt_sr_cr_%s.pdf"%(channel,year,prong))
  canv17.SaveAs("plots/%s_%s/tt_sr_cr_%s.png"%(channel,year,prong))
outfile.Close()
print("Done")
