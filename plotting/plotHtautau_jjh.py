import ROOT
from analysis import *
from argparse import ArgumentParser
import json
import utils
import sys
import shutil
sys.path.insert(1, os.path.join(sys.path[0], '..')) #to get file in parent directory
from xsections import xsection
from samplenames import getsamples

# import CombineHarvester.CombineTools.plotting as plot

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.TH1.AddDirectory(False)

parser = ArgumentParser()
parser.add_argument('-y', '--year',    dest='year', type=str, default='2018', action='store')
parser.add_argument('-c', '--channel', dest='channel', type=str, default='mutau', action='store')
parser.add_argument('-b', '--BDT', default=False,action='store_true')
parser.add_argument('-p', '--preVFP',  dest='preVFP', action='store_const', const="_preVFP",default="")
parser.add_argument('-t', '--comb',  dest='UL2016comb', action='store_true',default=False)
parser.add_argument('-s', '--sysvar', dest='sysvar', type=str, default='', action='store',choices=["jesTotalUp","jesTotalDown","jerUp","jerDown","met_unclusteredUp","met_unclusteredDown","jesAbsoluteUp","jesAbsoluteDown","jesAbsolute_2018Up","jesAbsolute_2018Down","jesAbsolute_2017Up","jesAbsolute_2017Down","jesAbsolute_2016Up","jesAbsolute_2016Down","jesBBEC1Up","jesBBEC1Down","jesBBEC1_2018Up","jesBBEC1_2018Down","jesBBEC1_2017Up","jesBBEC1_2017Down","jesBBEC1_2016Up","jesBBEC1_2016Down","jesEC2Up","jesEC2Down","jesEC2_2018Up","jesEC2_2018Down","jesEC2_2017Up","jesEC2_2017Down","jesEC2_2016Up","jesEC2_2016Down","jesFlavorQCDUp","jesFlavorQCDDown","jesHFUp","jesHFDown","jesHF_2018Up","jesHF_2018Down","jesHF_2017Up","jesHF_2017Down","jesHF_2016Up","jesHF_2016Down","jesRelativeBalUp","jesRelativeBalDown","jesRelativeSample_2018Up","jesRelativeSample_2018Down","jesRelativeSample_2017Up","jesRelativeSample_2017Down","jesRelativeSample_2016Up","jesRelativeSample_2016Down","scale_t_1prongUp","scale_t_1prongDown","scale_t_1prong1piUp","scale_t_1prong1piDown","scale_t_3prongUp","scale_t_3prongDown"])
args = parser.parse_args()

year = args.year
channel = args.channel
sysvar = args.sysvar
preVFP = args.preVFP
isBDT = args.BDT
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
sysvar_noyear = sysvar

if channel=="mutau":
    channel_sys = "mt"
elif channel=="etau":
    channel_sys = "et"
else:
    channel_sys = channel


if isBDT:
    samplesdir = '/pnfs/psi.ch/cms/trivcat/store/user/pbaertsc/bbh/samples_UL%s%s%s_BDT_jjh/%s/'%(year,preVFP,sysvar,channel)   
else:
    samplesdir = '/pnfs/psi.ch/cms/trivcat/store/user/pbaertsc/bbh/samples_UL%s%s%s/'%(year,preVFP,sysvar)

hists = Node()

weight_run2017B = 4.823
weight_run2017C = 9.664
weight_run2017D = 4.252
weight_run2017E = 9.278
weight_run2017F = 13.54
weight_run2017BCDEF = 41.557

weight_run2018A = 14.0
weight_run2018B = 7.1
weight_run2018C = 6.94
weight_run2018D = 31.93
weight_run2018ABCD = 59.97

selections_prong = [
    {'name':'1prong',
     'selection':'&& (Tau1_decaymode==0 || Tau1_decaymode==1 || Tau1_decaymode==2)'},
    {'name':'3prong',
     'selection':'&& (Tau1_decaymode==10 || Tau1_decaymode==11)'}]

if preVFP=="_comb" or year!="2016":
    btag_variations = ['btag%s_jesUp'%year,'btag%s_jesDown'%year,'btag%s_lfUp'%year,'btag%s_lfDown'%year,'btag%s_hfUp'%year,'btag%s_hfDown'%year,'btag%s_hfstats1Up'%year,'btag%s_hfstats1Down'%year,'btag%s_hfstats2Up'%year,'btag%s_hfstats2Down'%year,'btag%s_lfstats1Up'%year,'btag%s_lfstats1Down'%year,'btag%s_lfstats2Up'%year,'btag%s_lfstats2Down'%year,'btag%s_cferr1Up'%year,'btag%s_cferr1Down'%year,'btag%s_cferr2Up'%year,'btag%s_cferr2Down'%year]
else:
    btag_variations = ['btag2016_lfUp','btag2016_lfDown','btag2016_hfUp','btag2016_hfDown','btag2016_cferr1Up','btag2016_cferr1Down','btag2016_cferr2Up','btag2016_cferr2Down','btag2016_preVFP_jesUp','btag2016_preVFP_jesDown','btag2016_preVFP_hfstats1Up','btag2016_preVFP_hfstats1Down','btag2016_preVFP_hfstats2Up','btag2016_preVFP_hfstats2Down','btag2016_preVFP_lfstats1Up','btag2016_preVFP_lfstats1Down','btag2016_preVFP_lfstats2Up','btag2016_preVFP_lfstats2Down','btag2016_postVFP_jesUp','btag2016_postVFP_jesDown','btag2016_postVFP_hfstats1Up','btag2016_postVFP_hfstats1Down','btag2016_postVFP_hfstats2Up','btag2016_postVFP_hfstats2Down','btag2016_postVFP_lfstats1Up','btag2016_postVFP_lfstats1Down','btag2016_postVFP_lfstats2Up','btag2016_postVFP_lfstats2Down']

ff_variations = ['ff%s_qcdUp'%year,'ff%s_qcdDown'%year,'ff%s_wUp'%year,'ff%s_wDown'%year,'ff%s_ttUp'%year,'ff%s_ttDown'%year,'ff%s_qcdfitpar0Up'%year,'ff%s_qcdfitpar0Down'%year,'ff%s_qcdfitpar1Up'%year,'ff%s_qcdfitpar1Down'%year,'ff%s_wfitpar0Up'%year,'ff%s_wfitpar0Down'%year,'ff%s_wfitpar1Up'%year,'ff%s_wfitpar1Down'%year,'ff%s_wfitpar2Up'%year,'ff%s_wfitpar2Down'%year,'ff%s_ttfitpar0Up'%year,'ff%s_ttfitpar0Down'%year,'ff%s_ttfitpar1Up'%year,'ff%s_ttfitpar1Down'%year,'ff%s_fracUp'%year,'ff%s_fracDown'%year]
tauid_variations = ['CMS_eff_t_1prong_%sUp'%year,'CMS_eff_t_1prong_%sDown'%year,'CMS_eff_t_1prong1pi_%sUp'%year,'CMS_eff_t_1prong1pi_%sDown'%year,'CMS_eff_t_3prong_%sUp'%year,'CMS_eff_t_3prong_%sDown'%year]

if "Total" in sysvar or "jer" in sysvar or "met" in sysvar or "scale_t" in sysvar:
    if "Up" in sysvar:
        sysvar = sysvar[:-2]+year+"Up"
    elif "Down" in sysvar:
        sysvar = sysvar[:-4]+year+"Down"


drawvars = [
    ('Mu1_pt',      'Mu1_pt',       (30, 0, 130)),
    ('Mu1_eta',     'Mu1_eta',      (30, -2.5, 2.5)),
    ('Mu1_phi',     'Mu1_phi',      (30, -3.2, 3.2)),
    #('Mu1_mass',    'Mu1_mass',     (30, 0., 0.2)),
    ('Ele1_pt',     'Ele1_pt',       (30, 0, 130)),
    #('Ele1_pt',     'Ele1_pt',       [25,27.5,30.,32.5,35.,37.5,40.,42.5,45.,47.5,50.,52.5,55.,57.5,60.,65.,70.,75.,80.,85.,90.,100.,105.,110.,115.,120.,125.,130.]),
    ('Ele1_eta',    'Ele1_eta',      (30, -2.5, 2.5)),
    #('Ele1_phi',    'Ele1_phi',      (30, -3.2, 3.2)),
    #('Ele1_mass',   'Ele1_mass',     (30, 0., 0.2)),
    ('Tau1_pt',     'Tau1_pt',      (30, 0, 130)),
    ('Tau1_eta',    'Tau1_eta',     (30, -2.5, 2.5)),
    ('Tau1_phi',    'Tau1_phi',     (30, -3.2, 3.2)),
    ('Tau1_mass',   'Tau1_mass',    (30, 0., 2.)),
    ('Tau1_decaymode', 'Tau1_decaymode', (12,0,12)),
    #('Tau1_Idvsjet','Tau1_Idvsjet',(30,0.,300.)),
    #('Tau1_Idvsmu', 'Tau1_Idvsmu',  (30,0.,300.)),
    #('Tau1_Idvse', 'Tau1_Idvse',    (30,0.,300.)),
    ('vistau1_pt',  'vistau1_pt',   (30, 0, 130)),
    ('vistau1_eta', 'vistau1_eta',  (30, -2.5, 2.5)),
    ('vistau1_phi', 'vistau1_phi',  (30, -3.2, 3.2)),
    ('vistau1_mass','vistau1_mass', (30, 0., 0.2)),
    ('Jet1_pt',     'Jet1_pt',      (30, 0, 200)),
    ('Jet1_eta',    'Jet1_eta',     (30, -2.5, 2.5)),
    ('Jet1_phi',    'Jet1_phi',     (30, -3.2, 3.2)),
    ('Jet1_mass',   'Jet1_mass',    (30, 0., 10.)),
    ('Jet1_btag',   'Jet1_btag',    (20, 0., 1.)),
    ('Jet2_pt',     'Jet2_pt',      (30, 0, 150)),
    ('Jet2_eta',    'Jet2_eta',     (30, -2.5, 2.5)),
    ('Jet2_phi',    'Jet2_phi',     (30, -3.2, 3.2)),
    ('Jet2_mass',   'Jet2_mass',    (30, 0., 10.)),
    ('Jet2_btag',   'Jet2_btag',    (30, 0., 1.)),
    ('Jet3_pt',     'Jet3_pt',      (30, 0, 150)),
    #('Jet3_eta',    'Jet3_eta',     (30, -2.5, 2.5)),
    #('Jet3_phi',    'Jet3_phi',     (30, -3.2, 3.2)),
    #('Jet3_mass',   'Jet3_mass',    (30, 0., 10.)),
    #('Jet3_btag',   'Jet3_btag',    (30, 0., 1.)),
    ('Bjet1_pt',    'Bjet1_pt',     (30, 0, 300)),
    ('Bjet1_eta',   'Bjet1_eta',    (30, -2.5, 2.5)),
    ('Bjet1_phi',   'Bjet1_phi',    (30, -3.2, 3.2)),
    ('Bjet1_mass',  'Bjet1_mass',   (30, 0., 10.)),
    ('Bjet2_pt',    'Bjet2_pt',     (30, 0, 300)),
    ('Bjet2_eta',   'Bjet2_eta',    (30, -2.5, 2.5)),
    ('Bjet2_phi',   'Bjet2_phi',    (30, -3.2, 3.2)),
    ('Bjet2_mass',  'Bjet2_mass',   (30, 0., 10.)),
    ('vis_pt',      'vis_pt',       (30, 0, 300)),
    ('vis_eta',     'vis_eta',      (30, -2.5, 2.5)),
    ('vis_phi',     'vis_phi',      (30, -3.2, 3.2)),
    ('vis_mass',    'vis_mass',     (30, 0., 250.)),
    ('collinear_mass', 'collinear_mass', (30, 0.,350.)),
    ('transverse_mass_lepmet', 'transverse_mass_lepmet',     (20, 0., 60.)),
    ('mt', 'mt',     (20, 0., 60.)),
    ('H_pt',        'H_pt',         (30, 0, 300)),
    ('H_eta',       'H_eta',        (30, -2.5, 2.5)),
    ('H_phi',       'H_phi',        (30, -3.2, 3.2)),
    ('H_mass',      'H_mass',       (30, 0., 350.)),
    #('H_mass',      'H_mass',       (30, 0, 500.)),
    ('MET',         'MET',          (30, 0, 150)),
    ('MET_chs',     'MET_chs',      (30, 0, 150)),
    ('MET_px',      'MET_px',       (30, 0, 150)),
    ('MET_py',      'MET_py',       (30, 0, 150)),
    ('MET_covXX',   'MET_covXX',    (30, 0, 1500)),
    ('MET_covXY',   'MET_covXY',    (30, -200, 200)),
    ('MET_covYY',   'MET_covYY',    (30, 0, 1500)),
    #('nMuons',      'nMuons',       (5, 0., 5.)),
    #('nElectrons',  'nElectrons',   (5, 0., 5.)),
    #('nTaus',       'nTaus',        (5, 0., 5.)),
    ('nJets',       'nJets',        (4, 0., 4.)),
    #('nBjets_l',    'nBjets_l',     (4, 0., 4.)),
    ('nBjets',    'nBjets_m',     (4, 0., 4.)),
    #('nBjets_t',    'nBjets_t',     (4, 0., 4.)),
    #('nJets_forward','nJets_forward',(4, 0., 4.)),
    #('nGenBjets',   'nGenBjets',    (4, 0., 4.)),
    #('LHE_Nb',      'LHE_Nb',       (4, 0., 4.)),
    #('LHE_NpNLO',   'LHE_NpNLO',    (4, 0., 4.)),
    ('DPhi',        'DPhi',         (30, -5., 5.)),
    ('DEta',        'DEta',         (30,0., 5.)),
    ('DPhiLepMET',  'DPhiLepMET',   (30, -5., 5.)),
    ('DRLepMET',    'DRLepMET',     (30, 0., 5.)),
    #('DRBjets',     'DRBjets',      (30, 0., 10.)),
    #('DEta_Bjets',  'DEta_Bjets',   (30, 0., 4.)),
    #('DPhi_Bjets',  'DPhi_Bjets',   (30, -4., 4.)),
    #('Bjets_pt', 'Bjets_pt',        (30, 0., 200.)),
    #('DRBjets_lm',  'DRBjets_lm',   (30, 0., 10.)),
    ('DRLepJ',      'DRLepJ',        (30, 0., 10.)),
    ('DEtaLepJ',    'DEtaLepJ',      (30, 0., 4.)),
    ('DPhiLepJ',    'DPhiLepJ',      (30, -4., 4.)),
    ('DRTauJ',      'DRTauJ',       (30, 0., 10.)),
    ('DEtaTauJ',    'DEtaTauJ',     (30, 0., 4.)),
    ('DEtaTauJ2',   'DEtaTauJ2',     (30, 0., 4.)),
    ('DPhiTauJ',    'DPhiTauJ',     (30, -4., 4.)),
    #('DRLepJ2',     'DRLepJ2',        (30, 0., 10.)),
    #('DEtaLepJ2',   'DEtaLepJ2',      (30, 0., 4.)),
    #('DPhiLepJ2',   'DPhiLepJ2',      (30, -4., 4.)),
    #('DRTauJ2',     'DRTauJ2',       (30, 0., 10.)),
    ('HJ_mass',     'HJ_mass',      (30, 0., 300.)),
    ('vistauJ_mass', 'vistauJ_mass',(30, 0., 300.)),
    #('vistauJMET_mass', 'vistauJMET_mass', (30, 0., 300.)),
    #('TauJMET_mass', 'TauJMET_mass',(30, 0., 300.)),
    ('TauJ_mass', 'TauJ_mass',      (30, 0., 300.)),
    #('METJ_mass', 'METJ_mass',      (30, 0., 300.)),
    ('Dzeta', 'Dzeta',              (30, -100.,100.)),
    #('mt2', 'mt2',                  (30, 0.,60.)),
    #('wt_ff', 'wt_ff',              (30, 0.,1.)),
    #('wt_ff_ttdr', 'wt_ff_ttdr',    (30, 0.,1.)),
    #('transverse_mass_taumet', 'transverse_mass_taumet', (30,0.,200.)),
    #('transverse_mass_leptau', 'transverse_mass_leptau', (30,0.,200.)),
    ('transverse_mass_total', 'transverse_mass_total', (30,0.,300.)),
    ('DRjets', 'DRjets', (30, 0., 6.)),
    ('DEta_jets', 'DEta_jets', (30, 0., 4.)),
    #('DPhi_jets', 'DPhi_jets', (30, -4., 4.)),
    #('DEta_jets_forward', 'DEta_jets_forward', (30, 0., 10.)),
    ('dijet_pt', 'dijet_pt', (30, 0., 200.)),
    ('dijet_eta', 'dijet_eta', (30, -4.,4.)),
    ('dijet_phi', 'dijet_phi', (30, -4.,4.)),
    ('dijet_mass', 'dijet_mass', (30, 0.,350.)),
    #('LepJ_pt', 'LepJ_pt', (30, 0., 200.)),
    #('TauJ_pt', 'TauJ_pt', (30, 0.,200.)),
    ('vistauJ_pt', 'vistauJ_pt', (30,0.,200.)),
    #('vistauJMET_pt', 'vistauJMET_pt', (30,0.,200.)),
    #('TauJMET_pt', 'TauJMET_pt', (30,0.,200.)),
    #('LepJMET_pt', 'LepJMET_pt', (30,0.,200.)),
    #('METJ_pt', 'METJ_pt', (30,0.,200.)),
    #('vistauMET_pt', 'vistauMET_pt', (30,0.,200.)),
    ('HJ_pt', 'HJ_pt', (30,0.,200.)),
    ('DRHJ', 'DRHJ', (30,0,5.)),
    ('DRHJ2', 'DRHJ2', (30,0,5.)),
    ('BTagWeight', 'BTagWeight', (30,0,3.)),
]

if isBDT:
    drawvars = [    
        ('BDTisSignal', 'BDTisSignal', [0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.75,0.8,0.85,0.9,1.0]),
        ('BDTisTT', 'BDTisTT',          [0,0.5,0.75,1]),
        ('BDTisDY', 'BDTisDY',          [0,0.5,0.75,1]),
        ('BDTisJJH', 'BDTisJJH',          [0,0.5,0.75,1]),
        #('BDToutTT_tt', 'BDTisTT',          [0,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1.]),
        #('BDToutDY_dy', 'BDTisDY',          [0,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1.]),
        ('BDToutput', 'BDToutput',      [0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.75,0.8,0.85,0.9,1.0]),
        ('BDToutTT', 'BDToutTT',      [0,0.5,0.75,1]),
        ('BDToutDY', 'BDToutDY',      [0,0.5,0.75,1]),
        ('BDToutJJH', 'BDToutJJH',      [0,0.5,0.75,1]),
        ('H_mass',      'H_mass',       (30, 0., 350.)),
        #('H_mass_sig',  'H_mass',       (30, 0., 350.)),
        #('H_mass_tt',  'H_mass',       (30, 0., 350.)),
        #('H_mass_dy',  'H_mass',       (30, 0., 350.)),
        ('vis_mass',    'vis_mass',     (30, 0., 250.)),
        ('collinear_mass', 'collinear_mass', (30, 0.,350.)),
        ('Jet1_pt',     'Jet1_pt',      (30, 0, 200)),
        ('transverse_mass_lepmet', 'transverse_mass_lepmet',     (20, 0., 60.)),
        ('mt', 'mt',     (20, 0., 60.)),
        ('TauJ_mass', 'TauJ_mass',      (30, 0., 300.)),
        ('H_pt',        'H_pt',         (30, 0, 300)),
        ('Jet1_btag',   'Jet1_btag',    (20, 0., 1.)),
        ('DEta',        'DEta',         (30,0., 5.)),
        ('DRHJ', 'DRHJ', (30,0,5.)),
        ('Ele1_pt',     'Ele1_pt',       (10, 30, 40)),
        ('DEtaLepJ',    'DEtaLepJ',      (30, 0., 4.)),
        ('Jet2_btag',   'Jet2_btag',    (30, 0., 1.)),
        ('HJ_pt', 'HJ_pt', (30,0.,200.)),
        ('Jet2_pt',     'Jet2_pt',      (30, 0, 150)),
        ('Dzeta', 'Dzeta',              (30, -100.,100.)),
    ]
    if channel=='mutau':
        if year=='2018':
            drawvars = drawvars+[('BDToutSig', 'BDToutSig', [0.0, 0.495, 0.565, 0.64, 0.705, 0.755, 0.805, 0.86, 0.91, 1.0]),]
        elif year=='2017':
            drawvars = drawvars+[('BDToutSig', 'BDToutSig', [0.0, 0.495, 0.565, 0.64, 0.705, 0.755, 0.805, 0.86, 0.91, 1.0]),]
        elif year=='2016':
            drawvars = drawvars+[('BDToutSig', 'BDToutSig', [0.0, 0.495, 0.565, 0.64, 0.705, 0.755, 0.805, 0.86, 0.91, 1.0]),]
    elif channel=='etau':
        if year=='2018':
            drawvars = drawvars+[('BDToutSig', 'BDToutSig', [0.0, 0.555, 0.715, 0.775, 0.835, 0.92, 1.0]),]
        elif year=='2017':
            drawvars = drawvars+[('BDToutSig', 'BDToutSig', [0.0, 0.555, 0.715, 0.775, 0.835, 0.92, 1.0]),]
        elif year=='2016':
            drawvars = drawvars+[('BDToutSig', 'BDToutSig', [0.0, 0.555, 0.715, 0.775, 0.835, 1.0]),]
for dirname, var, binning in drawvars:
    for sample in getsamples(channel,year,preVFP):
        #if preVFP!="" and sample=="data_obs": continue 
        if channel=="mutau":
            if sample=='data_obs': #no veto on gen matched taus and no selection on EventNumber
                selection = 'isHtoMuTau && Mu1_charge*Tau1_charge==-1 && dimuon_veto==0 && electron_veto==0 && extra_muon_veto==0 && nBjets_m>=1 && mt<60'
                selection_ar = 'isHtoMuTauAR && dimuon_veto==0 && electron_veto==0 && Mu1_charge*Tau1_charge==-1 && extra_muon_veto==0 && nBjets_m>=1 && mt<60'
            else:
                selection = 'isHtoMuTau && Mu1_charge*Tau1_charge==-1 && dimuon_veto==0 && electron_veto==0 && extra_muon_veto==0 && Tau1_genmatch!=6 && nBjets_m>=1 && mt<60 && EventNumber%10>=4'
                selection_ar = 'isHtoMuTauAR && dimuon_veto==0 && electron_veto==0 && extra_muon_veto==0 && Mu1_charge*Tau1_charge==-1 && Tau1_genmatch!=6 && nBjets_m>=1 && mt<60 && EventNumber%10>=4'
        elif channel=="etau":
            if sample=='data_obs': #no veto on gen matched taus and no selection on EventNumber
                selection = 'isHtoETau && Ele1_charge*Tau1_charge==-1 && dielectron_veto==0 && muon_veto==0 && extra_electron_veto==0 && nBjets_m>=1 && mt<60'
                selection_ar = 'isHtoETauAR && dielectron_veto==0 && muon_veto==0 && extra_electron_veto==0 && Ele1_charge*Tau1_charge==-1 && nBjets_m>=1 && mt<60'
            else:
                selection = 'isHtoETau && Ele1_charge*Tau1_charge==-1 && dielectron_veto==0 && muon_veto==0 && extra_electron_veto==0 && Tau1_genmatch!=6 && nBjets_m>=1 && mt<60 && EventNumber%10>=4'
                selection_ar = 'isHtoETauAR && dielectron_veto==0 && muon_veto==0 && extra_electron_veto==0 && Ele1_charge*Tau1_charge==-1 && Tau1_genmatch!=6 && nBjets_m>=1 && mt<60 && EventNumber%10>=4'
        if "sig" in dirname:
            selection = selection + " && BDTSigmax"
            selection_ar = selection_ar + " && BDTSigmax"
        elif "tt" in dirname:
            selection = selection + " && BDTTTmax"
            selection_ar = selection_ar + " && BDTTTmax"
        elif "dy" in dirname:
            selection = selection + " && BDTDYmax"
            selection_ar = selection_ar + " && BDTDYmax"
        if sample=='data_obs':
            weight = '1.'
            weight_btag = '1.'
            weight_ar = 'wt_ff'
            #weight_ar = 'wt_ff_nocorr'
            weight_ar_up = 'wt_ffUp'
            weight_ar_down = 'wt_ffDown'
        else:
            if channel=="mutau":
                weight = 'EventWeight * LumiWeight * (1./0.6) * BTagWeight * PUIdWeight * MuWeight * MuTriggerWeight * TauWeight * wt_tt_pt * wt_tt * wt_dy * wt_w * wt_dy_nlo * wt_w_nlo'
                weight_ar = 'EventWeight * LumiWeight * (1./0.6) * BTagWeight * PUIdWeight * MuWeight * MuTriggerWeight * TauWeight * wt_tt_pt * wt_tt * wt_dy * wt_w* wt_dy_nlo * wt_w_nlo * wt_ff'
                weight_btag = 'EventWeight * LumiWeight * (1./0.6) * PUIdWeight * MuWeight * MuTriggerWeight * TauWeight * wt_tt_pt * wt_tt * wt_dy * wt_w * wt_dy_nlo * wt_w_nlo'
                weight_ar_up = 'EventWeight * LumiWeight * (1./0.6) * BTagWeight * PUIdWeight * MuWeight * MuTriggerWeight * TauWeight * wt_tt_pt * wt_tt * wt_dy * wt_w * wt_dy_nlo * wt_w_nlo * wt_ffUp'
                weight_ar_down = 'EventWeight * LumiWeight * (1./0.6) * BTagWeight * PUIdWeight * MuWeight * MuTriggerWeight * TauWeight * wt_tt_pt * wt_tt * wt_dy * wt_w* wt_dy_nlo * wt_w_nlo * wt_ffDown'
                weight_trig_up = 'EventWeight * LumiWeight * (1./0.6) * BTagWeight * PUIdWeight * MuWeight * MuTriggerWeight_up * TauWeight * wt_tt_pt * wt_tt * wt_dy * wt_w * wt_dy_nlo * wt_w_nlo'
                weight_trig_down = 'EventWeight * LumiWeight * (1./0.6) * BTagWeight * PUIdWeight * MuWeight * MuTriggerWeight_down * TauWeight * wt_tt_pt * wt_tt * wt_dy * wt_w * wt_dy_nlo * wt_w_nlo'
                weight_pu_up = 'EventWeight * LumiWeight * (1./0.6) * BTagWeight * PUIdWeight_up * MuWeight * MuTriggerWeight * TauWeight * wt_tt_pt * wt_tt * wt_dy * wt_w * wt_dy_nlo * wt_w_nlo'
                weight_pu_down = 'EventWeight * LumiWeight * (1./0.6) * BTagWeight * PUIdWeight_down * MuWeight * MuTriggerWeight * TauWeight * wt_tt_pt * wt_tt * wt_dy * wt_w * wt_dy_nlo * wt_w_nlo'
                weight_tt_up = 'EventWeight * LumiWeight * (1./0.6) * BTagWeight * PUIdWeight * MuWeight * MuTriggerWeight * TauWeight * wt_tt_pt_up * wt_tt * wt_dy * wt_w * wt_dy_nlo * wt_w_nlo'
                weight_tt_down = 'EventWeight * LumiWeight * (1./0.6) * BTagWeight * PUIdWeight * MuWeight * MuTriggerWeight * TauWeight * wt_tt_pt_down * wt_tt * wt_dy * wt_w * wt_dy_nlo * wt_w_nlo'
                weight_dy_up = 'EventWeight * LumiWeight * (1./0.6) * BTagWeight * PUIdWeight * MuWeight * MuTriggerWeight * TauWeight * wt_tt_pt * wt_tt * wt_dy_up * wt_w * wt_dy_nlo * wt_w_nlo'
                weight_dy_down = 'EventWeight * LumiWeight * (1./0.6) * BTagWeight * PUIdWeight * MuWeight * MuTriggerWeight * TauWeight * wt_tt_pt * wt_tt * wt_dy_down * wt_w * wt_dy_nlo * wt_w_nlo'
                weight_dy_1b_up = 'EventWeight * LumiWeight * (1./0.6) * BTagWeight * PUIdWeight * MuWeight * MuTriggerWeight * TauWeight * wt_tt_pt * wt_tt * wt_dy_1b_up * wt_w * wt_dy_nlo * wt_w_nlo'
                weight_dy_1b_down = 'EventWeight * LumiWeight * (1./0.6) * BTagWeight * PUIdWeight * MuWeight * MuTriggerWeight * TauWeight * wt_tt_pt * wt_tt * wt_dy_1b_down * wt_w * wt_dy_nlo * wt_w_nlo'
                weight_dy_2b_up = 'EventWeight * LumiWeight * (1./0.6) * BTagWeight * PUIdWeight * MuWeight * MuTriggerWeight * TauWeight * wt_tt_pt * wt_tt * wt_dy_2b_up * wt_w * wt_dy_nlo * wt_w_nlo'
                weight_dy_2b_down = 'EventWeight * LumiWeight * (1./0.6) * BTagWeight * PUIdWeight * MuWeight * MuTriggerWeight * TauWeight * wt_tt_pt * wt_tt * wt_dy_2b_down * wt_w * wt_dy_nlo * wt_w_nlo'
                weight_dy_xsecup = 'EventWeight * LumiWeight * (1./0.6) * BTagWeight * PUIdWeight * MuWeight * MuTriggerWeight * TauWeight * wt_tt_pt * wt_tt * wt_dy_ttxsecup * wt_w * wt_dy_nlo * wt_w_nlo'
                weight_dy_xsecdown = 'EventWeight * LumiWeight * (1./0.6) * BTagWeight * PUIdWeight * MuWeight * MuTriggerWeight * TauWeight * wt_tt_pt * wt_tt * wt_dy_ttxsecdown * wt_w * wt_dy_nlo * wt_w_nlo'
                weight_dy_1b_xsecup = 'EventWeight * LumiWeight * (1./0.6) * BTagWeight * PUIdWeight * MuWeight * MuTriggerWeight * TauWeight * wt_tt_pt * wt_tt * wt_dy_1b_ttxsecup * wt_w * wt_dy_nlo * wt_w_nlo'
                weight_dy_1b_xsecdown = 'EventWeight * LumiWeight * (1./0.6) * BTagWeight * PUIdWeight * MuWeight * MuTriggerWeight * TauWeight * wt_tt_pt * wt_tt * wt_dy_1b_ttxsecdown * wt_w * wt_dy_nlo * wt_w_nlo'
                weight_dy_2b_xsecup = 'EventWeight * LumiWeight * (1./0.6) * BTagWeight * PUIdWeight * MuWeight * MuTriggerWeight * TauWeight * wt_tt_pt * wt_tt * wt_dy_2b_ttxsecup * wt_w * wt_dy_nlo * wt_w_nlo'
                weight_dy_2b_xsecdown = 'EventWeight * LumiWeight * (1./0.6) * BTagWeight * PUIdWeight * MuWeight * MuTriggerWeight * TauWeight * wt_tt_pt * wt_tt * wt_dy_2b_ttxsecdown * wt_w * wt_dy_nlo * wt_w_nlo'
                weight_fake_m_up = 'EventWeight * LumiWeight * (1./0.6) * BTagWeight * PUIdWeight * MuWeight * MuTriggerWeight * TauWeightVSjet * TauWeightVSe * TauWeightVSmu_up * wt_tt_pt * wt_tt * wt_dy * wt_w * wt_dy_nlo * wt_w_nlo'
                weight_fake_m_down = 'EventWeight * LumiWeight * (1./0.6) * BTagWeight * PUIdWeight * MuWeight * MuTriggerWeight * TauWeightVSjet * TauWeightVSe * TauWeightVSmu_down * wt_tt_pt * wt_tt * wt_dy * wt_w * wt_dy_nlo * wt_w_nlo'
                weight_fake_e_up = 'EventWeight * LumiWeight * (1./0.6) * BTagWeight * PUIdWeight * MuWeight * MuTriggerWeight * TauWeightVSjet * TauWeightVSmu * TauWeightVSe_up * wt_tt_pt * wt_tt * wt_dy * wt_w * wt_dy_nlo * wt_w_nlo'
                weight_fake_e_down = 'EventWeight * LumiWeight * (1./0.6) * BTagWeight * PUIdWeight * MuWeight * MuTriggerWeight * TauWeightVSjet * TauWeightVSmu * TauWeightVSe_down * wt_tt_pt * wt_tt * wt_dy * wt_w * wt_dy_nlo * wt_w_nlo'
                weight_notauidvsjet = 'EventWeight * LumiWeight * (1./0.6) * BTagWeight * PUIdWeight * MuWeight * MuTriggerWeight * TauWeightVSmu * TauWeightVSe * wt_tt_pt * wt_tt * wt_dy * wt_w * wt_dy_nlo * wt_w_nlo' 
        
            elif channel=="etau":
                weight = 'EventWeight * LumiWeight * (1./0.6) * BTagWeight * PUIdWeight * EWeight * ETriggerWeight * TauWeight * wt_tt_pt * wt_tt * wt_dy * wt_w * wt_dy_nlo * wt_w_nlo'
                weight_ar = 'EventWeight * LumiWeight * (1./0.6) * BTagWeight * PUIdWeight * EWeight * ETriggerWeight * TauWeight * wt_tt_pt * wt_tt * wt_dy * wt_w *  wt_dy_nlo * wt_w_nlo * wt_ff'
                #weight_ar = 'EventWeight * LumiWeight * (1./0.6) * BTagWeight * PUIdWeight * EWeight * ETriggerWeight * TauWeight * wt_tt_pt * wt_tt * wt_dy * wt_w *  wt_dy_nlo * wt_w_nlo * wt_ff_nocorr'
                weight_btag = 'EventWeight * LumiWeight * (1./0.6) * PUIdWeight * EWeight * ETriggerWeight * TauWeight * wt_tt_pt * wt_tt * wt_dy * wt_w * wt_dy_nlo * wt_w_nlo'
                weight_ar_up = 'EventWeight * LumiWeight * (1./0.6) * BTagWeight * PUIdWeight * EWeight * ETriggerWeight * TauWeight * wt_tt_pt * wt_tt * wt_dy * wt_w * wt_dy_nlo * wt_w_nlo * wt_ffUp'
                weight_ar_down = 'EventWeight * LumiWeight * (1./0.6) * BTagWeight * PUIdWeight * EWeight * ETriggerWeight * TauWeight * wt_tt_pt * wt_tt * wt_dy * wt_w* wt_dy_nlo * wt_w_nlo * wt_ffDown'
                weight_trig_up = 'EventWeight * LumiWeight * (1./0.6) * BTagWeight * PUIdWeight * EWeight * ETriggerWeight_up * TauWeight * wt_tt_pt * wt_tt * wt_dy * wt_w * wt_dy_nlo * wt_w_nlo'
                weight_trig_down = 'EventWeight * LumiWeight * (1./0.6) * BTagWeight * PUIdWeight * EWeight * ETriggerWeight_down * TauWeight * wt_tt_pt * wt_tt * wt_dy * wt_w * wt_dy_nlo * wt_w_nlo'
                weight_pu_up = 'EventWeight * LumiWeight * (1./0.6) * BTagWeight * PUIdWeight_up * EWeight * ETriggerWeight * TauWeight * wt_tt_pt * wt_tt * wt_dy * wt_w * wt_dy_nlo * wt_w_nlo'
                weight_pu_down = 'EventWeight * LumiWeight * (1./0.6) * BTagWeight * PUIdWeight_down * EWeight * ETriggerWeight * TauWeight * wt_tt_pt * wt_tt * wt_dy * wt_w * wt_dy_nlo * wt_w_nlo'
                weight_tt_up = 'EventWeight * LumiWeight * (1./0.6) * BTagWeight * PUIdWeight * EWeight * ETriggerWeight * TauWeight * wt_tt_pt_up * wt_tt * wt_dy * wt_w * wt_dy_nlo * wt_w_nlo'
                weight_tt_down = 'EventWeight * LumiWeight * (1./0.6) * BTagWeight * PUIdWeight * EWeight * ETriggerWeight * TauWeight * wt_tt_pt_down * wt_tt * wt_dy * wt_w * wt_dy_nlo * wt_w_nlo'
                weight_dy_up = 'EventWeight * LumiWeight * (1./0.6) * BTagWeight * PUIdWeight * EWeight * ETriggerWeight * TauWeight * wt_tt_pt * wt_tt * wt_dy_up * wt_w * wt_dy_nlo * wt_w_nlo'
                weight_dy_down = 'EventWeight * LumiWeight * (1./0.6) * BTagWeight * PUIdWeight * EWeight * ETriggerWeight * TauWeight * wt_tt_pt * wt_tt * wt_dy_down * wt_w * wt_dy_nlo * wt_w_nlo'
                weight_dy_1b_up = 'EventWeight * LumiWeight * (1./0.6) * BTagWeight * PUIdWeight * EWeight * ETriggerWeight * TauWeight * wt_tt_pt * wt_tt * wt_dy_1b_up * wt_w * wt_dy_nlo * wt_w_nlo'
                weight_dy_1b_down = 'EventWeight * LumiWeight * (1./0.6) * BTagWeight * PUIdWeight * EWeight * ETriggerWeight * TauWeight * wt_tt_pt * wt_tt * wt_dy_1b_down * wt_w * wt_dy_nlo * wt_w_nlo'
                weight_dy_2b_up = 'EventWeight * LumiWeight * (1./0.6) * BTagWeight * PUIdWeight * EWeight * ETriggerWeight * TauWeight * wt_tt_pt * wt_tt * wt_dy_2b_up * wt_w * wt_dy_nlo * wt_w_nlo'
                weight_dy_2b_down = 'EventWeight * LumiWeight * (1./0.6) * BTagWeight * PUIdWeight * EWeight * ETriggerWeight * TauWeight * wt_tt_pt * wt_tt * wt_dy_2b_down * wt_w * wt_dy_nlo * wt_w_nlo'
                weight_dy_xsecup = 'EventWeight * LumiWeight * (1./0.6) * BTagWeight * PUIdWeight * EWeight * ETriggerWeight * TauWeight * wt_tt_pt * wt_tt * wt_dy_ttxsecup * wt_w * wt_dy_nlo * wt_w_nlo'
                weight_dy_xsecdown = 'EventWeight * LumiWeight * (1./0.6) * BTagWeight * PUIdWeight * EWeight * ETriggerWeight * TauWeight * wt_tt_pt * wt_tt * wt_dy_ttxsecdown * wt_w * wt_dy_nlo * wt_w_nlo'
                weight_dy_1b_xsecup = 'EventWeight * LumiWeight * (1./0.6) * BTagWeight * PUIdWeight * EWeight * ETriggerWeight * TauWeight * wt_tt_pt * wt_tt * wt_dy_1b_ttxsecup * wt_w * wt_dy_nlo * wt_w_nlo'
                weight_dy_1b_xsecdown = 'EventWeight * LumiWeight * (1./0.6) * BTagWeight * PUIdWeight * EWeight * ETriggerWeight * TauWeight * wt_tt_pt * wt_tt * wt_dy_1b_ttxsecdown * wt_w * wt_dy_nlo * wt_w_nlo'
                weight_dy_2b_xsecup = 'EventWeight * LumiWeight * (1./0.6) * BTagWeight * PUIdWeight * EWeight * ETriggerWeight * TauWeight * wt_tt_pt * wt_tt * wt_dy_2b_ttxsecup * wt_w * wt_dy_nlo * wt_w_nlo'
                weight_dy_2b_xsecdown = 'EventWeight * LumiWeight * (1./0.6) * BTagWeight * PUIdWeight * EWeight * ETriggerWeight * TauWeight * wt_tt_pt * wt_tt * wt_dy_2b_ttxsecdown * wt_w * wt_dy_nlo * wt_w_nlo'
                weight_fake_m_up = 'EventWeight * LumiWeight * (1./0.6) * BTagWeight * PUIdWeight * EWeight * ETriggerWeight * TauWeightVSjet * TauWeightVSe * TauWeightVSmu_up * wt_tt_pt * wt_tt * wt_dy * wt_w * wt_dy_nlo * wt_w_nlo'
                weight_fake_m_down = 'EventWeight * LumiWeight * (1./0.6) * BTagWeight * PUIdWeight * EWeight * ETriggerWeight * TauWeightVSjet * TauWeightVSe * TauWeightVSmu_down * wt_tt_pt * wt_tt * wt_dy * wt_w * wt_dy_nlo * wt_w_nlo'
                weight_fake_e_up = 'EventWeight * LumiWeight * (1./0.6) * BTagWeight * PUIdWeight * EWeight * ETriggerWeight * TauWeightVSjet * TauWeightVSmu * TauWeightVSe_up * wt_tt_pt * wt_tt * wt_dy * wt_w * wt_dy_nlo * wt_w_nlo'
                weight_fake_e_down = 'EventWeight * LumiWeight * (1./0.6) * BTagWeight * PUIdWeight * EWeight * ETriggerWeight * TauWeightVSjet * TauWeightVSmu * TauWeightVSe_down * wt_tt_pt * wt_tt * wt_dy * wt_w * wt_dy_nlo * wt_w_nlo'
                weight_notauidvsjet = 'EventWeight * LumiWeight * (1./0.6) * BTagWeight * PUIdWeight * EWeight * ETriggerWeight * TauWeightVSmu * TauWeightVSe * wt_tt_pt * wt_tt * wt_dy * wt_w * wt_dy_nlo * wt_w_nlo'
        if "intH" in sample: #negative weights cause problems with combine
            weight = weight + '* -1.'
            weight_btag = weight_btag + '* -1.'
            weight_ar = weight_ar + '* -1.'
            weight_ar_up = weight_ar_up + '* -1.'
            weight_ar_down = weight_ar_down + '* -1.'
            weight_trig_up = weight_trig_up + '* -1.'
            weight_trig_down = weight_trig_down + '* -1.'
            weight_pu_up = weight_pu_up + '* -1.'
            weight_pu_down = weight_pu_down + '* -1.'
            weight_tt_up = weight_tt_up + '* -1.'
            weight_tt_down = weight_tt_down + '* -1.'
            weight_dy_up = weight_dy_up + '* -1.'
            weight_dy_down = weight_dy_down + '* -1.'
            weight_fake_m_up = weight_fake_m_up +'* -1.'
            weight_fake_m_down = weight_fake_m_down +'* -1.'
            weight_fake_e_up = weight_fake_e_up +'* -1.'
            weight_fake_e_down = weight_fake_e_down +'* -1.'
            weight_notauidvsjet = weight_notauidvsjet +'* -1.'
        if year in ["2017","2016"] and sample!="data_obs":
            weight = weight + '* PrefireWeight'
            weight_btag = weight_btag + '* PrefireWeight'
            weight_ar = weight_ar + '* PrefireWeight'
            weight_ar_up = weight_ar_up + '* PrefireWeight'
            weight_ar_down = weight_ar_down + '* PrefireWeight'
            weight_trig_up = weight_trig_up + '* PrefireWeight'
            weight_trig_down = weight_trig_down + '* PrefireWeight'
            weight_pu_up = weight_pu_up + '* PrefireWeight'
            weight_pu_down = weight_pu_down + '* PrefireWeight'
            weight_tt_up = weight_tt_up + '* PrefireWeight'
            weight_tt_down = weight_tt_down + '* PrefireWeight'
            weight_dy_up = weight_dy_up + '* PrefireWeight'
            weight_dy_down = weight_dy_down + '* PrefireWeight'
            weight_dy_1b_up = weight_dy_1b_up + '* PrefireWeight'
            weight_dy_1b_down = weight_dy_1b_down + '* PrefireWeight'
            weight_dy_2b_up = weight_dy_2b_up + '* PrefireWeight'
            weight_dy_2b_down = weight_dy_2b_down + '* PrefireWeight'
            weight_dy_xsecup = weight_dy_xsecup + '* PrefireWeight'
            weight_dy_xsecdown = weight_dy_xsecdown + '* PrefireWeight'
            weight_dy_1b_xsecup = weight_dy_1b_xsecup + '* PrefireWeight'
            weight_dy_1b_xsecdown = weight_dy_1b_xsecdown + '* PrefireWeight'
            weight_dy_2b_xsecup = weight_dy_2b_xsecup + '* PrefireWeight'
            weight_dy_2b_xsecdown = weight_dy_2b_xsecdown + '* PrefireWeight'
            weight_fake_m_up = weight_fake_m_up +'* PrefireWeight'
            weight_fake_m_down = weight_fake_m_down +'* PrefireWeight'
            weight_fake_e_up = weight_fake_e_up +'* PrefireWeight'
            weight_fake_e_down = weight_fake_e_down +'* PrefireWeight'
            weight_notauidvsjet = weight_notauidvsjet +'* PrefireWeight'
        if sysvar=="":
            hists[dirname][sample] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight)            
            hists[dirname][sample + '_AR']= Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection_ar, wt=weight_ar)
            hists[dirname][sample + '_Hcut'] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection+" && (H_mass < 100. || H_mass > 140.)", wt=weight)
            hists[dirname][sample + '_AR_Hcut'] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection_ar+" && (H_mass < 100. || H_mass > 140.)", wt=weight_ar)
            hists[dirname][sample + '_Hsigcut'] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection+" && (H_mass > 100. && H_mass < 140.)", wt=weight)
            hists[dirname][sample + '_AR_Hsigcut'] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection_ar+" && (H_mass > 100. && H_mass < 140.)", wt=weight_ar)
            if isBDT:
                hists[dirname][sample + '_cut'] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection+" && %s<0.4"%var, wt=weight)
                hists[dirname][sample + '_AR_cut'] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection_ar+" && %s<0.4"%var, wt=weight_ar)
                hists[dirname][sample + '_sig'+year] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection+" && BDTSigmax", wt=weight)
                hists[dirname][sample + '_AR_sig'+year] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection+" && BDTSigmax", wt=weight_ar)
                hists[dirname][sample + '_tt'+year] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection+" && BDTTTmax", wt=weight)
                hists[dirname][sample + '_AR_tt'+year] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection_ar+" && BDTTTmax", wt=weight_ar)
                hists[dirname][sample + '_dy'+year] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection+" && BDTDYmax", wt=weight)
                hists[dirname][sample + '_AR_dy'+year] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection_ar+" && BDTDYmax", wt=weight_ar)
                hists[dirname][sample + '_ff%sUp'%year] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight) #weight is the same as normal
                hists[dirname][sample + '_ff%sDown'%year] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight) #weight is the same as normal
                hists[dirname][sample + '_AR_ff%sUp'%year] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection_ar, wt=weight_ar_up)
                hists[dirname][sample + '_AR_ff%sDown'%year] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection_ar, wt=weight_ar_down)
                if year in ["2017","2016"]:
                    hists[dirname][sample + '_AR_prefiring%sUp'%year] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection_ar, wt=weight_ar+' * PrefireWeight_up')
                    hists[dirname][sample + '_AR_prefiring%sDown'%year] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection_ar, wt=weight_ar+' * PrefireWeight_down')
                for ffvar in ff_variations:
                    ffvar_name = ffvar[7:]
                    hists[dirname][sample + '_'+ffvar] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight) #weight is the same as normal
                    hists[dirname][sample + '_AR_'+ffvar] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection_ar, wt=weight+'* wt_ff_'+ffvar_name)
                if sample!="data_obs":  #following uncertainties only for MC
                    for btag_var in btag_variations:
                        if year=="2016" and preVFP!="_comb":
                            if preVFP=="_preVFP":
                                if "preVFP" in btag_var:
                                    btag_var_name = btag_var[16:]
                                    hists[dirname][sample + '_'+btag_var] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight_btag+'* BTagWeight_'+btag_var_name)
                                elif "postVFP" in btag_var:
                                    hists[dirname][sample + '_'+btag_var] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight_btag+'* BTagWeight') 
                                else:
                                    btag_var_name = btag_var[9:]
                                    hists[dirname][sample + '_'+btag_var] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight_btag+'* BTagWeight_'+btag_var_name) #uncorrelated
                            else:
                                if "preVFP" in btag_var:
                                    hists[dirname][sample + '_'+btag_var] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight_btag+'* BTagWeight')
                                elif "postVFP" in btag_var:
                                    btag_var_name = btag_var[17:]
                                    hists[dirname][sample + '_'+btag_var] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight_btag+'* BTagWeight_'+btag_var_name)
                                else:
                                    btag_var_name = btag_var[9:]
                                    hists[dirname][sample + '_'+btag_var] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight_btag+'* BTagWeight_'+btag_var_name) #uncorrelated
                        else:
                            btag_var_name = btag_var[9:]
                            hists[dirname][sample + '_'+btag_var] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight_btag+'* BTagWeight_'+btag_var_name)
                    for taudm in ['1prong','1prong1pi','3prong']:
                        tauid_var = 'CMS_eff_t_%s_%s'%(taudm,year)
                        hists[dirname][sample + '_'+tauid_var+"Up"] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight_notauidvsjet+' * TauWeightVSjet_%s_up'%taudm)
                        hists[dirname][sample + '_'+tauid_var+"Down"] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight_notauidvsjet+' * TauWeightVSjet_%s_down'%taudm)
                    hists[dirname][sample + '_eff_trig_%s_%sUp'%(channel_sys,year)] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight_trig_up)
                    hists[dirname][sample + '_eff_trig_%s_%sDown'%(channel_sys,year)] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight_trig_down)
                    hists[dirname][sample + '_pu_%sUp'%year] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight_pu_up)
                    hists[dirname][sample + '_pu_%sDown'%year] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight_pu_down)
                    hists[dirname][sample + '_ttbarShapeUp'] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight_tt_up)
                    hists[dirname][sample + '_ttbarShapeDown'] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight_tt_down)
                    hists[dirname][sample + '_dyShapeUp'] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight_dy_up)
                    hists[dirname][sample + '_dyShapeDown'] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight_dy_down)
                    hists[dirname][sample + '_dyShape1bUp'] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight_dy_1b_up)
                    hists[dirname][sample + '_dyShape1bDown'] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight_dy_1b_down)
                    hists[dirname][sample + '_dyShape2bUp'] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight_dy_2b_up)
                    hists[dirname][sample + '_dyShape2bDown'] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight_dy_2b_down)
                    hists[dirname][sample + '_dyxsecUp'] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight_dy_xsecup)
                    hists[dirname][sample + '_dyxsecDown'] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight_dy_xsecdown)
                    hists[dirname][sample + '_dyxsec1bUp'] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight_dy_1b_xsecup)
                    hists[dirname][sample + '_dyxsec1bDown'] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight_dy_1b_xsecdown)
                    hists[dirname][sample + '_dyxsec2bUp'] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight_dy_2b_xsecup)
                    hists[dirname][sample + '_dyxsec2bDown'] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight_dy_2b_xsecdown)
                    hists[dirname][sample + '_fake_m_%sUp'%year] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight_fake_m_up)
                    hists[dirname][sample + '_fake_m_%sDown'%year] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight_fake_m_down)
                    hists[dirname][sample + '_fake_e_%sUp'%year] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight_fake_e_up)
                    hists[dirname][sample + '_fake_e_%sDown'%year] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight_fake_e_down)
                    hists[dirname][sample + '_QCDscaleUp'] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight+' * LHEScaleWeightUp')      
                    hists[dirname][sample + '_QCDscaleDown'] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight+' * LHEScaleWeightDown')
                    hists[dirname][sample + '_QCDscaleMURUp'] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight+' * LHEScaleWeightMURUp')            
                    hists[dirname][sample + '_QCDscaleMURDown'] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight+' * LHEScaleWeightMURDown')
                    hists[dirname][sample + '_QCDscaleMUFUp'] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight+' * LHEScaleWeightMUFUp')            
                    hists[dirname][sample + '_QCDscaleMUFDown'] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight+' * LHEScaleWeightMUFDown')
                    hists[dirname][sample + '_QCDscaleMURSigUp'] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight+' * LHEScaleWeightMURUp')            
                    hists[dirname][sample + '_QCDscaleMURSigDown'] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight+' * LHEScaleWeightMURDown')
                    hists[dirname][sample + '_QCDscaleMUFSigUp'] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight+' * LHEScaleWeightMUFUp')            
                    hists[dirname][sample + '_QCDscaleMUFSigDown'] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight+' * LHEScaleWeightMUFDown')
                    hists[dirname][sample + '_QCDscaleMURTTUp'] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight+' * LHEScaleWeightMURUp')            
                    hists[dirname][sample + '_QCDscaleMURTTDown'] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight+' * LHEScaleWeightMURDown')
                    hists[dirname][sample + '_QCDscaleMUFTTUp'] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight+' * LHEScaleWeightMUFUp')            
                    hists[dirname][sample + '_QCDscaleMUFTTDown'] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight+' * LHEScaleWeightMUFDown')
                    hists[dirname][sample + '_QCDscaleMURDYUp'] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight+' * LHEScaleWeightMURUp')            
                    hists[dirname][sample + '_QCDscaleMURDYDown'] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight+' * LHEScaleWeightMURDown')
                    hists[dirname][sample + '_QCDscaleMUFDYUp'] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight+' * LHEScaleWeightMUFUp')            
                    hists[dirname][sample + '_QCDscaleMUFDYDown'] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight+' * LHEScaleWeightMUFDown')
                    hists[dirname][sample + '_PS_ISRUp'] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight+' * PSWeightISRUp')            
                    hists[dirname][sample + '_PS_ISRDown'] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight+' * PSWeightISRDown')            
                    hists[dirname][sample + '_PS_FSRUp'] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight+' * PSWeightFSRUp')            
                    hists[dirname][sample + '_PS_FSRDown'] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight+' * PSWeightFSRDown') 
                    hists[dirname][sample + '_PS_ISRSigUp'] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight+' * PSWeightISRUp')            
                    hists[dirname][sample + '_PS_ISRSigDown'] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight+' * PSWeightISRDown')            
                    hists[dirname][sample + '_PS_FSRSigUp'] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight+' * PSWeightFSRUp')            
                    hists[dirname][sample + '_PS_FSRSigDown'] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight+' * PSWeightFSRDown')
                    hists[dirname][sample + '_PS_ISRTTUp'] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight+' * PSWeightISRUp')            
                    hists[dirname][sample + '_PS_ISRTTDown'] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight+' * PSWeightISRDown')            
                    hists[dirname][sample + '_PS_FSRTTUp'] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight+' * PSWeightFSRUp')            
                    hists[dirname][sample + '_PS_FSRTTDown'] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight+' * PSWeightFSRDown')
                    hists[dirname][sample + '_PS_ISRDYUp'] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight+' * PSWeightISRUp')            
                    hists[dirname][sample + '_PS_ISRDYDown'] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight+' * PSWeightISRDown')            
                    hists[dirname][sample + '_PS_FSRDYUp'] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight+' * PSWeightFSRUp')            
                    hists[dirname][sample + '_PS_FSRDYDown'] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight+' * PSWeightFSRDown')
                    if year in ["2017","2016"]:
                        hists[dirname][sample + '_prefiring%sUp'%year] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight+' * PrefireWeight_up')
                        hists[dirname][sample + '_prefiring%sDown'%year] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight+' * PrefireWeight_down')
                
                    


        else: #JEC variation not for application region
            if sample!="data_obs":
                hists[dirname][sample+sysvar] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection, wt=weight)


MultiDraw(hists, samplesdir, getsamples(channel,year,preVFP), 'tree', mt_cores=8)

if isBDT and sysvar=="":
    print("channel:",channel)
    if channel=="mutau":
        channel_sys = "mt"
    elif channel=="etau":
        channel_sys = "et"
    else:
        channel_sys = channel
    variations_list = ["","ff%sUp"%year,"ff%sDown"%year,"Hcut","Hsigcut","cut","sig"+year,"tt"+year,"dy"+year,"eff_trig_%s_%sUp"%(channel_sys,year),"eff_trig_%s_%sDown"%(channel_sys,year),"pu_%sUp"%year,"pu_%sDown"%year,"ttbarShapeUp","ttbarShapeDown","dyShapeUp","dyShapeDown","dyShape1bUp","dyShape1bDown","dyShape2bUp","dyShape2bDown","dyxsecUp","dyxsecDown","dyxsec1bUp","dyxsec1bDown","dyxsec2bUp","dyxsec2bDown","fake_m_%sUp"%year,"fake_m_%sDown"%year,"fake_e_%sUp"%year,"fake_e_%sDown"%year,"QCDscaleUp","QCDscaleDown","QCDscaleMURUp","QCDscaleMURDown","QCDscaleMUFUp","QCDscaleMUFDown","QCDscaleMURSigUp","QCDscaleMURSigDown","QCDscaleMUFSigUp","QCDscaleMUFSigDown","QCDscaleMURTTUp","QCDscaleMURTTDown","QCDscaleMUFTTUp","QCDscaleMUFTTDown","QCDscaleMURDYUp","QCDscaleMURDYDown","QCDscaleMUFDYUp","QCDscaleMUFDYDown","PS_ISRUp","PS_ISRDown","PS_FSRUp","PS_FSRDown","PS_ISRSigUp","PS_ISRSigDown","PS_FSRSigUp","PS_FSRSigDown","PS_ISRTTUp","PS_ISRTTDown","PS_FSRTTUp","PS_FSRTTDown","PS_ISRDYUp","PS_ISRDYDown","PS_FSRDYUp","PS_FSRDYDown"]+ff_variations+btag_variations+tauid_variations
    if year in ["2017","2016"]:
        variations_list = variations_list + ["prefiring%sUp"%year,"prefiring%sDown"%year]
elif sysvar!="":
    variations_list = [""]
else:
    variations_list = ["","Hcut","Hsigcut"]
        

# Loop through all nodes (just the ones containing TH1s)
for path, node in hists.ListNodes(withObjects=True):
    print('>> %s' % path)
    
    for variation in variations_list:
        if variation!="":
            variation = "_"+variation
        node['ggH_bb_htt%s%s'%(sysvar,variation)] = node['ggH_bb_htt_inc%s%s'%(sysvar,variation)] + node['ggH_bb_htt_excl%s%s'%(sysvar,variation)]
        node['ggH_htt%s%s'%(sysvar,variation)] = node['ggH_htt_inc%s%s'%(sysvar,variation)] + node['ggH_htt_excl%s%s'%(sysvar,variation)]
        node['bbHtt%s%s'%(sysvar,variation)] = node['bbH_htt%s%s'%(sysvar,variation)] + node['ggH_bb_htt_inc%s%s'%(sysvar,variation)] + node['ggH_bb_htt_excl%s%s'%(sysvar,variation)] - node['intH_bb_htt%s%s'%(sysvar,variation)]
        node['jjHtt%s%s'%(sysvar,variation)] = node['bbH_nobb_htt%s%s'%(sysvar,variation)] + node['ggH_htt_inc%s%s'%(sysvar,variation)] + node['ggH_htt_excl%s%s'%(sysvar,variation)] - node['intH_htt%s%s'%(sysvar,variation)]
        node['ST%s%s'%(sysvar,variation)] = node['ST_t_channel_antitop%s%s'%(sysvar,variation)] + node['ST_t_channel_top%s%s'%(sysvar,variation)] + node['ST_s_channel%s%s'%(sysvar,variation)] + node['ST_tW_antitop%s%s'%(sysvar,variation)] + node['ST_tW_top%s%s'%(sysvar,variation)]
        node['TT%s%s'%(sysvar,variation)] = node['TTTo2L2Nu%s%s'%(sysvar,variation)] + node['TTToHadronic%s%s'%(sysvar,variation)] + node['TTToSemiLeptonic%s%s'%(sysvar,variation)]
        node['WH%s%s'%(sysvar,variation)] = node['WplusH%s%s'%(sysvar,variation)] + node['WminusH%s%s'%(sysvar,variation)]
        node['VV%s%s'%(sysvar,variation)] = node['WWTo2L2Nu%s%s'%(sysvar,variation)] + node['WWTo1L1Nu2Q%s%s'%(sysvar,variation)] + node['WWTo4Q%s%s'%(sysvar,variation)] + node['WZTo2L2Q%s%s'%(sysvar,variation)] + node['WZTo3LNu%s%s'%(sysvar,variation)] + node['WZTo1L3Nu%s%s'%(sysvar,variation)] + node['WZTo1L1Nu2Q%s%s'%(sysvar,variation)] + node['ZZTo4L%s%s'%(sysvar,variation)] + node['ZZTo2Nu2Q%s%s'%(sysvar,variation)] + node['ZZTo2L2Q%s%s'%(sysvar,variation)]
        node['DYJets%s%s'%(sysvar,variation)] = node['DYJets_incl%s%s'%(sysvar,variation)] + node['DYJets_0J%s%s'%(sysvar,variation)] + node['DYJets_1J%s%s'%(sysvar,variation)] + node['DYJets_2J%s%s'%(sysvar,variation)] #NLO
        node['WJets%s%s'%(sysvar,variation)] = node['WJets_incl%s%s'%(sysvar,variation)] + node['WJets_0J%s%s'%(sysvar,variation)] + node['WJets_1J%s%s'%(sysvar,variation)] + node['WJets_2J%s%s'%(sysvar,variation)] #NLO
    if sysvar!="": continue #no AR for JEC variations
    ######### application region  ######
    if isBDT:
        variations_list_AR = ["","ff%sUp"%year,"ff%sDown"%year,"Hcut","Hsigcut","cut","sig"+year,"tt"+year,"dy"+year]+ff_variations
        if year in ["2017","2016"]:
            variations_list_AR = variations_list_AR + ["prefiring%sUp"%year,"prefiring%sDown"%year]
    else:
        variations_list_AR = ["","Hcut","Hsigcut"]
    for variation in variations_list_AR:
        if variation!="":
            variation = "_"+variation
        node['jjHtt_AR%s'%variation] = node['bbH_nobb_htt_AR%s'%variation] + node['ggH_htt_inc_AR%s'%variation] + node['ggH_htt_excl_AR%s'%variation] - node['intH_htt_AR%s'%variation]
        node['ST_AR%s'%variation] = node['ST_t_channel_antitop_AR%s'%variation] + node['ST_t_channel_top_AR%s'%variation] + node['ST_s_channel_AR%s'%variation] + node['ST_tW_antitop_AR%s'%variation] + node['ST_tW_top_AR%s'%variation]
        node['TT_AR%s'%variation] = node['TTTo2L2Nu_AR%s'%variation] + node['TTToHadronic_AR%s'%variation] + node['TTToSemiLeptonic_AR%s'%variation]
        node['WH_AR%s'%variation] = node['WplusH_AR%s'%variation] + node['WminusH_AR%s'%variation]
        node['VV_AR%s'%variation] = node['WWTo2L2Nu_AR%s'%variation] + node['WWTo1L1Nu2Q_AR%s'%variation] + node['WWTo4Q_AR%s'%variation] + node['WZTo3LNu_AR%s'%variation] + node['WZTo2L2Q_AR%s'%variation] + node['WZTo1L3Nu_AR%s'%variation] + node['WZTo1L1Nu2Q_AR%s'%variation] + node['ZZTo4L_AR%s'%variation] + node['ZZTo2L2Q_AR%s'%variation] + node['ZZTo2Nu2Q_AR%s'%variation]
        node['DYJets_AR%s'%variation] = node['DYJets_incl_AR%s'%variation] + node['DYJets_0J_AR%s'%variation] + node['DYJets_1J_AR%s'%variation] + node['DYJets_2J_AR%s'%variation] #NLO
        node['WJets_AR%s'%variation] = node['WJets_incl_AR%s'%variation] + node['WJets_0J_AR%s'%variation] + node['WJets_1J_AR%s'%variation] + node['WJets_2J_AR%s'%variation] #NLO
        node['MC_AR%s'%variation] = node['DYJets_AR%s'%variation] + node['WJets_AR%s'%variation] + node['TT_AR%s'%variation] + node['ST_AR%s'%variation] + node['VBF_AR%s'%variation] + node['ZH_AR%s'%variation] + node['WH_AR%s'%variation] + node['VV_AR%s'%variation] + node['ttH_AR%s'%variation] + node['jjHtt_AR%s'%variation]
        node['QCD%s'%variation] = node['data_obs_AR%s'%variation]-node['MC_AR%s'%variation]
        #### summing all bkg including QCD ####
        if "ff" in variation: #for fakefactor up and down only QCD changes
            node['MC%s'%variation] = node['DYJets'] + node['WJets'] + node['TT'] + node['ST'] + node['QCD%s'%variation] + node['VV'] + node['VBF'] + node['ZH'] + node['WH'] + node['ttH'] + node['jjHtt']
        else:
            node['MC%s'%variation] = node['DYJets%s'%variation] + node['WJets%s'%variation] + node['TT%s'%variation] + node['ST%s'%variation] + node['QCD%s'%variation] + node['VV%s'%variation] + node['VBF%s'%variation] + node['ZH%s'%variation] + node['WH%s'%variation] + node['ttH%s'%variation] + node['jjHtt%s'%variation]
                
if isBDT:
    if year=="2016" and preVFP=="":
        filename = './root/%s_UL%s%s%s_BDT.root'%(channel,year,"postVFP",sysvar_noyear)
    else:
        filename = './root/%s_UL%s%s%s_BDT.root'%(channel,year,preVFP,sysvar_noyear)
else:
    if year=="2016" and preVFP=="":
        filename = './root/%s_UL%s%s%s.root'%(channel,year,"postVFP",sysvar_noyear)
    else:
        filename = './root/%s_UL%s%s%s.root'%(channel,year,preVFP,sysvar_noyear)
    
 
fout = ROOT.TFile(filename, 'RECREATE')
NodeToTDir(fout, hists)
fout.Close()


if isBDT:
    if sysvar_noyear == "":
        sysvar_noyear = "_nominal"
    if channel=="mutau":
        if year=="2016" and sysvar_noyear=="_nominal":
            if preVFP=="_preVFP":
                filename_limit = './root/htt_mt_bbH_nominal.Run2016_preVFP.root'
                copyfile_to = '/work/pbaertsc/bbh/CMSSW_10_2_13/src/CombineHarvester/bbHRun2Legacy/shapes/htt_mt_bbH_nominal.Run2016_preVFP.root'
            elif preVFP!="_comb":
                filename_limit = './root/htt_mt_bbH_nominal.Run2016_postVFP.root'
                copyfile_to = '/work/pbaertsc/bbh/CMSSW_10_2_13/src/CombineHarvester/bbHRun2Legacy/shapes/htt_mt_bbH_nominal.Run2016_postVFP.root'
        else:
            filename_limit = './root/htt_mt_bbH%s.Run%s.root'%(sysvar_noyear,year)
            copyfile_to = '/work/pbaertsc/bbh/CMSSW_10_2_13/src/CombineHarvester/bbHRun2Legacy/shapes/htt_mt_bbH%s_jjh.Run%s.root'%(sysvar_noyear,year)
    elif channel=="etau":
        if year=="2016" and sysvar_noyear=="_nominal":
            if preVFP=="_preVFP":
                filename_limit = './root/htt_et_bbH_nominal.Run2016_preVFP.root'
                copyfile_to = '/work/pbaertsc/bbh/CMSSW_10_2_13/src/CombineHarvester/bbHRun2Legacy/shapes/htt_et_bbH_nominal.Run2016_preVFP.root'
            elif preVFP!="_comb":
                filename_limit = './root/htt_et_bbH_nominal.Run2016_postVFP.root'
                copyfile_to = '/work/pbaertsc/bbh/CMSSW_10_2_13/src/CombineHarvester/bbHRun2Legacy/shapes/htt_et_bbH_nominal.Run2016_postVFP.root'
        else:
            filename_limit = './root/htt_et_bbH%s.Run%s.root'%(sysvar_noyear,year)
            copyfile_to = '/work/pbaertsc/bbh/CMSSW_10_2_13/src/CombineHarvester/bbHRun2Legacy/shapes/htt_et_bbH%s_jjh.Run%s.root'%(sysvar_noyear,year)
    fout_limit = ROOT.TFile(filename_limit, 'RECREATE')
    NodeToTDir(fout_limit, hists)
    fout_limit.Close()
    #os.system(hadd_rootfiles)
    """
    if sysvar=="":
        shutil.copyfile(filename_limit,copyfile_to)
        #shutil.copyfile(filename_limit_comb,copyfile_to_comb)
    """

