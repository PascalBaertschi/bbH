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
        self.trigger_e = TrigObjMatcher(trigdata.combdict['SingleElectron'])
        self.trigger_etau = TrigObjMatcher(trigdata.combdict['etau'])
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
        self.out.nElectrons[0]              = self.nElectrons
        self.out.Etrigger_fired[0]          = self.Etrigger_fired
        self.out.Etautrigger_fired[0]       = self.Etautrigger_fired
        self.out.L1Tau_lep1[0]              = self.L1Tau_lep1
        self.out.L1Tau_lep2[0]              = self.L1Tau_lep2
        self.out.L1Tau_lep1_reco[0]         = self.L1Tau_lep1_reco
        self.out.L1Tau_lep2_reco[0]         = self.L1Tau_lep2_reco
        self.out.dielectron_pt[0]           = self.dielectron_pt
        self.out.dielectron_mass[0]         = self.dielectron_mass
        self.out.Ele1_pt[0]                 = self.Ele1_pt
        self.out.Ele1_eta[0]                = self.Ele1_eta
        self.out.Ele1_phi[0]                = self.Ele1_phi
        self.out.Ele1_mass[0]               = self.Ele1_mass
        self.out.Ele1_charge[0]             = self.Ele1_charge
        self.out.Ele1_iso[0]                = self.Ele1_iso
        self.out.Ele1_id[0]                 = self.Ele1_id
        self.out.Ele1_fired[0]              = self.Ele1_fired
        self.out.Ele1_etaufired[0]          = self.Ele1_etaufired
        self.out.Ele1_tag[0]                = self.Ele1_tag
        self.out.Ele2_pt[0]                 = self.Ele2_pt
        self.out.Ele2_eta[0]                = self.Ele2_eta
        self.out.Ele2_phi[0]                = self.Ele2_phi
        self.out.Ele2_mass[0]               = self.Ele2_mass
        self.out.Ele2_charge[0]             = self.Ele2_charge
        self.out.Ele2_iso[0]                = self.Ele2_iso
        self.out.Ele2_id[0]                 = self.Ele2_id
        self.out.Ele2_fired[0]              = self.Ele2_fired
        self.out.Ele2_etaufired[0]          = self.Ele2_etaufired
        self.out.Ele2_tag[0]                = self.Ele2_tag
        ## gen particles
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
        self.nElectrons            = -1
        self.Etrigger_fired        = False
        self.Etautrigger_fired     = False
        self.L1Tau_lep1            = False
        self.L1Tau_lep2            = False
        self.L1Tau_lep1_reco       = False
        self.L1Tau_lep2_reco       = False
        self.EventWeight           = 1.
        self.GenWeight             = 1.
        self.PUWeight              = 1.
        self.dielectron_pt         = -1.
        self.dielectron_mass       = -1.
        self.Ele1_pt               = -1.
        self.Ele1_eta              = -10.
        self.Ele1_phi              = -10.
        self.Ele1_mass             = -1.
        self.Ele1_charge           = -1.
        self.Ele1_iso              = -1.
        self.Ele1_id               = False
        self.Ele1_fired            = False
        self.Ele1_etaufired        = False
        self.Ele1_tag              = False
        self.Ele2_pt               = -1.
        self.Ele2_eta              = -10.
        self.Ele2_phi              = -10.
        self.Ele2_mass             = -1.
        self.Ele2_charge           = -1.
        self.Ele2_iso              = -1.
        self.Ele2_id               = False
        self.Ele2_fired            = False
        self.Ele2_etaufired        = False
        self.Ele2_tag              = False
        self.gendielectron_pt      = -1.
        self.gendielectron_mass    = -1.
        self.GenEle1_pt            = -1.
        self.GenEle1_eta           = -10.
        self.GenEle2_pt            = -1.
        self.GenEle2_eta           = -10.
      
        if self.year == 2016 and self.data_era in ["F","G","H"] and event.run>278240:
            self.trigger_etau = self.trigger_etau_postVFP
        
        if self.isMC:
            self.GenWeight = event.genWeight
            self.PUweight = event.puWeight
            self.EventWeight *= self.GenWeight
            self.EventWeight *= self.PUWeight

        electron_list = []
        electrons = Collection(event, "Electron")
               

        for electron in electrons:
            if electron.pt > 25. and abs(electron.eta) < 2.1 and abs(electron.dxy) < 0.045 and abs(electron.dz) < 0.2 and electron.convVeto and electron.lostHits < 2:
                electron_list.append(electron)
          
        self.nElectrons = len(electron_list)

        if  self.nElectrons<2:
            return False
        self.Etrigger_fired = self.trigger_e.fired(event)
        self.Etautrigger_fired = self.trigger_etau.fired(event)
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
            self.Ele1_id = electron1.mvaFall17V2noIso_WP90
            self.Ele1_fired = self.trigger_e.match(event,electron1,leg=1)
            self.Ele1_etaufired = self.trigger_etau.match_crosstrigger(event,electron1,leg=1)
            self.Ele1_tag = self.trigger_e_tag.match(event,electron1,leg=1)
            self.Ele2_pt = electron2.pt
            self.Ele2_eta = electron2.eta
            self.Ele2_phi = electron2.phi
            self.Ele2_mass = electron2.mass
            self.Ele2_charge = electron2.charge
            self.Ele2_iso    = electron2.pfRelIso03_all
            self.Ele2_id = electron2.mvaFall17V2noIso_WP90
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
            gen_electron_list = []

            for genPart in genParts:
                if abs(genPart.pdgId)==11 and genPart.pt > 25. and abs(genPart.eta) < 2.6:
                    gen_electron_list.append(genPart)
            self.nGenElectrons = len(gen_electron_list)
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
        
        
