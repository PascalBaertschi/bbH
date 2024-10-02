import ROOT
from analysis import *
from argparse import ArgumentParser
import json
import utils
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..')) #to get file in parent directory
from xsections import xsection
from samplenames import getsamples

# import CombineHarvester.CombineTools.plotting as plot

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.TH1.AddDirectory(False)

parser = ArgumentParser()
parser.add_argument('-y', '--year',    dest='year', type=str, default='2018', action='store')
parser.add_argument('-c', '--channel', dest='channel', type=str, default='mutau', action='store',)
parser.add_argument('-b', '--BDT', default=False,action='store_true')
parser.add_argument('-n', '--NN', default=False,action='store_true')
parser.add_argument('-d', '--DR', default=False,action='store_true')
parser.add_argument('-u', '--UL',      dest='ULtag', action='store_const', const="UL",default="UL")
parser.add_argument('-p', '--preVFP',  dest='preVFP', action='store_const', const="_preVFP",default="")
parser.add_argument('-t', '--comb',  dest='UL2016comb', action='store_true',default=False)
parser.add_argument('-s', '--sysvar', dest='sysvar', type=str, default='', action='store')
args = parser.parse_args()

year = args.year
channel = args.channel
sysvar = args.sysvar
ULtag = args.ULtag
plotDR = args.DR
preVFP = args.preVFP
isBDT = args.BDT
isNN = args.NN
UL2016comb = args.UL2016comb

if UL2016comb:
    preVFP="_comb"

#LUMI        = 137190.
if year=='2018':
    LUMI = 59740
elif year=='2017':
    LUMI = 41530
elif year=='2016':
    if preVFP=="_preVFP":
        LUMI = 19500
    else:
        LUMI = 16800

if sysvar!="":
    sysvar="_"+sysvar

if isBDT:
    if isNN:
        samplesdir = '/pnfs/psi.ch/cms/trivcat/store/user/pbaertsc/bbh/samples_%s%s%s%s_NNBDT/%s/'%(ULtag,year,preVFP,sysvar,channel)
    else:
        samplesdir = '/pnfs/psi.ch/cms/trivcat/store/user/pbaertsc/bbh/samples_%s%s%s%s_BDT/%s/'%(ULtag,year,preVFP,sysvar,channel)  
else:
    #samplesdir = '../samples_%s%s%s/'%(ULtag,year,preVFP)
    samplesdir = '/pnfs/psi.ch/cms/trivcat/store/user/pbaertsc/bbh/samples_%s%s%s%s/'%(ULtag,year,preVFP,sysvar)

hists = Node()

if channel=="mutau":
    selection = 'isHtoMuTau && Mu1_charge*Tau1_charge==-1 && dimuon_veto==0 && electron_veto==0 && Tau1_genmatch!=6 && nBjets_m>=1 && transverse_mass_lepmet<60'# && EventNumber%10>=4
    selection_ar = 'isHtoMuTauAR && dimuon_veto==0 && electron_veto==0 && Mu1_charge*Tau1_charge==-1 && Tau1_genmatch!=6 && nBjets_m>=1 && transverse_mass_lepmet<60'# && EventNumber%10>=4
    #selection = 'isHtoMuTau && Mu1_charge*Tau1_charge==-1 && dimuon_veto==0 && electron_veto==0 && Tau1_genmatch!=6 && nBjets_m>=1 && transverse_mass_lepmet<60 && (dijet_mass < 70. || dijet_mass > 100.)'
    #selection_ar = 'isHtoMuTauAR && dimuon_veto==0 && electron_veto==0 && Mu1_charge*Tau1_charge==-1 && Tau1_genmatch!=6 && nBjets_m>=1 && transverse_mass_lepmet<60 && (dijet_mass < 70. || dijet_mass > 100.)'
    #selection = 'isHtoMuTau && Mu1_charge*Tau1_charge==1 && dimuon_veto==0 && electron_veto==0 && transverse_mass_lepmet < 60 && nBjets_m>0' #QCD DR
    #selection_ar = 'isHtoMuTauAR && dimuon_veto==0 && electron_veto==0 && Mu1_charge*Tau1_charge==1 && transverse_mass_lepmet < 60 && nBjets_m>0' #QCD DR AR
    
    #selection = 'isHtoMuTau && Mu1_charge*Tau1_charge==-1 && dimuon_veto==0 && electron_veto==0 && nBjets_m>=1 && EventNumber%10>=4'
    #selection = 'isHtoMuTau && Mu1_charge*Tau1_charge==-1 && dimuon_veto==0 && electron_veto==0 && Tau1_genmatch!=6 && transverse_mass_lepmet > 70 && transverse_mass_lepmet < 90 && nBjets_m>=1 && EventNumber%10>=4 && Tau1_pt > 70 && Tau1_pt < 80 && (Tau1_decaymode==0||Tau1_decaymode==1)'
    #selection = 'isHtoMuTau && dimuon_veto==0 && electron_veto==0 && Mu1_charge*Tau1_charge==-1 && transverse_mass_lepmet > 70 && transverse_mass_lepmet < 90 && nBjets_m>0 && Tau1_genmatch!=6'
    #selection_ar = 'isHtoMuTauAR && dimuon_veto==0 && electron_veto==0 && Mu1_charge*Tau1_charge==-1 && Tau1_genmatch!=6 && transverse_mass_lepmet > 70 && transverse_mass_lepmet < 90 && nBjets_m>=1 && EventNumber%10>=4'
    #selection_ss = 'isHtoMuTau && Mu1_charge*Tau1_charge==1 && dimuon_veto==0 && electron_veto==0 && transverse_mass_lepmet<60 && nBjets_m>=1 && EventNumber%10>=4'
    selections_DR = [
        {'name':'DR_QCD',
         'selection':'isHtoMuTau && Mu1_charge*Tau1_charge==1 && dimuon_veto==0 && electron_veto==0 && transverse_mass_lepmet < 60 && nBjets_m>0 && Tau1_genmatch!=6',
         'selection_ar':'isHtoMuTauAR && dimuon_veto==0 && electron_veto==0 && Mu1_charge*Tau1_charge==1 && transverse_mass_lepmet < 60 && nBjets_m>0 && Tau1_genmatch!=6'},
        {'name':'DR_W',
         'selection':'isHtoMuTau && dimuon_veto==0 && electron_veto==0 && Mu1_charge*Tau1_charge==-1 && transverse_mass_lepmet > 80 && nBjets_m==0 && Tau1_genmatch!=6',
         'selection_ar':'isHtoMuTauAR && dimuon_veto==0 && electron_veto==0 && Mu1_charge*Tau1_charge==-1 && transverse_mass_lepmet > 80 && nBjets_m==0 && Tau1_genmatch!=6'},
        {'name' : 'DR_TT',
         'selection':'isHtoMuTau && dimuon_veto==0 && electron_veto==0 && Mu1_charge*Tau1_charge==-1 && transverse_mass_lepmet > 70 && transverse_mass_lepmet < 90 && nBjets_m>0 && Tau1_genmatch!=6',
         'selection_ar':'isHtoMuTauAR && dimuon_veto==0 && electron_veto==0 && Mu1_charge*Tau1_charge==-1 && transverse_mass_lepmet > 70 && transverse_mass_lepmet < 90 && nBjets_m>0 && Tau1_genmatch!=6'},
        {'name':'CR_QCD',
         'selection':'isHtolooseMuTau && Mu1_charge*Tau1_charge==1 && Mu1_iso>0.15 && dimuon_veto==0 && electron_veto==0 && transverse_mass_lepmet < 60 && nBjets_m>0 && Tau1_genmatch!=6',
         'selection_ar':'isHtolooseMuTauAR && dimuon_veto==0 && Mu1_iso>0.15 && electron_veto==0 && Mu1_charge*Tau1_charge==1 && transverse_mass_lepmet < 60 && nBjets_m>0 && Tau1_genmatch!=6'},
        {'name':'CR_W',
         'selection':'isHtoMuTau && dimuon_veto==0 && electron_veto==0 && Mu1_charge*Tau1_charge==-1 && transverse_mass_lepmet > 60 && transverse_mass_lepmet < 80 && nBjets_m==0 && Tau1_genmatch!=6',
         'selection_ar':'isHtoMuTauAR && dimuon_veto==0 && electron_veto==0 && Mu1_charge*Tau1_charge==-1 && transverse_mass_lepmet > 60 && transverse_mass_lepmet < 80 && nBjets_m==0 && Tau1_genmatch!=6'},
        {'name':'CR_TT',
         'selection':'isHtoMuTau && dimuon_veto==0 && electron_veto==0 && Mu1_charge*Tau1_charge==-1 && transverse_mass_lepmet > 60 && transverse_mass_lepmet < 70 && nBjets_m>0 && Tau1_genmatch!=6',
         'selection_ar':'isHtoMuTauAR && dimuon_veto==0 && electron_veto==0 && Mu1_charge*Tau1_charge==-1 && transverse_mass_lepmet > 60 && transverse_mass_lepmet < 70 && nBjets_m>0 && Tau1_genmatch!=6'},
    ]

elif channel=="etau":
    #selection = 'isHtoETau && Ele1_charge*Tau1_charge==-1 && dielectron_veto==0 && muon_veto==0 && Tau1_genmatch!=6 && nBjets_m>=1 && transverse_mass_lepmet<60 && EventNumber%10>=4'
    selection = 'isHtoETau && Ele1_charge*Tau1_charge==-1 && dielectron_veto==0 && muon_veto==0 && Tau1_genmatch!=6 && nBjets_m>=1 && transverse_mass_lepmet<60'# && EventNumber%10>=4
    selection_ar = 'isHtoETauAR && dielectron_veto==0 && muon_veto==0 && Ele1_charge*Tau1_charge==-1 && Tau1_genmatch!=6 && nBjets_m>=1 && transverse_mass_lepmet<60'# && EventNumber%10>=4
    #selection = 'isHtoETau && Ele1_charge*Tau1_charge==1 && dielectron_veto==0 && muon_veto==0 && transverse_mass_lepmet < 60 && nBjets_m>0' #QCD DR
    #selection_ar = 'isHtoETauAR && dielectron_veto==0 && muon_veto==0 && Ele1_charge*Tau1_charge==1 && transverse_mass_lepmet < 60 && nBjets_m>0' #QCD DR AR
    #selection_ar = 'isHtoETauAR && Ele1_charge*Tau1_charge==-1 && H_pt > 40 && H_pt < 120 && dielectron_veto==0 && muon_veto==0 && Tau1_genmatch!=6  && nBjets_m>=1  && EventNumber%10>=4 && transverse_mass_lepmet < 60'
    #selection = 'isHtoETau && Ele1_charge*Tau1_charge==-1 && dielectron_veto==0 && muon_veto==0 && nBjets_m>=1 && EventNumber%10>=4'
    #selection = 'isHtoETau && Ele1_charge*Tau1_charge==-1 && dielectron_veto==0 && muon_veto==0 && Tau1_genmatch!=6 && transverse_mass_lepmet > 70 && transverse_mass_lepmet < 90 && nBjets_m>=1 && EventNumber%10>=4 && Tau1_pt > 70 && Tau1_pt < 80 && (Tau1_decaymode==0||Tau1_decaymode==1)'
    #selection = 'isHtoETau && dielectron_veto==0 && muon_veto==0 && Ele1_charge*Tau1_charge==-1 && transverse_mass_lepmet > 70 && transverse_mass_lepmet < 90 && nBjets_m>0 && Tau1_genmatch!=6'
    #selection_ar = 'isHtoETauAR && dielectron_veto==0 && muon_veto==0 && Ele1_charge*Tau1_charge==-1 && Tau1_genmatch!=6 && transverse_mass_lepmet > 70 && transverse_mass_lepmet < 90 && nBjets_m>=1 && EventNumber%10>=4'
    #selection_ss = 'isHtoETau && Ele1_charge*Tau1_charge==1 && dielectron_veto==0 && muon_veto==0 && transverse_mass_lepmet<60 && nBjets_m>=1 && EventNumber%10>=4'
    selections_DR = [
        {'name':'DR_QCD',
         'selection':'isHtoETau && Ele1_charge*Tau1_charge==1 && dielectron_veto==0 && muon_veto==0 && transverse_mass_lepmet < 60 && nBjets_m>0 && Tau1_genmatch!=6',
         'selection_ar':'isHtoETauAR && dielectron_veto==0 && muon_veto==0 && Ele1_charge*Tau1_charge==1 && transverse_mass_lepmet < 60 && nBjets_m>0 && Tau1_genmatch!=6'},
        {'name':'DR_W',
         'selection':'isHtoETau && dielectron_veto==0 && muon_veto==0 && Ele1_charge*Tau1_charge==-1 && transverse_mass_lepmet > 80 && nBjets_m==0 && Tau1_genmatch!=6',
         'selection_ar':'isHtoETauAR && dielectron_veto==0 && muon_veto==0 && Ele1_charge*Tau1_charge==-1 && transverse_mass_lepmet > 80 && nBjets_m==0 && Tau1_genmatch!=6'},
        {'name' : 'DR_TT',
         'selection':'isHtoETau && dielectron_veto==0 && muon_veto==0 && Ele1_charge*Tau1_charge==-1 && transverse_mass_lepmet > 70 && transverse_mass_lepmet < 90 && nBjets_m>0 && Tau1_genmatch!=6',
         'selection_ar':'isHtoETauAR && dielectron_veto==0 && muon_veto==0 && Ele1_charge*Tau1_charge==-1 && transverse_mass_lepmet > 70 && transverse_mass_lepmet < 90 && nBjets_m>0 && Tau1_genmatch!=6'},
        {'name':'CR_QCD',
         'selection':'isHtolooseETau && Ele1_charge*Tau1_charge==1 && Ele1_iso>0.1 && dielectron_veto==0 && muon_veto==0 && transverse_mass_lepmet < 60 && nBjets_m>0 && Tau1_genmatch!=6',
         'selection_ar':'isHtolooseETauAR && dielectron_veto==0 && Ele1_iso>0.1 && muon_veto==0 && Ele1_charge*Tau1_charge==1 && transverse_mass_lepmet < 60 && nBjets_m>0 && Tau1_genmatch!=6'},
        {'name':'CR_W',
         'selection':'isHtoETau && dielectron_veto==0 && muon_veto==0 && Ele1_charge*Tau1_charge==-1 && transverse_mass_lepmet > 60 && transverse_mass_lepmet < 80 && nBjets_m==0 && Tau1_genmatch!=6',
         'selection_ar':'isHtoETauAR && dielectron_veto==0 && muon_veto==0 && Ele1_charge*Tau1_charge==-1 && transverse_mass_lepmet > 60 && transverse_mass_lepmet < 80 && nBjets_m==0 && Tau1_genmatch!=6'},
        {'name':'CR_TT',
         'selection':'isHtoETau && dielectron_veto==0 && muon_veto==0 && Ele1_charge*Tau1_charge==-1 && transverse_mass_lepmet > 60 && transverse_mass_lepmet < 70 && nBjets_m>0 && Tau1_genmatch!=6',
         'selection_ar':'isHtoETauAR && dielectron_veto==0 && muon_veto==0 && Ele1_charge*Tau1_charge==-1 && transverse_mass_lepmet > 60 && transverse_mass_lepmet < 70 && nBjets_m>0 && Tau1_genmatch!=6'},
    ]
elif channel=="mumu":
    selection = 'isMuMu && nBjets_m>0'
elif channel=="tt":
    selection = 'isTTCR && nBjets_m>0'


selections_prong = [
    {'name':'1prong',
     'selection':'&& (Tau1_decaymode==0 || Tau1_decaymode==1 || Tau1_decaymode==2)'},
    {'name':'3prong',
     'selection':'&& (Tau1_decaymode==10 || Tau1_decaymode==11)'}]


drawvars = [
    ('Mu1_pt',      'Mu1_pt',       (20, 0, 130)),
    ('Mu1_eta',     'Mu1_eta',      (20, -2.5, 2.5)),
    ('Mu1_phi',     'Mu1_phi',      (20, -3.2, 3.2)),
    ('Mu1_mass',    'Mu1_mass',     (20, 0., 0.2)),
    ('Ele1_pt',     'Ele1_pt',       (20, 0, 130)),
    ('Ele1_eta',    'Ele1_eta',      (20, -2.5, 2.5)),
    ('Ele1_phi',    'Ele1_phi',      (20, -3.2, 3.2)),
    ('Ele1_mass',   'Ele1_mass',     (20, 0., 0.2)),
    ('Tau1_pt',     'Tau1_pt',      (20, 0, 130)),
    ('Tau1_eta',    'Tau1_eta',     (20, -2.5, 2.5)),
    ('Tau1_phi',    'Tau1_phi',     (20, -3.2, 3.2)),
    ('Tau1_mass',   'Tau1_mass',    (20, 0., 2.)),
    ('Tau1_decaymode', 'Tau1_decaymode', (11,0,11)),
    ('Tau1_Idvsjet','Tau1_Idvsjet',(20,0.,300.)),
    ('Tau1_Idvsmu', 'Tau1_Idvsmu',  (20,0.,300.)),
    ('Tau1_Idvse', 'Tau1_Idvse',    (20,0.,300.)),
    ('vistau1_pt',  'vistau1_pt',   (20, 0, 130)),
    ('vistau1_eta', 'vistau1_eta',  (20, -2.5, 2.5)),
    ('vistau1_phi', 'vistau1_phi',  (20, -3.2, 3.2)),
    ('vistau1_mass','vistau1_mass', (20, 0., 0.2)),
    #('Jet1_pt',     'Jet1_pt',      (30, 0, 200)),
    ('Jet1_pt',     'Jet1_pt',      (20, 0, 200)),
    ('Jet1_eta',    'Jet1_eta',     (20, -2.5, 2.5)),
    ('Jet1_phi',    'Jet1_phi',     (20, -3.2, 3.2)),
    ('Jet1_mass',   'Jet1_mass',    (20, 0., 10.)),
    #('Jet1_btag',   'Jet1_btag',    (30, 0., 1.)),
    ('Jet1_btag',   'Jet1_btag',    (20, 0., 1.)),
    ('Jet2_pt',     'Jet2_pt',      (20, 0, 150)),
    ('Jet2_eta',    'Jet2_eta',     (20, -2.5, 2.5)),
    ('Jet2_phi',    'Jet2_phi',     (20, -3.2, 3.2)),
    ('Jet2_mass',   'Jet2_mass',    (20, 0., 10.)),
    ('Jet2_btag',   'Jet2_btag',    (20, 0., 1.)),
    ('Jet3_pt',     'Jet3_pt',      (20, 0, 150)),
    ('Jet3_eta',    'Jet3_eta',     (20, -2.5, 2.5)),
    ('Jet3_phi',    'Jet3_phi',     (20, -3.2, 3.2)),
    ('Jet3_mass',   'Jet3_mass',    (20, 0., 10.)),
    ('Jet3_btag',   'Jet3_btag',    (20, 0., 1.)),
    ('Bjet1_pt',    'Bjet1_pt',     (20, 0, 300)),
    ('Bjet1_eta',   'Bjet1_eta',    (20, -2.5, 2.5)),
    ('Bjet1_phi',   'Bjet1_phi',    (20, -3.2, 3.2)),
    ('Bjet1_mass',  'Bjet1_mass',   (20, 0., 10.)),
    ('Bjet2_pt',    'Bjet2_pt',     (20, 0, 300)),
    ('Bjet2_eta',   'Bjet2_eta',    (20, -2.5, 2.5)),
    ('Bjet2_phi',   'Bjet2_phi',    (20, -3.2, 3.2)),
    ('Bjet2_mass',  'Bjet2_mass',   (20, 0., 10.)),
    ('vis_pt',      'vis_pt',       (20, 0, 300)),
    ('vis_eta',     'vis_eta',      (20, -2.5, 2.5)),
    ('vis_phi',     'vis_phi',      (20, -3.2, 3.2)),
    ('vis_mass',    'vis_mass',     (20, 0., 250.)),
    #('collinear_mass', 'collinear_mass', (30, 0.,250.)),
    ('collinear_mass', 'collinear_mass', (20, 0.,250.)),
    ('transverse_mass_lepmet', 'transverse_mass_lepmet',     (20, 0., 200.)),
    ('H_pt',        'H_pt',         (20, 0, 300)),
    ('H_eta',       'H_eta',        (20, -2.5, 2.5)),
    ('H_phi',       'H_phi',        (20, -3.2, 3.2)),
    #('H_mass',      'H_mass',       (30, 0., 200.)),
    ('H_mass',      'H_mass',       (20, 0., 200.)),
    #('MET',         'MET',          (30, 0, 150)),
    ('MET',         'MET',          (20, 0, 150)),
    #('MET_phi',     'MET_phi',      (30, -3.2, 3.2)),
    ('MET_chs',     'MET_chs',      (20, 0, 200)),
    ('nMuons',      'nMuons',       (5, 0., 5.)),
    ('nElectrons',  'nElectrons',   (5, 0., 5.)),
    ('nTaus',       'nTaus',        (5, 0., 5.)),
    ('nJets',       'nJets',        (8, 0., 8.)),
    ('nBjets_l',    'nBjets_l',     (4, 0., 4.)),
    ('nBjets_m',    'nBjets_m',     (4, 0., 4.)),
    ('nBjets_t',    'nBjets_t',     (4, 0., 4.)),
    ('nJets_forward','nJets_forward',(4, 0., 4.)),
    ('nGenBjets',   'nGenBjets',    (4, 0., 4.)),
    ('LHE_Nb',      'LHE_Nb',       (4, 0., 4.)),
    ('LHE_NpNLO',   'LHE_NpNLO',    (4, 0., 4.)),
    ('DPhi',        'DPhi',         (20, -5., 5.)),
    ('DEta',        'DEta',         (20,0., 5.)),
    ('DPhiLepMET',  'DPhiLepMET',   (20, -5., 5.)),
    ('DRLepMET',    'DRLepMET',     (20, 0., 5.)),
    ('met_var_qcd', 'met_var_qcd',  (20, 0., 5.)),
    ('met_var_w',   'met_var_w',    (20, 0., 5.)),
    ('wpt',         'wpt',          (20, 0., 300.)),
    ('DRBjets',     'DRBjets',      (20, 0., 10.)),
    ('DEta_Bjets',  'DEta_Bjets',   (20, 0., 4.)),
    ('DPhi_Bjets',  'DPhi_Bjets',   (20, -4., 4.)),
    ('Bjets_pt', 'Bjets_pt',        (20, 0., 200.)),
    ('DRBjets_lm',  'DRBjets_lm',   (20, 0., 10.)),
    ('DRLepJ',      'DRLepJ',        (20, 0., 10.)),
    ('DEtaLepJ',    'DEtaLepJ',      (20, 0., 4.)),
    ('DPhiLepJ',    'DPhiLepJ',      (20, -4., 4.)),
    ('DRTauJ',      'DRTauJ',       (20, 0., 10.)),
    ('DEtaTauJ',    'DEtaTauJ',     (20, 0., 4.)),
    ('DEtaTauJ2',   'DEtaTauJ2',     (20, 0., 4.)),
    ('DPhiTauJ',    'DPhiTauJ',     (20, -4., 4.)),
    ('DRLepJ2',     'DRLepJ2',        (20, 0., 10.)),
    ('DEtaLepJ2',   'DEtaLepJ2',      (20, 0., 4.)),
    ('DPhiLepJ2',   'DPhiLepJ2',      (20, -4., 4.)),
    ('DRTauJ2',     'DRTauJ2',       (20, 0., 10.)),
    ('HJ_mass',     'HJ_mass',      (20, 0., 300.)),
    ('vistauJ_mass', 'vistauJ_mass',(20, 0., 300.)),
    ('vistauJMET_mass', 'vistauJMET_mass', (20, 0., 300.)),
    ('TauJMET_mass', 'TauJMET_mass',(20, 0., 300.)),
    ('TauJ_mass', 'TauJ_mass',      (20, 0., 300.)),
    ('METJ_mass', 'METJ_mass',      (20, 0., 300.)),
    ('Dzeta', 'Dzeta',              (20, -100.,100.)),
    ('mt2', 'mt2',                  (20, 0.,60.)),
    ('wt_ff', 'wt_ff',              (20, 0.,1.)),
    ('wt_ff_ttdr', 'wt_ff_ttdr',    (20, 0.,1.)),
    ('transverse_mass_taumet', 'transverse_mass_taumet', (20,0.,200.)),
    ('transverse_mass_leptau', 'transverse_mass_leptau', (20,0.,200.)),
    ('transverse_mass_total', 'transverse_mass_total', (20,0.,300.)),
    ('DRjets', 'DRjets', (20, 0., 10.)),
    ('DEta_jets', 'DEta_jets', (20, 0., 4.)),
    ('DPhi_jets', 'DPhi_jets', (20, -4., 4.)),
    ('DEta_jets_forward', 'DEta_jets_forward', (20, 0., 10.)),
    ('dijet_pt', 'dijet_pt', (20, 0., 200.)),
    ('dijet_eta', 'dijet_eta', (20, -4.,4.)),
    ('dijet_phi', 'dijet_phi', (20, -4.,4.)),
    ('dijet_mass', 'dijet_mass', (20, 0.,200.)),
    ('LepJ_pt', 'LepJ_pt', (20, 0., 200.)),
    ('TauJ_pt', 'TauJ_pt', (20, 0.,200.)),
    ('vistauJ_pt', 'vistauJ_pt', (20,0.,200.)),
    ('vistauJMET_pt', 'vistauJMET_pt', (20,0.,200.)),
    ('TauJMET_pt', 'TauJMET_pt', (20,0.,200.)),
    ('LepJMET_pt', 'LepJMET_pt', (20,0.,200.)),
    ('METJ_pt', 'METJ_pt', (20,0.,200.)),
    ('vistauMET_pt', 'vistauMET_pt', (20,0.,200.)),
    ('HJ_pt', 'HJ_pt', (20,0.,200.)),
    ('DRHJ', 'DRHJ', (20,0,5.)),
    ('DRHJ2', 'DRHJ2', (20,0,5.)),
]

if isBDT:
    drawvars.append(('BDTisSignal', 'BDTisSignal',  (40, 0., 1.)))
    #drawvars.append(('BDTisbbH', 'BDTisbbH',  (30, 0., 1.)))
    #drawvars.append(('BDTisggH', 'BDTisggH',  (30, 0., 1.)))
    #drawvars.append(('BDTisjjH','BDTisjjH', (40, 0., 1.)))
    drawvars.append(('BDTisTT', 'BDTisTT',          (40, 0., 1.)))
    drawvars.append(('BDTisDY', 'BDTisDY',  (40, 0., 1.)))
    drawvars.append(('BDToutput', 'BDToutput',      (40,0.,1.)))
    drawvars.append(('BDToutSig', 'BDToutSig',      (40,0.,1.)))
    drawvars.append(('BDToutTT', 'BDToutTT',      (40,0.,1.)))
    drawvars.append(('BDToutDY', 'BDToutDY',      (40,0.,1.)))
if isNN:
    drawvars.append(('NNoutput',      'NNoutput',       (40, 0., 200.))),


for dirname, var, binning in drawvars:
    for sample in getsamples(channel,ULtag,year,preVFP):
        #if (isBDT or isNN) and sample in ["DYJets_incl","DYJets_0J","DYJets_1J","DYJets_2J","WJets_0J","WJets_1J","WJets_2J"]: continue 
        if "bbH_M" in sample: continue 
        if sample=='data_obs':
            weight = '1.'
            weight_btag_up = '1.'
            weight_btag_down = '1.'
            weight_ar = 'wt_ff'
            weight_ar_btag_up = 'wt_ff'
            weight_ar_btag_down = 'wt_ff'
            weight_ar_norm = 'wt_ff_norm'
            weight_ar_up = 'wt_ff_up'
            weight_ar_down = 'wt_ff_down'
            #weight_ar = '0.15'
        else:
            if channel=="mutau":
                weight = 'EventWeight * LumiWeight * BTagWeight * MuWeight * MuTriggerWeight * TauWeight * TauTriggerWeight * wt_tt * wt_dy * wt_w * wt_dy_nlo * wt_w_nlo'
                weight_btag_up = 'EventWeight * LumiWeight * BTagWeight_up * MuWeight * MuTriggerWeight * TauWeight * TauTriggerWeight * wt_tt * wt_dy * wt_w * wt_dy_nlo * wt_w_nlo'
                weight_btag_down = 'EventWeight * LumiWeight * BTagWeight_down * MuWeight * MuTriggerWeight * TauWeight * TauTriggerWeight * wt_tt * wt_dy * wt_w * wt_dy_nlo * wt_w_nlo'
                weight_shape = 'EventWeight * LumiWeight * BTagWeight_shape * MuWeight * MuTriggerWeight * TauWeight * TauTriggerWeight * wt_tt * wt_dy * wt_w * wt_dy_nlo * wt_w_nlo'
                weight_jes_up = 'EventWeight * LumiWeight * BTagWeight_jes_up * MuWeight * MuTriggerWeight * TauWeight * TauTriggerWeight * wt_tt * wt_dy * wt_w * wt_dy_nlo * wt_w_nlo'
                weight_jes_down = 'EventWeight * LumiWeight * BTagWeight_jes_down * MuWeight * MuTriggerWeight * TauWeight * TauTriggerWeight * wt_tt * wt_dy * wt_w * wt_dy_nlo * wt_w_nlo'
                weight_lf_up = 'EventWeight * LumiWeight * BTagWeight_lf_up * MuWeight * MuTriggerWeight * TauWeight * TauTriggerWeight * wt_tt * wt_dy * wt_w * wt_dy_nlo * wt_w_nlo'
                weight_lf_down = 'EventWeight * LumiWeight * BTagWeight_lf_down * MuWeight * MuTriggerWeight * TauWeight * TauTriggerWeight * wt_tt * wt_dy * wt_w * wt_dy_nlo * wt_w_nlo'
                weight_hf_up = 'EventWeight * LumiWeight * BTagWeight_hf_up * MuWeight * MuTriggerWeight * TauWeight * TauTriggerWeight * wt_tt * wt_dy * wt_w * wt_dy_nlo * wt_w_nlo'
                weight_hf_down = 'EventWeight * LumiWeight * BTagWeight_hf_down * MuWeight * MuTriggerWeight * TauWeight * TauTriggerWeight * wt_tt * wt_dy * wt_w * wt_dy_nlo * wt_w_nlo'
                weight_hfstats1_up = 'EventWeight * LumiWeight * BTagWeight_hfstats1_up * MuWeight * MuTriggerWeight * TauWeight * TauTriggerWeight * wt_tt * wt_dy * wt_w * wt_dy_nlo * wt_w_nlo'
                weight_hfstats1_down = 'EventWeight * LumiWeight * BTagWeight_hfstats1_down * MuWeight * MuTriggerWeight * TauWeight * TauTriggerWeight * wt_tt * wt_dy * wt_w * wt_dy_nlo * wt_w_nlo'
                weight_hfstats2_up = 'EventWeight * LumiWeight * BTagWeight_hfstats2_up * MuWeight * MuTriggerWeight * TauWeight * TauTriggerWeight * wt_tt * wt_dy * wt_w * wt_dy_nlo * wt_w_nlo'
                weight_hfstats2_down = 'EventWeight * LumiWeight * BTagWeight_hfstats2_down * MuWeight * MuTriggerWeight * TauWeight * TauTriggerWeight * wt_tt * wt_dy * wt_w * wt_dy_nlo * wt_w_nlo'
                weight_lfstats1_up = 'EventWeight * LumiWeight * BTagWeight_lfstats1_up * MuWeight * MuTriggerWeight * TauWeight * TauTriggerWeight * wt_tt * wt_dy * wt_w * wt_dy_nlo * wt_w_nlo'
                weight_lfstats1_down = 'EventWeight * LumiWeight * BTagWeight_lfstats1_down * MuWeight * MuTriggerWeight * TauWeight * TauTriggerWeight * wt_tt * wt_dy * wt_w * wt_dy_nlo * wt_w_nlo'
                weight_lfstats2_up = 'EventWeight * LumiWeight * BTagWeight_lfstats2_up * MuWeight * MuTriggerWeight * TauWeight * TauTriggerWeight * wt_tt * wt_dy * wt_w * wt_dy_nlo * wt_w_nlo'
                weight_lfstats2_down = 'EventWeight * LumiWeight * BTagWeight_lfstats2_down * MuWeight * MuTriggerWeight * TauWeight * TauTriggerWeight * wt_tt * wt_dy * wt_w * wt_dy_nlo * wt_w_nlo'
                weight_cferr1_up = 'EventWeight * LumiWeight * BTagWeight_lfstats1_up * MuWeight * MuTriggerWeight * TauWeight * TauTriggerWeight * wt_tt * wt_dy * wt_w * wt_dy_nlo * wt_w_nlo'
                weight_cferr1_down = 'EventWeight * LumiWeight * BTagWeight_lfstats1_down * MuWeight * MuTriggerWeight * TauWeight * TauTriggerWeight * wt_tt * wt_dy * wt_w * wt_dy_nlo * wt_w_nlo'
                weight_cferr2_up = 'EventWeight * LumiWeight * BTagWeight_lfstats2_up * MuWeight * MuTriggerWeight * TauWeight * TauTriggerWeight * wt_tt * wt_dy * wt_w * wt_dy_nlo * wt_w_nlo'
                weight_cferr2_down = 'EventWeight * LumiWeight * BTagWeight_lfstats2_down * MuWeight * MuTriggerWeight * TauWeight * TauTriggerWeight * wt_tt * wt_dy * wt_w * wt_dy_nlo * wt_w_nlo'
                weight_ar = 'EventWeight * LumiWeight * BTagWeight * MuWeight * MuTriggerWeight * TauWeight * TauTriggerWeight * wt_tt * wt_dy * wt_w* wt_dy_nlo * wt_w_nlo * wt_ff'
                weight_ar_btag_up = 'EventWeight * LumiWeight * BTagWeight_up * MuWeight * MuTriggerWeight * TauWeight * TauTriggerWeight * wt_tt * wt_dy * wt_w* wt_dy_nlo * wt_w_nlo * wt_ff'
                weight_ar_btag_down = 'EventWeight * LumiWeight * BTagWeight_down * MuWeight * MuTriggerWeight * TauWeight * TauTriggerWeight * wt_tt * wt_dy * wt_w* wt_dy_nlo * wt_w_nlo * wt_ff'
                weight_ar_norm = 'EventWeight * LumiWeight * BTagWeight * MuWeight * MuTriggerWeight * TauWeight * TauTriggerWeight * wt_tt * wt_dy * wt_w* wt_dy_nlo * wt_w_nlo * wt_ff_norm'
                weight_ar_up = 'EventWeight * LumiWeight * BTagWeight * MuWeight * MuTriggerWeight * TauWeight * TauTriggerWeight * wt_tt * wt_dy * wt_w * wt_dy_nlo * wt_w_nlo * wt_ff_up'
                weight_ar_down = 'EventWeight * LumiWeight * BTagWeight * MuWeight * MuTriggerWeight * TauWeight * TauTriggerWeight * wt_tt * wt_dy * wt_w* wt_dy_nlo * wt_w_nlo * wt_ff_down'
            elif channel=="etau":
                weight = 'EventWeight * LumiWeight * BTagWeight * EWeight * ETriggerWeight * TauWeight * TauTriggerWeight * wt_tt * wt_dy * wt_w * wt_dy_nlo * wt_w_nlo'
                weight_btag_up = 'EventWeight * LumiWeight * BTagWeight_up * EWeight * ETriggerWeight * TauWeight * TauTriggerWeight * wt_tt * wt_dy * wt_w * wt_dy_nlo * wt_w_nlo'
                weight_btag_down = 'EventWeight * LumiWeight * BTagWeight_down * EWeight * ETriggerWeight * TauWeight * TauTriggerWeight * wt_tt * wt_dy * wt_w * wt_dy_nlo * wt_w_nlo'
                weight_ar = 'EventWeight * LumiWeight * BTagWeight * EWeight * ETriggerWeight * TauWeight * TauTriggerWeight * wt_tt * wt_dy * wt_w * wt_dy_nlo * wt_w_nlo * wt_ff'
                weight_ar_btag_up = 'EventWeight * LumiWeight * BTagWeight_up * EWeight * ETriggerWeight * TauWeight * TauTriggerWeight * wt_tt * wt_dy * wt_w * wt_dy_nlo * wt_w_nlo * wt_ff'
                weight_ar_btag_down = 'EventWeight * LumiWeight * BTagWeight_down * EWeight * ETriggerWeight * TauWeight * TauTriggerWeight * wt_tt * wt_dy * wt_w * wt_dy_nlo * wt_w_nlo * wt_ff'
                weight_ar_norm = 'EventWeight * LumiWeight * BTagWeight * EWeight * ETriggerWeight * TauWeight * TauTriggerWeight * wt_tt * wt_dy * wt_w * wt_dy_nlo * wt_w_nlo * wt_ff_norm'
                weight_ar_up = 'EventWeight * LumiWeight * BTagWeight * EWeight * ETriggerWeight * TauWeight * TauTriggerWeight * wt_tt * wt_dy * wt_w * wt_dy_nlo * wt_w_nlo * wt_ff_up'
                weight_ar_down = 'EventWeight * LumiWeight * BTagWeight * EWeight * ETriggerWeight * TauWeight * TauTriggerWeight * wt_tt * wt_dy * wt_w* wt_dy_nlo * wt_w_nlo * wt_ff_down'
            elif channel=="mumu":
                weight = 'EventWeight * LumiWeight * BTagWeight * MuWeight * MuTriggerWeight * wt_dy * wt_w * wt_dy_nlo * wt_w_nlo * wt_tt' #weights include both muons  
            elif channel=="tt":
                weight = 'EventWeight * LumiWeight * BTagWeight * MuWeight * MuTriggerWeight * EWeight * wt_dy * wt_w * wt_dy_nlo * wt_w_nlo * wt_tt' #MuTriggerWeight includes SingleElectron trigger
            #weight_ar = 'EventWeight * BTagWeight * MuWeight * MuTriggerWeight * TauWeight * TauTriggerWeight * 0.15'
            #weight = 'EventWeight'
            #weight_ar = 'EventWeight * wt_ff'

        if plotDR:
            for selection_DR in selections_DR:
                if "QCD" in selection_DR["name"]:
                    if sample=='data_obs':
                        weight = '1.'
                        weight_ar = 'wt_ff_qcd * wt_ffcorr_leppt_qcd * wt_ffcorr_hmass_qcd * wt_ffcorr_met_qcd'
                    else:
                        if channel=="mutau":
                            weight = 'EventWeight * LumiWeight * BTagWeight * MuWeight * MuTriggerWeight * TauWeight * TauTriggerWeight * wt_dy_nlo * wt_w_nlo * wt_dy * wt_tt * wt_w'
                            weight_ar = 'EventWeight * LumiWeight * BTagWeight * MuWeight * MuTriggerWeight * TauWeight * TauTriggerWeight * wt_dy_nlo * wt_w_nlo * wt_dy * wt_tt * wt_w * wt_ff_qcd * wt_ffcorr_leppt_qcd * wt_ffcorr_hmass_qcd * wt_ffcorr_met_qcd'
                        elif channel=="etau":
                            weight = 'EventWeight * LumiWeight * BTagWeight * EWeight * ETriggerWeight * TauWeight * TauTriggerWeight * wt_dy_nlo * wt_w_nlo * wt_dy * wt_tt * wt_w'
                            weight_ar = 'EventWeight * LumiWeight * BTagWeight * EWeight * ETriggerWeight * TauWeight * TauTriggerWeight * wt_dy_nlo * wt_w_nlo * wt_dy * wt_tt * wt_w * wt_ff_qcd * wt_ffcorr_leppt_qcd * wt_ffcorr_hmass_qcd * wt_ffcorr_met_qcd'
                elif "W" in selection_DR["name"]:
                    if sample=='data_obs':
                        weight = '1.'
                        weight_ar = 'wt_ff_w * wt_ffcorr_leppt_w * wt_ffcorr_hmass_w * wt_ffcorr_met_w'
                    else:
                        if channel=="mutau":
                            weight = 'EventWeight * LumiWeight * BTagWeight * MuWeight * MuTriggerWeight * TauWeight * TauTriggerWeight * wt_dy_nlo * wt_w_nlo * wt_dy * wt_tt * wt_w'
                            weight_ar = 'EventWeight * LumiWeight * BTagWeight * MuWeight * MuTriggerWeight * TauWeight * TauTriggerWeight * wt_dy_nlo * wt_w_nlo * wt_dy * wt_tt * wt_w * wt_ff_w * wt_ffcorr_leppt_w * wt_ffcorr_hmass_w * wt_ffcorr_met_w'
                        elif channel=="etau":
                            weight = 'EventWeight * LumiWeight * BTagWeight * EWeight * ETriggerWeight * TauWeight * TauTriggerWeight * wt_dy_nlo * wt_w_nlo * wt_dy * wt_tt * wt_w'
                            weight_ar = 'EventWeight * LumiWeight * BTagWeight * EWeight * ETriggerWeight * TauWeight * TauTriggerWeight * wt_dy_nlo * wt_w_nlo * wt_dy * wt_tt * wt_w * wt_ff_w * wt_ffcorr_leppt_w * wt_ffcorr_hmass_w * wt_ffcorr_met_w'
                elif "TT" in selection_DR["name"]:
                    if sample=='data_obs':
                        weight = '1.'
                        weight_ar = 'wt_ff_tt * wt_ffcorr_leppt_tt * wt_ffcorr_hmass_tt * wt_ffcorr_jetpt_tt * wt_ffcorr_jet2pt_tt * wt_ffcorr_met_tt'
                    else:
                        if channel=="mutau":
                            weight = 'EventWeight * LumiWeight * BTagWeight * MuWeight * MuTriggerWeight * TauWeight * TauTriggerWeight * wt_dy_nlo * wt_w_nlo * wt_dy * wt_tt * wt_w'
                            weight_ar = 'EventWeight * LumiWeight * BTagWeight * MuWeight * MuTriggerWeight * TauWeight * TauTriggerWeight * wt_dy_nlo * wt_w_nlo * wt_dy * wt_tt * wt_w * wt_ff_tt * wt_ffcorr_leppt_tt * wt_ffcorr_hmass_tt * wt_ffcorr_jetpt_tt * wt_ffcorr_jet2pt_tt * wt_ffcorr_met_tt'
                        elif channel=="etau":
                            weight = 'EventWeight * LumiWeight * BTagWeight * EWeight * ETriggerWeight * TauWeight * TauTriggerWeight * wt_dy_nlo * wt_w_nlo * wt_dy * wt_tt * wt_w'
                            weight_ar = 'EventWeight * LumiWeight * BTagWeight * EWeight * ETriggerWeight * TauWeight * TauTriggerWeight * wt_dy_nlo * wt_w_nlo * wt_dy * wt_tt * wt_w * wt_ff_tt * wt_ffcorr_leppt_tt * wt_ffcorr_hmass_tt * wt_ffcorr_jetpt_tt * wt_ffcorr_jet2pt_tt * wt_ffcorr_met_tt' 
                hists[selection_DR["name"]][dirname][sample] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection_DR["selection"], wt=weight)
                hists[selection_DR["name"]][dirname][sample + '_AR']= Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection_DR["selection_ar"], wt=weight_ar)
        else:
            #hists[dirname][sample] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight)
            if sysvar=="":
                hists[dirname][sample] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight)
                hists[dirname][sample + '_shape'] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight_shape)
                hists[dirname][sample + '_jes_up'] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight_jes_up)
                hists[dirname][sample + '_jes_down'] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight_jes_dwon)
                hists[dirname][sample + '_lf_up'] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight_lf_up)
                hists[dirname][sample + '_lf_down'] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight_lf_down)
                hists[dirname][sample + '_hf_up'] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight_hf_up)
                hists[dirname][sample + '_hf_down'] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight_hf_down)
                hists[dirname][sample + '_hfstats1_up'] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight_hfstats1_up)
                hists[dirname][sample + '_hfstats1_down'] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight_hfstats1_down)                                         
                hists[dirname][sample + '_hfstats2_up'] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight_hfstats2_up)
                hists[dirname][sample + '_hfstats2_down'] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight_hfstats2_down)                                         
                hists[dirname][sample + '_lfstats1_up'] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight_lfstats1_up)
                hists[dirname][sample + '_lfstats1_down'] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight_lfstats1_down)                                         
                hists[dirname][sample + '_lfstats2_up'] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight_lfstats2_up)
                hists[dirname][sample + '_lfstats2_down'] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight_lfstats2_down)
                hists[dirname][sample + '_cferr1_up'] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight_cferr1_up)
                hists[dirname][sample + '_cferr1_down'] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight_cferr1_down)                                         
                hists[dirname][sample + '_cferr2_up'] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight_cferr2_up)
                hists[dirname][sample + '_cferr2_down'] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight_cferr2_down)
                hists[dirname][sample + '_AR']= Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection_ar, wt=weight_ar)
                hists[dirname][sample + '_AR_btag_up']= Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection_ar, wt=weight_ar_btag_up)
                hists[dirname][sample + '_AR_btag_down']= Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection_ar, wt=weight_ar_btag_down)
                hists[dirname][sample + '_AR_norm']= Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection_ar, wt=weight_ar_norm)
                hists[dirname][sample + '_AR_up'] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection_ar, wt=weight_ar_up)
                hists[dirname][sample + '_AR_down']= Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection_ar, wt=weight_ar_down)
                #hists[dirname][sample + '_SS']= Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection_ss, wt=(weight+"*1.18"))
            else: #JEC variation not for application region
               if sample not in ["WZTo2L2Q","WZTo1L3Nu","ZZTo2L2Q","data_obs"]: #no UL samples -> no JEC variation
                   hists[dirname][sample+sysvar] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight)
        



"""
#########
for dirname, var, binning in drawvars:
    for sample in samples['%s%s%s'%(ULtag,year,preVFP)]:
        for selection_DR in selections_DR:
            for selection_prongjet in selections_prong:
                selection = selection_DR['selection']+selection_prongjet['selection']
                if sample=='data_obs':
                    weight = '1.'
                else:
                    if channel=="mutau":
                        weight = 'EventWeight * LumiWeight * BTagWeight * MuWeight * MuTriggerWeight * TauWeight * TauTriggerWeight * wt_dy * wt_tt'
                    elif channel=="etau":
                        weight = 'EventWeight * LumiWeight * BTagWeight * EWeight * ETriggerWeight * TauWeight * TauTriggerWeight * wt_dy * wt_tt'
                    
                hists[dirname][sample+'_%s_%s'%(selection_DR['name'],selection_prongjet['name'])] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight)
"""

MultiDraw(hists, samplesdir, getsamples(channel,ULtag,year,preVFP), 'tree', mt_cores=8)


# Loop through all nodes (just the ones containing TH1s)
if plotDR==False:
    for path, node in hists.ListNodes(withObjects=True):
        print('>> %s' % path)
        for variation in ["","btag_up","btag_down"]:
            if variation!="":
                variation = "_"+variation
            node['ggH%s%s'%(sysvar,variation)] = node['ggH_inc%s%s'%(sysvar,variation)] + node['ggbbH%s%s'%(sysvar,variation)] #+ node['ggbbH_ext%s'%sysvar]
            #node['bbH_ybybyt%s'%sysvar] = node['bbH%s'%sysvar] + node['bbH_ybyt%s'%sysvar]
            node['bbHtautau%s%s'%(sysvar,variation)] = node['bbH%s%s'%(sysvar,variation)] + node['ggH_inc%s%s'%(sysvar,variation)] + node['ggbbH%s%s'%(sysvar,variation)] #node['bbH_ybyt%s'%sysvar] + node['ggbbH_ext%s'%sysvar]
            node['jjHtautau%s%s'%(sysvar,variation)] = node['jjH%s%s'%(sysvar,variation)] + node['jjH_inc%s%s'%(sysvar,variation)]  + node['ggjjH%s%s'%(sysvar,variation)]
            node['ST%s%s'%(sysvar,variation)] = node['ST_t_channel_antitop%s%s'%(sysvar,variation)] + node['ST_t_channel_top%s%s'%(sysvar,variation)] + node['ST_s_channel%s%s'%(sysvar,variation)] + node['ST_tW_antitop%s%s'%(sysvar,variation)] + node['ST_tW_top%s%s'%(sysvar,variation)]
            node['TT%s%s'%(sysvar,variation)] = node['TTTo2L2Nu%s%s'%(sysvar,variation)] + node['TTToHadronic%s%s'%(sysvar,variation)] + node['TTToSemiLeptonic%s%s'%(sysvar,variation)]
            if sysvar=="": #WZTo2L2Q,WZTo1L3Nu,ZZTo2L2Q no UL samples -> no JEC variation
                node['VV%s%s'%(sysvar,variation)] = node['WWTo2L2Nu%s%s'%(sysvar,variation)] + node['WWTo1L1Nu2Q%s%s'%(sysvar,variation)] + node['WWTo4Q%s%s'%(sysvar,variation)] + node['WZTo3LNu%s%s'%(sysvar,variation)] + node['WZTo2L2Q%s%s'%(sysvar,variation)] + node['WZTo1L3Nu%s%s'%(sysvar,variation)] + node['WZTo1L1Nu2Q%s%s'%(sysvar,variation)] + node['ZZTo4L%s%s'%(sysvar,variation)] + node['ZZTo2L2Q%s%s'%(sysvar,variation)] + node['ZZTo2Q2Nu%s%s'%(sysvar,variation)]
            else:
                node['VV%s%s'%(sysvar,variation)] = node['WWTo2L2Nu%s%s'%(sysvar,variation)] + node['WWTo1L1Nu2Q%s%s'%(sysvar,variation)] + node['WWTo4Q%s%s'%(sysvar,variation)] + node['WZTo3LNu%s%s'%(sysvar,variation)] + node['WZTo1L1Nu2Q%s%s'%(sysvar,variation)] + node['ZZTo4L%s%s'%(sysvar,variation)] + node['ZZTo2Q2Nu%s%s'%(sysvar,variation)]
            #node['DYJets%s'%sysvar] = node['DYJets_LOincl%s'%sysvar] + node['DY1Jets%s'%sysvar] + node['DY2Jets%s'%sysvar] + node['DY3Jets%s'%sysvar] + node['DY4Jets%s'%sysvar] #LO
            #node['WJets%s'%sysvar] = node['WJets_LOincl%s'%sysvar] + node['W1Jets%s'%sysvar]+ node['W2Jets%s'%sysvar]+ node['W3Jets%s'%sysvar]+ node['W4Jets%s'%sysvar] #LO
            node['DYJets%s%s'%(sysvar,variation)] = node['DYJets_incl%s%s'%(sysvar,variation)] + node['DYJets_0J%s%s'%(sysvar,variation)] + node['DYJets_1J%s%s'%(sysvar,variation)] + node['DYJets_2J%s%s'%(sysvar,variation)] #NLO
            node['WJets%s%s'%(sysvar,variation)] = node['WJets_incl%s%s'%(sysvar,variation)] + node['WJets_0J%s%s'%(sysvar,variation)] + node['WJets_1J%s%s'%(sysvar,variation)] + node['WJets_2J%s%s'%(sysvar,variation)] #NLO
        if sysvar!="": continue #no AR for JEC variations
        ########### only for test ##########
        #node['ST_SS'] = node['ST_t_channel_antitop_SS'] + node['ST_t_channel_top_SS']
        #node['TT_SS'] = node['TTTo2L2Nu_SS'] + node['TTToHadronic_SS'] + node['TTToSemiLeptonic_SS']
        #node['MC_SS'] = node['DYJets_SS'] + node['DY1Jets_SS'] + node['DY2Jets_SS'] + node['DY3Jets_SS'] + node['DY4Jets_SS'] + node['WJets_SS']+ node['W1Jets_SS']+ node['W2Jets_SS']+ node['W3Jets_SS']+ node['W4Jets_SS']  + node['TT_SS'] + node['ST_SS']
        #node['QCD_SS'] = node['data_obs_SS']-node['MC_SS']
        ######### application region  ######
        for variation in ["","norm","up","down","btag_up","btag_down"]:
            if variation!="":
                variation = "_"+variation
            node['jjHtautau_AR%s'%variation] = node['jjH_AR%s'%variation] + node['jjH_inc_AR%s'%variation] + node['ggjjH_AR%s'%variation]
            node['ST_AR%s'%variation] = node['ST_t_channel_antitop_AR%s'%variation] + node['ST_t_channel_top_AR%s'%variation] + node['ST_s_channel_AR%s'%variation] + node['ST_tW_antitop_AR%s'%variation] + node['ST_tW_top_AR%s'%variation]
            node['TT_AR%s'%variation] = node['TTTo2L2Nu_AR%s'%variation] + node['TTToHadronic_AR%s'%variation] + node['TTToSemiLeptonic_AR%s'%variation]
            node['VV_AR%s'%variation] = node['WWTo2L2Nu_AR%s'%variation] + node['WWTo1L1Nu2Q_AR%s'%variation] + node['WWTo4Q_AR%s'%variation] + node['WZTo3LNu_AR%s'%variation] + node['WZTo2L2Q_AR%s'%variation] + node['WZTo1L3Nu_AR%s'%variation] + node['WZTo1L1Nu2Q_AR%s'%variation] + node['ZZTo4L_AR%s'%variation] + node['ZZTo2L2Q_AR%s'%variation] + node['ZZTo2Q2Nu_AR%s'%variation]
            #node['DYJets_AR%s'%variation] = node['DYJets_LOincl_AR%s'%variation] + node['DY1Jets_AR%s'%variation] + node['DY2Jets_AR%s'%variation] + node['DY3Jets_AR%s'%variation] + node['DY4Jets_AR%s'%variation] #LO
            #node['WJets_AR%s'%variation] = node['WJets_LOincl_AR%s'%variation] + node['W1Jets_AR%s'%variation] + node['W2Jets_AR%s'%variation] + node['W3Jets_AR%s'%variation] + node['W4Jets_AR%s'%variation] #LO
            node['DYJets_AR%s'%variation] = node['DYJets_incl_AR%s'%variation] + node['DYJets_0J_AR%s'%variation] + node['DYJets_1J_AR%s'%variation] + node['DYJets_2J_AR%s'%variation] #NLO
            node['WJets_AR%s'%variation] = node['WJets_incl_AR%s'%variation] + node['WJets_0J_AR%s'%variation] + node['WJets_1J_AR%s'%variation] + node['WJets_2J_AR%s'%variation] #NLO
            node['MC_AR%s'%variation] = node['DYJets_AR%s'%variation] + node['WJets_AR%s'%variation] + node['TT_AR%s'%variation] + node['ST_AR%s'%variation] + node['VBF_AR%s'%variation] + node['ZH_AR%s'%variation] + node['VV_AR%s'%variation] + node['ttH_AR%s'%variation] + node['jjHtautau_AR%s'%variation]
            node['QCD%s'%variation] = node['data_obs_AR%s'%variation]-node['MC_AR%s'%variation]
            if variation in ["_btag_up","_btag_down"]:
                node['MC%s'%variation] = node['DYJets%s'%variation] + node['WJets%s'%variation] + node['TT%s'%variation] + node['ST%s'%variation] + node['QCD%s'%variation] + node['VV%s'%variation] + node['VBF%s'%variation] + node['ZH%s'%variation] + node['ttH%s'%variation] + node['jjHtautau%s'%variation]
            #### summing all bkg including QCD ####
        node['MC'] = node['DYJets'] + node['WJets'] + node['TT'] + node['ST'] + node['QCD'] + node['VV'] + node['VBF'] + node['ZH'] + node['ttH'] + node['jjHtautau']

else:
    for selection_DR in selections_DR:
        hists_DR = hists[selection_DR["name"]]
        for path, node in hists_DR.ListNodes(withObjects=True):
            node['ST_AR'] = node['ST_t_channel_antitop_AR'] + node['ST_t_channel_top_AR'] + node['ST_s_channel_AR'] + node['ST_tW_antitop_AR'] + node['ST_tW_top_AR']
            node['TT_AR'] = node['TTTo2L2Nu_AR'] + node['TTToHadronic_AR'] + node['TTToSemiLeptonic_AR']
            node['VV_AR'] = node['WWTo2L2Nu_AR'] + node['WWTo1L1Nu2Q_AR'] + node['WWTo4Q_AR'] + node['WZTo3LNu_AR'] + node['WZTo2L2Q_AR'] + node['WZTo1L3Nu_AR'] + node['WZTo1L1Nu2Q_AR'] + node['ZZTo4L_AR'] + node['ZZTo2L2Q_AR'] + node['ZZTo2Q2Nu_AR']
            #node['DYJets_AR'] = node['DYJets_LOincl_AR'] + node['DY1Jets_AR'] + node['DY2Jets_AR'] + node['DY3Jets_AR'] + node['DY4Jets_AR'] #LO
            #node['WJets_AR'] = node['WJets_LOincl_AR']+ node['W1Jets_AR']+ node['W2Jets_AR']+ node['W3Jets_AR']+ node['W4Jets_AR'] #LO
            node['DYJets_AR'] = node['DYJets_incl_AR'] + node['DYJets_0J_AR'] + node['DYJets_1J_AR'] + node['DYJets_2J_AR'] #NLO
            node['WJets_AR'] = node['WJets_incl_AR']+ node['WJets_0J_AR']+ node['WJets_1J_AR']+ node['WJets_2J_AR']  #NLO
            node['MC_AR'] = node['DYJets_AR'] + node['WJets_AR'] + node['TT_AR'] + node['ST_AR'] + node['VV_AR']
            node['QCD'] = node['data_obs_AR']-node['MC_AR']
            node['ST'] = node['ST_t_channel_antitop'] + node['ST_t_channel_top'] + node['ST_s_channel'] + node['ST_tW_antitop'] + node['ST_tW_top']
            node['VV'] = node['WWTo2L2Nu'] + node['WWTo4Q'] + node['WWTo1L1Nu2Q'] + node['WZTo1L1Nu2Q'] + node['WZTo1L3Nu'] + node['WZTo2L2Q'] + node['WZTo3LNu'] + node['ZZTo2L2Q'] + node['ZZTo2Q2Nu'] + node['ZZTo4L']
            node['TT'] = node['TTTo2L2Nu'] + node['TTToHadronic'] + node['TTToSemiLeptonic']
            #node['DYJets'] = node['DYJets_LOincl'] + node['DY1Jets'] + node['DY2Jets'] + node['DY3Jets'] + node['DY4Jets'] #LO
            #node['WJets'] = node['WJets_LOincl']+ node['W1Jets']+ node['W2Jets']+ node['W3Jets']+ node['W4Jets'] #LO
            node['DYJets'] = node['DYJets_incl'] + node['DYJets_0J'] + node['DYJets_1J'] + node['DYJets_2J'] #NLO
            node['WJets'] = node['WJets_incl']+ node['WJets_0J']+ node['WJets_1J']+ node['WJets_2J']  #NLO
            node['jjHtautau'] = node['jjH'] + node['jjH_inc'] + node['ggjjH']
            node['MC'] = node['DYJets'] + node['WJets'] + node['TT'] + node['ST'] + node['VV'] + node['QCD'] + node['ttH'] + node['jjHtautau'] + node['VBF'] + node['ZH']
            #if selection_DR["name"]=="DR_W":
            #    print "selection_DR:",selection_DR["name"]
            #    node['data_obs']=node['data_obs']-node['DYJets']-node['TT']-node['ST']-node['VV']
            if year=='2018':
                node['ggH'] = node['ggH_inc'] + node['ggbbH']# + node['ggbbH_ext']
                #node['bbH_ybybyt'] = node['bbH'] + node['bbH_ybyt']
                node['bbHtautau'] = node['bbH'] + node['ggH_inc'] + node['ggbbH'] #+ node['ggbbH_ext'] + node['bbH_ybyt']
            else:
                node['ggH'] = node['ggH_inc'] + node['ggbbH']
                #node['bbH_ybybyt'] = node['bbH'] + node['bbH_ybyt']
                node['bbHtautau'] = node['bbH'] + node['ggH_inc'] + node['ggbbH']#+ node['bbH_ybyt'] 


if isBDT:
    if isNN:
        fout = ROOT.TFile('./root/%s_%s%s%s%s_NNBDT.root'%(channel,ULtag,year,preVFP,sysvar), 'RECREATE')
    else:
        fout = ROOT.TFile('./root/%s_%s%s%s%s_BDT.root'%(channel,ULtag,year,preVFP,sysvar), 'RECREATE')
elif plotDR:
    fout = ROOT.TFile('./root/%s_%s%s%s_DR.root'%(channel,ULtag,year,preVFP), 'RECREATE')
else:
    fout = ROOT.TFile('./root/%s_%s%s%s%s.root'%(channel,ULtag,year,preVFP,sysvar), 'RECREATE')
NodeToTDir(fout, hists)
fout.Close()

#fout = ROOT.TFile('../CorrectionTools/fakefactor/root/DR_%s_%s%s%s.root'%(channel,ULtag,year,preVFP), 'RECREATE')
#NodeToTDir(fout, hists)
#fout.Close()
