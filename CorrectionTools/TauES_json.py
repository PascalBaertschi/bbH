import numpy as np
import correctionlib
import os
# https://github.com/cms-tau-pog/TauTriggerSFs/tree/run2_SFs
# https://github.com/cms-tau-pog/TauIDSFs
#https://twiki.cern.ch/twiki/bin/viewauth/CMS/TauIDRecommendationForRun2
#https://cms-nanoaod-integration.web.cern.ch/commonJSONSFs/TAU_tau_Run2_UL/

path_json = 'CorrectionTools/jsonpog-integration/POG/TAU/'

class TauES:
    
    def __init__(self, year,VFPtag):
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


    def getES(self, pt, eta, dm, genmatch,tes):
        return self.taujson["tau_energy_scale"].evaluate(pt,eta,dm,genmatch,"DeepTau2017v2p1",tes)
            
    
