import re, math
from math import sqrt, sin, cos, pi
import numpy as np 
import array
import ROOT
from ROOT import TTree, TH1D, TH2D, TLorentzVector, TVector3
from ROOT.heppy import Davismt2
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Event



def calculate_topPtWeight(pt, a, b, c, max_pt):
    if pt > max_pt: pt = max_pt # approximation works only up to 400 GeV
    w = np.exp(a + (b*pt) + (c*pt*pt))
    return w

def topPtWeight(event):
    a = 0.088
    b = -0.00087
    c = 9.2e-07
    max_pt = 472.0
    w_pos = 1
    w_neg = 1
    topPt = -1
    antitopPt = -1
    genParticles = Collection(event,"GenPart")
    for i,genPart in enumerate(genParticles):
        if genPart.pdgId == 6:
            if genParticles[genPart.genPartIdxMother].pdgId!=6: #avoiding self coupling
                topPt = genPart.pt
                w_pos = calculate_topPtWeight(topPt, a, b, c, max_pt)
        elif genPart.pdgId == -6:
            if genParticles[genPart.genPartIdxMother].pdgId!=-6: #avoiding self coupling
                antitopPt = genPart.pt
                w_neg = calculate_topPtWeight(antitopPt, a, b, c, max_pt)
    if topPt > 0. and antitopPt > 0.:
        return np.sqrt(w_pos*w_neg)
    else:
        return 1.

def getJERsplitID(pt, eta):
    if abs(eta) < 1.93:
        return 0
    elif abs(eta) < 2.5:
        return 1
    elif abs(eta) < 3:
        if pt < 50:
            return 2
        else:
            return 3
    else:
        if pt < 50:
            return 4
        else:
            return 5       



def computeMT2(visaVec, visbVec, metVec):
    
    davismt2 = Davismt2()    

    metVector = array.array('d',[0.,metVec.Px(), metVec.Py()])
    visaVector = array.array('d',[0.,visaVec.Px(), visaVec.Py()])
    visbVector = array.array('d',[0.,visbVec.Px(), visbVec.Py()])

    davismt2.set_momenta(visaVector,visbVector,metVector);
    davismt2.set_mn(0);

    return davismt2.get_mt2()


def Dzeta(lep1,lep2,MET,alpha):
  lep1x = np.cos(lep1.Phi())
  lep1y = np.sin(lep1.Phi())
  lep2x = np.cos(lep2.Phi())
  lep2y = np.sin(lep2.Phi())
  zetaX = lep1x + lep2x
  zetaY = lep1y + lep2y
  zetaR = np.sqrt(zetaX*zetaX+zetaY*zetaY)
  if zetaR > 0.:
    zetaX /= zetaR
    zetaY /= zetaR

  visPx = lep1.Px() + lep2.Px()
  visPy = lep1.Py() + lep2.Py()
  pZetaVis = visPx*zetaX + visPy*zetaY
  px = visPx + MET.Px()
  py = visPy + MET.Py()
  pZetaMiss = px*zetaX + py*zetaY
  
  return (pZetaMiss - alpha * pZetaVis)
  


def genmatching(event,recoPart):
  reco_tlv = TLorentzVector()
  reco_tlv.SetPtEtaPhiM(recoPart.pt,recoPart.eta,recoPart.phi,recoPart.mass)
  genParticles = Collection(event,"GenPart")
  idx_genPart = -1
  deltaR_cut = 0.2
  genPart_match = None
  idx_genPart_match = None
  for genPart in genParticles:
    idx_genPart += 1
    gen_tlv = TLorentzVector()
    gen_tlv.SetPtEtaPhiM(genPart.pt,genPart.eta,genPart.phi,genPart.mass)
    if abs(genPart.pdgId) == 15 and genPart.statusFlags&1 == 1:  #IsPrompt
      genTau_decays = Collection(event,"GenPart")
      genTau_tlv = TLorentzVector()
      for genTau_decay in genTau_decays:
        if genTau_decay.genPartIdxMother == idx_genPart and not abs(genTau_decay.pdgId) in [11,12,13,14,15,16]:
          genTau_decay_tlv = TLorentzVector()
          genTau_decay_tlv.SetPtEtaPhiM(genTau_decay.pt,genTau_decay.eta,genTau_decay.phi,genTau_decay.mass)
          genTau_tlv += genTau_decay_tlv
      if genTau_tlv.Pt() < 15: #don't need to check for match if pt of tau jet is below 15 GeV
        continue
      deltaR = genTau_tlv.DeltaR(reco_tlv)
    else:
      if genPart.pt < 8. or not (genPart.statusFlags&1 == 1 or genPart.statusFlags&32 == 32): #don't need to check for match if pt of lepton is below 8 GeV or statusFlag doesn't match
        continue
      deltaR = gen_tlv.DeltaR(reco_tlv)
    if deltaR < deltaR_cut and abs(genPart.pdgId) in [11,13,15]:
      deltaR_cut = deltaR
      idx_genPart_match = idx_genPart
      genPart_match = genPart
  if genPart_match != None:
    if abs(genPart_match.pdgId) == 11 and genPart_match.pt > 8.:
      if genPart_match.statusFlags&1 == 1:     #IsPrompt
        return 1
      elif genPart_match.statusFlags&32 == 32:   #IsDirectPromptTauDecayProduct 
        return 3
    elif abs(genPart_match.pdgId) == 13 and genPart_match.pt > 8:
      if genPart_match.statusFlags&1 == 1:    #IsPrompt
        return 2
      elif genPart_match.statusFlags&32 == 32:    #IsDirectPromptTauDecayProduct
        return 4
    elif abs(genPart_match.pdgId) == 15 and genPart_match.statusFlags&1 == 1:  #IsPrompt
      return 5
  return 6   # return 6 if no match with gen particle or any of the above categories 

def getGenV(event,recoPart1,recoPart2):
  reco1_tlv = TLorentzVector()
  reco1_tlv.SetPtEtaPhiM(recoPart1.pt,recoPart1.eta,recoPart1.phi,recoPart1.mass)
  reco2_tlv = TLorentzVector()
  reco2_tlv.SetPtEtaPhiM(recoPart2.pt,recoPart2.eta,recoPart2.phi,recoPart2.mass)
  gen1_tlv = None
  gen2_tlv = None
  genParticles = Collection(event,"GenPart")
  idx_genPart = -1
  deltaR_cut1 = 0.2
  deltaR_cut2 = 0.2
  for genPart in genParticles:
    idx_genPart += 1
    gen_tlv = TLorentzVector()
    gen_tlv.SetPtEtaPhiM(genPart.pt,genPart.eta,genPart.phi,genPart.mass)
    if abs(genPart.pdgId) == 15 and genPart.statusFlags&1 == 1:  #IsPrompt
      genTau_decays = Collection(event,"GenPart")
      genTau_tlv = TLorentzVector()
      for genTau_decay in genTau_decays:
        if genTau_decay.genPartIdxMother == idx_genPart and not abs(genTau_decay.pdgId) in [11,12,13,14,15,16]:
          genTau_decay_tlv = TLorentzVector()
          genTau_decay_tlv.SetPtEtaPhiM(genTau_decay.pt,genTau_decay.eta,genTau_decay.phi,genTau_decay.mass)
          genTau_tlv += genTau_decay_tlv
      if genTau_tlv.Pt() < 15: #don't need to check for match if pt of tau jet is below 15 GeV
        continue
      deltaR1 = genTau_tlv.DeltaR(reco1_tlv)
      deltaR2 = genTau_tlv.DeltaR(reco2_tlv)
    else:
      if genPart.pt < 8. or not (genPart.statusFlags&1 == 1 or genPart.statusFlags&32 == 32): #don't need to check for match if pt of lepton is below 8 GeV or statusFlag doesn't match
        continue
      deltaR1 = gen_tlv.DeltaR(reco1_tlv)
      deltaR2 = gen_tlv.DeltaR(reco2_tlv)
    if deltaR1<deltaR2:
        if deltaR1 < deltaR_cut1 and abs(genPart.pdgId) in [11,13,15]:
            deltaR_cut1 = deltaR1
            gen1_tlv = gen_tlv
    else:
        if deltaR2 < deltaR_cut2 and abs(genPart.pdgId) in [11,13,15]:
            deltaR_cut2 = deltaR2
            gen2_tlv = gen_tlv

  if gen1_tlv!=None and gen2_tlv!=None:
      V_tlv = gen1_tlv+gen2_tlv
      return V_tlv
  else:
      return TLorentzVector(0.,0.,0.,0.)
      






def getJetID(year,jet):
  eta = abs(jet.eta)
  neutral_hadron_frac = jet.neHEF
  neutral_em_frac = jet.neEmEF
  number_constituents = jet.nConstituents
  charged_hadron_frac = jet.chHEF
  charged_em_frac = jet.chEmEF
  muon_frac = jet.muEF
  if year == 2016:
    if 2.4 < eta and eta <= 2.7:
      if neutral_hadron_frac < 0.9 and neutral_em_frac < 0.9 and number_constituents > 1:
        return True
      else:
        return False
    elif eta <=2.4:
      if neutral_hadron_frac < 0.9 and neutral_em_frac < 0.9 and number_constituents > 1 and charged_hadron_frac > 0 and charged_em_frac < 0.99:
        return True 
      else: 
        return False
    else:
      return True
  elif year == 2017:
    if eta > 3.0:
      if neutral_em_frac < 0.9 and neutral_hadron_frac > 0.02:
        return True
      else:
        return False
    elif 2.7 < eta and eta <= 3.0:
      if neutral_hadron_frac < 0.99:
        return True
      else:
        return False
    elif 2.4 < eta and eta <= 2.7:
      if neutral_hadron_frac < 0.9 and neutral_em_frac < 0.9 and number_constituents > 1:
        return True
      else:
        return False
    elif eta <=2.4:
      if neutral_hadron_frac < 0.9 and neutral_em_frac < 0.9 and number_constituents > 1 and charged_hadron_frac > 0:
        return True
      else:
        return False
   
  elif year == 2018:
    if 3.0 < eta and eta <= 5.0:
      if neutral_hadron_frac > 0.2 and neutral_em_frac < 0.9:
        return True
      else:
        return False
    elif 2.7 < eta and eta <= 3.0:
      if 0.02 < neutral_hadron_frac < 0.99:
        return True
      else:
        return False
    elif 2.6 < eta and eta <= 2.7:
      if neutral_hadron_frac < 0.9 and neutral_em_frac < 0.99:
        return True
      else:
        return False
    elif eta <= 2.6:
      if neutral_hadron_frac < 0.9 and neutral_em_frac < 0.9 and number_constituents > 1 and charged_hadron_frac > 0:
        return True
      else:
        return False


def getGenVpt(event):
  GenVpt = 0.
  VPt = -1.
  idx_V = -1
  LepP = TLorentzVector()
  LepM = TLorentzVector()
  particle_masses = {11 : 0.000511,
                     12 : 0.,
                     13 : 0.10566,
                     14 : 0.,
                     15 : 1.77686, 
                     16 : 0.}
  
  for idx_gen in range(event.nGenPart):
    if event.GenPart_pdgId[idx_gen] == 23 or event.GenPart_pdgId[idx_gen] == 24:
      if VPt<=0.:
        VPt = event.GenPart_pt[idx_gen]
        idx_V = idx_gen
      else:
        if event.GenPart_genPartIdxMother[idx_gen]==idx_V:
          VPt = event.GenPart_pt[idx_gen]
          idx_V = idx_gen
    elif (event.GenPart_status[idx_gen]==1 and event.GenPart_pdgId[idx_gen] >= +11 and event.GenPart_pdgId[idx_gen] <= +16)  or (event.GenPart_pdgId[idx_gen]== +15 and event.GenPart_status[idx_gen]==2):
      if event.GenPart_pt[idx_gen]>LepP.Pt():
        particle_mass = particle_masses[abs(event.GenPart_pdgId[idx_gen])]
        LepP.SetPtEtaPhiM(event.GenPart_pt[idx_gen],event.GenPart_eta[idx_gen],event.GenPart_phi[idx_gen],particle_mass)
    elif (event.GenPart_status[idx_gen]==1 and event.GenPart_pdgId[idx_gen] >= -16 and event.GenPart_pdgId[idx_gen] <= -11) or (event.GenPart_pdgId[idx_gen]== -15 and event.GenPart_status[idx_gen]==2):
      if event.GenPart_pt[idx_gen]>LepM.Pt():
        particle_mass = particle_masses[abs(event.GenPart_pdgId[idx_gen])]
        LepM.SetPtEtaPhiM(event.GenPart_pt[idx_gen],event.GenPart_eta[idx_gen],event.GenPart_phi[idx_gen],particle_mass)
  if VPt > 0.:
    GenVpt = VPt
  elif LepP.Pt() > 0. and LepM.Pt() > 0.:
    GenVpt = (LepP+LepM).Pt()
  return GenVpt



def checkBranches(tree):
  """Redirect some branch names in case they are not available in some samples or nanoAOD version."""
  branches = [
    ('Electron_mvaFall17V2Iso',      'Electron_mvaFall17Iso'     ),
    ('Electron_mvaFall17V2Iso_WPL',  'Electron_mvaFall17Iso_WPL' ),
    ('Electron_mvaFall17V2Iso_WP80', 'Electron_mvaFall17Iso_WP80'),
    ('Electron_mvaFall17V2Iso_WP90', 'Electron_mvaFall17Iso_WP90'),
    ('HLT_Ele32_WPTight_Gsf',        False                       ),
  ]
  fullbranchlist = tree.GetListOfBranches()
  for newbranch, oldbranch in branches:
    if newbranch not in fullbranchlist:
      if isinstance(oldbranch,str):
        print("checkBranches: directing '%s' -> '%s'"%(newbranch,oldbranch))
        exec("setattr(Event,newbranch,property(lambda self: self._tree.readBranch('%s')))"%oldbranch)
      else:
        print("checkBranches: directing '%s' -> %s"%(newbranch,oldbranch))
        exec("setattr(Event,newbranch,%s)"%(oldbranch))
        
  
def setBranchStatuses(tree,otherbranches=[ ]):
  """Activate or deactivate branch statuses."""
  tree.SetBranchStatus('*',0)
  branches = [
   'run', 'luminosityBlock', 'event', 'PV_*', 'Pileup_*', 'Flag_*', 'HLT_*',
   'LHE_*', 'nGenPart', 'GenPart_*', 'GenMET_*', 'nGenVisTau', 'GenVisTau_*', 'genWeight',
   'nElectron', 'Electron_*', 'nMuon', 'Muon_*', 'nTau', 'Tau_*',
   'nJet', 'Jet_*', 'MET_*',
  ]
  for branchname in branches+otherbranches:
   tree.SetBranchStatus(branchname,1)
  

def getVLooseTauIso(year):
  """Return a method to check whether event passes the VLoose working
  point of all available tau IDs. (For tau ID measurement.)"""
  return lambda e,i: ord(e.Tau_idMVAoldDM[i])>0 or ord(e.Tau_idMVAnewDM2017v2[i])>0 or ord(e.Tau_idMVAoldDM2017v1[i])>0 or ord(e.Tau_idMVAoldDM2017v2[i])>0
  
def getMETFilters(year,ULtag,isData):
  """Return a method to check if an event passes the recommended MET filters."""
  if year == 2016:
    if isData:
      return lambda e: e.Flag_goodVertices and e.Flag_HBHENoiseFilter and e.Flag_HBHENoiseIsoFilter and e.Flag_globalSuperTightHalo2016Filter and e.Flag_BadPFMuonFilter and e.Flag_EcalDeadCellTriggerPrimitiveFilter and e.Flag_eeBadScFilter
    else:
      return lambda e: e.Flag_goodVertices and e.Flag_HBHENoiseFilter and e.Flag_HBHENoiseIsoFilter and e.Flag_globalSuperTightHalo2016Filter and e.Flag_BadPFMuonFilter and e.Flag_EcalDeadCellTriggerPrimitiveFilter
  else:
    if ULtag=="UL":
        #CHECK once recommendations updated
        if isData:
            return lambda e: e.Flag_goodVertices and e.Flag_HBHENoiseFilter and e.Flag_HBHENoiseIsoFilter and e.Flag_globalSuperTightHalo2016Filter and e.Flag_BadPFMuonFilter and e.Flag_ecalBadCalibFilter and e.Flag_EcalDeadCellTriggerPrimitiveFilter and e.Flag_eeBadScFilter
        else:
            return lambda e: e.Flag_goodVertices and e.Flag_HBHENoiseFilter and e.Flag_HBHENoiseIsoFilter and e.Flag_globalSuperTightHalo2016Filter and e.Flag_BadPFMuonFilter and e.Flag_ecalBadCalibFilter and e.Flag_EcalDeadCellTriggerPrimitiveFilter
    else:
        if isData:
            return lambda e: e.Flag_goodVertices and e.Flag_HBHENoiseFilter and e.Flag_HBHENoiseIsoFilter and e.Flag_globalSuperTightHalo2016Filter and e.Flag_BadPFMuonFilter and e.Flag_ecalBadCalibFilterV2 and e.Flag_EcalDeadCellTriggerPrimitiveFilter and e.Flag_eeBadScFilter
        else:
            return lambda e: e.Flag_goodVertices and e.Flag_HBHENoiseFilter and e.Flag_HBHENoiseIsoFilter and e.Flag_globalSuperTightHalo2016Filter and e.Flag_BadPFMuonFilter and e.Flag_ecalBadCalibFilterV2 and e.Flag_EcalDeadCellTriggerPrimitiveFilter
    

def Tau_idIso(event,i):
  raw = event.Tau_rawIso[i]
  if event.Tau_photonsOutsideSignalCone[i]/event.Tau_pt[i]<0.10:
    return 0 if raw>4.5 else 1 if raw>3.5 else 3 if raw>2.5 else 7 if raw>1.5 else 15 if raw>0.8 else 31 # VVLoose, VLoose, Loose, Medium, Tight
  return 0 if raw>4.5 else 1 if raw>3.5 else 3 # VVLoose, VLoose
  

root_dtype = {
  float: 'D',  int: 'I',  bool: 'O',
  'f':   'D',  'i': 'I',  '?':  'O',  'b': 'b'
}
num_dtype = {
  'D':   'f',  'I': 'i',  'O':  '?',  'b': 'b'
}

class TreeProducerCommon(object):
    
    def __init__(self, name):
        
        print('TreeProducerCommon is called', name)
        
        # TREE
        self.outputfile = ROOT.TFile(name, 'RECREATE')
        self.tree = TTree('tree','tree')
        
        # HISTOGRAM
        self.cutflow = TH1D('cutflow', 'cutflow',  25, 0,  25)
        self.pileup  = TH1D('pileup',  'pileup',  100, 0, 100)
        
        ## CHECK genPartFlav
        #self.flags_LTF_DM1 = TH1D('flags_LTF_DM1', "flags for l #rightarrow #tau_{h}, DM1", 18, 0, 18)
        #self.flags_LTF_DM0 = TH1D('flags_LTF_DM0', "flags for l #rightarrow #tau_{h}, DM0", 18, 0, 18)
        #self.flags_LTF_mis = TH1D('flags_LTF_mis', "flags for l #rightarrow #tau_{h}, DM1, wrong genPartFlav", 18, 0, 18)
        #self.flags_LTF_DM1_sn1 = TH1D('flags_LTF_DM1_sn1', "flags for l #rightarrow #tau_{h}, DM1 (status!=1)", 18, 0, 18)
        #self.flags_LTF_DM0_sn1 = TH1D('flags_LTF_DM0_sn1', "flags for l #rightarrow #tau_{h}, DM0 (status!=1)", 18, 0, 18)
        #self.flags_LTF_mis_sn1 = TH1D('flags_LTF_mis_sn1', "flags for l #rightarrow #tau_{h}, DM1, wrong genPartFlav (status!=1)", 18, 0, 18)
        #for hist in [self.flags_LTF_DM1, self.flags_LTF_DM0, self.flags_LTF_mis, self.flags_LTF_DM0_sn1, self.flags_LTF_DM1_sn1, self.flags_LTF_mis_sn1]:
        #  hist.GetXaxis().SetBinLabel( 1,  "isPrompt"                            )
        #  hist.GetXaxis().SetBinLabel( 2,  "isDirectPromptTauDecayProduct"       )
        #  hist.GetXaxis().SetBinLabel( 3,  "isHardProcess"                       )
        #  hist.GetXaxis().SetBinLabel( 4,  "fromHardProcess"                     )
        #  hist.GetXaxis().SetBinLabel( 5,  "isDirectHardProcessTauDecayProduct"  )
        #  hist.GetXaxis().SetBinLabel( 6,  "fromHardProcessBeforeFSR"            )
        #  hist.GetXaxis().SetBinLabel( 7,  "isFirstCopy"                         )
        #  hist.GetXaxis().SetBinLabel( 8,  "isLastCopy"                          )
        #  hist.GetXaxis().SetBinLabel( 9,  "isLastCopyBeforeFSR"                 )
        #  hist.GetXaxis().SetBinLabel(10,  "status==1"                           )
        #  hist.GetXaxis().SetBinLabel(11,  "status==23"                          )
        #  hist.GetXaxis().SetBinLabel(12,  "status==44"                          )
        #  hist.GetXaxis().SetBinLabel(13,  "status==51"                          )
        #  hist.GetXaxis().SetBinLabel(14,  "status==52"                          )
        #  hist.GetXaxis().SetBinLabel(15,  "other status"                        )
        #  hist.GetXaxis().SetLabelSize(0.041)
        #self.genmatch_corr     = TH2D("genmatch_corr","correlation between Tau_genPartFlav and genmatch",6,0,6,6,0,6)
        #self.genmatch_corr_DM0 = TH2D("genmatch_corr_DM0","correlation between Tau_genPartFlav and genmatch for DM0",6,0,6,6,0,6)
        #self.genmatch_corr_DM1 = TH2D("genmatch_corr_DM1","correlation between Tau_genPartFlav and genmatch for DM1",6,0,6,6,0,6)
        
        
        #############
        #   EVENT   #
        #############
        
        self.addBranch('run',                     int)
        self.addBranch('lumi',                    int)
        self.addBranch('event',                   int)
        self.addBranch('isData',                  bool)
        
        self.addBranch('nPU',                     int)
        self.addBranch('nTrueInt',                int)
        self.addBranch('npvs',                    int)
        self.addBranch('npvsGood',                int)
        self.addBranch('LHE_Njets',               int)
        self.addBranch('metfilter',               bool)
        
        
        ##############
        #   WEIGHT   #
        ##############
        
        self.addBranch('genweight',               float)
        self.addBranch('weight',                  float)
        self.addBranch('trigweight',              float)
        self.addBranch('puweight',                float)
        self.addBranch('zptweight',               float)
        self.addBranch('ttptweight',              float)
        self.addBranch('idisoweight_1',           float)
        self.addBranch('idisoweight_2',           float)
        self.addBranch('btagweight',              float)
        
        
        ############
        #   JETS   #
        ############
        
        self.addBranch('njets',                   int)
        self.addBranch('njets50',                 int)
        self.addBranch('ncjets',                  int)
        self.addBranch('nfjets',                  int)
        self.addBranch('nbtag',                   int)
        
        self.addBranch('jpt_1',                   float)
        self.addBranch('jeta_1',                  float)
        self.addBranch('jphi_1',                  float)
        self.addBranch('jdeepb_1',                float)
        self.addBranch('jpt_2',                   float)
        self.addBranch('jeta_2',                  float)
        self.addBranch('jphi_2',                  float)
        self.addBranch('jdeepb_2',                float)
        
        self.addBranch('bpt_1',                   float)
        self.addBranch('beta_1',                  float)
        self.addBranch('bpt_2',                   float)
        self.addBranch('beta_2',                  float)
        
        self.addBranch('met',                     float)
        self.addBranch('metphi',                  float)
        self.addBranch('genmet',                  float)
        self.addBranch('genmetphi',               float)
        ###self.addBranch('puppimet',                float)
        ###self.addBranch('puppimetphi',             float)
        ###self.addBranch('metsignificance',         float)
        ###self.addBranch('metcovXX',                float)
        ###self.addBranch('metcovXY',                float)
        ###self.addBranch('metcovYY',                float)
        ###self.addBranch('fixedGridRhoFastjetAll',  float)
        
        
        #############
        #   OTHER   #
        #############
        
        self.addBranch('pfmt_1',                  float)
        self.addBranch('pfmt_2',                  float)
        self.addBranch('m_vis',                   float)
        self.addBranch('pt_ll',                   float)
        self.addBranch('dR_ll',                   float)
        self.addBranch('dphi_ll',                 float)
        self.addBranch('deta_ll',                 float)
        
        self.addBranch('pzetamiss',               float)
        self.addBranch('pzetavis',                float)
        self.addBranch('dzeta',                   float)
        
        self.addBranch('dilepton_veto',           bool)
        self.addBranch('extraelec_veto',          bool)
        self.addBranch('extramuon_veto',          bool)
        self.addBranch('lepton_vetos',            bool)
        
        self.addBranch('ngentauhads',             int)
        self.addBranch('ngentaus',                int)
        
        self.addBranch('m_genboson',              float)
        self.addBranch('pt_genboson',             float)
        
        #self.addBranch('m_taub',                    float)
        #self.addBranch('m_taumub',                  float)
        #self.addBranch('m_tauj',                    float)
        #self.addBranch('m_muj',                     float)
        #self.addBranch('m_coll_muj',                float)
        #self.addBranch('m_coll_tauj',               float)
        #self.addBranch('mt_coll_muj',               float)
        #self.addBranch('mt_coll_tauj',              float)
        #self.addBranch('m_max_lj',                  float)
        #self.addBranch('m_max_lb',                  float)
        #self.addBranch('m_mub',                     float)
        
        self.nPU[0]           = -1
        self.nTrueInt[0]      = -1
        self.LHE_Njets[0]     = -1
        
        self.weight[0]        = 1.
        self.genweight[0]     = 1.
        self.trigweight[0]    = 1.
        self.puweight[0]      = 1.
        self.idisoweight_1[0] = 1.
        self.idisoweight_2[0] = 1.
        self.btagweight[0]    = 1.
        self.zptweight[0]     = 1.
        self.ttptweight[0]    = 1.
        self.genmet[0]        = -1
        self.genmetphi[0]     = -9
        
        self.m_genboson[0]    = -1
        self.pt_genboson[0]   = -1
        
    def addBranch(self, name, dtype=float):
        """Add branch with a given name, and create an array of the same name as address."""
        if hasattr(self,name):
          print("ERROR! TreeProducerCommon.addBranch: Branch of name '%s' already exists!"%(name))
          exit(1)
        setattr(self,name,num.zeros(1,dtype=dtype))
        self.tree.Branch(name, getattr(self,name), '%s/%s'%(name,root_dtype[dtype]))
        
    def endJob(self):
        self.outputfile.Write()
        self.outputfile.Close()
        


class DiLeptonBasicClass:
    def __init__(self, id1, pt1, iso1, id2, pt2, iso2):
        self.id1  = id1
        self.id2  = id2
        self.pt1  = pt1
        self.pt2  = pt2
        self.iso1 = iso1
        self.iso2 = iso2
        
    def __gt__(self, odilep):
        """Order dilepton pairs according to the pT of both objects first, then in isolation."""
        if   self.pt1  != odilep.pt1:  return self.pt1  > odilep.pt1  # greater = higher pT
        elif self.pt2  != odilep.pt2:  return self.pt2  > odilep.pt2  # greater = higher pT
        elif self.iso1 != odilep.iso1: return self.iso1 < odilep.iso1 # greater = smaller isolation
        elif self.iso2 != odilep.iso2: return self.iso2 < odilep.iso2 # greater = smaller isolation
        return True
    
class LeptonTauPair(DiLeptonBasicClass):
    def __gt__(self, oltau):
        """Override for tau isolation."""
        if   self.pt1  != oltau.pt1:  return self.pt1  > oltau.pt1  # greater = higher pT
        elif self.pt2  != oltau.pt2:  return self.pt2  > oltau.pt2  # greater = higher pT
        elif self.iso1 != oltau.iso1: return self.iso1 < oltau.iso1 # greater = smaller lepton isolation
        elif self.iso2 != oltau.iso2: return self.iso2 > oltau.iso2 # greater = larger tau isolation
        return True
    
class DiTauPair(DiLeptonBasicClass):
    def __gt__(self, oditau):
        """Override for tau isolation."""
        if   self.pt1  != oditau.pt1:  return self.pt1  > oditau.pt1  # greater = higher pT
        elif self.pt2  != oditau.pt2:  return self.pt2  > oditau.pt2  # greater = higher pT
        elif self.iso1 != oditau.iso1: return self.iso1 > oditau.iso1 # greater = larger tau isolation
        elif self.iso2 != oditau.iso2: return self.iso2 > oditau.iso2 # greater = larger tau isolation
        return True
    


def bestDiLepton(diLeptons):
    """Take best dilepton pair."""
    if len(diLeptons)==1:
        return diLeptons[0]
    #least_iso_highest_pt = lambda dl: (-dl.tau1_pt, -dl.tau2_pt, dl.tau2_iso, -dl.tau1_iso)
    #return sorted(diLeptons, key=lambda dl: least_iso_highest_pt(dl), reverse=False)[0]
    return sorted(diLeptons, reverse=True)[0]
    

def deltaR(eta1, phi1, eta2, phi2):
    """Compute DeltaR."""
    deta = eta1 - eta2
    dphi = deltaPhi(phi1, phi2)
    return sqrt( deta*deta + dphi*dphi )
    
def deltaPhi(phi1, phi2):
    """Computes Delta phi, handling periodic limit conditions."""
    res = phi1 - phi2
    while res > pi:
      res -= 2*pi
    while res < -pi:
      res += 2*pi
    return res
    
def hasBit(value,bit):
  """Check if i'th bit is set to 1, i.e. binary of 2^(i-1),
  from the right to the left, starting from position i=0."""
  #return bin(value)[-bit-1]=='1'
  #return format(value,'b').zfill(bit+1)[-bit-1]=='1'
  return (value & (1 << bit))>0

def genmatch(event,index,out=None):
    """Match reco tau to gen particles, as there is a bug in the nanoAOD matching
    for lepton to tau fakes of taus reconstructed as DM1."""
    genmatch  = 0
    dR_min    = 0.2
    particles = Collection(event,'GenPart')
    eta_reco  = event.Tau_eta[index]
    phi_reco  = event.Tau_phi[index]
    
    # lepton -> tau fakes
    for id in range(event.nGenPart):
      particle = particles[id]
      PID = abs(particle.pdgId)
      if (particle.status!=1 and PID!=13) or particle.pt<8: continue
      dR = deltaR(eta_reco,phi_reco,particle.eta,particle.phi)
      if dR<dR_min:
        if hasBit(particle.statusFlags,0): # isPrompt
          if   PID==11: genmatch = 1; dR_min = dR
          elif PID==13: genmatch = 2; dR_min = dR
        elif hasBit(particle.statusFlags,5): # isDirectPromptTauDecayProduct
          if   PID==11: genmatch = 3; dR_min = dR
          elif PID==13: genmatch = 4; dR_min = dR
    
    # real tau leptons
    for id in range(event.nGenVisTau):
      dR = deltaR(eta_reco,phi_reco,event.GenVisTau_eta[id],event.GenVisTau_phi[id])
      if dR<dR_min:
        dR_min = dR
        genmatch = 5
    
    return genmatch
    


def genmatchCheck(event,index,out):
    """Match reco tau to gen particles, as there is a bug in the nanoAOD matching
    for lepton to tau fakes of taus reconstructed as DM1."""
    #print '-'*80
    genmatch  = 0
    #partmatch_s1 = None
    #partmatch_sn1 = None # status != 1
    dR_min    = 1.0
    particles = Collection(event,'GenPart')
    eta_reco  = event.Tau_eta[index]
    phi_reco  = event.Tau_phi[index]
    
    # lepton -> tau fakes
    for id in range(event.nGenPart):
      particle = particles[id]
      PID = abs(particle.pdgId)
      if particle.status!=1 or particle.pt<8: continue
      #if (particle.status!=1 and PID!=13) or particle.pt<8: continue
      dR = deltaR(eta_reco,phi_reco,particle.eta,particle.phi)
      if dR<dR_min:
        if hasBit(particle.statusFlags,0): # isPrompt
          if   PID==11:
            genmatch = 1; dR_min = dR
            #if particle.status==1: partmatch_s1 = particle
            #else:                  partmatch_sn1 = particle
          elif PID==13:
            genmatch = 2; dR_min = dR
            #if particle.status==1: partmatch_s1 = particle
            #else:                  partmatch_sn1 = particle
        elif hasBit(particle.statusFlags,5): # isDirectPromptTauDecayProduct
          if   PID==11:
            genmatch = 3; dR_min = dR
            #if particle.status==1: partmatch_s1 = particle
            #else:                  partmatch_sn1 = particle
          elif PID==13:
            genmatch = 4; dR_min = dR
            #if particle.status==1: partmatch_s1 = particle
            #else:                  partmatch_sn1 = particle
        #if particle.status!=1 and particle.status!=23:
        # mother = abs(particles[particle.genPartIdxMother].pdgId) if hasattr(particle,'genPartIdxMother') and particle.genPartIdxMother>0 else 0
        # print "%3d: PID=%3d, mass=%3.1f, pt=%4.1f, status=%2d, mother=%2d, statusFlags=%5d (%16s), isPrompt=%d, isDirectPromptTauDecayProduct=%d, fromHardProcess=%1d, isHardProcessTauDecayProduct=%1d, isDirectHardProcessTauDecayProduct=%1d"%\
        # (id,particle.pdgId,particle.mass,particle.pt,particle.status,mother,particle.statusFlags,bin(particle.statusFlags),hasBit(particle.statusFlags,0),hasBit(particle.statusFlags,5),hasBit(particle.statusFlags,8),hasBit(particle.statusFlags,9),hasBit(particle.statusFlags,10))
    
    # real tau leptons
    for id in range(event.nGenVisTau):
      dR = deltaR(eta_reco,phi_reco,event.GenVisTau_eta[id],event.GenVisTau_phi[id])
      if dR<dR_min:
        dR_min = dR
        genmatch = 5
    
    ## CHECKS
    #if genmatch!=ord(event.Tau_genPartFlav[index]):
    # #mother = abs(particles[partmatch_s1.genPartIdxMother].pdgId) if hasattr(partmatch_s1,'genPartIdxMother') else 0
    # #print "gen mismatch: Tau_genPartFlav = %s, genmatch = %s, Tau_decayMode = %2s, mother = %s"%(ord(event.Tau_genPartFlav[index]),genmatch,event.Tau_decayMode[index],mother)
    # if genmatch>0 and genmatch<5 and event.Tau_decayMode[index]==1:
    #   if partmatch_s1:
    #     fillFlagHistogram(out.flags_LTF_mis,partmatch_s1)
    #   elif partmatch_sn1:
    #     fillFlagHistogram(out.flags_LTF_mis_sn1,partmatch_sn1)
    #
    ## CHECK status and flags
    #if genmatch>0 and genmatch<5:
    # if event.Tau_decayMode[index]==0:
    #   if partmatch_s1:
    #     fillFlagHistogram(out.flags_LTF_DM0,partmatch_s1)       
    #   elif partmatch_sn1:
    #     fillFlagHistogram(out.flags_LTF_DM0_sn1,partmatch_sn1)
    # elif event.Tau_decayMode[index]==1:
    #   if partmatch_s1:
    #     fillFlagHistogram(out.flags_LTF_DM1,partmatch_s1)
    #   elif partmatch_sn1:
    #     fillFlagHistogram(out.flags_LTF_DM1_sn1,partmatch_sn1)
    #     #if partmatch_sn1.status not in [23,44,52]:
    #     #  print partmatch_sn1.status
    #
    ## CHECK correlation
    #out.genmatch_corr.Fill(ord(event.Tau_genPartFlav[index]),genmatch)
    #if event.Tau_decayMode[index]==0:
    # out.genmatch_corr_DM0.Fill(ord(event.Tau_genPartFlav[index]),genmatch)
    #if event.Tau_decayMode[index]==1:
    # out.genmatch_corr_DM1.Fill(ord(event.Tau_genPartFlav[index]),genmatch)
    
    return genmatch





def fillFlagHistogram(hist,particle):
  """Fill histograms with status flags for genPartFlav check."""
  if hasBit(particle.statusFlags, 0): hist.Fill( 0) # isPrompt
  if hasBit(particle.statusFlags, 5): hist.Fill( 1) # isDirectPromptTauDecayProduct
  if hasBit(particle.statusFlags, 7): hist.Fill( 2) # isHardProcess
  if hasBit(particle.statusFlags, 8): hist.Fill( 3) # fromHardProcess
  if hasBit(particle.statusFlags,10): hist.Fill( 4) # isDirectHardProcessTauDecayProduct
  if hasBit(particle.statusFlags,11): hist.Fill( 5) # fromHardProcessBeforeFSR
  if hasBit(particle.statusFlags,12): hist.Fill( 6) # isFirstCopy
  if hasBit(particle.statusFlags,13): hist.Fill( 7) # isLastCop
  if hasBit(particle.statusFlags,14): hist.Fill( 8) # isLastCopyBeforeFSR
  if   particle.status==1:            hist.Fill( 9) # status==1
  elif particle.status==23:           hist.Fill(10) # status==23
  elif particle.status==44:           hist.Fill(11) # status==44
  elif particle.status==51:           hist.Fill(12) # status==51
  elif particle.status==52:           hist.Fill(13) # status==52
  else:                               hist.Fill(14) # other status



def extraLeptonVetos(event, muon_idxs, electron_idxs, channel):
    
    extramuon_veto = False
    extraelec_veto = False
    dilepton_veto  = False
    
    LooseMuons = [ ]
    for imuon in range(event.nMuon):
        if event.Muon_pt[imuon] < 10: continue
        if abs(event.Muon_eta[imuon]) > 2.4: continue
        if abs(event.Muon_dz[imuon]) > 0.2: continue
        if abs(event.Muon_dxy[imuon]) > 0.045: continue
        if event.Muon_pfRelIso04_all[imuon] > 0.3: continue
        if event.Muon_mediumId[imuon] > 0.5 and (imuon not in muon_idxs):
            extramuon_veto = True
        if event.Muon_pt[imuon] > 15 and event.Muon_isPFcand[imuon]: #Muon_isGlobal[imuon] and Muon_isTracker[imuon]
            LooseMuons.append(imuon)
    
    LooseElectrons = [ ]
    for ielectron in range(event.nElectron):
        if event.Electron_pt[ielectron] < 10: continue
        if abs(event.Electron_eta[ielectron]) > 2.5: continue
        if abs(event.Electron_dz[ielectron]) > 0.2: continue
        if abs(event.Electron_dxy[ielectron]) > 0.045: continue
        if event.Electron_pfRelIso03_all[ielectron] > 0.3: continue
        if event.Electron_convVeto[ielectron] ==1 and ord(event.Electron_lostHits[ielectron]) <= 1 and event.Electron_mvaFall17V2Iso_WP90[ielectron] > 0.5 and (ielectron not in electron_idxs):
            extraelec_veto = True
        if event.Electron_pt[ielectron] > 15 and event.Electron_mvaFall17V2Iso_WPL[ielectron] > 0.5:
            LooseElectrons.append(ielectron)
    
    if channel=='mutau':
      for idx1 in LooseMuons:
        for idx2 in LooseMuons:
            if idx1 >= idx2: continue 
            dR = deltaR(event.Muon_eta[idx1], event.Muon_phi[idx1], 
                        event.Muon_eta[idx2], event.Muon_phi[idx2])
            if event.Muon_charge[idx1] * event.Muon_charge[idx2] < 0 and dR > 0.15:
                dilepton_veto = True
    
    if channel=='eletau':
      for idx1 in LooseElectrons:
        for idx2 in LooseElectrons:
            if idx1 >= idx2: continue 
            dR = deltaR(event.Electron_eta[idx1], event.Electron_phi[idx1], 
                        event.Electron_eta[idx2], event.Electron_phi[idx2])
            if event.Electron_charge[idx1] * event.Electron_charge[idx2] < 0 and dR > 0.15:
                dilepton_veto = True
    
    return extramuon_veto, extraelec_veto, dilepton_veto
