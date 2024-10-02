import ROOT
from ROOT import TFile, TH1D, TCanvas, gStyle, TLegend, TLatex, TGraphErrors
import correctionlib
import os
import numpy as np
from argparse import ArgumentParser
import plotting as plot
path_json = '/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/jsonpog-integration/POG/TAU/'
path_root = '/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/triggerSF/root/'
#path_root = '/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/triggerSF/root/check/'

class TriggerSFs:

    def __init__(self,year,VFPtag):
        self.year = year
        self.VFPtag = VFPtag
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
        
        if self.year==2017:
            ### tag  ####
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
            ##########################

        if self.year==2016:
            if self.VFPtag=="_preVFP":
                year_name = "2016preVFP_UL"
            else:
                year_name = "2016postVFP_UL"
        elif self.year==2017:
            year_name = "2017_UL"
        elif self.year==2018:
            year_name = "2018_UL"
        path_json = '/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/jsonpog-integration/POG/MUO/'
        self.muonjson = correctionlib.CorrectionSet.from_file(os.path.join(path_json,year_name,"muon_Z.json.gz"))


    def getBinContent(self,hist,pt,eta):
        low_pt = hist.GetXaxis().GetBinCenter(1)
        high_pt = hist.GetXaxis().GetBinCenter(hist.GetNbinsX())
        high_eta = hist.GetYaxis().GetBinCenter(hist.GetNbinsY())
        if pt<low_pt: pt = low_pt
        if pt>high_pt: pt = high_pt
        if abs(eta)>high_eta: eta=high_eta
        return [hist.GetBinContent(hist.GetXaxis().FindBin(pt),hist.GetYaxis().FindBin(abs(eta))),hist.GetBinError(hist.GetXaxis().FindBin(pt),hist.GetYaxis().FindBin(abs(eta)))]

        
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
                cross_eff_data = [0.,0.]
                cross_eff_mc = [0.,0.]
                crossSLF_eff_data = [0.,0.]
                crossSLF_eff_mc = [0.,0.]
        return [sl_eff_data[0],sl_eff_mc[0],cross_eff_data[0],cross_eff_mc[0],crossSLF_eff_data[0],crossSLF_eff_mc[0],sl_eff_data[1],sl_eff_mc[1],cross_eff_data[1],cross_eff_mc[1],crossSLF_eff_data[1],crossSLF_eff_mc[1]]
        

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
                cross_eff_data = [0.,0.]
                cross_eff_mc = [0.,0.]
                crossSLF_eff_data = [0.,0.]
                crossSLF_eff_mc = [0.,0.]
        return [sl_eff_data[0],sl_eff_mc[0],cross_eff_data[0],cross_eff_mc[0],crossSLF_eff_data[0],crossSLF_eff_mc[0],sl_eff_data[1],sl_eff_mc[1],cross_eff_data[1],cross_eff_mc[1],crossSLF_eff_data[1],crossSLF_eff_mc[1]]

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
                cross_eff_data = [0.,0.]
                cross_eff_mc = [0.,0.]
                crossSLF_eff_data = [0.,0.]
                crossSLF_eff_mc = [0.,0.]
        return [sl_eff_data[0],sl_eff_mc[0],cross_eff_data[0],cross_eff_mc[0],crossSLF_eff_data[0],crossSLF_eff_mc[0],sl_eff_data[1],sl_eff_mc[1],cross_eff_data[1],cross_eff_mc[1],crossSLF_eff_data[1],crossSLF_eff_mc[1]]

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
                cross_eff_data = [0.,0.]
                cross_eff_mc = [0.,0.]
                crossSLF_eff_data = [0.,0.]
                crossSLF_eff_mc = [0.,0.]
        return [sl_eff_data[0],sl_eff_mc[0],cross_eff_data[0],cross_eff_mc[0],crossSLF_eff_data[0],crossSLF_eff_mc[0],sl_eff_data[1],sl_eff_mc[1],cross_eff_data[1],cross_eff_mc[1],crossSLF_eff_data[1],crossSLF_eff_mc[1]]
        
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
                cross_eff_data = [0.,0.]
                cross_eff_mc = [0.,0.]
                crossSLF_eff_data = [0.,0.]
                crossSLF_eff_mc = [0.,0.]
        return [sl_eff_data[0],sl_eff_mc[0],cross_eff_data[0],cross_eff_mc[0],crossSLF_eff_data[0],crossSLF_eff_mc[0],sl_eff_data[1],sl_eff_mc[1],cross_eff_data[1],cross_eff_mc[1],crossSLF_eff_data[1],crossSLF_eff_mc[1]]


    def getLepTriggerEffTag(self,pt,eta):
        sl_eff_data = self.getBinContent(self.e_data_hist_tag,pt,eta)
        sl_eff_mc = self.getBinContent(self.e_mc_hist_tag,pt,eta)
        return [sl_eff_data[0],sl_eff_mc[0],sl_eff_data[1],sl_eff_mc[1]]

    def getLepTriggerEffEle32(self,pt,eta):
        sl_eff_data_ele32ac = self.getBinContent(self.e_data_hist_ele32ac,pt,eta)
        sl_eff_data_ele32deac = self.getBinContent(self.e_data_hist_ele32deac,pt,eta)
        return [sl_eff_data_ele32ac[0],sl_eff_data_ele32deac[0],sl_eff_data_ele32ac[1],sl_eff_data_ele32deac[1]]
        
    def getEffCentral(self,pt,eta):
        SF = self.muonjson["NUM_IsoMu24_DEN_CutBasedIdTight_and_PFIsoTight"].evaluate(self.year_name,abs(eta),pt,"sf")
        return SF


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
    #triggers = ["SL","Cross","CrossSLF"]
    triggers = ["SL"]
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
                if trigger=="SL":
                    lep_pt = mu_pt
                    lep_eta = mu_eta
                elif trigger=="Cross":
                    lep_pt = mutau_pt
                    lep_eta = mutau_eta
                else:
                    lep_pt = mu_pt #taking the shorter list
                    lep_eta = mutau_eta #taking the shorter list
            elif channel=="etau":
                if trigger=="SL":
                    lep_pt = e_pt
                    lep_eta = e_eta
                elif trigger=="Cross":
                    lep_pt = etau_pt
                    lep_eta = etau_eta
                else:
                    lep_pt = e_pt #taking the shorter list
                    lep_eta = etau_eta #taking the shorter list
            Nbinsx = len(lep_pt)-1
            eta_len = len(lep_eta)-1
            for i in range(eta_len):
                eta_label = "eta%s-%s"%(lep_eta[i],lep_eta[i+1])
                eta_label = eta_label.replace(".",",")
                eta = lep_eta[i]+(lep_eta[i+1]-lep_eta[i])/2.
                data_eff_list = []
                data_eff_error_list = []
                mc_eff_list = []
                mc_eff_error_list = []
                data_pt_list = []
                data_pt_error_list = []
                mc_pt_list = []
                mc_pt_error_list = []
                zeros_list = []
                data_eff_fit_list = []
                data_eff_error_fit_list = []
                mc_eff_fit_list = []
                mc_eff_error_fit_list = []
                data_eff_up_list = []
                data_eff_error_up_list = []
                mc_eff_up_list = []
                mc_eff_error_up_list = []
                data_eff_down_list = []
                data_eff_error_down_list = []
                mc_eff_down_list = []
                mc_eff_error_down_list = []
                mc_eff_gen_list = []
                mc_eff_error_gen_list = []
                data_eff_tag_list = []
                data_eff_error_tag_list = []
                mc_eff_tag_list = []
                mc_eff_error_tag_list = []
                data_eff_ele32ac_list = []
                data_eff_error_ele32ac_list = []
                data_eff_ele32deac_list = []
                data_eff_error_ele32deac_list = []
                data_eff_ele32_list = []
                data_eff_error_ele32_list = []
                data_eff_hist = TH1D("data_eff","",Nbinsx,np.array(lep_pt))
                mc_eff_hist = TH1D("data_mc","",Nbinsx,np.array(lep_pt))
                for j in range(Nbinsx):
                    pt = lep_pt[j]+((lep_pt[j+1]-lep_pt[j])/2.)
                    pt_error = (lep_pt[j+1]-lep_pt[j])/2.
                    effs=triggerSFs.getLepTriggerEff(channel,pt,eta)
                    effsFit = triggerSFs.getLepTriggerEffFit(channel,pt,eta)
                    effsUp = triggerSFs.getLepTriggerEffUp(channel,pt,eta)
                    effsDown = triggerSFs.getLepTriggerEffDown(channel,pt,eta)
                    effsGen = triggerSFs.getLepTriggerEffGen(channel,pt,eta)
                    if year==2017 and channel=="etau":
                        effsTag = triggerSFs.getLepTriggerEffTag(pt,eta)
                        eff_data_tag = effsTag[0]
                        eff_mc_tag = effsTag[1]
                        effErr_data_tag = effsTag[2]
                        effErr_mc_tag = effsTag[3]
                        effsEle32 = triggerSFs.getLepTriggerEffEle32(pt,eta)
                        eff_data_ele32ac = effsEle32[0]
                        eff_data_ele32deac = effsEle32[1]
                        effErr_data_ele32ac = effsEle32[2]
                        effErr_data_ele32deac = effsEle32[3]
                        eff_data_ele32 = (eff_data_ele32ac * (27.13/41.54)) + (eff_data_ele32deac * (14.41/41.54))
                        effErr_data_ele32 = np.sqrt((effErr_data_ele32ac * (27.13/41.54))**2 + (effErr_data_ele32deac * (14.41/41.54))**2)
                    if trigger=="SL":
                        eff_data = effs[0]
                        eff_mc = effs[1]
                        effErr_data = effs[6]
                        effErr_mc = effs[7]
                        eff_data_fit = effsFit[0]
                        eff_mc_fit = effsFit[1]
                        effErr_data_fit = effsFit[6]
                        effErr_mc_fit = effsFit[7]
                        eff_data_up = effsUp[0]
                        eff_mc_up = effsUp[1]
                        effErr_data_up = effsUp[6]
                        effErr_mc_up = effsUp[7]
                        eff_data_down = effsDown[0]
                        eff_mc_down = effsDown[1]
                        effErr_data_down = effsDown[6]
                        effErr_mc_down = effsDown[7]
                        eff_mc_gen = effsGen[1]
                        effErr_mc_gen = effsGen[7]
                    elif trigger=="Cross":
                        eff_data = effs[2]
                        eff_mc = effs[3]
                        effErr_data = effs[8]
                        effErr_mc = effs[9]
                        eff_data_fit = effsFit[2]
                        eff_mc_fit = effsFit[3]
                        effErr_data_fit = effsFit[8]
                        effErr_mc_fit = effsFit[9]
                        eff_data_up = effsUp[2]
                        eff_mc_up = effsUp[3]
                        effErr_data_up = effsUp[8]
                        effErr_mc_up = effsUp[9]
                        eff_data_down = effsDown[2]
                        eff_mc_down = effsDown[3]
                        effErr_data_down = effsDown[8]
                        effErr_mc_down = effsDown[9]
                        eff_mc_gen = effsGen[3]
                        effErr_mc_gen = effsGen[9]
                    elif trigger=="CrossSLF":
                        eff_data = effs[4]
                        eff_mc = effs[5]
                        effErr_data = effs[10]
                        effErr_mc = effs[11]
                        eff_data_fit = effsFit[4]
                        eff_mc_fit = effsFit[5]
                        effErr_data_fit = effsFit[10]
                        effErr_mc_fit = effsFit[11]
                        eff_data_up = effsUp[4]
                        eff_mc_up = effsUp[5]
                        effErr_data_up = effsUp[10]
                        effErr_mc_up = effsUp[11]
                        eff_data_down = effsDown[4]
                        eff_mc_down = effsDown[5]
                        effErr_data_down = effsDown[10]
                        effErr_mc_down = effsDown[11]
                        eff_mc_gen = effsGen[5]
                        effErr_mc_gen = effsGen[11]
                    data_eff_list.append(eff_data)
                    mc_eff_list.append(eff_mc)
                    #data_eff_error_list.append(round(effErr_data*1000,2))
                    #mc_eff_error_list.append(round(effErr_mc*1000,2))
                    data_eff_error_list.append(effErr_data)
                    mc_eff_error_list.append(effErr_mc)
                    #####
                    data_eff_fit_list.append(eff_data_fit)
                    mc_eff_fit_list.append(eff_mc_fit)
                    data_eff_error_fit_list.append(effErr_data_fit)
                    mc_eff_error_fit_list.append(effErr_mc_fit)
                    data_eff_up_list.append(eff_data_up)
                    mc_eff_up_list.append(eff_mc_up)
                    data_eff_error_up_list.append(effErr_data_up)
                    mc_eff_error_up_list.append(effErr_mc_up)
                    data_eff_down_list.append(eff_data_down)
                    mc_eff_down_list.append(eff_mc_down)
                    data_eff_error_down_list.append(effErr_data_down)
                    mc_eff_error_down_list.append(effErr_mc_down)
                    mc_eff_gen_list.append(eff_mc_gen)
                    mc_eff_error_gen_list.append(effErr_mc_gen)
                    if year==2017 and channel=="etau":
                        data_eff_tag_list.append(eff_data_tag)
                        mc_eff_tag_list.append(eff_mc_tag)
                        data_eff_error_tag_list.append(effErr_data_tag)
                        mc_eff_error_tag_list.append(effErr_mc_tag)
                        data_eff_ele32ac_list.append(eff_data_ele32ac)
                        data_eff_ele32deac_list.append(eff_data_ele32deac)
                        data_eff_error_ele32ac_list.append(effErr_data_ele32ac)
                        data_eff_error_ele32deac_list.append(effErr_data_ele32deac)
                        data_eff_ele32_list.append(eff_data_ele32)
                        data_eff_error_ele32_list.append(effErr_data_ele32)
                    #####
                    data_pt_list.append(pt)
                    mc_pt_list.append(pt)
                    data_pt_error_list.append(pt_error)
                    mc_pt_error_list.append(pt_error)
                    zeros_list.append(0.)
                    data_eff_hist.SetBinContent(j,eff_data)
                    mc_eff_hist.SetBinContent(j,eff_mc)
                canv = TCanvas("triggerEff_%s_%s_%s_UL%s%s"%(channel,trigger,eta_label,year,preVFP),"%s trigger %s %s UL%s%s"%(trigger,channel,eta_label,year,preVFP),600,400)
                canv.SetBottomMargin(0.2)
                pads = plot.TwoPadSplit(0.29,0.01,0.01)
                plot.DrawCMSLogo(canv, "Private work", "(CMS data/simulation)", 10, 0.045, 0.02, 1.0, '', 0.6)
                ratio_list = np.array(data_eff_list)/np.array(mc_eff_list)
                ratio_error_list = []
                for index in range(len(data_eff_error_list)):
                    data_eff = data_eff_list[index]
                    mc_eff = mc_eff_list[index]
                    data_eff_error = data_eff_error_list[index]
                    mc_eff_error = mc_eff_error_list[index]
                    ratio_error = np.sqrt((data_eff_error/mc_eff)**2+((data_eff*mc_eff_error)/mc_eff**2)**2)
                    ratio_error_list.append(ratio_error)
                ratio_error_list = data_eff_error_list
                ratio = TGraphErrors(Nbinsx,np.array(data_pt_list),np.array(ratio_list),np.array(data_pt_error_list),np.array(ratio_error_list))
                graph_data = TGraphErrors(Nbinsx,np.array(data_pt_list),np.array(data_eff_list),np.array(data_pt_error_list),np.array(data_eff_error_list))
                graph_mc = TGraphErrors(Nbinsx,np.array(mc_pt_list),np.array(mc_eff_list),np.array(mc_pt_error_list),np.array(mc_eff_error_list))
                ####
                graph_data_fit = TGraphErrors(Nbinsx,np.array(data_pt_list),np.array(data_eff_fit_list),np.array(zeros_list),np.array(data_eff_error_fit_list))
                graph_mc_fit = TGraphErrors(Nbinsx,np.array(mc_pt_list),np.array(mc_eff_fit_list),np.array(zeros_list),np.array(mc_eff_error_fit_list))
                graph_data_up = TGraphErrors(Nbinsx,np.array(data_pt_list),np.array(data_eff_up_list),np.array(zeros_list),np.array(data_eff_error_up_list))
                graph_mc_up = TGraphErrors(Nbinsx,np.array(mc_pt_list),np.array(mc_eff_up_list),np.array(zeros_list),np.array(mc_eff_error_up_list))
                graph_data_down = TGraphErrors(Nbinsx,np.array(data_pt_list),np.array(data_eff_down_list),np.array(zeros_list),np.array(data_eff_error_down_list))
                graph_mc_down = TGraphErrors(Nbinsx,np.array(mc_pt_list),np.array(mc_eff_down_list),np.array(zeros_list),np.array(mc_eff_error_down_list))
                graph_mc_gen = TGraphErrors(Nbinsx,np.array(mc_pt_list),np.array(mc_eff_gen_list),np.array(zeros_list),np.array(mc_eff_error_gen_list))
                if year==2017 and channel=="etau":
                    graph_data_tag = TGraphErrors(Nbinsx,np.array(data_pt_list),np.array(data_eff_tag_list),np.array(zeros_list),np.array(data_eff_error_tag_list))
                    graph_mc_tag = TGraphErrors(Nbinsx,np.array(mc_pt_list),np.array(mc_eff_tag_list),np.array(zeros_list),np.array(mc_eff_error_tag_list))
                    graph_data_ele32ac = TGraphErrors(Nbinsx,np.array(data_pt_list),np.array(data_eff_ele32ac_list),np.array(zeros_list),np.array(data_eff_error_ele32ac_list))
                    graph_data_ele32deac = TGraphErrors(Nbinsx,np.array(data_pt_list),np.array(data_eff_ele32deac_list),np.array(zeros_list),np.array(data_eff_error_ele32deac_list))
                    graph_data_ele32 = TGraphErrors(Nbinsx,np.array(data_pt_list),np.array(data_eff_ele32_list),np.array(zeros_list),np.array(data_eff_error_ele32_list))
                ####


                if channel=="mutau":
                    graph_data.GetXaxis().SetTitle("#mu p_{T} [GeV]")
                    ratio.GetXaxis().SetTitle("#mu p_{T} [GeV]")
                elif channel=="etau":
                    graph_data.GetXaxis().SetTitle("e p_{T} [GeV]")
                    ratio.GetXaxis().SetTitle("e p_{T} [GeV]")
                graph_data.GetYaxis().SetTitle("efficiency")
                graph_data.SetMarkerStyle(21)
                graph_mc.SetMarkerStyle(20)
                graph_data.SetMarkerColor(1)
                graph_mc.SetMarkerColor(2)
                graph_data.SetLineColor(1)
                graph_mc.SetLineColor(2)
                graph_data.SetTitle("")
                graph_data.GetYaxis().SetRangeUser(0.,1.2)
                graph_data.GetYaxis().SetTitleSize(0.05)
                graph_data.GetYaxis().SetTitleOffset(0.95)
                graph_data.GetYaxis().SetLabelSize(0.043)
                ratio.GetXaxis().SetLabelSize(0.043)
                ratio.GetYaxis().SetLabelSize(0.043)
                ratio.GetXaxis().SetTitleSize(0.05)
                ratio.GetYaxis().SetTitleSize(0.05)
                ratio.GetXaxis().SetTitleOffset(0.9)
                ratio.GetYaxis().SetTitleOffset(0.97)
                
                #graph_data.GetYaxis().SetRangeUser(0.5,1.25)
                #leg = TLegend(0.7,0.4,0.85,0.55)
                leg = TLegend(0.7,0.45,0.85,0.6)
                #leg = TLegend(0.7,0.3,0.85,0.45)
                if sys=="":
                    #leg = TLegend(0.7,0.4,0.85,0.55)
                    leg = TLegend(0.7,0.45,0.85,0.6)
                    leg.AddEntry(graph_data,"data","p")
                    leg.AddEntry(graph_mc,"mc","p")
                else:
                    #leg = TLegend(0.5,0.4,0.85,0.65)
                    #leg = TLegend(0.5,0.3,0.85,0.55)
                    leg = TLegend(0.5,0.45,0.85,0.7)
                    leg.AddEntry(graph_data,"data","p")
                    leg.AddEntry(graph_mc,"mc","p")
                    if sys=="fit":
                        leg.AddEntry(graph_data_fit,"data alt. fit","p")
                        leg.AddEntry(graph_mc_fit,"mc alt. fit","p")
                    elif sys=="up":
                        leg.AddEntry(graph_data_up,"data up var","p")
                        leg.AddEntry(graph_mc_up,"mc up var","p")
                    elif sys=="down":
                        leg.AddEntry(graph_data_down,"data down var","p")
                        leg.AddEntry(graph_mc_down,"mc down var","p")
                    elif sys=="gen":
                        leg.AddEntry(graph_mc_gen,"mc gen","p")
                    elif sys=="tag":
                        leg.AddEntry(graph_data_tag,"data Ele35","p")
                        leg.AddEntry(graph_mc_tag,"mc Ele35","p")
                    elif sys=="ele32":
                        #leg.AddEntry(graph_data_ele32ac,"data Ele32 active","p")
                        #leg.AddEntry(graph_data_ele32deac, "data Ele32 deactive","p")
                        leg.AddEntry(graph_data_ele32, "data Ele32 split","p")
                ###
                leg.SetBorderSize(0)
                pads[0].cd()
                graph_data.GetXaxis().SetTitle("")
                graph_data.GetXaxis().SetLabelSize(0)
                graph_data.Draw("AP0")
                graph_mc.Draw("P0 SAME")
                ###
                if sys=="fit":
                    graph_data_fit.SetMarkerColor(7)
                    graph_mc_fit.SetMarkerColor(3)
                    graph_data_fit.SetLineColor(7)
                    graph_mc_fit.SetLineColor(3)
                    graph_data_fit.SetMarkerStyle(34)
                    graph_mc_fit.SetMarkerStyle(34)
                    graph_data_fit.Draw("P0 SAME")
                    graph_mc_fit.Draw("P0 SAME")
                elif sys=="up":
                    graph_data_up.SetMarkerColor(7)
                    graph_mc_up.SetMarkerColor(3)
                    graph_data_up.SetLineColor(7)
                    graph_mc_up.SetLineColor(3)
                    graph_data_up.SetMarkerStyle(34)
                    graph_mc_up.SetMarkerStyle(34)
                    graph_data_up.Draw("P0 SAME")
                    graph_mc_up.Draw("P0 SAME")
                elif sys=="down":
                    graph_data_down.SetMarkerColor(7)
                    graph_mc_down.SetMarkerColor(3)
                    graph_data_down.SetLineColor(7)
                    graph_mc_down.SetLineColor(3)
                    graph_data_down.SetMarkerStyle(34)
                    graph_mc_down.SetMarkerStyle(34)
                    graph_data_down.Draw("P0 SAME")
                    graph_mc_down.Draw("P0 SAME")
                elif sys=="gen":
                    graph_mc_gen.SetMarkerColor(3)
                    graph_mc_gen.SetLineColor(3)
                    graph_mc_gen.SetMarkerStyle(34)
                    graph_mc_gen.Draw("P0 SAME")
                elif sys=="tag":
                    graph_data_tag.SetMarkerColor(7)
                    graph_mc_tag.SetMarkerColor(3)
                    graph_data_tag.SetLineColor(7)
                    graph_mc_tag.SetLineColor(3)
                    graph_data_tag.SetMarkerStyle(34)
                    graph_mc_tag.SetMarkerStyle(34)
                    graph_data_tag.Draw("P0 SAME")
                    graph_mc_tag.Draw("P0 SAME")
                elif sys=="ele32":
                    #graph_data_ele32ac.SetMarkerColor(7)
                    #graph_data_ele32deac.SetMarkerColor(3)
                    graph_data_ele32.SetMarkerColor(3)
                    #graph_data_ele32ac.SetLineColor(7)
                    #graph_data_ele32deac.SetLineColor(3)
                    graph_data_ele32.SetLineColor(3)
                    #graph_data_ele32ac.SetMarkerStyle(34)
                    #graph_data_ele32deac.SetMarkerStyle(34)
                    graph_data_ele32.SetMarkerStyle(34)
                    #graph_data_ele32ac.Draw("P0 SAME")
                    #graph_data_ele32deac.Draw("P0 SAME")
                    graph_data_ele32.Draw("P0 SAME")
                pads[1].cd()
                pads[1].SetGrid(0,1)
                ratio.SetTitle("")
                ratio.GetYaxis().SetTitle("SF")
                ratio.GetYaxis().SetNdivisions(5)
                ratio.SetMarkerStyle(20)
                ratio.Draw("AP")    
            
                ###
                leg.Draw("SAME")
                latex = TLatex()
                latex.SetNDC()
                latex.SetTextSize(0.045)
                latex.SetTextColor(1)
                latex.SetTextFont(42)
                if channel =="mutau":
                    SLtag = "muon"
                    Crosstag = "#mu#tau_{h}"
                elif channel == "etau":
                    SLtag = "electron"
                    Crosstag = "e#tau_{h}"
                if trigger=="SL":
                    #latex.DrawLatex(0.55, 0.25, "%s trigger efficiency"%SLtag)
                    #latex.DrawLatex(0.55, 0.20, "#eta: [%s-%s]"%(lep_eta[i],lep_eta[i+1]))
                    latex.DrawLatex(0.55, 0.40, "%s trigger efficiency"%SLtag)
                    latex.DrawLatex(0.55, 0.35, "#eta: [%s-%s]"%(lep_eta[i],lep_eta[i+1]))
                    #latex.DrawLatex(0.55, 0.35, "%s trigger efficiency"%SLtag)
                    #latex.DrawLatex(0.55, 0.30, "#eta: [%s-%s]"%(lep_eta[i],lep_eta[i+1]))
                    #latex.DrawLatex(0.55, 0.25, "%s trigger efficiency"%SLtag)
                    #latex.DrawLatex(0.55, 0.2, "#eta: [%s-%s]"%(lep_eta[i],lep_eta[i+1]))
                elif trigger=="Cross":
                    latex.DrawLatex(0.55, 0.35, "%s trigger efficiency"%Crosstag)
                    latex.DrawLatex(0.55, 0.30, "#eta: [%s-%s]"%(lep_eta[i],lep_eta[i+1]))
                    #latex.DrawLatex(0.55, 0.25, "%s trigger efficiency"%Crosstag)
                    #latex.DrawLatex(0.55, 0.2, "#eta: [%s-%s]"%(lep_eta[i],lep_eta[i+1]))
                elif trigger=="CrossSLF":
                    latex.DrawLatex(0.55, 0.35, "%s trigger efficiency"%Crosstag)
                    latex.DrawLatex(0.55, 0.3, "if single %s trigger fired"%SLtag)
                    latex.DrawLatex(0.55, 0.25, "#eta: [%s-%s]"%(lep_eta[i],lep_eta[i+1]))
                    #latex.DrawLatex(0.55, 0.25, "%s trigger efficiency"%Crosstag)
                    #latex.DrawLatex(0.55, 0.2, "if single %s trigger fired"%SLtag)
                    #latex.DrawLatex(0.55, 0.15, "#eta: [%s-%s]"%(lep_eta[i],lep_eta[i+1]))
                if year==2016:
                    if preVFP == "_preVFP": 
                        VFPtag_plots = " preVFP"
                    else:
                        VFPtag_plots = " postVFP"
                    latex.DrawLatex(0.52, 0.91, "%s%s %s fb^{-1} (13 TeV)"%(year,VFPtag_plots,lumi))
                else:
                    latex.DrawLatex(0.62, 0.91, "%s %s fb^{-1} (13 TeV)"%(year,lumi))
                if sys=="":
                    if turn_on_region:
                        canv.SaveAs("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/triggerSF/plots/efficiencies/UL%s%s/turn_on_region/%striggerEff_%s_%s_UL%s%s.pdf"%(year,preVFP,trigger,channel,eta_label,year,preVFP))
                        canv.SaveAs("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/triggerSF/plots/efficiencies/UL%s%s/turn_on_region/%striggerEff_%s_%s_UL%s%s.png"%(year,preVFP,trigger,channel,eta_label,year,preVFP))
                    else:
                        canv.SaveAs("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/triggerSF/plots/efficiencies/UL%s%s/%striggerEff_%s_%s_UL%s%s.pdf"%(year,preVFP,trigger,channel,eta_label,year,preVFP))
                        canv.SaveAs("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/triggerSF/plots/efficiencies/UL%s%s/%striggerEff_%s_%s_UL%s%s.png"%(year,preVFP,trigger,channel,eta_label,year,preVFP))
                        canv.SaveAs("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/triggerSF/plots/thesis/%striggerEff_%s_%s_UL%s%s.pdf"%(trigger,channel,eta_label,year,preVFP))
                else:
                   sys_tag = sys.capitalize()
                   if turn_on_region:
                       canv.SaveAs("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/triggerSF/plots/efficiencies/sys%s/UL%s%s/turn_on_region/%striggerEff_%s_%s_UL%s%s.pdf"%(sys_tag,year,preVFP,trigger,channel,eta_label,year,preVFP))
                       canv.SaveAs("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/triggerSF/plots/efficiencies/sys%s/UL%s%s/turn_on_region/%striggerEff_%s_%s_UL%s%s.png"%(sys_tag,year,preVFP,trigger,channel,eta_label,year,preVFP))
                   else:
                       canv.SaveAs("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/triggerSF/plots/efficiencies/sys%s/UL%s%s/%striggerEff_%s_%s_UL%s%s.pdf"%(sys_tag,year,preVFP,trigger,channel,eta_label,year,preVFP))
                       canv.SaveAs("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/triggerSF/plots/efficiencies/sys%s/UL%s%s/%striggerEff_%s_%s_UL%s%s.png"%(sys_tag,year,preVFP,trigger,channel,eta_label,year,preVFP))

