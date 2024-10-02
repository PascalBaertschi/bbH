#! /bin/usr/env python
# Author: Pascal Baertschi (January 2022)
# https://twiki.cern.ch/twiki/bin/view/CMS/BTagSFMethods
# https://twiki.cern.ch/twiki/bin/view/CMSPublic/BTagCalibration
# https://twiki.cern.ch/twiki/bin/view/CMS/BtagRecommendation106XUL18
# https://twiki.cern.ch/twiki/bin/view/CMS/BtagRecommendation
# https://btv-wiki.docs.cern.ch/ScaleFactors/
# https://gitlab.cern.ch/cms-nanoAOD/jsonpog-integration/-/tree/master/
from array import array
import correctionlib
import ROOT
import os
import numpy as np
#ROOT.gROOT.ProcessLine('.L ./BTagCalibrationStandalone.cpp+')
from ROOT import TH2F, BTagCalibration, BTagCalibrationReader, TLorentzVector
from ROOT.BTagEntry import OP_LOOSE, OP_MEDIUM, OP_TIGHT, OP_RESHAPING
from ROOT.BTagEntry import FLAV_B, FLAV_C, FLAV_UDSG
from BTagSFcorr import btagSFcorr_dict

path = 'btag/'
path_json = 'jsonpog-integration/POG/BTV/'
class BTagWPs:
  """Contain b tagging working points."""
  def __init__(self, year,preVFP):
    if year==2016:
      if preVFP=="_preVFP":
        self.loose    = 0.0508
        self.medium   = 0.2598
        self.tight    = 0.6502
      else:
        self.loose    = 0.0480
        self.medium   = 0.2489
        self.tight    = 0.6377
    elif year==2017:
      self.loose    = 0.0532
      self.medium   = 0.3040
      self.tight    = 0.7476
      
    elif year==2018:
      self.loose    = 0.0490
      self.medium   = 0.2783
      self.tight    = 0.7100

  def getWP(self):
      return [self.loose,self.medium,self.tight]
  

class BTagWeightTool:
    
    def __init__(self, tagger, wp, year, preVFP):
        """Load b tag weights from CSV file."""
        #print "Loading BTagWeightTool for %s (%s WP)..."%(tagger,wp)
        
        # FILE
        if year==2016:
          if preVFP=="_preVFP":
            #csvname = path+'DeepJet_2016LegacySF_V1.csv'
            sfDir = os.path.join(path_json, "2016preVFP_UL")
            effname = path+'DeepJet_UL2016_preVFP_eff.root'
          else:
            #csvname = path+'DeepJet_2016LegacySF_V1.csv'
            sfDir = os.path.join(path_json, "2016postVFP_UL")
            effname = path+'DeepJet_UL2016_eff.root'
        elif year==2017:
          #csvname = path+'DeepJet_106XUL17SF_V2.csv'
          sfDir = os.path.join(path_json, "2017_UL")
          effname = path+'DeepJet_UL2017_eff.root'
       
        elif year==2018:
          #csvname = path+'DeepJet_106XUL18SF.csv'
          sfDir = os.path.join(path_json, "2018_UL")
          effname = path+'DeepJet_UL2018_eff.root'

        self.btvjson = correctionlib.CorrectionSet.from_file(os.path.join(sfDir, "btagging.json.gz"))
        self.tagger = tagger
        self.year = year
        # TAGGING WP
        self.wp     = getattr(BTagWPs(year,preVFP),wp)
        self.SFcorr_dict = btagSFcorr_dict['UL%s'%year]
        # CSV READER
        self.workpoint        = 'L' if wp=='loose' else 'M' if wp=='medium' else 'T' if wp=='tight' else wp=="M"
  

        # EFFICIENCIES
        ptbins     = array('d',[10,20,30,50,70,100,140,200,300,500,1000,1500])
        etabins    = array('d',[-2.5,-1.5,0.0,1.5,2.5])
        bins       = (len(ptbins)-1,ptbins,len(etabins)-1,etabins)
        hists      = { }
        effs       = { }
        
        
        efffile    = ROOT.TFile(effname,"READ")
        for flavor in [0,4,5]:
          flavor   = flavorToString(flavor)
          histname = "%s_%s_%s"%(tagger,flavor,wp)
          effname  = "eff_%s_%s_%s"%(tagger,flavor,wp) #effname  = "%s/eff_%s_%s_%s"%(JECvar,tagger,flavor,wp)
          hists[flavor]        = TH2F(histname,histname,*bins)
          hists[flavor+'_all'] = TH2F(histname+'_all',histname+'_all',*bins)
          effs[flavor]         = efffile.Get(effname)
          hists[flavor].SetDirectory(0)
          hists[flavor+'_all'].SetDirectory(0)
          effs[flavor].SetDirectory(0)
        efffile.Close()
      
        
        #self.calib  = calib
        #self.reader = reader
        self.hists  = hists
        self.effs   = effs
       

    def tagged(self,Jet):
      return Jet.btagDeepFlavB>self.wp


    
    def getWeight(self,Jets,measurementType,sysType,samplename,isMuTau,isETau,isTTCR,isMuMu):
        """Get event weight for a given set of jets."""
        weight = 1.
        for jet in Jets:
          weight *= self.getSF(jet.pt,jet.eta,jet.partonFlavour,jet.hadronFlavour,jet.btagDeepFlavB,self.tagged(jet),measurementType,sysType)
        if measurementType=="shape" and (sysType=="central" or (weight!=1.0 and sysType!="central")):
          if isMuTau:
            channel = "mutau"
          elif isETau:
            channel = "etau"
          elif isTTCR:
            channel = "tt"
          elif isMuMu:
            channel = "mumu"
          weight = weight * self.SFcorr_dict[channel][samplename]
        return weight
    
    #def getWeight(self,Jets,measurementType,sysType,samplename,isMuTau,isETau,isTTCR,isMuMu):
    #    """Get event weight for a given set of jets."""
    #    weight = 1.
    #    for jet in Jets:
    #      weight *= self.getSF(jet.pt,jet.eta,jet.partonFlavour,jet.hadronFlavour,jet.btagDeepFlavB,self.tagged(jet),measurementType,sysType)
    #    return weight


    def getWeight_nocorr(self,Jets,measurementType,sysType):
        """Get event weight for a given set of jets."""
        weight = 1.
        for jet in Jets:
          weight *= self.getSF(jet.pt,jet.eta,jet.partonFlavour,jet.hadronFlavour,jet.btagDeepFlavB,self.tagged(jet),measurementType,sysType)
        return weight

    def getSFcorr(self,samplename,isMuTau,isETau,isTTCR,isMuMu):
        if isMuTau:
          channel = "mutau"
        elif isETau:
          channel = "etau"
        elif isTTCR:
          channel = "tt"
        elif isMuMu:
          channel = "mumu"
        return self.SFcorr_dict[channel][samplename]

    def matchSystoFlavor(self,sysType,flavor):
        if sysType=="central": return True
        sys = sysType.split("_")[1]
        if sys=="jes" and flavor in [0,5]:                         #Combined JES uncertainty
          return True
        elif sys=="lf" and flavor in [0,5]:                          #Contamination from udsg+c jets in HF region
          return True
        elif sys=="hf" and flavor in [0,5]:                        #Contamination from b+c jets in LF region
          return True
        elif (sys=="hfstats1" or sys=="hfstats2") and flavor in [0,5]:   #Linear and quadratic statistical fluctuations for b jets
          return True
        elif (sys=="lfstats1" or sys=="lfstats2") and flavor in [0,5]:   #Linear and quadratic statistical fluctuations for udsg jets
          return True
        elif (sys=="cferr1" or sys=="cferr2") and flavor==4:       #Uncertainty for charm jets
          return True
        else:
          return False

    def getSF(self,pt,eta,flavor,flavor_hadron,discriminator,tagged,measurementType,sysType):

        """Get b tag SF for a single jet."""
        FLAV = flavorToFLAV(flavor)
        if   eta>=+2.4: eta = +2.399 # BTagCalibrationReader returns zero if |eta| > 2.4
        elif eta<=-2.4: eta = -2.399
        #if pt > 1000.: pt = 999 # BTagCalibrationReader returns zero if pt > 1000
        #SF   = self.reader.eval_auto_bounds(self.sigma,FLAV,abs(eta),pt)
        if measurementType=="shape":
          if self.matchSystoFlavor(sysType,flavor_hadron):
            SF = self.btvjson["deepJet_%s"%measurementType].evaluate(sysType, flavor_hadron, abs(eta),pt,discriminator)
          else:
            SF = 1.
        else:
          if flavor_hadron==0:
            measurementType = "incl" #for light jets
          else:
            measurementType = "comb" #for b/c jets
          SF = self.btvjson["deepJet_%s"%measurementType].evaluate(sysType, self.workpoint, flavor_hadron, abs(eta),pt)
        
        if tagged or measurementType=="shape":
          weight = SF
        else:
          eff = self.getEfficiency(pt,eta,flavor)
          if eff==1:
            print("Warning! BTagWeightTool.getSF: MC efficiency is 1 for pt=%s, eta=%s, flavor=%s, SF=%s"%(pt,eta,flavor,SF))
            return 1
          else:
            weight = (1-SF*eff)/(1-eff)
        return weight

        
    def getEfficiency(self,pt,eta,flavor):
        """Get SF for one jet."""
        flavor = flavorToString(flavor)
        hist   = self.effs[flavor]
        xbin   = hist.GetXaxis().FindBin(pt)
        ybin   = hist.GetYaxis().FindBin(eta)
        if xbin==0: xbin = 1
        elif xbin>hist.GetXaxis().GetNbins(): xbin -= 1
        if ybin==0: ybin = 1
        elif ybin>hist.GetYaxis().GetNbins(): ybin -= 1
        sf     = hist.GetBinContent(xbin,ybin)
        return sf
        
    def fillEfficiencies(self,Jets):
        """Fill efficiency of MC."""
        for jet in Jets:
          flavor = flavorToString(jet.partonFlavour)
          if self.tagged(jet):
            self.hists[flavor].Fill(jet.pt,jet.eta)
          self.hists[flavor+'_all'].Fill(jet.pt,jet.eta)

        
          

    def setDirectory(self,directory,subdirname=None):
        if subdirname:
          subdir = directory.Get(subdirname)
          if not subdir:
            subdir = directory.mkdir(subdirname)
          directory = subdir
        for histname, hist in self.hists.items():
          hist.SetDirectory(directory)

def flavorToFLAV(flavor):
  return FLAV_B if abs(flavor)==5 else FLAV_C if abs(flavor)==4 or abs(flavor)==15 else FLAV_UDSG       

def flavorToString(flavor):
  return 'b' if abs(flavor)==5 else 'c' if abs(flavor)==4 else 'udsg'
  
  
if __name__=="__main__":
  WeightTool = BTagWeightTool("DeepJet", "medium", 2018, "")
  print("b")
  print("central:",round(WeightTool.getSF(25.0,0.2,5,5,0.85,True,"shape","central"),4))
  print("jes down:",round(WeightTool.getSF(25.0,0.2,5,5,0.85,True,"shape","down_jes"),4),"up:",round(WeightTool.getSF(25.0,0.2,5,5,0.85,True,"shape","up_jes"),4))
  print("lf down:",round(WeightTool.getSF(25.0,0.2,5,5,0.85,True,"shape","down_lf"),4),"up:",round(WeightTool.getSF(25.0,0.2,5,5,0.85,True,"shape","up_lf"),4))
  print("hf down:",round(WeightTool.getSF(25.0,0.2,5,5,0.85,True,"shape","down_hf"),4),"up:",round(WeightTool.getSF(25.0,0.2,5,5,0.85,True,"shape","up_hf"),4))
  print("light")
  print("central:",round(WeightTool.getSF(25.0,0.2,0,0,0.85,True,"shape","central"),4))
  print("jes down:",round(WeightTool.getSF(25.0,0.2,0,0,0.85,True,"shape","down_jes"),4),"up:",round(WeightTool.getSF(25.0,0.2,0,0,0.85,True,"shape","up_jes"),4))
  print("lf down:",round(WeightTool.getSF(25.0,0.2,0,0,0.85,True,"shape","down_lf"),4),"up:",round(WeightTool.getSF(25.0,0.2,0,0,0.85,True,"shape","up_lf"),4))
  print("hf down:",round(WeightTool.getSF(25.0,0.2,0,0,0.85,True,"shape","down_hf"),4),"up:",round(WeightTool.getSF(25.0,0.2,0,0,0.85,True,"shape","up_hf"),4))
