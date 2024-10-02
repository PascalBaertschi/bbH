import ROOT
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection,Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

from TreeProducer import *
from TreeProducerCommon import *
from CorrectionTools.TauES_json import *
from CorrectionTools.TrigObjMatcher import loadTriggerDataFromJSON, TrigObjMatcher
import struct
from xsections import xsection
import plotting.utils as utils
import numpy as np
import time
from array import array

        
class Producer(Module):

    def __init__(self, name, DataType, filelist, **kwargs):
        
        self.name = name
        self.sample = filelist[0].split("/")[-4]
        self.sample_name = self.sample.split("__")[0]
        self.data_era = None

        if DataType=='data':
            self.isData = True
            self.isMC = False
            self.data_era = self.sample[self.sample.find("Run")+7]
        else:
            self.isData = False
            self.isMC = True
        self.year           = kwargs.get('year',     2018 )
        self.ULtag          = kwargs.get('ULtag',    "" )
        self.preVFP         = kwargs.get('preVFP', "")
        self.tes            = kwargs.get('tes',    "")
        self.ltf            = kwargs.get('ltf',      1.0  )
        self.jtf            = kwargs.get('jtf',      1.0 )
        self.calcSVFit      = kwargs.get('doSVFit')
        self.JECvar         = kwargs.get('JECvar', "")
        year                = self.year
        self.METfilter         = getMETFilters(year,self.ULtag,self.isData)
        ##### Trigger ####
        jsonfile        = "CorrectionTools/triggers/tau_triggers_%d.json"%self.year
        trigdata        = loadTriggerDataFromJSON(jsonfile,isData=self.isData)
        self.trigger_Mu = TrigObjMatcher(trigdata.combdict['SingleMuon'])
        self.trigger_E = TrigObjMatcher(trigdata.combdict['SingleElectron'])
        self.tauES = TauES(self.year,self.preVFP)
   
    def beginJob(self):
        pass

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass


    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):     
        pass

    def vec(self,lepton):
        lepton_v = TVector3()
        lepton_v.SetPtEtaPhi(lepton.pt,lepton.eta,lepton.phi)
        return lepton_v

    def tlv(self,lepton):
        lepton_tlv = TLorentzVector()
        lepton_tlv.SetPtEtaPhiM(lepton.pt,lepton.eta,lepton.phi,lepton.mass)
        return lepton_tlv      

    def iso(self, lepton):
        try:
            return lepton.pfRelIso04_all
        except RuntimeError:
            try: 
                return lepton.rawDeepTau2017v2p1VSjet
            except RuntimeError:
                try:
                    return lepton.pfRelIso03_all
                except RuntimeError:
                    print("ERROR: No Isolation found!")

    def isocheck(self,lepton,checkvalue):
        self.moreiso = False
        try:
            if lepton.pfRelIso04_all < checkvalue:          #muon more isolated -> smaller value
                self.moreiso = True
        except RuntimeError:
            try:
                if lepton.pfRelIso03_all < checkvalue:          #electron more isolated -> smaller value
                    self.moreiso = True
            except RuntimeError:
                try:
                    if lepton.rawDeepTau2017v2p1VSjet > checkvalue: #tau more isolated -> larger value
                        self.moreiso = True
                except RuntimeError:
                    print("ERROR: No Isolation found!")
        return self.moreiso

    def pair_selection(self,list):
        list = np.array(list)
        best_pair = 0
        for i in range(len(list)):
            if i==0:
                lep1_iso = self.iso(list[i,0])
            else:
                if self.isocheck(list[i,0],lep1_iso):     #take pair with most isolated lepton1
                    lep1_iso = self.iso(list[i,0])
                    best_pair = i
                elif self.iso(list[i,0]) == lep1_iso:     #if two pairs with same isolation of lepton 1:
                    if list[i,0].pt > list[best_pair,0].pt:      # take pair with highest pt of lepton 1
                        best_pair = i
                    elif list[i,0].pt == list[best_pair,0].pt:   # if two pairs with same pt of lepton 1:  
                        if self.isocheck(list[i,1],self.iso(list[best_pair,1])): # take pair with most isolated lepton 2
                            best_pair = i
                        elif self.iso(list[i,1]) == self.iso(list[best_pair,1]): # if two pairs with same isolation of lepton 2:
                            if list[i,1].pt > list[best_pair,1].pt:                 # take pair with highest pt of lepton 2
                                best_pair = i
        return list[best_pair]



    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        #####   set variables     ####
        self.nGenBjets             = 0
        self.isHtoMuTau            = False
        self.isHtoETau             = False
        self.Mu1_sltrig_fired      = False
        self.Ele1_sltrig_fired     = False
        self.MuTrigger_fired       = False
        self.ETrigger_fired        = False
        #############   Gen Weight ######################
        if self.isMC:
            genJets = Collection(event, "GenJet")
            genJets_list = []
            for genJet in genJets:
                if abs(genJet.hadronFlavour)==5:
                    genJets_list.append(genJet)
          
            self.nGenBjets = len(genJets_list)
            # only for ggH samples
            if "HToTauTau" in self.sample:
                genParticles = Collection(event,"GenPart")
                genParts_list = []
                genParts_checklist = []
                genParts_mother_checklist = []
                for i,genPart in enumerate(genParticles):
                    if genPart.status==2 and str(abs(genPart.pdgId))[0]=="5" and len(str(abs(genPart.pdgId))) in [3,4]:
                        genParts_checklist.append(i)
                        genParts_mother_checklist.append(genPart.genPartIdxMother)
                for idx in genParts_checklist:
                    if idx not in genParts_mother_checklist:
                        genParts_list.append(genParticles[idx])
                GenBjet_match = 0
                if self.nGenBjets==1:
                    for genB in genParts_list:
                        if genJets_list[0].DeltaR(genB)<1.5:
                            GenBjet_match += 1
        
        if not self.isData:
            #self.out.pileup.Fill(event.Pileup_nTrueInt)
            if event.Pileup_nTrueInt == 0:
                return False

        if "ZZTo2Nu2Q_5f" in self.sample and self.year==2018:
            try:
                trigger1 = event.HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTauHPS30_eta2p1_CrossL1
                trigger2 = event.HLT_Ele35_WPTight_Gsf
                trigger3 = event.HLT_IsoMu20_eta2p1_LooseChargedIsoPFTauHPS27_eta2p1_CrossL1
            except:
                event.HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTauHPS30_eta2p1_CrossL1 = False
                event.HLT_Ele35_WPTight_Gsf = False
                event.HLT_IsoMu20_eta2p1_LooseChargedIsoPFTauHPS27_eta2p1_CrossL1 = False
                
        # only selecting events with zero jets for inclusive DYjets sample to combine with jet binned samples
        if self.sample_name=="DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8":
            if event.LHE_Njets>0:
                return False
        if self.sample_name=="WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8":
            if event.LHE_Njets>0:
                return False
        #splitting sample bbHToTauTau_M-125_4FS_TuneCP5_yt2
        if "bbHToTauTau_M-125_4FS_TuneCP5_yt2" in self.sample:
            if self.nGenBjets==0 or (self.nGenBjets==1 and GenBjet_match<2):
                return False
        if "jjHToTauTau_M-125_4FS_TuneCP5_yt2" in self.sample:
            if self.nGenBjets>0:
                return False    
        #splitting sample ggH
        if "GluGluHToTauTau" in self.sample:
            if self.nGenBjets==0 or self.nGenBjets>1 or (self.nGenBjets==1 and GenBjet_match>1):
                return False
        if "GGFHToTauTau" in self.sample and self.nGenBjets>0:
            return False  
        #splitting sample bbHToTauTau_M-125_4FS_TuneCP5_yb2
        if "bbHToTauTau_M-125_4FS_TuneCP5_yb2" in self.sample:
            if self.nGenBjets==0:
                return False
        if "jjHToTauTau_M-125_4FS_TuneCP5_yb2" in self.sample:
            if self.nGenBjets>0:
                return False
        #splitting interference sample
        if "bbHToTauTau_M-125_4FS_ybyt_TuneCP5" in self.sample:
            if self.nGenBjets==0:
                return False
        if "jjHToTauTau_M-125_4FS_ybyt_TuneCP5" in self.sample:
            if self.nGenBjets>0:
                return False

        ############  lepton selection  ####################
        tau_vetomu_list = []
        tau_vetoe_list = []
        muon_list = []
        electron_list = []
        mutau_list =[]
        etau_list = []
        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        taus = Collection(event, "Tau")
        

        for tau in taus:
            try:
                tau_idDecayMode = tau.idDecayMode
            except:
                tau_idDecayMode = tau.idDecayModeOldDMs

            if tau.decayMode==0: tau_decaymode = 0
            elif tau.decayMode in [1,2]: tau_decaymode = 1
            elif tau.decayMode in [10,11]: tau_decaymode = 10
            else: continue #only use tau with decaymodes 0,1,2,10 or 11

            tau_tlv = self.tlv(tau)
            if self.isMC:
                tau_energyscale = self.tauES.getES(tau.pt,tau.eta,tau_decaymode,genmatching(event,tau),"nom")
                tau_tlv = tau_tlv * tau_energyscale
                tau.pt = tau_tlv.Pt()
                tau.eta = tau_tlv.Eta()
                tau.phi = tau_tlv.Phi()
                tau.mass = tau_tlv.M()
                tau.es = tau_energyscale

            if tau.pt > 30. and abs(tau.eta) < 2.3 and abs(tau.charge) == 1 and abs(tau.dz) < 0.2 and tau_idDecayMode and tau.idDeepTau2017v2p1VSjet >= 31:
                if tau.idDeepTau2017v2p1VSe >= 3 and tau.idDeepTau2017v2p1VSmu == 15:
                    tau_vetomu_list.append(tau)
                if tau.idDeepTau2017v2p1VSe >= 63 and tau.idDeepTau2017v2p1VSmu >= 1:
                    tau_vetoe_list.append(tau)
                    
        #disregard event if no taus for skimming
        if len(tau_vetomu_list)==0 and len(tau_vetoe_list)==0:
            return False

        for muon in muons:
            if muon.pt > 20. and abs(muon.eta) < 2.4 and abs(muon.dxy) < 0.045 and abs(muon.dz) < 0.2 and muon.pfRelIso04_all < 0.15 and muon.mediumId:
                muon_list.append(muon)
                
        for electron in electrons:
            if electron.pt > 25. and abs(electron.eta) < 2.1 and (abs(electron.eta)<1.444 or abs(electron.eta)>1.566) and abs(electron.dxy) < 0.045 and abs(electron.dz) < 0.2 and electron.mvaFall17V2noIso_WP90 and electron.pfRelIso03_all < 0.1 and electron.convVeto and electron.lostHits < 2:
                electron_list.append(electron)

        for tau in tau_vetomu_list:
            for muon in muon_list:
                if self.vec(tau).DeltaR(self.vec(muon)) > 0.5:
                    mutau_list.append([muon,tau])
                    self.isHtoMuTau = True
        for tau in tau_vetoe_list:
            for ele in electron_list:
                if self.vec(tau).DeltaR(self.vec(ele)) > 0.5:
                    etau_list.append([ele,tau])
                    self.isHtoETau = True
            
        if not (self.isHtoMuTau or self.isHtoETau):
            return False
        

        if self.isHtoMuTau:
            pair = self.pair_selection(mutau_list)
        elif self.isHtoETau:
            pair = self.pair_selection(etau_list)


        if self.METfilter(event)==False:
            return False

        self.MuTrigger_fired = self.trigger_Mu.fired(event)
        self.ETrigger_fired = self.trigger_E.fired(event)
            
        if self.isHtoMuTau:
            self.Mu1_sltrig_fired = self.trigger_Mu.match(event,pair[0])
            if not self.MuTrigger_fired:
                return False
            if not self.Mu1_sltrig_fired:
                return False

        elif self.isHtoETau:
            self.Ele1_sltrig_fired = self.trigger_E.match(event,pair[0])
            if not self.ETrigger_fired:
                return False
            if not self.Ele1_sltrig_fired:
                return False

        return True
        
        
