import ROOT
import math 
import numpy as np


root_dtype = {
  float: 'D',  int: 'I',  bool: 'O',
  'f':   'D',  'i': 'I',  '?':  'O',  'b': 'b'
}
num_dtype = {
  'D':   'f',  'I': 'i',  'O':  '?',  'b': 'b'
}

class TreeProducer(object):

    def __init__(self, name):
        print('TreeProducer is called', name)

        # TREE
        self.outputfile = ROOT.TFile(name, 'RECREATE')
        self.tree = ROOT.TTree('tree','tree')
        
        # HISTOGRAM
        
        ##################
        # trees branches #
        ##################
        self.addBranch('isMC', bool)
        self.addBranch('is2016', bool)
        self.addBranch('is2017', bool)
        self.addBranch('is2018', bool)
        self.addBranch('EventNumber', float)
        self.addBranch('LumiNumber', float)
        self.addBranch('RunNumber', float)
        self.addBranch('EventWeight', float)
        self.addBranch('GenWeight', float)
        self.addBranch('PUWeight', float)
        self.addBranch('LumiWeight', float)
        self.addBranch('Mutrigger_fired', bool)
        self.addBranch('Etrigger_fired', bool)
        self.addBranch('Mutautrigger_fired', bool)
        self.addBranch('Etautrigger_fired', bool)
        self.addBranch('L1Tau_lep1', bool)
        self.addBranch('L1Tau_lep2', bool)
        self.addBranch('L1Tau_lep1_reco', bool)
        self.addBranch('L1Tau_lep2_reco', bool)
        self.addBranch('nMuons', int)
        self.addBranch('nElectrons', int)
        self.addBranch('dimuon_pt',float)
        self.addBranch('dimuon_mass', float)
        self.addBranch('Mu1_pt', float)
        self.addBranch('Mu1_eta', float)
        self.addBranch('Mu1_phi', float)
        self.addBranch('Mu1_mass', float)
        self.addBranch('Mu1_charge', float)
        self.addBranch('Mu1_iso', float)
        self.addBranch('Mu1_fired', bool)
        self.addBranch('Mu1_mutaufired', bool)
        self.addBranch('Mu1_tag', bool)
        self.addBranch('Mu2_pt', float)
        self.addBranch('Mu2_eta', float)
        self.addBranch('Mu2_phi', float)
        self.addBranch('Mu2_mass', float)
        self.addBranch('Mu2_charge', float)
        self.addBranch('Mu2_iso', float)
        self.addBranch('Mu2_fired', bool)
        self.addBranch('Mu2_mutaufired', bool)
        self.addBranch('Mu2_tag', bool)
        self.addBranch('dielectron_pt',float)
        self.addBranch('dielectron_mass', float)
        self.addBranch('Ele1_pt', float)
        self.addBranch('Ele1_eta', float)
        self.addBranch('Ele1_phi', float)
        self.addBranch('Ele1_mass', float)
        self.addBranch('Ele1_charge', float)
        self.addBranch('Ele1_iso', float)
        self.addBranch('Ele1_fired', bool)
        self.addBranch('Ele1_etaufired', bool)
        self.addBranch('Ele1_tag', bool)
        self.addBranch('Ele2_pt', float)
        self.addBranch('Ele2_eta', float)
        self.addBranch('Ele2_phi', float)
        self.addBranch('Ele2_mass', float)
        self.addBranch('Ele2_charge', float)
        self.addBranch('Ele2_iso', float)
        self.addBranch('Ele2_fired', bool)
        self.addBranch('Ele2_etaufired', bool)
        self.addBranch('Ele2_tag', bool)
        self.addBranch('nGenMuons',int)
        self.addBranch('nGenElectrons',int)
        self.addBranch('gendimuon_pt', float)
        self.addBranch('gendimuon_mass', float)
        self.addBranch('GenMu1_pt', float)
        self.addBranch('GenMu1_eta', float)
        self.addBranch('GenMu2_pt', float)
        self.addBranch('GenMu2_eta', float)
        self.addBranch('gendielectron_pt', float)
        self.addBranch('gendielectron_mass', float)
        self.addBranch('GenEle1_pt', float)
        self.addBranch('GenEle1_eta', float)
        self.addBranch('GenEle2_pt', float)
        self.addBranch('GenEle2_eta', float)

    def addBranch(self, name, dtype=float):
        """Add branch with a given name, and create an array of the same name as address."""
        if hasattr(self,name):
          print("ERROR! TreeProducer.addBranch: Branch of name '%s' already exists!"%(name))
          exit(1)
        setattr(self,name,np.zeros(1,dtype=dtype))
        self.tree.Branch(name, getattr(self,name), '%s/%s'%(name,root_dtype[dtype]))
