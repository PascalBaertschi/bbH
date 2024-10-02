import ROOT
from analysis import *
from argparse import ArgumentParser
import json
import utils
import sys
sys.path.insert(1, os.path.join(sys.path[0], '../..')) #to get file in parent directory
from xsections import xsection
from CorrectionTools.DYCorrection import *
from samplenames import getsamples

# import CombineHarvester.CombineTools.plotting as plot

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.TH1.AddDirectory(False)

parser = ArgumentParser()
parser.add_argument('-y', '--year',    dest='year', type=str, default='2018', action='store')
parser.add_argument('-c', '--channel', dest='channel', choices=['mutau','singlelep'], type=str, default='mutau', action='store',)
parser.add_argument('-p', '--preVFP',  dest='preVFP', action='store_const', const="_preVFP",default="")
parser.add_argument('-t', '--comb',  dest='UL2016comb', action='store_true',default=False)
args = parser.parse_args()

year = args.year
channel = args.channel
preVFP = args.preVFP
UL2016comb = args.UL2016comb
#LUMI        = 137190.

if year=="2016":
        preVFP="_comb"   #assume to use only preVFP+postVFP combined

           
if channel=="singlelep":
    selection = 'nMuons==1 && nTaus==0'
elif channel=="mutau":
    selection = 'isHtoMuTau && dimuon_veto==0 && electron_veto==0 && Mu1_charge*Tau1_charge==-1 && transverse_mass_lepmet > 80 && nBjets_m==0'
     


def drawPlots(hists,year,channel,preVFP):
    if UL2016comb:
        preVFP="_comb"
    for sample in getsamples(channel,"UL",year,preVFP):
        samplesdir = '/pnfs/psi.ch/cms/trivcat/store/user/pbaertsc/bbh/samples_UL%s%s/'%(year,preVFP)
        if sample=='data_obs':
            weight = '1.'
        elif sample=='WJets_NLO_incl':
            weight = 'EventWeight * LumiWeight * MuWeight * MuTriggerWeight  * wt_dy * wt_tt * wt_dy_nlo' 
        else:
            weight = 'EventWeight * LumiWeight * MuWeight * MuTriggerWeight  * wt_dy * wt_tt * wt_dy_nlo * wt_w_nlo' 
        hists["vis_pt"][sample]= Hist('TH1F', sample=sample, var=["vis_pt"], binning=(30,0.,200.), sel=selection, wt=weight)
        hists["vis_mass"][sample]= Hist('TH1F', sample=sample, var=["vis_mass"], binning=(30,50.,130.), sel=selection, wt=weight)
        hists["LHE_Vpt"][sample]= Hist('TH1F', sample=sample, var=["LHE_Vpt"], binning=(30,0.,200.), sel=selection, wt=weight)
        hists["Jet1_btag"][sample]= Hist('TH1F', sample=sample, var=["Jet1_btag"], binning=(30,0.,1.), sel=selection, wt=weight)
        hists["Jet1_pt"][sample]= Hist('TH1F', sample=sample, var=["Jet1_pt"], binning=(30,0.,200.), sel=selection, wt=weight)
        hists["Jet2_btag"][sample]= Hist('TH1F', sample=sample, var=["Jet2_btag"], binning=(30,0.,1.), sel=selection, wt=weight)
        hists["Jet2_pt"][sample]= Hist('TH1F', sample=sample, var=["Jet2_pt"], binning=(30,0.,150.), sel=selection, wt=weight)
        hists["MET"][sample]= Hist('TH1F', sample=sample, var=["MET"], binning=(30,0.,150.), sel=selection, wt=weight)
        hists["collinear_mass"][sample]= Hist('TH1F', sample=sample, var=["collinear_mass"], binning=(30,0.,250.), sel=selection, wt=weight)
        hists["vistauJ_mass"][sample]= Hist('TH1F', sample=sample, var=["vistauJ_mass"], binning=(30,0.,300.), sel=selection, wt=weight)
        hists["TauJ_mass"][sample]= Hist('TH1F', sample=sample, var=["TauJ_mass"], binning=(30,0.,300.), sel=selection, wt=weight)
        hists["HJ_pt"][sample]= Hist('TH1F', sample=sample, var=["HJ_pt"], binning=(30,0.,200.), sel=selection, wt=weight)
        hists["H_pt"][sample]= Hist('TH1F', sample=sample, var=["H_pt"], binning=(30,0.,300.), sel=selection, wt=weight)
        hists["DRHJ"][sample]= Hist('TH1F', sample=sample, var=["DRHJ"], binning=(30,0.,5.), sel=selection, wt=weight)
        hists["dijet_pt"][sample]= Hist('TH1F', sample=sample, var=["dijet_pt"], binning=(30,0.,200.), sel=selection, wt=weight)
        hists["DRHJ2"][sample]= Hist('TH1F', sample=sample, var=["DRHJ2"], binning=(30,0.,5.), sel=selection, wt=weight)
        hists["dijet_mass"][sample]= Hist('TH1F', sample=sample, var=["dijet_mass"], binning=(30,0.,200.), sel=selection, wt=weight)
        hists["DEta"][sample]= Hist('TH1F', sample=sample, var=["DEta"], binning=(30,0.,5.), sel=selection, wt=weight)
        hists["transverse_mass_total"][sample]= Hist('TH1F', sample=sample, var=["transverse_mass_total"], binning=(30,0.,200.), sel=selection, wt=weight)
        hists["DPhiLepMET"][sample]= Hist('TH1F', sample=sample, var=["DPhiLepMET"], binning=(30,-5.,5.), sel=selection, wt=weight)
        hists["vistau1_eta"][sample]= Hist('TH1F', sample=sample, var=["vistau1_eta"], binning=(30,-2.5,2.5), sel=selection, wt=weight)
        hists["DEtaLepJ"][sample]= Hist('TH1F', sample=sample, var=["DEtaLepJ"], binning=(30,0.,4.), sel=selection, wt=weight)
        hists["DPhi"][sample]= Hist('TH1F', sample=sample, var=["DPhi"], binning=(30,-5.,5.), sel=selection, wt=weight)
        hists["DEtaTauJ2"][sample]= Hist('TH1F', sample=sample, var=["DEtaTauJ2"], binning=(30,0.,4.), sel=selection, wt=weight)
        hists["vistau1_pt"][sample]= Hist('TH1F', sample=sample, var=["vistau1_pt"], binning=(30,0.,150.), sel=selection, wt=weight)
        hists["Dzeta"][sample]= Hist('TH1F', sample=sample, var=["Dzeta"], binning=(30,-100.,100.), sel=selection, wt=weight)
        hists["Jet3_pt"][sample]= Hist('TH1F', sample=sample, var=["Jet3_pt"], binning=(30,0.,150.), sel=selection, wt=weight)
    MultiDraw(hists, samplesdir, getsamples(channel,"UL",year,preVFP), 'tree', mt_cores=4)




hists = Node()
drawPlots(hists,year,channel,preVFP)


for path, node in hists.ListNodes(withObjects=True):
    print('>> %s' % path)
    node['TT'] = node['TTTo2L2Nu'] + node['TTToHadronic'] + node['TTToSemiLeptonic']
    node['DYJetscomb_NLO'] = node['DYJets_NLO'] + node['DYJets_0J'] + node['DYJets_1J'] + node['DYJets_2J']
    node['ST'] = node['ST_t_channel_antitop'] + node['ST_t_channel_top'] + node['ST_s_channel'] + node['ST_tW_antitop'] + node['ST_tW_top']
    node['data_obs'] = node['data_obs'] - node['TT']- node['DYJetscomb_NLO'] - node['ST']


fout = ROOT.TFile('root/%s_UL%s.root'%(channel,year), 'RECREATE')
NodeToTDir(fout, hists)
fout.Close()
