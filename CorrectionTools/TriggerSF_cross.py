import ROOT
from ROOT import TFile, TH2D, TCanvas, gStyle
import correctionlib
import os
from argparse import ArgumentParser
import numpy as np
from .TauTriggerSFs import TauTriggerSFs

path_json = '/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/jsonpog-integration/POG/TAU/'
path_root = '/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/triggerSF/root/'
#path_root = '/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/triggerSF/root/check/'

class TriggerSFs:

    def __init__(self,year,VFPtag):
        self.year = year
        self.VFPtag = VFPtag
        if year==2018:
            self.year_name = "2018_UL"
        elif year==2017:
            self.year_name = "2017_UL"
        elif year==2016:
            if VFPtag == "_preVFP":
                self.year_name = "2016preVFP_UL"
            else:
                self.year_name = "2016postVFP_UL"
        self.taujson = correctionlib.CorrectionSet.from_file(os.path.join(path_json,self.year_name,"tau.json.gz"))
        self.tauTriggerTool_mutau_medium = TauTriggerSFs("%s"%year,"mutau","Medium")
        self.tauTriggerTool_etau_medium = TauTriggerSFs("%s"%year,"etau","Medium")
        self.tauTriggerTool_mutau_vvvloose = TauTriggerSFs("%s"%year,"mutau","VVVLoose")
        self.tauTriggerTool_etau_vvvloose = TauTriggerSFs("%s"%year,"etau","VVVLoose")
        #mu triggers
        mu_data_file = TFile('%smutriggerEff_UL%s%s_data_Fits_dimuon_mass_pt_eta_bins.root'%(path_root,year,VFPtag),'READ')
        self.mu_data_hist = mu_data_file.Get("dimuon_mass_pt_eta_bins")
        self.mu_data_hist.SetDirectory(0)
        mu_data_file.Close()
        mu_mc_file = TFile('%smutriggerEff_UL%s%s_mc_Fits_dimuon_mass_pt_eta_bins.root'%(path_root,year,VFPtag),'READ')
        self.mu_mc_hist = mu_mc_file.Get("dimuon_mass_pt_eta_bins")
        self.mu_mc_hist.SetDirectory(0)
        mu_mc_file.Close()
        
        mutau_data_file = TFile('%smutautriggerEff_UL%s%s_data_Fits_dimuon_mass_pt_eta_bins.root'%(path_root,year,VFPtag),'READ')
        self.mutau_data_hist = mutau_data_file.Get("dimuon_mass_pt_eta_bins")
        self.mutau_data_hist.SetDirectory(0)
        mutau_data_file.Close()
        mutau_mc_file = TFile('%smutautriggerEff_UL%s%s_mc_Fits_dimuon_mass_pt_eta_bins.root'%(path_root,year,VFPtag),'READ')
        self.mutau_mc_hist = mutau_mc_file.Get("dimuon_mass_pt_eta_bins")
        self.mutau_mc_hist.SetDirectory(0)
        mutau_mc_file.Close()
        
        mutauSLF_data_file = TFile('%smutautriggerSLFEff_UL%s%s_data_Fits_dimuon_mass_pt_eta_bins.root'%(path_root,year,VFPtag),'READ')
        self.mutauSLF_data_hist = mutauSLF_data_file.Get("dimuon_mass_pt_eta_bins")
        self.mutauSLF_data_hist.SetDirectory(0)
        mutauSLF_data_file.Close()
        mutauSLF_mc_file = TFile('%smutautriggerSLFEff_UL%s%s_mc_Fits_dimuon_mass_pt_eta_bins.root'%(path_root,year,VFPtag),'READ')
        self.mutauSLF_mc_hist = mutauSLF_mc_file.Get("dimuon_mass_pt_eta_bins")
        self.mutauSLF_mc_hist.SetDirectory(0)
        mutauSLF_mc_file.Close()
        
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
        
        mutau_data_file_fit = TFile('%smutautriggerEff_UL%s%s_data_fit_Fits_dimuon_mass_pt_eta_bins.root'%(path_root,year,VFPtag),'READ')
        self.mutau_data_hist_fit = mutau_data_file_fit.Get("dimuon_mass_pt_eta_bins")
        self.mutau_data_hist_fit.SetDirectory(0)
        mutau_data_file_fit.Close()
        mutau_mc_file_fit = TFile('%smutautriggerEff_UL%s%s_mc_fit_Fits_dimuon_mass_pt_eta_bins.root'%(path_root,year,VFPtag),'READ')
        self.mutau_mc_hist_fit = mutau_mc_file_fit.Get("dimuon_mass_pt_eta_bins")
        self.mutau_mc_hist_fit.SetDirectory(0)
        mutau_mc_file_fit.Close()
        
        mutauSLF_data_file_fit = TFile('%smutautriggerSLFEff_UL%s%s_data_fit_Fits_dimuon_mass_pt_eta_bins.root'%(path_root,year,VFPtag),'READ')
        self.mutauSLF_data_hist_fit = mutauSLF_data_file_fit.Get("dimuon_mass_pt_eta_bins")
        self.mutauSLF_data_hist_fit.SetDirectory(0)
        mutauSLF_data_file_fit.Close()
        mutauSLF_mc_file_fit = TFile('%smutautriggerSLFEff_UL%s%s_mc_fit_Fits_dimuon_mass_pt_eta_bins.root'%(path_root,year,VFPtag),'READ')
        self.mutauSLF_mc_hist_fit = mutauSLF_mc_file_fit.Get("dimuon_mass_pt_eta_bins")
        self.mutauSLF_mc_hist_fit.SetDirectory(0)
        mutauSLF_mc_file_fit.Close()
        #up
        mu_data_file_up = TFile('%smutriggerEff_UL%s%s_data_up_Fits_dimuon_mass_pt_eta_bins.root'%(path_root,year,VFPtag),'READ')
        self.mu_data_hist_up = mu_data_file_up.Get("dimuon_mass_pt_eta_bins")
        self.mu_data_hist_up.SetDirectory(0)
        mu_data_file_up.Close()
        mu_mc_file_up = TFile('%smutriggerEff_UL%s%s_mc_up_Fits_dimuon_mass_pt_eta_bins.root'%(path_root,year,VFPtag),'READ')
        self.mu_mc_hist_up = mu_mc_file_up.Get("dimuon_mass_pt_eta_bins")
        self.mu_mc_hist_up.SetDirectory(0)
        mu_mc_file_up.Close()
        
        mutau_data_file_up = TFile('%smutautriggerEff_UL%s%s_data_up_Fits_dimuon_mass_pt_eta_bins.root'%(path_root,year,VFPtag),'READ')
        self.mutau_data_hist_up = mutau_data_file_up.Get("dimuon_mass_pt_eta_bins")
        self.mutau_data_hist_up.SetDirectory(0)
        mutau_data_file_up.Close()
        mutau_mc_file_up = TFile('%smutautriggerEff_UL%s%s_mc_up_Fits_dimuon_mass_pt_eta_bins.root'%(path_root,year,VFPtag),'READ')
        self.mutau_mc_hist_up = mutau_mc_file_up.Get("dimuon_mass_pt_eta_bins")
        self.mutau_mc_hist_up.SetDirectory(0)
        mutau_mc_file_up.Close()
        
        mutauSLF_data_file_up = TFile('%smutautriggerSLFEff_UL%s%s_data_up_Fits_dimuon_mass_pt_eta_bins.root'%(path_root,year,VFPtag),'READ')
        self.mutauSLF_data_hist_up = mutauSLF_data_file_up.Get("dimuon_mass_pt_eta_bins")
        self.mutauSLF_data_hist_up.SetDirectory(0)
        mutauSLF_data_file_up.Close()
        mutauSLF_mc_file_up = TFile('%smutautriggerSLFEff_UL%s%s_mc_up_Fits_dimuon_mass_pt_eta_bins.root'%(path_root,year,VFPtag),'READ')
        self.mutauSLF_mc_hist_up = mutauSLF_mc_file_up.Get("dimuon_mass_pt_eta_bins")
        self.mutauSLF_mc_hist_up.SetDirectory(0)
        mutauSLF_mc_file_up.Close()
        #down
        mu_data_file_down = TFile('%smutriggerEff_UL%s%s_data_down_Fits_dimuon_mass_pt_eta_bins.root'%(path_root,year,VFPtag),'READ')
        self.mu_data_hist_down = mu_data_file_down.Get("dimuon_mass_pt_eta_bins")
        self.mu_data_hist_down.SetDirectory(0)
        mu_data_file_down.Close()
        mu_mc_file_down = TFile('%smutriggerEff_UL%s%s_mc_down_Fits_dimuon_mass_pt_eta_bins.root'%(path_root,year,VFPtag),'READ')
        self.mu_mc_hist_down = mu_mc_file_down.Get("dimuon_mass_pt_eta_bins")
        self.mu_mc_hist_down.SetDirectory(0)
        mu_mc_file_down.Close()
        
        mutau_data_file_down = TFile('%smutautriggerEff_UL%s%s_data_down_Fits_dimuon_mass_pt_eta_bins.root'%(path_root,year,VFPtag),'READ')
        self.mutau_data_hist_down = mutau_data_file_down.Get("dimuon_mass_pt_eta_bins")
        self.mutau_data_hist_down.SetDirectory(0)
        mutau_data_file_down.Close()
        mutau_mc_file_down = TFile('%smutautriggerEff_UL%s%s_mc_down_Fits_dimuon_mass_pt_eta_bins.root'%(path_root,year,VFPtag),'READ')
        self.mutau_mc_hist_down = mutau_mc_file_down.Get("dimuon_mass_pt_eta_bins")
        self.mutau_mc_hist_down.SetDirectory(0)
        mutau_mc_file_down.Close()
        
        mutauSLF_data_file_down = TFile('%smutautriggerSLFEff_UL%s%s_data_down_Fits_dimuon_mass_pt_eta_bins.root'%(path_root,year,VFPtag),'READ')
        self.mutauSLF_data_hist_down = mutauSLF_data_file_down.Get("dimuon_mass_pt_eta_bins")
        self.mutauSLF_data_hist_down.SetDirectory(0)
        mutauSLF_data_file_down.Close()
        mutauSLF_mc_file_down = TFile('%smutautriggerSLFEff_UL%s%s_mc_down_Fits_dimuon_mass_pt_eta_bins.root'%(path_root,year,VFPtag),'READ')
        self.mutauSLF_mc_hist_down = mutauSLF_mc_file_down.Get("dimuon_mass_pt_eta_bins")
        self.mutauSLF_mc_hist_down.SetDirectory(0)
        mutauSLF_mc_file_down.Close()
        #gen
        mu_mc_file_gen = TFile('%smutriggerEff_UL%s%s_mc_gen_Fits_dimuon_mass_pt_eta_bins.root'%(path_root,year,VFPtag),'READ')
        self.mu_mc_hist_gen = mu_mc_file_gen.Get("dimuon_mass_pt_eta_bins")
        self.mu_mc_hist_gen.SetDirectory(0)
        mu_mc_file_gen.Close()
        
        mutau_mc_file_gen = TFile('%smutautriggerEff_UL%s%s_mc_gen_Fits_dimuon_mass_pt_eta_bins.root'%(path_root,year,VFPtag),'READ')
        self.mutau_mc_hist_gen = mutau_mc_file_gen.Get("dimuon_mass_pt_eta_bins")
        self.mutau_mc_hist_gen.SetDirectory(0)
        mutau_mc_file_gen.Close()
        
        mutauSLF_mc_file_gen = TFile('%smutautriggerSLFEff_UL%s%s_mc_gen_Fits_dimuon_mass_pt_eta_bins.root'%(path_root,year,VFPtag),'READ')
        self.mutauSLF_mc_hist_gen = mutauSLF_mc_file_gen.Get("dimuon_mass_pt_eta_bins")
        self.mutauSLF_mc_hist_gen.SetDirectory(0)
        mutauSLF_mc_file_gen.Close()

        #e triggers
        e_data_file = TFile('%setriggerEff_UL%s%s_data_Fits_dielectron_mass_pt_eta_bins.root'%(path_root,year,VFPtag),'READ')
        self.e_data_hist = e_data_file.Get("dielectron_mass_pt_eta_bins")
        self.e_data_hist.SetDirectory(0)
        e_data_file.Close()
        e_mc_file = TFile('%setriggerEff_UL%s%s_mc_Fits_dielectron_mass_pt_eta_bins.root'%(path_root,year,VFPtag),'READ')
        self.e_mc_hist = e_mc_file.Get("dielectron_mass_pt_eta_bins")
        self.e_mc_hist.SetDirectory(0)
        e_mc_file.Close()
        if self.year!=2016 or self.VFPtag=="_preVFP":
            etau_data_file = TFile('%setautriggerEff_UL%s%s_data_Fits_dielectron_mass_pt_eta_bins.root'%(path_root,year,VFPtag),'READ')
            self.etau_data_hist = etau_data_file.Get("dielectron_mass_pt_eta_bins")
            self.etau_data_hist.SetDirectory(0)
            etau_data_file.Close()
            etau_mc_file = TFile('%setautriggerEff_UL%s%s_mc_Fits_dielectron_mass_pt_eta_bins.root'%(path_root,year,VFPtag),'READ')
            self.etau_mc_hist = etau_mc_file.Get("dielectron_mass_pt_eta_bins")
            self.etau_mc_hist.SetDirectory(0)
            etau_mc_file.Close()
        
            etauSLF_data_file = TFile('%setautriggerSLFEff_UL%s%s_data_Fits_dielectron_mass_pt_eta_bins.root'%(path_root,year,VFPtag),'READ')
            self.etauSLF_data_hist = etauSLF_data_file.Get("dielectron_mass_pt_eta_bins")
            self.etauSLF_data_hist.SetDirectory(0)
            etauSLF_data_file.Close()
            etauSLF_mc_file = TFile('%setautriggerSLFEff_UL%s%s_mc_Fits_dielectron_mass_pt_eta_bins.root'%(path_root,year,VFPtag),'READ')
            self.etauSLF_mc_hist = etauSLF_mc_file.Get("dielectron_mass_pt_eta_bins")
            self.etauSLF_mc_hist.SetDirectory(0)
            etauSLF_mc_file.Close()

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
        
        if self.year!=2016 or self.VFPtag=="_preVFP":
            etau_data_file_fit = TFile('%setautriggerEff_UL%s%s_data_fit_Fits_dielectron_mass_pt_eta_bins.root'%(path_root,year,VFPtag),'READ')
            self.etau_data_hist_fit = etau_data_file_fit.Get("dielectron_mass_pt_eta_bins")
            self.etau_data_hist_fit.SetDirectory(0)
            etau_data_file_fit.Close()
            etau_mc_file_fit = TFile('%setautriggerEff_UL%s%s_mc_fit_Fits_dielectron_mass_pt_eta_bins.root'%(path_root,year,VFPtag),'READ')
            self.etau_mc_hist_fit = etau_mc_file_fit.Get("dielectron_mass_pt_eta_bins")
            self.etau_mc_hist_fit.SetDirectory(0)
            etau_mc_file_fit.Close()
            
            etauSLF_data_file_fit = TFile('%setautriggerSLFEff_UL%s%s_data_fit_Fits_dielectron_mass_pt_eta_bins.root'%(path_root,year,VFPtag),'READ')
            self.etauSLF_data_hist_fit = etauSLF_data_file_fit.Get("dielectron_mass_pt_eta_bins")
            self.etauSLF_data_hist_fit.SetDirectory(0)
            etauSLF_data_file_fit.Close()
            etauSLF_mc_file_fit = TFile('%setautriggerSLFEff_UL%s%s_mc_fit_Fits_dielectron_mass_pt_eta_bins.root'%(path_root,year,VFPtag),'READ')
            self.etauSLF_mc_hist_fit = etauSLF_mc_file_fit.Get("dielectron_mass_pt_eta_bins")
            self.etauSLF_mc_hist_fit.SetDirectory(0)
            etauSLF_mc_file_fit.Close()
        #up
        e_data_file_up = TFile('%setriggerEff_UL%s%s_data_up_Fits_dielectron_mass_pt_eta_bins.root'%(path_root,year,VFPtag),'READ')
        self.e_data_hist_up = e_data_file_up.Get("dielectron_mass_pt_eta_bins")
        self.e_data_hist_up.SetDirectory(0)
        e_data_file_up.Close()
        e_mc_file_up = TFile('%setriggerEff_UL%s%s_mc_up_Fits_dielectron_mass_pt_eta_bins.root'%(path_root,year,VFPtag),'READ')
        self.e_mc_hist_up = e_mc_file_up.Get("dielectron_mass_pt_eta_bins")
        self.e_mc_hist_up.SetDirectory(0)
        e_mc_file_up.Close()

        if self.year!=2016 or self.VFPtag=="_preVFP":
            etau_data_file_up = TFile('%setautriggerEff_UL%s%s_data_up_Fits_dielectron_mass_pt_eta_bins.root'%(path_root,year,VFPtag),'READ')
            self.etau_data_hist_up = etau_data_file_up.Get("dielectron_mass_pt_eta_bins")
            self.etau_data_hist_up.SetDirectory(0)
            etau_data_file_up.Close()
            etau_mc_file_up = TFile('%setautriggerEff_UL%s%s_mc_up_Fits_dielectron_mass_pt_eta_bins.root'%(path_root,year,VFPtag),'READ')
            self.etau_mc_hist_up = etau_mc_file_up.Get("dielectron_mass_pt_eta_bins")
            self.etau_mc_hist_up.SetDirectory(0)
            etau_mc_file_up.Close()
        
            etauSLF_data_file_up = TFile('%setautriggerSLFEff_UL%s%s_data_up_Fits_dielectron_mass_pt_eta_bins.root'%(path_root,year,VFPtag),'READ')
            self.etauSLF_data_hist_up = etauSLF_data_file_up.Get("dielectron_mass_pt_eta_bins")
            self.etauSLF_data_hist_up.SetDirectory(0)
            etauSLF_data_file_up.Close()
            etauSLF_mc_file_up = TFile('%setautriggerSLFEff_UL%s%s_mc_up_Fits_dielectron_mass_pt_eta_bins.root'%(path_root,year,VFPtag),'READ')
            self.etauSLF_mc_hist_up = etauSLF_mc_file_up.Get("dielectron_mass_pt_eta_bins")
            self.etauSLF_mc_hist_up.SetDirectory(0)
            etauSLF_mc_file_up.Close()

        #down
        e_data_file_down = TFile('%setriggerEff_UL%s%s_data_down_Fits_dielectron_mass_pt_eta_bins.root'%(path_root,year,VFPtag),'READ')
        self.e_data_hist_down = e_data_file_down.Get("dielectron_mass_pt_eta_bins")
        self.e_data_hist_down.SetDirectory(0)
        e_data_file_down.Close()
        e_mc_file_down = TFile('%setriggerEff_UL%s%s_mc_down_Fits_dielectron_mass_pt_eta_bins.root'%(path_root,year,VFPtag),'READ')
        self.e_mc_hist_down = e_mc_file_down.Get("dielectron_mass_pt_eta_bins")
        self.e_mc_hist_down.SetDirectory(0)
        e_mc_file_down.Close()
        
        if self.year!=2016 or self.VFPtag=="_preVFP":
            etau_data_file_down = TFile('%setautriggerEff_UL%s%s_data_down_Fits_dielectron_mass_pt_eta_bins.root'%(path_root,year,VFPtag),'READ')
            self.etau_data_hist_down = etau_data_file_down.Get("dielectron_mass_pt_eta_bins")
            self.etau_data_hist_down.SetDirectory(0)
            etau_data_file_down.Close()
            etau_mc_file_down = TFile('%setautriggerEff_UL%s%s_mc_down_Fits_dielectron_mass_pt_eta_bins.root'%(path_root,year,VFPtag),'READ')
            self.etau_mc_hist_down = etau_mc_file_down.Get("dielectron_mass_pt_eta_bins")
            self.etau_mc_hist_down.SetDirectory(0)
            etau_mc_file_down.Close()
        
            etauSLF_data_file_down = TFile('%setautriggerSLFEff_UL%s%s_data_down_Fits_dielectron_mass_pt_eta_bins.root'%(path_root,year,VFPtag),'READ')
            self.etauSLF_data_hist_down = etauSLF_data_file_down.Get("dielectron_mass_pt_eta_bins")
            self.etauSLF_data_hist_down.SetDirectory(0)
            etauSLF_data_file_down.Close()
            etauSLF_mc_file_down = TFile('%setautriggerSLFEff_UL%s%s_mc_down_Fits_dielectron_mass_pt_eta_bins.root'%(path_root,year,VFPtag),'READ')
            self.etauSLF_mc_hist_down = etauSLF_mc_file_down.Get("dielectron_mass_pt_eta_bins")
            self.etauSLF_mc_hist_down.SetDirectory(0)
            etauSLF_mc_file_down.Close()

        #gen
        e_mc_file_gen = TFile('%setriggerEff_UL%s%s_mc_gen_Fits_dielectron_mass_pt_eta_bins.root'%(path_root,year,VFPtag),'READ')
        self.e_mc_hist_gen = e_mc_file_gen.Get("dielectron_mass_pt_eta_bins")
        self.e_mc_hist_gen.SetDirectory(0)
        e_mc_file_gen.Close()
        
        if self.year!=2016 or self.VFPtag=="_preVFP":
            etau_mc_file_gen = TFile('%setautriggerEff_UL%s%s_mc_gen_Fits_dielectron_mass_pt_eta_bins.root'%(path_root,year,VFPtag),'READ')
            self.etau_mc_hist_gen = etau_mc_file_gen.Get("dielectron_mass_pt_eta_bins")
            self.etau_mc_hist_gen.SetDirectory(0)
            etau_mc_file_gen.Close()
            
            etauSLF_mc_file_gen = TFile('%setautriggerSLFEff_UL%s%s_mc_gen_Fits_dielectron_mass_pt_eta_bins.root'%(path_root,year,VFPtag),'READ')
            self.etauSLF_mc_hist_gen = etauSLF_mc_file_gen.Get("dielectron_mass_pt_eta_bins")
            self.etauSLF_mc_hist_gen.SetDirectory(0)
            etauSLF_mc_file_gen.Close()
        

    def getTauTriggerEff(self, pt, dm, channel,wp):
        if dm==2:
            print("decaymode 2 for tautrigger SF, changed to dm 1")
            dm=1
        Eff_tau_data = self.taujson["tau_trigger"].evaluate(pt,dm,channel,wp,"eff_data","nom")
        Eff_tau_mc = self.taujson["tau_trigger"].evaluate(pt,dm,channel,wp,"eff_mc","nom")
        return [Eff_tau_data,Eff_tau_mc]

    def getTauTriggerEffOld(self, pt, dm, channel,wp):
        if dm==2:
            print("decaymode 2 for tautrigger SF, changed to dm 1")
            dm=1
        if channel=="mutau":
            if wp == "Medium":
                Eff_tau_data = self.tauTriggerTool_mutau_medium.getEff_data(pt,dm)
                Eff_tau_mc = self.tauTriggerTool_mutau_medium.getEff_mc(pt,dm)
            else:
                Eff_tau_data = self.tauTriggerTool_mutau_vvvloose.getEff_data(pt,dm)
                Eff_tau_mc = self.tauTriggerTool_mutau_vvvloose.getEff_mc(pt,dm)
        elif channel=="etau":
            if wp == "Medium":
                Eff_tau_data = self.tauTriggerTool_etau_medium.getEff_data(pt,dm)
                Eff_tau_mc = self.tauTriggerTool_etau_medium.getEff_mc(pt,dm)
            else:
                Eff_tau_data = self.tauTriggerTool_etau_vvvloose.getEff_data(pt,dm)
                Eff_tau_mc = self.tauTriggerTool_etau_vvvloose.getEff_mc(pt,dm)
        return [Eff_tau_data,Eff_tau_mc]

    def getBinContent(self,hist,pt,eta):
        low_pt = hist.GetXaxis().GetBinCenter(1)
        high_pt = hist.GetXaxis().GetBinCenter(hist.GetNbinsX())
        high_eta = hist.GetYaxis().GetBinCenter(hist.GetNbinsY())
        if pt<low_pt: pt = low_pt
        if pt>high_pt: pt = high_pt
        if abs(eta)>high_eta: eta=high_eta
        return hist.GetBinContent(hist.GetXaxis().FindBin(pt),hist.GetYaxis().FindBin(abs(eta)))

    def getLepTriggerEff(self,channel,pt,eta):
        if channel=="mutau":
            sl_eff_data = self.getBinContent(self.mu_data_hist,pt,eta)
            sl_eff_mc = self.getBinContent(self.mu_mc_hist,pt,eta)
            cross_eff_data = self.getBinContent(self.mutau_data_hist,pt,eta)
            cross_eff_mc = self.getBinContent(self.mutau_mc_hist,pt,eta)
            crossSLF_eff_data = self.getBinContent(self.mutauSLF_data_hist,pt,eta)
            crossSLF_eff_mc = self.getBinContent(self.mutauSLF_mc_hist,pt,eta)
        elif channel=="etau":
            sl_eff_data = self.getBinContent(self.e_data_hist,pt,eta)
            sl_eff_mc = self.getBinContent(self.e_mc_hist,pt,eta)
            if self.year!=2016 or self.VFPtag=="_preVFP":
                cross_eff_data = self.getBinContent(self.etau_data_hist,pt,eta)
                cross_eff_mc = self.getBinContent(self.etau_mc_hist,pt,eta)
                crossSLF_eff_data = self.getBinContent(self.etauSLF_data_hist,pt,eta)
                crossSLF_eff_mc = self.getBinContent(self.etauSLF_mc_hist,pt,eta)
            else:
                cross_eff_data = 0.
                cross_eff_mc = 0.
                crossSLF_eff_data = 0.
                crossSLF_eff_mc = 0.
        return [sl_eff_data,sl_eff_mc,cross_eff_data,cross_eff_mc,crossSLF_eff_data,crossSLF_eff_mc]
    
    def getLepTriggerEffFit(self,channel,pt,eta):
        if channel=="mutau":
            sl_eff_data = self.getBinContent(self.mu_data_hist_fit,pt,eta)
            sl_eff_mc = self.getBinContent(self.mu_mc_hist_fit,pt,eta)
            cross_eff_data = self.getBinContent(self.mutau_data_hist_fit,pt,eta)
            cross_eff_mc = self.getBinContent(self.mutau_mc_hist_fit,pt,eta)
            crossSLF_eff_data = self.getBinContent(self.mutauSLF_data_hist_fit,pt,eta)
            crossSLF_eff_mc = self.getBinContent(self.mutauSLF_mc_hist_fit,pt,eta)
        elif channel=="etau":
            sl_eff_data = self.getBinContent(self.e_data_hist_fit,pt,eta)
            sl_eff_mc = self.getBinContent(self.e_mc_hist_fit,pt,eta)
            if self.year!=2016 or self.VFPtag=="_preVFP":
                cross_eff_data = self.getBinContent(self.etau_data_hist_fit,pt,eta)
                cross_eff_mc = self.getBinContent(self.etau_mc_hist_fit,pt,eta)
                crossSLF_eff_data = self.getBinContent(self.etauSLF_data_hist_fit,pt,eta)
                crossSLF_eff_mc = self.getBinContent(self.etauSLF_mc_hist_fit,pt,eta)
            else:
                cross_eff_data = 0.
                cross_eff_mc = 0.
                crossSLF_eff_data = 0.
                crossSLF_eff_mc = 0.
        return [sl_eff_data,sl_eff_mc,cross_eff_data,cross_eff_mc,crossSLF_eff_data,crossSLF_eff_mc]
    
    def getLepTriggerEffUp(self,channel,pt,eta):
        if channel=="mutau":
            sl_eff_data = self.getBinContent(self.mu_data_hist_up,pt,eta)
            sl_eff_mc = self.getBinContent(self.mu_mc_hist_up,pt,eta)
            cross_eff_data = self.getBinContent(self.mutau_data_hist_up,pt,eta)
            cross_eff_mc = self.getBinContent(self.mutau_mc_hist_up,pt,eta)
            crossSLF_eff_data = self.getBinContent(self.mutauSLF_data_hist_up,pt,eta)
            crossSLF_eff_mc = self.getBinContent(self.mutauSLF_mc_hist_up,pt,eta)
        elif channel=="etau":
            sl_eff_data = self.getBinContent(self.e_data_hist_up,pt,eta)
            sl_eff_mc = self.getBinContent(self.e_mc_hist_up,pt,eta)
            if self.year!=2016 or self.VFPtag=="_preVFP":
                cross_eff_data = self.getBinContent(self.etau_data_hist_up,pt,eta)
                cross_eff_mc = self.getBinContent(self.etau_mc_hist_up,pt,eta)
                crossSLF_eff_data = self.getBinContent(self.etauSLF_data_hist_up,pt,eta)
                crossSLF_eff_mc = self.getBinContent(self.etauSLF_mc_hist_up,pt,eta)
            else:
                cross_eff_data = 0.
                cross_eff_mc = 0.
                crossSLF_eff_data = 0.
                crossSLF_eff_mc = 0.
        return [sl_eff_data,sl_eff_mc,cross_eff_data,cross_eff_mc,crossSLF_eff_data,crossSLF_eff_mc]

    def getLepTriggerEffDown(self,channel,pt,eta):
        if channel=="mutau":
            sl_eff_data = self.getBinContent(self.mu_data_hist_down,pt,eta)
            sl_eff_mc = self.getBinContent(self.mu_mc_hist_down,pt,eta)
            cross_eff_data = self.getBinContent(self.mutau_data_hist_down,pt,eta)
            cross_eff_mc = self.getBinContent(self.mutau_mc_hist_down,pt,eta)
            crossSLF_eff_data = self.getBinContent(self.mutauSLF_data_hist_down,pt,eta)
            crossSLF_eff_mc = self.getBinContent(self.mutauSLF_mc_hist_down,pt,eta)
        elif channel=="etau":
            sl_eff_data = self.getBinContent(self.e_data_hist_down,pt,eta)
            sl_eff_mc = self.getBinContent(self.e_mc_hist_down,pt,eta)
            if self.year!=2016 or self.VFPtag=="_preVFP":
                cross_eff_data = self.getBinContent(self.etau_data_hist_down,pt,eta)
                cross_eff_mc = self.getBinContent(self.etau_mc_hist_down,pt,eta)
                crossSLF_eff_data = self.getBinContent(self.etauSLF_data_hist_down,pt,eta)
                crossSLF_eff_mc = self.getBinContent(self.etauSLF_mc_hist_down,pt,eta)
            else:
                cross_eff_data = 0.
                cross_eff_mc = 0.
                crossSLF_eff_data = 0.
                crossSLF_eff_mc = 0.
        return [sl_eff_data,sl_eff_mc,cross_eff_data,cross_eff_mc,crossSLF_eff_data,crossSLF_eff_mc]
        
    def getLepTriggerEffGen(self,channel,pt,eta):
        if channel=="mutau":
            sl_eff_data = self.getBinContent(self.mu_data_hist,pt,eta)
            sl_eff_mc = self.getBinContent(self.mu_mc_hist_gen,pt,eta)
            cross_eff_data = self.getBinContent(self.mutau_data_hist,pt,eta)
            cross_eff_mc = self.getBinContent(self.mutau_mc_hist_gen,pt,eta)
            crossSLF_eff_data = self.getBinContent(self.mutauSLF_data_hist,pt,eta)
            crossSLF_eff_mc = self.getBinContent(self.mutauSLF_mc_hist_gen,pt,eta)
        elif channel=="etau":
            sl_eff_data = self.getBinContent(self.e_data_hist,pt,eta)
            sl_eff_mc = self.getBinContent(self.e_mc_hist_gen,pt,eta)
            if self.year!=2016 or self.VFPtag=="_preVFP":
                cross_eff_data = self.getBinContent(self.etau_data_hist,pt,eta)
                cross_eff_mc = self.getBinContent(self.etau_mc_hist_gen,pt,eta)
                crossSLF_eff_data = self.getBinContent(self.etauSLF_data_hist,pt,eta)
                crossSLF_eff_mc = self.getBinContent(self.etauSLF_mc_hist_gen,pt,eta)
            else:
                cross_eff_data = 0.
                cross_eff_mc = 0.
                crossSLF_eff_data = 0.
                crossSLF_eff_mc = 0.
        return [sl_eff_data,sl_eff_mc,cross_eff_data,cross_eff_mc,crossSLF_eff_data,crossSLF_eff_mc]


    def TriggerSF_onlySL(self,channel,lep_pt,lep_eta,tau_pt,tau_dm,tau_wp,var):
        tautriggerEff=self.getTauTriggerEff(tau_pt,tau_dm,channel,tau_wp)
        eff_tau_data = tautriggerEff[0]
        eff_tau_mc = tautriggerEff[1]
        if var=="": leptriggerEff = self.getLepTriggerEff(channel,lep_pt,abs(lep_eta))
        elif var=="fit": leptriggerEff = self.getLepTriggerEffFit(channel,lep_pt,abs(lep_eta))
        elif var=="gen": leptriggerEff = self.getLepTriggerEffGen(channel,lep_pt,abs(lep_eta))
        elif var=="up": leptriggerEff = self.getLepTriggerEffUp(channel,lep_pt,abs(lep_eta))
        elif var=="down": leptriggerEff = self.getLepTriggerEffDown(channel,lep_pt,abs(lep_eta))
        eff_lep_sl_data = leptriggerEff[0]
        eff_lep_sl_mc = leptriggerEff[1]
        eff_lep_cross_data = leptriggerEff[2]
        eff_lep_cross_mc = leptriggerEff[3]
        eff_lep_crossSLF_data = leptriggerEff[4] 
        eff_lep_crossSLF_mc = leptriggerEff[5]
        num = eff_lep_sl_data * (1 - eff_lep_crossSLF_data * eff_tau_data)
        den = eff_lep_sl_mc * (1 - eff_lep_crossSLF_mc * eff_tau_mc)
        return num/den

    def TriggerSF_onlyCross(self,channel,lep_pt,lep_eta,tau_pt,tau_dm,tau_wp,var):
        tautriggerEff=self.getTauTriggerEff(tau_pt,tau_dm,channel,tau_wp)
        eff_tau_data = tautriggerEff[0]
        eff_tau_mc = tautriggerEff[1]
        if var=="": leptriggerEff = self.getLepTriggerEff(channel,lep_pt,abs(lep_eta))
        elif var=="fit": leptriggerEff = self.getLepTriggerEffFit(channel,lep_pt,abs(lep_eta))
        elif var=="gen": leptriggerEff = self.getLepTriggerEffGen(channel,lep_pt,abs(lep_eta))
        elif var=="up": leptriggerEff = self.getLepTriggerEffUp(channel,lep_pt,abs(lep_eta))
        elif var=="down": leptriggerEff = self.getLepTriggerEffDown(channel,lep_pt,abs(lep_eta))
        eff_lep_sl_data = leptriggerEff[0]
        eff_lep_sl_mc = leptriggerEff[1]
        eff_lep_cross_data = leptriggerEff[2]
        eff_lep_cross_mc = leptriggerEff[3]
        eff_lep_crossSLF_data = leptriggerEff[4] 
        eff_lep_crossSLF_mc = leptriggerEff[5]
        num = (eff_lep_cross_data - eff_lep_crossSLF_data * eff_lep_sl_data) * eff_tau_data
        den = (eff_lep_cross_mc - eff_lep_crossSLF_mc * eff_lep_sl_mc) * eff_tau_mc
        if num/den<0. or num/den>5.:
            return self.TriggerSF_onlyCross_FIX(channel,lep_pt,lep_eta,tau_pt,tau_dm,tau_wp,var)
        else:
            return num/den

    def TriggerSF_onlyCross_FIX(self,channel,lep_pt,lep_eta,tau_pt,tau_dm,tau_wp,var):
        if channel == "mutau":
            lower_pt = self.mutau_data_hist.GetXaxis().GetBinCenter(self.mutau_data_hist.GetXaxis().FindBin(lep_pt)-1)
        elif channel == "etau":
            lower_pt = self.etau_data_hist.GetXaxis().GetBinCenter(self.etau_data_hist.GetXaxis().FindBin(lep_pt)-1)
        return self.TriggerSF_onlyCross(channel,lower_pt,lep_eta,tau_pt,tau_dm,tau_wp,var)    

    def TriggerSF_both(self,channel,lep_pt,lep_eta,tau_pt,tau_dm,tau_wp,var):
        tautriggerEff=self.getTauTriggerEff(tau_pt,tau_dm,channel,tau_wp)
        eff_tau_data = tautriggerEff[0]
        eff_tau_mc = tautriggerEff[1]
        if var=="": leptriggerEff = self.getLepTriggerEff(channel,lep_pt,abs(lep_eta))
        elif var=="fit": leptriggerEff = self.getLepTriggerEffFit(channel,lep_pt,abs(lep_eta))
        elif var=="gen": leptriggerEff = self.getLepTriggerEffGen(channel,lep_pt,abs(lep_eta))
        elif var=="up": leptriggerEff = self.getLepTriggerEffUp(channel,lep_pt,abs(lep_eta))
        elif var=="down": leptriggerEff = self.getLepTriggerEffDown(channel,lep_pt,abs(lep_eta))
        eff_lep_sl_data = leptriggerEff[0]
        eff_lep_sl_mc = leptriggerEff[1]
        eff_lep_crossSLF_data = leptriggerEff[4] 
        eff_lep_crossSLF_mc = leptriggerEff[5]
        num = eff_lep_crossSLF_data * eff_lep_sl_data * eff_tau_data
        den = eff_lep_crossSLF_mc * eff_lep_sl_mc * eff_tau_mc
        return num/den
    
    def getTriggerSF(self,channel,lep_pt,lep_eta,tau_pt,tau_dm,tau_wp,slfired,crossfired):
        if slfired and not crossfired:
            return self.TriggerSF_onlySL(channel,lep_pt,lep_eta,tau_pt,tau_dm,tau_wp,"")
        elif not slfired and crossfired:
            return self.TriggerSF_onlyCross(channel,lep_pt,lep_eta,tau_pt,tau_dm,tau_wp,"")
        elif slfired and crossfired:
            return self.TriggerSF_both(channel,lep_pt,lep_eta,tau_pt,tau_dm,tau_wp,"")
       

    def TriggerSFError_onlySL(self,channel,lep_pt,lep_eta,tau_pt,tau_dm,tau_wp):
        SFFit = self.TriggerSF_onlySL(channel,lep_pt,lep_eta,tau_pt,tau_dm,tau_wp,"fit")
        SFGen = self.TriggerSF_onlySL(channel,lep_pt,lep_eta,tau_pt,tau_dm,tau_wp,"gen")
        SFUp = self.TriggerSF_onlySL(channel,lep_pt,lep_eta,tau_pt,tau_dm,tau_wp,"up")
        SFDown = self.TriggerSF_onlySL(channel,lep_pt,lep_eta,tau_pt,tau_dm,tau_wp,"down")
        return [SFFit,SFGen,SFUp,SFDown]

    def TriggerSFError_onlyCross(self,channel,lep_pt,lep_eta,tau_pt,tau_dm,tau_wp):
        SFFit = self.TriggerSF_onlyCross(channel,lep_pt,lep_eta,tau_pt,tau_dm,tau_wp,"fit")
        SFGen = self.TriggerSF_onlyCross(channel,lep_pt,lep_eta,tau_pt,tau_dm,tau_wp,"gen")
        SFUp = self.TriggerSF_onlyCross(channel,lep_pt,lep_eta,tau_pt,tau_dm,tau_wp,"up")
        SFDown = self.TriggerSF_onlyCross(channel,lep_pt,lep_eta,tau_pt,tau_dm,tau_wp,"down")
        return [SFFit,SFGen,SFUp,SFDown]
    
    def TriggerSFError_both(self,channel,lep_pt,lep_eta,tau_pt,tau_dm,tau_wp):
        SFFit = self.TriggerSF_both(channel,lep_pt,lep_eta,tau_pt,tau_dm,tau_wp,"fit")
        SFGen = self.TriggerSF_both(channel,lep_pt,lep_eta,tau_pt,tau_dm,tau_wp,"gen")
        SFUp = self.TriggerSF_both(channel,lep_pt,lep_eta,tau_pt,tau_dm,tau_wp,"up")
        SFDown = self.TriggerSF_both(channel,lep_pt,lep_eta,tau_pt,tau_dm,tau_wp,"down")
        return [SFFit,SFGen,SFUp,SFDown]


    def getTriggerSFError(self,channel,lep_pt,lep_eta,tau_pt,tau_dm,tau_wp,slfired,crossfired):
        if slfired and not crossfired:
            return [abs(SF-self.TriggerSF_onlySL(channel,lep_pt,lep_eta,tau_pt,tau_dm,tau_wp,"")) for SF in self.TriggerSFError_onlySL(channel,lep_pt,lep_eta,tau_pt,tau_dm,tau_wp)]
        elif not slfired and crossfired:
            return [abs(SF-self.TriggerSF_onlyCross(channel,lep_pt,lep_eta,tau_pt,tau_dm,tau_wp,"")) for SF in self.TriggerSFError_onlyCross(channel,lep_pt,lep_eta,tau_pt,tau_dm,tau_wp)]
        elif slfired and crossfired:
            return [abs(SF-self.TriggerSF_both(channel,lep_pt,lep_eta,tau_pt,tau_dm,tau_wp,"")) for SF in self.TriggerSFError_both(channel,lep_pt,lep_eta,tau_pt,tau_dm,tau_wp)]

    def getTriggerSF_MuMu(self,mu1_pt,mu1_eta,mu2_pt,mu2_eta):
        mu1triggerEff = self.getLepTriggerEff("mutau",mu1_pt,abs(mu1_eta))
        mu2triggerEff = self.getLepTriggerEff("mutau",mu2_pt,abs(mu2_eta))
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
        mutriggerEff = self.getLepTriggerEff("mutau",mu_pt,abs(mu_eta))
        etriggerEff = self.getLepTriggerEff("etau",e_pt,abs(e_eta))
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

    def getTriggerSF_SL(self,channel,lep_pt,lep_eta):
        leptriggerEff = self.getLepTriggerEff(channel,lep_pt,abs(lep_eta))
        eff_lep_sl_data = leptriggerEff[0]
        eff_lep_sl_mc = leptriggerEff[1]
        num = eff_lep_sl_data
        den = eff_lep_sl_mc
        return num/den

    def getTriggerSF_Cross(self,channel,lep_pt,lep_eta,tau_pt,tau_dm,tau_wp):
        tautriggerEff=self.getTauTriggerEff(tau_pt,tau_dm,channel,tau_wp)
        eff_tau_data = tautriggerEff[0]
        eff_tau_mc = tautriggerEff[1]
        leptriggerEff = self.getLepTriggerEff(channel,lep_pt,abs(lep_eta))
        eff_lep_cross_data = leptriggerEff[2]
        eff_lep_cross_mc = leptriggerEff[3]
        num = eff_lep_cross_data * eff_tau_data
        den = eff_lep_cross_mc * eff_tau_mc
        if den!=0:
            return num/den
        else:
            return 1.

    def getTriggerSF_CrossOld(self,channel,lep_pt,lep_eta,tau_pt,tau_dm,tau_wp):
        tautriggerEff=self.getTauTriggerEffOld(tau_pt,tau_dm,channel,tau_wp)
        eff_tau_data = tautriggerEff[0]
        eff_tau_mc = tautriggerEff[1]
        leptriggerEff = self.getLepTriggerEff(channel,lep_pt,abs(lep_eta))
        eff_lep_cross_data = leptriggerEff[2]
        eff_lep_cross_mc = leptriggerEff[3]
        num = eff_lep_cross_data * eff_tau_data
        den = eff_lep_cross_mc * eff_tau_mc
        if den!=0:
            return num/den
        else:
            return 1.

    def getTriggerSF_lepCross(self,channel,lep_pt,lep_eta,tau_pt,tau_dm,tau_wp):
        leptriggerEff = self.getLepTriggerEff(channel,lep_pt,abs(lep_eta))
        eff_lep_cross_data = leptriggerEff[2]
        eff_lep_cross_mc = leptriggerEff[3]
        num = eff_lep_cross_data
        den = eff_lep_cross_mc
        if den!=0:
            return num/den
        else:
            return 1.
    
    def getTriggerSF_tauCross(self,channel,lep_pt,lep_eta,tau_pt,tau_dm,tau_wp):
        tautriggerEff=self.getTauTriggerEff(tau_pt,tau_dm,channel,tau_wp)
        eff_tau_data = tautriggerEff[0]
        eff_tau_mc = tautriggerEff[1]
        num = eff_tau_data
        den = eff_tau_mc
        if den!=0:
            return num/den
        else:
            return 1.
    
    
if __name__=="__main__":
    parser = ArgumentParser()
    parser.add_argument('-y', '--year',    dest='year', choices=[2016,2017,2018], type=int, default=2018, action='store')
    parser.add_argument('-p', '--preVFP',  dest='preVFP', action='store_const', const="_preVFP",default="")
    parser.add_argument('-r', '--realm', dest='realm', action='store',default="")
    args = parser.parse_args()
    realm = args.realm
    regions = ["onlySL","onlyCross","both"]
    channels = ["mutau","etau"]
    #channels = ["mutau"]
    year = args.year
    VFPtag = args.preVFP
    ROOT.gROOT.SetBatch(ROOT.kTRUE)
    if year!=2016:
        mu_pt = [25., 26., 27., 28., 29., 30., 31., 32., 33., 34., 35., 40., 45., 50. ,75., 100., 200.]
        #mu_pt = [25.,30.,35.,40.,50., 75., 200.]
        mu_pt_low = [25., 26., 27., 28., 29., 30., 31., 32., 33., 34., 35.]
        mu_pt_high = [35., 40., 45., 50. ,75., 100., 200.]
    else:
        mu_pt = [23., 24., 25., 26., 27., 28., 29., 30., 31., 32., 33., 34., 35., 40., 45., 50. ,75., 100., 200.]
        mu_pt_low = [23., 24., 25., 26., 27., 28., 29., 30., 31., 32., 33., 34., 35.]
        mu_pt_high = [35., 40., 45., 50. ,75., 100., 200.]
    mutau_pt = [21., 22., 23., 24., 25., 26., 27., 28., 29., 30., 35., 40., 45., 50. ,75., 100., 200.]
    #mutau_pt = [25.,30.,35.,40.,50., 75., 200.]
    mutau_pt_low = [21., 22., 23., 24., 25., 26., 27., 28., 29., 30.]
    mutau_pt_high = [30., 35., 40., 45., 50. ,75., 100., 200.]
    mu_eta =  [0., 0.9, 1.2, 2.1, 2.4]
    mutau_eta = [0., 0.9, 1.2, 2.1]
    if year!=2016:
        e_pt = [33., 34., 35., 36., 37., 38., 39., 40., 45., 50. ,75., 100., 200.]
        e_pt_low = [33., 34., 35., 36., 37., 38., 39., 40.]
        e_pt_high = [40., 45., 50. ,75., 100., 200.]
    else:
        e_pt = [26., 27., 28., 29., 30., 31., 32., 33., 34., 35., 36., 37., 38., 39., 40., 45., 50. ,75., 100., 200.]
        e_pt_low = [26., 27., 28., 29., 30., 31., 32., 33., 34., 35., 36., 37., 38., 39., 40.]
        e_pt_high = [40., 45., 50. ,75., 100., 200.]
    etau_pt = [25., 26., 27., 28., 29.,  30., 31., 32., 33., 34., 35., 40., 45., 50. ,75., 100., 200.]
    etau_pt_low = [25., 26., 27., 28., 29.,  30., 31., 32., 33., 34., 35.]
    etau_pt_high = [35., 40., 45., 50. ,75., 100., 200.]
    e_eta = [0., 0.8, 1.444, 1.566, 2., 2.1]
    etau_eta = [0., 0.8, 1.444, 1.566, 2., 2.1]
    tau_pt = 40.
    tau_dm = 0 #[0,10]
    tau_wp = "Medium" #["Medium","VVVLoose"]
    triggerSFs = TriggerSFs(year,VFPtag)

    for channel in channels:
        for region in regions:
            if channel == "mutau":
                if region=="onlySL":
                    lep_pt = mu_pt
                    lep_eta = mu_eta
                    lep_pt_low = mu_pt_low
                    lep_pt_high = mu_pt_high
                elif region=="onlyCross":
                    lep_pt = mutau_pt
                    lep_eta = mutau_eta
                    lep_pt_low = mutau_pt_low
                    lep_pt_high = mutau_pt_high
                else:
                    lep_pt = mu_pt #taking the shorter list
                    lep_eta = mutau_eta #taking the shorter list
                    lep_pt_low = mu_pt_low
                    lep_pt_high = mu_pt_high
            else:
                if year == 2016 and VFPtag=="" and region!="onlySL": continue
                if region in ["onlySL","both"]:
                    lep_pt = e_pt
                    lep_eta = e_eta
                    lep_pt_low = e_pt_low
                    lep_pt_high = e_pt_high
                else:
                    lep_pt = etau_pt
                    lep_eta = etau_eta
                    lep_pt_low = etau_pt_low
                    lep_pt_high = etau_pt_high
            Nbinsx = len(lep_pt)-1
            Nbinsy = len(lep_eta)-1
            Nbinsx_low = len(lep_pt_low)-1
            Nbinsx_high = len(lep_pt_high)-1

            if realm=="":
                outfile = TFile("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/triggerSF/root/triggerSF_%s_%s_UL%s%s.root"%(channel,region,year,VFPtag),"RECREATE")
            canv = TCanvas("triggerSF_%s_%s_UL%s%s"%(channel,region,year,VFPtag),"trigger SF %s %s UL%s%s"%(channel,region,year,VFPtag))
            hist = TH2D("triggerSF_%s_%s_UL%s%s"%(channel,region,year,VFPtag),"trigger SF %s %s UL%s%s"%(channel,region,year,VFPtag),Nbinsx,np.array(lep_pt),Nbinsy,np.array(lep_eta))
            hist_low = TH2D("triggerSF_%s_%s_UL%s%s_low"%(channel,region,year,VFPtag),"trigger SF %s %s UL%s%s"%(channel,region,year,VFPtag),Nbinsx_low,np.array(lep_pt_low),Nbinsy,np.array(lep_eta))
            hist_high = TH2D("triggerSF_%s_%s_UL%s%s_high"%(channel,region,year,VFPtag),"trigger SF %s %s UL%s%s"%(channel,region,year,VFPtag),Nbinsx_high,np.array(lep_pt_high),Nbinsy,np.array(lep_eta))
            gStyle.SetOptStat(0)
            for i,pt in enumerate(lep_pt[:-1]):
                pt = pt + 0.5
                i = i+1
                for j,eta in enumerate(lep_eta[:-1]):
                    eta = eta + 0.05
                    j = j+1
                    if region == "onlySL":
                        SF = triggerSFs.TriggerSF_onlySL(channel,pt,eta,tau_pt,tau_dm,tau_wp,"")
                    elif region == "onlyCross":
                        SF = triggerSFs.TriggerSF_onlyCross(channel,pt,eta,tau_pt,tau_dm,tau_wp,"")
                    elif region == "both":
                        SF = triggerSFs.TriggerSF_both(channel,pt,eta,tau_pt,tau_dm,tau_wp,"") 
                    if channel=="etau" and (eta>1.444 and eta<1.566):
                        SF = 1. #gap excluded in analysis
                    hist.SetBinContent(i,j,SF)
            for i,pt in enumerate(lep_pt_low[:-1]):
                pt = pt + 0.5
                i = i+1
                for j,eta in enumerate(lep_eta[:-1]):
                    eta = eta + 0.05
                    j = j+1
                    if region == "onlySL":
                        SF = triggerSFs.TriggerSF_onlySL(channel,pt,eta,tau_pt,tau_dm,tau_wp,"")
                    elif region == "onlyCross":
                        SF = triggerSFs.TriggerSF_onlyCross(channel,pt,eta,tau_pt,tau_dm,tau_wp,"")
                    elif region == "both":
                        SF = triggerSFs.TriggerSF_both(channel,pt,eta,tau_pt,tau_dm,tau_wp,"") 
                    if channel=="etau" and (eta>1.444 and eta<1.566):
                        SF = 1. #gap excluded in analysis
                    hist_low.SetBinContent(i,j,SF)
            for i,pt in enumerate(lep_pt_high[:-1]):
                pt = pt + 0.5
                i = i+1
                for j,eta in enumerate(lep_eta[:-1]):
                    eta = eta + 0.05
                    j = j+1
                    if region == "onlySL":
                        SF = triggerSFs.TriggerSF_onlySL(channel,pt,eta,tau_pt,tau_dm,tau_wp,"")
                    elif region == "onlyCross":
                        SF = triggerSFs.TriggerSF_onlyCross(channel,pt,eta,tau_pt,tau_dm,tau_wp,"")
                    elif region == "both":
                        SF = triggerSFs.TriggerSF_both(channel,pt,eta,tau_pt,tau_dm,tau_wp,"") 
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
            elif channel=="etau":
                hist.GetXaxis().SetTitle("e p_{T}")
                hist.GetYaxis().SetTitle("e |#eta|")
                hist_low.GetXaxis().SetTitle("e p_{T}")
                hist_low.GetYaxis().SetTitle("e |#eta|")
                hist_high.GetXaxis().SetTitle("e p_{T}")
                hist_high.GetYaxis().SetTitle("e |#eta|")
            #if region=="onlyCross":
            #    hist.GetZaxis().SetRangeUser(0.5,1.5)
            #hist.GetZaxis().SetRangeUser(-2,0.)
            gStyle.SetPaintTextFormat(".3f")
            if realm=="":
                hist.Draw("COLZ")
                canv.SaveAs("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/triggerSF/plots/triggerSF_%s_%s_UL%s%s.pdf"%(channel,region,year,VFPtag))
                canv.SaveAs("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/triggerSF/plots/triggerSF_%s_%s_UL%s%s.png"%(channel,region,year,VFPtag))
                hist.Write()
                outfile.Close()
            elif realm=="low":
                hist_low.Draw("COLZTEXT45")
                canv.SaveAs("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/triggerSF/plots/triggerSF_%s_%s_UL%s%s_low.pdf"%(channel,region,year,VFPtag))
                canv.SaveAs("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/triggerSF/plots/triggerSF_%s_%s_UL%s%s_low.png"%(channel,region,year,VFPtag))
            elif realm=="high":
                hist_high.Draw("COLZTEXT45")
                canv.SaveAs("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/triggerSF/plots/triggerSF_%s_%s_UL%s%s_high.pdf"%(channel,region,year,VFPtag))
                canv.SaveAs("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/triggerSF/plots/triggerSF_%s_%s_UL%s%s_high.png"%(channel,region,year,VFPtag))

            
            #SF errors
            for n,sys in enumerate(["Fit","Gen","Up","Down"]):
                if realm=="":
                    outfile = TFile("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/triggerSF/root/triggerSF%s_%s_%s_UL%s%s.root"%(sys,channel,region,year,VFPtag),"RECREATE")
                canv = TCanvas("triggerSF%s_%s_%s_UL%s%s"%(sys,channel,region,year,VFPtag),"trigger SF %s %s %s UL%s%s"%(sys,channel,region,year,VFPtag),1000,600)
                hist = TH2D("triggerSF%s_%s_%s_UL%s%s"%(sys,channel,region,year,VFPtag),"trigger SF %s %s %s UL%s%s"%(sys,channel,region,year,VFPtag),Nbinsx,np.array(lep_pt),Nbinsy,np.array(lep_eta))
                hist_low = TH2D("triggerSF%s_%s_%s_UL%s%s_low"%(sys,channel,region,year,VFPtag),"trigger SF %s %s %s UL%s%s"%(sys,channel,region,year,VFPtag),Nbinsx_low,np.array(lep_pt_low),Nbinsy,np.array(lep_eta))
                hist_high = TH2D("triggerSF%s_%s_%s_UL%s%s_high"%(sys,channel,region,year,VFPtag),"trigger SF %s %s %s UL%s%s"%(sys,channel,region,year,VFPtag),Nbinsx_high,np.array(lep_pt_high),Nbinsy,np.array(lep_eta))
                gStyle.SetOptStat(0)
                for i,pt in enumerate(lep_pt[:-1]):
                    pt = pt + 0.5
                    i = i+1
                    for j,eta in enumerate(lep_eta[:-1]):
                        eta = eta + 0.05
                        j = j+1
                        if region == "onlySL":
                            SFError = triggerSFs.getTriggerSFError(channel,pt,eta,tau_pt,tau_dm,tau_wp,True,False)[n]
                        elif region == "onlyCross":
                            SFError = triggerSFs.getTriggerSFError(channel,pt,eta,tau_pt,tau_dm,tau_wp,False,True)[n]
                        elif region == "both":
                            SFError = triggerSFs.getTriggerSFError(channel,pt,eta,tau_pt,tau_dm,tau_wp,True,True)[n]
                        if channel=="etau" and (eta>1.444 and eta<1.566):
                            SFError = 0. #gap excluded in analysis
                        hist.SetBinContent(i,j,SFError)
                for i,pt in enumerate(lep_pt_low[:-1]):
                    pt = pt + 0.5
                    i = i+1
                    for j,eta in enumerate(lep_eta[:-1]):
                        eta = eta + 0.05
                        j = j+1
                        if region == "onlySL":
                            SFError = triggerSFs.getTriggerSFError(channel,pt,eta,tau_pt,tau_dm,tau_wp,True,False)[n]
                        elif region == "onlyCross":
                            SFError = triggerSFs.getTriggerSFError(channel,pt,eta,tau_pt,tau_dm,tau_wp,False,True)[n]
                        elif region == "both":
                            SFError = triggerSFs.getTriggerSFError(channel,pt,eta,tau_pt,tau_dm,tau_wp,True,True)[n]
                        if channel=="etau" and (eta>1.444 and eta<1.566):
                            SFError = 0. #gap excluded in analysis
                        hist_low.SetBinContent(i,j,SFError)
                for i,pt in enumerate(lep_pt_high[:-1]):
                    pt = pt + 0.5
                    i = i+1
                    for j,eta in enumerate(lep_eta[:-1]):
                        eta = eta + 0.05
                        j = j+1
                        if region == "onlySL":
                            SFError = triggerSFs.getTriggerSFError(channel,pt,eta,tau_pt,tau_dm,tau_wp,True,False)[n]
                        elif region == "onlyCross":
                            SFError = triggerSFs.getTriggerSFError(channel,pt,eta,tau_pt,tau_dm,tau_wp,False,True)[n]
                        elif region == "both":
                            SFError = triggerSFs.getTriggerSFError(channel,pt,eta,tau_pt,tau_dm,tau_wp,True,True)[n]
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
                    canv.SaveAs("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/triggerSF/plots/Systematics/triggerSF%s_%s_%s_UL%s%s.pdf"%(sys,channel,region,year,VFPtag))
                    canv.SaveAs("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/triggerSF/plots/Systematics/triggerSF%s_%s_%s_UL%s%s.png"%(sys,channel,region,year,VFPtag))
                    hist.Write()
                    outfile.Close()
                elif realm=="low":
                    hist_low.Draw("COLZTEXT45")
                    canv.SaveAs("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/triggerSF/plots/Systematics/triggerSF%s_%s_%s_UL%s%s_low.pdf"%(sys,channel,region,year,VFPtag))
                    canv.SaveAs("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/triggerSF/plots/Systematics/triggerSF%s_%s_%s_UL%s%s_low.png"%(sys,channel,region,year,VFPtag))
                elif realm=="high":
                    hist_high.Draw("COLZTEXT45")
                    canv.SaveAs("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/triggerSF/plots/Systematics/triggerSF%s_%s_%s_UL%s%s_high.pdf"%(sys,channel,region,year,VFPtag))
                    canv.SaveAs("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/triggerSF/plots/Systematics/triggerSF%s_%s_%s_UL%s%s_high.png"%(sys,channel,region,year,VFPtag))
            
