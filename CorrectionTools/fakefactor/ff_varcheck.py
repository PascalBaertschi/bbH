import ROOT
from analysis import *
from argparse import ArgumentParser
import json
import utils
import sys
sys.path.insert(1, os.path.join(sys.path[0], '../..')) #to get file in parent directory
from xsections import xsection
from samplenames import getsamples

# import CombineHarvester.CombineTools.plotting as plot

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.TH1.AddDirectory(False)

parser = ArgumentParser()
parser.add_argument('-y', '--year',    dest='year', type=str, default='2018', action='store')
parser.add_argument('-c', '--channel', dest='channel', choices=['mutau','etau'], type=str, default='mutau', action='store',)
parser.add_argument('-p', '--preVFP',  dest='preVFP', action='store_const', const="_preVFP",default="")
parser.add_argument('-t', '--comb',  dest='UL2016comb', action='store_true',default=False)
args = parser.parse_args()

year = args.year
channel = args.channel
preVFP = args.preVFP
UL2016comb = args.UL2016comb
#LUMI        = 137190.

if year=='2016': #needed to make sure that preVFP+postVFP are used
    preVFP="_comb"
           

if channel=="mutau":
    selections_DR = [
        {'name':'DR_QCD',
         'selection':'isHtoMuTau && Mu1_charge*Tau1_charge==1 && dimuon_veto==0 && electron_veto==0 && extra_muon_veto==0 && mt < 60 && nBjets_m>0'},
        {'name':'DR_QCD_AR',
         'selection':'isHtoMuTauAR && dimuon_veto==0 && electron_veto==0 && extra_muon_veto==0 && Mu1_charge*Tau1_charge==1 && mt < 60 && nBjets_m>0'},
        {'name':'DR_W',
         'selection':'isHtoMuTau && dimuon_veto==0 && electron_veto==0 && extra_muon_veto==0 && Mu1_charge*Tau1_charge==-1 && mt > 80 && nBjets_m==0'},
        {'name':'DR_W_AR',
         'selection':'isHtoMuTauAR && dimuon_veto==0 && electron_veto==0 && extra_muon_veto==0 && Mu1_charge*Tau1_charge==-1 && mt > 80 && nBjets_m==0'},
        {'name' : 'DR_TT',
         'selection':'isHtoMuTau && dimuon_veto==0 && electron_veto==0 && extra_muon_veto==0 && Mu1_charge*Tau1_charge==-1 && mt > 70 && mt < 90 && nBjets_m>0'},
        {'name':'DR_TT_AR',
         'selection':'isHtoMuTauAR && dimuon_veto==0 && electron_veto==0 && extra_muon_veto==0 && Mu1_charge*Tau1_charge==-1 && mt > 70 && mt < 90 && nBjets_m>0'},
    ]

elif channel=="etau":
    selections_DR = [
        {'name':'DR_QCD',
         'selection':'isHtoETau && Ele1_charge*Tau1_charge==1 && dielectron_veto==0 && muon_veto==0 && extra_electron_veto==0 && mt < 60 && nBjets_m>0'},
        {'name':'DR_QCD_AR',
         'selection':'isHtoETauAR && dielectron_veto==0 && muon_veto==0 && extra_electron_veto==0 && Ele1_charge*Tau1_charge==1 && mt < 60 && nBjets_m>0'},
        {'name':'DR_W',
         'selection':'isHtoETau && dielectron_veto==0 && muon_veto==0 && extra_electron_veto==0 && Ele1_charge*Tau1_charge==-1 && mt > 80 && nBjets_m==0'},
        {'name':'DR_W_AR',
         'selection':'isHtoETauAR && dielectron_veto==0 && muon_veto==0 && extra_electron_veto==0 && Ele1_charge*Tau1_charge==-1 && mt > 80 && nBjets_m==0'},
        {'name' : 'DR_TT',
         'selection':'isHtoETau && dielectron_veto==0 && muon_veto==0 && extra_electron_veto==0 && Ele1_charge*Tau1_charge==-1 && mt > 70 && mt < 90 && nBjets_m>0'},
        {'name':'DR_TT_AR',
         'selection':'isHtoETauAR && dielectron_veto==0 && muon_veto==0 && extra_electron_veto==0 && Ele1_charge*Tau1_charge==-1 && mt > 70 && mt < 90 && nBjets_m>0'},
  
        ]


selections_prong = [
    {'name':'1prong',
     'selection':'&& (Tau1_decaymode==0 || Tau1_decaymode==1 || Tau1_decaymode==2)'},
    {'name':'3prong',
     'selection':'&& (Tau1_decaymode==10 || Tau1_decaymode==11)'}]


def drawPlots(hists,year,channel,preVFP):
    mutau_wts = 'EventWeight * LumiWeight * BTagWeight * PUIdWeight * MuWeight * MuTriggerWeight * TauWeight  * wt_tt_pt * wt_tt * wt_dy * wt_w * wt_dy_nlo * wt_w_nlo'
    etau_wts = 'EventWeight * LumiWeight * BTagWeight * PUIdWeight * EWeight * ETriggerWeight * TauWeight  * wt_tt_pt * wt_tt * wt_dy * wt_w * wt_dy_nlo * wt_w_nlo'
    if year=='2016':
        preVFP="_comb"
    files = ["data_obs","DYJets_incl","DYJets_0J","DYJets_1J","DYJets_2J","WJets_incl","WJets_0J","WJets_1J","WJets_2J","TTTo2L2Nu","TTToHadronic","TTToSemiLeptonic","ST_t_channel_antitop","ST_t_channel_top","ST_s_channel","ST_tW_antitop","ST_tW_top"]
    for sample in files:
        samplesdir = '/pnfs/psi.ch/cms/trivcat/store/user/pbaertsc/bbh/samples_UL%s%s/'%(year,preVFP)
        #samplesdir = '/pnfs/psi.ch/cms/trivcat/store/user/pbaertsc/bbh/ffvarcorr/samples_UL%s%s/'%(year,preVFP)
        for selection_DR in selections_DR:
            if 'QCD' in selection_DR['name']:
                if channel=="mutau":
                    tau_pt_binning = [30.,40.,50.,60.,70.,80.,130.]
                    h_mass_binning = [0.,80.,120.,160.,200.,300.]
                    jet_pt_binning = [20.,40.,60.,80.,200.]
                    collinear_mass_binning = [0.,120.,160.,200.,250.,300.]
                    tauj_mass_binning = [0.,80.,120.,160.,200.,300.]
                elif channel=="etau":
                    tau_pt_binning = [30.,40.,50.,130.]
                    h_mass_binning = [0.,120.,300.]
                    jet_pt_binning = [20.,50.,200.]
                    collinear_mass_binning = [0.,120.,200.,300.]
                    tauj_mass_binning = [0.,120.,300.]
            else:
                tau_pt_binning = [30.,40.,50.,60.,70.,80.,100.,130.]
                h_mass_binning = [0.,40.,80.,120.,160.,200.,250.,300.]  
                jet_pt_binning = [20.,40.,60.,80.,110.,140.,200.]
                collinear_mass_binning = [0.,40.,80.,120.,160.,200.,250.,300.]
                tauj_mass_binning = [0.,40.,80.,120.,160.,200.,250.,300.]
            if selection_DR["name"]=="DR_QCD_AR":
                if sample=='data_obs':
                    weight = 'wt_ff_qcd * wt_ffcorr_hmass_qcd * wt_ffcorr_jetpt_qcd * wt_ffcorr_collinearmass_qcd * wt_ffcorr_taujmass_qcd'
                    weight_hmass = 'wt_ff_qcd'
                    weight_jetpt = 'wt_ff_qcd * wt_ffcorr_hmass_qcd'
                    weight_collinearmass = 'wt_ff_qcd * wt_ffcorr_hmass_qcd * wt_ffcorr_jetpt_qcd'
                    weight_taujmass = 'wt_ff_qcd * wt_ffcorr_hmass_qcd * wt_ffcorr_jetpt_qcd * wt_ffcorr_collinearmass_qcd'
                    weight_hpt = 'wt_ff_qcd * wt_ffcorr_hmass_qcd * wt_ffcorr_jetpt_qcd * wt_ffcorr_collinearmass_qcd * wt_ffcorr_taujmass_qcd'
                    #weight = 'wt_ff_qcd * wt_ffvarcorr_hmass_qcd * wt_ffvarcorr_jetpt_qcd * wt_ffvarcorr_collinearmass_qcd * wt_ffvarcorr_taujmass_qcd'
                    #weight_hmass = 'wt_ff_qcd'
                    #weight_jetpt = 'wt_ff_qcd * wt_ffvarcorr_hmass_qcd'
                    #weight_collinearmass = 'wt_ff_qcd * wt_ffvarcorr_hmass_qcd * wt_ffvarcorr_jetpt_qcd'
                    #weight_taujmass = 'wt_ff_qcd * wt_ffvarcorr_hmass_qcd * wt_ffvarcorr_jetpt_qcd * wt_ffvarcorr_collinearmass_qcd'
                    #weight_hpt = 'wt_ff_qcd * wt_ffvarcorr_hmass_qcd * wt_ffvarcorr_jetpt_qcd * wt_ffvarcorr_collinearmass_qcd * wt_ffvarcorr_taujmass_qcd'
                else:
                    if channel=="mutau":
                        weight = mutau_wts+' * wt_ff_qcd * wt_ffcorr_hmass_qcd * wt_ffcorr_jetpt_qcd * wt_ffcorr_collinearmass_qcd * wt_ffcorr_taujmass_qcd'
                        weight_hmass = mutau_wts+' * wt_ff_qcd'
                        weight_jetpt = mutau_wts+' * wt_ff_qcd * wt_ffcorr_hmass_qcd'
                        weight_collinearmass = mutau_wts+' * wt_ff_qcd * wt_ffcorr_hmass_qcd * wt_ffcorr_jetpt_qcd'
                        weight_taujmass = mutau_wts+' * wt_ff_qcd * wt_ffcorr_hmass_qcd * wt_ffcorr_jetpt_qcd * wt_ffcorr_collinearmass_qcd'
                        weight_hpt = mutau_wts+' * wt_ff_qcd * wt_ffcorr_hmass_qcd * wt_ffcorr_jetpt_qcd * wt_ffcorr_collinearmass_qcd * wt_ffcorr_taujmass_qcd'
                        #weight = mutau_wts+' * wt_ff_qcd * wt_ffvarcorr_hmass_qcd * wt_ffvarcorr_jetpt_qcd * wt_ffvarcorr_collinearmass_qcd * wt_ffvarcorr_taujmass_qcd'
                        #weight_hmass = mutau_wts+' * wt_ff_qcd'
                        #weight_jetpt = mutau_wts+' * wt_ff_qcd * wt_ffvarcorr_hmass_qcd'
                        #weight_collinearmass = mutau_wts+' * wt_ff_qcd * wt_ffvarcorr_hmass_qcd * wt_ffvarcorr_jetpt_qcd'
                        #weight_taujmass = mutau_wts+' * wt_ff_qcd * wt_ffvarcorr_hmass_qcd * wt_ffvarcorr_jetpt_qcd * wt_ffvarcorr_collinearmass_qcd'
                        #weight_hpt = mutau_wts+' * wt_ff_qcd * wt_ffvarcorr_hmass_qcd * wt_ffvarcorr_jetpt_qcd * wt_ffvarcorr_collinearmass_qcd * wt_ffvarcorr_taujmass_qcd'    
            
                    elif channel=="etau":
                        weight = etau_wts+' * wt_ff_qcd * wt_ffcorr_hmass_qcd * wt_ffcorr_jetpt_qcd * wt_ffcorr_collinearmass_qcd * wt_ffcorr_taujmass_qcd'
                        weight_hmass = etau_wts+' * wt_ff_qcd'
                        weight_jetpt = etau_wts+' * wt_ff_qcd * wt_ffcorr_hmass_qcd'
                        weight_collinearmass = etau_wts+' * wt_ff_qcd * wt_ffcorr_hmass_qcd * wt_ffcorr_jetpt_qcd'
                        weight_taujmass = etau_wts+' * wt_ff_qcd * wt_ffcorr_hmass_qcd * wt_ffcorr_jetpt_qcd * wt_ffcorr_collinearmass_qcd'
                        weight_hpt = etau_wts+' * wt_ff_qcd * wt_ffcorr_hmass_qcd * wt_ffcorr_jetpt_qcd * wt_ffcorr_taujmass_qcd * wt_ffcorr_taujmass_qcd'
                        #weight = etau_wts+' * wt_ff_qcd * wt_ffvarcorr_hmass_qcd * wt_ffvarcorr_jetpt_qcd * wt_ffvarcorr_collinearmass_qcd * wt_ffvarcorr_taujmass_qcd'
                        #weight_hmass = etau_wts+' * wt_ff_qcd'
                        #weight_jetpt = etau_wts+' * wt_ff_qcd * wt_ffvarcorr_hmass_qcd'
                        #weight_collinearmass = etau_wts+' * wt_ff_qcd * wt_ffvarcorr_hmass_qcd * wt_ffvarcorr_jetpt_qcd'
                        #weight_taujmass = etau_wts+' * wt_ff_qcd * wt_ffvarcorr_hmass_qcd * wt_ffvarcorr_jetpt_qcd * wt_ffvarcorr_collinearmass_qcd'
                        #weight_hpt = etau_wts+' * wt_ff_qcd * wt_ffvarcorr_hmass_qcd * wt_ffvarcorr_jetpt_qcd * wt_ffvarcorr_collinearmass_qcd * wt_ffvarcorr_taujmass_qcd'

            elif selection_DR["name"]=="DR_W_AR": #don't apply corrections for DR W fakefactors
                if sample=='data_obs':
                    weight = 'wt_ff_w'
                else:
                    if channel=="mutau":
                        weight = mutau_wts+' * wt_ff_w'
                    elif channel=="etau":
                        weight = etau_wts+' * wt_ff_w'
                weight_hmass = weight
                weight_jetpt = weight
                weight_collinearmass = weight
                weight_taujmass = weight
                weight_hpt = weight
            elif selection_DR["name"]=="DR_TT_AR":
                if sample=='data_obs':
                    weight = 'wt_ff_tt * wt_ffcorr_hmass_tt * wt_ffcorr_jetpt_tt * wt_ffcorr_collinearmass_tt * wt_ffcorr_taujmass_tt'
                    weight_hmass = 'wt_ff_tt'
                    weight_jetpt =  'wt_ff_tt * wt_ffcorr_hmass_tt'
                    weight_collinearmass = 'wt_ff_tt * wt_ffcorr_hmass_tt * wt_ffcorr_jetpt_tt'
                    weight_taujmass = 'wt_ff_tt * wt_ffcorr_hmass_tt * wt_ffcorr_jetpt_tt * wt_ffcorr_collinearmass_tt'
                    weight_hpt = 'wt_ff_tt * wt_ffcorr_hmass_tt * wt_ffcorr_jetpt_tt * wt_ffcorr_collinearmass_tt * wt_ffcorr_taujmass_tt'
                    #weight = 'wt_ff_tt * wt_ffvarcorr_hmass_tt * wt_ffvarcorr_jetpt_tt * wt_ffvarcorr_collinearmass_tt * wt_ffvarcorr_taujmass_tt'
                    #weight_hmass = 'wt_ff_tt'
                    #weight_jetpt =  'wt_ff_tt * wt_ffvarcorr_hmass_tt'
                    #weight_collinearmass = 'wt_ff_tt * wt_ffvarcorr_hmass_tt * wt_ffvarcorr_jetpt_tt'
                    #weight_taujmass = 'wt_ff_tt * wt_ffvarcorr_hmass_tt * wt_ffvarcorr_jetpt_tt * wt_ffvarcorr_collinearmass_tt'
                    #weight_hpt = 'wt_ff_tt * wt_ffvarcorr_hmass_tt * wt_ffvarcorr_jetpt_tt * wt_ffvarcorr_collinearmass_tt * wt_ffvarcorr_taujmass_tt'
                else:
                    if channel=="mutau":
                        weight = mutau_wts+' * wt_ff_tt * wt_ffcorr_hmass_tt * wt_ffcorr_jetpt_tt * wt_ffcorr_collinearmass_tt * wt_ffcorr_taujmass_tt'
                        weight_hmass = mutau_wts+'* wt_ff_tt'
                        weight_jetpt =  mutau_wts+'* wt_ff_tt * wt_ffcorr_hmass_tt'
                        weight_collinearmass = mutau_wts+'* wt_ff_tt * wt_ffcorr_hmass_tt * wt_ffcorr_jetpt_tt'
                        weight_taujmass = mutau_wts+'* wt_ff_tt * wt_ffcorr_hmass_tt * wt_ffcorr_jetpt_tt * wt_ffcorr_collinearmass_tt'
                        weight_hpt = mutau_wts+'* wt_ff_tt * wt_ffcorr_hmass_tt * wt_ffcorr_jetpt_tt * wt_ffcorr_collinearmass_tt * wt_ffcorr_taujmass_tt'
                        #weight = mutau_wts+' * wt_ff_tt * wt_ffvarcorr_hmass_tt * wt_ffvarcorr_jetpt_tt * wt_ffvarcorr_collinearmass_tt * wt_ffvarcorr_taujmass_tt'
                        #weight_hmass = mutau_wts+'* wt_ff_tt'
                        #weight_jetpt =  mutau_wts+'* wt_ff_tt * wt_ffvarcorr_hmass_tt'
                        #weight_collinearmass = mutau_wts+'* wt_ff_tt * wt_ffvarcorr_hmass_tt * wt_ffvarcorr_jetpt_tt'
                        #weight_taujmass = mutau_wts+'* wt_ff_tt * wt_ffvarcorr_hmass_tt * wt_ffvarcorr_jetpt_tt * wt_ffvarcorr_collinearmass_tt'
                        #weight_hpt = mutau_wts+'* wt_ff_tt * wt_ffvarcorr_hmass_tt * wt_ffvarcorr_jetpt_tt * wt_ffvarcorr_collinearmass_tt * wt_ffvarcorr_taujmass_tt'
                    elif channel=="etau":
                        weight = etau_wts+' * wt_ff_tt * wt_ffcorr_hmass_tt * wt_ffcorr_jetpt_tt * wt_ffcorr_collinearmass_tt * wt_ffcorr_taujmass_tt'
                        weight_hmass = etau_wts+'* wt_ff_tt'
                        weight_jetpt =  etau_wts+'* wt_ff_tt * wt_ffcorr_hmass_tt'
                        weight_collinearmass = etau_wts+'* wt_ff_tt * wt_ffcorr_hmass_tt * wt_ffcorr_jetpt_tt'
                        weight_taujmass = etau_wts+'* wt_ff_tt * wt_ffcorr_hmass_tt * wt_ffcorr_jetpt_tt * wt_ffcorr_collinearmass_tt'
                        weight_hpt = etau_wts+'* wt_ff_tt * wt_ffcorr_hmass_tt * wt_ffcorr_jetpt_tt * wt_ffcorr_collinearmass_tt * wt_ffcorr_taujmass_tt'
                        #weight = etau_wts+' * wt_ff_tt * wt_ffvarcorr_hmass_tt * wt_ffvarcorr_jetpt_tt * wt_ffvarcorr_collinearmass_tt * wt_ffvarcorr_taujmass_tt'
                        #weight_hmass = etau_wts+'* wt_ff_tt'
                        #weight_jetpt =  etau_wts+'* wt_ff_tt * wt_ffvarcorr_hmass_tt'
                        #weight_collinearmass = etau_wts+'* wt_ff_tt * wt_ffvarcorr_hmass_tt * wt_ffvarcorr_jetpt_tt'
                        #weight_taujmass = etau_wts+'* wt_ff_tt * wt_ffvarcorr_hmass_tt * wt_ffvarcorr_jetpt_tt * wt_ffvarcorr_collinearmass_tt'
                        #weight_hpt = etau_wts+'* wt_ff_tt * wt_ffvarcorr_hmass_tt * wt_ffvarcorr_jetpt_tt * wt_ffvarcorr_collinearmass_tt * wt_ffvarcorr_taujmass_tt'
            else:
                if sample=='data_obs':
                    weight = '1.'
                else:
                    if channel=="mutau":
                        weight = mutau_wts
                    elif channel=="etau":
                        weight = etau_wts
                weight_hmass = weight
                weight_jetpt = weight
                weight_collinearmass = weight
                weight_taujmass = weight
                weight_hpt = weight
            
          
            for selection_prongjet in selections_prong:
                selection = selection_DR['selection']+selection_prongjet['selection']
                hists['Tau1_pt'][sample + '_%s_%s'%(selection_DR['name'],selection_prongjet['name'])]= Hist('TH1F', sample=sample, var=['Tau1_pt'], binning=tau_pt_binning, sel=selection, wt=weight)
                hists['H_mass'][sample + '_%s_%s'%(selection_DR['name'],selection_prongjet['name'])]= Hist('TH1F', sample=sample, var=['H_mass'], binning=h_mass_binning, sel=selection, wt=weight_hmass)
                hists['Jet1_pt'][sample + '_%s_%s'%(selection_DR['name'],selection_prongjet['name'])]= Hist('TH1F', sample=sample, var=['Jet1_pt'], binning=jet_pt_binning, sel=selection, wt=weight_jetpt)
                hists['collinear_mass'][sample + '_%s_%s'%(selection_DR['name'],selection_prongjet['name'])]= Hist('TH1F', sample=sample, var=['collinear_mass'], binning=collinear_mass_binning, sel=selection, wt=weight_collinearmass)
                hists['TauJ_mass'][sample + '_%s_%s'%(selection_DR['name'],selection_prongjet['name'])]= Hist('TH1F', sample=sample, var=['TauJ_mass'], binning=tauj_mass_binning, sel=selection, wt=weight_taujmass)
                hists['Jet1_btag'][sample + '_%s_%s'%(selection_DR['name'],selection_prongjet['name'])]= Hist('TH1F', sample=sample, var=['Jet1_btag'], binning=[0.2,0.5,0.8,0.9,1.], sel=selection, wt=weight)
                hists['Dzeta'][sample + '_%s_%s'%(selection_DR['name'],selection_prongjet['name'])]= Hist('TH1F', sample=sample, var=['Dzeta'], binning=[-100.,-70.,-30.,0.,30.,70.,100.], sel=selection, wt=weight)
                hists['DRHJ'][sample + '_%s_%s'%(selection_DR['name'],selection_prongjet['name'])]= Hist('TH1F', sample=sample, var=['DRHJ'], binning=[0.,1.,2.,3.,4.,5.], sel=selection, wt=weight)
                hists['HJ_pt'][sample + '_%s_%s'%(selection_DR['name'],selection_prongjet['name'])]= Hist('TH1F', sample=sample, var=['HJ_pt'], binning=[0.,40.,80.,120.,160.,200.], sel=selection, wt=weight)
                hists['vis_mass'][sample + '_%s_%s'%(selection_DR['name'],selection_prongjet['name'])]= Hist('TH1F', sample=sample, var=['vis_mass'], binning=[0.,40.,80.,120.,160.,200.,250.,300.], sel=selection, wt=weight)
                hists['Jet2_pt'][sample + '_%s_%s'%(selection_DR['name'],selection_prongjet['name'])]= Hist('TH1F', sample=sample, var=['Jet2_pt'], binning=[20.,40.,60.,80.,110.,150.], sel=selection, wt=weight)
                hists['Jet2_btag'][sample + '_%s_%s'%(selection_DR['name'],selection_prongjet['name'])]= Hist('TH1F', sample=sample, var=['Jet2_btag'], binning=[0.,0.1,0.2,0.5,0.8,0.9,1.], sel=selection, wt=weight)
                hists['Mu1_pt'][sample + '_%s_%s'%(selection_DR['name'],selection_prongjet['name'])]= Hist('TH1F', sample=sample, var=['Mu1_pt'], binning=[30,40,50,60,70,80,100,130], sel=selection, wt=weight)
                hists['Ele1_pt'][sample + '_%s_%s'%(selection_DR['name'],selection_prongjet['name'])]= Hist('TH1F', sample=sample, var=['Ele1_pt'], binning=[30,40,50,60,70,80,100,130], sel=selection, wt=weight)
                hists['H_pt'][sample + '_%s_%s'%(selection_DR['name'],selection_prongjet['name'])]= Hist('TH1F', sample=sample, var=['H_pt'], binning=[0.,40.,80.,120.,160.,200.,250.,300.], sel=selection, wt=weight_hpt)
                hists['MET'][sample + '_%s_%s'%(selection_DR['name'],selection_prongjet['name'])]= Hist('TH1F', sample=sample, var=['MET'], binning=[0.,20.,40.,60.,80.,110.,150.,200.], sel=selection, wt=weight_hpt)



                if 'DR_TT' in selection_DR['name'] or 'CR_TT' in selection_DR['name']:
                    hists['Tau1_pt'][sample + '_%s_%s_true'%(selection_DR['name'],selection_prongjet['name'])]= Hist('TH1F', sample=sample, var=['Tau1_pt'], binning=tau_pt_binning, sel=selection+'&& Tau1_genmatch!=6', wt=weight)
                    hists['H_mass'][sample + '_%s_%s_true'%(selection_DR['name'],selection_prongjet['name'])]= Hist('TH1F', sample=sample, var=['H_mass'], binning=h_mass_binning, sel=selection+'&& Tau1_genmatch!=6', wt=weight_hmass)
                    hists['Jet1_pt'][sample + '_%s_%s_true'%(selection_DR['name'],selection_prongjet['name'])]= Hist('TH1F', sample=sample, var=['Jet1_pt'], binning=jet_pt_binning, sel=selection+'&& Tau1_genmatch!=6', wt=weight_jetpt)
                    hists['collinear_mass'][sample + '_%s_%s_true'%(selection_DR['name'],selection_prongjet['name'])]= Hist('TH1F', sample=sample, var=['collinear_mass'], binning=collinear_mass_binning, sel=selection+'&& Tau1_genmatch!=6', wt=weight_collinearmass)
                    hists['TauJ_mass'][sample + '_%s_%s_true'%(selection_DR['name'],selection_prongjet['name'])]= Hist('TH1F', sample=sample, var=['TauJ_mass'], binning=tauj_mass_binning, sel=selection+'&& Tau1_genmatch!=6', wt=weight_taujmass)
                    hists['Jet1_btag'][sample + '_%s_%s_true'%(selection_DR['name'],selection_prongjet['name'])]= Hist('TH1F', sample=sample, var=['Jet1_btag'], binning=[0.2,0.5,0.8,0.9,1.], sel=selection+'&& Tau1_genmatch!=6', wt=weight)
                    hists['Dzeta'][sample + '_%s_%s_true'%(selection_DR['name'],selection_prongjet['name'])]= Hist('TH1F', sample=sample, var=['Dzeta'], binning=[-100.,-70.,-30.,0.,30.,70.,100.], sel=selection+'&& Tau1_genmatch!=6', wt=weight)
                    hists['DRHJ'][sample + '_%s_%s_true'%(selection_DR['name'],selection_prongjet['name'])]= Hist('TH1F', sample=sample, var=['DRHJ'], binning=[0.,1.,2.,3.,4.,5.], sel=selection+'&& Tau1_genmatch!=6', wt=weight)
                    hists['HJ_pt'][sample + '_%s_%s_true'%(selection_DR['name'],selection_prongjet['name'])]= Hist('TH1F', sample=sample, var=['HJ_pt'], binning=[0.,40.,80.,120.,160.,200.], sel=selection+'&& Tau1_genmatch!=6', wt=weight)
                    hists['vis_mass'][sample + '_%s_%s_true'%(selection_DR['name'],selection_prongjet['name'])]= Hist('TH1F', sample=sample, var=['vis_mass'], binning=[0.,40.,80.,120.,160.,200.,250.,300.], sel=selection+'&& Tau1_genmatch!=6', wt=weight)
                    hists['Jet2_pt'][sample + '_%s_%s_true'%(selection_DR['name'],selection_prongjet['name'])]= Hist('TH1F', sample=sample, var=['Jet2_pt'], binning=[20.,40.,60.,80.,110.,150.], sel=selection+'&& Tau1_genmatch!=6', wt=weight)
                    hists['Jet2_btag'][sample + '_%s_%s_true'%(selection_DR['name'],selection_prongjet['name'])]= Hist('TH1F', sample=sample, var=['Jet2_btag'], binning=[0.,0.1,0.2,0.5,0.8,0.9,1.], sel=selection+'&& Tau1_genmatch!=6', wt=weight)
                    hists['Mu1_pt'][sample + '_%s_%s_true'%(selection_DR['name'],selection_prongjet['name'])]= Hist('TH1F', sample=sample, var=['Mu1_pt'], binning=[30.,40.,50.,60.,70.,80.,100.,130.], sel=selection+'&& Tau1_genmatch!=6', wt=weight)
                    hists['Ele1_pt'][sample + '_%s_%s_true'%(selection_DR['name'],selection_prongjet['name'])]= Hist('TH1F', sample=sample, var=['Ele1_pt'], binning=[30.,40.,50.,60.,70.,80.,100.,130.], sel=selection+'&& Tau1_genmatch!=6', wt=weight)
                    hists['H_pt'][sample + '_%s_%s_true'%(selection_DR['name'],selection_prongjet['name'])]= Hist('TH1F', sample=sample, var=['H_pt'], binning=[0.,40.,80.,120.,160.,200.,250.,300.], sel=selection+'&& Tau1_genmatch!=6', wt=weight_hpt)
                    hists['MET'][sample + '_%s_%s_true'%(selection_DR['name'],selection_prongjet['name'])]= Hist('TH1F', sample=sample, var=['MET'], binning=[0.,20.,40.,60.,80.,110.,150.,200.], sel=selection+'&& Tau1_genmatch!=6', wt=weight_hpt)


    MultiDraw(hists, samplesdir, getsamples(channel,year,preVFP), 'tree', mt_cores=4)


hists = Node()
drawPlots(hists,year,channel,preVFP)


# Loop through all nodes (just the ones containing TH1s)
for path, node in hists.ListNodes(withObjects=True):
    print('>> %s' % path)
    for selection_DR in selections_DR:
        for selection_prongjet in selections_prong:
            node['ST_%s_%s'%(selection_DR['name'],selection_prongjet['name'])] = node['ST_t_channel_antitop_%s_%s'%(selection_DR['name'],selection_prongjet['name'])] + node['ST_t_channel_top_%s_%s'%(selection_DR['name'],selection_prongjet['name'])]+node['ST_s_channel_%s_%s'%(selection_DR['name'],selection_prongjet['name'])] + node['ST_tW_antitop_%s_%s'%(selection_DR['name'],selection_prongjet['name'])]+node['ST_tW_top_%s_%s'%(selection_DR['name'],selection_prongjet['name'])]
            node['TT_%s_%s'%(selection_DR['name'],selection_prongjet['name'])] = node['TTTo2L2Nu_%s_%s'%(selection_DR['name'],selection_prongjet['name'])] + node['TTToHadronic_%s_%s'%(selection_DR['name'],selection_prongjet['name'])] + node['TTToSemiLeptonic_%s_%s'%(selection_DR['name'],selection_prongjet['name'])]
            node['DYJetscomb_%s_%s'%(selection_DR['name'],selection_prongjet['name'])] = node['DYJets_incl_%s_%s'%(selection_DR['name'],selection_prongjet['name'])] + node['DYJets_0J_%s_%s'%(selection_DR['name'],selection_prongjet['name'])] + node['DYJets_1J_%s_%s'%(selection_DR['name'],selection_prongjet['name'])] + node['DYJets_2J_%s_%s'%(selection_DR['name'],selection_prongjet['name'])]
            node['WJetscomb_%s_%s'%(selection_DR['name'],selection_prongjet['name'])] = node['WJets_incl_%s_%s'%(selection_DR['name'],selection_prongjet['name'])] + node['WJets_0J_%s_%s'%(selection_DR['name'],selection_prongjet['name'])] + node['WJets_1J_%s_%s'%(selection_DR['name'],selection_prongjet['name'])] + node['WJets_2J_%s_%s'%(selection_DR['name'],selection_prongjet['name'])]
            #subtracting rest for each DR
            if 'DR_QCD' in selection_DR['name'] or 'CR_QCD' in selection_DR['name']:
                node['REST_%s_%s'%(selection_DR['name'],selection_prongjet['name'])] = node['DYJetscomb_%s_%s'%(selection_DR['name'],selection_prongjet['name'])] + node['WJetscomb_%s_%s'%(selection_DR['name'],selection_prongjet['name'])] + node['TT_%s_%s'%(selection_DR['name'],selection_prongjet['name'])] + node['ST_%s_%s'%(selection_DR['name'],selection_prongjet['name'])]
                node['%s_%s'%(selection_DR['name'],selection_prongjet['name'])] = node['data_obs_%s_%s'%(selection_DR['name'],selection_prongjet['name'])] - node['REST_%s_%s'%(selection_DR['name'],selection_prongjet['name'])]
            elif 'DR_W' in selection_DR['name'] or 'CR_W' in selection_DR['name']:
                node['REST_%s_%s'%(selection_DR['name'],selection_prongjet['name'])] = node['DYJetscomb_%s_%s'%(selection_DR['name'],selection_prongjet['name'])] + node['TT_%s_%s'%(selection_DR['name'],selection_prongjet['name'])] + node['ST_%s_%s'%(selection_DR['name'],selection_prongjet['name'])]
                node['%s_%s'%(selection_DR['name'],selection_prongjet['name'])] = node['data_obs_%s_%s'%(selection_DR['name'],selection_prongjet['name'])] - node['REST_%s_%s'%(selection_DR['name'],selection_prongjet['name'])]
            elif 'DR_TT' in selection_DR['name'] or 'CR_TT' in selection_DR['name']:
                node['REST_%s_%s'%(selection_DR['name'],selection_prongjet['name'])] = node['DYJetscomb_%s_%s'%(selection_DR['name'],selection_prongjet['name'])] + node['WJetscomb_%s_%s'%(selection_DR['name'],selection_prongjet['name'])] + node['ST_%s_%s'%(selection_DR['name'],selection_prongjet['name'])]
                node['TT_%s_%s_true'%(selection_DR['name'],selection_prongjet['name'])] = node['TTTo2L2Nu_%s_%s_true'%(selection_DR['name'],selection_prongjet['name'])] + node['TTToHadronic_%s_%s_true'%(selection_DR['name'],selection_prongjet['name'])] + node['TTToSemiLeptonic_%s_%s_true'%(selection_DR['name'],selection_prongjet['name'])]
                node['TT_%s_%s_fakes'%(selection_DR['name'],selection_prongjet['name'])]= node['TT_%s_%s'%(selection_DR['name'],selection_prongjet['name'])]-node['TT_%s_%s_true'%(selection_DR['name'],selection_prongjet['name'])]
                node['%s_%s'%(selection_DR['name'],selection_prongjet['name'])] = node['data_obs_%s_%s'%(selection_DR['name'],selection_prongjet['name'])] - node['REST_%s_%s'%(selection_DR['name'],selection_prongjet['name'])]- node['TT_%s_%s_true'%(selection_DR['name'],selection_prongjet['name'])]  
                

fout = ROOT.TFile('root/ffvarcheck_%s_UL%s.root'%(channel,year), 'RECREATE')
NodeToTDir(fout, hists)
fout.Close()
