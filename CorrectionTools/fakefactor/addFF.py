import ROOT
from ROOT import TChain, TFile, TH1F, TCanvas
import numpy as np
from array import array
import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from plotting.utils import getJSON
from xsections import xsection
from argparse import ArgumentParser
parser = ArgumentParser()

parser.add_argument('-c', '--channel', dest='channel', type=str, default='mutau', action='store',)
parser.add_argument('-y', '--year',    dest='year', type=str, default='2018', action='store')
parser.add_argument('-u', '--UL',      dest='ULtag', action='store_const', const="UL",default="")
args = parser.parse_args()

year = args.year
channel = args.channel
ULtag = args.ULtag
if ULtag=="UL":
    JSON_path = '/work/pbaertsc/bbh/CMSSW_10_2_16_NanoSkim/src/NanoAODv2_UL2018/json/'
else:
    JSON_path = '/work/pbaertsc/bbh/CMSSW_10_2_16_NanoSkim/src/NanoAODv7_2018/json/'

samples = {
     'UL2018':{
    'data_obs': 'SingleMuon_Run2018ABCD',
    'WJets': 'WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8',
    'DYJets':'DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8',
    'DY1Jets':'DY1JetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8',
    'DY2Jets':'DY2JetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8',
    'DY3Jets':'DY3JetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8',
    'DY4Jets':'DY4JetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8',
    'TTTo2L2Nu':'TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8',
    'TTToHadronic':'TTToHadronic_TuneCP5_13TeV-powheg-pythia8',
    'TTToSemiLeptonic':'TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8',
    'ST_t_channel_antitop': 'ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8',
    'ST_t_channel_top': 'ST_t-channel_top_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8',
    'bbH': 'BBHToTauTau',
    'ggbbH': 'gghplusbb',
    'ggbbH_ext': 'gghplusbb_ext',    
    },
    '2018':{
    'data_obs': 'SingleMuon_Run2018ABCD',
    'WJets': 'WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8',
    'DYJets':'DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8',
    'DY1Jets':'DY1JetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8',
    'DY2Jets':'DY2JetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8',
    'DY3Jets':'DY3JetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8',
    'DY4Jets':'DY4JetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8',
    'TTTo2L2Nu':'TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8',
    'TTToHadronic':'TTToHadronic_TuneCP5_13TeV-powheg-pythia8',
    'TTToHadronic_ext':'TTToHadronic_TuneCP5_13TeV-powheg-pythia8_ext2',
    'TTToSemiLeptonic':'TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8',
    'ST_s_channel_antitop': 'ST_s-channel_antitop_leptonDecays_13TeV-PSweights_powheg-pythia',
    'ST_s_channel_top': 'ST_s-channel_top_leptonDecays_13TeV-PSweights_powheg-pythia',
    'ST_t_channel_antitop': 'ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8',
    'ST_t_channel_top': 'ST_t-channel_top_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8',
    'ST_tW_antitop': 'ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8',
    'ST_tW_top': 'ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8',
    'WWTo2L2Nu': 'WWTo2L2Nu_NNPDF31_TuneCP5_13TeV-powheg-pythia8',
    'WWTo4Q': 'WWTo4Q_NNPDF31_TuneCP5_13TeV-powheg-pythia8',
    'WWToLNuQQ': 'WWToLNuQQ_NNPDF31_TuneCP5_13TeV-powheg-pythia8',
    'WZTo1L1Nu2Q': 'WZTo1L1Nu2Q_13TeV_amcatnloFXFX_madspin_pythia8',
    'WZTo1L3Nu': 'WZTo1L3Nu_13TeV_amcatnloFXFX_madspin_pythia8',
    'WZTo2L2Q': 'WZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8',
    'WZTo3LNu': 'WZTo3LNu_TuneCP5_13TeV-amcatnloFXFX-pythia8',
    'WZTo3LNu_ext': 'WZTo3LNu_TuneCP5_13TeV-amcatnloFXFX-pythia8_ext1',
    'ZZTo2L2Q': 'ZZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8',
    'ZZTo2Q2Nu': 'ZZTo2Q2Nu_TuneCP5_13TeV_amcatnloFXFX_madspin_pythia8',
    'ZZTo4L': 'ZZTo4L_TuneCP5_13TeV-amcatnloFXFX-pythia8',
    'bbH' : 'SUSYGluGluToBBHToTauTau_M-125_TuneCP5_13TeV-amcatnlo-pythia8',
    'jjH' : 'SUSYGluGluToJJHToTauTau_M-125_TuneCP5_13TeV-amcatnlo-pythia8',
    'ggH' : 'GluGluHToTauTau_M125_13TeV_powheg_pythia8',
    'ggF' : 'GGFHToTauTau_M125_13TeV_powheg_pythia8',
    'ttH' : 'ttHToTauTau_M125_TuneCP5_13TeV-powheg-pythia8',
    'ggbbH': 'gghplusbb',}
}

filedir = "../samples_%s%s"%(ULtag,year)
if ULtag=="UL":
    signal_samples = ['bbH','ggbbH','ggbbH_ext']
    bkg_samples = ['WJets','DYJets','DY1Jets','DY2Jets','DY3Jets','DY4Jets','TTTo2L2Nu','TTToHadronic','TTToSemiLeptonic','ST_t_channel_antitop','ST_t_channel_top']
    mc_samples = ['bbH','ggbbH','ggbbH_ext','WJets','DYJets','DY1Jets','DY2Jets','DY3Jets','DY4Jets','TTTo2L2Nu','TTToHadronic','TTToSemiLeptonic','ST_t_channel_antitop','ST_t_channel_top']
else:
    signal_samples = ["bbH",'ggbbH']
    bkg_samples = ['WJets','DYJets','DY1Jets','DY2Jets','DY3Jets','DY4Jets','TTTo2L2Nu','TTToHadronic','TTToHadronic_ext','TTToSemiLeptonic','ST_s_channel_antitop','ST_s_channel_top','ST_t_channel_antitop','ST_t_channel_top','ST_tW_antitop','ST_tW_top','WWTo2L2Nu','WWTo4Q','WWToLNuQQ','WZTo1L1Nu2Q','WZTo1L3Nu','WZTo2L2Q','WZTo3LNu','WZTo3LNu_ext','ZZTo2L2Q','ZZTo2Q2Nu','ZZTo4L','ttH','ggF','jjH']
    mc_samples = ['bbH','ggbbH','jjH', 'ggF','WJets','DYJets','DY1Jets','DY2Jets','DY3Jets','DY4Jets','TTTo2L2Nu','TTToHadronic','TTToHadronic_ext','TTToSemiLeptonic','ST_s_channel_antitop','ST_s_channel_top','ST_t_channel_antitop','ST_t_channel_top','ST_tW_antitop','ST_tW_top','WWTo2L2Nu','WWTo4Q','WWToLNuQQ','WZTo1L1Nu2Q','WZTo1L3Nu','WZTo2L2Q','WZTo3LNu','WZTo3LNu_ext','ZZTo2L2Q','ZZTo2Q2Nu','ZZTo4L','ttH']




if channel=="mutau":
    selection = 'isHtoMuTau && Mu1_charge*Tau1_charge==-1 && dimuon_veto==0 && electron_veto==0 && Tau1_genmatch!=6 && transverse_mass_mumet<60 && nBjets_m>=1'
    selection_ar = 'isHtoMuTauAR && dimuon_veto==0 && electron_veto==0 && Mu1_charge*Tau1_charge==-1 && Tau1_genmatch!=6 && transverse_mass_mumet<60 && nBjets_m>=1'
    
for sample_shortname in mc_samples:
    eventWeightLumi = array('f', [1.0])# global event weight with lumi
    fakefactor = array('f', [1.0])
    sample = samples["%s%s"%(ULtag,year)][sample_shortname]
    infile = TFile(filedir+"/"+sample+".root")
    intree = infile.Get("tree")
    outfile = TFile("%s_fakefactor.root"%sample,"RECREATE")
    xsec = xsection[samples['%s%s'%(ULtag,year)]['%s'%sample_shortname]]['xsec']
    if ULtag=="" and sample_shortname in ['DY2Jets','TTTo2L2Nu','TTToSemiLeptonic','ttH']:  #do not use JSON because event based splitting
        nevents =  xsection[samples['%s%s'%(ULtag,year)][sample_shortname]]['sumw']
    else:
        nevents = getJSON(JSON_path,samples['%s%s'%(ULtag,year)][sample_shortname],year,ULtag)
    scale_weight=(59508.332160 * xsec / nevents)
    ar_tree=intree.CopyTree(selection_ar)
    infile.Close()
    eventWeightLumiBranch = ar_tree.Branch('eventWeightLumi', eventWeightLumi, 'eventWeightLumi/F')
    
    for event in range(0,skimmed_tree.GetEntries()):
        skimmed_tree.GetEntry(event)
        eventWeightLumi[0] = skimmed_tree.EventWeight * scale_weight
        eventWeightLumiBranch.Fill()
    outfile.Write()
    outfile.Close()

