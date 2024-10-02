from ROOT import TFile, RooArgList
import numpy as np
from array import array
import correctionlib
import os
# https://twiki.cern.ch/twiki/bin/view/CMS/EgammaUL2016To2018
#https://cms-nanoaod-integration.web.cern.ch/commonJSONSFs/EGM_electron_Run2_UL/EGM_electron_2018_UL.html
#https://gitlab.cern.ch/cms-nanoAOD/jsonpog-integration/
path    = 'CorrectionTools/leptonEfficiencies/ElectronPOG/'
path_json = 'CorrectionTools/jsonpog-integration/POG/EGM/'
path_root = '/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/EIsoSF/root/'
triggerSFpath = 'CorrectionTools/triggerSF/root/'
class ElectronSFs:
    
    def __init__(self, year, ULtag, preVFP):
        """Load histograms from files."""
        
        assert year in [2016,2017,2018], "ElectronSFs: You must choose a year from: 2016, 2017 or 2018."
        self.year = year
        if year==2016:
            sftool_file = TFile.Open(path+"RunUL2016/htt_scalefactors_legacy_2016.root")
            sftool_workframe=sftool_file.Get("w")
            sftool_file.Close()
            self.sftool_trig = sftool_workframe.function("e_trg_ic_ratio").functor(RooArgList(sftool_workframe.argSet("e_pt,e_eta")))
            if preVFP=="_preVFP":
               self.year_name = "2016preVFP_UL"
            else:
               self.year_name = "2016postVFP_UL"
        elif year==2017:
            self.year_name = "2017_UL"
            sftool_file = TFile.Open(path+"RunUL2017/htt_scalefactors_legacy_2017.root")
            sftool_workframe=sftool_file.Get("w")
            sftool_file.Close()
            self.sftool_trig = sftool_workframe.function("e_trg_ic_ratio").functor(RooArgList(sftool_workframe.argSet("e_pt,e_eta")))
        elif year==2018: 
            self.year_name = "2018_UL"
            sftool_file = TFile.Open(path+"RunUL2018/htt_scalefactors_legacy_2018.root")
            sftool_workframe=sftool_file.Get("w")
            sftool_file.Close()
            self.sftool_trig = sftool_workframe.function("e_trg_ic_ratio").functor(RooArgList(sftool_workframe.argSet("e_pt,e_eta")))
        self.elejson = correctionlib.CorrectionSet.from_file(os.path.join(path_json,self.year_name,"electron.json.gz"))
        #### E iso SF  ####
        e_data_file = TFile('%sEIsoEff_UL%s%s_data_Fits_dielectron_mass_pt_eta_bins.root'%(path_root,year,preVFP),'READ')
        self.e_data_hist = e_data_file.Get("dielectron_mass_pt_eta_bins")
        self.e_data_hist.SetDirectory(0)
        e_data_file.Close()
        e_mc_file = TFile('%sEIsoEff_UL%s%s_mc_Fits_dielectron_mass_pt_eta_bins.root'%(path_root,year,preVFP),'READ')
        self.e_mc_hist = e_mc_file.Get("dielectron_mass_pt_eta_bins")
        self.e_mc_hist.SetDirectory(0)
        e_mc_file.Close()
        ##################

    def getBinContent(self,hist,pt,eta):
        low_pt = hist.GetXaxis().GetBinCenter(1)
        high_pt = hist.GetXaxis().GetBinCenter(hist.GetNbinsX())
        high_eta = hist.GetYaxis().GetBinCenter(hist.GetNbinsY())
        if pt<low_pt: pt = low_pt
        if pt>high_pt: pt = high_pt
        if abs(eta)>high_eta: eta=high_eta
        return [hist.GetBinContent(hist.GetXaxis().FindBin(pt),hist.GetYaxis().FindBin(abs(eta))),hist.GetBinError(hist.GetXaxis().FindBin(pt),hist.GetYaxis().FindBin(abs(eta)))]

    def getEIsoSF(self,pt,eta):
        eff_data = self.getBinContent(self.e_data_hist,pt,abs(eta))[0]
        eff_mc = self.getBinContent(self.e_mc_hist,pt,abs(eta))[0]
        eff_data_error = self.getBinContent(self.e_data_hist,pt,abs(eta))[1]
        eff_mc_error = self.getBinContent(self.e_mc_hist,pt,abs(eta))[1]
        return eff_data/eff_mc

    def getTriggerSF(self, pt, eta):
        return self.sftool_trig.eval(array('d',[pt,eta]))

    def getSF(self, pt, eta):
        RecoSF = self.elejson["UL-Electron-ID-SF"].evaluate(self.year_name[:-3],"sf","RecoAbove20",abs(eta),pt)
        IdSF = self.elejson["UL-Electron-ID-SF"].evaluate(self.year_name[:-3],"sf","wp90noiso",abs(eta),pt)
        IsoSF = self.getEIsoSF(pt,eta)
        RecoSFerror = self.elejson["UL-Electron-ID-SF"].evaluate(self.year_name[:-3],"sfup","RecoAbove20",abs(eta),pt)-RecoSF
        IdSFerror = self.elejson["UL-Electron-ID-SF"].evaluate(self.year_name[:-3],"sfup","wp90noiso",abs(eta),pt)-IdSF
        SFerror = np.sqrt((RecoSFerror * IdSF * IsoSF)**2+(RecoSF * IdSFerror * IsoSF)**2) #not considering error for Iso SF because it is negligible
        SF = RecoSF * IdSF * IsoSF
        SF_up = SF+SFerror
        SF_down = SF-SFerror
        return [SF,SF_up,SF_down]    
