import ROOT
from ROOT import TFile, TH2D, TCanvas, gStyle, TLatex, TH1D
import correctionlib
import os
import plotting as plot
from argparse import ArgumentParser
import numpy as np

path_root = '/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/triggerSF/root/'

class TriggerSFs:

    def __init__(self,year,VFPtag):
        self.year = year
        self.VFPtag = VFPtag
        #mu triggers
        mu_data_file = TFile('%smutriggerEff_UL%s%s_data_Fits_dimuon_mass_pt_eta_bins.root'%(path_root,year,VFPtag),'READ')
        self.mu_data_hist = mu_data_file.Get("dimuon_mass_pt_eta_bins")
        self.mu_data_hist.SetDirectory(0)
        mu_data_file.Close()
        mu_mc_file = TFile('%smutriggerEff_UL%s%s_mc_Fits_dimuon_mass_pt_eta_bins.root'%(path_root,year,VFPtag),'READ')
        self.mu_mc_hist = mu_mc_file.Get("dimuon_mass_pt_eta_bins")
        self.mu_mc_hist.SetDirectory(0)
        mu_mc_file.Close()

        #e triggers
        e_data_file = TFile('%setriggerEff_UL%s%s_data_Fits_dielectron_mass_pt_eta_bins.root'%(path_root,year,VFPtag),'READ')
        self.e_data_hist = e_data_file.Get("dielectron_mass_pt_eta_bins")
        self.e_data_hist.SetDirectory(0)
        e_data_file.Close()
        e_mc_file = TFile('%setriggerEff_UL%s%s_mc_Fits_dielectron_mass_pt_eta_bins.root'%(path_root,year,VFPtag),'READ')
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
        return hist.GetBinContent(hist.GetXaxis().FindBin(pt),hist.GetYaxis().FindBin(abs(eta)))

    def getLepTriggerEff(self,channel,pt,eta,var):
        if channel=="mutau":
            if var=="":
                sl_eff_data = self.getBinContent(self.mu_data_hist,pt,eta)
                sl_eff_mc = self.getBinContent(self.mu_mc_hist,pt,eta)
        elif channel=="etau":
            if var=="":
                sl_eff_data = self.getBinContent(self.e_data_hist,pt,eta)
                sl_eff_mc = self.getBinContent(self.e_mc_hist,pt,eta)
        return [sl_eff_data,sl_eff_mc]


    def getTriggerSF(self,channel,lep_pt,lep_eta,var=""):
        leptriggerEff = self.getLepTriggerEff(channel,lep_pt,abs(lep_eta),var)
        eff_lep_sl_data = leptriggerEff[0]
        eff_lep_sl_mc = leptriggerEff[1]
        num = eff_lep_sl_data
        den = eff_lep_sl_mc
        return num/den

    def getTriggerSFError(self,channel,lep_pt,lep_eta):
        SF_error_list = []
        SF_nom = self.getTriggerSF(channel,lep_pt,lep_eta)
        for var in ["fit","gen","up","down"]:
            SF_error_list.append(abs(self.getTriggerSF(channel,lep_pt,lep_eta,var)-SF_nom))
        return SF_error_list

    def getTriggerSFUnc(self,channel,lep_pt,lep_eta):
        SF_error_list = []
        for var in ["fit","gen","up","down"]:
            SF_error_list.append(self.getTriggerSF(channel,lep_pt,lep_eta,var))
        return SF_error_list

    def getTriggerSFTAG(self,channel,lep_pt,lep_eta):
        num = self.getBinContent(self.e_data_hist_tag,lep_pt,lep_eta)
        den = self.getBinContent(self.e_mc_hist_tag,lep_pt,lep_eta)
        if den==0.:
            return 1.
        else:
            return num/den

    def getTriggerSF_MuMu(self,mu1_pt,mu1_eta,mu2_pt,mu2_eta):
        mu1triggerEff = self.getLepTriggerEff("mutau",mu1_pt,abs(mu1_eta),"")
        mu2triggerEff = self.getLepTriggerEff("mutau",mu2_pt,abs(mu2_eta),"")
        eff_mu1_data = mu1triggerEff[0]
        eff_mu1_mc = mu1triggerEff[1]
        eff_mu2_data = mu2triggerEff[0]
        eff_mu2_mc = mu2triggerEff[1]
        num = eff_mu1_data+eff_mu2_data-(eff_mu1_data*eff_mu2_data)
        den = eff_mu1_mc+eff_mu2_mc-(eff_mu1_mc*eff_mu2_mc)
        if den==0: 
            SF = 1.
        else:
            SF = num/den
        SF_up = SF+(SF*0.02)
        SF_down = SF-(SF*0.02)
        return [SF,SF_up,SF_down]

    def getTriggerSF_MuE(self,mu_pt,mu_eta,e_pt,e_eta):
        mutriggerEff = self.getLepTriggerEff("mutau",mu_pt,abs(mu_eta),"")
        etriggerEff = self.getLepTriggerEff("etau",e_pt,abs(e_eta),"")
        eff_mu_data = mutriggerEff[0]
        eff_mu_mc = mutriggerEff[1]
        eff_e_data = etriggerEff[0]
        eff_e_mc = etriggerEff[1]
        num = eff_mu_data+eff_e_data-(eff_mu_data*eff_e_data)
        den = eff_mu_mc+eff_e_mc-(eff_mu_mc*eff_e_mc)
        if den==0:
            SF = 1.
        else:
            SF = num/den
        SF_up = SF+(SF*0.02)
        SF_down = SF-(SF*0.02)
        return [SF,SF_up,SF_down]

    
    
if __name__=="__main__":
    parser = ArgumentParser()
    parser.add_argument('-y', '--year',    dest='year', choices=[2016,2017,2018], type=int, default=2018, action='store')
    parser.add_argument('-p', '--preVFP',  dest='preVFP', action='store_const', const="_preVFP",default="")
    parser.add_argument('-r', '--realm', dest='realm', action='store',default="")
    args = parser.parse_args()
    realm = args.realm
    channels = ["mutau","etau"]
    year = args.year
    VFPtag = args.preVFP
    ROOT.gROOT.SetBatch(ROOT.kTRUE)
    if year!=2016:
        mu_pt = [25., 26., 27., 28., 29., 30., 31., 32., 33., 34., 35., 40., 45., 50. ,75., 100., 200.]
        mu_pt_low = [25., 26., 27., 28., 29., 30., 31., 32., 33., 34., 35.]
        mu_pt_high = [35., 40., 45., 50. ,75., 100., 200.]
    else:
        mu_pt = [23., 24., 25., 26., 27., 28., 29., 30., 31., 32., 33., 34., 35., 40., 45., 50. ,75., 100., 200.]
        mu_pt_low = [23., 24., 25., 26., 27., 28., 29., 30., 31., 32., 33., 34., 35.]
        mu_pt_high = [35., 40., 45., 50. ,75., 100., 200.]
    mu_eta =  [0., 0.9, 1.2, 2.1, 2.4]
    if year!=2016:
        e_pt = [33., 34., 35., 36., 37., 38., 39., 40., 45., 50. ,75., 100., 200.]
        e_pt_low = [33., 34., 35., 36., 37., 38., 39., 40.]
        e_pt_high = [40., 45., 50. ,75., 100., 200.]
    else:
        e_pt = [26., 27., 28., 29., 30., 31., 32., 33., 34., 35., 36., 37., 38., 39., 40., 45., 50. ,75., 100., 200.]
        e_pt_low = [26., 27., 28., 29., 30., 31., 32., 33., 34., 35., 36., 37., 38., 39., 40.]
        e_pt_high = [40., 45., 50. ,75., 100., 200.]
    e_eta = [0., 0.8, 1.444, 1.566, 2., 2.1]
    triggerSFs = TriggerSFs(year,VFPtag)
    if year == 2018:
        lumi = 59.7
    elif year == 2017:
        lumi = 41.5
    elif year == 2016:
        if preVFP=="_preVFP":
            lumi = 19.5
        else:
            lumi = 16.8

    for channel in channels:
        if channel == "mutau":
            lep_pt = mu_pt
            lep_eta = mu_eta
            lep_pt_low = mu_pt_low
            lep_pt_high = mu_pt_high
        else:
            lep_pt = e_pt
            lep_eta = e_eta
            lep_pt_low = e_pt_low
            lep_pt_high = e_pt_high
        Nbinsx = len(lep_pt)-1
        Nbinsy = len(lep_eta)-1
        Nbinsx_low = len(lep_pt_low)-1
        Nbinsx_high = len(lep_pt_high)-1

        if realm=="":
            outfile = TFile("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/triggerSF/root/triggerSF_%s_UL%s%s.root"%(channel,year,VFPtag),"RECREATE")
        canv = TCanvas("triggerSF_%s_UL%s%s"%(channel,year,VFPtag),"trigger SF %s UL%s%s"%(channel,year,VFPtag))
        hist = TH2D("triggerSF_%s_UL%s%s"%(channel,year,VFPtag),"",Nbinsx,np.array(lep_pt),Nbinsy,np.array(lep_eta))
        if channel=="mutau":
            hist1 = TH1D("triggerSF_%s_UL%s%s_eta00"%(channel,year,VFPtag),"",Nbinsx,np.array(lep_pt))
            hist2 = TH1D("triggerSF_%s_UL%s%s_eta09"%(channel,year,VFPtag),"",Nbinsx,np.array(lep_pt))
            hist3 = TH1D("triggerSF_%s_UL%s%s_eta12"%(channel,year,VFPtag),"",Nbinsx,np.array(lep_pt))
            hist4 = TH1D("triggerSF_%s_UL%s%s_eta21"%(channel,year,VFPtag),"",Nbinsx,np.array(lep_pt))
        else:
            hist1 = TH1D("triggerSF_%s_UL%s%s_eta00"%(channel,year,VFPtag),"",Nbinsx,np.array(lep_pt))
            hist2 = TH1D("triggerSF_%s_UL%s%s_eta08"%(channel,year,VFPtag),"",Nbinsx,np.array(lep_pt))
            hist3 = TH1D("triggerSF_%s_UL%s%s_eta1566"%(channel,year,VFPtag),"",Nbinsx,np.array(lep_pt))
            hist4 = TH1D("triggerSF_%s_UL%s%s_eta2"%(channel,year,VFPtag),"",Nbinsx,np.array(lep_pt))
        gStyle.SetOptStat(0)
        for i,pt in enumerate(lep_pt[:-1]):
            pt = pt + 0.5
            i = i+1
            if channel=="mutau":
                SF1 = triggerSFs.getTriggerSF(channel,pt,0.0+0.05)
                SF2 = triggerSFs.getTriggerSF(channel,pt,0.9+0.05)
                SF3 = triggerSFs.getTriggerSF(channel,pt,1.2+0.05)
                SF4 = triggerSFs.getTriggerSF(channel,pt,2.1+0.05)
            else:
                SF1 = triggerSFs.getTriggerSF(channel,pt,0.0+0.05)
                SF2 = triggerSFs.getTriggerSF(channel,pt,0.8+0.05)
                SF3 = triggerSFs.getTriggerSF(channel,pt,1.566+0.05)
                SF4 = triggerSFs.getTriggerSF(channel,pt,2.0+0.05)
            if SF1 > 1.3: SF1 = 1.3
            if SF2 > 1.3: SF2 = 1.3
            if SF3 > 1.3: SF3 = 1.3
            if SF4 > 1.3: SF4 = 1.3
            hist1.SetBinContent(i,SF1)
            hist2.SetBinContent(i,SF2)
            hist3.SetBinContent(i,SF3)
            hist4.SetBinContent(i,SF4)

        if channel=="mutau":
            hist1.GetXaxis().SetTitle("#mu p_{T}")
            hist1.GetYaxis().SetTitle("#mu |#eta|")
            channel_text = "single #mu trigger"
        elif channel=="etau":
            hist1.GetXaxis().SetTitle("e p_{T}")
            hist1.GetYaxis().SetTitle("e |#eta|")
            channel_text = "single e trigger"
        gStyle.SetPaintTextFormat(".3f")
        if realm=="":
            if channel=="mutau":
                hist1.GetYaxis().SetRangeUser(0.94,1.05)
            else:
                hist1.GetYaxis().SetRangeUser(0.8,1.3)
            hist1.Draw("HIST")
            hist2.Draw("HISTSAME")
            hist3.Draw("HISTSAME")
            hist4.Draw("HISTSAME")
            plot.DrawCMSLogo(canv, "Private work", "(CMS data/simulation)", 10, 0.01, -0.12, 0.9, '', 0.6)
            latex = TLatex()
            latex.SetNDC()
            latex.SetTextSize(0.04)
            latex.SetTextColor(1)
            latex.SetTextFont(42)
            if year==2016:
                if preVFP == "_preVFP": 
                    VFPtag = " preVFP"
                else:
                    VFPtag = " postVFP"
                latex.DrawLatex(0.54, 0.91, "%s%s %s fb^{-1} (13 TeV)"%(year,VFPtag,lumi))
            else:
                latex.DrawLatex(0.64, 0.91, "%s %s fb^{-1} (13 TeV)"%(year,lumi))
            latex.DrawLatex(0.42, 0.93, channel_text)
            canv.SaveAs("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/triggerSF/plots/thesis/triggerSF_%s_UL%s%s_split.pdf"%(channel,year,VFPtag))
            hist.Write()
            outfile.Close()
