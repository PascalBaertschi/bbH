#! /usr/bin/env python

import os, multiprocessing, math
import numpy as np
from array import array
from ROOT import TFile, TH1, TF1, TLorentzVector
import ROOT

from xsections import xsection

import optparse
usage = 'usage: %prog [options]'
parser = optparse.OptionParser(usage)
parser.add_option('-y', '--year', action='store', type='string', dest='year',default='2017')
parser.add_option('-f', '--filter', action='store', type='string', dest='filter', default='')
parser.add_option('-s', '--single', action='store_true', dest='single', default=False)
parser.add_option('-v', '--verbose', action='store_true', dest='verbose', default=False)

(options, args) = parser.parse_args()

filterset   = options.filter
singlecore  = options.single
verboseout  = options.verbose
year        = options.year


#origin = '/pnfs/psi.ch/cms/trivcat/store/user/pbaertsc/bbh/SingleMuon/SingleMuon_Run2016B-ver2_HIPM_UL2016_MiniAODv1_NanoAODv2-v1__UL2016/210607_123433/0000/'
origin = '/pnfs/psi.ch/cms/trivcat/store/user/pbaertsc/bbh/SingleMuon/SingleMuon_Run2016B-ver2_HIPM_UL2016_MiniAODv1_NanoAODv2-v1__UL2016_old/'
target = '/pnfs/psi.ch/cms/trivcat/store/user/pbaertsc/bbh/SingleMuon/SingleMuon_Run2016B-ver2_HIPM_UL2016_MiniAODv1_NanoAODv2-v1__UL2016/210607_123433/0000/'



#LUMI  = 36220
#LUMI  = 27220 #24470
#LUMI = 12700
#Tau21_SF = { 1.03 : [0., 0.4], 0.88 : [0.4, 0.75], }

if not os.path.exists(origin):
    print 'Origin directory', origin, 'does not exist, aborting...'
    exit()
if not os.path.exists(target):
    print 'Target directory', target,'does not exist, aborting...'
    exit()


##############################

def processFile(filename, verbose=False):
    new_filename = filename
    #if os.path.exists(new_file_name):
    #    print '  WARNING: weighted file exists, overwriting'
        #return True
    
    new_file = TFile(target+new_filename, 'RECREATE')
    new_file.cd()
    
    # Open old file
    ref_file = TFile(origin+filename, 'READ')
    obj = ref_file.Get('Events')
    # Variables declaration
    HLT_IsoMu22_eta2p1 = array('f', [0.0])
    HLT_IsoTkMu22_eta2p1 = array('f', [0.0])
    # Looping over file content
    #for key in ref_file.GetListOfKeys():
    #    obj = key.ReadObj()
    nev = obj.GetEntriesFast()
    new_file.cd()
    new_tree = obj.CopyTree("")
    # New branches
    HLT_IsoMu22_eta2p1Branch = new_tree.Branch('HLT_IsoMu22_eta2p1', HLT_IsoMu22_eta2p1, 'HLT_IsoMu22_eta2p1/F')
    HLT_IsoTkMu22_eta2p1Branch = new_tree.Branch('HLT_IsoTkMu22_eta2p1', HLT_IsoTkMu22_eta2p1, 'HLT_IsoTkMu22_eta2p1/F')
    # looping over events
    for event in range(0, obj.GetEntries()):
        obj.GetEntry(event)
        # Initialize
        HLT_IsoMu22_eta2p1[0] = 0.
        HLT_IsoTkMu22_eta2p1[0] = 0.
        # Fill the branches
        HLT_IsoMu22_eta2p1Branch.Fill()
        HLT_IsoTkMu22_eta2p1Branch.Fill()
    new_file.cd()
    new_tree.Write("", obj.kOverwrite)
    new_file.Close() 




#treelist = ["tree_1.root","tree_5.root","tree_6.root","tree_7.root","tree_8.root","tree_9.root","tree_10.root","tree_11.root","tree_12.root","tree_13.root","tree_14.root","tree_15.root","tree_40.root"]
#for tree in treelist:
#    print "processing file:",tree
#    processFile(tree)
processFile("tree_40.root") 
   
#print '\nDone.'

