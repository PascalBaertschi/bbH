import ROOT
from ROOT import TFile, TH2D, TCanvas, gStyle
import correctionlib
import os
from argparse import ArgumentParser
import numpy as np

path_root = '/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/EIsoSF/root/'

class EIsoSFs:

    def __init__(self,year,VFPtag):
        self.year = year
        self.VFPtag = VFPtag
        e_data_file = TFile('%sEIsoEff_UL%s%s_data_Fits_dielectron_mass_pt_eta_bins.root'%(path_root,year,VFPtag),'READ')
        self.e_data_hist = e_data_file.Get("dielectron_mass_pt_eta_bins")
        self.e_data_hist.SetDirectory(0)
        e_data_file.Close()
        e_mc_file = TFile('%sEIsoEff_UL%s%s_mc_Fits_dielectron_mass_pt_eta_bins.root'%(path_root,year,VFPtag),'READ')
        self.e_mc_hist = e_mc_file.Get("dielectron_mass_pt_eta_bins")
        self.e_mc_hist.SetDirectory(0)
        e_mc_file.Close()
        

    def getBinContent(self,hist,pt,eta):
        low_pt = hist.GetXaxis().GetBinCenter(1)
        high_pt = hist.GetXaxis().GetBinCenter(hist.GetNbinsX())
        high_eta = hist.GetYaxis().GetBinCenter(hist.GetNbinsY())
        if pt<low_pt: pt = low_pt
        if pt>high_pt: pt = high_pt
        if abs(eta)>high_eta: eta=high_eta
        return [hist.GetBinContent(hist.GetXaxis().FindBin(pt),hist.GetYaxis().FindBin(abs(eta))),hist.GetBinError(hist.GetXaxis().FindBin(pt),hist.GetYaxis().FindBin(abs(eta)))]

    def getEIsoEff(self,pt,eta):
        sl_eff_data = self.getBinContent(self.e_data_hist,pt,eta)
        sl_eff_mc = self.getBinContent(self.e_mc_hist,pt,eta)
        return [sl_eff_data[0],sl_eff_mc[0],sl_eff_data[1],sl_eff_mc[1]]


    def getEIsoSF(self,lep_pt,lep_eta):
        EIsoEff = self.getEIsoEff(lep_pt,abs(lep_eta))
        num = EIsoEff[0]
        den = EIsoEff[1]
        return num/den

    
    
if __name__=="__main__":
    parser = ArgumentParser()
    parser.add_argument('-y', '--year',    dest='year', choices=[2016,2017,2018], type=int, default=2018, action='store')
    parser.add_argument('-p', '--preVFP',  dest='preVFP', action='store_const', const="_preVFP",default="")
    parser.add_argument('-r', '--realm', dest='realm', action='store',default="")
    args = parser.parse_args()
    realm = args.realm
    year = args.year
    VFPtag = args.preVFP
    ROOT.gROOT.SetBatch(ROOT.kTRUE)
    if year!=2016:
        e_pt = [33., 34., 35., 36., 37., 38., 39., 40., 45., 50. ,75., 100., 200.]
        e_pt_low = [33., 34., 35., 36., 37., 38., 39., 40.]
        e_pt_high = [40., 45., 50. ,75., 100., 200.]
    else:
        e_pt = [26., 27., 28., 29., 30., 31., 32., 33., 34., 35., 36., 37., 38., 39., 40., 45., 50. ,75., 100., 200.]
        e_pt_low = [26., 27., 28., 29., 30., 31., 32., 33., 34., 35., 36., 37., 38., 39., 40.]
        e_pt_high = [40., 45., 50. ,75., 100., 200.]
    e_eta = [0., 0.8, 1.444, 1.566, 2., 2.1]
    EIsoSFs = EIsoSFs(year,VFPtag)

    lep_pt = e_pt
    lep_eta = e_eta
    lep_pt_low = e_pt_low
    lep_pt_high = e_pt_high
    Nbinsx = len(lep_pt)-1
    Nbinsy = len(lep_eta)-1
    Nbinsx_low = len(lep_pt_low)-1
    Nbinsx_high = len(lep_pt_high)-1

    if realm=="":
        outfile = TFile("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/EIsoSF/root/EIsoSF_UL%s%s.root"%(year,VFPtag),"RECREATE")
    canv = TCanvas("EIsoSF_UL%s%s"%(year,VFPtag),"e iso SF UL%s%s"%(year,VFPtag))
    hist = TH2D("EIsoSF_UL%s%s"%(year,VFPtag),"e iso SF UL%s%s"%(year,VFPtag),Nbinsx,np.array(lep_pt),Nbinsy,np.array(lep_eta))
    hist_low = TH2D("EIsoSF_UL%s%s_low"%(year,VFPtag),"e iso SF UL%s%s"%(year,VFPtag),Nbinsx_low,np.array(lep_pt_low),Nbinsy,np.array(lep_eta))
    hist_high = TH2D("EIsoSF_UL%s%s_high"%(year,VFPtag),"e iso SF UL%s%s"%(year,VFPtag),Nbinsx_high,np.array(lep_pt_high),Nbinsy,np.array(lep_eta))
    gStyle.SetOptStat(0)
    for i,pt in enumerate(lep_pt[:-1]):
        pt = pt + 0.5
        i = i+1
        for j,eta in enumerate(lep_eta[:-1]):
            eta = eta + 0.05
            j = j+1
            SF = EIsoSFs.getEIsoSF(pt,eta)
            if eta>1.444 and eta<1.566:
                SF = 1. #gap excluded in analysis
            hist.SetBinContent(i,j,SF)
    for i,pt in enumerate(lep_pt_low[:-1]):
        pt = pt + 0.5
        i = i+1
        for j,eta in enumerate(lep_eta[:-1]):
            eta = eta + 0.05
            j = j+1
            SF = EIsoSFs.getEIsoSF(pt,eta)
            if eta>1.444 and eta<1.566:
                SF = 1. #gap excluded in analysis
            hist_low.SetBinContent(i,j,SF)
    for i,pt in enumerate(lep_pt_high[:-1]):
        pt = pt + 0.5
        i = i+1
        for j,eta in enumerate(lep_eta[:-1]):
            eta = eta + 0.05
            j = j+1
            SF = EIsoSFs.getEIsoSF(pt,eta)
            if eta>1.444 and eta<1.566:
                SF = 1. #gap excluded in analysis
            hist_high.SetBinContent(i,j,SF)

     
    hist.GetXaxis().SetTitle("e p_{T}")
    hist.GetYaxis().SetTitle("e |#eta|")
    hist_low.GetXaxis().SetTitle("e p_{T}")
    hist_low.GetYaxis().SetTitle("e |#eta|")
    hist_high.GetXaxis().SetTitle("e p_{T}")
    hist_high.GetYaxis().SetTitle("e |#eta|")
    gStyle.SetPaintTextFormat(".3f")
    if realm=="":
        hist.Draw("COLZ")
        canv.SaveAs("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/EIsoSF/plots/EIsoSF_UL%s%s.pdf"%(year,VFPtag))
        canv.SaveAs("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/EIsoSF/plots/EIsoSF_UL%s%s.png"%(year,VFPtag))
        hist.Write()
        outfile.Close()
    elif realm=="low":
        hist_low.Draw("COLZTEXT45")
        canv.SaveAs("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/EIsoSF/plots/EIsoSF_UL%s%s_low.pdf"%(year,VFPtag))
        canv.SaveAs("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/EIsoSF/plots/EIsoSF_UL%s%s_low.png"%(year,VFPtag))
    elif realm=="high":
        hist_high.Draw("COLZTEXT45")
        canv.SaveAs("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/EIsoSF/plots/EIsoSF_UL%s%s_high.pdf"%(year,VFPtag))
        canv.SaveAs("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/EIsoSF/plots/EIsoSF_UL%s%s_high.png"%(year,VFPtag))
        
            

