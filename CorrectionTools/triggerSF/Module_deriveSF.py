import ROOT
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection,Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

from TreeProducer import *
import struct
import utils as utils
from TrigObjMatcher import loadTriggerDataFromJSON, TrigObjMatcher
import numpy as np
import time
from array import array


DY_xsec = 6077.22
class Producer(Module):

    def __init__(self, name, DataType, filelist, **kwargs):
        
        self.name = name
        self.out = TreeProducer(name)
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
        self.tes            = kwargs.get('tes',      1.0  )
        self.ltf            = kwargs.get('ltf',      1.0  )
        self.jtf            = kwargs.get('jtf',      1.0 )
        year                = self.year
        jsonfile        = "/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/triggers/effmeasure_triggers_%d.json"%self.year
        trigdata        = loadTriggerDataFromJSON(jsonfile,isData=self.isData)
        self.trigger_mu = TrigObjMatcher(trigdata.combdict['SingleMuon'])
        self.trigger_e = TrigObjMatcher(trigdata.combdict['SingleElectron'])
        self.trigger_mutau = TrigObjMatcher(trigdata.combdict['mutau'])
        self.trigger_etau = TrigObjMatcher(trigdata.combdict['etau'])
        self.trigger_mu_tag = TrigObjMatcher(trigdata.combdict['SingleMuon_tag'])
        self.trigger_e_tag = TrigObjMatcher(trigdata.combdict['SingleElectron_tag'])
        jsonfile_postVFP        = "/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/triggers/effmeasure_triggers_2016_postVFP.json"
        trigdata_postVFP        = loadTriggerDataFromJSON(jsonfile_postVFP,isData=self.isData)
        self.trigger_etau_postVFP = TrigObjMatcher(trigdata_postVFP.combdict['etau'])
        self.LumiWeight = 1.
        if self.isMC:
            if self.year==2018:
                LUMI = 59740
            elif self.year==2017:
                LUMI = 41530
            elif self.year==2016:
                if self.preVFP=="_preVFP":
                    LUMI = 19500
                else:
                    LUMI = 16800

            JSON_path = '/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/triggerSF/json/UL%s%s/'%(self.year,self.preVFP)
            xsec = DY_xsec
            nevents = utils.getJSON(JSON_path,self.sample_name,self.year,self.ULtag,self.preVFP)
            self.LumiWeight = LUMI * xsec / nevents
   
    def beginJob(self):
        pass

    def endJob(self):
        self.out.outputfile.Write()
        self.out.outputfile.Close()

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass


    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):     
        pass
        
    def fillBranches(self,event):
        self.out.isMC[0]                    = self.isMC
        self.out.is2016[0]                  = self.is2016
        self.out.is2017[0]                  = self.is2017
        self.out.is2018[0]                  = self.is2018
        self.out.EventNumber[0]             = event.event
        self.out.LumiNumber[0]              = event.luminosityBlock
        self.out.RunNumber[0]               = event.run
        self.out.EventWeight[0]             = self.EventWeight
        self.out.LumiWeight[0]              = self.LumiWeight
        self.out.GenWeight[0]               = self.GenWeight
        self.out.PUWeight[0]                = self.PUWeight
        self.out.nMuons[0]                  = self.nMuons
        self.out.nElectrons[0]              = self.nElectrons
        self.out.Mutrigger_fired[0]         = self.Mutrigger_fired
        self.out.Etrigger_fired[0]          = self.Etrigger_fired
        self.out.Mutautrigger_fired[0]      = self.Mutautrigger_fired
        self.out.Etautrigger_fired[0]       = self.Etautrigger_fired
        self.out.L1Tau_lep1[0]              = self.L1Tau_lep1
        self.out.L1Tau_lep2[0]              = self.L1Tau_lep2
        self.out.L1Tau_lep1_reco[0]         = self.L1Tau_lep1_reco
        self.out.L1Tau_lep2_reco[0]         = self.L1Tau_lep2_reco
        self.out.dimuon_pt[0]               = self.dimuon_pt
        self.out.dimuon_mass[0]             = self.dimuon_mass
        self.out.Mu1_pt[0]                  = self.Mu1_pt
        self.out.Mu1_eta[0]                 = self.Mu1_eta
        self.out.Mu1_phi[0]                 = self.Mu1_phi
        self.out.Mu1_mass[0]                = self.Mu1_mass
        self.out.Mu1_charge[0]              = self.Mu1_charge
        self.out.Mu1_iso[0]                 = self.Mu1_iso
        self.out.Mu1_fired[0]               = self.Mu1_fired
        self.out.Mu1_mutaufired[0]          = self.Mu1_mutaufired
        self.out.Mu1_tag[0]                 = self.Mu1_tag
        self.out.Mu2_pt[0]                  = self.Mu2_pt
        self.out.Mu2_eta[0]                 = self.Mu2_eta
        self.out.Mu2_phi[0]                 = self.Mu2_phi
        self.out.Mu2_mass[0]                = self.Mu2_mass
        self.out.Mu2_charge[0]              = self.Mu2_charge
        self.out.Mu2_iso[0]                 = self.Mu2_iso
        self.out.Mu2_fired[0]               = self.Mu2_fired
        self.out.Mu2_mutaufired[0]          = self.Mu2_mutaufired
        self.out.Mu2_tag[0]                 = self.Mu2_tag
        self.out.dielectron_pt[0]           = self.dielectron_pt
        self.out.dielectron_mass[0]         = self.dielectron_mass
        self.out.Ele1_pt[0]                 = self.Ele1_pt
        self.out.Ele1_eta[0]                = self.Ele1_eta
        self.out.Ele1_phi[0]                = self.Ele1_phi
        self.out.Ele1_mass[0]               = self.Ele1_mass
        self.out.Ele1_charge[0]             = self.Ele1_charge
        self.out.Ele1_iso[0]                = self.Ele1_iso
        self.out.Ele1_fired[0]              = self.Ele1_fired
        self.out.Ele1_etaufired[0]          = self.Ele1_etaufired
        self.out.Ele1_tag[0]                = self.Ele1_tag
        self.out.Ele2_pt[0]                 = self.Ele2_pt
        self.out.Ele2_eta[0]                = self.Ele2_eta
        self.out.Ele2_phi[0]                = self.Ele2_phi
        self.out.Ele2_mass[0]               = self.Ele2_mass
        self.out.Ele2_charge[0]             = self.Ele2_charge
        self.out.Ele2_iso[0]                = self.Ele2_iso
        self.out.Ele2_fired[0]              = self.Ele2_fired
        self.out.Ele2_etaufired[0]          = self.Ele2_etaufired
        self.out.Ele2_tag[0]                = self.Ele2_tag
        ## gen particles
        self.out.nGenMuons[0]               = self.nGenMuons
        self.out.nGenElectrons[0]           = self.nGenElectrons
        self.out.gendimuon_pt[0]            = self.gendimuon_pt
        self.out.gendimuon_mass[0]          = self.gendimuon_mass
        self.out.GenMu1_pt[0]               = self.GenMu1_pt
        self.out.GenMu1_eta[0]              = self.GenMu1_eta
        self.out.GenMu2_pt[0]               = self.GenMu2_pt
        self.out.GenMu2_eta[0]              = self.GenMu2_eta
        self.out.gendielectron_pt[0]        = self.gendielectron_pt
        self.out.gendielectron_mass[0]      = self.gendielectron_mass
        self.out.GenEle1_pt[0]              = self.GenEle1_pt
        self.out.GenEle1_eta[0]             = self.GenEle1_eta
        self.out.GenEle2_pt[0]              = self.GenEle2_pt
        self.out.GenEle2_eta[0]             = self.GenEle2_eta




        self.out.tree.Fill()

    def tlv(self,lepton):
        lepton_tlv = ROOT.TLorentzVector()
        lepton_tlv.SetPtEtaPhiM(lepton.pt,lepton.eta,lepton.phi,lepton.mass)
        return lepton_tlv
        

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        #####   set variables     ####
        self.is2016                = False
        self.is2017                = False
        self.is2018                = False
        self.nMuons                = -1
        self.nElectrons            = -1
        self.Mutrigger_fired       = False
        self.Etrigger_fired        = False
        self.Mutautrigger_fired    = False
        self.Etautrigger_fired     = False
        self.L1Tau_lep1            = False
        self.L1Tau_lep2            = False
        self.L1Tau_lep1_reco       = False
        self.L1Tau_lep2_reco       = False
        self.EventWeight           = 1.
        self.GenWeight             = 1.
        self.PUWeight              = 1.
        self.dimuon_pt             = -1.
        self.dimuon_mass           = -1.
        self.Mu1_pt                = -1.
        self.Mu1_eta               = -10.
        self.Mu1_phi               = -10.
        self.Mu1_mass              = -1.
        self.Mu1_charge            = -1.
        self.Mu1_iso               = -1.
        self.Mu1_fired             = False
        self.Mu1_mutaufired        = False
        self.Mu1_tag               = False
        self.Mu2_pt                = -1.
        self.Mu2_eta               = -10.
        self.Mu2_phi               = -10.
        self.Mu2_mass              = -1.
        self.Mu2_charge            = -1.
        self.Mu2_iso               = -1.
        self.Mu2_fired             = False
        self.Mu2_mutaufired        = False
        self.Mu2_tag               = False
        self.dielectron_pt         = -1.
        self.dielectron_mass       = -1.
        self.Ele1_pt               = -1.
        self.Ele1_eta              = -10.
        self.Ele1_phi              = -10.
        self.Ele1_mass             = -1.
        self.Ele1_charge           = -1.
        self.Ele1_iso              = -1.
        self.Ele1_fired            = False
        self.Ele1_etaufired        = False
        self.Ele1_tag              = False
        self.Ele2_pt               = -1.
        self.Ele2_eta              = -10.
        self.Ele2_phi              = -10.
        self.Ele2_mass             = -1.
        self.Ele2_charge           = -1.
        self.Ele2_iso              = -1.
        self.Ele2_fired            = False
        self.Ele2_etaufired        = False
        self.Ele2_tag              = False
        self.nGenMuons             = -1
        self.nGenElectrons         = -1
        self.gendimuon_pt          = -1.
        self.gendimuon_mass        = -1.
        self.GenMu1_pt             = -1.
        self.GenMu1_eta            = -10.
        self.GenMu2_pt             = -1.
        self.GenMu2_eta            = -10.
        self.gendielectron_pt      = -1.
        self.gendielectron_mass    = -1.
        self.GenEle1_pt            = -1.
        self.GenEle1_eta           = -10.
        self.GenEle2_pt            = -1.
        self.GenEle2_eta           = -10.
      
        if self.year == 2016 and self.data_era in ["F","G","H"] and event.run>278240:
            self.trigger_etau = self.trigger_etau_postVFP
        
        if "SingleElectron_Run2016B" in self.sample:
            try:
                trigger1 = event.HLT_IsoMu22_eta2p1
                trigger2 = event.HLT_IsoTkMu22_eta2p1
            except:
                event.HLT_IsoMu22_eta2p1 = False
                event.HLT_IsoTkMu22_eta2p1 = False 
        
        if self.isMC:
            self.GenWeight = event.genWeight
            self.PUweight = event.puWeight
            self.EventWeight *= self.GenWeight
            self.EventWeight *= self.PUWeight

        muon_list = []
        electron_list = []
        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
       
        for muon in muons:
            if muon.pt > 10. and abs(muon.eta) < 2.4 and abs(muon.dxy) < 0.045 and abs(muon.dz) < 0.2 and muon.pfRelIso04_all < 0.3:
                if muon.pt > 20. and muon.mediumId and muon.pfRelIso04_all < 0.15:
                    muon_list.append(muon)
               

        for electron in electrons:
            if electron.pt > 10. and abs(electron.eta) < 2.5 and abs(electron.dxy) < 0.045 and abs(electron.dz) < 0.2 and electron.mvaFall17V2noIso_WP90 and electron.pfRelIso03_all < 0.3:
                if electron.pt > 25. and abs(electron.eta) < 2.1 and electron.convVeto and electron.lostHits < 2 and electron.pfRelIso03_all < 0.1:
                    electron_list.append(electron)


        self.nMuons     = len(muon_list)           
        self.nElectrons = len(electron_list)

        if self.nMuons<2 and self.nElectrons<2:
            return False
        self.Mutrigger_fired = self.trigger_mu.fired(event)
        self.Etrigger_fired = self.trigger_e.fired(event)
        self.Mutautrigger_fired = self.trigger_mutau.fired(event)
        self.Etautrigger_fired = self.trigger_etau.fired(event)
        if self.nMuons>1:
            muon1 = muon_list[0]
            muon2 = muon_list[1]
            dimuon = self.tlv(muon1)+self.tlv(muon2)
            self.dimuon_pt = dimuon.Pt()
            self.dimuon_mass = dimuon.M()
            self.Mu1_pt = muon1.pt
            self.Mu1_eta = muon1.eta
            self.Mu1_phi = muon1.phi
            self.Mu1_mass = muon1.mass
            self.Mu1_charge = muon1.charge
            self.Mu1_iso    = muon1.pfRelIso04_all
            self.Mu1_fired = self.trigger_mu.match(event,muon1,leg=1)
            self.Mu1_mutaufired = self.trigger_mutau.match_crosstrigger(event,muon1,leg=1)
            self.Mu1_tag = self.trigger_mu_tag.match(event,muon1,leg=1)
            self.Mu2_pt = muon2.pt
            self.Mu2_eta = muon2.eta
            self.Mu2_phi = muon2.phi
            self.Mu2_mass = muon2.mass
            self.Mu2_charge = muon2.charge
            self.Mu2_iso    = muon2.pfRelIso04_all
            self.Mu2_fired = self.trigger_mu.match(event,muon2,leg=1)
            self.Mu2_mutaufired = self.trigger_mutau.match_crosstrigger(event,muon2,leg=1)
            self.Mu2_tag = self.trigger_mu_tag.match(event,muon2,leg=1)
            if self.year == 2016:
                self.L1Tau_lep1 = True
                self.L1Tau_lep2 = True
                self.L1Tau_lep1_reco = True
                self.L1Tau_lep2_reco = True
            else:
                self.L1Tau_lep1 = self.trigger_mutau.findL1Tau(event,24.,muon1,13)
                self.L1Tau_lep2 = self.trigger_mutau.findL1Tau(event,24.,muon2,13)
                self.L1Tau_lep1_reco = self.trigger_mutau.findL1Tau_reco(event,24.,muon1,13)
                self.L1Tau_lep2_reco = self.trigger_mutau.findL1Tau_reco(event,24.,muon2,13)
        if self.nElectrons>1:
            electron1 = electron_list[0]
            electron2 = electron_list[1]
            dielectron = self.tlv(electron1)+self.tlv(electron2)
            self.dielectron_pt = dielectron.Pt()
            self.dielectron_mass = dielectron.M()
            self.Ele1_pt = electron1.pt
            self.Ele1_eta = electron1.eta
            self.Ele1_phi = electron1.phi
            self.Ele1_mass = electron1.mass
            self.Ele1_charge = electron1.charge
            self.Ele1_iso    = electron1.pfRelIso03_all
            self.Ele1_fired = self.trigger_e.match(event,electron1,leg=1)
            self.Ele1_etaufired = self.trigger_etau.match_crosstrigger(event,electron1,leg=1)
            self.Ele1_tag = self.trigger_e_tag.match(event,electron1,leg=1)
            self.Ele2_pt = electron2.pt
            self.Ele2_eta = electron2.eta
            self.Ele2_phi = electron2.phi
            self.Ele2_mass = electron2.mass
            self.Ele2_charge = electron2.charge
            self.Ele2_iso    = electron2.pfRelIso03_all
            self.Ele2_fired = self.trigger_e.match(event,electron2,leg=1)
            self.Ele2_etaufired = self.trigger_etau.match_crosstrigger(event,electron2,leg=1)
            self.Ele2_tag = self.trigger_e_tag.match(event,electron2,leg=1)
            if self.year == 2016:
                if self.data_era in ["F","G","H"] and event.run>278240:
                    self.L1Tau_lep1 = self.trigger_etau.findL1Tau(event,26.,electron1,11)
                    self.L1Tau_lep2 = self.trigger_etau.findL1Tau(event,26.,electron2,11)
                    self.L1Tau_lep1_reco = self.trigger_etau.findL1Tau_reco(event,26.,electron1,11)
                    self.L1Tau_lep2_reco = self.trigger_etau.findL1Tau_reco(event,26.,electron2,11)
                else:
                    self.L1Tau_lep1 = True
                    self.L1Tau_lep2 = True
                    self.L1Tau_lep1_reco = True
                    self.L1Tau_lep2_reco = True
            else: #2017,2018
                self.L1Tau_lep1 = self.trigger_etau.findL1Tau(event,24.,electron1,11)
                self.L1Tau_lep2 = self.trigger_etau.findL1Tau(event,24.,electron2,11)
                self.L1Tau_lep1_reco = self.trigger_etau.findL1Tau_reco(event,24.,electron1,11)
                self.L1Tau_lep2_reco = self.trigger_etau.findL1Tau_reco(event,24.,electron2,11)

        #gen Particles   
        if self.isMC:
            genParts = Collection(event,"GenPart")
            gen_muon_list = []
            gen_electron_list = []

            for genPart in genParts:
                if abs(genPart.pdgId)==11 and genPart.pt > 25. and abs(genPart.eta) < 2.6:
                    gen_electron_list.append(genPart)
                elif abs(genPart.pdgId)==13 and genPart.pt > 20. and abs(genPart.eta) < 2.6:
                    gen_muon_list.append(genPart)

            self.nGenMuons = len(gen_muon_list)
            self.nGenElectrons = len(gen_electron_list)

            if self.nGenMuons>1:
                genmuon1 = gen_muon_list[0]
                genmuon2 = gen_muon_list[1]
                gendimuon = self.tlv(genmuon1)+self.tlv(genmuon2)
                self.gendimuon_pt = gendimuon.Pt()
                self.gendimuon_mass = gendimuon.M()
                self.GenMu1_pt = genmuon1.pt
                self.GenMu1_eta = genmuon1.eta
                self.GenMu2_pt = genmuon2.pt
                self.GenMu2_eta = genmuon2.eta
            if self.nGenElectrons>1:
                genelectron1 = gen_electron_list[0]
                genelectron2 = gen_electron_list[1]
                gendielectron = self.tlv(genelectron1)+self.tlv(genelectron2)
                self.gendielectron_pt = gendielectron.Pt()
                self.gendielectron_mass = gendielectron.M()
                self.GenEle1_pt = genelectron1.pt
                self.GenEle1_eta = genelectron1.eta
                self.GenEle2_pt = genelectron2.pt
                self.GenEle2_eta = genelectron2.eta

        self.fillBranches(event)
        return True
        
        
