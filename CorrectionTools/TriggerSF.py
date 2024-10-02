import ROOT
from ROOT import TFile, TH2D, TCanvas, gStyle, TLatex
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
        
        ##variations ####
        #fit
        mu_data_file_fit = TFile('%smutriggerEff_UL%s%s_data_fit_Fits_dimuon_mass_pt_eta_bins.root'%(path_root,year,VFPtag),'READ')
        self.mu_data_hist_fit = mu_data_file_fit.Get("dimuon_mass_pt_eta_bins")
        self.mu_data_hist_fit.SetDirectory(0)
        mu_data_file_fit.Close()
        mu_mc_file_fit = TFile('%smutriggerEff_UL%s%s_mc_fit_Fits_dimuon_mass_pt_eta_bins.root'%(path_root,year,VFPtag),'READ')
        self.mu_mc_hist_fit = mu_mc_file_fit.Get("dimuon_mass_pt_eta_bins")
        self.mu_mc_hist_fit.SetDirectory(0)
        mu_mc_file_fit.Close()

        #up
        mu_data_file_up = TFile('%smutriggerEff_UL%s%s_data_up_Fits_dimuon_mass_pt_eta_bins.root'%(path_root,year,VFPtag),'READ')
        self.mu_data_hist_up = mu_data_file_up.Get("dimuon_mass_pt_eta_bins")
        self.mu_data_hist_up.SetDirectory(0)
        mu_data_file_up.Close()
        mu_mc_file_up = TFile('%smutriggerEff_UL%s%s_mc_up_Fits_dimuon_mass_pt_eta_bins.root'%(path_root,year,VFPtag),'READ')
        self.mu_mc_hist_up = mu_mc_file_up.Get("dimuon_mass_pt_eta_bins")
        self.mu_mc_hist_up.SetDirectory(0)
        mu_mc_file_up.Close()
        
        #down
        mu_data_file_down = TFile('%smutriggerEff_UL%s%s_data_down_Fits_dimuon_mass_pt_eta_bins.root'%(path_root,year,VFPtag),'READ')
        self.mu_data_hist_down = mu_data_file_down.Get("dimuon_mass_pt_eta_bins")
        self.mu_data_hist_down.SetDirectory(0)
        mu_data_file_down.Close()
        mu_mc_file_down = TFile('%smutriggerEff_UL%s%s_mc_down_Fits_dimuon_mass_pt_eta_bins.root'%(path_root,year,VFPtag),'READ')
        self.mu_mc_hist_down = mu_mc_file_down.Get("dimuon_mass_pt_eta_bins")
        self.mu_mc_hist_down.SetDirectory(0)
        mu_mc_file_down.Close()
    
        #gen
        mu_mc_file_gen = TFile('%smutriggerEff_UL%s%s_mc_gen_Fits_dimuon_mass_pt_eta_bins.root'%(path_root,year,VFPtag),'READ')
        self.mu_mc_hist_gen = mu_mc_file_gen.Get("dimuon_mass_pt_eta_bins")
        self.mu_mc_hist_gen.SetDirectory(0)
        mu_mc_file_gen.Close()

        #e triggers
        e_data_file = TFile('%setriggerEff_UL%s%s_data_Fits_dielectron_mass_pt_eta_bins.root'%(path_root,year,VFPtag),'READ')
        self.e_data_hist = e_data_file.Get("dielectron_mass_pt_eta_bins")
        self.e_data_hist.SetDirectory(0)
        e_data_file.Close()
        e_mc_file = TFile('%setriggerEff_UL%s%s_mc_Fits_dielectron_mass_pt_eta_bins.root'%(path_root,year,VFPtag),'READ')
        self.e_mc_hist = e_mc_file.Get("dielectron_mass_pt_eta_bins")
        self.e_mc_hist.SetDirectory(0)
        e_mc_file.Close()

        ##variations ####
        #fit
        e_data_file_fit = TFile('%setriggerEff_UL%s%s_data_fit_Fits_dielectron_mass_pt_eta_bins.root'%(path_root,year,VFPtag),'READ')
        self.e_data_hist_fit = e_data_file_fit.Get("dielectron_mass_pt_eta_bins")
        self.e_data_hist_fit.SetDirectory(0)
        e_data_file_fit.Close()
        e_mc_file_fit = TFile('%setriggerEff_UL%s%s_mc_fit_Fits_dielectron_mass_pt_eta_bins.root'%(path_root,year,VFPtag),'READ')
        self.e_mc_hist_fit = e_mc_file_fit.Get("dielectron_mass_pt_eta_bins")
        self.e_mc_hist_fit.SetDirectory(0)
        e_mc_file_fit.Close()
        
        #up
        e_data_file_up = TFile('%setriggerEff_UL%s%s_data_up_Fits_dielectron_mass_pt_eta_bins.root'%(path_root,year,VFPtag),'READ')
        self.e_data_hist_up = e_data_file_up.Get("dielectron_mass_pt_eta_bins")
        self.e_data_hist_up.SetDirectory(0)
        e_data_file_up.Close()
        e_mc_file_up = TFile('%setriggerEff_UL%s%s_mc_up_Fits_dielectron_mass_pt_eta_bins.root'%(path_root,year,VFPtag),'READ')
        self.e_mc_hist_up = e_mc_file_up.Get("dielectron_mass_pt_eta_bins")
        self.e_mc_hist_up.SetDirectory(0)
        e_mc_file_up.Close()

        #down
        e_data_file_down = TFile('%setriggerEff_UL%s%s_data_down_Fits_dielectron_mass_pt_eta_bins.root'%(path_root,year,VFPtag),'READ')
        self.e_data_hist_down = e_data_file_down.Get("dielectron_mass_pt_eta_bins")
        self.e_data_hist_down.SetDirectory(0)
        e_data_file_down.Close()
        e_mc_file_down = TFile('%setriggerEff_UL%s%s_mc_down_Fits_dielectron_mass_pt_eta_bins.root'%(path_root,year,VFPtag),'READ')
        self.e_mc_hist_down = e_mc_file_down.Get("dielectron_mass_pt_eta_bins")
        self.e_mc_hist_down.SetDirectory(0)
        e_mc_file_down.Close()

        #gen
        e_mc_file_gen = TFile('%setriggerEff_UL%s%s_mc_gen_Fits_dielectron_mass_pt_eta_bins.root'%(path_root,year,VFPtag),'READ')
        self.e_mc_hist_gen = e_mc_file_gen.Get("dielectron_mass_pt_eta_bins")
        self.e_mc_hist_gen.SetDirectory(0)
        e_mc_file_gen.Close()

        if year==2017:
            e_data_file_tag = TFile('%setriggerEff_UL%s%s_data_tag_Fits_dielectron_mass_pt_eta_bins.root'%(path_root,year,VFPtag),'READ')
            self.e_data_hist_tag = e_data_file_tag.Get("dielectron_mass_pt_eta_bins")
            self.e_data_hist_tag.SetDirectory(0)
            e_data_file_tag.Close()
            e_mc_file_tag = TFile('%setriggerEff_UL%s%s_mc_tag_Fits_dielectron_mass_pt_eta_bins.root'%(path_root,year,VFPtag),'READ')
            self.e_mc_hist_tag = e_mc_file_tag.Get("dielectron_mass_pt_eta_bins")
            self.e_mc_hist_tag.SetDirectory(0)
            e_mc_file_tag.Close()
            
            e_data_file_ele32ac = TFile('%setriggerEff_UL%s%s_data_ele32ac_Fits_dielectron_mass_pt_eta_bins.root'%(path_root,year,VFPtag),'READ')
            self.e_data_hist_ele32ac = e_data_file_ele32ac.Get("dielectron_mass_pt_eta_bins")
            self.e_data_hist_ele32ac.SetDirectory(0)
            e_data_file_ele32ac.Close()
            e_data_file_ele32deac = TFile('%setriggerEff_UL%s%s_data_ele32deac_Fits_dielectron_mass_pt_eta_bins.root'%(path_root,year,VFPtag),'READ')
            self.e_data_hist_ele32deac = e_data_file_ele32deac.Get("dielectron_mass_pt_eta_bins")
            self.e_data_hist_ele32deac.SetDirectory(0)
            e_data_file_ele32deac.Close()

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
            elif var=="fit":
                sl_eff_data = self.getBinContent(self.mu_data_hist_fit,pt,eta)
                sl_eff_mc = self.getBinContent(self.mu_mc_hist_fit,pt,eta)
            elif var=="up":
                sl_eff_data = self.getBinContent(self.mu_data_hist_up,pt,eta)
                sl_eff_mc = self.getBinContent(self.mu_mc_hist_up,pt,eta)
            elif var=="down":
                sl_eff_data = self.getBinContent(self.mu_data_hist_down,pt,eta)
                sl_eff_mc = self.getBinContent(self.mu_mc_hist_down,pt,eta)
            elif var=="gen":
                sl_eff_data = self.getBinContent(self.mu_data_hist,pt,eta)
                sl_eff_mc = self.getBinContent(self.mu_mc_hist_gen,pt,eta)
        elif channel=="etau":
            if var=="":
                if self.year==2017:
                    sl_eff_data_ele32ac = self.getBinContent(self.e_data_hist_ele32ac,pt,eta)
                    sl_eff_data_ele32deac = self.getBinContent(self.e_data_hist_ele32deac,pt,eta)
                    sl_eff_data = (sl_eff_data_ele32ac * (27.13/41.54)) + (sl_eff_data_ele32deac * (14.41/41.54))
                    sl_eff_mc = self.getBinContent(self.e_mc_hist,pt,eta)
                else:
                    sl_eff_data = self.getBinContent(self.e_data_hist,pt,eta)
                    sl_eff_mc = self.getBinContent(self.e_mc_hist,pt,eta)
            elif var=="fit":
                sl_eff_data = self.getBinContent(self.e_data_hist_fit,pt,eta)
                sl_eff_mc = self.getBinContent(self.e_mc_hist_fit,pt,eta)
            elif var=="up":
                sl_eff_data = self.getBinContent(self.e_data_hist_up,pt,eta)
                sl_eff_mc = self.getBinContent(self.e_mc_hist_up,pt,eta)
            elif var=="down":
                sl_eff_data = self.getBinContent(self.e_data_hist_down,pt,eta)
                sl_eff_mc = self.getBinContent(self.e_mc_hist_down,pt,eta)
            elif var=="gen":
                sl_eff_data = self.getBinContent(self.e_data_hist,pt,eta)
                sl_eff_mc = self.getBinContent(self.e_mc_hist_gen,pt,eta)
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
        if VFPtag=="_preVFP":
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
        hist_low = TH2D("triggerSF_%s_UL%s%s_low"%(channel,year,VFPtag),"trigger SF %s UL%s%s"%(channel,year,VFPtag),Nbinsx_low,np.array(lep_pt_low),Nbinsy,np.array(lep_eta))
        hist_high = TH2D("triggerSF_%s_UL%s%s_high"%(channel,year,VFPtag),"trigger SF %s UL%s%s"%(channel,year,VFPtag),Nbinsx_high,np.array(lep_pt_high),Nbinsy,np.array(lep_eta))
        gStyle.SetOptStat(0)
        for i,pt in enumerate(lep_pt[:-1]):
            pt = pt + 0.5
            i = i+1
            for j,eta in enumerate(lep_eta[:-1]):
                eta = eta + 0.05
                j = j+1
                SF = triggerSFs.getTriggerSF(channel,pt,eta)
                if SF > 1.3: SF = 1.3
                if channel=="etau" and (eta>1.444 and eta<1.566):
                    SF = 1. #gap excluded in analysis
                hist.SetBinContent(i,j,SF)
        for i,pt in enumerate(lep_pt_low[:-1]):
            pt = pt + 0.5
            i = i+1
            for j,eta in enumerate(lep_eta[:-1]):
                eta = eta + 0.05
                j = j+1
                SF = triggerSFs.getTriggerSF(channel,pt,eta)
                if channel=="etau" and (eta>1.444 and eta<1.566):
                    SF = 1. #gap excluded in analysis
                hist_low.SetBinContent(i,j,SF)
        for i,pt in enumerate(lep_pt_high[:-1]):
            pt = pt + 0.5
            i = i+1
            for j,eta in enumerate(lep_eta[:-1]):
                eta = eta + 0.05
                j = j+1
                SF = triggerSFs.getTriggerSF(channel,pt,eta)
                if channel=="etau" and (eta>1.444 and eta<1.566):
                    SF = 1. #gap excluded in analysis
                hist_high.SetBinContent(i,j,SF)

        if channel=="mutau":
            hist.GetXaxis().SetTitle("#mu p_{T}")
            hist.GetYaxis().SetTitle("#mu |#eta|")
            hist_low.GetXaxis().SetTitle("#mu p_{T}")
            hist_low.GetYaxis().SetTitle("#mu |#eta|")
            hist_high.GetXaxis().SetTitle("#mu p_{T}")
            hist_high.GetYaxis().SetTitle("#mu |#eta|")
            channel_text = "single #mu trigger"
            hist.GetXaxis().SetTitleSize(0.05)
            hist.GetYaxis().SetTitleSize(0.05)
            hist.GetYaxis().SetTitleOffset(0.95)
            hist.GetXaxis().SetLabelSize(0.05)
            hist.GetYaxis().SetLabelSize(0.05)
            canv.SetTopMargin(0.12)
            canv.SetBottomMargin(0.12)
        elif channel=="etau":
            hist.GetXaxis().SetTitle("e p_{T}")
            hist.GetYaxis().SetTitle("e |#eta|")
            hist_low.GetXaxis().SetTitle("e p_{T}")
            hist_low.GetYaxis().SetTitle("e |#eta|")
            hist_high.GetXaxis().SetTitle("e p_{T}")
            hist_high.GetYaxis().SetTitle("e |#eta|")
            channel_text = "single e trigger"
            hist.GetXaxis().SetTitleSize(0.05)
            hist.GetYaxis().SetTitleSize(0.05)
            hist.GetYaxis().SetTitleOffset(0.95)
            hist.GetXaxis().SetLabelSize(0.05)
            hist.GetYaxis().SetLabelSize(0.05)
            canv.SetTopMargin(0.12)
            canv.SetBottomMargin(0.12)
        gStyle.SetPaintTextFormat(".3f")
        if realm=="":
            hist.Draw("COLZ")
            plot.DrawCMSLogo(canv, "Private work", "(CMS data/simulation)", 10, 0.01, -0.14, 0.9, '', 0.55)
            latex = TLatex()
            latex.SetNDC()
            latex.SetTextSize(0.045)
            latex.SetTextColor(1)
            latex.SetTextFont(42)
            if year==2016:
                if VFPtag=="_preVFP":
                    VFPtag_plots = " preVFP"
                else:
                    VFPtag_plots = " postVFP"
                latex.DrawLatex(0.55, 0.89, "%s%s %s fb^{-1} (13 TeV)"%(year,VFPtag_plots,lumi))
            else:
                VFPtag_plots = ""
                latex.DrawLatex(0.65, 0.89, "%s %s fb^{-1} (13 TeV)"%(year,lumi))
            latex.DrawLatex(0.42, 0.95, channel_text)
            canv.SaveAs("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/triggerSF/plots/triggerSF_%s_UL%s%s.pdf"%(channel,year,VFPtag))
            canv.SaveAs("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/triggerSF/plots/triggerSF_%s_UL%s%s.png"%(channel,year,VFPtag))
            canv.SaveAs("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/triggerSF/plots/thesis/triggerSF_%s_UL%s%s.pdf"%(channel,year,VFPtag))
            hist.Write()
            outfile.Close()
        elif realm=="low":
            hist_low.Draw("COLZTEXT45")
            canv.SaveAs("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/triggerSF/plots/triggerSF_%s__UL%s%s_low.pdf"%(channel,year,VFPtag))
            canv.SaveAs("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/triggerSF/plots/triggerSF_%s__UL%s%s_low.png"%(channel,year,VFPtag))
        elif realm=="high":
            hist_high.Draw("COLZTEXT45")
            canv.SaveAs("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/triggerSF/plots/triggerSF_%s__UL%s%s_high.pdf"%(channel,year,VFPtag))
            canv.SaveAs("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/triggerSF/plots/triggerSF_%s__UL%s%s_high.png"%(channel,year,VFPtag))

            
        #SF errors
        for n,sys in enumerate(["Fit","Gen","Up","Down"]):
            if realm=="":
                outfile = TFile("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/triggerSF/root/triggerSF%s_%s__UL%s%s.root"%(sys,channel,year,VFPtag),"RECREATE")
            canv = TCanvas("triggerSF%s_%s__UL%s%s"%(sys,channel,year,VFPtag),"trigger SF %s %s UL%s%s"%(sys,channel,year,VFPtag),1000,600)
            hist = TH2D("triggerSF%s_%s_UL%s%s"%(sys,channel,year,VFPtag),"trigger SF %s %s UL%s%s"%(sys,channel,year,VFPtag),Nbinsx,np.array(lep_pt),Nbinsy,np.array(lep_eta))
            hist_low = TH2D("triggerSF%s_%s_UL%s%s_low"%(sys,channel,year,VFPtag),"trigger SF %s %s UL%s%s"%(sys,channel,year,VFPtag),Nbinsx_low,np.array(lep_pt_low),Nbinsy,np.array(lep_eta))
            hist_high = TH2D("triggerSF%s_%s_UL%s%s_high"%(sys,channel,year,VFPtag),"trigger SF %s %s UL%s%s"%(sys,channel,year,VFPtag),Nbinsx_high,np.array(lep_pt_high),Nbinsy,np.array(lep_eta))
            gStyle.SetOptStat(0)
            for i,pt in enumerate(lep_pt[:-1]):
                pt = pt + 0.5
                i = i+1
                for j,eta in enumerate(lep_eta[:-1]):
                    eta = eta + 0.05
                    j = j+1
                    #SFError = triggerSFs.getTriggerSFError(channel,pt,eta)[n]
                    SFError = triggerSFs.getTriggerSFUnc(channel,pt,eta)[n]
                    if channel=="etau" and (eta>1.444 and eta<1.566):
                        SFError = 0. #gap excluded in analysis
                    hist.SetBinContent(i,j,SFError)
            for i,pt in enumerate(lep_pt_low[:-1]):
                pt = pt + 0.5
                i = i+1
                for j,eta in enumerate(lep_eta[:-1]):
                    eta = eta + 0.05
                    j = j+1
                    #SFError = triggerSFs.getTriggerSFError(channel,pt,eta)[n]
                    SFError = triggerSFs.getTriggerSFUnc(channel,pt,eta)[n]
                    if channel=="etau" and (eta>1.444 and eta<1.566):
                        SFError = 0. #gap excluded in analysis
                    hist_low.SetBinContent(i,j,SFError)
            for i,pt in enumerate(lep_pt_high[:-1]):
                pt = pt + 0.5
                i = i+1
                for j,eta in enumerate(lep_eta[:-1]):
                    eta = eta + 0.05
                    j = j+1
                    #SFError = triggerSFs.getTriggerSFError(channel,pt,eta)[n]
                    SFError = triggerSFs.getTriggerSFUnc(channel,pt,eta)[n]
                    if channel=="etau" and (eta>1.444 and eta<1.566):
                        SFError = 0. #gap excluded in analysis
                    hist_high.SetBinContent(i,j,SFError)
                        
    
            if channel=="mutau":
                hist.GetXaxis().SetTitle("#mu p_{T}")
                hist.GetYaxis().SetTitle("#mu |#eta|")
                hist_low.GetXaxis().SetTitle("#mu p_{T}")
                hist_low.GetYaxis().SetTitle("#mu |#eta|")
                hist_high.GetXaxis().SetTitle("#mu p_{T}")
                hist_high.GetYaxis().SetTitle("#mu |#eta|")
            elif channel=="etau":
                hist.GetXaxis().SetTitle("e p_{T}")
                hist.GetYaxis().SetTitle("e |#eta|")
                hist_low.GetXaxis().SetTitle("e p_{T}")
                hist_low.GetYaxis().SetTitle("e |#eta|")
                hist_high.GetXaxis().SetTitle("e p_{T}")
                hist_high.GetYaxis().SetTitle("e |#eta|")
            hist.GetZaxis().SetMaxDigits(3)
            hist_low.GetZaxis().SetMaxDigits(3)
            hist_high.GetZaxis().SetMaxDigits(3)
            gStyle.SetPaintTextFormat(".5f")
            if realm=="":
                hist.Draw("COLZ")
                canv.SaveAs("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/triggerSF/plots/Systematics/triggerSF%s_%s_UL%s%s.pdf"%(sys,channel,year,VFPtag))
                canv.SaveAs("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/triggerSF/plots/Systematics/triggerSF%s_%s_UL%s%s.png"%(sys,channel,year,VFPtag))
                hist.Write()
                outfile.Close()
            elif realm=="low":
                hist_low.Draw("COLZTEXT45")
                canv.SaveAs("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/triggerSF/plots/Systematics/triggerSF%s_%s_UL%s%s_low.pdf"%(sys,channel,year,VFPtag))
                canv.SaveAs("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/triggerSF/plots/Systematics/triggerSF%s_%s_UL%s%s_low.png"%(sys,channel,year,VFPtag))
            elif realm=="high":
                hist_high.Draw("COLZTEXT45")
                canv.SaveAs("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/triggerSF/plots/Systematics/triggerSF%s_%s_UL%s%s_high.pdf"%(sys,channel,year,VFPtag))
                canv.SaveAs("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/triggerSF/plots/Systematics/triggerSF%s_%s_UL%s%s_high.png"%(sys,channel,year,VFPtag))
            
