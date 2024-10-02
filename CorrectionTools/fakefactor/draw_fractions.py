import os, sys
import copy, math, pickle, numpy
from array import array
import argparse
import plotting as plot
from ROOT import gROOT, gSystem, gStyle, gRandom
from ROOT import TMath, TFile, TChain, TTree, TCut, TH1F, TH2F, THStack, TGraph, TGaxis
from ROOT import TStyle, TCanvas, TPad, TLegend, TLatex, TText, TColor, TPaveText
from ROOT import TH1, TF1, TGraph, TGraphErrors, TGraphAsymmErrors, TVirtualFitter
from ROOT import TColor
import ROOT

ROOT.gROOT.SetBatch(ROOT.kTRUE)

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

if year=="UL2018":
  lumi = 59.7
elif year=="UL2017":
  lumi = 41.5
elif year=="2018":
  lumi = 59.7
else:
  lumi = 36.3
  #if "comb" in filename:
  #  lumi = 36.3
  #elif "preVFP" in filename:
  #  lumi = 19.5
  #else:
  #  lumi = 16.8

titleright = "%s %.1f fb^{-1} (13 TeV)"%(year[2:],float(lumi))


def getRatio(hist,data,MC,QCD,bin):
    bin_MC = hist.GetBinContent(bin)
    if bin_MC<0.:bin_MC=0.
    if QCD < 0.:
        return bin_MC/MC
    else:
        return bin_MC/data


file = TFile("root/"+filename,"READ")
tau_pt = file.Get("Tau1_pt")
for prong in selections_prong:
    if channel == "mutau":
        channel_text = "#mu#tau_{h}, %s, AR"%prong
    elif channel == "etau":
        channel_text = "e#tau_{h}, %s, AR"%prong

    hist_data = tau_pt.Get("data_obs_AR_%s"%prong)
    data_integral = hist_data.Integral()
    hist_DY=tau_pt.Get("DYJetscomb_AR_%s"%prong)
    hist_DY.SetFillColor(TColor.GetColor("#f89c20"))
    #hist_DY.SetFillColor(TColor.GetColor(248, 206, 104))
    hist_W=tau_pt.Get("WJetscomb_AR_%s"%prong)
    hist_W.SetFillColor(TColor.GetColor("#e42536"))
    #hist_W.SetFillColor(TColor.GetColor(222,90,106))
    hist_TT=tau_pt.Get("TT_AR_%s"%prong)
    hist_TT.SetFillColor(TColor.GetColor("#964a8b"))
    #hist_TT.SetFillColor(TColor.GetColor(155, 152, 204))
    hist_ST=tau_pt.Get("ST_AR_%s"%prong)
    hist_ST.SetFillColor(TColor.GetColor("#832db6"))
    #hist_ST.SetFillColor(TColor.GetColor(208,240,193))
    hist_Multijet = tau_pt.Get("Multijet_AR_%s"%prong)
    hist_Multijet.SetFillColor(TColor.GetColor("#9c9ca1"))
    #hist_Multijet.SetFillColor(TColor.GetColor(250, 202, 255))
    hist_VV = tau_pt.Get("VV_AR_%s"%prong)
    hist_VV.SetFillColor(TColor.GetColor("#b9ac70"))
    #hist_VV.SetFillColor(TColor.GetColor(111,45,53))
    hist_true = tau_pt.Get("Truetau_AR_%s"%prong)
    hist_true.SetFillColor(TColor.GetColor("#92dadd"))
    #hist_true.SetFillColor(430)
    hist_MC = tau_pt.Get("MCnoQCD_AR_%s"%prong)
    for bin in range(1,8):
        data=hist_data.GetBinContent(bin)
        MC = hist_MC.GetBinContent(bin)
        QCD = hist_Multijet.GetBinContent(bin)
        """
        print "bin:",bin
        print "pt:",hist_DY.GetXaxis().GetBinCenter(bin)
        print "pt QCD:",hist_Multijet.GetXaxis().GetBinCenter(bin)
        print "data:",data
        print "DY:",hist_DY.GetBinContent(bin)/data
        print "W:",hist_W.GetBinContent(bin)/data
        print "TT:",hist_TT.GetBinContent(bin)/data
        print "QCD:",hist_Multijet.GetBinContent(bin)/data
        print "true:",hist_true.GetBinContent(bin)/data
        print "ST:",hist_ST.GetBinContent(bin)/data
        
        hist_DY.SetBinContent(bin,hist_DY.GetBinContent(bin)/data)
        hist_W.SetBinContent(bin,hist_W.GetBinContent(bin)/data)
        hist_TT.SetBinContent(bin,hist_TT.GetBinContent(bin)/data)
        hist_Multijet.SetBinContent(bin,hist_Multijet.GetBinContent(bin)/data)
        hist_true.SetBinContent(bin,hist_true.GetBinContent(bin)/data)
        hist_ST.SetBinContent(bin,hist_ST.GetBinContent(bin)/data)

        print("bin:",bin)
        print("data:",data)
        print("DY:",getRatio(hist_DY,data,MC,QCD,bin))
        print("W:",getRatio(hist_W,data,MC,QCD,bin))
        print("TT:",getRatio(hist_TT,data,MC,QCD,bin))
        print("QCD:",getRatio(hist_Multijet,data,MC,QCD,bin))
        print("true:",getRatio(hist_true,data,MC,QCD,bin))
        print("ST:",getRatio(hist_ST,data,MC,QCD,bin))
        """
        hist_DY.SetBinContent(bin,getRatio(hist_DY,data,MC,QCD,bin))
        hist_W.SetBinContent(bin,getRatio(hist_W,data,MC,QCD,bin))
        hist_TT.SetBinContent(bin,getRatio(hist_TT,data,MC,QCD,bin))
        hist_Multijet.SetBinContent(bin,getRatio(hist_Multijet,data,MC,QCD,bin))
        hist_VV.SetBinContent(bin,getRatio(hist_VV,data,MC,QCD,bin))
        hist_true.SetBinContent(bin,getRatio(hist_true,data,MC,QCD,bin))
        hist_ST.SetBinContent(bin,getRatio(hist_ST,data,MC,QCD,bin))
        
    hist_DY.GetYaxis().SetTitle("Fractions")
    stack = THStack()
    stack.Add(hist_W)
    stack.Add(hist_DY)
    stack.Add(hist_Multijet)
    stack.Add(hist_true)
    stack.Add(hist_VV)
    stack.Add(hist_ST)
    stack.Add(hist_TT)
    #save histograms in root file
    outfile = TFile("root/fractions_%s_%s_%s.root"%(channel,year,prong),'Recreate')
    hist_W.Write()
    hist_ST.Write()
    hist_VV.Write()
    hist_Multijet.Write()
    hist_DY.Write()
    hist_TT.Write()
    outfile.Close()
    canv = TCanvas(prong,prong,600,400)
    gStyle.SetOptStat(0)
    stack.Draw('HIST')
    #stack.SetTitle("Fractions AR %s"%prong)
    stack.GetXaxis().SetTitle("#tau_{h} p_{T} (GeV)")
    stack.GetYaxis().SetTitle("Fractions")
    stack.GetXaxis().SetTitleSize(0.05)
    stack.GetYaxis().SetTitleSize(0.05)
    stack.GetYaxis().SetTitleOffset(0.95)
    stack.GetXaxis().SetLabelSize(0.05)
    stack.GetYaxis().SetLabelSize(0.05)
    canv.SetBottomMargin(0.12)
    #stack.SetMinimum(100.)
    #canv.SetLogy()
    leg = TLegend(0.65, 0.65, 0.89, 0.85)#0.15 0.12 0.3 0.32
    leg.SetNColumns(2)
    leg.AddEntry(hist_TT,"t#bar{t}","F")
    leg.AddEntry(hist_ST,"ST","F")
    leg.AddEntry(hist_VV,"VV","F")
    leg.AddEntry(hist_true,"true #tau","F")
    leg.AddEntry(hist_Multijet,"QCD","F")
    leg.AddEntry(hist_DY,"Z+jets","F")
    leg.AddEntry(hist_W,"W+jets","F")
    leg.Draw("SAME")
    latex = TLatex()
    plot.DrawCMSLogo(canv, "Private work", "(CMS data/simulation)", 10, 0.045, 0.05, 1.0, '', 0.8)
    #plot.DrawCMSLogo(canv, "CMS", "Internal", 10, 0.045, 0.05, 1.0, '', 0.8)
    plot.DrawTitle(canv, titleright, 3, 0.2, 0.5)
    plot.Set(latex, NDC=None, TextFont=42, TextSize=0.05)
    latex.DrawLatex(0.15, 0.68, channel_text)
    #canv.SetLogx()
    canv.SaveAs(outdir+"/%s_%s/fractions_%s.pdf"%(channel,year,prong))
    canv.SaveAs(outdir+"/%s_%s/fractions_%s.png"%(channel,year,prong))
    canv.SaveAs(outdir+"/thesis/ff_fractions_%s_%s_%s.pdf"%(prong,channel,year))
###save fractions for TT DR

for prong in selections_prong:
    if channel == "mutau":
        channel_text = "#mu#tau_{h}, %s, AR"%prong
    elif channel == "etau":
        channel_text = "e#tau_{h}, %s, AR"%prong
    hist_data = tau_pt.Get("data_obs_ARTT_%s"%prong)
    data_integral = hist_data.Integral()
    hist_DY=tau_pt.Get("DYJetscomb_ARTT_%s"%prong)
    hist_DY.SetFillColor(TColor.GetColor(248, 206, 104))
    hist_W=tau_pt.Get("WJetscomb_ARTT_%s"%prong)
    hist_W.SetFillColor(TColor.GetColor(222,90,106))
    hist_TT=tau_pt.Get("TT_ARTT_%s"%prong)
    hist_TT.SetFillColor(TColor.GetColor(155, 152, 204))
    hist_ST=tau_pt.Get("ST_ARTT_%s"%prong)
    hist_ST.SetFillColor(TColor.GetColor(208,240,193))
    hist_Multijet = tau_pt.Get("Multijet_ARTT_%s"%prong)
    hist_Multijet.SetFillColor(TColor.GetColor(250, 202, 255))
    hist_VV = tau_pt.Get("VV_ARTT_%s"%prong)
    hist_VV.SetFillColor(TColor.GetColor(111,45,53))
    hist_true = tau_pt.Get("Truetau_ARTT_%s"%prong)
    hist_true.SetFillColor(430)
    hist_MC = tau_pt.Get("MCnoQCD_ARTT_%s"%prong)
    for bin in range(1,14):
        data=hist_data.GetBinContent(bin)
        MC = hist_MC.GetBinContent(bin)
        QCD = hist_Multijet.GetBinContent(bin)
        hist_DY.SetBinContent(bin,getRatio(hist_DY,data,MC,QCD,bin))
        hist_W.SetBinContent(bin,getRatio(hist_W,data,MC,QCD,bin))
        hist_TT.SetBinContent(bin,getRatio(hist_TT,data,MC,QCD,bin))
        hist_VV.SetBinContent(bin,getRatio(hist_VV,data,MC,QCD,bin))
        hist_Multijet.SetBinContent(bin,getRatio(hist_Multijet,data,MC,QCD,bin))
        hist_true.SetBinContent(bin,getRatio(hist_true,data,MC,QCD,bin))
        hist_ST.SetBinContent(bin,getRatio(hist_ST,data,MC,QCD,bin))
    hist_DY.GetYaxis().SetTitle("Fractions")
    stack = THStack()
    stack.Add(hist_W)
    stack.Add(hist_DY)
    stack.Add(hist_Multijet)
    stack.Add(hist_true)
    stack.Add(hist_VV)
    stack.Add(hist_ST)
    stack.Add(hist_TT)
    #save histograms in root file
    outfile = TFile("root/fractions_TTDR_%s_%s_%s.root"%(channel,year,prong),'Recreate')
    hist_W.Write()
    hist_Multijet.Write()
    hist_DY.Write()
    hist_TT.Write()
    hist_ST.Write()
    outfile.Close()
    canv = TCanvas(prong,prong,600,400)
    gStyle.SetOptStat(0)
    stack.Draw('HIST')
    #stack.SetTitle("Fractions AR %s"%prong)
    stack.GetXaxis().SetTitle("#tau_{h} p_{T}")
    stack.GetYaxis().SetTitle("Fractions")
    leg = TLegend(0.75, 0.55, 0.85, 0.85)
    leg.AddEntry(hist_TT,"TT","F")
    leg.AddEntry(hist_ST,"ST","F")
    leg.AddEntry(hist_VV,"VV","F")
    leg.AddEntry(hist_true,"true #tau","F")
    leg.AddEntry(hist_Multijet,"QCD","F")
    leg.AddEntry(hist_DY,"DYJets","F")
    leg.AddEntry(hist_W,"WJets","F")
    leg.Draw("SAME")
    latex = TLatex()
    plot.DrawCMSLogo(canv, "Private work", "(CMS data/simulation)", 10, 0.045, 0.05, 1.0, '', 0.8)
    #plot.DrawCMSLogo(canv, "CMS", "Internal", 10, 0.045, 0.05, 1.0, '', 0.8)
    plot.DrawTitle(canv, titleright, 3, 0.2, 0.5)
    plot.Set(latex, NDC=None, TextFont=42, TextSize=0.05)
    latex.DrawLatex(0.15, 0.68, channel_text)
    canv.SetLogx()
    canv.SaveAs(outdir+"/%s_%s/fractions_TTDR_%s.pdf"%(channel,year,prong))



###save fractions for QCD DR

for prong in selections_prong:
    if channel == "mutau":
        channel_text = "#mu#tau_{h}, %s, AR"%prong
    elif channel == "etau":
        channel_text = "e#tau_{h}, %s, AR"%prong
    hist_data = tau_pt.Get("data_obs_ARQCD_%s"%prong)
    data_integral = hist_data.Integral()
    hist_DY=tau_pt.Get("DYJetscomb_ARQCD_%s"%prong)
    hist_DY.SetFillColor(TColor.GetColor(248, 206, 104))
    hist_W=tau_pt.Get("WJetscomb_ARQCD_%s"%prong)
    hist_W.SetFillColor(TColor.GetColor(222,90,106))
    hist_TT=tau_pt.Get("TT_ARQCD_%s"%prong)
    hist_TT.SetFillColor(TColor.GetColor(155, 152, 204))
    hist_ST=tau_pt.Get("ST_ARQCD_%s"%prong)
    hist_ST.SetFillColor(TColor.GetColor(208,240,193))
    hist_Multijet = tau_pt.Get("Multijet_ARQCD_%s"%prong)
    hist_Multijet.SetFillColor(TColor.GetColor(250, 202, 255))
    hist_VV = tau_pt.Get("VV_ARQCD_%s"%prong)
    hist_VV.SetFillColor(TColor.GetColor(111,45,53))
    hist_true = tau_pt.Get("Truetau_ARQCD_%s"%prong)
    hist_true.SetFillColor(430)
    hist_MC = tau_pt.Get("MCnoQCD_ARQCD_%s"%prong)
    for bin in range(1,14):
        data=hist_data.GetBinContent(bin)
        MC = hist_MC.GetBinContent(bin)
        QCD = hist_Multijet.GetBinContent(bin)
        hist_DY.SetBinContent(bin,getRatio(hist_DY,data,MC,QCD,bin))
        hist_W.SetBinContent(bin,getRatio(hist_W,data,MC,QCD,bin))
        hist_TT.SetBinContent(bin,getRatio(hist_TT,data,MC,QCD,bin))
        hist_VV.SetBinContent(bin,getRatio(hist_VV,data,MC,QCD,bin))
        hist_Multijet.SetBinContent(bin,getRatio(hist_Multijet,data,MC,QCD,bin))
        hist_true.SetBinContent(bin,getRatio(hist_true,data,MC,QCD,bin))
        hist_ST.SetBinContent(bin,getRatio(hist_ST,data,MC,QCD,bin))
    hist_DY.GetYaxis().SetTitle("Fractions")
    stack = THStack()
    stack.Add(hist_W)
    stack.Add(hist_DY)
    stack.Add(hist_Multijet)
    stack.Add(hist_true)
    stack.Add(hist_VV)
    stack.Add(hist_ST)
    stack.Add(hist_TT)
    #save histograms in root file
    outfile = TFile("root/fractions_QCDDR_%s_%s_%s.root"%(channel,year,prong),'Recreate')
    hist_W.Write()
    hist_Multijet.Write()
    hist_DY.Write()
    hist_TT.Write()
    hist_ST.Write()
    hist_VV.Write()
    outfile.Close()
    canv = TCanvas(prong,prong,600,400)
    gStyle.SetOptStat(0)
    stack.Draw('HIST')
    #stack.SetTitle("Fractions AR %s"%prong)
    stack.GetXaxis().SetTitle("#tau_{h} p_{T}")
    stack.GetYaxis().SetTitle("Fractions")
    leg = TLegend(0.75, 0.55, 0.85, 0.85)
    leg.AddEntry(hist_TT,"TT","F")
    leg.AddEntry(hist_ST,"ST","F")
    leg.AddEntry(hist_VV,"VV","F")
    leg.AddEntry(hist_true,"true #tau","F")
    leg.AddEntry(hist_Multijet,"QCD","F")
    leg.AddEntry(hist_DY,"DYJets","F")
    leg.AddEntry(hist_W,"WJets","F")
    leg.Draw("SAME")
    latex = TLatex()
    plot.DrawCMSLogo(canv, "Private work", "(CMS data/simulation)", 10, 0.045, 0.05, 1.0, '', 0.8)
    #plot.DrawCMSLogo(canv, "CMS", "Internal", 10, 0.045, 0.05, 1.0, '', 0.8)
    plot.DrawTitle(canv, titleright, 3, 0.2, 0.5)
    plot.Set(latex, NDC=None, TextFont=42, TextSize=0.05)
    latex.DrawLatex(0.15, 0.68, channel_text)
    canv.SetLogx()
    canv.SaveAs(outdir+"/%s_%s/fractions_QCDDR_%s.pdf"%(channel,year,prong))


####QCD Scale Up

for prong in selections_prong:
    if channel == "mutau":
        channel_text = "#mu#tau_{h}, %s, AR"%prong
    elif channel == "etau":
        channel_text = "e#tau_{h}, %s, AR"%prong
    hist_data = tau_pt.Get("data_obs_ARQCDScaleUp_%s"%prong)
    data_integral = hist_data.Integral()
    hist_DY=tau_pt.Get("DYJetscomb_ARQCDScaleUp_%s"%prong)
    hist_DY.SetFillColor(TColor.GetColor(248, 206, 104))
    hist_W=tau_pt.Get("WJetscomb_ARQCDScaleUp_%s"%prong)
    hist_W.SetFillColor(TColor.GetColor(222,90,106))
    hist_TT=tau_pt.Get("TT_ARQCDScaleUp_%s"%prong)
    hist_TT.SetFillColor(TColor.GetColor(155, 152, 204))
    hist_ST=tau_pt.Get("ST_ARQCDScaleUp_%s"%prong)
    hist_ST.SetFillColor(TColor.GetColor(208,240,193))
    hist_Multijet = tau_pt.Get("Multijet_ARQCDScaleUp_%s"%prong)
    hist_Multijet.SetFillColor(TColor.GetColor(250, 202, 255))
    hist_VV = tau_pt.Get("VV_ARQCDScaleUp_%s"%prong)
    hist_VV.SetFillColor(TColor.GetColor(111,45,53))
    hist_true = tau_pt.Get("Truetau_ARQCDScaleUp_%s"%prong)
    hist_true.SetFillColor(430)
    hist_MC = tau_pt.Get("MCnoQCD_ARQCDScaleUp_%s"%prong)
    for bin in range(1,14):
        data=hist_data.GetBinContent(bin)
        MC = hist_MC.GetBinContent(bin)
        QCD = hist_Multijet.GetBinContent(bin)  
        hist_DY.SetBinContent(bin,getRatio(hist_DY,data,MC,QCD,bin))
        hist_W.SetBinContent(bin,getRatio(hist_W,data,MC,QCD,bin))
        hist_TT.SetBinContent(bin,getRatio(hist_TT,data,MC,QCD,bin))
        hist_VV.SetBinContent(bin,getRatio(hist_VV,data,MC,QCD,bin))
        hist_Multijet.SetBinContent(bin,getRatio(hist_Multijet,data,MC,QCD,bin))
        hist_true.SetBinContent(bin,getRatio(hist_true,data,MC,QCD,bin))
        hist_ST.SetBinContent(bin,getRatio(hist_ST,data,MC,QCD,bin))
    hist_DY.GetYaxis().SetTitle("Fractions")
    stack = THStack()
    stack.Add(hist_W)
    stack.Add(hist_DY)
    stack.Add(hist_Multijet)
    stack.Add(hist_true)
    stack.Add(hist_VV)
    stack.Add(hist_ST)
    stack.Add(hist_TT)
    #save histograms in root file
    outfile = TFile("root/fractions_QCDScaleUp_%s_%s_%s.root"%(channel,year,prong),'Recreate')
    hist_W.Write()
    hist_Multijet.Write()
    hist_DY.Write()
    hist_TT.Write()
    hist_ST.Write()
    outfile.Close()
    canv = TCanvas(prong,prong,600,400)
    gStyle.SetOptStat(0)
    stack.Draw('HIST')
    #stack.SetTitle("Fractions AR %s"%prong)
    stack.GetXaxis().SetTitle("#tau_{h} p_{T}")
    stack.GetYaxis().SetTitle("Fractions")
    leg = TLegend(0.75, 0.55, 0.85, 0.85)
    leg.AddEntry(hist_TT,"TT","F")
    leg.AddEntry(hist_ST,"ST","F")
    leg.AddEntry(hist_VV,"VV","F")
    leg.AddEntry(hist_true,"true #tau","F")
    leg.AddEntry(hist_Multijet,"QCD","F")
    leg.AddEntry(hist_DY,"DYJets","F")
    leg.AddEntry(hist_W,"WJets","F")
    leg.Draw("SAME")
    latex = TLatex()
    plot.DrawCMSLogo(canv, "Private work", "(CMS data/simulation)", 10, 0.045, 0.05, 1.0, '', 0.8)
    #plot.DrawCMSLogo(canv, "CMS", "Internal", 10, 0.045, 0.05, 1.0, '', 0.8)
    plot.DrawTitle(canv, titleright, 3, 0.2, 0.5)
    plot.Set(latex, NDC=None, TextFont=42, TextSize=0.05)
    latex.DrawLatex(0.15, 0.68, channel_text+", QCD Scale up")
    canv.SetLogx()
    canv.SaveAs(outdir+"/%s_%s/fractions_QCDScaleUp_%s.pdf"%(channel,year,prong))
    canv.SaveAs(outdir+"/%s_%s/fractions_QCDScaleUp_%s.png"%(channel,year,prong))


####QCD Scale Down

for prong in selections_prong:
    if channel == "mutau":
        channel_text = "#mu#tau_{h}, %s, AR"%prong
    elif channel == "etau":
        channel_text = "e#tau_{h}, %s, AR"%prong
    hist_data = tau_pt.Get("data_obs_ARQCDScaleDown_%s"%prong)
    data_integral = hist_data.Integral()
    hist_DY=tau_pt.Get("DYJetscomb_ARQCDScaleDown_%s"%prong)
    hist_DY.SetFillColor(TColor.GetColor(248, 206, 104))
    hist_W=tau_pt.Get("WJetscomb_ARQCDScaleDown_%s"%prong)
    hist_W.SetFillColor(TColor.GetColor(222,90,106))
    hist_TT=tau_pt.Get("TT_ARQCDScaleDown_%s"%prong)
    hist_TT.SetFillColor(TColor.GetColor(155, 152, 204))
    hist_ST=tau_pt.Get("ST_ARQCDScaleDown_%s"%prong)
    hist_ST.SetFillColor(TColor.GetColor(208,240,193))
    hist_Multijet = tau_pt.Get("Multijet_ARQCDScaleDown_%s"%prong)
    hist_Multijet.SetFillColor(TColor.GetColor(250, 202, 255))
    hist_VV = tau_pt.Get("VV_ARQCDScaleDown_%s"%prong)
    hist_VV.SetFillColor(TColor.GetColor(111,45,53))
    hist_true = tau_pt.Get("Truetau_ARQCDScaleDown_%s"%prong)
    hist_true.SetFillColor(430)
    hist_MC = tau_pt.Get("MCnoQCD_ARQCDScaleDown_%s"%prong)
    for bin in range(1,14):
        data=hist_data.GetBinContent(bin)
        MC = hist_MC.GetBinContent(bin)
        QCD = hist_Multijet.GetBinContent(bin)
        hist_DY.SetBinContent(bin,getRatio(hist_DY,data,MC,QCD,bin))
        hist_W.SetBinContent(bin,getRatio(hist_W,data,MC,QCD,bin))
        hist_TT.SetBinContent(bin,getRatio(hist_TT,data,MC,QCD,bin))
        hist_VV.SetBinContent(bin,getRatio(hist_VV,data,MC,QCD,bin))
        hist_Multijet.SetBinContent(bin,getRatio(hist_Multijet,data,MC,QCD,bin))
        hist_true.SetBinContent(bin,getRatio(hist_true,data,MC,QCD,bin))
        hist_ST.SetBinContent(bin,getRatio(hist_ST,data,MC,QCD,bin))
    hist_DY.GetYaxis().SetTitle("Fractions")
    stack = THStack()
    stack.Add(hist_W)
    stack.Add(hist_DY)
    stack.Add(hist_Multijet)
    stack.Add(hist_true)
    stack.Add(hist_VV)
    stack.Add(hist_ST)
    stack.Add(hist_TT)
    #save histograms in root file
    outfile = TFile("root/fractions_QCDScaleDown_%s_%s_%s.root"%(channel,year,prong),'Recreate')
    hist_W.Write()
    hist_Multijet.Write()
    hist_DY.Write()
    hist_TT.Write()
    hist_ST.Write()
    outfile.Close()
    canv = TCanvas(prong,prong,600,400)
    gStyle.SetOptStat(0)
    stack.Draw('HIST')
    #stack.SetTitle("Fractions AR %s"%prong)
    stack.GetXaxis().SetTitle("#tau_{h} p_{T}")
    stack.GetYaxis().SetTitle("Fractions")
    leg = TLegend(0.75, 0.55, 0.85, 0.85)
    leg.AddEntry(hist_TT,"TT","F")
    leg.AddEntry(hist_ST,"ST","F")
    leg.AddEntry(hist_VV,"VV","F")
    leg.AddEntry(hist_true,"true #tau","F")
    leg.AddEntry(hist_Multijet,"QCD","F")
    leg.AddEntry(hist_DY,"DYJets","F")
    leg.AddEntry(hist_W,"WJets","F")
    leg.Draw("SAME")
    latex = TLatex()
    plot.DrawCMSLogo(canv, "Private work", "(CMS data/simulation)", 10, 0.045, 0.05, 1.0, '', 0.8)
    #plot.DrawCMSLogo(canv, "CMS", "Internal", 10, 0.045, 0.05, 1.0, '', 0.8)
    plot.DrawTitle(canv, titleright, 3, 0.2, 0.5)
    plot.Set(latex, NDC=None, TextFont=42, TextSize=0.05)
    latex.DrawLatex(0.15, 0.68, channel_text+", QCD Scale down")
    canv.SetLogx()
    canv.SaveAs(outdir+"/%s_%s/fractions_QCDScaleDown_%s.pdf"%(channel,year,prong))
    canv.SaveAs(outdir+"/%s_%s/fractions_QCDScaleDown_%s.png"%(channel,year,prong))
"""
##### print

for prong in selections_prong:
    print("prong:",prong)
    hist_data = tau_pt.Get("data_obs_AR_%s"%prong)
    hist_Multijet = tau_pt.Get("Multijet_AR_%s"%prong)
    hist_Multijet_up = tau_pt.Get("Multijet_ARQCDScaleUp_%s"%prong)
    hist_Multijet_down = tau_pt.Get("Multijet_ARQCDScaleDown_%s"%prong)
    hist_TT = tau_pt.Get("TT_AR_%s"%prong)
    hist_TT_up = tau_pt.Get("TT_ARQCDScaleUp_%s"%prong)
    hist_TT_down = tau_pt.Get("TT_ARQCDScaleDown_%s"%prong)
    hist_W = tau_pt.Get("WJetscomb_AR_%s"%prong)
    hist_W_up = tau_pt.Get("WJetscomb_ARQCDScaleUp_%s"%prong)
    hist_W_down = tau_pt.Get("WJetscomb_ARQCDScaleDown_%s"%prong)
    hist_MC = tau_pt.Get("MCnoQCD_AR_%s"%prong)
    hist_MC_up = tau_pt.Get("MCnoQCD_ARQCDScaleUp_%s"%prong)
    hist_MC_down = tau_pt.Get("MCnoQCD_ARQCDScaleDown_%s"%prong)
    for bin in range(1,14):
        data=hist_data.GetBinContent(bin)
        MC = hist_MC.GetBinContent(bin)
        MC_up = hist_MC_up.GetBinContent(bin)
        MC_down = hist_MC_down.GetBinContent(bin)
        QCD = hist_Multijet.GetBinContent(bin)
        QCD_up = hist_Multijet_up.GetBinContent(bin)
        QCD_down = hist_Multijet_down.GetBinContent(bin)
        TT = hist_TT.GetBinContent(bin)
        TT_up = hist_TT_up.GetBinContent(bin)
        TT_down = hist_TT_down.GetBinContent(bin)
        W = hist_W.GetBinContent(bin)
        W_up = hist_W_up.GetBinContent(bin)
        W_down = hist_W_down.GetBinContent(bin)
        print("bin:",bin, "taupt:",hist_data.GetXaxis().GetBinCenter(bin),"QCD contribution.",round(getRatio(hist_Multijet,data,MC,QCD,bin),4),"up",round(getRatio(hist_Multijet_up,data,MC_up,QCD_up,bin),4),"down",round(getRatio(hist_Multijet_down,data,MC_down,QCD_down,bin),4))
        print("bin:",bin, "taupt:",hist_data.GetXaxis().GetBinCenter(bin),"TT contribution.",round(getRatio(hist_TT,data,MC,TT,bin),4),"up",round(getRatio(hist_TT_up,data,MC_up,TT_up,bin),4),"down",round(getRatio(hist_TT_down,data,MC_down,TT_down,bin),4))
        print("bin:",bin, "taupt:",hist_data.GetXaxis().GetBinCenter(bin),"W contribution.",round(getRatio(hist_W,data,MC,W,bin),4),"up",round(getRatio(hist_W_up,data,MC_up,W_up,bin),4),"down",round(getRatio(hist_W_down,data,MC_down,W_down,bin),4))
"""    
