import numpy as np
import correctionlib
import os
from ROOT import TVector3
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection,Object
#https://cms-nanoaod-integration.web.cern.ch/commonJSONSFs/summaries/JME_2018_UL_jmar.html

path_json = 'CorrectionTools/jsonpog-integration/POG/JME/'

class PUIdSF:
    
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
        self.puidjson = correctionlib.CorrectionSet.from_file(os.path.join(path_json,self.year_name,"jmar.json.gz"))

    def vec(self,jet):
        jet_v = TVector3()
        jet_v.SetPtEtaPhi(jet.pt,jet.eta,jet.phi)
        return jet_v

    def getSF(self, event, jet_list, sys):
        weight = 1.
        genjets = Collection(event,"GenJet")
        for jet in jet_list:
            if jet.puId !=0 and jet.pt < 50.:
                genmatch = False
                for genjet in genjets:
                    if self.vec(genjet).DeltaR(self.vec(jet)) < 0.4:
                        genmatch = True
                if genmatch:
                    weight *= self.puidjson["PUJetID_eff"].evaluate(jet.eta,jet.pt,sys,"L")
        return weight
            
    
