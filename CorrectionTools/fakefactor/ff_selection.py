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
args = parser.parse_args()

year = args.year
channel = args.channel
preVFP = args.preVFP
#LUMI        = 137190.

if year=="2016":
    preVFP="_comb"         

if channel=="mutau":
    selection_AR = 'isHtoMuTauAR && dimuon_veto==0 && electron_veto==0 && extra_muon_veto==0 && Mu1_charge*Tau1_charge==-1 && mt < 60 && nBjets_m>0'
    selection_ARTT = 'isHtoMuTauAR && dimuon_veto==0 && electron_veto==0 && extra_muon_veto==0 && Mu1_charge*Tau1_charge==-1 && mt > 70 && mt < 90 && nBjets_m>0'
    selection_ARQCD = 'isHtoMuTauAR && dimuon_veto==0 && electron_veto==0 && extra_muon_veto==0 && Mu1_charge*Tau1_charge==1 && mt < 60 && nBjets_m>0'
    

    selections_DR = [
        {'name':'DR_QCD',
         'selection':'isHtoMuTau && Mu1_charge*Tau1_charge==1 && dimuon_veto==0 && electron_veto==0 && extra_muon_veto==0 && mt < 60 && nBjets_m>0'},
        {'name':'CR_QCD',
         'selection':'isHtolooseMuTau && Mu1_charge*Tau1_charge==1 && Mu1_iso>0.15 && dimuon_veto==0 && electron_veto==0 && extra_muon_veto==0 && mt < 60 && nBjets_m>0'},
        {'name':'DR_QCD_AR',
         'selection':'isHtoMuTauAR && dimuon_veto==0 && electron_veto==0 && extra_muon_veto==0 && Mu1_charge*Tau1_charge==1 && mt < 60 && nBjets_m>0'},
        {'name':'CR_QCD_AR',
         'selection':'isHtolooseMuTauAR && dimuon_veto==0 && Mu1_iso>0.15 && electron_veto==0 && extra_muon_veto==0 && Mu1_charge*Tau1_charge==1 && mt < 60 && nBjets_m>0'},
        {'name':'DR_W',
         'selection':'isHtoMuTau && dimuon_veto==0 && electron_veto==0 && extra_muon_veto==0 && Mu1_charge*Tau1_charge==-1 && mt > 80 && nBjets_m==0'},
        {'name':'CR_W',
         'selection':'isHtoMuTau && dimuon_veto==0 && electron_veto==0 && extra_muon_veto==0 && Mu1_charge*Tau1_charge==-1 && mt > 60 && mt < 80 && nBjets_m==0'}, 
        {'name':'SR_W',
         'selection':'isHtoMuTau && dimuon_veto==0 && electron_veto==0 && extra_muon_veto==0 && Mu1_charge*Tau1_charge==-1 && mt < 60 && nBjets_m>0'},            
        {'name':'DR_W_AR',
         'selection':'isHtoMuTauAR && dimuon_veto==0 && electron_veto==0 && extra_muon_veto==0 && Mu1_charge*Tau1_charge==-1 && mt > 80 && nBjets_m==0'},
        {'name':'CR_W_AR',
         'selection':'isHtoMuTauAR && dimuon_veto==0 && electron_veto==0 && extra_muon_veto==0 && Mu1_charge*Tau1_charge==-1 && mt > 60 && mt < 80 && nBjets_m==0'},
        {'name':'SR_W_AR',
         'selection':'isHtoMuTauAR && dimuon_veto==0 && electron_veto==0 && extra_muon_veto==0 && Mu1_charge*Tau1_charge==-1 && mt < 60 && nBjets_m>0'},            
        {'name' : 'DR_TT',
        'selection':'isHtoMuTau && dimuon_veto==0 && electron_veto==0 && extra_muon_veto==0 && Mu1_charge*Tau1_charge==-1 && mt > 70 && mt < 90 && nBjets_m>0'},
        {'name' : 'LCR_TT',
         'selection':'isHtoMuTauAR && dimuon_veto==0 && electron_veto==0 && extra_muon_veto==0 && Mu1_charge*Tau1_charge==-1 && mt > 70 && mt < 90 && nBjets_m>0 && Tau1_Idvsjet==15'},
        {'name':'CR_TT',
         'selection':'isHtoMuTau && dimuon_veto==0 && electron_veto==0 && extra_muon_veto==0 && Mu1_charge*Tau1_charge==-1 && mt > 60 && mt < 70 && nBjets_m>0'},
        {'name':'SR_TT',
         'selection':'isHtoMuTau && dimuon_veto==0 && electron_veto==0 && extra_muon_veto==0 && Mu1_charge*Tau1_charge==-1 && mt < 60 && nBjets_m>0'},   
        {'name':'All_TT',
         'selection':'isHtoMuTau && dimuon_veto==0 && electron_veto==0 && extra_muon_veto==0 && Mu1_charge*Tau1_charge==-1 && nBjets_m>0'},
        {'name':'DR_TT_AR',
        'selection':'isHtoMuTauAR && dimuon_veto==0 && electron_veto==0 && extra_muon_veto==0 && Mu1_charge*Tau1_charge==-1 && mt > 70 && mt < 90 && nBjets_m>0'},
        {'name':'LCR_TT_AR',
         'selection':'isHtoMuTauAR && dimuon_veto==0 && electron_veto==0 && extra_muon_veto==0 && Mu1_charge*Tau1_charge==-1 && mt > 70 && mt < 90 && nBjets_m>0 && Tau1_Idvsjet>=1 && Tau1_Idvsjet<15'},
        {'name':'CR_TT_AR',
         'selection':'isHtoMuTauAR && dimuon_veto==0 && electron_veto==0 && extra_muon_veto==0 && Mu1_charge*Tau1_charge==-1 && mt > 60 && mt < 70 && nBjets_m>0'},
        {'name':'SR_TT_AR',
         'selection':'isHtoMuTauAR && dimuon_veto==0 && electron_veto==0 && extra_muon_veto==0 && Mu1_charge*Tau1_charge==-1 && mt < 60 && nBjets_m>0'},
        {'name':'All_TT_AR',
         'selection':'isHtoMuTauAR && dimuon_veto==0 && electron_veto==0 && extra_muon_veto==0 && Mu1_charge*Tau1_charge==-1 && nBjets_m>0'},
    ]

elif channel=="etau":
    selection_AR = 'isHtoETauAR && dielectron_veto==0 && muon_veto==0 && extra_electron_veto==0 && Ele1_charge*Tau1_charge==-1 && mt < 60 && nBjets_m>0'
    selection_ARTT = 'isHtoETauAR && dielectron_veto==0 && muon_veto==0 && extra_electron_veto==0 && Ele1_charge*Tau1_charge==-1 && mt > 70 && mt < 90 && nBjets_m>0'
    selection_ARQCD = 'isHtoETauAR && dielectron_veto==0 && muon_veto==0 && extra_electron_veto==0 && Ele1_charge*Tau1_charge==1 && mt < 60 && nBjets_m>0'

    selections_DR = [
        {'name':'DR_QCD',
         'selection':'isHtoETau && Ele1_charge*Tau1_charge==1 && dielectron_veto==0 && muon_veto==0 && extra_electron_veto==0 && mt < 60 && nBjets_m>0'},
        {'name':'CR_QCD',
         'selection':'isHtolooseETau && Ele1_charge*Tau1_charge==1 && Ele1_iso>0.1 && dielectron_veto==0 && muon_veto==0 && extra_electron_veto==0 && mt < 60 && nBjets_m>0'},
        {'name':'DR_QCD_AR',
         'selection':'isHtoETauAR && dielectron_veto==0 && muon_veto==0 && extra_electron_veto==0 && Ele1_charge*Tau1_charge==1 && mt < 60 && nBjets_m>0'},
        {'name':'CR_QCD_AR',
         'selection':'isHtolooseETauAR && dielectron_veto==0 && Ele1_iso>0.1 && muon_veto==0 && extra_electron_veto==0 && Ele1_charge*Tau1_charge==1 && mt < 60 && nBjets_m>0'},
        {'name':'DR_W',
         'selection':'isHtoETau && dielectron_veto==0 && muon_veto==0 && extra_electron_veto==0 && Ele1_charge*Tau1_charge==-1 && mt > 80 && nBjets_m==0'},
        {'name':'CR_W',
         'selection':'isHtoETau && dielectron_veto==0 && muon_veto==0 && extra_electron_veto==0 && Ele1_charge*Tau1_charge==-1 && mt > 60 && mt < 80 && nBjets_m==0'}, 
        {'name':'SR_W',
         'selection':'isHtoETau && dielectron_veto==0 && muon_veto==0 && extra_electron_veto==0 && Ele1_charge*Tau1_charge==-1 && mt < 60 && nBjets_m>0'},            
        {'name':'DR_W_AR',
         'selection':'isHtoETauAR && dielectron_veto==0 && muon_veto==0 && extra_electron_veto==0 && Ele1_charge*Tau1_charge==-1 && mt > 80 && nBjets_m==0'},
        {'name':'CR_W_AR',
         'selection':'isHtoETauAR && dielectron_veto==0 && muon_veto==0 && extra_electron_veto==0 && Ele1_charge*Tau1_charge==-1 && mt > 60 && mt < 80 && nBjets_m==0'},
        {'name':'SR_W_AR',
         'selection':'isHtoETauAR && dielectron_veto==0 && muon_veto==0 && extra_electron_veto==0 && Ele1_charge*Tau1_charge==-1 && mt < 60 && nBjets_m>0'},            
        {'name' : 'DR_TT',
         'selection':'isHtoETau && dielectron_veto==0 && muon_veto==0 && extra_electron_veto==0 && Ele1_charge*Tau1_charge==-1 && mt > 70 && mt < 90 && nBjets_m>0'},
        {'name' : 'LCR_TT',
         'selection':'isHtoETauAR && dielectron_veto==0 && muon_veto==0 && extra_electron_veto==0 && Ele1_charge*Tau1_charge==-1 && mt > 70 && mt < 90 && nBjets_m>0 && Tau1_Idvsjet==15'},
        {'name':'CR_TT',
         'selection':'isHtoETau && dielectron_veto==0 && muon_veto==0 && extra_electron_veto==0 && Ele1_charge*Tau1_charge==-1 && mt > 60 && mt < 70 && nBjets_m>0'},
        {'name':'SR_TT',
         'selection':'isHtoETau && dielectron_veto==0 && muon_veto==0 && extra_electron_veto==0 && Ele1_charge*Tau1_charge==-1 && mt < 60 && nBjets_m>0'},   
        {'name':'All_TT',
         'selection':'isHtoETau && dielectron_veto==0 && muon_veto==0 && extra_electron_veto==0 && Ele1_charge*Tau1_charge==-1 && nBjets_m>0'},
        {'name':'DR_TT_AR',
         'selection':'isHtoETauAR && dielectron_veto==0 && muon_veto==0 && extra_electron_veto==0 && Ele1_charge*Tau1_charge==-1 && mt > 70 && mt < 90 && nBjets_m>0'},
        {'name':'LCR_TT_AR',
         'selection':'isHtoETauAR && dielectron_veto==0 && muon_veto==0 && extra_electron_veto==0 && Ele1_charge*Tau1_charge==-1 && mt > 70 && mt < 90 && nBjets_m>0 && Tau1_Idvsjet>=1 && Tau1_Idvsjet<15'},
        {'name':'CR_TT_AR',
         'selection':'isHtoETauAR && dielectron_veto==0 && muon_veto==0 && extra_electron_veto==0 && Ele1_charge*Tau1_charge==-1 && mt > 60 && mt < 70 && nBjets_m>0'},
        {'name':'SR_TT_AR',
         'selection':'isHtoETauAR && dielectron_veto==0 && muon_veto==0 && extra_electron_veto==0 && Ele1_charge*Tau1_charge==-1 && mt < 60 && nBjets_m>0'},
        {'name':'All_TT_AR',
         'selection':'isHtoETauAR && dielectron_veto==0 && muon_veto==0 && extra_electron_veto==0 && Ele1_charge*Tau1_charge==-1 && nBjets_m>0'},
        ]


selections_prong = [
    {'name':'1prong',
     'selection':'&& (Tau1_decaymode==0 || Tau1_decaymode==1 || Tau1_decaymode==2)'},
    {'name':'3prong',
     'selection':'&& (Tau1_decaymode==10 || Tau1_decaymode==11)'}]

def drawPlots(hists,year,channel,preVFP):
    for sample in getsamples(channel,year,preVFP):
        samplesdir = '/pnfs/psi.ch/cms/trivcat/store/user/pbaertsc/bbh/samples_UL%s%s/'%(year,preVFP)
        if sample=='data_obs':
            weight = '1.'
        else:
            if channel=="mutau":
                weight = 'EventWeight * LumiWeight * BTagWeight * PUIdWeight * MuWeight * MuTriggerWeight * TauWeight * wt_tt_pt * wt_tt * wt_dy * wt_w  * wt_dy_nlo * wt_w_nlo'   
            elif channel=="etau":
                weight = 'EventWeight * LumiWeight * BTagWeight * PUIdWeight * EWeight * ETriggerWeight * TauWeight * wt_tt_pt * wt_tt * wt_dy * wt_w * wt_dy_nlo * wt_w_nlo' 
        for selection_prongjet in selections_prong:
            tau_pt_binning = [30.,40.,50.,60.,70.,80.,100.,130.]
            selection = selection_AR+selection_prongjet['selection'] 
            selection_TT = selection_ARTT+selection_prongjet['selection']
            selection_QCD = selection_ARQCD+selection_prongjet['selection']
            hists['Tau1_pt'][sample + '_AR_%s'%selection_prongjet['name']]= Hist('TH1F', sample=sample, var=['Tau1_pt'], binning=tau_pt_binning, sel=selection, wt=weight)
            hists['Tau1_pt'][sample + '_ARtrue_%s'%selection_prongjet['name']]= Hist('TH1F', sample=sample, var=['Tau1_pt'], binning=tau_pt_binning, sel=selection+'&& Tau1_genmatch!=6', wt=weight)
            hists['Tau1_pt'][sample + '_ARTT_%s'%selection_prongjet['name']]= Hist('TH1F', sample=sample, var=['Tau1_pt'], binning=tau_pt_binning, sel=selection_TT, wt=weight)
            hists['Tau1_pt'][sample + '_ARTTtrue_%s'%selection_prongjet['name']]= Hist('TH1F', sample=sample, var=['Tau1_pt'], binning=tau_pt_binning, sel=selection_TT+'&& Tau1_genmatch!=6', wt=weight)
            hists['Tau1_pt'][sample + '_ARQCD_%s'%selection_prongjet['name']]= Hist('TH1F', sample=sample, var=['Tau1_pt'], binning=tau_pt_binning, sel=selection_QCD, wt=weight)
            hists['Tau1_pt'][sample + '_ARQCDtrue_%s'%selection_prongjet['name']]= Hist('TH1F', sample=sample, var=['Tau1_pt'], binning=tau_pt_binning, sel=selection_QCD+'&& Tau1_genmatch!=6', wt=weight)
            ####
            hists['Tau1_pt'][sample + '_ARQCDScaleUp_%s'%selection_prongjet['name']]= Hist('TH1F', sample=sample, var=['Tau1_pt'], binning=tau_pt_binning, sel=selection, wt=weight+' * LHEScaleWeightUp')
            hists['Tau1_pt'][sample + '_ARQCDScaleDown_%s'%selection_prongjet['name']]= Hist('TH1F', sample=sample, var=['Tau1_pt'], binning=tau_pt_binning, sel=selection, wt=weight+' * LHEScaleWeightDown') 
            hists['Tau1_pt'][sample + '_ARQCDScaleUptrue_%s'%selection_prongjet['name']]= Hist('TH1F', sample=sample, var=['Tau1_pt'], binning=tau_pt_binning, sel=selection+'&& Tau1_genmatch!=6', wt=weight+' * LHEScaleWeightUp')
            hists['Tau1_pt'][sample + '_ARQCDScaleDowntrue_%s'%selection_prongjet['name']]= Hist('TH1F', sample=sample, var=['Tau1_pt'], binning=tau_pt_binning, sel=selection+'&& Tau1_genmatch!=6', wt=weight+' * LHEScaleWeightDown')

        for selection_DR in selections_DR:
            if 'QCD' in selection_DR['name']:
                if channel=="mutau":
                    tau_pt_binning = [30.,40.,50.,60.,70.,80.,130.]
                elif channel=="etau":
                    tau_pt_binning = [30.,40.,50.,130.]
            else:
                tau_pt_binning = [30.,40.,50.,60.,70.,80.,100.,130.]
            for selection_prongjet in selections_prong:
                selection = selection_DR['selection']+selection_prongjet['selection']
                hists['Tau1_pt'][sample + '_%s_%s'%(selection_DR['name'],selection_prongjet['name'])]= Hist('TH1F', sample=sample, var=['Tau1_pt'], binning=tau_pt_binning, sel=selection, wt=weight)
                if 'DR_TT' in selection_DR['name'] or 'CR_TT' in selection_DR['name'] or 'LCR_TT' in selection_DR['name']:
                    hists['Tau1_pt'][sample + '_%s_%s_true'%(selection_DR['name'],selection_prongjet['name'])]= Hist('TH1F', sample=sample, var=['Tau1_pt'], binning=tau_pt_binning, sel=selection+'&& Tau1_genmatch!=6', wt=weight)
                    
    MultiDraw(hists, samplesdir, getsamples(channel,year,preVFP), 'tree', mt_cores=4)

hists = Node()
drawPlots(hists,year,channel,preVFP)


# Loop through all nodes (just the ones containing TH1s)
for path, node in hists.ListNodes(withObjects=True):
    print('>> %s' % path)
    for selection_prongjet in selections_prong:
        #AR with fake+true contribution
        for region in ["","TT","QCD","QCDScaleUp","QCDScaleDown"]:
            node['ST_AR%s_%s'%(region,selection_prongjet['name'])] = node['ST_t_channel_antitop_AR%s_%s'%(region,selection_prongjet['name'])] + node['ST_t_channel_top_AR%s_%s'%(region,selection_prongjet['name'])] + node['ST_s_channel_AR%s_%s'%(region,selection_prongjet['name'])] + node['ST_tW_antitop_AR%s_%s'%(region,selection_prongjet['name'])] + node['ST_tW_top_AR%s_%s'%(region,selection_prongjet['name'])]
            node['TT_AR%s_%s'%(region,selection_prongjet['name'])] = node['TTTo2L2Nu_AR%s_%s'%(region,selection_prongjet['name'])] + node['TTToHadronic_AR%s_%s'%(region,selection_prongjet['name'])] + node['TTToSemiLeptonic_AR%s_%s'%(region,selection_prongjet['name'])]
            node['DYJetscomb_AR%s_%s'%(region,selection_prongjet['name'])] = node['DYJets_incl_AR%s_%s'%(region,selection_prongjet['name'])] + node['DYJets_0J_AR%s_%s'%(region,selection_prongjet['name'])] + node['DYJets_1J_AR%s_%s'%(region,selection_prongjet['name'])] + node['DYJets_2J_AR%s_%s'%(region,selection_prongjet['name'])]
            node['WJetscomb_AR%s_%s'%(region,selection_prongjet['name'])] = node['WJets_incl_AR%s_%s'%(region,selection_prongjet['name'])] + node['WJets_0J_AR%s_%s'%(region,selection_prongjet['name'])] + node['WJets_1J_AR%s_%s'%(region,selection_prongjet['name'])] + node['WJets_2J_AR%s_%s'%(region,selection_prongjet['name'])]
            node['VV_AR%s_%s'%(region,selection_prongjet['name'])] = node['WWTo2L2Nu_AR%s_%s'%(region,selection_prongjet['name'])] + node['WWTo1L1Nu2Q_AR%s_%s'%(region,selection_prongjet['name'])] + node['WWTo4Q_AR%s_%s'%(region,selection_prongjet['name'])] + node['WZTo3LNu_AR%s_%s'%(region,selection_prongjet['name'])] + node['WZTo2L2Q_AR%s_%s'%(region,selection_prongjet['name'])] + node['WZTo1L3Nu_AR%s_%s'%(region,selection_prongjet['name'])] + node['WZTo1L1Nu2Q_AR%s_%s'%(region,selection_prongjet['name'])] + node['ZZTo4L_AR%s_%s'%(region,selection_prongjet['name'])] + node['ZZTo2L2Q_AR%s_%s'%(region,selection_prongjet['name'])] + node['ZZTo2Nu2Q_AR%s_%s'%(region,selection_prongjet['name'])]

            #derive QCD Multijet (true contribution has to be included, otherwise would count as QCD)
            node['Multijet_AR%s_%s'%(region,selection_prongjet['name'])]=node['data_obs_AR%s_%s'%(region,selection_prongjet['name'])]-node['ST_AR%s_%s'%(region,selection_prongjet['name'])]-node['TT_AR%s_%s'%(region,selection_prongjet['name'])]-node['DYJetscomb_AR%s_%s'%(region,selection_prongjet['name'])]-node['WJetscomb_AR%s_%s'%(region,selection_prongjet['name'])]-node['VV_AR%s_%s'%(region,selection_prongjet['name'])]
       
            #true contribution
            node['ST_AR%strue_%s'%(region,selection_prongjet['name'])] = node['ST_t_channel_antitop_AR%strue_%s'%(region,selection_prongjet['name'])] + node['ST_t_channel_top_AR%strue_%s'%(region,selection_prongjet['name'])] + node['ST_s_channel_AR%strue_%s'%(region,selection_prongjet['name'])] + node['ST_tW_antitop_AR%strue_%s'%(region,selection_prongjet['name'])] + node['ST_tW_top_AR%strue_%s'%(region,selection_prongjet['name'])]
            node['TT_AR%strue_%s'%(region,selection_prongjet['name'])] = node['TTTo2L2Nu_AR%strue_%s'%(region,selection_prongjet['name'])] + node['TTToHadronic_AR%strue_%s'%(region,selection_prongjet['name'])] + node['TTToSemiLeptonic_AR%strue_%s'%(region,selection_prongjet['name'])]
            node['DYJetscomb_AR%strue_%s'%(region,selection_prongjet['name'])] = node['DYJets_incl_AR%strue_%s'%(region,selection_prongjet['name'])] + node['DYJets_0J_AR%strue_%s'%(region,selection_prongjet['name'])] + node['DYJets_1J_AR%strue_%s'%(region,selection_prongjet['name'])] + node['DYJets_2J_AR%strue_%s'%(region,selection_prongjet['name'])]
            node['WJetscomb_AR%strue_%s'%(region,selection_prongjet['name'])] = node['WJets_incl_AR%strue_%s'%(region,selection_prongjet['name'])] + node['WJets_0J_AR%strue_%s'%(region,selection_prongjet['name'])] + node['WJets_1J_AR%strue_%s'%(region,selection_prongjet['name'])] + node['WJets_2J_AR%strue_%s'%(region,selection_prongjet['name'])]
            node['VV_AR%strue_%s'%(region,selection_prongjet['name'])] = node['WWTo2L2Nu_AR%strue_%s'%(region,selection_prongjet['name'])] + node['WWTo1L1Nu2Q_AR%strue_%s'%(region,selection_prongjet['name'])] + node['WWTo4Q_AR%strue_%s'%(region,selection_prongjet['name'])] + node['WZTo3LNu_AR%strue_%s'%(region,selection_prongjet['name'])] + node['WZTo2L2Q_AR%strue_%s'%(region,selection_prongjet['name'])] + node['WZTo1L3Nu_AR%strue_%s'%(region,selection_prongjet['name'])] + node['WZTo1L1Nu2Q_AR%strue_%s'%(region,selection_prongjet['name'])] + node['ZZTo4L_AR%strue_%s'%(region,selection_prongjet['name'])] + node['ZZTo2L2Q_AR%strue_%s'%(region,selection_prongjet['name'])] + node['ZZTo2Nu2Q_AR%strue_%s'%(region,selection_prongjet['name'])]
            node['Truetau_AR%s_%s'%(region,selection_prongjet['name'])]=node['ST_AR%strue_%s'%(region,selection_prongjet['name'])]+node['TT_AR%strue_%s'%(region,selection_prongjet['name'])]+node['DYJetscomb_AR%strue_%s'%(region,selection_prongjet['name'])]+node['WJetscomb_AR%strue_%s'%(region,selection_prongjet['name'])]+node['VV_AR%strue_%s'%(region,selection_prongjet['name'])]
            #remove true contribution from MC AR
            node['ST_AR%s_%s'%(region,selection_prongjet['name'])] = node['ST_AR%s_%s'%(region,selection_prongjet['name'])]-node['ST_AR%strue_%s'%(region,selection_prongjet['name'])]
            node['TT_AR%s_%s'%(region,selection_prongjet['name'])] = node['TT_AR%s_%s'%(region,selection_prongjet['name'])]-node['TT_AR%strue_%s'%(region,selection_prongjet['name'])]
            node['DYJetscomb_AR%s_%s'%(region,selection_prongjet['name'])] = node['DYJetscomb_AR%s_%s'%(region,selection_prongjet['name'])]-node['DYJetscomb_AR%strue_%s'%(region,selection_prongjet['name'])]
            node['WJetscomb_AR%s_%s'%(region,selection_prongjet['name'])] = node['WJetscomb_AR%s_%s'%(region,selection_prongjet['name'])]-node['WJetscomb_AR%strue_%s'%(region,selection_prongjet['name'])]
            node['VV_AR%s_%s'%(region,selection_prongjet['name'])] = node['VV_AR%s_%s'%(region,selection_prongjet['name'])]-node['VV_AR%strue_%s'%(region,selection_prongjet['name'])]
            node['MCnoQCD_AR%s_%s'%(region,selection_prongjet['name'])]=node['ST_AR%s_%s'%(region,selection_prongjet['name'])]+node['TT_AR%s_%s'%(region,selection_prongjet['name'])]+node['DYJetscomb_AR%s_%s'%(region,selection_prongjet['name'])]+node['WJetscomb_AR%s_%s'%(region,selection_prongjet['name'])]+node['VV_AR%s_%s'%(region,selection_prongjet['name'])]+node['Truetau_AR%s_%s'%(region,selection_prongjet['name'])] #QCD not included!!
            
    
        ############################################
    for selection_DR in selections_DR:
        for selection_prongjet in selections_prong:
            node['ST_%s_%s'%(selection_DR['name'],selection_prongjet['name'])] = node['ST_t_channel_antitop_%s_%s'%(selection_DR['name'],selection_prongjet['name'])] + node['ST_t_channel_top_%s_%s'%(selection_DR['name'],selection_prongjet['name'])]+node['ST_s_channel_%s_%s'%(selection_DR['name'],selection_prongjet['name'])] + node['ST_tW_antitop_%s_%s'%(selection_DR['name'],selection_prongjet['name'])]+node['ST_tW_top_%s_%s'%(selection_DR['name'],selection_prongjet['name'])]
            node['TT_%s_%s'%(selection_DR['name'],selection_prongjet['name'])] = node['TTTo2L2Nu_%s_%s'%(selection_DR['name'],selection_prongjet['name'])] + node['TTToHadronic_%s_%s'%(selection_DR['name'],selection_prongjet['name'])] + node['TTToSemiLeptonic_%s_%s'%(selection_DR['name'],selection_prongjet['name'])]
            node['DYJetscomb_%s_%s'%(selection_DR['name'],selection_prongjet['name'])] = node['DYJets_incl_%s_%s'%(selection_DR['name'],selection_prongjet['name'])] + node['DYJets_0J_%s_%s'%(selection_DR['name'],selection_prongjet['name'])] + node['DYJets_1J_%s_%s'%(selection_DR['name'],selection_prongjet['name'])] + node['DYJets_2J_%s_%s'%(selection_DR['name'],selection_prongjet['name'])]
            node['WJetscomb_%s_%s'%(selection_DR['name'],selection_prongjet['name'])] = node['WJets_incl_%s_%s'%(selection_DR['name'],selection_prongjet['name'])] + node['WJets_0J_%s_%s'%(selection_DR['name'],selection_prongjet['name'])] + node['WJets_1J_%s_%s'%(selection_DR['name'],selection_prongjet['name'])] + node['WJets_2J_%s_%s'%(selection_DR['name'],selection_prongjet['name'])]
            node['VV_%s_%s'%(selection_DR['name'],selection_prongjet['name'])] = node['WWTo2L2Nu_%s_%s'%(selection_DR['name'],selection_prongjet['name'])] + node['WWTo1L1Nu2Q_%s_%s'%(selection_DR['name'],selection_prongjet['name'])] + node['WWTo4Q_%s_%s'%(selection_DR['name'],selection_prongjet['name'])] + node['WZTo3LNu_%s_%s'%(selection_DR['name'],selection_prongjet['name'])] + node['WZTo2L2Q_%s_%s'%(selection_DR['name'],selection_prongjet['name'])] + node['WZTo1L3Nu_%s_%s'%(selection_DR['name'],selection_prongjet['name'])] + node['WZTo1L1Nu2Q_%s_%s'%(selection_DR['name'],selection_prongjet['name'])] + node['ZZTo4L_%s_%s'%(selection_DR['name'],selection_prongjet['name'])] + node['ZZTo2L2Q_%s_%s'%(selection_DR['name'],selection_prongjet['name'])] + node['ZZTo2Nu2Q_%s_%s'%(selection_DR['name'],selection_prongjet['name'])]
            #subtracting rest for each DR
            if 'DR_QCD' in selection_DR['name'] or 'CR_QCD' in selection_DR['name']:
                node['REST_%s_%s'%(selection_DR['name'],selection_prongjet['name'])] = node['DYJetscomb_%s_%s'%(selection_DR['name'],selection_prongjet['name'])] + node['WJetscomb_%s_%s'%(selection_DR['name'],selection_prongjet['name'])] + node['TT_%s_%s'%(selection_DR['name'],selection_prongjet['name'])] + node['ST_%s_%s'%(selection_DR['name'],selection_prongjet['name'])] + node['VV_%s_%s'%(selection_DR['name'],selection_prongjet['name'])]
                node['%s_%s'%(selection_DR['name'],selection_prongjet['name'])] = node['data_obs_%s_%s'%(selection_DR['name'],selection_prongjet['name'])] - node['REST_%s_%s'%(selection_DR['name'],selection_prongjet['name'])]
            elif 'DR_W' in selection_DR['name'] or 'CR_W' in selection_DR['name']:
                node['REST_%s_%s'%(selection_DR['name'],selection_prongjet['name'])] = node['DYJetscomb_%s_%s'%(selection_DR['name'],selection_prongjet['name'])] + node['TT_%s_%s'%(selection_DR['name'],selection_prongjet['name'])] + node['ST_%s_%s'%(selection_DR['name'],selection_prongjet['name'])] + node['VV_%s_%s'%(selection_DR['name'],selection_prongjet['name'])]
                node['%s_%s'%(selection_DR['name'],selection_prongjet['name'])] = node['data_obs_%s_%s'%(selection_DR['name'],selection_prongjet['name'])] - node['REST_%s_%s'%(selection_DR['name'],selection_prongjet['name'])]
            elif 'DR_TT' in selection_DR['name'] or 'CR_TT' in selection_DR['name'] or 'LCR_TT' in selection_DR['name']:
                node['REST_%s_%s'%(selection_DR['name'],selection_prongjet['name'])] = node['DYJetscomb_%s_%s'%(selection_DR['name'],selection_prongjet['name'])] + node['WJetscomb_%s_%s'%(selection_DR['name'],selection_prongjet['name'])] + node['ST_%s_%s'%(selection_DR['name'],selection_prongjet['name'])] + node['VV_%s_%s'%(selection_DR['name'],selection_prongjet['name'])]
                node['TT_%s_%s_true'%(selection_DR['name'],selection_prongjet['name'])] = node['TTTo2L2Nu_%s_%s_true'%(selection_DR['name'],selection_prongjet['name'])] + node['TTToHadronic_%s_%s_true'%(selection_DR['name'],selection_prongjet['name'])] + node['TTToSemiLeptonic_%s_%s_true'%(selection_DR['name'],selection_prongjet['name'])]
                node['TT_%s_%s_fakes'%(selection_DR['name'],selection_prongjet['name'])]= node['TT_%s_%s'%(selection_DR['name'],selection_prongjet['name'])]-node['TT_%s_%s_true'%(selection_DR['name'],selection_prongjet['name'])]
                node['%s_%s'%(selection_DR['name'],selection_prongjet['name'])] = node['data_obs_%s_%s'%(selection_DR['name'],selection_prongjet['name'])] - node['REST_%s_%s'%(selection_DR['name'],selection_prongjet['name'])]- node['TT_%s_%s_true'%(selection_DR['name'],selection_prongjet['name'])]
                

fout = ROOT.TFile('root/ff_%s_UL%s.root'%(channel,year), 'RECREATE')
NodeToTDir(fout, hists)
fout.Close()
