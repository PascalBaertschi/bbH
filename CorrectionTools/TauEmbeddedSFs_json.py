import numpy as np
from ROOT import TFile, RooArgList
from array import array
import os
import correctionlib


path = 'CorrectionTools/leptonEfficiencies/MuonPOG/'
path_mu_json = 'CorrectionTools/jsonpog-integration/POG/MUO/'
path_e_json = 'CorrectionTools/jsonpog-integration/POG/EGM/'
class TauEmbeddedSFs:
    
    def __init__(self, year,preVFP):
        """Load histograms from files."""
        assert year in [2016,2017,2018], "MuonSFs: You must choose a year from: 2016, 2017 or 2018."
        self.year = year
        if year==2018:
            self.year_name = "2018_UL"
        self.muonjson = correctionlib.CorrectionSet.from_file(os.path.join(path_mu_json,self.year_name,"muon_2018UL.json.gz"))
        self.electronjson = correctionlib.CorrectionSet.from_file(os.path.join(path_e_json,self.year_name,"electron_2018UL.json.gz"))

    
    def getMuIdSF(self, pt, eta):
        IdSF = self.muonjson["EmbID_pt_eta_bins"].evaluate(pt,abs(eta))
        return IdSF

    def getTriggerSF(self,pt1,eta1,pt2,eta2):
         TriggerSF = self.muonjson["m_sel_trg_kit_ratio"].evaluate(pt1,abs(eta1),pt2,abs(eta2))
         return TriggerSF
