#! /bin/usr/env python
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import ROOT
import os
import numpy as np
ROOT.PyConfig.IgnoreCommandLineOptions = True


  
class puWeightProducer(Module):
    def __init__(self,year,ispreVFP):
        CMSSW_BASE = "/work/pbaertsc/bbh/CMSSW_12_1_1"
        if year == 2018:
            datafile = os.path.join(CMSSW_BASE, "src/PhysicsTools/NanoAODTools/python/postprocessing/data/pileup/PileupHistogram-goldenJSON-13tev-UL2018_withVar.root")
            mcfile = os.path.join(CMSSW_BASE, "src/PhysicsTools/NanoAODTools/python/postprocessing/data/pileup/mcPileupUL2018.root")
        elif year == 2017:
            datafile = os.path.join(CMSSW_BASE, "src/PhysicsTools/NanoAODTools/python/postprocessing/data/pileup/PileupHistogram-goldenJSON-13tev-UL2017_withVar.root")
            mcfile = os.path.join(CMSSW_BASE, "src/PhysicsTools/NanoAODTools/python/postprocessing/data/pileup/mcPileupUL2017.root")
        elif year == 2016:
            mcfile = os.path.join(CMSSW_BASE, "src/PhysicsTools/NanoAODTools/python/postprocessing/data/pileup/mcPileupUL2016.root")
            if ispreVFP:
                datafile = os.path.join(CMSSW_BASE, "src/PhysicsTools/NanoAODTools/python/postprocessing/data/pileup/PileupHistogram-goldenJSON-13tev-UL2016BF_withVar.root")
            else:
                datafile = os.path.join(CMSSW_BASE, "src/PhysicsTools/NanoAODTools/python/postprocessing/data/pileup/PileupHistogram-goldenJSON-13tev-UL2016GH_withVar.root")
        mchist_name="pu_mc"
        datahist_name="pileup"
        norm=True
        verbose=False
        nvtx_var="Pileup_nTrueInt"
        doSysVar=True
        self.datahist = self.loadHisto(datafile, datahist_name)
        self.datahist_plus = self.loadHisto(datafile, datahist_name + "_plus")
        self.datahist_minus = self.loadHisto(datafile, datahist_name + "_minus")
        self.mchist = self.loadHisto(mcfile, mchist_name)
        self.fixLargeWeights = True  # temporary fix
        self.norm = norm
        self.verbose = verbose
        self.nvtxVar = nvtx_var
        self.doSysVar = doSysVar
        self.worker = ROOT.WeightCalculatorFromHistogram(self.mchist, self.datahist, self.norm, self.fixLargeWeights,self.verbose)
        self.worker_plus = ROOT.WeightCalculatorFromHistogram(self.mchist, self.datahist_plus, self.norm, self.fixLargeWeights,self.verbose)
        self.worker_minus = ROOT.WeightCalculatorFromHistogram(self.mchist, self.datahist_minus, self.norm, self.fixLargeWeights,self.verbose)


    def loadHisto(self, filename, hname):
        tf = ROOT.TFile.Open(filename)
        hist = tf.Get(hname)
        hist.SetDirectory(0)
        tf.Close()
        return hist
  

    def getWeight(self, event):
        nvtx = int(getattr(event, self.nvtxVar))
        weight = self.worker.getWeight(nvtx) if nvtx < self.mchist.GetNbinsX() else 1
        weight_plus = self.worker_plus.getWeight(nvtx) if nvtx < self.mchist.GetNbinsX() else 1
        weight_minus = self.worker_minus.getWeight(nvtx) if nvtx < self.mchist.GetNbinsX() else 1
        return [weight,weight_plus,weight_minus]




    
