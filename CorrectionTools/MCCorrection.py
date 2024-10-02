#! /bin/usr/env bash
import os, re
from ROOT import TFile, TH2F, TLorentzVector
import numpy as np
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Event

class MCCorrection:
    
    def __init__(self, year,order="NLO"):
        filename_tt = "/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/MCCorrection/root/MCCorr_tt_UL%s.root"%year
        rootfile_tt = TFile(filename_tt,"READ")
        self.hist_tt = rootfile_tt.Get("TTcorr")
        self.wt_tt =self.hist_tt.GetFunction("pol0").GetParameter(0)
        self.hist_tt_pol1 = rootfile_tt.Get("TTcorr_pol1")
        self.hist_tt_pol1.SetDirectory(0)
        self.hist_tt_pol2 = rootfile_tt.Get("TTcorr_pol2")
        self.hist_tt_pol2.SetDirectory(0)
        rootfile_tt.Close()
        filename_w_mutau = "/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/MCCorrection/root/MCCorr_mutau_UL%s.root"%year
        rootfile_w_mutau = TFile(filename_w_mutau,"READ")
        self.hist_w_mutau = rootfile_w_mutau.Get("Wcorr")
        self.hist_w_mutau.SetDirectory(0)
        rootfile_w_mutau.Close()
        filename_w_etau = "/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/MCCorrection/root/MCCorr_etau_UL%s.root"%year
        rootfile_w_etau = TFile(filename_w_etau,"READ")
        self.hist_w_etau = rootfile_w_etau.Get("Wcorr")
        self.hist_w_etau.SetDirectory(0)
        rootfile_w_etau.Close()
        filename_dy = "/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/MCCorrection/root/MCCorr_mumu_UL%s.root"%year
        rootfile_dy = TFile(filename_dy,"READ")
        if order=="LO":
          self.hist_dy = rootfile_dy.Get("DYJetscorr")
          self.hist_dy_1btag = rootfile_dy.Get("DYJetscorr_1btag")
          self.hist_dy_2btag = rootfile_dy.Get("DYJetscorr_2btag")
        elif order=="NLO":
          self.hist_dy = rootfile_dy.Get("DYJetscorr_NLO")
          self.hist_dy_1btag = rootfile_dy.Get("DYJetscorr_NLO_1btag")
          self.hist_dy_2btag = rootfile_dy.Get("DYJetscorr_NLO_2btag")
          self.hist_dy_up = rootfile_dy.Get("DYJetscorr_NLO_up")
          self.hist_dy_1btag_up = rootfile_dy.Get("DYJetscorr_NLO_1btag_up")
          self.hist_dy_2btag_up = rootfile_dy.Get("DYJetscorr_NLO_2btag_up")
          self.hist_dy_down = rootfile_dy.Get("DYJetscorr_NLO_down")
          self.hist_dy_1btag_down = rootfile_dy.Get("DYJetscorr_NLO_1btag_down")
          self.hist_dy_2btag_down = rootfile_dy.Get("DYJetscorr_NLO_2btag_down")
        self.hist_dy.SetDirectory(0)
        self.hist_dy_1btag.SetDirectory(0)
        self.hist_dy_2btag.SetDirectory(0)
        self.hist_dy_up.SetDirectory(0)
        self.hist_dy_1btag_up.SetDirectory(0)
        self.hist_dy_2btag_up.SetDirectory(0)
        self.hist_dy_down.SetDirectory(0)
        self.hist_dy_1btag_down.SetDirectory(0)
        self.hist_dy_2btag_down.SetDirectory(0)
        rootfile_dy.Close()
        

    def getWeight(self,pt,mass):
      if pt==0. or mass==0.:
        return 1.
      if pt>200.:
        pt=200.-1.
      if mass<50.: mass=50.+1.
      if mass>150.: mass=150.-1. 
      binx = self.hist_dy.GetXaxis().FindBin(pt)
      biny = self.hist_dy.GetYaxis().FindBin(mass)
      weight = self.hist_dy.GetBinContent(binx,biny)
      if weight==0.: weight=1.
      return weight

    def getWeight_btag(self,pt,mass,btag,var):
      if pt==0. or mass==0.:
        return 1.
      if pt>200.:
        pt=200.-1.
      if mass<50.: mass=50.+1.
      if mass>150.: mass=150.-1.
      if btag==1:
          if var=="":
              binx = self.hist_dy_1btag.GetXaxis().FindBin(pt)
              biny = self.hist_dy_1btag.GetYaxis().FindBin(mass)
              weight = self.hist_dy_1btag.GetBinContent(binx,biny)
          elif var=="up":
              binx = self.hist_dy_1btag_up.GetXaxis().FindBin(pt)
              biny = self.hist_dy_1btag_up.GetYaxis().FindBin(mass)
              weight = self.hist_dy_1btag_up.GetBinContent(binx,biny)
          elif var=="down":
              binx = self.hist_dy_1btag_down.GetXaxis().FindBin(pt)
              biny = self.hist_dy_1btag_down.GetYaxis().FindBin(mass)
              weight = self.hist_dy_1btag_down.GetBinContent(binx,biny)
      elif btag>=2:
          if var=="":
              binx = self.hist_dy_2btag.GetXaxis().FindBin(pt)
              biny = self.hist_dy_2btag.GetYaxis().FindBin(mass)
              weight = self.hist_dy_2btag.GetBinContent(binx,biny)
          elif var=="up":
              binx = self.hist_dy_2btag_up.GetXaxis().FindBin(pt)
              biny = self.hist_dy_2btag_up.GetYaxis().FindBin(mass)
              weight = self.hist_dy_2btag_up.GetBinContent(binx,biny)
          elif var=="down":
              binx = self.hist_dy_2btag_down.GetXaxis().FindBin(pt)
              biny = self.hist_dy_2btag_down.GetYaxis().FindBin(mass)
              weight = self.hist_dy_2btag_down.GetBinContent(binx,biny)
      elif btag==0:
        weight = 1.
      if weight==0.: weight=1.
      return weight

    def getWeight_tt(self):
      return self.wt_tt

    def getWeight_tt_pol1(self,pt):
        wt_tt_pol1 = self.hist_tt_pol1.GetFunction("pol1").Eval(pt)
        return wt_tt_pol1

    def getWeight_tt_pol2(self,pt):
        wt_tt_pol2 = self.hist_tt_pol2.GetFunction("pol2").Eval(pt)
        return wt_tt_pol2

    def getWeight_w(self,isMuTau,isETau,pt):
      if pt>130.:
          pt = 125.
      if isMuTau:
        wt_w = self.hist_w_mutau.GetFunction("pol1").Eval(pt)
      elif isETau:
        wt_w = self.hist_w_etau.GetFunction("pol1").Eval(pt)
      else:
          return 1. #if not mutau or etau
      return wt_w


if __name__=="__main__":
    MCCorrection = MCCorrection(2017,"NLO")
    for i in range(220):
        for j in range(140):
            weight = MCCorrection.getWeight_btag(i,j,2)
            #weight = MCCorrection.getWeight(i,j)
            if weight < -10. or weight > 10.:
                print("pt:",i, "mass:",j," dy weight:",weight)
    #print("tt weight:",MCCorrection.getWeight_tt())
    #print("w weight:",MCCorrection.getWeight_w(False,True,140.))
