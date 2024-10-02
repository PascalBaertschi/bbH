import ROOT
from analysis import *
from argparse import ArgumentParser
import json
import utils
from array import array
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
parser.add_argument('-c', '--channel', dest='channel', choices=['mutau','etau','tautau'], type=str, default='mutau', action='store',)
parser.add_argument('-u', '--UL',      dest='ULtag', action='store_const', const="UL",default="")
parser.add_argument('-p', '--preVFP',  dest='preVFP', action='store_const', const="_preVFP",default="")
parser.add_argument('-t', '--comb',  dest='UL2016comb', action='store_true',default=False)
args = parser.parse_args()

year = args.year
channel = args.channel
ULtag = args.ULtag
preVFP = args.preVFP
UL2016comb = args.UL2016comb
#LUMI        = 137190.

if UL2016comb:
        preVFP="_comb"

           

if channel=="mutau":
    #selection_AR = 'isHtoMuTauAR && dimuon_veto==0 && electron_veto==0 && Mu1_charge*Tau1_charge==1'
    selection_AR = 'isHtoMuTauAR && dimuon_veto==0 && electron_veto==0 && Mu1_charge*Tau1_charge==-1 && transverse_mass_lepmet < 60 && nBjets_m>0'
    selection_ARTT = 'isHtoMuTauAR && dimuon_veto==0 && electron_veto==0 && Mu1_charge*Tau1_charge==-1 && transverse_mass_lepmet > 70 && transverse_mass_lepmet < 90 && nBjets_m>0'

    selections_DR = [
        {'name':'DR_QCD',
         'selection':'isHtoMuTau && Mu1_charge*Tau1_charge==1 && dimuon_veto==0 && electron_veto==0 && transverse_mass_lepmet < 60 && nBjets_m>0'},
        {'name':'CR_QCD',
         'selection':'isHtolooseMuTau && Mu1_charge*Tau1_charge==1 && Mu1_iso>0.15 && dimuon_veto==0 && electron_veto==0 && transverse_mass_lepmet < 60 && nBjets_m>0'},
        {'name':'DR_QCD_AR',
         'selection':'isHtoMuTauAR && dimuon_veto==0 && electron_veto==0 && Mu1_charge*Tau1_charge==1 && transverse_mass_lepmet < 60 && nBjets_m>0'},
        {'name':'CR_QCD_AR',
         'selection':'isHtolooseMuTauAR && dimuon_veto==0 && Mu1_iso>0.15 && electron_veto==0 && Mu1_charge*Tau1_charge==1 && transverse_mass_lepmet < 60 && nBjets_m>0'},
        {'name':'DR_W',
         'selection':'isHtoMuTau && dimuon_veto==0 && electron_veto==0 && Mu1_charge*Tau1_charge==-1 && transverse_mass_lepmet > 80 && nBjets_m==0'},
        {'name':'CR_W',
         'selection':'isHtoMuTau && dimuon_veto==0 && electron_veto==0 && Mu1_charge*Tau1_charge==-1 && transverse_mass_lepmet > 60 && transverse_mass_lepmet < 80 && nBjets_m==0'}, 
        {'name':'SR_W',
         'selection':'isHtoMuTau && dimuon_veto==0 && electron_veto==0 && Mu1_charge*Tau1_charge==-1 && transverse_mass_lepmet < 60 && nBjets_m>0'},            
        {'name':'DR_W_AR',
         'selection':'isHtoMuTauAR && dimuon_veto==0 && electron_veto==0 && Mu1_charge*Tau1_charge==-1 && transverse_mass_lepmet > 80 && nBjets_m==0'},
        {'name':'CR_W_AR',
         'selection':'isHtoMuTauAR && dimuon_veto==0 && electron_veto==0 && Mu1_charge*Tau1_charge==-1 && transverse_mass_lepmet > 60 && transverse_mass_lepmet < 80 && nBjets_m==0'},
        {'name':'SR_W_AR',
         'selection':'isHtoMuTauAR && dimuon_veto==0 && electron_veto==0 && Mu1_charge*Tau1_charge==-1 && transverse_mass_lepmet < 60 && nBjets_m>0'},            
        {'name' : 'DR_TT',
         'selection':'isHtoMuTau && dimuon_veto==0 && electron_veto==0 && Mu1_charge*Tau1_charge==-1 && transverse_mass_lepmet > 70 && transverse_mass_lepmet < 90 && nBjets_m>0'},
        {'name':'CR_TT',
         'selection':'isHtoMuTau && dimuon_veto==0 && electron_veto==0 && Mu1_charge*Tau1_charge==-1 && transverse_mass_lepmet > 60 && transverse_mass_lepmet < 70 && nBjets_m>0'},
        {'name':'SR_TT',
         'selection':'isHtoMuTau && dimuon_veto==0 && electron_veto==0 && Mu1_charge*Tau1_charge==-1 && transverse_mass_lepmet < 60 && nBjets_m>0'},   
        {'name':'All_TT',
         'selection':'isHtoMuTau && dimuon_veto==0 && electron_veto==0 && Mu1_charge*Tau1_charge==-1 && nBjets_m>0'},
        {'name':'DR_TT_AR',
         'selection':'isHtoMuTauAR && dimuon_veto==0 && electron_veto==0 && Mu1_charge*Tau1_charge==-1 && transverse_mass_lepmet > 70 && transverse_mass_lepmet < 90 && nBjets_m>0'},
        {'name':'CR_TT_AR',
         'selection':'isHtoMuTauAR && dimuon_veto==0 && electron_veto==0 && Mu1_charge*Tau1_charge==-1 && transverse_mass_lepmet > 60 && transverse_mass_lepmet < 70 && nBjets_m>0'},
        {'name':'SR_TT_AR',
         'selection':'isHtoMuTauAR && dimuon_veto==0 && electron_veto==0 && Mu1_charge*Tau1_charge==-1 && transverse_mass_lepmet < 60 && nBjets_m>0'},
        {'name':'All_TT_AR',
         'selection':'isHtoMuTauAR && dimuon_veto==0 && electron_veto==0 && Mu1_charge*Tau1_charge==-1 && nBjets_m>0'},
    ]

elif channel=="etau":
    #selection_AR = 'isHtoMuTauAR && dimuon_veto==0 && electron_veto==0 && Mu1_charge*Tau1_charge==1'
    selection_AR = 'isHtoETauAR && dielectron_veto==0 && muon_veto==0 && Ele1_charge*Tau1_charge==-1 && transverse_mass_lepmet < 60 && nBjets_m>0'
    selection_ARTT = 'isHtoETauAR && dielectron_veto==0 && muon_veto==0 && Ele1_charge*Tau1_charge==-1 && transverse_mass_lepmet > 70 && transverse_mass_lepmet < 90 && nBjets_m>0'

    selections_DR = [
        {'name':'DR_QCD',
         'selection':'isHtoETau && Ele1_charge*Tau1_charge==1 && dielectron_veto==0 && muon_veto==0 && transverse_mass_lepmet < 60 && nBjets_m>0'},
        {'name':'CR_QCD',
         'selection':'isHtolooseETau && Ele1_charge*Tau1_charge==1 && Ele1_iso>0.1 && dielectron_veto==0 && muon_veto==0 && transverse_mass_lepmet < 60 && nBjets_m>0'},
        {'name':'DR_QCD_AR',
         'selection':'isHtoETauAR && dielectron_veto==0 && muon_veto==0 && Ele1_charge*Tau1_charge==1 && transverse_mass_lepmet < 60 && nBjets_m>0'},
        {'name':'CR_QCD_AR',
         'selection':'isHtolooseETauAR && dielectron_veto==0 && Ele1_iso>0.1 && muon_veto==0 && Ele1_charge*Tau1_charge==1 && transverse_mass_lepmet < 60 && nBjets_m>0'},
        {'name':'DR_W',
         'selection':'isHtoETau && dielectron_veto==0 && muon_veto==0 && Ele1_charge*Tau1_charge==-1 && transverse_mass_lepmet > 80 && nBjets_m==0'},
        {'name':'CR_W',
         'selection':'isHtoETau && dielectron_veto==0 && muon_veto==0 && Ele1_charge*Tau1_charge==-1 && transverse_mass_lepmet > 60 && transverse_mass_lepmet < 80 && nBjets_m==0'}, 
        {'name':'SR_W',
         'selection':'isHtoETau && dielectron_veto==0 && muon_veto==0 && Ele1_charge*Tau1_charge==-1 && transverse_mass_lepmet < 60 && nBjets_m>0'},            
        {'name':'DR_W_AR',
         'selection':'isHtoETauAR && dielectron_veto==0 && muon_veto==0 && Ele1_charge*Tau1_charge==-1 && transverse_mass_lepmet > 80 && nBjets_m==0'},
        {'name':'CR_W_AR',
         'selection':'isHtoETauAR && dielectron_veto==0 && muon_veto==0 && Ele1_charge*Tau1_charge==-1 && transverse_mass_lepmet > 60 && transverse_mass_lepmet < 80 && nBjets_m==0'},
        {'name':'SR_W_AR',
         'selection':'isHtoETauAR && dielectron_veto==0 && muon_veto==0 && Ele1_charge*Tau1_charge==-1 && transverse_mass_lepmet < 60 && nBjets_m>0'},            
        {'name' : 'DR_TT',
         'selection':'isHtoETau && dielectron_veto==0 && muon_veto==0 && Ele1_charge*Tau1_charge==-1 && transverse_mass_lepmet > 70 && transverse_mass_lepmet < 90 && nBjets_m>0'},
        {'name':'CR_TT',
         'selection':'isHtoETau && dielectron_veto==0 && muon_veto==0 && Ele1_charge*Tau1_charge==-1 && transverse_mass_lepmet > 60 && transverse_mass_lepmet < 70 && nBjets_m>0'},
        {'name':'SR_TT',
         'selection':'isHtoETau && dielectron_veto==0 && muon_veto==0 && Ele1_charge*Tau1_charge==-1 && transverse_mass_lepmet < 60 && nBjets_m>0'},   
        {'name':'All_TT',
         'selection':'isHtoETau && dielectron_veto==0 && muon_veto==0 && Ele1_charge*Tau1_charge==-1 && nBjets_m>0'},
        {'name':'DR_TT_AR',
         'selection':'isHtoETauAR && dielectron_veto==0 && muon_veto==0 && Ele1_charge*Tau1_charge==-1 && transverse_mass_lepmet > 70 && transverse_mass_lepmet < 90 && nBjets_m>0'},
        {'name':'CR_TT_AR',
         'selection':'isHtoETauAR && dielectron_veto==0 && muon_veto==0 && Ele1_charge*Tau1_charge==-1 && transverse_mass_lepmet > 60 && transverse_mass_lepmet < 70 && nBjets_m>0'},
        {'name':'SR_TT_AR',
         'selection':'isHtoETauAR && dielectron_veto==0 && muon_veto==0 && Ele1_charge*Tau1_charge==-1 && transverse_mass_lepmet < 60 && nBjets_m>0'},
        {'name':'All_TT_AR',
         'selection':'isHtoETauAR && dielectron_veto==0 && muon_veto==0 && Ele1_charge*Tau1_charge==-1 && nBjets_m>0'},
        ]




selections_prong = [
    {'name':'1prong',
     'selection':'&& (Tau1_decaymode==0 || Tau1_decaymode==1 || Tau1_decaymode==2)'},
    {'name':'3prong',
     'selection':'&& (Tau1_decaymode==10 || Tau1_decaymode==11)'}]

def drawPlots(hists,year,channel,ULtag,preVFP):
    if UL2016comb:
        preVFP="_comb"
    for sample in getsamples(channel,ULtag,year,preVFP):
        #samplesdir = '/work/pbaertsc/bbh/NanoTreeProducer/samples_%s%s%s/'%(ULtag,year,preVFP)
        samplesdir = '/pnfs/psi.ch/cms/trivcat/store/user/pbaertsc/bbh/samples_%s%s%s/'%(ULtag,year,preVFP)
        if sample=='data_obs':
            weight = '1.'
        else:
            if channel=="mutau":
                if "DY" in sample:
                    weight = 'EventWeight * LumiWeight * BTagWeight * MuWeight * MuTriggerWeight * TauWeight * TauTriggerWeight * wt_dy'
                elif "TT" in sample:
                    weight = 'EventWeight * LumiWeight * BTagWeight * MuWeight * MuTriggerWeight * TauWeight * TauTriggerWeight * wt_tt'
                else:
                    weight = 'EventWeight * LumiWeight * BTagWeight * MuWeight * MuTriggerWeight * TauWeight * TauTriggerWeight'
            elif channel=="etau":
                if "DY" in sample:
                    weight = 'EventWeight * LumiWeight * BTagWeight * EWeight * ETriggerWeight * TauWeight * TauTriggerWeight * wt_dy'
                elif "TT" in sample:
                    weight = 'EventWeight * LumiWeight * BTagWeight * EWeight * ETriggerWeight * TauWeight * TauTriggerWeight * wt_tt'
                else:
                    weight = 'EventWeight * LumiWeight * BTagWeight * EWeight * ETriggerWeight * TauWeight * TauTriggerWeight'
        for selection_prongjet in selections_prong:
            selection = selection_AR+selection_prongjet['selection']
            selection_TT = selection_ARTT+selection_prongjet['selection']
            #hists['Tau1_pt'][sample + '_AR_%s'%selection_prongjet['name']]= Hist('TH1F', sample=sample, var=['Tau1_pt'], binning=(10,30,130), sel=selection, wt=weight)
            #hists['Tau1_pt'][sample + '_ARtrue_%s'%selection_prongjet['name']]= Hist('TH1F', sample=sample, var=['Tau1_pt'], binning=(10,30,130), sel=selection+'&& Tau1_genmatch!=6', wt=weight)
            hists['Tau1_pt'][sample + '_AR_%s'%selection_prongjet['name']]= Hist('TH1F', sample=sample, var=['Tau1_pt'], binning=[30,40,50,60,70,80,100,130], sel=selection, wt=weight)
            hists['Tau1_pt'][sample + '_ARtrue_%s'%selection_prongjet['name']]= Hist('TH1F', sample=sample, var=['Tau1_pt'], binning=[30,40,50,60,70,80,100,130], sel=selection+'&& Tau1_genmatch!=6', wt=weight)
            hists['Tau1_pt'][sample + '_ARTT_%s'%selection_prongjet['name']]= Hist('TH1F', sample=sample, var=['Tau1_pt'], binning=[30,40,50,60,70,80,100,130], sel=selection_TT, wt=weight)
            hists['Tau1_pt'][sample + '_ARTTtrue_%s'%selection_prongjet['name']]= Hist('TH1F', sample=sample, var=['Tau1_pt'], binning=[30,40,50,60,70,80,100,130], sel=selection_TT+'&& Tau1_genmatch!=6', wt=weight)
       
            hists['transverse_mass_lepmet'][sample + '_AR_%s'%selection_prongjet['name']]= Hist('TH1F', sample=sample, var=['transverse_mass_lepmet'], binning=(50,0,250), sel=selection, wt=weight)
            hists['transverse_mass_lepmet'][sample + '_ARtrue_%s'%selection_prongjet['name']]= Hist('TH1F', sample=sample, var=['transverse_mass_lepmet'], binning=(50,0,250), sel=selection+'&& Tau1_genmatch!=6', wt=weight)
            hists['transverse_mass_lepmet'][sample + '_ARTT_%s'%selection_prongjet['name']]= Hist('TH1F', sample=sample, var=['transverse_mass_lepmet'], binning=(50,0,250), sel=selection_TT, wt=weight)
            hists['transverse_mass_lepmet'][sample + '_ARTTtrue_%s'%selection_prongjet['name']]= Hist('TH1F', sample=sample, var=['transverse_mass_lepmet'], binning=(50,0,250), sel=selection_TT+'&& Tau1_genmatch!=6', wt=weight)

        #binning=(7,array('d',[30,40,50,60,70,80,100,130]),6,array('d',[20,60,100,140,180,240,300]))
        for selection_DR in selections_DR:
            for selection_prongjet in selections_prong:
                selection = selection_DR['selection']+selection_prongjet['selection']
                #hists['Tau1_pt'][sample + '_%s_%s'%(selection_DR['name'],selection_prongjet['name'])]= Hist('TH1F', sample=sample, var=['Tau1_pt'], binning=[30,35,40,50,60,80,100,130], sel=selection, wt)
                #hists['Tau1_pt'][sample + '_%s_%s'%(selection_DR['name'],selection_prongjet['name'])]= Hist('TH1F', sample=sample, var=['Tau1_pt'], binning=(10,30,130), sel=selection, wt=weight)
                hists['Tau1_pt'][sample + '_%s_%s'%(selection_DR['name'],selection_prongjet['name'])]= Hist('TH1F', sample=sample, var=['Tau1_pt'], binning=[30,40,50,60,70,80,100,130], sel=selection, wt=weight)
                hists['transverse_mass_lepmet'][sample + '_%s_%s'%(selection_DR['name'],selection_prongjet['name'])]= Hist('TH1F', sample=sample, var=['transverse_mass_lepmet'], binning=(50,0,250), sel=selection, wt=weight)
                hists["2D"][sample + '_%s_%s'%(selection_DR['name'],selection_prongjet['name'])]= Hist('TH2F', sample=sample, var=["Tau1_pt","vis_mass"], binning=(6,array('d',[30,40,50,60,75,90,130]),5,array('d',[20,60,100,140,200,300])),sel=selection, wt=weight)
                #create emty histograms
                hists["2D"]['ST_%s_%s'%(selection_DR['name'],selection_prongjet['name'])]= Hist('TH2F', sample=sample, var=["Tau1_pt","vis_mass"], binning=(6,array('d',[30,40,50,60,75,90,130]),5,array('d',[20,60,100,140,200,300])), sel="isHtoMuTau && isHtoETau", wt=weight)
                hists["2D"]['TT_%s_%s'%(selection_DR['name'],selection_prongjet['name'])]= Hist('TH2F', sample=sample, var=["Tau1_pt","vis_mass"], binning=(6,array('d',[30,40,50,60,75,90,130]),5,array('d',[20,60,100,140,200,300])), sel="isHtoMuTau && isHtoETau", wt=weight)
                hists["2D"]['TT_%s_%s_true'%(selection_DR['name'],selection_prongjet['name'])]= Hist('TH2F', sample=sample, var=["Tau1_pt","vis_mass"], binning=(6,array('d',[30,40,50,60,75,90,130]),5,array('d',[20,60,100,140,200,300])), sel="isHtoMuTau && isHtoETau", wt=weight)
                hists["2D"]['DYJetscomb_%s_%s'%(selection_DR['name'],selection_prongjet['name'])]= Hist('TH2F', sample=sample, var=["Tau1_pt","vis_mass"], binning=(6,array('d',[30,40,50,60,75,90,130]),5,array('d',[20,60,100,140,200,300])), sel="isHtoMuTau && isHtoETau", wt=weight)
                hists["2D"]['WJetscomb_%s_%s'%(selection_DR['name'],selection_prongjet['name'])]= Hist('TH2F', sample=sample, var=["Tau1_pt","vis_mass"], binning=(6,array('d',[30,40,50,60,75,90,130]),5,array('d',[20,60,100,140,200,300])), sel="isHtoMuTau && isHtoETau", wt=weight)
                hists["2D"]['%s_%s'%(selection_DR['name'],selection_prongjet['name'])]= Hist('TH2F', sample=sample, var=["Tau1_pt","vis_mass"], binning=(6,array('d',[30,40,50,60,75,90,130]),5,array('d',[20,60,100,140,200,300])), sel="isHtoMuTau && isHtoETau", wt=weight)
                if 'DR_TT' in selection_DR['name'] or 'CR_TT' in selection_DR['name']:
                    hists['Tau1_pt'][sample + '_%s_%s_true'%(selection_DR['name'],selection_prongjet['name'])]= Hist('TH1F', sample=sample, var=['Tau1_pt'], binning=[30,40,50,60,70,80,100,130], sel=selection+'&& Tau1_genmatch!=6', wt=weight)
                    hists['transverse_mass_lepmet'][sample + '_%s_%s_true'%(selection_DR['name'],selection_prongjet['name'])]= Hist('TH1F', sample=sample, var=['transverse_mass_lepmet'], binning=(50,0,250), sel=selection+'&& Tau1_genmatch!=6', wt=weight)
                    hists["2D"][sample + '_%s_%s_true'%(selection_DR['name'],selection_prongjet['name'])]= Hist('TH2F', sample=sample, var=["Tau1_pt","vis_mass"], binning=(6,array('d',[30,40,50,60,75,90,130]),5,array('d',[20,60,100,140,200,300])), sel=selection+'&& Tau1_genmatch!=6', wt=weight)
                    
    MultiDraw(hists, samplesdir, getsamples(channel,ULtag,year,preVFP), 'tree', mt_cores=4)





hists = Node()
drawPlots(hists,year,channel,ULtag,preVFP)

hists_2D = hists["2D"]
for selection_DR in selections_DR:
        for selection_prongjet in selections_prong:
                hists_2D['ST_%s_%s'%(selection_DR['name'],selection_prongjet['name'])].Add(hists_2D['ST_t_channel_antitop_%s_%s'%(selection_DR['name'],selection_prongjet['name'])])
                hists_2D['ST_%s_%s'%(selection_DR['name'],selection_prongjet['name'])].Add(hists_2D['ST_t_channel_top_%s_%s'%(selection_DR['name'],selection_prongjet['name'])])
                hists_2D['TT_%s_%s'%(selection_DR['name'],selection_prongjet['name'])].Add(hists_2D['TTTo2L2Nu_%s_%s'%(selection_DR['name'],selection_prongjet['name'])])
                hists_2D['TT_%s_%s'%(selection_DR['name'],selection_prongjet['name'])].Add(hists_2D['TTToHadronic_%s_%s'%(selection_DR['name'],selection_prongjet['name'])])
                hists_2D['TT_%s_%s'%(selection_DR['name'],selection_prongjet['name'])].Add(hists_2D['TTToSemiLeptonic_%s_%s'%(selection_DR['name'],selection_prongjet['name'])])
                hists_2D['DYJetscomb_%s_%s'%(selection_DR['name'],selection_prongjet['name'])].Add(hists_2D['DYJets_%s_%s'%(selection_DR['name'],selection_prongjet['name'])])
                hists_2D['DYJetscomb_%s_%s'%(selection_DR['name'],selection_prongjet['name'])].Add(hists_2D['DY1Jets_%s_%s'%(selection_DR['name'],selection_prongjet['name'])])
                hists_2D['DYJetscomb_%s_%s'%(selection_DR['name'],selection_prongjet['name'])].Add(hists_2D['DY2Jets_%s_%s'%(selection_DR['name'],selection_prongjet['name'])])
                hists_2D['DYJetscomb_%s_%s'%(selection_DR['name'],selection_prongjet['name'])].Add(hists_2D['DY3Jets_%s_%s'%(selection_DR['name'],selection_prongjet['name'])])
                hists_2D['DYJetscomb_%s_%s'%(selection_DR['name'],selection_prongjet['name'])].Add(hists_2D['DY4Jets_%s_%s'%(selection_DR['name'],selection_prongjet['name'])])
                hists_2D['WJetscomb_%s_%s'%(selection_DR['name'],selection_prongjet['name'])].Add(hists_2D['WJets_%s_%s'%(selection_DR['name'],selection_prongjet['name'])])
                hists_2D['WJetscomb_%s_%s'%(selection_DR['name'],selection_prongjet['name'])].Add(hists_2D['W1Jets_%s_%s'%(selection_DR['name'],selection_prongjet['name'])])
                hists_2D['WJetscomb_%s_%s'%(selection_DR['name'],selection_prongjet['name'])].Add(hists_2D['W2Jets_%s_%s'%(selection_DR['name'],selection_prongjet['name'])])
                hists_2D['WJetscomb_%s_%s'%(selection_DR['name'],selection_prongjet['name'])].Add(hists_2D['W3Jets_%s_%s'%(selection_DR['name'],selection_prongjet['name'])])
                hists_2D['WJetscomb_%s_%s'%(selection_DR['name'],selection_prongjet['name'])].Add(hists_2D['W4Jets_%s_%s'%(selection_DR['name'],selection_prongjet['name'])])
                if 'DR_QCD' in selection_DR['name'] or 'CR_QCD' in selection_DR['name']:
                        hists_2D['%s_%s'%(selection_DR['name'],selection_prongjet['name'])].Add(hists_2D['data_obs_%s_%s'%(selection_DR['name'],selection_prongjet['name'])])
                        hists_2D['%s_%s'%(selection_DR['name'],selection_prongjet['name'])].Add(hists_2D['DYJetscomb_%s_%s'%(selection_DR['name'],selection_prongjet['name'])],-1)
                        hists_2D['%s_%s'%(selection_DR['name'],selection_prongjet['name'])].Add(hists_2D['WJetscomb_%s_%s'%(selection_DR['name'],selection_prongjet['name'])],-1)
                        hists_2D['%s_%s'%(selection_DR['name'],selection_prongjet['name'])].Add(hists_2D['TT_%s_%s'%(selection_DR['name'],selection_prongjet['name'])],-1)
                        hists_2D['%s_%s'%(selection_DR['name'],selection_prongjet['name'])].Add(hists_2D['ST_%s_%s'%(selection_DR['name'],selection_prongjet['name'])],-1)
                elif 'DR_W' in selection_DR['name'] or 'CR_W' in selection_DR['name']:
                        hists_2D['%s_%s'%(selection_DR['name'],selection_prongjet['name'])].Add(hists_2D['data_obs_%s_%s'%(selection_DR['name'],selection_prongjet['name'])])
                        hists_2D['%s_%s'%(selection_DR['name'],selection_prongjet['name'])].Add(hists_2D['DYJetscomb_%s_%s'%(selection_DR['name'],selection_prongjet['name'])],-1)
                        hists_2D['%s_%s'%(selection_DR['name'],selection_prongjet['name'])].Add(hists_2D['TT_%s_%s'%(selection_DR['name'],selection_prongjet['name'])],-1)
                        hists_2D['%s_%s'%(selection_DR['name'],selection_prongjet['name'])].Add(hists_2D['ST_%s_%s'%(selection_DR['name'],selection_prongjet['name'])],-1)
                elif 'DR_TT' in selection_DR['name'] or 'CR_TT' in selection_DR['name']:
                        hists_2D['TT_%s_%s_true'%(selection_DR['name'],selection_prongjet['name'])].Add(hists_2D['TTTo2L2Nu_%s_%s_true'%(selection_DR['name'],selection_prongjet['name'])])
                        hists_2D['TT_%s_%s_true'%(selection_DR['name'],selection_prongjet['name'])].Add(hists_2D['TTToHadronic_%s_%s_true'%(selection_DR['name'],selection_prongjet['name'])])
                        hists_2D['TT_%s_%s_true'%(selection_DR['name'],selection_prongjet['name'])].Add(hists_2D['TTToSemiLeptonic_%s_%s_true'%(selection_DR['name'],selection_prongjet['name'])])
                        hists_2D['%s_%s'%(selection_DR['name'],selection_prongjet['name'])].Add(hists_2D['data_obs_%s_%s'%(selection_DR['name'],selection_prongjet['name'])])
                        hists_2D['%s_%s'%(selection_DR['name'],selection_prongjet['name'])].Add(hists_2D['DYJetscomb_%s_%s'%(selection_DR['name'],selection_prongjet['name'])],-1)
                        hists_2D['%s_%s'%(selection_DR['name'],selection_prongjet['name'])].Add(hists_2D['WJetscomb_%s_%s'%(selection_DR['name'],selection_prongjet['name'])],-1)
                        hists_2D['%s_%s'%(selection_DR['name'],selection_prongjet['name'])].Add(hists_2D['ST_%s_%s'%(selection_DR['name'],selection_prongjet['name'])],-1)
                        hists_2D['%s_%s'%(selection_DR['name'],selection_prongjet['name'])].Add(hists_2D['TT_%s_%s_true'%(selection_DR['name'],selection_prongjet['name'])],-1)
                

fout = ROOT.TFile('root/ff_%s_%s%s%s_2D.root'%(channel,ULtag,year,preVFP), 'RECREATE')
NodeToTDir(fout, hists)
fout.Close()
