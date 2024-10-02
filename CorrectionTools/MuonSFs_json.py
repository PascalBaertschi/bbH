import numpy as np
from ROOT import TFile, RooArgList
from array import array
import os
import correctionlib
# https://twiki.cern.ch/twiki/bin/view/CMS/MuonReferenceEffs2018
# https://twiki.cern.ch/twiki/bin/view/CMS/MuonUL2018
# https://twiki.cern.ch/twiki/bin/view/CMS/MuonUL2017
# https://twiki.cern.ch/twiki/bin/view/CMS/MuonUL2016
#https://gitlab.cern.ch/cms-nanoAOD/jsonpog-integration/
#https://cms-nanoaod-integration.web.cern.ch/commonJSONSFs/MUO_muon_Z_Run2_UL/

path = 'CorrectionTools/leptonEfficiencies/MuonPOG/'
path_json = 'CorrectionTools/jsonpog-integration/POG/MUO/'
triggerSFpath = 'CorrectionTools/triggerSF/root/'
class MuonSFs:
    
    def __init__(self, year,ULtag,preVFP):
        """Load histograms from files."""
        assert year in [2016,2017,2018], "MuonSFs: You must choose a year from: 2016, 2017 or 2018."
        self.year = year
        if year==2016:
            sftool_file = TFile.Open(path+"RunUL2016/htt_scalefactors_legacy_2016.root")
            sftool_workframe=sftool_file.Get("w")
            sftool_file.Close()
            self.sftool_trig = sftool_workframe.function("m_trg_ic_ratio").functor(RooArgList(sftool_workframe.argSet("m_pt,m_eta")))
            self.sftool_trig_data = sftool_workframe.function("m_trg_ic_data").functor(RooArgList(sftool_workframe.argSet("m_pt,m_eta")))
            self.sftool_trig_mc = sftool_workframe.function("m_trg_ic_mc").functor(RooArgList(sftool_workframe.argSet("m_pt,m_eta")))
            self.sftool_trig_data_ele = sftool_workframe.function("e_trg_ic_data").functor(RooArgList(sftool_workframe.argSet("e_pt,e_eta")))  #ELECTRONS
            self.sftool_trig_mc_ele = sftool_workframe.function("e_trg_ic_mc").functor(RooArgList(sftool_workframe.argSet("e_pt,e_eta")))      #ELECTRONS
            if preVFP=="_preVFP":
                self.year_name = "2016preVFP_UL"
            else:
                self.year_name = "2016postVFP_UL"
        elif year==2017:
            self.year_name = "2017_UL"
            sftool_file = TFile.Open(path+"RunUL2017/htt_scalefactors_legacy_2017.root")
            sftool_workframe=sftool_file.Get("w")
            sftool_file.Close()
            self.sftool_trig = sftool_workframe.function("m_trg_ic_ratio").functor(RooArgList(sftool_workframe.argSet("m_pt,m_eta")))
            self.sftool_trig_data = sftool_workframe.function("m_trg_ic_data").functor(RooArgList(sftool_workframe.argSet("m_pt,m_eta")))
            self.sftool_trig_mc = sftool_workframe.function("m_trg_ic_mc").functor(RooArgList(sftool_workframe.argSet("m_pt,m_eta")))
            self.sftool_trig_data_ele = sftool_workframe.function("e_trg_ic_data").functor(RooArgList(sftool_workframe.argSet("e_pt,e_eta"))) #ELECTRONS
            self.sftool_trig_mc_ele = sftool_workframe.function("e_trg_ic_mc").functor(RooArgList(sftool_workframe.argSet("e_pt,e_eta")))     #ELECTRONS
        elif year==2018:
            self.year_name = "2018_UL"
            sftool_file = TFile.Open(path+"RunUL2018/htt_scalefactors_legacy_2018.root")
            sftool_workframe=sftool_file.Get("w")
            sftool_file.Close()
            self.sftool_trig = sftool_workframe.function("m_trg_ic_ratio").functor(RooArgList(sftool_workframe.argSet("m_pt,m_eta")))
            self.sftool_trig_data = sftool_workframe.function("m_trg_ic_data").functor(RooArgList(sftool_workframe.argSet("m_pt,m_eta")))
            self.sftool_trig_mc = sftool_workframe.function("m_trg_ic_mc").functor(RooArgList(sftool_workframe.argSet("m_pt,m_eta")))
            self.sftool_trig_data_ele = sftool_workframe.function("e_trg_ic_data").functor(RooArgList(sftool_workframe.argSet("e_pt,e_eta")))  #ELECTRONS
            self.sftool_trig_mc_ele = sftool_workframe.function("e_trg_ic_mc").functor(RooArgList(sftool_workframe.argSet("e_pt,e_eta")))      #ELECTRONS
        self.muonjson = correctionlib.CorrectionSet.from_file(os.path.join(path_json,self.year_name,"muon_Z.json.gz"))

    def getTriggerSF(self,pt,eta):
        return self.sftool_trig.eval(array('d',[pt,eta]))

    def getTriggerSFMuMu(self,pt1,eta1,pt2,eta2):
        eff_data1 = self.sftool_trig_data.eval(array('d',[pt1,eta1])) 
        eff_mc1 = self.sftool_trig_mc.eval(array('d',[pt1,eta1]))
        eff_data2 = self.sftool_trig_data.eval(array('d',[pt2,eta2])) 
        eff_mc2 = self.sftool_trig_mc.eval(array('d',[pt2,eta2]))
        SF = (eff_data1+eff_data2-(eff_data1*eff_data2))/(eff_mc1+eff_mc2-(eff_mc1*eff_mc2))
        SF_up = SF+(SF*0.02)
        SF_down = SF-(SF*0.02)
        return [SF,SF_up,SF_down]   

    def getTriggerSFMuE(self,Mu_pt,Mu_eta,Ele_pt,Ele_eta):
        eff_data_mu = self.sftool_trig_data.eval(array('d',[Mu_pt,Mu_eta])) 
        eff_mc_mu = self.sftool_trig_mc.eval(array('d',[Mu_pt,Mu_eta]))
        eff_data_ele = self.sftool_trig_data_ele.eval(array('d',[Ele_pt,Ele_eta])) 
        eff_mc_ele = self.sftool_trig_mc_ele.eval(array('d',[Ele_pt,Ele_eta]))
        SF = (eff_data_mu+eff_data_ele-(eff_data_mu*eff_data_ele))/(eff_mc_mu+eff_mc_ele-(eff_mc_mu*eff_mc_ele))
        SF_up = SF+(SF*0.02)
        SF_down = SF-(SF*0.02)
        return [SF,SF_up,SF_down]       
    
    
    def getSF(self, pt, eta):
        IdSF = self.muonjson["NUM_MediumID_DEN_TrackerMuons"].evaluate(self.year_name,abs(eta),pt,"sf")
        IdSFerror = self.muonjson["NUM_MediumID_DEN_TrackerMuons"].evaluate(self.year_name,abs(eta),pt,"stat")
        IsoSF = self.muonjson["NUM_TightRelIso_DEN_MediumID"].evaluate(self.year_name,abs(eta),pt,"sf")
        IsoSFerror = self.muonjson["NUM_TightRelIso_DEN_MediumID"].evaluate(self.year_name,abs(eta),pt,"stat")
        sigma = np.sqrt((IdSFerror*IsoSF)**2+(IdSF*IsoSFerror)**2)
        SF = IdSF*IsoSF
        SF_up = SF+sigma
        SF_down = SF-sigma
        return [SF,SF_up,SF_down]

    def getSFMuMu(self, pt1, eta1, pt2, eta2):
        IdSF1 = self.muonjson["NUM_MediumID_DEN_TrackerMuons"].evaluate(self.year_name,abs(eta1),pt1,"sf")
        IdSFerror1 = self.muonjson["NUM_MediumID_DEN_TrackerMuons"].evaluate(self.year_name,abs(eta1),pt1,"stat")
        IsoSF1 = self.muonjson["NUM_TightRelIso_DEN_MediumID"].evaluate(self.year_name,abs(eta1),pt1,"sf")
        IsoSFerror1 = self.muonjson["NUM_TightRelIso_DEN_MediumID"].evaluate(self.year_name,abs(eta1),pt1,"stat")
        IdSF2 = self.muonjson["NUM_MediumID_DEN_TrackerMuons"].evaluate(self.year_name,abs(eta2),pt2,"sf")
        IdSFerror2 = self.muonjson["NUM_MediumID_DEN_TrackerMuons"].evaluate(self.year_name,abs(eta2),pt2,"stat")
        IsoSF2 = self.muonjson["NUM_TightRelIso_DEN_MediumID"].evaluate(self.year_name,abs(eta2),pt2,"sf")
        IsoSFerror2 = self.muonjson["NUM_TightRelIso_DEN_MediumID"].evaluate(self.year_name,abs(eta2),pt2,"stat")
        sigma = np.sqrt((IdSFerror1*IsoSF1*IdSF2*IsoSF2)**2+(IsoSFerror1*IdSF1*IdSF2*IsoSF2)**2+(IdSFerror2*IdSF1*IsoSF1*IsoSF2)**2+(IsoSFerror2*IdSF1*IsoSF1*IdSF2)**2)
        SF = IdSF1*IsoSF1*IdSF2*IsoSF2
        SF_up = SF+sigma
        SF_down = SF-sigma
        return [SF,SF_up,SF_down]
