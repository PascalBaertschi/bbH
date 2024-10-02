import ROOT
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection,Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

from TreeProducer import *
from TreeProducerCommon import *
from CorrectionTools.PileupWeightTool import *
from CorrectionTools.BTaggingTool import BTagWeightTool, BTagWPs
from CorrectionTools.TauSFs import *
from CorrectionTools.MuonSFs import *
from CorrectionTools.ElectronSFs import *
from CorrectionTools.RecoilCorrectionTool import getTTptWeight, getTTPt
from CorrectionTools.TrigObjMatcher import loadTriggerDataFromJSON, TrigObjMatcher
from CorrectionTools.DYCorrection import *
from CorrectionTools.fakefactor import ffclass
from CorrectionTools.ffunc import ffuncclass
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
        self.data_era = None

        if DataType=='data':
            self.isData = True
            self.isMC = False
            self.data_era = self.sample[self.sample.find("Run")+7]
        else:
            self.isData = False
            self.isMC = True

        fffile = ROOT.TFile.Open("CorrectionTools/fakefactor/root/fakefactors_ws_mt_lite_2018.root") 
        self.ffws = fffile.Get("w")
        fffile.Close()
        self.ff_functor_obj = self.ffws.function("ff_mt_medium_dmbins").functor(ROOT.RooArgList(self.ffws.argSet("pt,dm,njets,m_pt,os,m_iso,pass_single,met_var_qcd,met_var_w,WpT,mt")))

        
        ROOT.gSystem.Load('$CMSSW_BASE/lib/$SCRAM_ARCH/libTauAnalysisNanoToolsInterface.so')
        ROOT.gROOT.ProcessLine('#include "TauAnalysis/NanoToolsInterface/interface/InterfaceFastMTT.h"')
        self.mysvinterface = ROOT.InterfaceFastMTT()
        self.year           = kwargs.get('year',     2018 )
        self.ULtag          = kwargs.get('ULtag',    "" )
        self.preVFP         = kwargs.get('preVFP', "")
        self.tes            = kwargs.get('tes',      1.0  )
        self.ltf            = kwargs.get('ltf',      1.0  )
        self.jtf            = kwargs.get('jtf',      1.0 )
        self.calcSVFit      = kwargs.get('doSVFit')
        year                = self.year
        self.METfilter         = getMETFilters(year,self.ULtag,self.isData)
        self.ffunc = ffuncclass(year)
        self.ff = ffclass(year)
        if "madgraphMLM" in self.sample_name:
            self.DYCorrection = DYCorrection(self.year,"LO")
        elif "amcatnloFXFX" in self.sample_name:
            self.DYCorrection = DYCorrection(self.year,"NLO")
        ##### Trigger ####
        jsonfile        = "CorrectionTools/triggers/tau_triggers_%d.json"%self.year
        trigdata        = loadTriggerDataFromJSON(jsonfile,isData=self.isData)
        self.trigger_Mu = TrigObjMatcher(trigdata.combdict['SingleMuon'])
        self.trigger_MuTau    = TrigObjMatcher(trigdata.combdict['mutau'])
        self.trigger_E = TrigObjMatcher(trigdata.combdict['SingleElectron'])
        self.trigger_ETau = TrigObjMatcher(trigdata.combdict['etau'])

        self.count_genJet_pos = 0
        self.count_genJet_neg = 0
        ##################
        self.LumiWeight = 1. #for data
        if self.isMC:
            self.btagTool = BTagWeightTool('DeepJet','medium','central','mutau',self.year,self.ULtag, self.preVFP)
            self.btagTool_up = BTagWeightTool('DeepJet','medium','up','mutau',self.year,self.ULtag, self.preVFP)
            self.btagTool_down = BTagWeightTool('DeepJet','medium','down','mutau',self.year,self.ULtag, self.preVFP)
            self.muSFs   = MuonSFs(self.year,self.ULtag, self.preVFP)
            self.eSFs    = ElectronSFs(self.year,self.ULtag, self.preVFP)
            self.tauSFs  = TauSFs(self.year,self.ULtag,self.preVFP)
            if self.year==2018:
                LUMI = 59740
            elif self.year==2017:
                LUMI = 41530
            elif self.year==2016:
                if self.preVFP=="_preVFP":
                    LUMI = 19500
                else:
                    LUMI = 16800
                    if "bbHToTauTau_M-125" in self.sample_name or "jjHToTauTau_M-125" in self.sample_name:
                        print "taking LUMI of preVFP and postVFP combined!"
                        print "change as soon as preVFP available!"
                        LUMI = 19500+16800

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
        self.out.BTagWeight[0]              = self.BTagWeight
        self.out.BTagWeight_up[0]           = self.BTagWeight_up
        self.out.BTagWeight_down[0]         = self.BTagWeight_down
        self.out.GenWeight[0]               = self.GenWeight
        self.out.PUWeight[0]                = self.PUWeight
        self.out.MuWeight[0]                = self.MuWeight
        self.out.MuWeight_up[0]             = self.MuWeight_up
        self.out.MuWeight_down[0]           = self.MuWeight_down
        self.out.MuTriggerWeight[0]         = self.MuTriggerWeight
        self.out.MuTriggerWeight_up[0]      = self.MuTriggerWeight_up
        self.out.MuTriggerWeight_down[0]    = self.MuTriggerWeight_down
        self.out.EWeight[0]                 = self.EWeight
        self.out.EWeight_up[0]              = self.EWeight_up
        self.out.EWeight_down[0]            = self.EWeight_down
        self.out.ETriggerWeight[0]          = self.ETriggerWeight
        self.out.ETriggerWeight_up[0]       = self.ETriggerWeight_up
        self.out.ETriggerWeight_down[0]     = self.ETriggerWeight_down
        self.out.TauWeight[0]               = self.TauWeight
        self.out.TauWeight_up[0]            = self.TauWeight_up
        self.out.TauWeight_down[0]          = self.TauWeight_down
        self.out.TauTriggerWeight[0]        = self.TauTriggerWeight
        self.out.TauTriggerWeight_up[0]     = self.TauTriggerWeight_up
        self.out.TauTriggerWeight_down[0]   = self.TauTriggerWeight_down
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
        self.out.Jet2_pt[0]                 = self.Jet2_pt
        self.out.Jet2_eta[0]                = self.Jet2_eta
        self.out.Jet2_phi[0]                = self.Jet2_phi
        self.out.Jet2_mass[0]               = self.Jet2_mass
        self.out.Jet2_btag[0]               = self.Jet2_btag
        self.out.Jet3_pt[0]                 = self.Jet3_pt
        self.out.Jet3_eta[0]                = self.Jet3_eta
        self.out.Jet3_phi[0]                = self.Jet3_phi
        self.out.Jet3_mass[0]               = self.Jet3_mass
        self.out.Jet3_btag[0]               = self.Jet3_btag
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
        self.out.Tau2_pt[0]                 = self.Tau2_pt
        self.out.Tau2_eta[0]                = self.Tau2_eta
        self.out.Tau2_phi[0]                = self.Tau2_phi
        self.out.Tau2_mass[0]               = self.Tau2_mass
        self.out.Tau2_charge[0]             = self.Tau2_charge
        self.out.Tau2_iso[0]                = self.Tau2_iso
        self.out.Tau2_genmatch[0]           = self.Tau2_genmatch
        self.out.H_pt[0]                    = self.H_pt
        self.out.H_eta[0]                   = self.H_eta
        self.out.H_phi[0]                   = self.H_phi
        self.out.H_mass[0]                  = self.H_mass
        self.out.vis_pt[0]                  = self.vis_pt
        self.out.vis_eta[0]                 = self.vis_eta
        self.out.vis_phi[0]                 = self.vis_phi
        self.out.vis_mass[0]                = self.vis_mass
        self.out.mt2[0]                     = self.mt2
        self.out.MET[0]                     = event.PuppiMET_pt
        self.out.MET_phi[0]                 = event.PuppiMET_phi
        self.out.MET_chs[0]                 = event.MET_pt
        self.out.MET_chs_phi[0]             = event.MET_phi
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
        self.out.wt_ff_ttdr[0]              = self.wt_ff_ttdr
        self.out.wt_ff_qcddr[0]             = self.wt_ff_qcddr
        self.out.wt_ff_qcddr_old[0]         = self.wt_ff_qcddr_old
        self.out.wt_ff_qcd[0]               = self.wt_ff_qcd
        self.out.wt_ff_w[0]                 = self.wt_ff_w
        self.out.wt_ff_tt[0]                = self.wt_ff_tt
        self.out.wt_ff_qcd_old[0]           = self.wt_ff_qcd_old
        self.out.wt_ff_w_old[0]             = self.wt_ff_w_old
        self.out.wt_ff_tt_old[0]            = self.wt_ff_tt_old
        self.out.wt_ff_old[0]               = self.wt_ff_old
        self.out.wt_ffcorr_leppt_qcd[0]     = self.wt_ffcorr_leppt_qcd
        self.out.wt_ffcorr_leppt_tt[0]      = self.wt_ffcorr_leppt_tt
        self.out.wt_ffcorr_leppt_w[0]       = self.wt_ffcorr_leppt_w
        self.out.wt_ffcorr_hmass_qcd[0]     = self.wt_ffcorr_hmass_qcd
        self.out.wt_ffcorr_hmass_tt[0]      = self.wt_ffcorr_hmass_tt
        self.out.wt_ffcorr_hmass_w[0]       = self.wt_ffcorr_hmass_w
        self.out.wt_ffcorr_jetbtag_qcd[0]   = self.wt_ffcorr_jetbtag_qcd
        self.out.wt_ffcorr_jetbtag_tt[0]    = self.wt_ffcorr_jetbtag_tt
        self.out.wt_ffcorr_jetbtag_w[0]     = self.wt_ffcorr_jetbtag_w
        self.out.wt_ffcorr_jetpt_qcd[0]     = self.wt_ffcorr_jetpt_qcd
        self.out.wt_ffcorr_jetpt_tt[0]      = self.wt_ffcorr_jetpt_tt
        self.out.wt_ffcorr_jetpt_w[0]       = self.wt_ffcorr_jetpt_w
        self.out.wt_ffcorr_jet2pt_qcd[0]    = self.wt_ffcorr_jet2pt_qcd
        self.out.wt_ffcorr_jet2pt_tt[0]     = self.wt_ffcorr_jet2pt_tt
        self.out.wt_ffcorr_jet2pt_w[0]      = self.wt_ffcorr_jet2pt_w
        self.out.wt_ffcorr_met_qcd[0]       = self.wt_ffcorr_met_qcd
        self.out.wt_ffcorr_met_tt[0]        = self.wt_ffcorr_met_tt
        self.out.wt_ffcorr_met_w[0]         = self.wt_ffcorr_met_w
        self.out.wt_ff_up[0]                = self.wt_ff_up
        self.out.wt_ff_down[0]              = self.wt_ff_down
        self.out.wt_ff_up_qcd[0]            = self.wt_ff_up_qcd
        self.out.wt_ff_down_qcd[0]          = self.wt_ff_down_qcd
        self.out.wt_ff_up_w[0]              = self.wt_ff_up_w
        self.out.wt_ff_down_w[0]            = self.wt_ff_down_w
        self.out.wt_ff_up_tt[0]             = self.wt_ff_up_tt
        self.out.wt_ff_down_tt[0]           = self.wt_ff_down_tt
        self.out.wt_dy[0]                   = self.wt_dy
        self.out.wt_dy_reco[0]              = self.wt_dy_reco
        self.out.wt_dy_nlo[0]               = self.wt_dy_nlo
        self.out.wt_tt[0]                   = self.wt_tt
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
        self.out.ff_fitunc_tt_par3[0]       = self.ff_fitunc_tt_par3
        self.out.ff_fitunc_tt_par4[0]       = self.ff_fitunc_tt_par4
        self.out.Dzeta[0]                   = self.Dzeta
        self.out.DPhi[0]                    = self.DPhi
        self.out.DEta[0]                    = self.DEta
        self.out.DEta_jets_forward[0]       = self.DEta_jets_forward
        self.out.DPhiLepMET[0]              = self.DPhiLepMET
        self.out.DRLepMET[0]                = self.DRLepMET
        self.out.met_var_qcd[0]             = self.met_var_qcd
        self.out.met_var_w[0]               = self.met_var_w
        self.out.wpt[0]                     = self.wpt
        self.out.DRLepB[0]                  = self.DRLepB
        self.out.DEtaLepB[0]                = self.DEtaLepB
        self.out.DPhiLepB[0]                = self.DPhiLepB
        self.out.DRTauB[0]                  = self.DRTauB
        self.out.DEtaTauB[0]                = self.DEtaTauB
        self.out.DPhiTauB[0]                = self.DPhiTauB
        self.out.DRLepB2[0]                 = self.DRLepB2
        self.out.DEtaLepB2[0]               = self.DEtaLepB2
        self.out.DPhiLepB2[0]               = self.DPhiLepB2
        self.out.DRTauB2[0]                 = self.DRTauB2
        self.out.DEtaTauB2[0]               = self.DEtaTauB2
        self.out.DPhiTauB2[0]               = self.DPhiTauB2
        self.out.HB_mass[0]                 = self.HB_mass
        self.out.HB_pt[0]                   = self.HB_pt
        self.out.DRHB[0]                    = self.DRHB
        self.out.DEtaHB[0]                  = self.DEtaHB
        self.out.DPhiHB[0]                  = self.DPhiHB
        self.out.HB2_mass[0]                = self.HB2_mass
        self.out.HB2_pt[0]                  = self.HB2_pt
        self.out.DRHB2[0]                   = self.DRHB2
        self.out.DEtaHB2[0]                 = self.DEtaHB2
        self.out.DPhiHB2[0]                 = self.DPhiHB2
        self.out.LepB_mass[0]               = self.LepB_mass
        self.out.TauB_mass[0]               = self.TauB_mass
        self.out.TauBMET_mass[0]            = self.TauBMET_mass
        self.out.METB_mass[0]               = self.METB_mass
        self.out.vistauB_mass[0]            = self.vistauB_mass
        self.out.vistauBMET_mass[0]         = self.vistauBMET_mass
        self.out.LepBMET_mass[0]            = self.LepBMET_mass
        self.out.dijet_pt[0]                = self.dijet_pt
        self.out.dijet_eta[0]               = self.dijet_eta
        self.out.dijet_phi[0]               = self.dijet_phi
        self.out.dijet_mass[0]              = self.dijet_mass
        self.out.DRjets[0]                  = self.DRjets
        self.out.DEta_jets[0]               = self.DEta_jets
        self.out.DPhi_jets[0]               = self.DPhi_jets
        self.out.LepB_pt[0]                 = self.LepB_pt
        self.out.TauB_pt[0]                 = self.TauB_pt
        self.out.vistauB_pt[0]              = self.vistauB_pt
        self.out.vistauBMET_pt[0]           = self.vistauBMET_pt
        self.out.TauBMET_pt[0]              = self.TauBMET_pt
        self.out.LepBMET_pt[0]              = self.LepBMET_pt
        self.out.METB_pt[0]                 = self.METB_pt
        self.out.vistauMET_pt[0]            = self.vistauMET_pt
        self.out.LepJ_mass[0]               = self.LepJ_mass
        self.out.TauJ_mass[0]               = self.TauJ_mass
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
        self.out.tree.Fill()

    def vec(self,lepton):
        lepton_v = TVector3()
        lepton_v.SetPtEtaPhi(lepton.pt,lepton.eta,lepton.phi)
        return lepton_v

    def tlv(self,lepton):
        lepton_tlv = TLorentzVector()
        lepton_tlv.SetPtEtaPhiM(lepton.pt,lepton.eta,lepton.phi,lepton.mass)
        return lepton_tlv    

    def mass_t(self,par1vec,par2vec):
        return np.sqrt(2*par1vec.Pt()*par2vec.Pt()*(1-np.cos(par1vec.DeltaPhi(par2vec)))) 

    def iso(self, lepton):
        if hasattr(lepton,'pfRelIso04_all'):
            return lepton.pfRelIso04_all
        elif hasattr(lepton,'rawDeepTau2017v2p1VSjet'):
            return lepton.rawDeepTau2017v2p1VSjet
        elif hasattr(lepton,'pfRelIso03_all'):
            return lepton.pfRelIso03_all
        else:
            print("ERROR: No isolation found")


    def isocheck(self,lepton,checkvalue):
        self.moreiso = False
        if hasattr(lepton,'pfRelIso04_all'):
            if lepton.pfRelIso04_all < checkvalue:          #muon more isolated -> smaller value
                self.moreiso = True
        elif hasattr(lepton,'pfRelIso03_all'):
            if lepton.pfRelIso03_all < checkvalue:          #electron more isolated -> smaller value
                self.moreiso = True
        elif hasattr(lepton,'rawDeepTau2017v2p1VSjet'):
            if lepton.rawDeepTau2017v2p1VSjet > checkvalue: #tau more isolated -> larger value
                self.moreiso = True
        else:
            print("ERROR: No isolation found")
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
        self.BTagWeight_up         = 1.
        self.BTagWeight_down       = 1.
        self.GenWeight             = 1.
        self.PUWeight              = 1.
        self.MuWeight              = 1.
        self.MuWeight_up           = 1.
        self.MuWeight_down         = 1.
        self.MuTriggerWeight       = 1.
        self.MuTriggerWeight_up    = 1.
        self.MuTriggerWeight_down  = 1.
        self.EWeight               = 1.
        self.EWeight_up            = 1.
        self.EWeight_down          = 1.
        self.ETriggerWeight        = 1.
        self.ETriggerWeight_up     = 1.
        self.ETriggerWeight_down   = 1.
        self.TauWeight             = 1.
        self.TauWeight_up          = 1.
        self.TauWeight_down        = 1.
        self.TauTriggerWeight      = 1.
        self.TauTriggerWeight_up   = 1.
        self.TauTriggerWeight_down = 1.
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
        self.Jet1_pt               = -1.
        self.Jet1_eta              = -10.
        self.Jet1_phi              = -10.
        self.Jet1_mass             = -1.
        self.Jet1_btag             = -1.
        self.Jet2_pt               = -1.
        self.Jet2_eta              = -10.
        self.Jet2_phi              = -10.
        self.Jet2_mass             = -1.
        self.Jet2_btag             = -1.
        self.Jet3_pt               = -1.
        self.Jet3_eta              = -10.
        self.Jet3_phi              = -10.
        self.Jet3_mass             = -1.
        self.Jet3_btag             = -1.
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
        self.Tau2_pt               = -1.
        self.Tau2_eta              = -10.
        self.Tau2_phi              = -10.
        self.Tau2_mass             = -1.
        self.Tau2_charge           = -1.
        self.Tau2_iso              = -1.
        self.Tau2_genmatch         = -1.
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
        self.wt_ff                 = 0.
        self.wt_ff_nocorr          = 0.
        self.wt_ff_ttdr            = 0.
        self.wt_ff_qcddr           = 0.
        self.wt_ff_qcddr_old       = 0.
        self.wt_ff_old             = 0.
        self.wt_ff_qcd             = 0.
        self.wt_ff_w               = 0.
        self.wt_ff_tt              = 0.
        self.wt_ff_qcd_old         = 0.
        self.wt_ff_w_old           = 0.
        self.wt_ff_tt_old          = 0.
        self.wt_ffcorr_leppt_qcd   = 1.
        self.wt_ffcorr_leppt_tt    = 1.
        self.wt_ffcorr_leppt_w     = 1.
        self.wt_ffcorr_hmass_qcd   = 1.
        self.wt_ffcorr_hmass_tt    = 1.
        self.wt_ffcorr_hmass_w     = 1.
        self.wt_ffcorr_jetbtag_qcd = 1.
        self.wt_ffcorr_jetbtag_tt  = 1.
        self.wt_ffcorr_jetbtag_w   = 1.
        self.wt_ffcorr_jetpt_qcd   = 1.
        self.wt_ffcorr_jetpt_tt    = 1.
        self.wt_ffcorr_jetpt_w     = 1.
        self.wt_ffcorr_jet2pt_qcd  = 1.
        self.wt_ffcorr_jet2pt_tt   = 1.
        self.wt_ffcorr_jet2pt_w    = 1.
        self.wt_ffcorr_met_qcd     = 1.
        self.wt_ffcorr_met_tt      = 1.
        self.wt_ffcorr_met_w       = 1.
        self.wt_ff_up              = 1.
        self.wt_ff_down            = 1.
        self.wt_ff_up_qcd          = 1.
        self.wt_ff_down_qcd        = 1.
        self.wt_ff_up_w            = 1.
        self.wt_ff_down_w          = 1.
        self.wt_ff_up_tt           = 1.
        self.wt_ff_down_tt         = 1.
        self.wt_dy                 = 1.
        self.wt_dy_reco            = 1.
        self.wt_tt                 = 1.
        self.wt_dy_nlo             = 1.
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
        self.ff_fitunc_tt_par3     = 0.
        self.ff_fitunc_tt_par4     = 0.
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
        self.met_var_qcd           = -1.
        self.met_var_w             = -1.
        self.wpt                   = -1.
        self.DRLepB                = -1.
        self.DEtaLepB              = -10.
        self.DPhiLepB              = -10.
        self.DRTauB                = -1.
        self.DEtaTauB              = -10.
        self.DPhiTauB              = -10.
        self.DRLepB2               = -1.
        self.DEtaLepB2             = -10.
        self.DPhiLepB2             = -10.
        self.DRTauB2               = -1.
        self.DEtaTauB2             = -10.
        self.DPhiTauB2             = -10.
        self.HB_mass               = -1.
        self.HB_pt                 = -1.
        self.DRHB                  = -1.
        self.DEtaHB                = -10.
        self.DPhiHB                = -10.
        self.HB2_mass              = -1.
        self.HB2_pt                = -1.
        self.DRHB2                 = -1.
        self.DEtaHB2               = -10.
        self.DPhiHB2               = -10.
        self.LepB_mass             = -1.
        self.TauB_mass             = -1.
        self.TauBMET_mass          = -1.
        self.METB_mass             = -1.
        self.vistauB_mass          = -1.
        self.vistauBMET_mass       = -1.
        self.LepBMET_mass          = -1.
        self.dijet_pt              = -1.
        self.dijet_eta             = -10.
        self.dijet_phi             = -10.
        self.dijet_mass            = -1.
        self.DRjets                = -1.
        self.DEta_jets             = -10.
        self.DPhi_jets             = -10.
        self.LepB_pt               = -1.
        self.TauB_pt               = -1.
        self.vistauB_pt            = -1.
        self.vistauBMET_pt         = -1.
        self.TauBMET_pt            = -1.
        self.LepBMET_pt            = -1.
        self.METB_pt               = -1.
        self.vistauMET_pt          = -1.
        self.LepJ_mass             = -1.
        self.TauJ_mass             = -1.
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

        #JEC 
        


        #############   Gen Weight ######################
        if self.isMC:
            self.GenWeight =  event.genWeight
            self.PUWeight = event.puWeight
            self.EventWeight *= self.GenWeight
            self.EventWeight *= self.PUWeight
            if "GluGluToBBHToTauTau" in self.sample:
                genParticles = Collection(event,"GenPart")
                for i,genPart in enumerate(genParticles):
                    if genPart.pdgId==25:
                        self.H_mass_gen = genPart.mass
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
                genweight_incl = 26540.
                genweight_0J = 7264.
                genweight_1J = 9763.
                genweight_2J = 8287.
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
            if "gghplusbb" in self.sample or "bbHToTauTau" in self.sample or "GluGluHToTauTau" in self.sample:
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

        # only selecting events with zero jets for inclusive DYjets sample to combine with jet binned samples
        if self.sample_name=="DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8":
            if event.LHE_Njets>0:
                return False
        if "JetsToLNu" in self.sample: #remove outliners in EventWeight in W+jets samples
            if self.EventWeight > 1000.:
                return False
        if self.sample_name=="WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8":
            if event.LHE_Njets>0:
                return False
        #splitting sample gghplusbb
        if "gghplusbb" in self.sample or "bbHToTauTau_M-125_4FS_TuneCP5_yt2" in self.sample:
            if self.nGenBjets==0 or (self.nGenBjets==1 and GenBjet_match<2):
                return False
        if "ggfhplusbb" in self.sample or "jjHToTauTau_M-125_4FS_TuneCP5_yt2" in self.sample:
            if self.nGenBjets>0:
                return False    
        if "gghplusbb_ext" in self.sample:
            if self.nGenBjets==0 or (self.nGenBjets==1 and GenBjet_match<2):
                return False    
        if "ggfhplusbb_ext" in self.sample and self.nGenBjets>0:
            return False 
        #splitting sample ggH
        if "GluGluHToTauTau" in self.sample:
            if self.nGenBjets==0 or self.nGenBjets>1 or (self.nGenBjets==1 and GenBjet_match>1):
                return False
        if "GGFHToTauTau" in self.sample and self.nGenBjets>0:
            return False  
        #splitting sample BBHToTauTau
        if "BBHToTauTau" in self.sample or "bbHToTauTau_M-125_4FS_TuneCP5_yb2" in self.sample:
            if self.nGenBjets==0:
                return False
        if "JJHToTauTau" in self.sample or "jjHToTauTau_M-125_4FS_TuneCP5_yb2" in self.sample:
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
        met = Object(event, "MET")


        for tau in taus:
            try:
                tau_decaymode = tau.idDecayMode
            except:
                tau_decaymode = tau.idDecayModeOldDMs
            if tau.pt > 30. and abs(tau.eta) < 2.3 and abs(tau.charge) == 1 and abs(tau.dz) < 0.2 and tau_decaymode > 0.5 and tau.idDeepTau2017v2p1VSjet >= 31:
                if tau.idDeepTau2017v2p1VSe >= 1 and tau.idDeepTau2017v2p1VSmu == 15:
                    tau_vetomu_list.append(tau)
                if tau.idDeepTau2017v2p1VSe >= 63 and tau.idDeepTau2017v2p1VSmu >= 1:
                    tau_vetoe_list.append(tau)
                if tau.pt > 40. and abs(tau.eta) < 2.1 and tau.idDeepTau2017v2p1VSe >= 1 and tau.idDeepTau2017v2p1VSmu >= 1:
                    ditau_list.append(tau)
            ### select taus for application region  ###
            #was tau.idDeepTau2017v2p1VSjet&1 == 1 && tau.idDeepTau2017v2p1VSjet&16 == 0
            #was tau.idDeepTau2017v2p1VSjet>=7 and tau.idDeepTau2017v2p1VSjet<31
            if tau.pt > 30. and abs(tau.eta) < 2.3 and abs(tau.charge) == 1 and abs(tau.dz) < 0.2 and tau_decaymode > 0.5 and tau.idDeepTau2017v2p1VSjet>=1 and tau.idDeepTau2017v2p1VSjet<31:
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
            if electron.pt > 10. and abs(electron.eta) < 2.5 and abs(electron.dxy) < 0.045 and abs(electron.dz) < 0.2 and electron.mvaFall17V2noIso_WP90 and electron.pfRelIso03_all < 0.3:
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
            return False

        if self.METfilter(event)==False:
            return False

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
        wp_loose = 0.0494
        wp_medium = 0.2770
        wp_tight = 0.7264
        

        for jet in jets: 
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
                        
        if len(jet_forward_list)>1.:
            self.DEta_jets_forward = abs(jet_forward_list[0].eta-jet_forward_list[1].eta)
          
        self.nJets = len(jet_list)
        self.nJets_forward = len(jet_forward_list)
        self.nBjets_l = len(jet_btag_loose_list)
        self.nBjets_m = len(jet_btag_medium_list)
        self.nBjets_t = len(jet_btag_tight_list)
        self.nBjets_l_excl = len(jet_btag_loose_excl_list)
        self.nBjets_m_excl = len(jet_btag_medium_excl_list)

        #btag scale factors
        if self.isMC:
            self.btagTool.fillEfficiencies(jet_list)
            self.BTagWeight  = self.btagTool.getWeight(jet_list)
            self.BTagWeight_up  = self.btagTool_up.getWeight(jet_list)
            self.BTagWeight_down  = self.btagTool_down.getWeight(jet_list)


        for jet in jets: 
            if abs(jet.eta) < 2.4 and jet.pt > 30. and jet.jetId >= 2:
                if self.vec(jet).DeltaR(self.vec(pair[0])) > 0.4:
                    if self.vec(jet).DeltaR(self.vec(pair[1])) > 0.4:
                        jet_list_tcut.append(jet)
                        if jet.btagDeepFlavB > wp_tight:
                            jet_btag_tight_list_tcut.append(jet)
                        if jet.btagDeepFlavB > wp_medium:
                            jet_btag_medium_list_tcut.append(jet)
                        if jet.btagDeepFlavB > wp_loose:
                            jet_btag_loose_list_tcut.append(jet)
            
        self.nJets_tcut = len(jet_list_tcut)
        self.nBjets_l_tcut = len(jet_btag_loose_list_tcut)
        self.nBjets_m_tcut = len(jet_btag_medium_list_tcut)
        self.nBjets_t_tcut = len(jet_btag_tight_list_tcut)

        jet_list.sort(key=lambda x: x.btagDeepFlavB,reverse=True)

        if len(jet_list) > 0:
            self.Jet1_pt = jet_list[0].pt
            self.Jet1_eta = jet_list[0].eta
            self.Jet1_phi = jet_list[0].phi
            self.Jet1_mass = jet_list[0].mass
            self.Jet1_btag = jet_list[0].btagDeepFlavB
            jet1_tlv = self.tlv(jet_list[0])
        if len(jet_list) > 1:
            self.Jet2_pt = jet_list[1].pt
            self.Jet2_eta = jet_list[1].eta
            self.Jet2_phi = jet_list[1].phi
            self.Jet2_mass = jet_list[1].mass
            self.Jet2_btag = jet_list[1].btagDeepFlavB
            jet2_tlv = self.tlv(jet_list[1])
            dijet_tlv = jet1_tlv + jet2_tlv
            self.dijet_pt = dijet_tlv.Pt()
            self.dijet_phi = dijet_tlv.Phi()
            self.dijet_eta = dijet_tlv.Eta()
            self.dijet_mass = dijet_tlv.M()
            self.DEta_jets = abs(jet1_tlv.Eta()-jet2_tlv.Eta())
            self.DPhi_jets = jet1_tlv.DeltaPhi(jet2_tlv)
            self.DRjets = jet1_tlv.DeltaR(jet2_tlv)
        if len(jet_list) > 2:
            self.Jet3_pt = jet_list[2].pt
            self.Jet3_eta = jet_list[2].eta
            self.Jet3_phi = jet_list[2].phi
            self.Jet3_mass = jet_list[2].mass
            self.Jet3_btag = jet_list[2].btagDeepFlavB   

        

        if len(jet_btag_medium_list) > 0:
            self.Bjet1_pt = jet_btag_medium_list[0].pt
            self.Bjet1_eta = jet_btag_medium_list[0].eta
            self.Bjet1_phi = jet_btag_medium_list[0].phi
            self.Bjet1_mass = jet_btag_medium_list[0].mass
            Bjet1_tlv = self.tlv(jet_btag_medium_list[0])
        if len(jet_btag_medium_list) > 1:
            self.Bjet2_pt = jet_btag_medium_list[1].pt
            self.Bjet2_eta = jet_btag_medium_list[1].eta
            self.Bjet2_phi = jet_btag_medium_list[1].phi
            self.Bjet2_mass = jet_btag_medium_list[1].mass
            Bjet2_tlv = self.tlv(jet_btag_medium_list[1])
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

        if isMuTau:
            if not (self.trigger_Mu.fired(event) or self.trigger_MuTau.fired(event)):
                return False
            if not (self.trigger_Mu.match(event,pair[0]) or (self.trigger_MuTau.match(event,pair[0]) and self.trigger_MuTau.match(event,pair[1]))):
                return False
            self.Mu1_pt                = pair[0].pt
            self.Mu1_eta               = pair[0].eta
            self.Mu1_phi               = pair[0].phi
            self.Mu1_mass              = pair[0].mass
            self.Mu1_charge            = pair[0].charge
            self.Mu1_iso               = self.iso(pair[0])
        elif isETau:
            if not (self.trigger_E.fired(event) or self.trigger_ETau.fired(event)):
                return False
            if not (self.trigger_E.match(event,pair[0]) or (self.trigger_ETau.match(event,pair[0]) and self.trigger_ETau.match(event,pair[1]))):
                return False                 
            self.Ele1_pt                = pair[0].pt
            self.Ele1_eta               = pair[0].eta
            self.Ele1_phi               = pair[0].phi
            self.Ele1_mass              = pair[0].mass
            self.Ele1_charge            = pair[0].charge
            self.Ele1_iso               = self.iso(pair[0])
        elif self.isMuMu:
            if not self.trigger_Mu.fired(event):
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
            if not (self.trigger_Mu.fired(event) or self.trigger_E.fired(event)):
                return False
            if not (self.trigger_Mu.match(event,pair[0]) or self.trigger_E.match(event,pair[1])):
                return False
            if self.trigger_Mu.fired(event) and ("EGamma" in self.sample_name or "SingleElectron" in self.sample_name):
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
        self.collinear_mass        = self.vis_mass/np.sqrt((self.vistau1_pt/(self.vistau1_pt+event.PuppiMET_pt))*(self.vistau2_pt/(self.vistau2_pt+event.PuppiMET_pt)))
        self.collinear_mass_chs    = self.vis_mass/np.sqrt((self.vistau1_pt/(self.vistau1_pt+event.MET_pt))*(self.vistau2_pt/(self.vistau2_pt+event.MET_pt)))
        if self.isMC:
            if "DY" in self.sample:
                genV                     = getGenV(event,pair[0],pair[1])
                self.wt_dy               = self.DYCorrection.getWeight(genV.Pt(),genV.M())
                self.wt_dy_reco          = self.DYCorrection.getWeight(self.vis_pt,self.vis_mass)
            if "TT" in self.sample:
                self.wt_tt = self.DYCorrection.getWeight_tt()
            
            if isMuTau:
                self.Mu1_genmatch      = genmatching(event,pair[0])
                MuTriggerSF                = self.muSFs.getTriggerSF(self.Mu1_pt,self.Mu1_eta)
                self.MuTriggerWeight       = MuTriggerSF[0]
                self.MuTriggerWeight_up    = MuTriggerSF[1]
                self.MuTriggerWeight_down  = MuTriggerSF[2]
                MuSF                       = self.muSFs.getSF(self.Mu1_pt,self.Mu1_eta)
                self.MuWeight              = MuSF[0]
                self.MuWeight_up           = MuSF[1]
                self.MuWeight_down         = MuSF[2]
                TauTriggerSF               = self.tauSFs.getTriggerSF(self.Tau1_pt,self.Tau1_decaymode,"mutau")
                self.TauTriggerWeight      = TauTriggerSF[0]
                self.TauTriggerWeight_up   = TauTriggerSF[1]
                self.TauTriggerWeight_down = TauTriggerSF[2]
                self.Tau1_genmatch     = genmatching(event,pair[1])
                TauSF                      = self.tauSFs.getSF(self.Tau1_pt,self.Tau1_genmatch)
                self.TauWeight             = TauSF[0]
                self.TauWeight_up          = TauSF[1]
                self.TauWeight_down        = TauSF[2]
            elif isETau:
                self.Ele1_genmatch      = genmatching(event,pair[0])
                ETriggerSF                = self.eSFs.getTriggerSF(self.Ele1_pt,self.Ele1_eta)
                self.ETriggerWeight       = ETriggerSF[0]
                self.ETriggerWeight_up    = ETriggerSF[1]
                self.ETriggerWeight_down  = ETriggerSF[2]
                ESF                       = self.eSFs.getSF(self.Ele1_pt,self.Ele1_eta)
                self.EWeight              = ESF[0]
                self.EWeight_up           = ESF[1]
                self.EWeight_down         = ESF[2]
                TauTriggerSF               = self.tauSFs.getTriggerSF(self.Tau1_pt,self.Tau1_decaymode,"etau")
                self.TauTriggerWeight      = TauTriggerSF[0]
                self.TauTriggerWeight_up   = TauTriggerSF[1]
                self.TauTriggerWeight_down = TauTriggerSF[2]
                self.Tau1_genmatch     = genmatching(event,pair[1])
                TauSF                      = self.tauSFs.getSF(self.Tau1_pt,self.Tau1_genmatch)
                self.TauWeight             = TauSF[0]
                self.TauWeight_up          = TauSF[1]
                self.TauWeight_down        = TauSF[2]
            elif self.isTTCR:
                self.Mu1_genmatch          = genmatching(event,pair[0])
                self.Ele1_genmatch         = genmatching(event,pair[1])
                MuETriggerSF                = self.muSFs.getTriggerSFMuE(self.Mu1_pt,self.Mu1_eta,self.Ele1_pt,self.Ele1_eta)
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
                MuTriggerSF                = self.muSFs.getTriggerSFMuMu(self.Mu1_pt,self.Mu1_eta,self.Mu2_pt,self.Mu2_eta)
                self.MuTriggerWeight       = MuTriggerSF[0]
                self.MuTriggerWeight_up    = MuTriggerSF[1]
                self.MuTriggerWeight_down  = MuTriggerSF[2]
                MuSF                       = self.muSFs.getSFMuMu(self.Mu1_pt,self.Mu1_eta,self.Mu2_pt,self.Mu2_eta)
                self.MuWeight              = MuSF[0]
                self.MuWeight_up           = MuSF[1]
                self.MuWeight_down         = MuSF[2]
                self.Mu2_genmatch      = genmatching(event,pair[1])

        if isMuTau or isETau:
            self.mysvinterface.clearLeptons()
            self.mysvinterface.setTauOne(1,pair[0].pt,pair[0].eta,pair[0].phi,pair[0].mass,-1)
            self.mysvinterface.setTauTwo(2,pair[1].pt,pair[1].eta,pair[1].phi,pair[1].mass,pair[1].decayMode)
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
            if len(jet_btag_medium_list)>0:
                bjet1_tlv = self.tlv(jet_btag_medium_list[0])
                HB_tlv = H_tlv + bjet1_tlv
                self.HB_mass = HB_tlv.M()
                self.HB_pt = HB_tlv.Pt()
                self.DRHB = H_tlv.DeltaR(bjet1_tlv)
                self.DEtaHB = abs(H_tlv.Eta()-bjet1_tlv.Eta())
                self.DPhiHB = H_tlv.DeltaPhi(bjet1_tlv)
            if len(jet_btag_medium_list)>1:
                bjet2_tlv = self.tlv(jet_btag_medium_list[1])
                HB2_tlv = H_tlv + bjet2_tlv
                self.HB2_mass = HB2_tlv.M()
                self.HB2_pt = HB2_tlv.Pt()
                self.DRHB2 = H_tlv.DeltaR(bjet2_tlv)
                self.DEtaHB2 = abs(H_tlv.Eta()-bjet2_tlv.Eta())
                self.DPhiHB2 = H_tlv.DeltaPhi(bjet2_tlv)
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
            met_tlv.SetPtEtaPhiM(met.pt,0.,met.phi,0.)
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
            if len(jet_btag_medium_list)>0:
                bjet1_tlv = self.tlv(jet_btag_medium_list[0])
                self.LepB_mass = (lep_tlv + bjet1_tlv).M()
                self.TauB_mass = (tau_tlv + bjet1_tlv).M()
                self.vistauB_mass = (tau_tlv + lep_tlv + bjet1_tlv).M()
                self.vistauBMET_mass = (tau_tlv + lep_tlv + bjet1_tlv + met_tlv).Mt()
                self.TauBMET_mass = (tau_tlv + bjet1_tlv + met_tlv).Mt()
                self.LepBMET_mass = (lep_tlv + bjet1_tlv + met_tlv).Mt()
                self.METB_mass = (bjet1_tlv + met_tlv).Mt()
                self.LepB_pt = (lep_tlv + bjet1_tlv).Pt()
                self.TauB_pt = (tau_tlv + bjet1_tlv).Pt()
                self.vistauB_pt = (tau_tlv + lep_tlv + bjet1_tlv).Pt()
                self.vistauBMET_pt = (tau_tlv + lep_tlv + bjet1_tlv + met_tlv).Pt()
                self.TauBMET_pt = (tau_tlv + bjet1_tlv + met_tlv).Pt()
                self.LepBMET_pt = (lep_tlv + bjet1_tlv + met_tlv).Pt()
                self.METB_pt = (bjet1_tlv + met_tlv).Pt()
                self.DRTauB = tau_tlv.DeltaR(bjet1_tlv) 
                self.DEtaTauB = abs(tau_tlv.Eta()-bjet1_tlv.Eta())
                self.DPhiTauB = tau_tlv.DeltaPhi(bjet1_tlv)
                self.DRLepB = lep_tlv.DeltaR(bjet1_tlv) 
                self.DEtaLepB = abs(lep_tlv.Eta()-bjet1_tlv.Eta())
                self.DPhiLepB = lep_tlv.DeltaPhi(bjet1_tlv)
            if len(jet_btag_medium_list)>1:
                bjet2_tlv = self.tlv(jet_btag_medium_list[1])
                self.DRTauB2 = tau_tlv.DeltaR(bjet2_tlv) 
                self.DEtaTauB2 = abs(tau_tlv.Eta()-bjet2_tlv.Eta())
                self.DPhiTauB2 = tau_tlv.DeltaPhi(bjet2_tlv)
                self.DRLepB2 = lep_tlv.DeltaR(bjet2_tlv) 
                self.DEtaLepB2 = abs(lep_tlv.Eta()-bjet2_tlv.Eta())
                self.DPhiLepB2 = lep_tlv.DeltaPhi(bjet2_tlv)
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
                self.DRTauJ2 = tau_tlv.DeltaR(jet2_tlv) 
                self.DEtaTauJ2 = abs(tau_tlv.Eta()-jet2_tlv.Eta())
                self.DPhiTauJ2 = tau_tlv.DeltaPhi(jet2_tlv)
                self.DRLepJ2 = lep_tlv.DeltaR(jet2_tlv) 
                self.DEtaLepJ2 = abs(lep_tlv.Eta()-jet2_tlv.Eta())
                self.DPhiLepJ2 = lep_tlv.DeltaPhi(jet2_tlv)


            self.DPhiLepMET = lep_tlv.DeltaPhi(met_tlv)
            self.DRLepMET = lep_tlv.DeltaR(met_tlv)
            

            self.met_var_qcd = met.pt*cos(tau_tlv.DeltaPhi(met_tlv))/pair[1].pt
            self.met_var_w = lepmet_tlv.Pt()*cos(tau_tlv.DeltaPhi(lepmet_tlv))/pair[1].pt
            self.wpt = lepmet_tlv.Pt()

        if isMuTau:
            isos = 1. if self.Mu1_charge*self.Tau1_charge!=1 else 0.
            pass_single = int(self.trigger_Mu.fired(event))
            self.wt_ff_old = self.ff_functor_obj.eval(array('d',[self.Tau1_pt,self.Tau1_decaymode,self.nJets,self.Mu1_pt,isos,self.Mu1_iso,pass_single,self.met_var_qcd,self.met_var_w,self.wpt,self.transverse_mass_lepmet]))
            wt_ff_list = self.ff.ffweight_corr(self.Tau1_pt,self.Mu1_pt,self.H_mass,self.Jet1_pt,self.Jet2_pt,event.PuppiMET_pt,self.Tau1_decaymode,"mutau")
            self.wt_ff = wt_ff_list[0]
            self.wt_ff_up = wt_ff_list[1]
            self.wt_ff_down = wt_ff_list[2]
            self.wt_ff_up_qcd = wt_ff_list[3]
            self.wt_ff_down_qcd = wt_ff_list[4]
            self.wt_ff_up_w = wt_ff_list[5]
            self.wt_ff_down_w = wt_ff_list[6]
            self.wt_ff_up_tt = wt_ff_list[7]
            self.wt_ff_down_tt = wt_ff_list[8]
            self.wt_ff_nocorr = self.ff.ffweight(self.Tau1_pt,self.Tau1_decaymode,"mutau")
            self.wt_ff_ttdr = self.ff.ffweight_ttdr(self.Tau1_pt,self.Tau1_decaymode,"mutau")
            self.wt_ff_qcddr = self.ff.ffweight_qcddr(self.Tau1_pt,self.Mu1_pt,self.H_mass,self.Jet1_pt,self.Jet2_pt,event.PuppiMET_pt,self.Tau1_decaymode,"mutau")
            self.wt_ff_qcddr_old = self.ff.ffweight_qcddr_old(self.Tau1_pt,self.Mu1_pt,self.H_mass,self.Jet1_pt,self.Jet2_pt,event.PuppiMET_pt,self.Tau1_decaymode,"mutau")
            ffweight_sep = self.ff.ffweight_sep(self.Tau1_pt,self.Tau1_decaymode,"mutau")
            self.wt_ff_qcd = ffweight_sep[0]
            self.wt_ff_w = ffweight_sep[1]
            self.wt_ff_tt = ffweight_sep[2]
            self.wt_ff_qcd_old = ffweight_sep[3]
            self.wt_ff_w_old = ffweight_sep[4]
            self.wt_ff_tt_old = ffweight_sep[5]
            ffweightcorr_leppt = self.ff.ffweightcorr_leppt(self.Mu1_pt,self.Tau1_decaymode,"mutau")
            self.wt_ffcorr_leppt_qcd = ffweightcorr_leppt[0]
            self.wt_ffcorr_leppt_w = ffweightcorr_leppt[1]
            self.wt_ffcorr_leppt_tt = ffweightcorr_leppt[2]
            ffweightcorr_hmass = self.ff.ffweightcorr_hmass(self.H_mass,self.Tau1_decaymode,"mutau")
            self.wt_ffcorr_hmass_qcd = ffweightcorr_hmass[0]
            self.wt_ffcorr_hmass_w = ffweightcorr_hmass[1]
            self.wt_ffcorr_hmass_tt = ffweightcorr_hmass[2]
            ffweightcorr_jetbtag = self.ff.ffweightcorr_jetbtag(self.Jet1_btag,self.Tau1_decaymode,"mutau")
            self.wt_ffcorr_jetbtag_qcd = ffweightcorr_jetbtag[0]
            self.wt_ffcorr_jetbtag_w = ffweightcorr_jetbtag[1]
            self.wt_ffcorr_jetbtag_tt = ffweightcorr_jetbtag[2]
            ffweightcorr_jetpt = self.ff.ffweightcorr_jetpt(self.Jet1_pt,self.Tau1_decaymode,"mutau")
            self.wt_ffcorr_jetpt_qcd = ffweightcorr_jetpt[0]
            self.wt_ffcorr_jetpt_w = ffweightcorr_jetpt[1]
            self.wt_ffcorr_jetpt_tt = ffweightcorr_jetpt[2]
            ffweightcorr_jet2pt = self.ff.ffweightcorr_jet2pt(self.Jet2_pt,self.Tau1_decaymode,"mutau")
            self.wt_ffcorr_jet2pt_qcd = ffweightcorr_jet2pt[0]
            self.wt_ffcorr_jet2pt_w = ffweightcorr_jet2pt[1]
            self.wt_ffcorr_jet2pt_tt = ffweightcorr_jet2pt[2]
            ffweightcorr_met = self.ff.ffweightcorr_met(event.PuppiMET_pt,self.Tau1_decaymode,"mutau")
            self.wt_ffcorr_met_qcd = ffweightcorr_met[0]
            self.wt_ffcorr_met_w = ffweightcorr_met[1]
            self.wt_ffcorr_met_tt = ffweightcorr_met[2]
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
            self.ff_fitunc_tt_par3 = ff_fitunc[2][2]
            self.ff_fitunc_tt_par4 = ff_fitunc[2][3]
        elif isETau:
            isos = 1. if self.Ele1_charge*self.Tau1_charge!=1 else 0.
            pass_single = int(self.trigger_E.fired(event))
            self.wt_ff_old = self.ff_functor_obj.eval(array('d',[self.Tau1_pt,self.Tau1_decaymode,self.nJets,self.Ele1_pt,isos,self.Ele1_iso,pass_single,self.met_var_qcd,self.met_var_w,self.wpt,self.transverse_mass_lepmet]))
            wt_ff_list = self.ff.ffweight_corr(self.Tau1_pt,self.Ele1_pt,self.H_mass,self.Jet1_pt,self.Jet2_pt,event.PuppiMET_pt,self.Tau1_decaymode,"etau")
            self.wt_ff = wt_ff_list[0]
            self.wt_ff_up = wt_ff_list[1]
            self.wt_ff_down = wt_ff_list[2]
            self.wt_ff_up_qcd = wt_ff_list[3]
            self.wt_ff_down_qcd = wt_ff_list[4]
            self.wt_ff_up_w = wt_ff_list[5]
            self.wt_ff_down_w = wt_ff_list[6]
            self.wt_ff_up_tt = wt_ff_list[7]
            self.wt_ff_down_tt = wt_ff_list[8]
            self.wt_ff_nocorr = self.ff.ffweight(self.Tau1_pt,self.Tau1_decaymode,"etau")
            self.wt_ff_ttdr = self.ff.ffweight_ttdr(self.Tau1_pt,self.Tau1_decaymode,"etau")
            self.wt_ff_qcddr = self.ff.ffweight_qcddr(self.Tau1_pt,self.Ele1_pt,self.H_mass,self.Jet1_pt,self.Jet2_pt,event.PuppiMET_pt,self.Tau1_decaymode,"etau")
            self.wt_ff_qcddr_old = self.ff.ffweight_qcddr_old(self.Tau1_pt,self.Ele1_pt,self.H_mass,self.Jet1_pt,self.Jet2_pt,event.PuppiMET_pt,self.Tau1_decaymode,"etau")
            ffweight_sep = self.ff.ffweight_sep(self.Tau1_pt,self.Tau1_decaymode,"etau")
            self.wt_ff_qcd = ffweight_sep[0]
            self.wt_ff_w = ffweight_sep[1]
            self.wt_ff_tt = ffweight_sep[2]
            self.wt_ff_qcd_old = ffweight_sep[3]
            self.wt_ff_w_old = ffweight_sep[4]
            self.wt_ff_tt_old = ffweight_sep[5]
            ffweightcorr_leppt = self.ff.ffweightcorr_leppt(self.Ele1_pt,self.Tau1_decaymode,"etau")
            self.wt_ffcorr_leppt_qcd = ffweightcorr_leppt[0]
            self.wt_ffcorr_leppt_w = ffweightcorr_leppt[1]
            self.wt_ffcorr_leppt_tt = ffweightcorr_leppt[2]
            ffweightcorr_hmass = self.ff.ffweightcorr_hmass(self.H_mass,self.Tau1_decaymode,"etau")
            self.wt_ffcorr_hmass_qcd = ffweightcorr_hmass[0]
            self.wt_ffcorr_hmass_w = ffweightcorr_hmass[1]
            self.wt_ffcorr_hmass_tt = ffweightcorr_hmass[2]
            ffweightcorr_jetbtag = self.ff.ffweightcorr_jetbtag(self.Jet1_btag,self.Tau1_decaymode,"etau")
            self.wt_ffcorr_jetbtag_qcd = ffweightcorr_jetbtag[0]
            self.wt_ffcorr_jetbtag_w = ffweightcorr_jetbtag[1]
            self.wt_ffcorr_jetbtag_tt = ffweightcorr_jetbtag[2]
            ffweightcorr_jetpt = self.ff.ffweightcorr_jetpt(self.Jet1_pt,self.Tau1_decaymode,"etau")
            self.wt_ffcorr_jetpt_qcd = ffweightcorr_jetpt[0]
            self.wt_ffcorr_jetpt_w = ffweightcorr_jetpt[1]
            self.wt_ffcorr_jetpt_tt = ffweightcorr_jetpt[2]
            ffweightcorr_jet2pt = self.ff.ffweightcorr_jet2pt(self.Jet2_pt,self.Tau1_decaymode,"etau")
            self.wt_ffcorr_jet2pt_qcd = ffweightcorr_jet2pt[0]
            self.wt_ffcorr_jet2pt_w = ffweightcorr_jet2pt[1]
            self.wt_ffcorr_jet2pt_tt = ffweightcorr_jet2pt[2]
            ffweightcorr_met = self.ff.ffweightcorr_met(event.PuppiMET_pt,self.Tau1_decaymode,"etau")
            self.wt_ffcorr_met_qcd = ffweightcorr_met[0]
            self.wt_ffcorr_met_w = ffweightcorr_met[1]
            self.wt_ffcorr_met_tt = ffweightcorr_met[2]
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
            self.ff_fitunc_tt_par3 = ff_fitunc[2][2]
            self.ff_fitunc_tt_par4 = ff_fitunc[2][3]
        self.fillBranches(event)
        return True
        
        
