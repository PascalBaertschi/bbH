import ROOT
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection,Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

from TreeProducer import *
from TreeProducerCommon import *
from CorrectionTools.BTaggingTool_json import BTagWeightTool, BTagWPs
from CorrectionTools.TauSFs_json import *
from CorrectionTools.TriggerSF import *
from CorrectionTools.MuonSFs_json import *
from CorrectionTools.ElectronSFs_json import *
from CorrectionTools.TauEmbeddedSFs_json import *
from CorrectionTools.TauES_json import *
from CorrectionTools.TrigObjMatcher import loadTriggerDataFromJSON, TrigObjMatcher
from CorrectionTools.MCCorrection import *
from CorrectionTools.fakefactor import ffclass
from CorrectionTools.ffunc import ffuncclass
from CorrectionTools.PileupWeightTool import *
import struct
from xsections import xsection
import plotting.utils as utils
import numpy as np
import time
from array import array

class Producer(Module):

    def __init__(self, name, DataType, filelist, **kwargs):
        
        self.name = name
        self.out = TreeProducer(name)
        self.sample = filelist[0].split("/")[-4]
        self.sample_name = self.sample.split("__")[0]
        if "Embedding" in filelist[0]:
            self.sample = filelist[0].split("/")[-3]
            self.sample_name = self.sample.split("_")[0]
        self.data_era = None

        if DataType=='data':
            self.isData = True
            self.isMC = False
            self.data_era = self.sample[self.sample.find("Run")+7]
        else:
            self.isData = False
            self.isMC = True

        
        ROOT.gSystem.Load('$CMSSW_BASE/lib/$SCRAM_ARCH/libTauAnalysisNanoToolsInterface.so')
        ROOT.gROOT.ProcessLine('#include "TauAnalysis/NanoToolsInterface/interface/InterfaceFastMTT.h"')
        self.mysvinterface = ROOT.InterfaceFastMTT()
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
        self.ffunc = ffuncclass(year)
        self.ff = ffclass(year)
        if "DY" in self.sample_name:
            if "madgraphMLM" in self.sample_name:
                self.MCCorrection = MCCorrection(self.year,"LO")
            elif "amcatnloFXFX" in self.sample_name:
                self.MCCorrection = MCCorrection(self.year,"NLO")
            elif "powhegMiNNLO" in self.sample_name:
                self.MCCorrection = MCCorrection(self.year,"NLO")
        elif "TT" in self.sample_name:
            self.MCCorrection = MCCorrection(self.year)
        elif "WJets" in self.sample_name and "amcatnloFXFX" in self.sample_name:
            self.MCCorrection = MCCorrection(self.year)
        self.puWeightProducer = puWeightProducer(self.year,self.preVFP)
        ##### Trigger ####
        if "HPS" in self.sample:
            jsonfile        = "CorrectionTools/triggers/tau_triggers_%d_HPS.json"%self.year
        else:
            jsonfile        = "CorrectionTools/triggers/tau_triggers_%d.json"%self.year
        if "TauEmbedding" in self.sample_name:
            trigdata        = loadTriggerDataFromJSON(jsonfile,isData=False) #Take MC triggers for Tau Embedding
        else:
            trigdata        = loadTriggerDataFromJSON(jsonfile,isData=self.isData)
        self.trigger_Mu = TrigObjMatcher(trigdata.combdict['SingleMuon'])
        self.trigger_MuTau    = TrigObjMatcher(trigdata.combdict['mutau'])
        self.trigger_E = TrigObjMatcher(trigdata.combdict['SingleElectron'])
        self.trigger_ETau = TrigObjMatcher(trigdata.combdict['etau'])
        self.trigger_MET = TrigObjMatcher(trigdata.combdict['MET'])
        if self.year==2018 and self.isData and not "TauEmbedding" in self.sample_name:
            self.trigger_MuTau_HPS = TrigObjMatcher(trigdata.combdict['mutau_HPS'])
            self.trigger_MuTau_noHPS = TrigObjMatcher(trigdata.combdict['mutau_noHPS'])
            self.trigger_ETau_HPS = TrigObjMatcher(trigdata.combdict['etau_HPS'])
            self.trigger_ETau_noHPS = TrigObjMatcher(trigdata.combdict['etau_noHPS'])
        self.count_genJet_pos = 0
        self.count_genJet_neg = 0
        ##################
        self.LumiWeight = 1. #for data
        self.btagToolWP = BTagWPs(self.year,self.preVFP)
        if self.year==2018:
            self.TauEmbeddedSFs = TauEmbeddedSFs(self.year,self.preVFP)
        if self.isMC:
            self.btagTool = BTagWeightTool('DeepJet','medium',self.year, self.preVFP)
            self.muSFs   = MuonSFs(self.year,self.ULtag, self.preVFP)
            self.eSFs    = ElectronSFs(self.year,self.ULtag, self.preVFP)
            self.tauSFs  = TauSFs(self.year,self.ULtag,self.preVFP)
            self.triggerSFs = TriggerSFs(self.year,self.preVFP)
            self.tauES = TauES(self.year,self.preVFP)
            if self.year==2018:
                LUMI = 59740
            elif self.year==2017:
                LUMI = 41530
            elif self.year==2016:
                if self.preVFP=="_preVFP":
                    LUMI = 19500
                else:
                    LUMI = 16800

            JSON_path = '/work/pbaertsc/bbh/NanoTreeProducer/json/UL%s%s/'%(self.year,self.preVFP)
            xsec = xsection[self.sample_name]['xsec']
            
            if "gghplusbb" in self.sample_name and self.year==2018:
                nevents = utils.getJSON(JSON_path,"gghplusbb",self.year,self.ULtag,self.preVFP)+utils.getJSON(JSON_path,"gghplusbb_ext",self.year,self.ULtag,self.preVFP)
            elif "ggfhplusbb" in self.sample_name and self.year==2018:
                nevents = utils.getJSON(JSON_path,"ggfhplusbb",self.year,self.ULtag,self.preVFP)+utils.getJSON(JSON_path,"ggfhplusbb_ext",self.year,self.ULtag,self.preVFP)
            else:
                nevents = utils.getJSON(JSON_path,self.sample_name,self.year,self.ULtag,self.preVFP)
            self.LumiWeight = LUMI * xsec / nevents
        
    
   
    def beginJob(self):
        pass

    def endJob(self):
        if not self.isData:
            self.btagTool.setDirectory(self.out.outputfile,'btag')
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
        self.out.GeneratorWeight[0]         = self.GeneratorWeight
        self.out.BTagWeight[0]              = self.BTagWeight
        self.out.BTagWeightCorr[0]          = self.BTagWeightCorr
        self.out.BTagWeight_nocorr[0]       = self.BTagWeight_nocorr
        self.out.BTagWeight_comb[0]         = self.BTagWeight_comb
        self.out.BTagWeight_combUp[0]      = self.BTagWeight_combUp
        self.out.BTagWeight_combDown[0]    = self.BTagWeight_combDown
        self.out.BTagWeight_jesUp[0]       = self.BTagWeight_jesUp 
        self.out.BTagWeight_jesDown[0]     = self.BTagWeight_jesDown  
        self.out.BTagWeight_lfUp[0]        = self.BTagWeight_lfUp 
        self.out.BTagWeight_lfDown[0]      = self.BTagWeight_lfDown  
        self.out.BTagWeight_hfUp[0]        = self.BTagWeight_hfUp
        self.out.BTagWeight_hfDown[0]      = self.BTagWeight_hfDown 
        self.out.BTagWeight_hfstats1Up[0]  = self.BTagWeight_hfstats1Up 
        self.out.BTagWeight_hfstats1Down[0]= self.BTagWeight_hfstats1Down
        self.out.BTagWeight_hfstats2Up[0]  = self.BTagWeight_hfstats2Up
        self.out.BTagWeight_hfstats2Down[0]= self.BTagWeight_hfstats2Down
        self.out.BTagWeight_lfstats1Up[0]  = self.BTagWeight_lfstats1Up 
        self.out.BTagWeight_lfstats1Down[0]= self.BTagWeight_lfstats1Down  
        self.out.BTagWeight_lfstats2Up[0]  = self.BTagWeight_lfstats2Up 
        self.out.BTagWeight_lfstats2Down[0]= self.BTagWeight_lfstats2Down
        self.out.BTagWeight_cferr1Up[0]    = self.BTagWeight_cferr1Up 
        self.out.BTagWeight_cferr1Down[0]  = self.BTagWeight_cferr1Down  
        self.out.BTagWeight_cferr2Up[0]    = self.BTagWeight_cferr2Up  
        self.out.BTagWeight_cferr2Down[0]  = self.BTagWeight_cferr2Down
        self.out.GenWeight[0]               = self.GenWeight
        self.out.PUWeight[0]                = self.PUWeight
        self.out.PUWeight_up[0]             = self.PUWeight_up
        self.out.PUWeight_down[0]           = self.PUWeight_down
        self.out.PUWeight_old[0]            = self.PUWeight_old
        self.out.MuWeight[0]                = self.MuWeight
        self.out.MuWeight_up[0]             = self.MuWeight_up
        self.out.MuWeight_down[0]           = self.MuWeight_down
        self.out.MuTriggerWeight[0]         = self.MuTriggerWeight
        self.out.MuTriggerWeight_gen[0]     = self.MuTriggerWeight_gen
        self.out.MuTriggerWeight_up[0]      = self.MuTriggerWeight_up
        self.out.MuTriggerWeight_down[0]    = self.MuTriggerWeight_down
        self.out.MuTriggerWeight_old[0]     = self.MuTriggerWeight_old
        self.out.MuTriggerWeight_sl[0]      = self.MuTriggerWeight_sl
        self.out.MuTriggerWeight_cross[0]   = self.MuTriggerWeight_cross
        self.out.MuTriggerWeight_crossold[0]   = self.MuTriggerWeight_crossold
        self.out.MuTriggerWeight_lepcross[0] = self.MuTriggerWeight_lepcross
        self.out.MuTriggerWeight_taucross[0] = self.MuTriggerWeight_taucross
        self.out.EWeight[0]                 = self.EWeight
        self.out.EWeight_up[0]              = self.EWeight_up
        self.out.EWeight_down[0]            = self.EWeight_down
        self.out.ETriggerWeight[0]          = self.ETriggerWeight
        self.out.ETriggerWeight_gen[0]      = self.ETriggerWeight_gen
        self.out.ETriggerWeight_up[0]       = self.ETriggerWeight_up
        self.out.ETriggerWeight_down[0]     = self.ETriggerWeight_down
        self.out.ETriggerWeight_old[0]      = self.ETriggerWeight_old
        self.out.ETriggerWeight_sl[0]       = self.ETriggerWeight_sl
        self.out.ETriggerWeight_cross[0]    = self.ETriggerWeight_cross
        self.out.ETriggerWeight_crossold[0]    = self.ETriggerWeight_crossold
        self.out.TauWeight[0]               = self.TauWeight
        self.out.TauWeight_up[0]            = self.TauWeight_up
        self.out.TauWeight_down[0]          = self.TauWeight_down
        self.out.TauWeightVSjet[0]          = self.TauWeightVSjet
        self.out.TauWeightVSjet_up[0]       = self.TauWeightVSjet_up
        self.out.TauWeightVSjet_down[0]     = self.TauWeightVSjet_down
        self.out.TauWeightVSmu[0]           = self.TauWeightVSmu
        self.out.TauWeightVSmu_up[0]        = self.TauWeightVSmu_up
        self.out.TauWeightVSmu_down[0]      = self.TauWeightVSmu_down
        self.out.TauWeightVSe[0]            = self.TauWeightVSe
        self.out.TauWeightVSe_up[0]         = self.TauWeightVSe_up
        self.out.TauWeightVSe_down[0]       = self.TauWeightVSe_down
        self.out.PrefireWeight[0]           = self.PrefireWeight
        self.out.PrefireWeight_up[0]        = self.PrefireWeight_up
        self.out.PrefireWeight_down[0]      = self.PrefireWeight_down
        self.out.TauEmbedding_TriggerWeight[0] = self.TauEmbedding_TriggerWeight
        self.out.TauEmbedding_IdWeight[0]      = self.TauEmbedding_IdWeight
        self.out.isHtoMuTau[0]              = self.isHtoMuTau
        self.out.isHtoETau[0]               = self.isHtoETau
        self.out.isHtoTauTau[0]             = self.isHtoTauTau
        self.out.isHtoMuTauAR[0]            = self.isHtoMuTauAR
        self.out.isHtoETauAR[0]             = self.isHtoETauAR
        self.out.isHtoTauTauAR[0]           = self.isHtoTauTauAR
        self.out.isHtolooseMuTau[0]         = self.isHtolooseMuTau
        self.out.isHtolooseMuTauAR[0]       = self.isHtolooseMuTauAR
        self.out.isHtolooseETau[0]          = self.isHtolooseETau
        self.out.isHtolooseETauAR[0]        = self.isHtolooseETauAR
        self.out.isTTCR[0]                  = self.isTTCR
        self.out.isMuMu[0]                  = self.isMuMu
        self.out.dimuon_veto                = self.dimuon_veto
        self.out.dielectron_veto            = self.dielectron_veto
        self.out.muon_veto                  = self.muon_veto
        self.out.electron_veto              = self.electron_veto
        self.out.nPV[0]                     = event.PV_npvsGood
        self.out.nTaus[0]                   = self.nTaus
        self.out.nElectrons[0]              = self.nElectrons
        self.out.nMuons[0]                  = self.nMuons
        self.out.nJets[0]                   = self.nJets
        self.out.nJets_forward[0]           = self.nJets_forward
        self.out.nGenBjets[0]               = self.nGenBjets
        self.out.LHE_Nb[0]                  = self.LHE_Nb
        self.out.LHE_Nc[0]                  = self.LHE_Nc
        self.out.LHE_Njets[0]               = self.LHE_Njets
        self.out.LHE_NpLO[0]                = self.LHE_NpLO
        self.out.LHE_NpNLO[0]               = self.LHE_NpNLO
        self.out.LHEPdfWeight[0]            = self.LHEPdfWeight
        self.out.LHE_Vpt[0]                 = self.LHE_Vpt
        self.out.nBjets_l[0]                = self.nBjets_l
        self.out.nBjets_m[0]                = self.nBjets_m
        self.out.nBjets_t[0]                = self.nBjets_t
        self.out.nBjets_l_excl[0]           = self.nBjets_l_excl
        self.out.nBjets_m_excl[0]           = self.nBjets_m_excl
        self.out.nJets_tcut[0]              = self.nJets_tcut
        self.out.nBjets_l_tcut[0]           = self.nBjets_l_tcut
        self.out.nBjets_m_tcut[0]           = self.nBjets_m_tcut
        self.out.nBjets_t_tcut[0]           = self.nBjets_t_tcut
        self.out.Jet1_pt[0]                 = self.Jet1_pt
        self.out.Jet1_eta[0]                = self.Jet1_eta
        self.out.Jet1_phi[0]                = self.Jet1_phi
        self.out.Jet1_mass[0]               = self.Jet1_mass
        self.out.Jet1_btag[0]               = self.Jet1_btag
        self.out.Jet1_hadronFlavour[0]      = self.Jet1_hadronFlavour
        self.out.Jet2_pt[0]                 = self.Jet2_pt
        self.out.Jet2_eta[0]                = self.Jet2_eta
        self.out.Jet2_phi[0]                = self.Jet2_phi
        self.out.Jet2_mass[0]               = self.Jet2_mass
        self.out.Jet2_btag[0]               = self.Jet2_btag
        self.out.Jet2_hadronFlavour[0]      = self.Jet2_hadronFlavour
        self.out.Jet3_pt[0]                 = self.Jet3_pt
        self.out.Jet3_eta[0]                = self.Jet3_eta
        self.out.Jet3_phi[0]                = self.Jet3_phi
        self.out.Jet3_mass[0]               = self.Jet3_mass
        self.out.Jet3_btag[0]               = self.Jet3_btag
        self.out.Jet3_hadronFlavour[0]      = self.Jet3_hadronFlavour
        self.out.Bjet1_pt[0]                = self.Bjet1_pt
        self.out.Bjet1_eta[0]               = self.Bjet1_eta
        self.out.Bjet1_phi[0]               = self.Bjet1_phi
        self.out.Bjet1_mass[0]              = self.Bjet1_mass
        self.out.Bjet2_pt[0]                = self.Bjet2_pt
        self.out.Bjet2_eta[0]               = self.Bjet2_eta
        self.out.Bjet2_phi[0]               = self.Bjet2_phi
        self.out.Bjet2_mass[0]              = self.Bjet2_mass
        self.out.Mu1_pt[0]                  = self.Mu1_pt
        self.out.Mu1_eta[0]                 = self.Mu1_eta
        self.out.Mu1_phi[0]                 = self.Mu1_phi
        self.out.Mu1_mass[0]                = self.Mu1_mass
        self.out.Mu1_charge[0]              = self.Mu1_charge
        self.out.Mu1_iso[0]                 = self.Mu1_iso
        self.out.Mu1_genmatch[0]            = self.Mu1_genmatch
        self.out.Mu1_sltrig_fired[0]        = self.Mu1_sltrig_fired
        self.out.Mu1_ctrig_fired[0]         = self.Mu1_ctrig_fired
        self.out.Mu1_ctrig_HPS_fired[0]     = self.Mu1_ctrig_HPS_fired
        self.out.Mu1_ctrig_noHPS_fired[0]   = self.Mu1_ctrig_noHPS_fired
        self.out.Mu2_pt[0]                  = self.Mu2_pt
        self.out.Mu2_eta[0]                 = self.Mu2_eta
        self.out.Mu2_phi[0]                 = self.Mu2_phi
        self.out.Mu2_mass[0]                = self.Mu2_mass
        self.out.Mu2_charge[0]              = self.Mu2_charge
        self.out.Mu2_iso[0]                 = self.Mu2_iso
        self.out.Mu2_genmatch[0]            = self.Mu2_genmatch
        self.out.Ele1_pt[0]                 = self.Ele1_pt
        self.out.Ele1_eta[0]                = self.Ele1_eta
        self.out.Ele1_phi[0]                = self.Ele1_phi
        self.out.Ele1_mass[0]               = self.Ele1_mass
        self.out.Ele1_charge[0]             = self.Ele1_charge
        self.out.Ele1_iso[0]                = self.Ele1_iso
        self.out.Ele1_genmatch[0]           = self.Ele1_genmatch
        self.out.Ele1_sltrig_fired[0]       = self.Ele1_sltrig_fired
        self.out.Ele1_ctrig_fired[0]        = self.Ele1_ctrig_fired
        self.out.Ele1_ctrig_HPS_fired[0]    = self.Ele1_ctrig_HPS_fired
        self.out.Ele1_ctrig_noHPS_fired[0]  = self.Ele1_ctrig_noHPS_fired
        self.out.Tau1_pt[0]                 = self.Tau1_pt
        self.out.Tau1_eta[0]                = self.Tau1_eta
        self.out.Tau1_phi[0]                = self.Tau1_phi
        self.out.Tau1_mass[0]               = self.Tau1_mass
        self.out.Tau1_charge[0]             = self.Tau1_charge
        self.out.Tau1_iso[0]                = self.Tau1_iso
        self.out.Tau1_decaymode[0]          = self.Tau1_decaymode
        self.out.Tau1_genmatch[0]           = self.Tau1_genmatch
        self.out.Tau1_Idvsjet[0]            = self.Tau1_Idvsjet
        self.out.Tau1_Idvse[0]              = self.Tau1_Idvse
        self.out.Tau1_Idvsmu[0]             = self.Tau1_Idvsmu
        self.out.Tau1_ES[0]                 = self.Tau1_ES
        self.out.Tau1_ctrig_fired[0]        = self.Tau1_ctrig_fired
        self.out.Tau1_ctrig_HPS_fired[0]    = self.Tau1_ctrig_HPS_fired
        self.out.Tau1_ctrig_noHPS_fired[0]  = self.Tau1_ctrig_noHPS_fired
        self.out.H_pt[0]                    = self.H_pt
        self.out.H_eta[0]                   = self.H_eta
        self.out.H_phi[0]                   = self.H_phi
        self.out.H_mass[0]                  = self.H_mass
        self.out.vis_pt[0]                  = self.vis_pt
        self.out.vis_eta[0]                 = self.vis_eta
        self.out.vis_phi[0]                 = self.vis_phi
        self.out.vis_mass[0]                = self.vis_mass
        self.out.mt2[0]                     = self.mt2
        self.out.MET[0]                     = self.MET
        self.out.MET_phi[0]                 = self.MET_phi
        self.out.MET_chs[0]                 = self.MET_chs
        self.out.MET_chs_phi[0]             = self.MET_chs_phi
        self.out.vistau1_pt[0]              = self.vistau1_pt
        self.out.vistau1_eta[0]             = self.vistau1_eta
        self.out.vistau1_phi[0]             = self.vistau1_phi
        self.out.vistau1_mass[0]            = self.vistau1_mass
        self.out.vistau1_energy[0]          = self.vistau1_energy
        self.out.vistau2_pt[0]              = self.vistau2_pt
        self.out.vistau2_eta[0]             = self.vistau2_eta
        self.out.vistau2_phi[0]             = self.vistau2_phi
        self.out.vistau2_mass[0]            = self.vistau2_mass
        self.out.vistau2_energy[0]          = self.vistau2_energy
        self.out.transverse_mass_lepmet[0]   = self.transverse_mass_lepmet
        self.out.transverse_mass_taumet[0]  = self.transverse_mass_taumet
        self.out.transverse_mass_leptau[0]   = self.transverse_mass_leptau
        self.out.transverse_mass_total[0]   = self.transverse_mass_total
        self.out.H_mass_gen[0]              = self.H_mass_gen
        self.out.collinear_mass[0]          = self.collinear_mass
        self.out.collinear_mass_chs[0]      = self.collinear_mass_chs
        self.out.DRBjets[0]                 = self.DRBjets
        self.out.DRBjets_lm[0]              = self.DRBjets_lm
        self.out.DRBjets_mt[0]              = self.DRBjets_mt
        self.out.DEta_Bjets[0]              = self.DEta_Bjets
        self.out.DPhi_Bjets[0]              = self.DPhi_Bjets
        self.out.Bjets_pt[0]                = self.Bjets_pt
        self.out.wt_ff[0]                   = self.wt_ff
        self.out.wt_ff_nocorr[0]            = self.wt_ff_nocorr
        self.out.wt_ff_nocorr_up[0]         = self.wt_ff_nocorr_up
        self.out.wt_ff_nocorr_down[0]       = self.wt_ff_nocorr_down
        self.out.wt_ff_norm[0]              = self.wt_ff_norm
        self.out.wt_ff_ttdr[0]              = self.wt_ff_ttdr
        self.out.wt_ff_qcddr[0]             = self.wt_ff_qcddr
        self.out.wt_ff_qcd[0]               = self.wt_ff_qcd
        self.out.wt_ff_w[0]                 = self.wt_ff_w
        self.out.wt_ff_tt[0]                = self.wt_ff_tt
        self.out.wt_ff_qcd_old[0]           = self.wt_ff_qcd_old
        self.out.wt_ff_w_old[0]             = self.wt_ff_w_old
        self.out.wt_ff_tt_old[0]            = self.wt_ff_tt_old
        self.out.wt_ffcorr_hmass_qcd[0]     = self.wt_ffcorr_hmass_qcd
        self.out.wt_ffcorr_jetpt_qcd[0]     = self.wt_ffcorr_jetpt_qcd
        self.out.wt_ffcorr_collinearmass_qcd[0]= self.wt_ffcorr_collinearmass_qcd
        self.out.wt_ffcorr_taujmass_qcd[0]  = self.wt_ffcorr_taujmass_qcd
        self.out.wt_ffUp[0]                 = self.wt_ffUp
        self.out.wt_ffDown[0]               = self.wt_ffDown
        self.out.wt_ff_qcdUp[0]             = self.wt_ff_qcdUp
        self.out.wt_ff_qcdDown[0]           = self.wt_ff_qcdDown
        self.out.wt_ff_wUp[0]               = self.wt_ff_wUp
        self.out.wt_ff_wDown[0]             = self.wt_ff_wDown
        self.out.wt_ff_ttUp[0]              = self.wt_ff_ttUp
        self.out.wt_ff_ttDown[0]            = self.wt_ff_ttDown
        self.out.wt_ff_qcdfitpar1Up[0]      = self.wt_ff_qcdfitpar1Up   
        self.out.wt_ff_qcdfitpar1Down[0]    = self.wt_ff_qcdfitpar1Down 
        self.out.wt_ff_qcdfitpar2Up[0]      = self.wt_ff_qcdfitpar2Up 
        self.out.wt_ff_qcdfitpar2Down[0]    = self.wt_ff_qcdfitpar2Down
        self.out.wt_ff_wfitpar1Up[0]        = self.wt_ff_wfitpar1Up   
        self.out.wt_ff_wfitpar1Down[0]      = self.wt_ff_wfitpar1Down
        self.out.wt_ff_wfitpar2Up[0]        = self.wt_ff_wfitpar2Up  
        self.out.wt_ff_wfitpar2Down[0]      = self.wt_ff_wfitpar2Down 
        self.out.wt_ff_wfitpar3Up[0]        = self.wt_ff_wfitpar3Up
        self.out.wt_ff_wfitpar3Down[0]      = self.wt_ff_wfitpar3Down
        self.out.wt_ff_wfitpar4Up[0]        = self.wt_ff_wfitpar4Up
        self.out.wt_ff_wfitpar4Down[0]      = self.wt_ff_wfitpar4Down
        self.out.wt_ff_ttfitpar1Up[0]       = self.wt_ff_ttfitpar1Up 
        self.out.wt_ff_ttfitpar1Down[0]     = self.wt_ff_ttfitpar1Down 
        self.out.wt_ff_ttfitpar2Up[0]       = self.wt_ff_ttfitpar2Up
        self.out.wt_ff_ttfitpar2Down[0]     = self.wt_ff_ttfitpar2Down
        self.out.wt_dy[0]                   = self.wt_dy
        self.out.wt_dy_old[0]               = self.wt_dy_old
        self.out.wt_dy_reco[0]              = self.wt_dy_reco
        self.out.wt_dy_nlo[0]               = self.wt_dy_nlo
        self.out.wt_w_nlo[0]                = self.wt_w_nlo
        self.out.wt_tt[0]                   = self.wt_tt
        self.out.wt_tt_pol1[0]              = self.wt_tt_pol1
        self.out.wt_tt_pol2[0]              = self.wt_tt_pol2
        self.out.wt_w[0]                    = self.wt_w
        self.out.ffunc_qcd[0]               = self.ffunc_qcd
        self.out.ffunc_w[0]                 = self.ffunc_w
        self.out.ffunc_tt[0]                = self.ffunc_tt
        self.out.ff_fitunc_qcd_par1[0]      = self.ff_fitunc_qcd_par1
        self.out.ff_fitunc_qcd_par2[0]      = self.ff_fitunc_qcd_par2
        self.out.ff_fitunc_w_par1[0]        = self.ff_fitunc_w_par1
        self.out.ff_fitunc_w_par2[0]        = self.ff_fitunc_w_par2
        self.out.ff_fitunc_w_par3[0]        = self.ff_fitunc_w_par3
        self.out.ff_fitunc_w_par4[0]        = self.ff_fitunc_w_par4
        self.out.ff_fitunc_tt_par1[0]       = self.ff_fitunc_tt_par1
        self.out.ff_fitunc_tt_par2[0]       = self.ff_fitunc_tt_par2
        self.out.Dzeta[0]                   = self.Dzeta
        self.out.DPhi[0]                    = self.DPhi
        self.out.DEta[0]                    = self.DEta
        self.out.DEta_jets_forward[0]       = self.DEta_jets_forward
        self.out.DPhiLepMET[0]              = self.DPhiLepMET
        self.out.DRLepMET[0]                = self.DRLepMET
        self.out.dijet_pt[0]                = self.dijet_pt
        self.out.dijet_eta[0]               = self.dijet_eta
        self.out.dijet_phi[0]               = self.dijet_phi
        self.out.dijet_mass[0]              = self.dijet_mass
        self.out.DRjets[0]                  = self.DRjets
        self.out.DEta_jets[0]               = self.DEta_jets
        self.out.DPhi_jets[0]               = self.DPhi_jets
        self.out.vistauMET_pt[0]            = self.vistauMET_pt
        self.out.LepJ_mass[0]               = self.LepJ_mass
        self.out.TauJ_mass[0]               = self.TauJ_mass
        self.out.Taudijet_mass[0]           = self.Taudijet_mass
        self.out.vistauJ_mass[0]            = self.vistauJ_mass
        self.out.vistauJMET_mass[0]         = self.vistauJMET_mass
        self.out.TauJMET_mass[0]            = self.TauJMET_mass
        self.out.LepJMET_mass[0]            = self.LepJMET_mass
        self.out.METJ_mass[0]               = self.METJ_mass
        self.out.LepJ_pt[0]                 = self.LepJ_pt
        self.out.TauJ_pt[0]                 = self.TauJ_pt
        self.out.vistauJ_pt[0]              = self.vistauJ_pt
        self.out.vistauJMET_pt[0]           = self.vistauJMET_pt 
        self.out.TauJMET_pt[0]              = self.TauJMET_pt
        self.out.LepJMET_pt[0]              = self.LepJMET_pt 
        self.out.METJ_pt[0]                 = self.METJ_pt 
        self.out.DRTauJ[0]                  = self.DRTauJ 
        self.out.DEtaTauJ[0]                = self.DEtaTauJ 
        self.out.DPhiTauJ[0]                = self.DPhiTauJ 
        self.out.DRLepJ[0]                  = self.DRLepJ 
        self.out.DEtaLepJ[0]                = self.DEtaLepJ
        self.out.DPhiLepJ[0]                = self.DPhiLepJ 
        self.out.DRTauJ2[0]                 = self.DRTauJ2  
        self.out.DEtaTauJ2[0]               = self.DEtaTauJ2 
        self.out.DPhiTauJ2[0]               = self.DPhiTauJ2 
        self.out.DRLepJ2[0]                 = self.DRLepJ2 
        self.out.DEtaLepJ2[0]               = self.DEtaLepJ2 
        self.out.DPhiLepJ2[0]               = self.DPhiLepJ2
        self.out.HJ_mass[0]                 = self.HJ_mass
        self.out.HJ_pt[0]                   = self.HJ_pt 
        self.out.DRHJ[0]                    = self.DRHJ 
        self.out.DEtaHJ[0]                  = self.DEtaHJ 
        self.out.DPhiHJ[0]                  = self.DPhiHJ 
        self.out.HJ2_mass[0]                = self.HJ2_mass
        self.out.HJ2_pt[0]                  = self.HJ2_pt
        self.out.DRHJ2[0]                   = self.DRHJ2
        self.out.DEtaHJ2[0]                 = self.DEtaHJ2
        self.out.DPhiHJ2[0]                 = self.DPhiHJ2
        self.out.TTCR_Mufired[0]            = self.TTCR_Mufired
        self.out.TTCR_Efired[0]             = self.TTCR_Efired
        self.out.HPStrigger[0]              = self.HPStrigger
        self.out.HPStrigger_error[0]        = self.HPStrigger_error
        self.out.MuTrigger_fired[0]         = self.MuTrigger_fired
        self.out.MuTauTrigger_fired[0]      = self.MuTauTrigger_fired
        self.out.MuTauTrigger_HPS_fired[0]  = self.MuTauTrigger_HPS_fired
        self.out.MuTauTrigger_noHPS_fired[0]= self.MuTauTrigger_noHPS_fired
        self.out.ETrigger_fired[0]          = self.ETrigger_fired
        self.out.ETauTrigger_fired[0]       = self.ETauTrigger_fired
        self.out.ETauTrigger_HPS_fired[0]   = self.ETauTrigger_HPS_fired
        self.out.ETauTrigger_noHPS_fired[0] = self.ETauTrigger_noHPS_fired
        self.out.METTrigger_fired[0]        = self.METTrigger_fired
        self.out.MuTriggermatch[0]          = self.MuTriggermatch
        self.out.ETriggermatch[0]           = self.ETriggermatch
        
        self.out.tree.Fill()

    def vec(self,lepton):
        lepton_v = TVector3()
        lepton_v.SetPtEtaPhi(lepton.pt,lepton.eta,lepton.phi)
        return lepton_v

    def tlv(self,lepton):
        lepton_tlv = TLorentzVector()
        lepton_tlv.SetPtEtaPhiM(lepton.pt,lepton.eta,lepton.phi,lepton.mass)
        return lepton_tlv

    #def tlv_jet(self,jet_list,row):
    #    jet_tlv = TLorentzVector()
    #    jet_tlv.SetPtEtaPhiM(jet_list[row][1],jet_list[row][0].eta,jet_list[row][0].phi,jet_list[row][2])
    #    return jet_tlv
    

    #def jet_vars(self,jet_list,row):
    #    return [jet_list[row][1],jet_list[row][0].eta,jet_list[row][0].phi,jet_list[row][2],jet_list[row][0].btagDeepFlavB]

    def mass_t(self,par1vec,par2vec):
        return np.sqrt(2*par1vec.Pt()*par2vec.Pt()*(1-np.cos(par1vec.DeltaPhi(par2vec)))) 
    
    #def iso(self, lepton):
    #    if hasattr(lepton,'pfRelIso04_all'):
    #        return lepton.pfRelIso04_all
    #    elif hasattr(lepton,'rawDeepTau2017v2p1VSjet'):
    #        return lepton.rawDeepTau2017v2p1VSjet
    #    elif hasattr(lepton,'pfRelIso03_all'):
    #        return lepton.pfRelIso03_all
    #    else:
    #        print("ERROR: No isolation found")
    
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
            
    
    #def isocheck(self,lepton,checkvalue):
    #    self.moreiso = False
    #    if hasattr(lepton,'pfRelIso04_all'):
    #        if lepton.pfRelIso04_all < checkvalue:          #muon more isolated -> smaller value
    #            self.moreiso = True
    #    elif hasattr(lepton,'pfRelIso03_all'):
    #        if lepton.pfRelIso03_all < checkvalue:          #electron more isolated -> smaller value
    #            self.moreiso = True
    #    elif hasattr(lepton,'rawDeepTau2017v2p1VSjet'):
    #        if lepton.rawDeepTau2017v2p1VSjet > checkvalue: #tau more isolated -> larger value
    #            self.moreiso = True
    #    else:
    #        print("ERROR: No isolation found")
    #    return self.moreiso
    

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
        self.nElectrons            = 0
        self.nMuons                = 0
        self.nTaus                 = 0
        self.nJets                 = 0
        self.nJets_forward         = 0
        self.nGenBjets             = 0
        self.nBjets_l              = 0
        self.nBjets_m              = 0
        self.nBjets_t              = 0
        self.nBjets_l_excl         = 0
        self.nBjets_m_excl         = 0
        self.nJets_tcut            = 0
        self.nBjets_l_tcut         = 0
        self.nBjets_m_tcut         = 0
        self.nBjets_t_tcut         = 0
        self.LHE_Nb                = 0
        self.LHE_Nc                = 0
        self.LHE_Njets             = 0
        self.LHE_NpLO              = 0
        self.LHE_NpNLO             = 0
        self.LHE_Vpt               =-1.
        self.LHEPdfWeight          = 1.
        self.EventWeight           = 1.
        self.BTagWeight            = 1.
        self.BTagWeightCorr        = 1.
        self.BTagWeight_nocorr     = 1.
        self.BTagWeightUp          = 1.
        self.BTagWeightDown        = 1.
        self.BTagWeight_comb       = 1.
        self.BTagWeight_combUp     = 1.
        self.BTagWeight_combDown   = 1.
        self.BTagWeight_jesUp      = 1.
        self.BTagWeight_jesDown    = 1. 
        self.BTagWeight_lfUp       = 1. 
        self.BTagWeight_lfDown     = 1.
        self.BTagWeight_hfUp       = 1.
        self.BTagWeight_hfDown     = 1.
        self.BTagWeight_hfstats1Up    = 1.
        self.BTagWeight_hfstats1Down  = 1.
        self.BTagWeight_hfstats2Up    = 1.
        self.BTagWeight_hfstats2Down  = 1.
        self.BTagWeight_lfstats1Up    = 1.
        self.BTagWeight_lfstats1Down  = 1.
        self.BTagWeight_lfstats2Up    = 1.
        self.BTagWeight_lfstats2Down  = 1.
        self.BTagWeight_cferr1Up      = 1.
        self.BTagWeight_cferr1Down    = 1.
        self.BTagWeight_cferr2Up      = 1.
        self.BTagWeight_cferr2Down    = 1.
        self.GenWeight             = 1.
        self.PUWeight              = 1.
        self.PUWeight_up           = 1.
        self.PUWeight_down         = 1.
        self.PUWeight_old          = 1.
        self.GeneratorWeight       = 1.
        self.MuWeight              = 1.
        self.MuWeight_up           = 1.
        self.MuWeight_down         = 1.
        self.MuTriggerWeight       = 1.
        self.MuTriggerWeight_gen   = 1.
        self.MuTriggerWeight_up    = 1.
        self.MuTriggerWeight_down  = 1.
        self.MuTriggerWeight_old   = 1.
        self.MuTriggerWeight_sl    = 1.
        self.MuTriggerWeight_cross = 1.
        self.MuTriggerWeight_crossold = 1.
        self.MuTriggerWeight_lepcross = 1.
        self.MuTriggerWeight_taucross = 1.
        self.EWeight               = 1.
        self.EWeight_up            = 1.
        self.EWeight_down          = 1.
        self.ETriggerWeight        = 1.
        self.ETriggerWeight_gen    = 1.
        self.ETriggerWeight_up     = 1.
        self.ETriggerWeight_down   = 1.
        self.ETriggerWeight_old    = 1.
        self.ETriggerWeight_sl     = 1.
        self.ETriggerWeight_cross  = 1.
        self.ETriggerWeight_crossold  = 1.
        self.TauWeight             = 1.
        self.TauWeight_up          = 1.
        self.TauWeight_down        = 1.
        self.TauWeightVSjet        = 1.
        self.TauWeightVSjet_up     = 1.
        self.TauWeightVSjet_down   = 1.
        self.TauWeightVSmu         = 1.
        self.TauWeightVSmu_up      = 1.
        self.TauWeightVSmu_down    = 1.
        self.TauWeightVSe          = 1.
        self.TauWeightVSe_up       = 1.
        self.TauWeightVSe_down     = 1.
        self.PrefireWeight         = 1.
        self.PrefireWeight_up      = 1.
        self.PrefireWeight_down    = 1.
        self.TauEmbedding_TriggerWeight = 1.
        self.TauEmbedding_IdWeight    = 1.
        self.isHtoMuTau            = False
        self.isHtoETau             = False
        self.isHtoTauTau           = False
        self.isHtoMuTauAR          = False
        self.isHtoETauAR           = False
        self.isHtoTauTauAR         = False
        self.isHtolooseMuTau       = False
        self.isHtolooseMuTauAR     = False
        self.isHtolooseETau        = False
        self.isHtolooseETauAR      = False
        self.isTTCR                = False
        self.isMuMu                = False
        self.is2016                = False
        self.is2017                = False
        self.is2018                = False
        self.dimuon_veto           = False
        self.dielectron_veto       = False
        self.muon_veto             = False
        self.electron_veto         = False
        self.Mu1_pt                = -1.
        self.Mu1_eta               = -10.
        self.Mu1_phi               = -10.
        self.Mu1_mass              = -1.
        self.Mu1_charge            = -1.
        self.Mu1_iso               = -1.
        self.Mu1_genmatch          = -1.
        self.Mu1_sltrig_fired      = False
        self.Mu1_ctrig_fired       = False
        self.Mu1_ctrig_HPS_fired   = False
        self.Mu1_ctrig_noHPS_fired = False
        self.Mu2_pt                = -1.
        self.Mu2_eta               = -10.
        self.Mu2_phi               = -10.
        self.Mu2_mass              = -1.
        self.Mu2_charge            = -1.
        self.Mu2_iso               = -1.
        self.Mu2_genmatch          = -1.
        self.Ele1_pt               = -1.
        self.Ele1_eta              = -10.
        self.Ele1_phi              = -10.
        self.Ele1_mass             = -1.
        self.Ele1_charge           = -1.
        self.Ele1_iso              = -1.
        self.Ele1_genmatch         = -1.
        self.Ele1_sltrig_fired     = False
        self.Ele1_ctrig_fired      = False
        self.Ele1_ctrig_HPS_fired  = False
        self.Ele1_ctrig_noHPS_fired= False
        self.Jet1_pt               = -1.
        self.Jet1_eta              = -10.
        self.Jet1_phi              = -10.
        self.Jet1_mass             = -1.
        self.Jet1_btag             = -1.
        self.Jet1_hadronFlavour    = -1.
        self.Jet2_pt               = -1.
        self.Jet2_eta              = -10.
        self.Jet2_phi              = -10.
        self.Jet2_mass             = -1.
        self.Jet2_btag             = -1.
        self.Jet2_hadronFlavour    = -1.
        self.Jet3_pt               = -1.
        self.Jet3_eta              = -10.
        self.Jet3_phi              = -10.
        self.Jet3_mass             = -1.
        self.Jet3_btag             = -1.
        self.Jet3_hadronFlavour    = -1.
        self.Bjet1_pt              = -1.
        self.Bjet1_eta             = -10.
        self.Bjet1_phi             = -10.
        self.Bjet1_mass            = -1.
        self.Bjet2_pt              = -1.
        self.Bjet2_eta             = -10.
        self.Bjet2_phi             = -10.
        self.Bjet2_mass            = -1.
        self.Tau1_pt               = -1.
        self.Tau1_eta              = -10.
        self.Tau1_phi              = -10.
        self.Tau1_mass             = -1.
        self.Tau1_charge           = -1.
        self.Tau1_iso              = -1.
        self.Tau1_decaymode        = -1.
        self.Tau1_genmatch         = -1.
        self.Tau1_Idvsjet          = -1.
        self.Tau1_Idvse            = -1.
        self.Tau1_Idvsmu           = -1.
        self.Tau1_ES               = -1.
        self.Tau1_ctrig_fired      = False
        self.Tau1_ctrig_HPS_fired  = False
        self.Tau1_ctrig_noHPS_fired = False
        self.H_pt                  = -1.
        self.H_eta                 = -10.
        self.H_phi                 = -10.
        self.H_mass                = -1.
        self.mt2                   = -1.
        self.vis_pt                = -1.
        self.vis_eta               = -10.
        self.vis_phi               = -10.
        self.vis_mass              = -1.
        self.vistau1_pt            = -1.
        self.vistau1_eta           = -10.
        self.vistau1_phi           = -10.
        self.vistau1_mass          = -1.
        self.vistau1_energy        = -1.
        self.vistau2_pt            = -1.
        self.vistau2_eta           = -10.
        self.vistau2_phi           = -10.
        self.vistau2_mass          = -1.
        self.vistau2_energy        = -1.
        self.transverse_mass_lepmet = -1.
        self.transverse_mass_taumet = -1.
        self.transverse_mass_leptau = -1.
        self.transverse_mass_total = -1.
        self.H_mass_gen            = -1.
        self.collinear_mass        = -1.
        self.collinear_mass_chs    = -1.
        self.MET                   = -1.
        self.MET_phi               = -1.
        self.MET_chs               = -1.
        self.MET_chs_phi           = -1.
        self.wt_ff                 = 0.
        self.wt_ff_nocorr          = 0.
        self.wt_ff_nocorr_up       = 0.
        self.wt_ff_nocorr_down     = 0.
        self.wt_ff_norm            = 0.
        self.wt_ff_ttdr            = 0.
        self.wt_ff_qcddr           = 0.
        self.wt_ff_qcd             = 0.
        self.wt_ff_w               = 0.
        self.wt_ff_tt              = 0.
        self.wt_ff_qcd_old         = 0.
        self.wt_ff_w_old           = 0.
        self.wt_ff_tt_old          = 0.
        self.wt_ffcorr_hmass_qcd   = 1.
        self.wt_ffcorr_jetpt_qcd   = 1.
        self.wt_ffcorr_collinearmass_qcd= 1.
        self.wt_ffcorr_taujmass_qcd= 1.
        self.wt_ffUp               = 0.
        self.wt_ffDown             = 0.
        self.wt_ff_qcdUp           = 0.
        self.wt_ff_qcdDown         = 0.
        self.wt_ff_wUp             = 0.
        self.wt_ff_wDown           = 0.
        self.wt_ff_ttUp            = 0.
        self.wt_ff_ttDown          = 0.
        self.wt_ff_qcdfitpar1Up    = 0.
        self.wt_ff_qcdfitpar1Down  = 0.
        self.wt_ff_qcdfitpar2Up    = 0.
        self.wt_ff_qcdfitpar2Down  = 0.
        self.wt_ff_wfitpar1Up      = 0.
        self.wt_ff_wfitpar1Down    = 0.
        self.wt_ff_wfitpar2Up      = 0.
        self.wt_ff_wfitpar2Down    = 0.
        self.wt_ff_wfitpar3Up      = 0.
        self.wt_ff_wfitpar3Down    = 0.
        self.wt_ff_wfitpar4Up      = 0.
        self.wt_ff_wfitpar4Down    = 0.
        self.wt_ff_ttfitpar1Up     = 0.
        self.wt_ff_ttfitpar1Down   = 0.
        self.wt_ff_ttfitpar2Up     = 0.
        self.wt_ff_ttfitpar2Down   = 0. 
        self.ffunc_qcd             = 0.
        self.ffunc_w               = 0.
        self.ffunc_tt              = 0.
        self.ff_fitunc_qcd_par1    = 0.
        self.ff_fitunc_qcd_par2    = 0.
        self.ff_fitunc_w_par1      = 0.
        self.ff_fitunc_w_par2      = 0.
        self.ff_fitunc_w_par3      = 0.
        self.ff_fitunc_w_par4      = 0.
        self.ff_fitunc_tt_par1     = 0.
        self.ff_fitunc_tt_par2     = 0.
        self.wt_dy                 = 1.
        self.wt_dy_old             = 1.
        self.wt_dy_reco            = 1.
        self.wt_tt                 = 1.
        self.wt_tt_pol1            = 1.
        self.wt_tt_pol2            = 1.
        self.wt_w                  = 1.
        self.wt_dy_nlo             = 1.
        self.wt_w_nlo              = 1.
        self.Dzeta                 = -100.
        self.DPhi                  = -10.
        self.DEta                  = -10.
        self.DEta_jets_forward     = -10.
        self.DPhiLepMET            = -10.
        self.DRLepMET              = -1.
        self.DRBjets               = -1.
        self.DRBjets_lm            = -1.
        self.DRBjets_mt            = -1.
        self.DEta_Bjets            = -10.
        self.DPhi_Bjets            = -10.
        self.Bjets_pt              = -1.
        self.dijet_pt              = -1.
        self.dijet_eta             = -10.
        self.dijet_phi             = -10.
        self.dijet_mass            = -1.
        self.DRjets                = -1.
        self.DEta_jets             = -10.
        self.DPhi_jets             = -10.
        self.vistauMET_pt          = -1.
        self.LepJ_mass             = -1.
        self.TauJ_mass             = -1.
        self.Taudijet_mass         = -1.
        self.vistauJ_mass          = -1.
        self.vistauJMET_mass       = -1.
        self.TauJMET_mass          = -1.
        self.LepJMET_mass          = -1.
        self.METJ_mass             = -1.
        self.LepJ_pt               = -1.
        self.TauJ_pt               = -1.
        self.vistauJ_pt            = -1.
        self.vistauJMET_pt         = -1.
        self.TauJMET_pt            = -1.
        self.LepJMET_pt            = -1.
        self.METJ_pt               = -1.
        self.DRTauJ                = -1.
        self.DEtaTauJ              = -10.
        self.DPhiTauJ              = -10.
        self.DRLepJ                = -1.
        self.DEtaLepJ               = -10.
        self.DPhiLepJ               = -10.
        self.DRTauJ2               = -1.
        self.DEtaTauJ2             = -10.
        self.DPhiTauJ2             = -10.
        self.DRLepJ2               = -1.
        self.DEtaLepJ2             = -10.
        self.DPhiLepJ2             = -10.
        self.HJ_mass               = -1.
        self.HJ_pt                 = -1.
        self.DRHJ                  = -1.
        self.DEtaHJ                = -10.
        self.DPhiHJ                = -10.
        self.HJ2_mass              = -1.
        self.HJ2_pt                = -1.
        self.DRHJ2                 = -1.
        self.DEtaHJ2               = -10.
        self.DPhiHJ2               = -10.
        self.TTCR_Mufired          = 0.
        self.TTCR_Efired           = 0.
        self.HPStrigger            = False
        self.HPStrigger_error      = False
        self.MuTrigger_fired       = False
        self.MuTauTrigger_fired    = False
        self.MuTauTrigger_HPS_fired = False
        self.MuTauTrigger_noHPS_fired = False
        self.ETrigger_fired        = False
        self.ETauTrigger_fired     = False
        self.ETauTrigger_HPS_fired = False
        self.ETauTrigger_noHPS_fired = False
        self.METTrigger_fired      = False
        self.MuTriggermatch        = True
        self.ETriggermatch         = True
        #############   Gen Weight ######################
        if "TauEmbedding" in self.sample:
            self.GeneratorWeight = event.Generator_weight
        if self.isMC:
            PUWeight = self.puWeightProducer.getWeight(event)
            self.PUWeight =  PUWeight[0]
            self.PUWeight_up = PUWeight[1]
            self.PUWeight_down = PUWeight[2]
            self.PUWeight_old = event.puWeight
            self.GenWeight =  event.genWeight
            self.EventWeight *= self.GenWeight
            self.EventWeight *= self.PUWeight
            #if self.year in [2016,2017]:
            #    self.PrefireWeight = event.PrefireWeight
            #    self.PrefireWeight_up = event.PrefireWeightUp
            #    self.PrefireWeight_down = event.PrefireWeightDown
            #apply stitching weights for NLO DYJets samples
            if self.sample_name in ["DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8","DYJetsToLL_0J_TuneCP5_13TeV-amcatnloFXFX-pythia8","DYJetsToLL_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8","DYJetsToLL_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8"]:
                xsec_0J = 5125.0
                xsec_1J = 951.4
                xsec_2J = 358.6
                xsec_sum = xsec_0J + xsec_1J + xsec_2J
                JSON_path = '/work/pbaertsc/bbh/NanoTreeProducer/json/UL%s%s/'%(self.year,self.preVFP)
                nevents_incl = utils.getJSON(JSON_path,"DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8",self.year,self.ULtag,self.preVFP)
                nevents_0J = utils.getJSON(JSON_path,"DYJetsToLL_0J_TuneCP5_13TeV-amcatnloFXFX-pythia8",self.year,self.ULtag,self.preVFP)
                nevents_1J = utils.getJSON(JSON_path,"DYJetsToLL_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8",self.year,self.ULtag,self.preVFP)
                nevents_2J = utils.getJSON(JSON_path,"DYJetsToLL_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8",self.year,self.ULtag,self.preVFP)
                genweight_incl = 25500. #values for Summer20UL production campaign
                genweight_0J = 7310.
                genweight_1J = 9775.
                genweight_2J = 8330.
                weight_0J_incl = ((xsec_0J/xsec_sum)*(nevents_incl/genweight_incl))/((xsec_0J/xsec_sum)*(nevents_incl/genweight_incl)+(nevents_0J/genweight_0J))
                weight_1J_incl = ((xsec_1J/xsec_sum)*(nevents_incl/genweight_incl))/((xsec_1J/xsec_sum)*(nevents_incl/genweight_incl)+(nevents_1J/genweight_1J))
                weight_2J_incl = ((xsec_2J/xsec_sum)*(nevents_incl/genweight_incl))/((xsec_2J/xsec_sum)*(nevents_incl/genweight_incl)+(nevents_2J/genweight_2J))
                weight_0J_excl = (nevents_0J/genweight_0J)/((xsec_0J/xsec_sum)*(nevents_incl/genweight_incl)+(nevents_0J/genweight_0J))
                weight_1J_excl = (nevents_1J/genweight_1J)/((xsec_1J/xsec_sum)*(nevents_incl/genweight_incl)+(nevents_1J/genweight_1J))
                weight_2J_excl = (nevents_2J/genweight_2J)/((xsec_2J/xsec_sum)*(nevents_incl/genweight_incl)+(nevents_2J/genweight_2J))
                if self.sample_name=="DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8":
                    if event.LHE_NpNLO==0:
                        self.wt_dy_nlo = weight_0J_incl
                    elif event.LHE_NpNLO==1:
                        self.wt_dy_nlo = weight_1J_incl
                    elif event.LHE_NpNLO==2:
                        self.wt_dy_nlo = weight_2J_incl
                elif self.sample_name=="DYJetsToLL_0J_TuneCP5_13TeV-amcatnloFXFX-pythia8":
                    self.wt_dy_nlo = weight_0J_excl
                elif self.sample_name=="DYJetsToLL_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8":
                    self.wt_dy_nlo = weight_1J_excl
                elif self.sample_name=="DYJetsToLL_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8":
                    self.wt_dy_nlo = weight_2J_excl  
            #apply stitching weights for NLO WJets samples   
            elif self.sample_name in ['WJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-pythia8','WJetsToLNu_0J_TuneCP5_13TeV-amcatnloFXFX-pythia8','WJetsToLNu_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8','WJetsToLNu_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8']:
                xsec_0J = 53300.0
                xsec_1J = 8949.0
                xsec_2J = 3335.0
                xsec_sum = xsec_0J + xsec_1J + xsec_2J
                JSON_path = '/work/pbaertsc/bbh/NanoTreeProducer/json/UL%s%s/'%(self.year,self.preVFP)
                nevents_incl = utils.getJSON(JSON_path,"WJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-pythia8",self.year,self.ULtag,self.preVFP)
                nevents_0J = utils.getJSON(JSON_path,"WJetsToLNu_0J_TuneCP5_13TeV-amcatnloFXFX-pythia8",self.year,self.ULtag,self.preVFP)
                nevents_1J = utils.getJSON(JSON_path,"WJetsToLNu_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8",self.year,self.ULtag,self.preVFP)
                nevents_2J = utils.getJSON(JSON_path,"WJetsToLNu_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8",self.year,self.ULtag,self.preVFP)
                genweight_incl = 249000. #values for Summer20UL production campaign
                genweight_0J = 74800.
                genweight_1J = 93500.
                genweight_2J = 78020.
                weight_0J_incl = ((xsec_0J/xsec_sum)*(nevents_incl/genweight_incl))/((xsec_0J/xsec_sum)*(nevents_incl/genweight_incl)+(nevents_0J/genweight_0J))
                weight_1J_incl = ((xsec_1J/xsec_sum)*(nevents_incl/genweight_incl))/((xsec_1J/xsec_sum)*(nevents_incl/genweight_incl)+(nevents_1J/genweight_1J))
                weight_2J_incl = ((xsec_2J/xsec_sum)*(nevents_incl/genweight_incl))/((xsec_2J/xsec_sum)*(nevents_incl/genweight_incl)+(nevents_2J/genweight_2J))
                weight_0J_excl = (nevents_0J/genweight_0J)/((xsec_0J/xsec_sum)*(nevents_incl/genweight_incl)+(nevents_0J/genweight_0J))
                weight_1J_excl = (nevents_1J/genweight_1J)/((xsec_1J/xsec_sum)*(nevents_incl/genweight_incl)+(nevents_1J/genweight_1J))
                weight_2J_excl = (nevents_2J/genweight_2J)/((xsec_2J/xsec_sum)*(nevents_incl/genweight_incl)+(nevents_2J/genweight_2J))
                if self.sample_name=="WJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-pythia8":
                    if event.LHE_NpNLO==0:
                        self.wt_w_nlo = weight_0J_incl
                    elif event.LHE_NpNLO==1:
                        self.wt_w_nlo = weight_1J_incl
                    elif event.LHE_NpNLO==2:
                        self.wt_w_nlo = weight_2J_incl
                elif self.sample_name=="WJetsToLNu_0J_TuneCP5_13TeV-amcatnloFXFX-pythia8":
                    self.wt_w_nlo = weight_0J_excl
                elif self.sample_name=="WJetsToLNu_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8":
                    self.wt_w_nlo = weight_1J_excl
                elif self.sample_name=="WJetsToLNu_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8":
                    self.wt_w_nlo = weight_2J_excl
            
            self.LHE_Nb = event.LHE_Nb
            self.LHE_Nc = event.LHE_Nc
            self.LHE_Njets = event.LHE_Njets
            self.LHE_NpLO = event.LHE_NpLO
            self.LHE_NpNLO = event.LHE_NpNLO
            self.LHEPdfWeight = event.LHEPdfWeight[0]
            self.LHE_Vpt = event.LHE_Vpt
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
    
        if self.isData and event.PV_npvs == 0:
            return False
        if not self.isData:
            #self.out.pileup.Fill(event.Pileup_nTrueInt)
            if event.Pileup_nTrueInt == 0:
                return False

        if "SingleElectron_Run2016B" in self.sample:
            try:
                trigger1 = event.HLT_IsoMu22_eta2p1
                trigger2 = event.HLT_IsoTkMu22_eta2p1
            except:
                event.HLT_IsoMu22_eta2p1 = False
                event.HLT_IsoTkMu22_eta2p1 = False  
        if "ZZTo2Nu2Q_5f" in self.sample and self.year==2018:
            try:
                trigger1 = event.HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTauHPS30_eta2p1_CrossL1
            except:
                event.HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTauHPS30_eta2p1_CrossL1 = False
            try:
                trigger1 = event.HLT_Ele35_WPTight_Gsf
            except:
                event.HLT_Ele35_WPTight_Gsf = False
            try:
                trigger1 = event.HLT_IsoMu20_eta2p1_LooseChargedIsoPFTauHPS27_eta2p1_CrossL1
            except:
                event.HLT_IsoMu20_eta2p1_LooseChargedIsoPFTauHPS27_eta2p1_CrossL1 = False
                
        # only selecting events with zero jets for inclusive DYjets sample to combine with jet binned samples
        if self.sample_name=="DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8":
            if event.LHE_Njets>0:
                return False
        if "W1JetsToLNu" in self.sample_name or "W3JetsToLNu" in self.sample_name: #remove outliners in EventWeight in 1 and 3 jet binned W+jets samples (don't apply for others!)
            if self.EventWeight > 1000.:
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
        #splitting sample SUSYGluGluToBBHToTauTau
        if "SUSYGluGluToBBHToTauTau" in self.sample and self.nGenBjets==0:
            return False
        if "SUSYGluGluToJJHToTauTau" in self.sample and self.nGenBjets>0:
            return False
        ############  lepton selection  ####################
        tau_vetomu_list = []
        tau_vetoe_list = []
        tau_vetomu_ar_list = []
        tau_vetoe_ar_list = []
        ditau_list = []
        muon_list = []
        muon_veto_list = []
        dimuon_veto_list = []
        dimuon_list = []
        muon_electron_list = []
        muon_loose_list = []
        electron_list = []
        electron_veto_list = []
        dielectron_veto_list = []
        electron_loose_list = []
        mutau_list =[]
        mutau_loose_list = []
        mutauAR_list = []
        mutauAR_loose_list = []
        etau_list = []
        etau_loose_list = []
        etauAR_list = []
        etauAR_loose_list = []
        tautau_list = []
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
                if "Up" in self.tes:
                    if (self.tes == "TauESdm0Up" and tau_decaymode==0) or (self.tes == "TauESdm1Up" and tau_decaymode == 1) or (self.tes == "TauESdm10Up" and tau_decaymode==10):
                        tau_energyscale = self.tauES.getES(tau.pt,tau.eta,tau_decaymode,genmatching(event,tau),"up")
                    else:
                        tau_energyscale = self.tauES.getES(tau.pt,tau.eta,tau_decaymode,genmatching(event,tau),"nom")
                elif "Down" in self.tes:
                    if (self.tes == "TauESdm0Down" and tau_decaymode==0) or (self.tes == "TauESdm1Down" and tau_decaymode == 1) or (self.tes == "TauESdm10Down" and tau_decaymode==10):
                        tau_energyscale = self.tauES.getES(tau.pt,tau.eta,tau_decaymode,genmatching(event,tau),"down")
                    else:
                        tau_energyscale = self.tauES.getES(tau.pt,tau.eta,tau_decaymode,genmatching(event,tau),"nom")
                else:
                    tau_energyscale = self.tauES.getES(tau.pt,tau.eta,tau_decaymode,genmatching(event,tau),"nom")
                
                tau_tlv = tau_tlv * tau_energyscale
                tau.pt = tau_tlv.Pt()
                tau.eta = tau_tlv.Eta()
                tau.phi = tau_tlv.Phi()
                tau.mass = tau_tlv.M()
                tau.es = tau_energyscale

            if tau.pt > 30. and abs(tau.eta) < 2.3 and abs(tau.charge) == 1 and abs(tau.dz) < 0.2 and tau_idDecayMode and tau.idDeepTau2017v2p1VSjet >= 31:
                if tau.idDeepTau2017v2p1VSe >= 1 and tau.idDeepTau2017v2p1VSmu == 15:
                    tau_vetomu_list.append(tau)
                if tau.idDeepTau2017v2p1VSe >= 63 and tau.idDeepTau2017v2p1VSmu >= 1:
                    tau_vetoe_list.append(tau)
                if tau.pt > 40. and abs(tau.eta) < 2.1 and tau.idDeepTau2017v2p1VSe >= 1 and tau.idDeepTau2017v2p1VSmu >= 1:
                    ditau_list.append(tau)
            ### select taus for application region  ###
            #was tau.idDeepTau2017v2p1VSjet&1 == 1 && tau.idDeepTau2017v2p1VSjet&16 == 0
            #was tau.idDeepTau2017v2p1VSjet>=7 and tau.idDeepTau2017v2p1VSjet<31
            if tau.pt > 30. and abs(tau.eta) < 2.3 and abs(tau.charge) == 1 and abs(tau.dz) < 0.2 and tau_idDecayMode and tau.idDeepTau2017v2p1VSjet>=1 and tau.idDeepTau2017v2p1VSjet<31:
                if tau.idDeepTau2017v2p1VSe >= 1 and tau.idDeepTau2017v2p1VSmu == 15:
                    tau_vetomu_ar_list.append(tau)
                if tau.idDeepTau2017v2p1VSe >= 63 and tau.idDeepTau2017v2p1VSmu >= 1:
                    tau_vetoe_ar_list.append(tau)

        for muon in muons:
            if muon.pt > 10. and abs(muon.eta) < 2.4 and abs(muon.dxy) < 0.045 and abs(muon.dz) < 0.2 and muon.pfRelIso04_all < 0.3:
                if muon.mediumId:
                    self.muon_veto = True
                    muon_veto_list.append(muon)
                if muon.pt > 15. and muon.isGlobal and muon.isPFcand and muon.isTracker:
                    dimuon_veto_list.append(muon)
                if muon.pt > 20. and muon.mediumId and muon.pfRelIso04_all < 0.15:
                    muon_list.append(muon)
                if muon.pt > 20. and muon.mediumId and muon.pfRelIso04_all > 0.15:
                    muon_loose_list.append(muon)
        for electron in electrons:
            if electron.pt > 10. and abs(electron.eta) < 2.5 and (abs(electron.eta)<1.444 or abs(electron.eta)>1.566) and abs(electron.dxy) < 0.045 and abs(electron.dz) < 0.2 and electron.mvaFall17V2noIso_WP90 and electron.pfRelIso03_all < 0.3:
                if electron.convVeto and electron.lostHits < 2:
                    self.electron_veto = True
                    electron_veto_list.append(electron)
                if electron.pt > 15.:
                    dielectron_veto_list.append(electron)
                if electron.pt > 25. and abs(electron.eta) < 2.1 and electron.convVeto and electron.lostHits < 2 and electron.pfRelIso03_all < 0.1:
                    electron_list.append(electron)
                if electron.pt > 25. and abs(electron.eta) < 2.1 and electron.convVeto and electron.lostHits < 2 and electron.pfRelIso03_all > 0.1:
                    electron_loose_list.append(electron)

        self.nTaus = len(tau_vetomu_list)
        self.nMuons = len(muon_list)
        self.nElectrons = len(electron_list)

        
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
        for tau1 in ditau_list:
            for tau2 in ditau_list:
                if self.vec(tau1).DeltaR(self.vec(tau2)) > 0.5:
                    tautau_list.append([tau1,tau2])    
                    self.isHtoTauTau = True
        ### signal region with looser muon isolation for fakefaktor derivation
        for tau in tau_vetomu_list:
            for muon in muon_loose_list:
                if self.vec(tau).DeltaR(self.vec(muon)) > 0.5:
                    mutau_loose_list.append([muon,tau])
                    self.isHtolooseMuTau = True
        for tau in tau_vetoe_list:
            for ele in electron_loose_list:
                if self.vec(tau).DeltaR(self.vec(ele)) > 0.5:
                    etau_loose_list.append([ele,tau])
                    self.isHtolooseETau = True
        ### define application region for fake factor method 
        for tau in tau_vetomu_ar_list:
            for muon in muon_list:
                if self.vec(tau).DeltaR(self.vec(muon)) > 0.5:
                    mutauAR_list.append([muon,tau])
                    self.isHtoMuTauAR = True
        for tau in tau_vetoe_ar_list:
            for ele in electron_list:
                if self.vec(tau).DeltaR(self.vec(ele)) > 0.5:
                    etauAR_list.append([ele,tau])
                    self.isHtoETauAR = True             
        ### application region with looser muon isolation for fakefaktor derivation
        for tau in tau_vetomu_ar_list:
            for muon in muon_loose_list:
                if self.vec(tau).DeltaR(self.vec(muon)) > 0.5:
                    mutauAR_loose_list.append([muon,tau])
                    self.isHtolooseMuTauAR = True
        for tau in tau_vetoe_ar_list:
            for ele in electron_loose_list:
                if self.vec(tau).DeltaR(self.vec(ele)) > 0.5:
                    etauAR_loose_list.append([ele,tau])
                    self.isHtolooseETauAR = True

            
        for muon1 in dimuon_veto_list:
            for muon2 in dimuon_veto_list:
                if self.vec(muon1).DeltaR(self.vec(muon2)) > 0.15:
                    if muon1.charge*muon2.charge == -1:
                        self.dimuon_veto = True
        for ele1 in dielectron_veto_list:
            for ele2 in dielectron_veto_list:
                if self.vec(ele1).DeltaR(self.vec(ele2)) > 0.15:
                    if ele1.charge*ele2.charge == -1:
                        self.dielectron_veto = True     
  
        for muon1 in muon_list:
            for muon2 in muon_list:
                if self.vec(muon1).DeltaR(self.vec(muon2)) > 0.15:
                    if muon1.charge*muon2.charge == -1:
                        self.isMuMu = True
                        dimuon_list.append([muon1,muon2])
            for ele in electron_list:
                if self.vec(muon1).DeltaR(self.vec(ele)) > 0.15:
                    if muon1.charge*ele.charge == -1:
                        self.isTTCR = True
                        muon_electron_list.append([muon1,ele])


        isMuTau = False
        isETau = False

        if self.isHtoMuTau:
            pair = self.pair_selection(mutau_list)
            isMuTau = True
            self.isHtoMuTauAR = False
            self.isHtolooseMuTau = False
            self.isHtolooseMuTauAR = False
            self.isHtoETau = False
            self.isHtoETauAR = False
            self.isHtolooseETau = False
            self.isHtolooseETauAR = False
            self.isMuMu = False
            self.isTTCR = False
        elif self.isHtoETau:
            pair = self.pair_selection(etau_list)
            isETau = True
            self.isHtoMuTau = False
            self.isHtoMuTauAR = False
            self.isHtolooseMuTau = False
            self.isHtolooseMuTauAR = False
            self.isHtoETauAR = False
            self.isHtolooseETau = False
            self.isHtolooseETauAR = False
            self.isMuMu = False
            self.isTTCR = False
        elif self.isHtoMuTauAR:
            pair = self.pair_selection(mutauAR_list)
            isMuTau = True
            self.isHtoMuTau = False
            self.isHtolooseMuTau = False
            self.isHtolooseMuTauAR = False
            self.isHtoETau = False
            self.isHtoETauAR = False
            self.isHtolooseETau = False
            self.isHtolooseETauAR = False
            self.isMuMu = False
            self.isTTCR = False
        elif self.isHtoETauAR:
            pair = self.pair_selection(etauAR_list)
            isETau = True
            self.isHtoMuTau = False
            self.isHtoMuTauAR = False
            self.isHtolooseMuTau = False
            self.isHtolooseMuTauAR = False
            self.isHtoETau = False
            self.isHtolooseETau = False
            self.isHtolooseETauAR = False
            self.isMuMu = False
            self.isTTCR = False
        elif self.isHtolooseMuTau:
            pair = self.pair_selection(mutau_loose_list)
            isMuTau = True
            self.isHtoMuTau = False
            self.isHtoMuTauAR = False
            self.isHtolooseMuTauAR = False
            self.isHtoETau = False
            self.isHtoETauAR = False
            self.isHtolooseETau = False
            self.isHtolooseETauAR = False
            self.isMuMu = False
            self.isTTCR = False
        elif self.isHtolooseETau:
            pair = self.pair_selection(etau_loose_list)
            isETau = True
            self.isHtoMuTau = False
            self.isHtoMuTauAR = False
            self.isHtolooseMuTau = False
            self.isHtolooseMuTauAR = False
            self.isHtoETau = False
            self.isHtoETauAR = False
            self.isHtolooseETauAR = False  
            self.isMuMu = False
            self.isTTCR = False
        elif self.isHtolooseMuTauAR:
            pair = self.pair_selection(mutauAR_loose_list)
            isMuTau = True
            self.isHtoMuTau = False
            self.isHtoMuTauAR = False
            self.isHtolooseMuTau = False
            self.isHtoETau = False
            self.isHtoETauAR = False
            self.isHtolooseETau = False
            self.isHtolooseETauAR = False
            self.isMuMu = False
            self.isTTCR = False
        elif self.isHtolooseETauAR:
            pair = self.pair_selection(etauAR_loose_list)
            isETau = True
            self.isHtoMuTau = False
            self.isHtoMuTauAR = False
            self.isHtolooseMuTau = False
            self.isHtolooseMuTauAR = False
            self.isHtoETau = False
            self.isHtoETauAR = False
            self.isHtolooseETau = False
            self.isTTCR = False
            self.isMuMu = False
        elif self.isTTCR:
            pair = self.pair_selection(muon_electron_list)
            self.isMuMu = False
        elif self.isMuMu:
            pair = self.pair_selection(dimuon_list)
        else:
            #return False
            pair = 1.
            

        if self.METfilter(event)==False:
            return False

        self.MuTrigger_fired = self.trigger_Mu.fired(event)
        self.MuTauTrigger_fired = self.trigger_MuTau.fired(event)
        self.ETrigger_fired = self.trigger_E.fired(event)
        self.ETauTrigger_fired = self.trigger_ETau.fired(event)
        self.METTrigger_fired = self.trigger_MET.fired(event)
            
        if self.year==2018 and self.isData:
            self.MuTauTrigger_HPS_fired = self.trigger_MuTau_HPS.fired(event)
            self.MuTauTrigger_noHPS_fired = self.trigger_MuTau_noHPS.fired(event)
            self.ETauTrigger_HPS_fired = self.trigger_ETau_HPS.fired(event)
            self.ETauTrigger_noHPS_fired = self.trigger_ETau_noHPS.fired(event)
            
        if isMuTau:
            self.Mu1_sltrig_fired = self.trigger_Mu.match(event,pair[0])
            self.Mu1_ctrig_fired = self.trigger_MuTau.match(event,pair[0],leg=1)
            self.Tau1_ctrig_fired = self.trigger_MuTau.match(event,pair[1],leg=2)
            if self.year == 2018 and self.isData:
                self.Mu1_ctrig_HPS_fired = self.trigger_MuTau_HPS.match(event,pair[0],leg=1)
                self.Tau1_ctrig_HPS_fired = self.trigger_MuTau_HPS.match(event,pair[1],leg=2)
                self.Mu1_ctrig_noHPS_fired = self.trigger_MuTau_noHPS.match(event,pair[0],leg=1)
                self.Tau1_ctrig_noHPS_fired = self.trigger_MuTau_noHPS.match(event,pair[1],leg=2)

            if not self.MuTrigger_fired:
                return False
            if not self.Mu1_sltrig_fired:
                return False
            
            #if not (self.MuTrigger_fired or self.MuTauTrigger_fired): 
            #    return False

            #if self.year==2018 and self.isData and not "TauEmbedding" in self.sample_name:
            #        if not self.trigger_Mu.fired(event) and not self.trigger_MuTau_noHPS.fired(event) and self.trigger_MuTau_HPS.fired(event):
            #            self.HPStrigger = True
            #            if not (self.trigger_MuTau_HPS.match(event,pair[0],leg=1) and self.trigger_MuTau_HPS.match(event,pair[1],leg=2)):
            #                self.HPStrigger_error = True

            #if not (self.Mu1_sltrig_fired or (self.trigger_MuTau.match(event,pair[0]) and self.trigger_MuTau.match(event,pair[1]))):
            #    self.MuTriggermatch = False
            
            #if not (self.Mu1_sltrig_fired or (self.Mu1_ctrig_fired and self.Tau1_ctrig_fired)):
            #    return False
            

            self.Mu1_pt                = pair[0].pt
            self.Mu1_eta               = pair[0].eta
            self.Mu1_phi               = pair[0].phi
            self.Mu1_mass              = pair[0].mass
            self.Mu1_charge            = pair[0].charge
            self.Mu1_iso               = self.iso(pair[0])
        elif isETau:
            self.Ele1_sltrig_fired = self.trigger_E.match(event,pair[0])
            self.Ele1_ctrig_fired = self.trigger_ETau.match(event,pair[0],leg=1)
            self.Tau1_ctrig_fired = self.trigger_ETau.match(event,pair[1],leg=2)
            if self.year == 2018 and self.isData:
                self.Ele1_ctrig_HPS_fired = self.trigger_ETau_HPS.match(event,pair[0],leg=1)
                self.Tau1_ctrig_HPS_fired = self.trigger_ETau_HPS.match(event,pair[1],leg=2)
                self.Ele1_ctrig_noHPS_fired = self.trigger_ETau_noHPS.match(event,pair[0],leg=1)
                self.Tau1_ctrig_noHPS_fired = self.trigger_ETau_noHPS.match(event,pair[1],leg=2) 

            
            if not self.ETrigger_fired:
                return False
            if not self.Ele1_sltrig_fired:
                return False
            #if self.year==2016 and ((self.isData and event.run > 278240) or (self.isMC and self.preVFP=="")): #only use single electron trigger for postVFP 2016 data and mc
            #    self.ETauTrigger_fired = False #to avoid problems with SF if both triggers are fired
            #    self.Ele1_ctrig_fired = False

            #if not (self.ETrigger_fired or self.ETauTrigger_fired):
            #    return False


            #if self.year==2018 and self.isData and not "TauEmbedding" in self.sample_name:
            #    if not self.trigger_E.fired(event) and not self.trigger_ETau_noHPS.fired(event) and self.trigger_ETau_HPS.fired(event):
            #        self.HPStrigger = True
            #        if not (self.trigger_ETau_HPS.match(event,pair[0],leg=1) and self.trigger_ETau_HPS.match(event,pair[1],leg=2)):
            #            self.HPStrigger_error = True
                            
            
            #if not (self.Ele1_sltrig_fired or (self.trigger_ETau.match(event,pair[0]) and self.trigger_ETau.match(event,pair[1]))):
            #    self.ETriggermatch = False
                
            #if not (self.Ele1_sltrig_fired or (self.Ele1_ctrig_fired and self.Tau1_ctrig_fired)):
            #    return False

            self.Ele1_pt                = pair[0].pt
            self.Ele1_eta               = pair[0].eta
            self.Ele1_phi               = pair[0].phi
            self.Ele1_mass              = pair[0].mass
            self.Ele1_charge            = pair[0].charge
            self.Ele1_iso               = self.iso(pair[0])
        elif self.isMuMu:
            if not self.MuTrigger_fired:
                return False
            if not (self.trigger_Mu.match(event,pair[0]) or self.trigger_Mu.match(event,pair[1])):
                return False
            self.Mu1_pt                = pair[0].pt
            self.Mu1_eta               = pair[0].eta
            self.Mu1_phi               = pair[0].phi
            self.Mu1_mass              = pair[0].mass
            self.Mu1_charge            = pair[0].charge
            self.Mu1_iso               = self.iso(pair[0])   
            self.Mu2_pt                = pair[1].pt
            self.Mu2_eta               = pair[1].eta
            self.Mu2_phi               = pair[1].phi
            self.Mu2_mass              = pair[1].mass
            self.Mu2_charge            = pair[1].charge
            self.Mu2_iso               = self.iso(pair[1])
        elif self.isTTCR:
            if not (self.MuTrigger_fired or self.ETrigger_fired):
                return False
            if not (self.trigger_Mu.match(event,pair[0]) or self.trigger_E.match(event,pair[1])):
                return False
            if self.MuTrigger_fired and ("EGamma" in self.sample_name or "SingleElectron" in self.sample_name):
                self.TTCR_Mufired      = 1.
                return False #avoid double counting
            if self.ETrigger_fired and not self.trigger_Mu.fired(event) and "SingleMuon" in self.sample_name:
                self.TTCR_Efired       = 1.
                return False #avoid double counting
            self.Mu1_pt                = pair[0].pt
            self.Mu1_eta               = pair[0].eta
            self.Mu1_phi               = pair[0].phi
            self.Mu1_mass              = pair[0].mass
            self.Mu1_charge            = pair[0].charge
            self.Mu1_iso               = self.iso(pair[0])   
            self.Ele1_pt                = pair[1].pt
            self.Ele1_eta               = pair[1].eta
            self.Ele1_phi               = pair[1].phi
            self.Ele1_mass              = pair[1].mass
            self.Ele1_charge            = pair[1].charge
            self.Ele1_iso               = self.iso(pair[1])

        if isMuTau or isETau:
            self.Tau1_pt               = pair[1].pt
            self.Tau1_eta              = pair[1].eta
            self.Tau1_phi              = pair[1].phi
            self.Tau1_mass             = pair[1].mass
            self.Tau1_charge           = pair[1].charge
            self.Tau1_iso              = self.iso(pair[1])
            if pair[1].decayMode not in [0,1,2,10,11]:
                return False
            self.Tau1_decaymode        = pair[1].decayMode
            self.Tau1_Idvsjet          = pair[1].idDeepTau2017v2p1VSjet
            self.Tau1_Idvse            = pair[1].idDeepTau2017v2p1VSe
            self.Tau1_Idvsmu           = pair[1].idDeepTau2017v2p1VSmu
            if self.isMC:
                self.Tau1_ES               = pair[1].es
            if self.isHtoMuTau or self.isHtolooseMuTau:
                self.Tau1_Idvsjetwp    = "Medium"
                self.Tau1_Idvsewp      = "VVLoose"
                self.Tau1_Idvsmuwp     = "Tight"
            elif self.isHtoETau or self.isHtolooseETau:      
                self.Tau1_Idvsjetwp    = "Medium"
                self.Tau1_Idvsewp      = "Tight"
                self.Tau1_Idvsmuwp     = "VLoose"
            elif self.isHtoMuTauAR or self.isHtolooseMuTauAR:
                self.Tau1_Idvsjetwp    = "VVVLoose"
                self.Tau1_Idvsewp      = "VVLoose"
                self.Tau1_Idvsmuwp     = "Tight"
            elif self.isHtoETauAR or self.isHtolooseETauAR:
                self.Tau1_Idvsjetwp    = "VVVLoose"
                self.Tau1_Idvsewp      = "Tight"
                self.Tau1_Idvsmuwp     = "VLoose"

            self.mysvinterface.clearLeptons()
            self.mysvinterface.setTauOne(1,pair[0].pt,pair[0].eta,pair[0].phi,pair[0].mass,-1)
            self.mysvinterface.setTauTwo(2,pair[1].pt,pair[1].eta,pair[1].phi,pair[1].mass,pair[1].decayMode)
            met = Object(event, "MET") #only CHS MET has covariance matrix
            metvec = ROOT.TLorentzVector()
            metvec.SetPtEtaPhiM(met.pt,0.,met.phi,0.)
            self.mysvinterface.setMetAndCovMat(metvec.Px(),metvec.Py(),met.covXX,met.covXY,met.covXY,met.covYY)
            self.mysvinterface.calcSV()
            self.H_mass                = self.mysvinterface.getMass()
            self.H_pt                  = self.mysvinterface.getPt()
            self.H_eta                 = self.mysvinterface.getEta()
            self.H_phi                 = self.mysvinterface.getPhi()
            H_tlv = ROOT.TLorentzVector()
            H_tlv.SetPtEtaPhiM(self.H_pt,self.H_eta,self.H_phi,self.H_mass)

        if isMuTau or isETau:
            vistau                     = self.tlv(pair[0])+self.tlv(pair[1])
            self.vis_pt                = vistau.Pt()
            self.vis_eta               = vistau.Eta()
            self.vis_phi               = vistau.Phi()
            self.vis_mass              = vistau.M()

            vistau1_tlv  = self.tlv(pair[0])
            self.vistau1_pt            = vistau1_tlv.Pt()
            self.vistau1_eta           = vistau1_tlv.Eta()
            self.vistau1_phi           = vistau1_tlv.Phi()
            self.vistau1_mass          = vistau1_tlv.M()
            self.vistau1_energy        = vistau1_tlv.E()
            vistau2_tlv  = self.tlv(pair[1])
            self.vistau2_pt            = vistau2_tlv.Pt()
            self.vistau2_eta           = vistau2_tlv.Eta()
            self.vistau2_phi           = vistau2_tlv.Phi()
            self.vistau2_mass          = vistau2_tlv.M()
            self.vistau2_energy        = vistau2_tlv.E()

        if 'Embedding' in self.sample:
            genParticles = Collection(event, "GenPart")
            genTau1_pt = 0.
            genTau1_eta = 0.
            genTau2_pt = 0.
            genTau2_eta = 0.
            for genPart in genParticles:
                if abs(genPart.pdgId) == 15:
                    if genPart.pt>genTau1_pt:
                        genTau2_pt = genTau1_pt
                        genTau2_eta = genTau1_eta
                        genTau1_pt = genPart.pt
                        genTau1_eta = genPart.eta
                    else:
                        genTau2_pt = genPart.pt
                        genTau2_eta = genPart.eta
            self.TauEmbedding_TriggerWeight = self.TauEmbeddedSFs.getTriggerSF(genTau1_pt,genTau1_eta,genTau2_pt,genTau2_eta)
            if isMuTau:
                self.TauEmbedding_IdWeight = self.TauEmbeddedSFs.getMuIdSF(self.Mu1_pt,self.Mu1_eta)
            elif isETau:
                self.TauEmbedding_IdWeight = self.TauEmbeddedSFs.getMuIdSF(self.Ele1_pt,self.Ele1_eta)
        if self.isMC:
            if isMuTau:
                self.Mu1_genmatch      = genmatching(event,pair[0])
                MuSF                      = self.muSFs.getSF(self.Mu1_pt,self.Mu1_eta)
                self.MuWeight             = MuSF[0]
                self.MuWeight_up          = MuSF[1]
                self.MuWeight_down        = MuSF[2]
                self.MuTriggerWeight_old  = self.muSFs.getTriggerSF(self.Mu1_pt,self.Mu1_eta)
                MuTriggerSF               = self.triggerSFs.getTriggerSF("mutau",self.Mu1_pt,self.Mu1_eta,self.Tau1_pt,self.Tau1_decaymode,self.Tau1_Idvsjetwp,self.Mu1_sltrig_fired,self.Mu1_ctrig_fired)
                self.MuTriggerWeight      = MuTriggerSF
                MuTriggerSFError          = self.triggerSFs.getTriggerSFError("mutau",self.Mu1_pt,self.Mu1_eta,self.Tau1_pt,self.Tau1_decaymode,self.Tau1_Idvsjetwp,self.Mu1_sltrig_fired,self.Mu1_ctrig_fired)
                self.MuTriggerWeight_gen  = MuTriggerSFError[0]
                self.MuTriggerWeight_up   = MuTriggerSFError[1]
                self.MuTriggerWeight_down = MuTriggerSFError[2]
                self.MuTriggerWeight_sl    = self.triggerSFs.getTriggerSF_SL("mutau",self.Mu1_pt,self.Mu1_eta)
                self.MuTriggerWeight_cross = self.triggerSFs.getTriggerSF_Cross("mutau",self.Mu1_pt,self.Mu1_eta,self.Tau1_pt,self.Tau1_decaymode,self.Tau1_Idvsjetwp)
                self.MuTriggerWeight_crossold = self.triggerSFs.getTriggerSF_CrossOld("mutau",self.Mu1_pt,self.Mu1_eta,self.Tau1_pt,self.Tau1_decaymode,self.Tau1_Idvsjetwp)
                self.MuTriggerWeight_lepcross = self.triggerSFs.getTriggerSF_lepCross("mutau",self.Mu1_pt,self.Mu1_eta,self.Tau1_pt,self.Tau1_decaymode,self.Tau1_Idvsjetwp)
                self.MuTriggerWeight_taucross = self.triggerSFs.getTriggerSF_tauCross("mutau",self.Mu1_pt,self.Mu1_eta,self.Tau1_pt,self.Tau1_decaymode,self.Tau1_Idvsjetwp)
                self.Tau1_genmatch     = genmatching(event,pair[1])
                TauSF                      = self.tauSFs.getSF(self.Tau1_pt,self.Tau1_eta,self.Tau1_decaymode,self.Tau1_genmatch,self.Tau1_Idvsjetwp,self.Tau1_Idvsmuwp,self.Tau1_Idvsewp)
                self.TauWeight             = TauSF[0]
                self.TauWeightVSjet        = TauSF[1]
                self.TauWeightVSjet_up     = TauSF[2]
                self.TauWeightVSjet_down   = TauSF[3]
                self.TauWeightVSmu         = TauSF[4]
                self.TauWeightVSmu_up      = TauSF[5]
                self.TauWeightVSmu_down    = TauSF[6]
                self.TauWeightVSe          = TauSF[7]
                self.TauWeightVSe_up       = TauSF[8]
                self.TauWeightVSe_down     = TauSF[9]
            elif isETau:
                self.Ele1_genmatch      = genmatching(event,pair[0])
                ESF                      = self.eSFs.getSF(self.Ele1_pt,self.Ele1_eta)
                self.EWeight             = ESF[0]
                self.EWeight_up          = ESF[1]
                self.EWeight_down        = ESF[2]
                self.ETriggerWeight_old  = self.eSFs.getTriggerSF(self.Ele1_pt,self.Ele1_eta)
                ETriggerSF               = self.triggerSFs.getTriggerSF("etau",self.Ele1_pt,self.Ele1_eta,self.Tau1_pt,self.Tau1_decaymode,self.Tau1_Idvsjetwp,self.Ele1_sltrig_fired,self.Ele1_ctrig_fired)
                self.ETriggerWeight      = ETriggerSF
                ETriggerSFError          = self.triggerSFs.getTriggerSFError("etau",self.Ele1_pt,self.Ele1_eta,self.Tau1_pt,self.Tau1_decaymode,self.Tau1_Idvsjetwp,self.Ele1_sltrig_fired,self.Ele1_ctrig_fired)
                self.ETriggerWeight_gen  = ETriggerSFError[0]
                self.ETriggerWeight_up   = ETriggerSFError[1]
                self.ETriggerWeight_down = ETriggerSFError[2]
                self.ETriggerWeight_sl    = self.triggerSFs.getTriggerSF_SL("etau",self.Ele1_pt,self.Ele1_eta)
                self.ETriggerWeight_cross = self.triggerSFs.getTriggerSF_Cross("etau",self.Ele1_pt,self.Ele1_eta,self.Tau1_pt,self.Tau1_decaymode,self.Tau1_Idvsjetwp)
                self.ETriggerWeight_crossold = self.triggerSFs.getTriggerSF_CrossOld("etau",self.Ele1_pt,self.Ele1_eta,self.Tau1_pt,self.Tau1_decaymode,self.Tau1_Idvsjetwp)
                self.ETriggerWeight_lepcross = self.triggerSFs.getTriggerSF_lepCross("etau",self.Ele1_pt,self.Ele1_eta,self.Tau1_pt,self.Tau1_decaymode,self.Tau1_Idvsjetwp)
                self.ETriggerWeight_taucross = self.triggerSFs.getTriggerSF_tauCross("etau",self.Ele1_pt,self.Ele1_eta,self.Tau1_pt,self.Tau1_decaymode,self.Tau1_Idvsjetwp)
                self.Tau1_genmatch     = genmatching(event,pair[1])
                TauSF                      = self.tauSFs.getSF(self.Tau1_pt,self.Tau1_eta,self.Tau1_decaymode,self.Tau1_genmatch,self.Tau1_Idvsjetwp,self.Tau1_Idvsmuwp,self.Tau1_Idvsewp)
                self.TauWeight             = TauSF[0]
                self.TauWeightVSjet        = TauSF[1]
                self.TauWeightVSjet_up     = TauSF[2]
                self.TauWeightVSjet_down   = TauSF[3]
                self.TauWeightVSmu         = TauSF[4]
                self.TauWeightVSmu_up      = TauSF[5]
                self.TauWeightVSmu_down    = TauSF[6]
                self.TauWeightVSe          = TauSF[7]
                self.TauWeightVSe_up       = TauSF[8]
                self.TauWeightVSe_down     = TauSF[9]
            elif self.isTTCR:
                self.Mu1_genmatch          = genmatching(event,pair[0])
                self.Ele1_genmatch         = genmatching(event,pair[1])
                MuETriggerSF                = self.triggerSFs.getTriggerSF_MuE(self.Mu1_pt,self.Mu1_eta,self.Ele1_pt,self.Ele1_eta)
                self.MuTriggerWeight       = MuETriggerSF[0]
                self.MuTriggerWeight_up    = MuETriggerSF[1]
                self.MuTriggerWeight_down  = MuETriggerSF[2]
                MuSF                       = self.muSFs.getSF(self.Mu1_pt,self.Mu1_eta)
                self.MuWeight              = MuSF[0]
                self.MuWeight_up           = MuSF[1]
                self.MuWeight_down         = MuSF[2]
                ESF                       = self.eSFs.getSF(self.Ele1_pt,self.Ele1_eta)
                self.EWeight              = ESF[0]
                self.EWeight_up           = ESF[1]
                self.EWeight_down         = ESF[2]
            elif self.isMuMu:
                self.Mu1_genmatch      = genmatching(event,pair[0])
                MuTriggerSF                = self.triggerSFs.getTriggerSF_MuMu(self.Mu1_pt,self.Mu1_eta,self.Mu2_pt,self.Mu2_eta)
                self.MuTriggerWeight       = MuTriggerSF[0]
                self.MuTriggerWeight_up    = MuTriggerSF[1]
                self.MuTriggerWeight_down  = MuTriggerSF[2]
                MuSF                       = self.muSFs.getSFMuMu(self.Mu1_pt,self.Mu1_eta,self.Mu2_pt,self.Mu2_eta)
                self.MuWeight              = MuSF[0]
                self.MuWeight_up           = MuSF[1]
                self.MuWeight_down         = MuSF[2]
                self.Mu2_genmatch      = genmatching(event,pair[1])
          
        
        #following MET and jet pt are used (jet pt neglected for derivation of fakefactor shape correction)
        ###################################################################################################

        if self.JECvar=="":
            self.MET         = event.PuppiMET_pt
            self.MET_phi     = event.PuppiMET_phi
            self.MET_chs     = event.MET_pt
            self.MET_chs_phi = event.MET_phi
        elif self.JECvar=='jesTotalDown':
            self.MET         = event.MET_T1_pt_jesTotalDown
            self.MET_phi     = event.MET_T1_phi_jesTotalDown
            self.MET_chs     = event.MET_T1_pt_jesTotalDown
            self.MET_chs_phi = event.MET_T1_phi_jesTotalDown
        elif self.JECvar=='jesTotalUp':   
            self.MET         = event.MET_T1_pt_jesTotalUp
            self.MET_phi     = event.MET_T1_phi_jesTotalUp
            self.MET_chs     = event.MET_T1_pt_jesTotalUp
            self.MET_chs_phi = event.MET_T1_phi_jesTotalUp
        
        self.collinear_mass        = self.vis_mass/np.sqrt((self.vistau1_pt/(self.vistau1_pt+self.MET))*(self.vistau2_pt/(self.vistau2_pt+self.MET)))
        self.collinear_mass_chs    = self.vis_mass/np.sqrt((self.vistau1_pt/(self.vistau1_pt+self.MET_chs))*(self.vistau2_pt/(self.vistau2_pt+self.MET_chs)))
        
        ######## jet selection   ########

        jet_list_tcut = []
        jet_btag_loose_list_tcut = []
        jet_btag_medium_list_tcut = []
        jet_btag_tight_list_tcut = []
        
        jet_list = []
        jet_forward_list = []
        jet_btag_loose_list = []
        jet_btag_medium_list = []
        jet_btag_tight_list = []
        
        jet_btag_loose_excl_list = []
        jet_btag_medium_excl_list = []

        jets = Collection(event, "Jet")
        btag_wp = self.btagToolWP.getWP() #get b-tag wp from BtagTool
        wp_loose = btag_wp[0]
        wp_medium = btag_wp[1]
        wp_tight = btag_wp[2]

        for i,jet in enumerate(jets):
            if self.JECvar=='jesTotalDown':
                jet.pt = event.Jet_pt_jesTotalDown[i]
                jet.mass = event.Jet_mass_jesTotalDown[i]
            elif self.JECvar=='jesTotalUp':
                jet.pt = event.Jet_pt_jesTotalUp[i]
                jet.mass = event.Jet_mass_jesTotalUp[i]
            if abs(jet.eta) < 2.4 and jet.pt > 20. and jet.jetId >= 2:
                if self.vec(jet).DeltaR(self.vec(pair[0])) > 0.4:
                    if self.vec(jet).DeltaR(self.vec(pair[1])) > 0.4:
                        jet_list.append(jet)
                        if jet.btagDeepFlavB > wp_tight:
                            jet_btag_tight_list.append(jet)
                        if jet.btagDeepFlavB > wp_medium:
                            jet_btag_medium_list.append(jet)
                        if jet.btagDeepFlavB > wp_loose:
                            jet_btag_loose_list.append(jet)
                        # make exclusive lists
                        if wp_medium > jet.btagDeepFlavB > wp_loose:
                            jet_btag_loose_excl_list.append(jet)
                        elif wp_tight > jet.btagDeepFlavB > wp_medium:
                            jet_btag_medium_excl_list.append(jet)
            elif abs(jet.eta) > 2.4 and jet.pt > 20. and jet.jetId >=2:
                if self.vec(jet).DeltaR(self.vec(pair[0])) > 0.4 and self.vec(jet).DeltaR(self.vec(pair[1])) > 0.4:
                    jet_forward_list.append(jet)
            if abs(jet.eta) < 2.4 and jet.pt > 30. and jet.jetId >= 2:   #has to be if!
                if self.vec(jet).DeltaR(self.vec(pair[0])) > 0.4:
                    if self.vec(jet).DeltaR(self.vec(pair[1])) > 0.4:
                        jet_list_tcut.append(jet)
                        if jet.btagDeepFlavB > wp_tight:
                            jet_btag_tight_list_tcut.append(jet)
                        if jet.btagDeepFlavB > wp_medium:
                            jet_btag_medium_list_tcut.append(jet)
                        if jet.btagDeepFlavB > wp_loose:
                            jet_btag_loose_list_tcut.append(jet)
        
        if len(jet_forward_list)>1.:
            self.DEta_jets_forward = abs(jet_forward_list[0].eta-jet_forward_list[1].eta)
          
        self.nJets = len(jet_list)
        self.nJets_forward = len(jet_forward_list)
        self.nBjets_l = len(jet_btag_loose_list)
        self.nBjets_m = len(jet_btag_medium_list)
        self.nBjets_t = len(jet_btag_tight_list)
        self.nBjets_l_excl = len(jet_btag_loose_excl_list)
        self.nBjets_m_excl = len(jet_btag_medium_excl_list)

        #MC Corrections
        if self.isMC:
         if "DY" in self.sample:
             genV                     = getGenV(event,pair[0],pair[1])
             self.wt_dy_old           = self.MCCorrection.getWeight(genV.Pt(),genV.M())
             self.wt_dy               = self.MCCorrection.getWeight_btag(genV.Pt(),genV.M(),self.nBjets_m)
             self.wt_dy_reco          = self.MCCorrection.getWeight(self.vis_pt,self.vis_mass)
        if "TT" in self.sample:
            genV                     = getGenV(event,pair[0],pair[1])
            self.wt_tt = self.MCCorrection.getWeight_tt()
            self.wt_tt_pol1 = self.MCCorrection.getWeight_tt_pol1(genV.Pt())
            self.wt_tt_pol2 = self.MCCorrection.getWeight_tt_pol2(genV.Pt())
        if "WJets" in self.sample_name and "amcatnloFXFX" in self.sample_name:
            self.wt_w = self.MCCorrection.getWeight_w(isMuTau,isETau,self.Tau1_pt)

    
        #btag scale factors
        if self.isMC:
            self.btagTool.fillEfficiencies(jet_list)
            self.BTagWeightCorr = self.btagTool.getSFcorr(self.sample_name,isMuTau,isETau,self.isTTCR,self.isMuMu)
            self.BTagWeight = self.btagTool.getWeight(jet_list,'shape','central',self.sample_name,isMuTau,isETau,self.isTTCR,self.isMuMu)
            self.BTagWeight_nocorr = self.btagTool.getWeight_nocorr(jet_list,'shape','central') #needed to derive the norm correction for shape SF
            self.BTagWeight_comb  = self.btagTool.getWeight(jet_list,'comb_incl','central',self.sample_name,isMuTau,isETau,self.isTTCR,self.isMuMu)
            self.BTagWeight_combUp  = self.btagTool.getWeight(jet_list,'comb_incl','up',self.sample_name,isMuTau,isETau,self.isTTCR,self.isMuMu)
            self.BTagWeight_combDown  = self.btagTool.getWeight(jet_list,'comb_incl','down',self.sample_name,isMuTau,isETau,self.isTTCR,self.isMuMu)
            self.BTagWeight_jesUp  = self.btagTool.getWeight(jet_list,'shape','up_jes',self.sample_name,isMuTau,isETau,self.isTTCR,self.isMuMu)
            self.BTagWeight_jesDown  = self.btagTool.getWeight(jet_list,'shape','down_jes',self.sample_name,isMuTau,isETau,self.isTTCR,self.isMuMu)
            self.BTagWeight_lfUp  = self.btagTool.getWeight(jet_list,'shape','up_lf',self.sample_name,isMuTau,isETau,self.isTTCR,self.isMuMu)
            self.BTagWeight_lfDown  = self.btagTool.getWeight(jet_list,'shape','down_lf',self.sample_name,isMuTau,isETau,self.isTTCR,self.isMuMu)
            self.BTagWeight_hfUp  = self.btagTool.getWeight(jet_list,'shape','up_hf',self.sample_name,isMuTau,isETau,self.isTTCR,self.isMuMu)
            self.BTagWeight_hfDown  = self.btagTool.getWeight(jet_list,'shape','down_hf',self.sample_name,isMuTau,isETau,self.isTTCR,self.isMuMu)
            self.BTagWeight_hfstats1Up  = self.btagTool.getWeight(jet_list,'shape','up_hfstats1',self.sample_name,isMuTau,isETau,self.isTTCR,self.isMuMu)
            self.BTagWeight_hfstats1Down  = self.btagTool.getWeight(jet_list,'shape','down_hfstats1',self.sample_name,isMuTau,isETau,self.isTTCR,self.isMuMu)
            self.BTagWeight_hfstats2Up  = self.btagTool.getWeight(jet_list,'shape','up_hfstats2',self.sample_name,isMuTau,isETau,self.isTTCR,self.isMuMu)
            self.BTagWeight_hfstats2Down  = self.btagTool.getWeight(jet_list,'shape','down_hfstats2',self.sample_name,isMuTau,isETau,self.isTTCR,self.isMuMu)
            self.BTagWeight_lfstats1Up  = self.btagTool.getWeight(jet_list,'shape','up_lfstats1',self.sample_name,isMuTau,isETau,self.isTTCR,self.isMuMu)
            self.BTagWeight_lfstats1Down  = self.btagTool.getWeight(jet_list,'shape','down_lfstats1',self.sample_name,isMuTau,isETau,self.isTTCR,self.isMuMu)
            self.BTagWeight_lfstats2Up  = self.btagTool.getWeight(jet_list,'shape','up_lfstats2',self.sample_name,isMuTau,isETau,self.isTTCR,self.isMuMu)
            self.BTagWeight_lfstats2Down  = self.btagTool.getWeight(jet_list,'shape','down_lfstats2',self.sample_name,isMuTau,isETau,self.isTTCR,self.isMuMu)
            self.BTagWeight_cferr1Up  = self.btagTool.getWeight(jet_list,'shape','up_cferr1',self.sample_name,isMuTau,isETau,self.isTTCR,self.isMuMu)
            self.BTagWeight_cferr1Down  = self.btagTool.getWeight(jet_list,'shape','down_cferr1',self.sample_name,isMuTau,isETau,self.isTTCR,self.isMuMu)
            self.BTagWeight_cferr2Up  = self.btagTool.getWeight(jet_list,'shape','up_cferr2',self.sample_name,isMuTau,isETau,self.isTTCR,self.isMuMu)
            self.BTagWeight_cferr2Down  = self.btagTool.getWeight(jet_list,'shape','down_cferr2',self.sample_name,isMuTau,isETau,self.isTTCR,self.isMuMu)
        self.nJets_tcut = len(jet_list_tcut)
        self.nBjets_l_tcut = len(jet_btag_loose_list_tcut)
        self.nBjets_m_tcut = len(jet_btag_medium_list_tcut)
        self.nBjets_t_tcut = len(jet_btag_tight_list_tcut)

        jet_list.sort(key=lambda x: x.btagDeepFlavB,reverse=True)
        
        
        if len(jet_list) > 0:
            jet1 = jet_list[0]
            self.Jet1_pt = jet1.pt
            self.Jet1_eta = jet1.eta
            self.Jet1_phi = jet1.phi
            self.Jet1_mass = jet1.mass
            self.Jet1_btag = jet1.btagDeepFlavB
            jet1_tlv = self.tlv(jet1)
            if self.isMC:
                self.Jet1_hadronFlavour = jet1.hadronFlavour
        if len(jet_list) > 1:
            jet2 = jet_list[1]
            self.Jet2_pt = jet2.pt
            self.Jet2_eta = jet2.eta
            self.Jet2_phi = jet2.phi
            self.Jet2_mass = jet2.mass
            self.Jet2_btag = jet2.btagDeepFlavB
            jet2_tlv = self.tlv(jet2)
            if self.isMC:
                self.Jet2_hadronFlavour = jet2.hadronFlavour
            dijet_tlv = jet1_tlv + jet2_tlv
            self.dijet_pt = dijet_tlv.Pt()
            self.dijet_phi = dijet_tlv.Phi()
            self.dijet_eta = dijet_tlv.Eta()
            self.dijet_mass = dijet_tlv.M()
            self.DEta_jets = abs(jet1_tlv.Eta()-jet2_tlv.Eta())
            self.DPhi_jets = jet1_tlv.DeltaPhi(jet2_tlv)
            self.DRjets = jet1_tlv.DeltaR(jet2_tlv)
        if len(jet_list) > 2:
            jet3 = jet_list[2]
            self.Jet3_pt = jet3.pt
            self.Jet3_eta = jet3.eta
            self.Jet3_phi = jet3.phi
            self.Jet3_mass = jet3.mass
            self.Jet3_btag = jet3.btagDeepFlavB   
            if self.isMC:
                self.Jet3_hadronFlavour = jet3.hadronFlavour

        if len(jet_btag_medium_list) > 0:
            bjet1 = jet_btag_medium_list[0]
            self.Bjet1_pt = bjet1.pt
            self.Bjet1_eta = bjet1.eta
            self.Bjet1_phi = bjet1.phi
            self.Bjet1_mass = bjet1.mass
            Bjet1_tlv = self.tlv(bjet1)
        if len(jet_btag_medium_list) > 1:
            bjet2 = jet_btag_medium_list[1]
            self.Bjet2_pt = bjet2.pt
            self.Bjet2_eta = bjet2.eta
            self.Bjet2_phi = bjet2.phi
            self.Bjet2_mass = bjet2.mass
            Bjet2_tlv = self.tlv(bjet2)
            self.Bjets_pt = (Bjet1_tlv+Bjet2_tlv).Pt()
            self.DRBjets = Bjet1_tlv.DeltaR(Bjet2_tlv)
            self.DEta_Bjets = abs(Bjet1_tlv.Eta()-Bjet2_tlv.Eta())
            self.DPhi_Bjets = Bjet1_tlv.DeltaPhi(Bjet2_tlv)
        
        if len(jet_btag_medium_list)>0 and len(jet_btag_loose_excl_list)>0:
            Bjet_m_tlv = self.tlv(jet_btag_medium_list[0])
            Bjet_l_tlv = self.tlv(jet_btag_loose_excl_list[0])
            self.DRBjets_lm = Bjet_m_tlv.DeltaR(Bjet_l_tlv)
        if len(jet_btag_tight_list)>0 and len(jet_btag_medium_excl_list)>0:
            Bjet_t_tlv = self.tlv(jet_btag_tight_list[0])
            Bjet_m_tlv = self.tlv(jet_btag_medium_excl_list[0])
            self.DRBjets_mt = Bjet_t_tlv.DeltaR(Bjet_m_tlv)

        

        if isMuTau or isETau:
            if len(jet_list)>0:
                jet1_tlv = self.tlv(jet_list[0])
                HJ_tlv = H_tlv + jet1_tlv
                self.HJ_mass = HJ_tlv.M()
                self.HJ_pt = HJ_tlv.Pt()
                self.DRHJ = H_tlv.DeltaR(jet1_tlv)
                self.DEtaHJ = abs(H_tlv.Eta()-jet1_tlv.Eta())
                self.DPhiHJ = H_tlv.DeltaPhi(jet1_tlv)
            if len(jet_list)>1:
                jet2_tlv = self.tlv(jet_list[1])
                HJ2_tlv = H_tlv + jet2_tlv
                self.HJ2_mass = HJ2_tlv.M()
                self.HJ2_pt = HJ2_tlv.Pt()
                self.DRHJ2 = H_tlv.DeltaR(jet2_tlv)
                self.DEtaHJ2 = abs(H_tlv.Eta()-jet2_tlv.Eta())
                self.DPhiHJ2 = H_tlv.DeltaPhi(jet2_tlv)
            
            # adding variables for BDT
            lep_tlv = self.tlv(pair[0])
            tau_tlv = self.tlv(pair[1])
            met_tlv = TLorentzVector()
            met_tlv.SetPtEtaPhiM(self.MET,0.,self.MET_phi,0.)
            lepmet_tlv = lep_tlv+met_tlv
            self.transverse_mass_lepmet  = self.mass_t(lep_tlv,met_tlv)
            self.transverse_mass_taumet= self.mass_t(tau_tlv,met_tlv)
            self.transverse_mass_leptau = self.mass_t(lep_tlv,tau_tlv)
            self.transverse_mass_total = np.sqrt(self.transverse_mass_lepmet**2+self.transverse_mass_taumet**2+self.transverse_mass_leptau**2)
            self.DPhi                  = lep_tlv.DeltaPhi(tau_tlv)
            self.DEta                  = abs(lep_tlv.Eta()-tau_tlv.Eta())
            self.Dzeta                 = Dzeta(lep_tlv,tau_tlv,met_tlv,1.85)
            self.mt2                   = computeMT2(lep_tlv,tau_tlv,met_tlv)
            self.vistauMET_pt          = (tau_tlv+lep_tlv+met_tlv).Pt()
            self.DPhiLepMET = lep_tlv.DeltaPhi(met_tlv)
            self.DRLepMET = lep_tlv.DeltaR(met_tlv)
            if len(jet_list)>0:
                jet1_tlv = self.tlv(jet_list[0])
                self.LepJ_mass = (lep_tlv + jet1_tlv).M()
                self.TauJ_mass = (tau_tlv + jet1_tlv).M()
                self.vistauJ_mass = (tau_tlv + lep_tlv + jet1_tlv).M()
                self.vistauJMET_mass = (tau_tlv + lep_tlv + jet1_tlv + met_tlv).Mt()
                self.TauJMET_mass = (tau_tlv + jet1_tlv + met_tlv).Mt()
                self.LepJMET_mass = (lep_tlv + jet1_tlv + met_tlv).Mt()
                self.METJ_mass = (jet1_tlv + met_tlv).Mt()
                self.LepJ_pt = (lep_tlv + jet1_tlv).Pt()
                self.TauJ_pt = (tau_tlv + jet1_tlv).Pt()
                self.vistauJ_pt = (tau_tlv + lep_tlv + jet1_tlv).Pt()
                self.vistauJMET_pt = (tau_tlv + lep_tlv + jet1_tlv + met_tlv).Pt()
                self.TauJMET_pt = (tau_tlv + jet1_tlv + met_tlv).Pt()
                self.LepJMET_pt = (lep_tlv + jet1_tlv + met_tlv).Pt()
                self.METJ_pt = (jet1_tlv + met_tlv).Pt()
                self.DRTauJ = tau_tlv.DeltaR(jet1_tlv) 
                self.DEtaTauJ = abs(tau_tlv.Eta()-jet1_tlv.Eta())
                self.DPhiTauJ = tau_tlv.DeltaPhi(jet1_tlv)
                self.DRLepJ = lep_tlv.DeltaR(jet1_tlv) 
                self.DEtaLepJ = abs(lep_tlv.Eta()-jet1_tlv.Eta())
                self.DPhiLepJ = lep_tlv.DeltaPhi(jet1_tlv)
            if len(jet_list)>1:
                jet2_tlv = self.tlv(jet_list[1])
                self.Taudijet_mass = (tau_tlv + jet1_tlv + jet2_tlv).M()
                self.DRTauJ2 = tau_tlv.DeltaR(jet2_tlv) 
                self.DEtaTauJ2 = abs(tau_tlv.Eta()-jet2_tlv.Eta())
                self.DPhiTauJ2 = tau_tlv.DeltaPhi(jet2_tlv)
                self.DRLepJ2 = lep_tlv.DeltaR(jet2_tlv) 
                self.DEtaLepJ2 = abs(lep_tlv.Eta()-jet2_tlv.Eta())
                self.DPhiLepJ2 = lep_tlv.DeltaPhi(jet2_tlv)
        #derive fakefactors
        if isMuTau:
            wt_ff_list = self.ff.ffweight_corr(self.Tau1_pt, self.H_mass, self.Jet1_pt, self.collinear_mass, self.TauJ_mass,self.Tau1_decaymode,"mutau")
            self.wt_ff = wt_ff_list[0][0]
            self.wt_ffUp = wt_ff_list[0][1]
            self.wt_ffDown = wt_ff_list[0][2]
            self.wt_ff_qcdUp = wt_ff_list[1][0]
            self.wt_ff_qcdDown = wt_ff_list[1][1]
            self.wt_ff_wUp = wt_ff_list[1][2]
            self.wt_ff_wDown = wt_ff_list[1][3]
            self.wt_ff_ttUp = wt_ff_list[1][4]
            self.wt_ff_ttDown = wt_ff_list[1][5]
            self.wt_ff_qcdfitpar1Up = wt_ff_list[2][0][0]
            self.wt_ff_qcdfitpar1Down = wt_ff_list[2][0][1]
            self.wt_ff_qcdfitpar2Up = wt_ff_list[2][0][2]
            self.wt_ff_qcdfitpar2Down = wt_ff_list[2][0][3]
            self.wt_ff_wfitpar1Up = wt_ff_list[2][1][0]
            self.wt_ff_wfitpar1Down = wt_ff_list[2][1][1]
            self.wt_ff_wfitpar2Up = wt_ff_list[2][1][2]
            self.wt_ff_wfitpar2Down = wt_ff_list[2][1][3]
            self.wt_ff_wfitpar3Up = wt_ff_list[2][1][4]
            self.wt_ff_wfitpar3Down = wt_ff_list[2][1][5]
            self.wt_ff_wfitpar4Up = wt_ff_list[2][1][6]
            self.wt_ff_wfitpar4Down = wt_ff_list[2][1][7]
            self.wt_ff_ttfitpar1Up = wt_ff_list[2][2][0]
            self.wt_ff_ttfitpar1Down = wt_ff_list[2][2][1]
            self.wt_ff_ttfitpar2Up = wt_ff_list[2][2][2]
            self.wt_ff_ttfitpar2Down = wt_ff_list[2][2][3]
            wt_ff_nocorr_list = self.ff.ffweight(self.Tau1_pt,self.Tau1_decaymode,"mutau")
            self.wt_ff_nocorr = wt_ff_nocorr_list[0]
            self.wt_ff_nocorr_up = wt_ff_nocorr_list[1]
            self.wt_ff_nocorr_down = wt_ff_nocorr_list[2]
            #self.wt_ff_norm = self.ff.ffweight_norm(self.Tau1_pt,self.Tau1_decaymode,"mutau")
            self.wt_ff_ttdr = self.ff.ffweight_ttdr(self.Tau1_pt,self.Tau1_decaymode,"mutau")
            self.wt_ff_qcddr = self.ff.ffweight_qcddr(self.Tau1_pt, self.H_mass, self.Jet1_pt, self.collinear_mass, self.TauJ_mass,self.Tau1_decaymode,"mutau")
            ffweight_sep = self.ff.ffweight_sep(self.Tau1_pt,self.Tau1_decaymode,"mutau")
            self.wt_ff_qcd = ffweight_sep[0]
            self.wt_ff_w = ffweight_sep[1]
            self.wt_ff_tt = ffweight_sep[2]
            self.wt_ff_qcd_old = ffweight_sep[3]
            self.wt_ff_w_old = ffweight_sep[4]
            self.wt_ff_tt_old = ffweight_sep[5]
            self.wt_ffcorr_hmass_qcd = self.ff.ffweightcorr_hmass(self.H_mass,self.Tau1_decaymode,"mutau")
            self.wt_ffcorr_jetpt_qcd = self.ff.ffweightcorr_jetpt(self.Jet1_pt,self.Tau1_decaymode,"mutau")
            self.wt_ffcorr_collinearmass_qcd = self.ff.ffweightcorr_collinearmass(self.collinear_mass,self.Tau1_decaymode,"mutau")
            self.wt_ffcorr_taujmass_qcd = self.ff.ffweightcorr_taujmass(self.TauJ_mass,self.Tau1_decaymode,"mutau")
            ffuncertainties = self.ffunc.ffuncertainty(self.Tau1_pt,self.Tau1_decaymode,"mutau")
            self.ffunc_qcd = ffuncertainties[0]
            self.ffunc_w = ffuncertainties[1]
            self.ffunc_tt = ffuncertainties[2]
            ff_fitunc = self.ffunc.ff_fitunc(self.Tau1_decaymode,"mutau")
            self.ff_fitunc_qcd_par1 = ff_fitunc[0][0]
            self.ff_fitunc_qcd_par2 = ff_fitunc[0][1]
            self.ff_fitunc_w_par1 = ff_fitunc[1][0]
            self.ff_fitunc_w_par2 = ff_fitunc[1][1]
            self.ff_fitunc_w_par3 = ff_fitunc[1][2]
            self.ff_fitunc_w_par4 = ff_fitunc[1][3]
            self.ff_fitunc_tt_par1 = ff_fitunc[2][0]
            self.ff_fitunc_tt_par2 = ff_fitunc[2][1]
        elif isETau:
            wt_ff_list = self.ff.ffweight_corr(self.Tau1_pt, self.H_mass, self.Jet1_pt, self.collinear_mass, self.TauJ_mass,self.Tau1_decaymode,"etau")
            self.wt_ff = wt_ff_list[0][0]
            self.wt_ffUp = wt_ff_list[0][1]
            self.wt_ffDown = wt_ff_list[0][2]
            self.wt_ff_qcdUp = wt_ff_list[1][0]
            self.wt_ff_qcdDown = wt_ff_list[1][1]
            self.wt_ff_wUp = wt_ff_list[1][2]
            self.wt_ff_wDown = wt_ff_list[1][3]
            self.wt_ff_ttUp = wt_ff_list[1][4]
            self.wt_ff_ttDown = wt_ff_list[1][5]
            self.wt_ff_qcdfitpar1Up = wt_ff_list[2][0][0]
            self.wt_ff_qcdfitpar1Down = wt_ff_list[2][0][1]
            self.wt_ff_qcdfitpar2Up = wt_ff_list[2][0][2]
            self.wt_ff_qcdfitpar2Down = wt_ff_list[2][0][3]
            self.wt_ff_wfitpar1Up = wt_ff_list[2][1][0]
            self.wt_ff_wfitpar1Down = wt_ff_list[2][1][1]
            self.wt_ff_wfitpar2Up = wt_ff_list[2][1][2]
            self.wt_ff_wfitpar2Down = wt_ff_list[2][1][3]
            self.wt_ff_wfitpar3Up = wt_ff_list[2][1][4]
            self.wt_ff_wfitpar3Down = wt_ff_list[2][1][5]
            self.wt_ff_wfitpar4Up = wt_ff_list[2][1][6]
            self.wt_ff_wfitpar4Down = wt_ff_list[2][1][7]
            self.wt_ff_ttfitpar1Up = wt_ff_list[2][2][0]
            self.wt_ff_ttfitpar1Down = wt_ff_list[2][2][1]
            self.wt_ff_ttfitpar2Up = wt_ff_list[2][2][2]
            self.wt_ff_ttfitpar2Down = wt_ff_list[2][2][3]
            wt_ff_nocorr_list = self.ff.ffweight(self.Tau1_pt,self.Tau1_decaymode,"etau")
            self.wt_ff_nocorr = wt_ff_nocorr_list[0]
            self.wt_ff_nocorr_up = wt_ff_nocorr_list[1]
            self.wt_ff_nocorr_down = wt_ff_nocorr_list[2]
            self.wt_ff_ttdr = self.ff.ffweight_ttdr(self.Tau1_pt,self.Tau1_decaymode,"etau")
            self.wt_ff_qcddr = self.ff.ffweight_qcddr(self.Tau1_pt, self.H_mass, self.Jet1_pt, self.collinear_mass, self.TauJ_mass,self.Tau1_decaymode,"etau")
            ffweight_sep = self.ff.ffweight_sep(self.Tau1_pt,self.Tau1_decaymode,"etau")
            self.wt_ff_qcd = ffweight_sep[0]
            self.wt_ff_w = ffweight_sep[1]
            self.wt_ff_tt = ffweight_sep[2]
            self.wt_ff_qcd_old = ffweight_sep[3]
            self.wt_ff_w_old = ffweight_sep[4]
            self.wt_ff_tt_old = ffweight_sep[5]
            self.wt_ffcorr_hmass_qcd = self.ff.ffweightcorr_hmass(self.H_mass,self.Tau1_decaymode,"etau")
            self.wt_ffcorr_jetpt_qcd = self.ff.ffweightcorr_jetpt(self.Jet1_pt,self.Tau1_decaymode,"etau")
            self.wt_ffcorr_collinearmass_qcd = self.ff.ffweightcorr_collinearmass(self.collinear_mass,self.Tau1_decaymode,"etau")
            self.wt_ffcorr_taujmass_qcd = self.ff.ffweightcorr_taujmass(self.TauJ_mass,self.Tau1_decaymode,"etau")
            ffuncertainties = self.ffunc.ffuncertainty(self.Tau1_pt,self.Tau1_decaymode,"etau")
            self.ffunc_qcd = ffuncertainties[0]
            self.ffunc_w = ffuncertainties[1]
            self.ffunc_tt = ffuncertainties[2]
            ff_fitunc = self.ffunc.ff_fitunc(self.Tau1_decaymode,"etau")
            self.ff_fitunc_qcd_par1 = ff_fitunc[0][0]
            self.ff_fitunc_qcd_par2 = ff_fitunc[0][1]
            self.ff_fitunc_w_par1 = ff_fitunc[1][0]
            self.ff_fitunc_w_par2 = ff_fitunc[1][1]
            self.ff_fitunc_w_par3 = ff_fitunc[1][2]
            self.ff_fitunc_w_par4 = ff_fitunc[1][3]
            self.ff_fitunc_tt_par1 = ff_fitunc[2][0]
            self.ff_fitunc_tt_par2 = ff_fitunc[2][1]
        self.fillBranches(event)
        return True
        
        
