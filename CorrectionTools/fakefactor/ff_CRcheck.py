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

if year=="2016": #needed to make sure that preVFP+postVFP are used
    preVFP="_comb"

if channel=="mutau":
    selections_CR = [
        {'name':'CR_QCD',
         'selection':'isHtolooseMuTau && Mu1_charge*Tau1_charge==1 && Mu1_iso>0.15 && dimuon_veto==0 && electron_veto==0  && extra_muon_veto==0 && mt < 60 && nBjets_m>0'},
        {'name':'CR_QCD_AR',
         'selection':'isHtolooseMuTauAR && dimuon_veto==0 && Mu1_iso>0.15 && electron_veto==0  && extra_muon_veto==0 && Mu1_charge*Tau1_charge==1 && mt < 60 && nBjets_m>0'},
        {'name':'CR_W',
         'selection':'isHtoMuTau && dimuon_veto==0 && electron_veto==0  && extra_muon_veto==0 && Mu1_charge*Tau1_charge==-1 && mt > 60 && mt < 80 && nBjets_m==0'}, 
        {'name':'CR_W_AR',
         'selection':'isHtoMuTauAR && dimuon_veto==0 && electron_veto==0  && extra_muon_veto==0 && Mu1_charge*Tau1_charge==-1 && mt > 60 && mt < 80 && nBjets_m==0'},
        {'name':'CR_TT',
         'selection':'isHtoMuTau && dimuon_veto==0 && electron_veto==0  && extra_muon_veto==0 && Mu1_charge*Tau1_charge==-1 && mt > 60 && mt < 70 && nBjets_m>0'},
        {'name':'CR_TT_AR',
         'selection':'isHtoMuTauAR && dimuon_veto==0 && electron_veto==0  && extra_muon_veto==0 && Mu1_charge*Tau1_charge==-1 && mt > 60 && mt < 70 && nBjets_m>0'},
    ]

elif channel=="etau":
    selections_CR = [
        {'name':'CR_QCD',
         'selection':'isHtolooseETau && Ele1_charge*Tau1_charge==1 && Ele1_iso>0.1 && dielectron_veto==0 && muon_veto==0 && extra_electron_veto==0 && mt < 60 && nBjets_m>0'},
        {'name':'CR_QCD_AR',
         'selection':'isHtolooseETauAR && dielectron_veto==0 && Ele1_iso>0.1 && muon_veto==0 && extra_electron_veto==0 && Ele1_charge*Tau1_charge==1 && mt < 60 && nBjets_m>0'},
        {'name':'CR_W',
         'selection':'isHtoETau && dielectron_veto==0 && muon_veto==0 && extra_electron_veto==0 && Ele1_charge*Tau1_charge==-1 && mt > 60 && mt < 80 && nBjets_m==0'}, 
        {'name':'CR_W_AR',
         'selection':'isHtoETauAR && dielectron_veto==0 && muon_veto==0 && extra_electron_veto==0 && Ele1_charge*Tau1_charge==-1 && mt > 60 && mt < 80 && nBjets_m==0'},
        {'name':'CR_TT',
         'selection':'isHtoETau && dielectron_veto==0 && muon_veto==0 && extra_electron_veto==0 && Ele1_charge*Tau1_charge==-1 && mt > 60 && mt < 70 && nBjets_m>0'},
        {'name':'CR_TT_AR',
         'selection':'isHtoETauAR && dielectron_veto==0 && muon_veto==0 && extra_electron_veto==0 && Ele1_charge*Tau1_charge==-1 && mt > 60 && mt < 70 && nBjets_m>0'},
     ]


selections_prong = [
    {'name':'1prong',
     'selection':'&& (Tau1_decaymode==0 || Tau1_decaymode==1 || Tau1_decaymode==2)'},
    {'name':'3prong',
     'selection':'&& (Tau1_decaymode==10 || Tau1_decaymode==11)'}]

def drawPlots(hists,year,channel,preVFP):
    mutau_wts = 'EventWeight * LumiWeight * BTagWeight * PUIdWeight * MuWeight * MuTriggerWeight * TauWeight * wt_tt_pt * wt_tt * wt_dy * wt_w * wt_dy_nlo * wt_w_nlo'
    etau_wts = 'EventWeight * LumiWeight * BTagWeight * PUIdWeight * EWeight * ETriggerWeight * TauWeight * wt_tt_pt * wt_tt * wt_dy * wt_w * wt_dy_nlo * wt_w_nlo'
    if UL2016comb:
        preVFP="_comb"
    files = ["data_obs","DYJets_incl","DYJets_0J","DYJets_1J","DYJets_2J","WJets_incl","WJets_0J","WJets_1J","WJets_2J","TTTo2L2Nu","TTToHadronic","TTToSemiLeptonic","ST_t_channel_antitop","ST_t_channel_top","ST_s_channel","ST_tW_antitop","ST_tW_top"]
    for sample in files:
        samplesdir = '/pnfs/psi.ch/cms/trivcat/store/user/pbaertsc/bbh/samples_UL%s%s/'%(year,preVFP)
        #samplesdir = '/pnfs/psi.ch/cms/trivcat/store/user/pbaertsc/bbh/ffvarcorr/samples_UL%s%s/'%(year,preVFP)    
        for selection_CR in selections_CR:
            if selection_CR["name"]=="CR_QCD_AR":
                if sample=='data_obs':
                    weight = 'wt_ff_qcd * wt_ffcorr_hmass_qcd * wt_ffcorr_jetpt_qcd * wt_ffcorr_collinearmass_qcd * wt_ffcorr_taujmass_qcd'
                    #weight = 'wt_ff_qcd * wt_ffvarcorr_hmass_qcd * wt_ffvarcorr_jetpt_qcd * wt_ffvarcorr_collinearmass_qcd * wt_ffvarcorr_taujmass_qcd'
                else:
                    if channel=="mutau":
                        weight = mutau_wts+' * wt_ff_qcd * wt_ffcorr_hmass_qcd * wt_ffcorr_jetpt_qcd * wt_ffcorr_collinearmass_qcd * wt_ffcorr_taujmass_qcd'
                        #weight = mutau_wts+' * wt_ff_qcd * wt_ffvarcorr_hmass_qcd * wt_ffvarcorr_jetpt_qcd * wt_ffvarcorr_collinearmass_qcd * wt_ffvarcorr_taujmass_qcd'
                    elif channel=="etau":
                        weight = etau_wts+' * wt_ff_qcd * wt_ffcorr_hmass_qcd * wt_ffcorr_jetpt_qcd * wt_ffcorr_collinearmass_qcd * wt_ffcorr_taujmass_qcd'
                        #weight = etau_wts+' * wt_ff_qcd * wt_ffvarcorr_hmass_qcd * wt_ffvarcorr_jetpt_qcd * wt_ffvarcorr_collinearmass_qcd * wt_ffvarcorr_taujmass_qcd'
            elif selection_CR["name"]=="CR_W_AR": #no corrections for W DR
                if sample=='data_obs':
                    weight = 'wt_ff_w'
                else:
                    if channel=="mutau":
                        weight = mutau_wts+' * wt_ff_w'
                    elif channel=="etau":
                        weight = etau_wts+' * wt_ff_w'
            elif selection_CR["name"]=="CR_TT_AR":
                if sample=='data_obs':
                    weight = 'wt_ff_tt * wt_ffcorr_hmass_tt * wt_ffcorr_jetpt_tt * wt_ffcorr_collinearmass_tt * wt_ffcorr_taujmass_tt'
                    #weight = 'wt_ff_tt * wt_ffvarcorr_hmass_tt * wt_ffvarcorr_jetpt_tt * wt_ffvarcorr_collinearmass_tt * wt_ffvarcorr_taujmass_tt'
                else:
                    if channel=="mutau":
                        weight = mutau_wts+' * wt_ff_tt * wt_ffcorr_hmass_tt * wt_ffcorr_jetpt_tt * wt_ffcorr_collinearmass_tt * wt_ffcorr_taujmass_tt'
                        #weight = mutau_wts+' * wt_ff_tt * wt_ffvarcorr_hmass_tt * wt_ffvarcorr_jetpt_tt * wt_ffvarcorr_collinearmass_tt * wt_ffvarcorr_taujmass_tt'
                    elif channel=="etau":
                        weight = etau_wts+' * wt_ff_tt * wt_ffcorr_hmass_tt * wt_ffcorr_jetpt_tt * wt_ffcorr_collinearmass_tt * wt_ffcorr_taujmass_tt'
                        #weight = etau_wts+' * wt_ff_tt * wt_ffvarcorr_hmass_tt * wt_ffvarcorr_jetpt_tt * wt_ffvarcorr_collinearmass_tt * wt_ffvarcorr_taujmass_tt'
            else:
                if sample=='data_obs':
                    weight = '1.'
                else:
                    if channel=="mutau":
                        weight = mutau_wts
                    elif channel=="etau":
                        weight = etau_wts
            if 'QCD' in selection_CR['name']:
                if channel=="mutau":
                    tau_pt_binning = [30.,40.,50.,60.,70.,80.,130.]
                elif channel=="etau":
                    tau_pt_binning = [30.,40.,50.,130.]
            else:
                tau_pt_binning = [30.,40.,50.,60.,70.,80.,100.,130.]
            for selection_prongjet in selections_prong:
                selection = selection_CR['selection']+selection_prongjet['selection']
                hists['Tau1_pt'][sample + '_%s_%s'%(selection_CR['name'],selection_prongjet['name'])]= Hist('TH1F', sample=sample, var=['Tau1_pt'], binning=tau_pt_binning, sel=selection, wt=weight)
                if 'CR_TT' in selection_CR['name']:
                    hists['Tau1_pt'][sample + '_%s_%s_true'%(selection_CR['name'],selection_prongjet['name'])]= Hist('TH1F', sample=sample, var=['Tau1_pt'], binning=tau_pt_binning, sel=selection+'&& Tau1_genmatch!=6', wt=weight)
                   


    MultiDraw(hists, samplesdir, getsamples(channel,year,preVFP), 'tree', mt_cores=4)


hists = Node()
drawPlots(hists,year,channel,preVFP)


# Loop through all nodes (just the ones containing TH1s)
for path, node in hists.ListNodes(withObjects=True):
    print('>> %s' % path)
    for selection_CR in selections_CR:
        for selection_prongjet in selections_prong:
            node['ST_%s_%s'%(selection_CR['name'],selection_prongjet['name'])] = node['ST_t_channel_antitop_%s_%s'%(selection_CR['name'],selection_prongjet['name'])] + node['ST_t_channel_top_%s_%s'%(selection_CR['name'],selection_prongjet['name'])] + node['ST_s_channel_%s_%s'%(selection_CR['name'],selection_prongjet['name'])] + node['ST_tW_antitop_%s_%s'%(selection_CR['name'],selection_prongjet['name'])]+node['ST_tW_top_%s_%s'%(selection_CR['name'],selection_prongjet['name'])]
            node['TT_%s_%s'%(selection_CR['name'],selection_prongjet['name'])] = node['TTTo2L2Nu_%s_%s'%(selection_CR['name'],selection_prongjet['name'])] + node['TTToHadronic_%s_%s'%(selection_CR['name'],selection_prongjet['name'])] + node['TTToSemiLeptonic_%s_%s'%(selection_CR['name'],selection_prongjet['name'])]
            node['DYJetscomb_%s_%s'%(selection_CR['name'],selection_prongjet['name'])] = node['DYJets_incl_%s_%s'%(selection_CR['name'],selection_prongjet['name'])] + node['DYJets_0J_%s_%s'%(selection_CR['name'],selection_prongjet['name'])] + node['DYJets_1J_%s_%s'%(selection_CR['name'],selection_prongjet['name'])] + node['DYJets_2J_%s_%s'%(selection_CR['name'],selection_prongjet['name'])]
            node['WJetscomb_%s_%s'%(selection_CR['name'],selection_prongjet['name'])] = node['WJets_incl_%s_%s'%(selection_CR['name'],selection_prongjet['name'])] + node['WJets_0J_%s_%s'%(selection_CR['name'],selection_prongjet['name'])] + node['WJets_1J_%s_%s'%(selection_CR['name'],selection_prongjet['name'])] + node['WJets_2J_%s_%s'%(selection_CR['name'],selection_prongjet['name'])]
            if 'CR_QCD' in selection_CR['name']:
                node['REST_%s_%s'%(selection_CR['name'],selection_prongjet['name'])] = node['DYJetscomb_%s_%s'%(selection_CR['name'],selection_prongjet['name'])] + node['WJetscomb_%s_%s'%(selection_CR['name'],selection_prongjet['name'])] + node['TT_%s_%s'%(selection_CR['name'],selection_prongjet['name'])] + node['ST_%s_%s'%(selection_CR['name'],selection_prongjet['name'])]
                node['%s_%s'%(selection_CR['name'],selection_prongjet['name'])] = node['data_obs_%s_%s'%(selection_CR['name'],selection_prongjet['name'])] - node['REST_%s_%s'%(selection_CR['name'],selection_prongjet['name'])]
            elif 'CR_W' in selection_CR['name']:
                node['REST_%s_%s'%(selection_CR['name'],selection_prongjet['name'])] = node['DYJetscomb_%s_%s'%(selection_CR['name'],selection_prongjet['name'])] + node['TT_%s_%s'%(selection_CR['name'],selection_prongjet['name'])] + node['ST_%s_%s'%(selection_CR['name'],selection_prongjet['name'])]
                node['%s_%s'%(selection_CR['name'],selection_prongjet['name'])] = node['data_obs_%s_%s'%(selection_CR['name'],selection_prongjet['name'])] - node['REST_%s_%s'%(selection_CR['name'],selection_prongjet['name'])]
            elif 'CR_TT' in selection_CR['name']:
                node['REST_%s_%s'%(selection_CR['name'],selection_prongjet['name'])] = node['DYJetscomb_%s_%s'%(selection_CR['name'],selection_prongjet['name'])] + node['WJetscomb_%s_%s'%(selection_CR['name'],selection_prongjet['name'])] + node['ST_%s_%s'%(selection_CR['name'],selection_prongjet['name'])]
                node['TT_%s_%s_true'%(selection_CR['name'],selection_prongjet['name'])] = node['TTTo2L2Nu_%s_%s_true'%(selection_CR['name'],selection_prongjet['name'])] + node['TTToHadronic_%s_%s_true'%(selection_CR['name'],selection_prongjet['name'])] + node['TTToSemiLeptonic_%s_%s_true'%(selection_CR['name'],selection_prongjet['name'])]
                node['TT_%s_%s_fakes'%(selection_CR['name'],selection_prongjet['name'])] = node['TT_%s_%s'%(selection_CR['name'],selection_prongjet['name'])] - node['TT_%s_%s_true'%(selection_CR['name'],selection_prongjet['name'])]
                node['%s_%s'%(selection_CR['name'],selection_prongjet['name'])] = node['data_obs_%s_%s'%(selection_CR['name'],selection_prongjet['name'])] - node['REST_%s_%s'%(selection_CR['name'],selection_prongjet['name'])]- node['TT_%s_%s_true'%(selection_CR['name'],selection_prongjet['name'])]
                  
                

fout = ROOT.TFile('root/ffCRcheck_%s_UL%s.root'%(channel,year), 'RECREATE')
NodeToTDir(fout, hists)
fout.Close()
