import ROOT
from ROOT import TFile, TH2D, TCanvas, gStyle
import correctionlib
import os
from argparse import ArgumentParser
import numpy as np
path_root = '/pnfs/psi.ch/cms/trivcat/store/user/pbaertsc/bbh/samples_UL2018/SingleMuon_Run2018ABCD.root'
      
       


if __name__=="__main__":
    mu_pt = [25., 26., 27., 28., 29., 30., 31., 32., 33., 34., 35., 40., 45., 50. ,75., 100., 200.]
    mu_pt_low = [25., 26., 27., 28., 29., 30., 31., 32., 33., 34., 35.]
    mu_pt_high = [35., 40., 45., 50. ,75., 100., 200.]
    mutau_pt = [21., 22., 23., 24., 25., 26., 27., 28., 29., 30., 35., 40., 45., 50. ,75., 100., 200.]
    mutau_pt_low = [21., 22., 23., 24., 25., 26., 27., 28., 29., 30.]
    mutau_pt_high = [30., 35., 40., 45., 50. ,75., 100., 200.]
    mu_eta =  [0., 0.9, 1.2, 2.1, 2.4]
    mutau_eta = [0., 0.9, 1.2, 2.1]
    
    #onlySL
    hist_onlySL = TH2D("Events_onlySL_UL2018","Events onlySL UL2018",len(mu_pt)-1,np.array(mu_pt),len(mu_eta)-1,np.array(mu_eta))
    hist_onlySL_low = TH2D("Events_onlySL_UL2018_low","Events onlySL UL2018 low pt bins",len(mu_pt_low)-1,np.array(mu_pt_low),len(mu_eta)-1,np.array(mu_eta))
    hist_onlySL_high = TH2D("Events_onlySL_UL2018_high","Events onlySL UL2018 high pt bins",len(mu_pt_high)-1,np.array(mu_pt_high),len(mu_eta)-1,np.array(mu_eta))
    hist_onlySL.GetXaxis().SetTitle("#mu p_{T}")
    hist_onlySL.GetYaxis().SetTitle("#mu |#eta|")
    hist_onlySL_low.GetXaxis().SetTitle("#mu p_{T}")
    hist_onlySL_low.GetYaxis().SetTitle("#mu |#eta|")
    hist_onlySL_high.GetXaxis().SetTitle("#mu p_{T}")
    hist_onlySL_high.GetYaxis().SetTitle("#mu |#eta|")
    #onlySL
    hist_onlyCross = TH2D("Events_onlyCross_UL2018","Events onlyCross UL2018",len(mutau_pt)-1,np.array(mutau_pt),len(mutau_eta)-1,np.array(mutau_eta))
    hist_onlyCross_low = TH2D("Events_onlyCross_UL2018_low","Events onlyCross UL2018 low pt bins",len(mutau_pt_low)-1,np.array(mutau_pt_low),len(mutau_eta)-1,np.array(mutau_eta))
    hist_onlyCross_high = TH2D("Events_onlyCross_UL2018_high","Events onlyCross UL2018 high pt bins",len(mutau_pt_high)-1,np.array(mutau_pt_high),len(mutau_eta)-1,np.array(mutau_eta))
    hist_onlyCross.GetXaxis().SetTitle("#mu p_{T}")
    hist_onlyCross.GetYaxis().SetTitle("#mu |#eta|")
    hist_onlyCross_low.GetXaxis().SetTitle("#mu p_{T}")
    hist_onlyCross_low.GetYaxis().SetTitle("#mu |#eta|")
    hist_onlyCross_high.GetXaxis().SetTitle("#mu p_{T}")
    hist_onlyCross_high.GetYaxis().SetTitle("#mu |#eta|")
    #both
    hist_both = TH2D("Events_both_UL2018","Events both UL2018",len(mu_pt)-1,np.array(mu_pt),len(mutau_eta)-1,np.array(mutau_eta))
    hist_both_low = TH2D("Events_both_UL2018_low","Events both UL2018 low pt bins",len(mu_pt_low)-1,np.array(mu_pt_low),len(mutau_eta)-1,np.array(mutau_eta))
    hist_both_high = TH2D("Events_both_UL2018_high","Events both UL2018 high pt bins",len(mu_pt_high)-1,np.array(mu_pt_high),len(mutau_eta)-1,np.array(mutau_eta))
    hist_both.GetXaxis().SetTitle("#mu p_{T}")
    hist_both.GetYaxis().SetTitle("#mu |#eta|")
    hist_both_low.GetXaxis().SetTitle("#mu p_{T}")
    hist_both_low.GetYaxis().SetTitle("#mu |#eta|")
    hist_both_high.GetXaxis().SetTitle("#mu p_{T}")
    hist_both_high.GetYaxis().SetTitle("#mu |#eta|")



    file = TFile(path_root,'READ')
    obj = file.Get("tree")
    nev = obj.GetEntriesFast()
    #nev = 1000000
    print("total events:",nev)
    for event in range(0, nev):
        if event%100000==0:
            print("event:",event)
        obj.GetEntry(event)
        Mu1_pt = obj.Mu1_pt
        Mu1_eta = obj.Mu1_eta
        if obj.MuTrigger_fired == True and obj.MuTauTrigger_fired == False:
            hist_onlySL.Fill(Mu1_pt,Mu1_eta)
            hist_onlySL_low.Fill(Mu1_pt,Mu1_eta)
            hist_onlySL_high.Fill(Mu1_pt,Mu1_eta)
        elif obj.MuTrigger_fired == False and obj.MuTauTrigger_fired == True:
            hist_onlyCross.Fill(Mu1_pt,Mu1_eta)
            hist_onlyCross_low.Fill(Mu1_pt,Mu1_eta)
            hist_onlyCross_high.Fill(Mu1_pt,Mu1_eta)
        elif obj.MuTrigger_fired == True and obj.MuTauTrigger_fired == True:
            hist_both.Fill(Mu1_pt,Mu1_eta)
            hist_both_low.Fill(Mu1_pt,Mu1_eta)
            hist_both_high.Fill(Mu1_pt,Mu1_eta)
    gStyle.SetOptStat(0)
    #gStyle.SetPaintTextFormat(".3f")
    canv1 = TCanvas("Events_onlySL_UL2018","Events onlySL UL2018")
    hist_onlySL.Draw("COLZTEXT45")
    canv1.SaveAs("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/triggerSF/plots/check/Events_onlySL_UL2018.pdf")
    canv2 = TCanvas("Events_onlySL_UL2018_low","Events onlySL UL2018")
    hist_onlySL_low.Draw("COLZTEXT45")
    canv2.SaveAs("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/triggerSF/plots/check/Events_onlySL_UL2018_low.pdf")
    canv3 = TCanvas("Events_onlySL_UL2018_high","Events onlySL UL2018")
    hist_onlySL_high.Draw("COLZTEXT45")
    canv3.SaveAs("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/triggerSF/plots/check/Events_onlySL_UL2018_high.pdf")
    canv4 = TCanvas("Events_onlyCross_UL2018","Events onlyCross UL2018")
    hist_onlyCross.Draw("COLZTEXT45")
    canv4.SaveAs("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/triggerSF/plots/check/Events_onlyCross_UL2018.pdf")
    canv5 = TCanvas("Events_onlyCross_UL2018_low","Events onlyCross UL2018")
    hist_onlyCross_low.Draw("COLZTEXT45")
    canv5.SaveAs("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/triggerSF/plots/check/Events_onlyCross_UL2018_low.pdf")
    canv6 = TCanvas("Events_onlyCross_UL2018_high","Events onlyCross UL2018")
    hist_onlyCross_high.Draw("COLZTEXT45")
    canv6.SaveAs("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/triggerSF/plots/check/Events_onlyCross_UL2018_high.pdf")
    canv7 = TCanvas("Events_both_UL2018","Events both UL2018")
    hist_both.Draw("COLZTEXT45")
    canv7.SaveAs("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/triggerSF/plots/check/Events_both_UL2018.pdf")
    canv8 = TCanvas("Events_both_UL2018_low","Events both UL2018")
    hist_both_low.Draw("COLZTEXT45")
    canv8.SaveAs("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/triggerSF/plots/check/Events_both_UL2018_low.pdf")
    canv9 = TCanvas("Events_both_UL2018_high","Events both UL2018")
    hist_both_high.Draw("COLZTEXT45")
    canv9.SaveAs("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/triggerSF/plots/check/Events_both_UL2018_high.pdf")
    file.Close()

