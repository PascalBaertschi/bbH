import numpy as np
import correctionlib
import os
# https://github.com/cms-tau-pog/TauTriggerSFs/tree/run2_SFs
# https://github.com/cms-tau-pog/TauIDSFs
# https://twiki.cern.ch/twiki/bin/viewauth/CMS/TauIDRecommendationForRun2
# https://cms-nanoaod-integration.web.cern.ch/commonJSONSFs/summaries/TAU_2018_UL_tau.html
# https://gitlab.cern.ch/cms-nanoAOD/jsonpog-integration/-/tree/master/
path_json = 'CorrectionTools/jsonpog-integration/POG/TAU/'

class TauSFs:
    
    def __init__(self, year,ULtag,VFPtag):
        """Load histograms from files."""
        assert year in [2016,2017,2018], "TauSFs: You must choose a year from: 2016, 2017 or 2018."
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


    def getSF(self, pt, eta, dm, genmatch, wp_jet, wp_mu, wp_e):
        SF_jet = self.taujson["DeepTau2017v2p1VSjet"].evaluate(pt,dm,genmatch,wp_jet,wp_e,"default","pt")
        SF_jet_up = self.taujson["DeepTau2017v2p1VSjet"].evaluate(pt,dm,genmatch,wp_jet,wp_e,"up","pt")
        SF_jet_down = self.taujson["DeepTau2017v2p1VSjet"].evaluate(pt,dm,genmatch,wp_jet,wp_e,"down","pt")
        SF_mu = self.taujson["DeepTau2017v2p1VSmu"].evaluate(eta,genmatch,wp_mu,"nom")
        SF_mu_up = self.taujson["DeepTau2017v2p1VSmu"].evaluate(eta,genmatch,wp_mu,"up")
        SF_mu_down = self.taujson["DeepTau2017v2p1VSmu"].evaluate(eta,genmatch,wp_mu,"down")
        SF_e = self.taujson["DeepTau2017v2p1VSe"].evaluate(eta,genmatch,wp_e,"nom")
        SF_e_up = self.taujson["DeepTau2017v2p1VSe"].evaluate(eta,genmatch,wp_e,"up")
        SF_e_down = self.taujson["DeepTau2017v2p1VSe"].evaluate(eta,genmatch,wp_e,"down")
        SF = SF_jet * SF_mu * SF_e
        SF_jet_1prong_up = SF_jet
        SF_jet_1prong_down = SF_jet
        SF_jet_1prong1pi_up = SF_jet
        SF_jet_1prong1pi_down = SF_jet
        SF_jet_3prong_up = SF_jet
        SF_jet_3prong_down = SF_jet
        if dm==0: 
            SF_jet_1prong_up = SF_jet_up
            SF_jet_1prong_down = SF_jet_down
        elif dm==1 or dm==2:
            SF_jet_1prong1pi_up = SF_jet_up
            SF_jet_1prong1pi_down = SF_jet_down
        elif dm==10 or dm==11:
            SF_jet_3prong_up = SF_jet_up
            SF_jet_3prong_down = SF_jet_down
        return [SF,SF_jet,SF_jet_up,SF_jet_down,SF_mu,SF_mu_up,SF_mu_down,SF_e,SF_e_up,SF_e_down,SF_jet_1prong_up,SF_jet_1prong_down,SF_jet_1prong1pi_up,SF_jet_1prong1pi_down,SF_jet_3prong_up,SF_jet_3prong_down]
            
    
