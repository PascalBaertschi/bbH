import ROOT
from ROOT import TFile, TH1D, TCanvas, gStyle, TLegend, TLatex, TGraphErrors, TH2D
import correctionlib
import os
import numpy as np
from argparse import ArgumentParser
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
        ############
        
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
        


    def getBinContent(self,hist,pt,eta):
        low_pt = hist.GetXaxis().GetBinCenter(1)
        high_pt = hist.GetXaxis().GetBinCenter(hist.GetNbinsX())
        high_eta = hist.GetYaxis().GetBinCenter(hist.GetNbinsY())
        if pt<low_pt: pt = low_pt
        if pt>high_pt: pt = high_pt
        if abs(eta)>high_eta: eta=high_eta
        return [hist.GetBinContent(hist.GetXaxis().FindBin(pt),hist.GetYaxis().FindBin(abs(eta))),hist.GetBinError(hist.GetXaxis().FindBin(pt),hist.GetYaxis().FindBin(abs(eta)))]
        
    def getLepTriggerEff(self,channel,pt,eta,tau_pt,tau_dm):
        eff_tau_data = self.taujson["tau_trigger"].evaluate(tau_pt,tau_dm,channel,"Medium","eff_data","nom")
        eff_tau_mc = self.taujson["tau_trigger"].evaluate(tau_pt,tau_dm,channel,"Medium","eff_mc","nom")
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
                cross_eff_data = [0.,0.]
                cross_eff_mc = [0.,0.]
                crossSLF_eff_data = [0.,0.]
                crossSLF_eff_mc = [0.,0.]
        return [sl_eff_data[0],sl_eff_mc[0],cross_eff_data[0],cross_eff_mc[0],crossSLF_eff_data[0],crossSLF_eff_mc[0],sl_eff_data[1],sl_eff_mc[1],cross_eff_data[1],cross_eff_mc[1],crossSLF_eff_data[1],crossSLF_eff_mc[1],eff_tau_data,eff_tau_mc]
        

if __name__=="__main__":
    parser = ArgumentParser()
    parser.add_argument('-y', '--year',    dest='year', choices=[2016,2017,2018], type=int, default=2018, action='store')
    parser.add_argument('-p', '--preVFP',  dest='preVFP', action='store_const', const="_preVFP",default="")
    parser.add_argument('-s', '--sys', dest='sys', action='store',default="")
    parser.add_argument('-r', '--turn_on_region', dest='turn_on_region', action='store_true',default=False)
    args = parser.parse_args()
    year = args.year
    preVFP = args.preVFP
    sys= args.sys
    turn_on_region = args.turn_on_region
    channels = ["mutau","etau"]
    #channels = ["etau"]
    triggers = ["Cross"]
    ROOT.gROOT.SetBatch(ROOT.kTRUE)
    if year!=2016:
        if turn_on_region:
            mu_pt = [25., 26., 27., 28., 29., 30., 31., 32., 33., 34., 35., 40.]
            e_pt = [33., 34., 35., 36., 37., 38., 39., 40., 45.]
        else:
            mu_pt = [25., 26., 27., 28., 29., 30., 31., 32., 33., 34., 35., 40., 45., 50. ,75., 100.,200.]
            e_pt = [33., 34., 35., 36., 37., 38., 39., 40., 45., 50. ,75., 100., 200.]
    else:
        if turn_on_region:
            mu_pt = [23., 24., 25., 26., 27., 28., 29., 30., 31., 32., 33., 34., 35., 40.]
            e_pt = [26., 27., 28., 29., 30., 31., 32., 33., 34., 35., 36., 37., 38., 39., 40., 45.]
        else:
            mu_pt = [23., 24., 25., 26., 27., 28., 29., 30., 31., 32., 33., 34., 35., 40., 45., 50. ,75., 100.,200.]
            e_pt = [26., 27., 28., 29., 30., 31., 32., 33., 34., 35., 36., 37., 38., 39., 40., 45., 50. ,75., 100., 200.]
    if turn_on_region:
        mutau_pt = [20., 21., 22., 23., 24., 25., 26., 27., 28., 29., 30., 35.]
        etau_pt = [25., 26., 27., 28., 29., 30., 31., 32., 33., 34., 35., 40.]
    else:
        mutau_pt = [20., 21., 22., 23., 24., 25., 26., 27., 28., 29., 30., 35., 40., 45., 50. ,75., 100.,200.]
        etau_pt = [25., 26., 27., 28., 29., 30., 31., 32., 33., 34., 35., 40., 45., 50. ,75., 100., 200]

    mu_eta =  [0., 0.9, 1.2, 2.1, 2.4]
    mutau_eta = [0., 0.9, 1.2, 2.1]
    e_eta = [0., 0.8, 1.444, 1.566, 2., 2.1]
    etau_eta = [0., 0.8, 1.444, 1.566, 2., 2.1]
    tau_pt = [30., 31., 32., 33., 34., 35., 40., 45., 50. ,75., 100.,200.]
    triggerSFs = TriggerSFs(year,preVFP)
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
        for trigger in triggers:
            if channel=="mutau":
                lep_pt = mutau_pt
                lep_eta = mutau_eta
            elif channel=="etau":
                lep_pt = etau_pt
                lep_eta = etau_eta
            Nbinsx = len(lep_pt)-1
            eta_len = len(lep_eta)-1
            Nbinsy = len(tau_pt)-1
            mc_eff_muon_list = []
            mc_eff_tau_list = []
            data_eff_muon_list = []
            data_eff_tau_list = []
            for tau_dm in [0,10]:
                for i in range(eta_len):
                    eta_label = "eta%s-%s"%(lep_eta[i],lep_eta[i+1])
                    eta_label = eta_label.replace(".",",")
                    eta = lep_eta[i]+(lep_eta[i+1]-lep_eta[i])/2.
                    hist_data = TH2D("2D_data","cross trigger lep * tau eff data",Nbinsx,np.array(lep_pt),Nbinsy,np.array(tau_pt))
                    hist_mc = TH2D("2D_data","cross trigger lep * tau eff mc",Nbinsx,np.array(lep_pt),Nbinsy,np.array(tau_pt))
                    for f in range(Nbinsy):
                        pt_tau = tau_pt[f]+((tau_pt[f+1]-tau_pt[f])/2.)
                        data_eff_list = []
                        data_eff_error_list = []
                        mc_eff_list = []
                        mc_eff_error_list = []
                        data_pt_list = []
                        data_pt_error_list = []
                        mc_pt_list = []
                        mc_pt_error_list = []
                        zeros_list = []
                        for j in range(Nbinsx):
                            pt = lep_pt[j]+((lep_pt[j+1]-lep_pt[j])/2.)
                            pt_error = (lep_pt[j+1]-lep_pt[j])/2.
                            effs=triggerSFs.getLepTriggerEff(channel,pt,eta,pt_tau,tau_dm)
                            eff_data = effs[2]*effs[12]
                            eff_mc = effs[3]*effs[13]
                            effErr_data = effs[8]
                            effErr_mc = effs[9]
                            hist_data.SetBinContent(j+1,f+1,eff_data)
                            hist_mc.SetBinContent(j+1,f+1,eff_mc)
                            data_eff_list.append(eff_data)
                            mc_eff_list.append(eff_mc)
                            data_eff_error_list.append(effErr_data)
                            mc_eff_error_list.append(effErr_mc)
                            data_pt_list.append(pt)
                            mc_pt_list.append(pt)
                            data_pt_error_list.append(pt_error)
                            mc_pt_error_list.append(pt_error)
                            zeros_list.append(0.)
                        canv = TCanvas("triggerEff_%s_%s_%s_taupt%s_taudm%s_UL%s%s"%(channel,trigger,eta_label,pt_tau,tau_dm,year,preVFP),"%s trigger %s %s UL%s%s"%(trigger,channel,eta_label,year,preVFP))
                        graph_data = TGraphErrors(Nbinsx,np.array(data_pt_list),np.array(data_eff_list),np.array(data_pt_error_list),np.array(data_eff_error_list))
                        graph_mc = TGraphErrors(Nbinsx,np.array(mc_pt_list),np.array(mc_eff_list),np.array(mc_pt_error_list),np.array(mc_eff_error_list))
               
                        if channel=="mutau":
                            graph_data.GetXaxis().SetTitle("#mu p_{T} [GeV]")
                        elif channel=="etau":
                            graph_data.GetXaxis().SetTitle("e p_{T} [GeV]")
                        graph_data.GetYaxis().SetTitle("efficiency")
                        graph_data.SetMarkerStyle(21)
                        graph_mc.SetMarkerStyle(20)
                        graph_data.SetMarkerColor(1)
                        graph_mc.SetMarkerColor(2)
                        graph_data.SetLineColor(1)
                        graph_mc.SetLineColor(2)
                        graph_data.SetTitle("")
                        graph_data.GetYaxis().SetRangeUser(0.,1.1)
                        #graph_data.GetYaxis().SetRangeUser(0.5,1.25)
                        leg = TLegend(0.7,0.4,0.85,0.55)
                        #leg = TLegend(0.7,0.3,0.85,0.45)
                        leg = TLegend(0.7,0.4,0.85,0.55)
                        leg.AddEntry(graph_data,"data","p")
                        leg.AddEntry(graph_mc,"mc","p")
                        leg.SetBorderSize(0)
                        graph_data.Draw("AP0")
                        graph_mc.Draw("P0 SAME")
                        leg.Draw("SAME")
                        latex = TLatex()
                        latex.SetNDC()
                        latex.SetTextSize(0.04)
                        latex.SetTextColor(1)
                        latex.SetTextFont(42)
                        if channel =="mutau":
                            SLtag = "muon"
                            Crosstag = "#mu#tau_{h}"
                        elif channel == "etau":
                            SLtag = "electron"
                            Crosstag = "e#tau_{h}"
                     
                        latex.DrawLatex(0.55, 0.35, "%s trigger lep * tau leg efficiency"%Crosstag)
                        latex.DrawLatex(0.55, 0.30, "#eta: [%s-%s]"%(lep_eta[i],lep_eta[i+1]))
                        latex.DrawLatex(0.55, 0.25, "#tau p_{T}: [%s-%s]"%(tau_pt[f],tau_pt[f+1]))
                        latex.DrawLatex(0.55, 0.20, "#tau dm: %s"%tau_dm)
                        if year==2016:
                            if preVFP == "_preVFP": 
                                VFPtag = " preVFP"
                            else:
                                VFPtag = " postVFP"
                            latex.DrawLatex(0.54, 0.91, "%s%s %s fb^{-1} (13 TeV)"%(year,VFPtag,lumi))
                        else:
                            latex.DrawLatex(0.64, 0.91, "%s %s fb^{-1} (13 TeV)"%(year,lumi))
                        if turn_on_region:
                            canv.SaveAs("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/triggerSF/plots/efficiencies/tauchecks/UL%s%s/turn_on_region/%staulegtriggerEff_%s_taupt%s_taudm%s_%s_UL%s%s.pdf"%(year,preVFP,trigger,channel,pt_tau,tau_dm,eta_label,year,preVFP))
                            canv.SaveAs("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/triggerSF/plots/efficiencies/tauchecks/UL%s%s/turn_on_region/%staulegtriggerEff_%s_taupt%s_taudm%s_%s_UL%s%s.png"%(year,preVFP,trigger,channel,pt_tau,tau_dm,eta_label,year,preVFP))
                        else:
                            canv.SaveAs("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/triggerSF/plots/efficiencies/tauchecks/UL%s%s/%staulegtriggerEff_%s_taupt%s_taudm%s_%s_UL%s%s.pdf"%(year,preVFP,trigger,channel,pt_tau,tau_dm,eta_label,year,preVFP))
                            canv.SaveAs("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/triggerSF/plots/efficiencies/tauchecks/UL%s%s/%staulegtriggerEff_%s_taupt%s_taudm%s_%s_UL%s%s.png"%(year,preVFP,trigger,channel,pt_tau,tau_dm,eta_label,year,preVFP))
                    if channel=="mutau":
                        hist_data.GetXaxis().SetTitle("#mu p_{T} [GeV]")
                        hist_mc.GetXaxis().SetTitle("#mu p_{T} [GeV]")
                    elif channel=="etau":
                        hist_data.GetXaxis().SetTitle("e p_{T} [GeV]")
                        hist_mc.GetXaxis().SetTitle("e pt_{T} [GeV]")
                    hist_data.GetYaxis().SetTitle("#tau p_{T} [GeV]")
                    hist_mc.GetYaxis().SetTitle("#tau p_{T} [GeV]")
                    canv_2d_data = TCanvas("triggerEff_2D_%s_%s_%s_UL%s%s"%(channel,trigger,eta_label,year,preVFP),"%s trigger 2D %s %s UL%s%s"%(trigger,channel,eta_label,year,preVFP))
                    gStyle.SetOptStat(0)
                    hist_data.Draw("COLZ")
                    canv_2d_data.SaveAs("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/triggerSF/plots/efficiencies/tauchecks/UL%s%s/2D_%staulegtriggerEff_%s_%s_data_taudm%s_UL%s%s.pdf"%(year,preVFP,trigger,channel,eta_label,tau_dm,year,preVFP))
                    canv_2d_mc = TCanvas("triggerEff_2D_%s_%s_%s_UL%s%s"%(channel,trigger,eta_label,year,preVFP),"%s trigger 2D %s %s UL%s%s"%(trigger,channel,eta_label,year,preVFP))
                    hist_mc.Draw("COLZ")
                    canv_2d_mc.SaveAs("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/triggerSF/plots/efficiencies/tauchecks/UL%s%s/2D_%staulegtriggerEff_%s_%s_mc_taudm%s_UL%s%s.pdf"%(year,preVFP,trigger,channel,eta_label,tau_dm,year,preVFP))
                    
          

