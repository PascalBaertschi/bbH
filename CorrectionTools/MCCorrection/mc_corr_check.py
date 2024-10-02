import ROOT
from analysis import *
from argparse import ArgumentParser
import json
import utils
import sys
sys.path.insert(1, os.path.join(sys.path[0], '../..')) #to get file in parent directory
from xsections import xsection
from CorrectionTools.MCCorrection import *
from samplenames import getsamples

# import CombineHarvester.CombineTools.plotting as plot

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.TH1.AddDirectory(False)

parser = ArgumentParser()
parser.add_argument('-y', '--year',    dest='year', type=str, default='2018', action='store')
parser.add_argument('-c', '--channel', dest='channel', choices=['mumu','tt','mutau','etau'], type=str, default='mumu', action='store',)
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

           
MCCorrection = MCCorrection(year,"NLO") #need to first derive tt correction weight
tt_weight = MCCorrection.getWeight_tt()



def drawPlots(hists,year,channel,preVFP):
    if UL2016comb:
        preVFP="_comb"
    for sample in getsamples(channel,"UL",year,preVFP):
        samplesdir = '/pnfs/psi.ch/cms/trivcat/store/user/pbaertsc/bbh/samples_UL%s%s/'%(year,preVFP)
        if channel=="mumu":
            selection = 'isMuMu && nBjets_m>0'
            selection_1btag = 'isMuMu && nJets==0'
            selection_2btag = 'isMuMu && nBjets_m==0'
            selection_nobcut = 'isMuMu'
        elif channel=="tt":
            selection = 'isTTCR && nBjets_m>0 && Dzeta < -35.'
            selection_nobcut = 'isTTCR && Dzeta < -35.'
        elif channel=="mutau":
            selection = "isHtoMuTau && dimuon_veto==0 && electron_veto==0 && extra_muon_veto==0 && Mu1_charge*Tau1_charge==-1 && transverse_mass_lepmet > 80 && nBjets_m==0" #for correction of W+Jets sample
            if "WJets" in sample:
                selection_nobcut = "isHtoMuTau && Mu1_charge*Tau1_charge==-1 && dimuon_veto==0 && electron_veto==0 && extra_muon_veto==0 && transverse_mass_lepmet>80" #use MCcorr and ff derivation selection for W+Jets sample
            else:
                selection_nobcut = "isHtoMuTau && Mu1_charge*Tau1_charge==-1 && dimuon_veto==0 && electron_veto==0 && extra_muon_veto==0 && Tau1_genmatch!=6 && transverse_mass_lepmet<60"
        elif channel=="etau":
            selection = "isHtoETau && dielectron_veto==0 && muon_veto==0 && extra_electron_veto==0 && Ele1_charge*Tau1_charge==-1 && transverse_mass_lepmet > 80 && nBjets_m==0" #for correction of W+Jets sample
            if "WJets" in sample:
                selection_nobcut = "isHtoETau && Ele1_charge*Tau1_charge==-1 && dielectron_veto==0 && muon_veto==0 && extra_electron_veto==0 && transverse_mass_lepmet>80" #use MCcorr and ff derivation selection for W+Jets sample
            else:
                selection_nobcut = "isHtoETau && Ele1_charge*Tau1_charge==-1 && dielectron_veto==0 && muon_veto==0 && extra_electron_veto==0 && Tau1_genmatch!=6 && transverse_mass_lepmet<60"

        if sample=='data_obs':
            weight = '1.'
            weight_btagSF = '1.'
            weight_nobtagSF = '1.'
        else:
            if channel=="mumu":
                if "TT" in sample:
                    weight = 'EventWeight * LumiWeight * BTagWeight * PUIdWeight * MuWeight * MuTriggerWeight * wt_dy_nlo * wt_w_nlo *%s * wt_tt_pt'%tt_weight #weights include both muons
                    weight_btagSF = 'EventWeight * LumiWeight * BTagWeight_nocorr * PUIdWeight * MuWeight * MuTriggerWeight * wt_dy_nlo * wt_w_nlo * wt_tt_pt'
                    weight_nobtagSF = 'EventWeight * LumiWeight * PUIdWeight * MuWeight * MuTriggerWeight * wt_dy_nlo * wt_w_nlo * wt_tt_pt'
                else:
                    weight = 'EventWeight * LumiWeight * BTagWeight * PUIdWeight * MuWeight * MuTriggerWeight * wt_dy_nlo * wt_w_nlo' #weights include both muons 
                    weight_nostitch = 'EventWeight * LumiWeight * BTagWeight * PUIdWeight * MuWeight * MuTriggerWeight'
                    weight_btagSF = 'EventWeight * LumiWeight * BTagWeight_nocorr * PUIdWeight * MuWeight * MuTriggerWeight * wt_dy_nlo * wt_w_nlo'
                    weight_nobtagSF = 'EventWeight * LumiWeight * PUIdWeight * MuWeight * MuTriggerWeight * wt_dy_nlo * wt_w_nlo'
            elif channel=="tt":
                if "TT" in sample:
                    weight = 'EventWeight * LumiWeight * BTagWeight * PUIdWeihgt * MuWeight * MuTriggerWeight * EWeight * wt_dy_nlo * wt_w_nlo * wt_tt_pt' #MuTriggerWeight includes SingleElectron trigger   
                    weight_btagSF = 'EventWeight * LumiWeight * BTagWeight_nocorr * PUIdWeight * MuWeight * MuTriggerWeight * EWeight * wt_dy_nlo * wt_w_nlo * wt_tt_pt'
                    weight_nobtagSF = 'EventWeight * LumiWeight * PUIdWeight * MuWeight * MuTriggerWeight * EWeight * wt_dy_nlo * wt_w_nlo * wt_tt_pt'
                    #weight = 'EventWeight * LumiWeight * BTagWeight * MuWeight * MuTriggerWeight * EWeight * wt_dy_nlo * wt_w_nlo' #MuTriggerWeight includes SingleElectron trigger   
                    #weight_btagSF = 'EventWeight * LumiWeight * BTagWeight_nocorr * MuWeight * MuTriggerWeight * EWeight * wt_dy_nlo * wt_w_nlo'
                    #weight_nobtagSF = 'EventWeight * LumiWeight * MuWeight * MuTriggerWeight * EWeight * wt_dy_nlo * wt_w_nlo'    
                else:
                    weight = 'EventWeight * LumiWeight * BTagWeight * PUIdWeight * MuWeight * MuTriggerWeight * EWeight * wt_dy_nlo * wt_w_nlo' #MuTriggerWeight includes SingleElectron trigger   
                    weight_btagSF = 'EventWeight * LumiWeight * BTagWeight_nocorr * PUIdWeight * MuWeight * MuTriggerWeight * EWeight * wt_dy_nlo * wt_w_nlo'
                    weight_nobtagSF = 'EventWeight * LumiWeight * PUIdWeight * MuWeight * MuTriggerWeight * EWeight * wt_dy_nlo * wt_w_nlo' 
            elif channel=="mutau":
                if "TT" in sample:
                    weight = 'EventWeight * LumiWeight * BTagWeight * PUIdWeight * MuWeight * MuTriggerWeight * TauWeight * %s * wt_dy * wt_dy_nlo * wt_w_nlo * wt_tt_pt'%tt_weight  #no wt_w because this will be derived
                    weight_nostitch = 'EventWeight * LumiWeight * BTagWeight * PUIdWeight * MuWeight * MuTriggerWeight * TauWeight * %s * wt_dy * wt_tt_pt'%tt_weight
                    weight_btagSF = 'EventWeight * LumiWeight * BTagWeight_nocorr * PUIdWeight * MuWeight * MuTriggerWeight * TauWeight * wt_dy_nlo * wt_w_nlo * wt_tt_pt'  
                    weight_nobtagSF = 'EventWeight * LumiWeight * PUIdWeight * MuWeight * MuTriggerWeight * TauWeight * wt_dy_nlo * wt_w_nlo * wt_tt_pt'  
                else:
                    weight = 'EventWeight * LumiWeight * BTagWeight * PUIdWeight * MuWeight * MuTriggerWeight * TauWeight * wt_dy * wt_dy_nlo * wt_w_nlo'  #no wt_w because this will be derived
                    weight_nostitch = 'EventWeight * LumiWeight * BTagWeight * PUIdWeight * MuWeight * MuTriggerWeight * TauWeight * wt_dy'
                    weight_btagSF = 'EventWeight * LumiWeight * BTagWeight_nocorr * PUIdWeight * MuWeight * MuTriggerWeight * TauWeight * wt_dy_nlo * wt_w_nlo'  
                    weight_nobtagSF = 'EventWeight * LumiWeight * PUIdWeight * MuWeight * MuTriggerWeight * TauWeight * wt_dy_nlo * wt_w_nlo'   
            elif channel=="etau":
                if "TT" in sample:
                    weight = 'EventWeight * LumiWeight * BTagWeight * PUIdWeight * EWeight * ETriggerWeight * TauWeight * %s * wt_dy * wt_dy_nlo * wt_w_nlo * wt_tt_pt'%tt_weight #no wt_w because this will be derived
                    weight_nostitch = 'EventWeight * LumiWeight * BTagWeight * PUIdWeight * EWeight * ETriggerWeight * TauWeight * %s * wt_dy * wt_tt_pt'%tt_weight
                    weight_btagSF = 'EventWeight * LumiWeight * BTagWeight_nocorr * PUIdWeight * EWeight * ETriggerWeight * TauWeight * wt_dy_nlo * wt_w_nlo * wt_tt_pt' 
                    weight_nobtagSF = 'EventWeight * LumiWeight * PUIdWeight * EWeight * ETriggerWeight * TauWeight * wt_dy_nlo * wt_w_nlo * wt_tt_pt'
                else:
                    weight = 'EventWeight * LumiWeight * BTagWeight * PUIdWeight * EWeight * ETriggerWeight * TauWeight * wt_dy * wt_dy_nlo * wt_w_nlo' #no wt_w because this will be derived
                    weight_nostitch = 'EventWeight * LumiWeight * BTagWeight * PUIdWeight * EWeight * ETriggerWeight * TauWeight * wt_dy'
                    weight_btagSF = 'EventWeight * LumiWeight * BTagWeight_nocorr * PUIdWeight * EWeight * ETriggerWeight * TauWeight * wt_dy_nlo * wt_w_nlo' 
                    weight_nobtagSF = 'EventWeight * LumiWeight * PUIdWeight * EWeight * ETriggerWeight * TauWeight * wt_dy_nlo * wt_w_nlo'
        hists["2D"][sample]= Hist('TH2F', sample=sample, var=["vis_pt","vis_mass"], binning=(20,0.,200.,16,50.,130.), sel=selection, wt=weight)
        if channel=="mumu":
                #hists["2D_1btag"][sample]= Hist('TH2F', sample=sample, var=["vis_pt","vis_mass"], binning=(20,0.,200.,16,50.,130.), sel=selection_1btag, wt=weight)
                #hists["2D_2btag"][sample]= Hist('TH2F', sample=sample, var=["vis_pt","vis_mass"], binning=(20,0.,200.,16,50.,130.), sel=selection_2btag, wt=weight)
                #hists["vis_pt_1btag"][sample]= Hist('TH1F', sample=sample, var=["vis_pt"], binning=(20,0.,200.), sel=selection_1btag, wt=weight)
                #hists["vis_pt_2btag"][sample]= Hist('TH1F', sample=sample, var=["vis_pt"], binning=(20,0.,200.), sel=selection_2btag, wt=weight)
                #hists["vis_mass_1btag"][sample]= Hist('TH1F', sample=sample, var=["vis_mass"], binning=(16,50.,130.), sel=selection_1btag, wt=weight)
                #hists["vis_mass_2btag"][sample]= Hist('TH1F', sample=sample, var=["vis_mass"], binning=(16,50.,130.), sel=selection_2btag, wt=weight)
                bins_pt = [0.,10.,20.,30.,40.,50.,60.,70.,90.,110.,150.,200.]
                bins_mass = [50.,70.,80.,85.,90.,95.,100.,110.,130.]
                hists["2D_1btag"][sample]= Hist('TH2F', sample=sample, var=["vis_pt","vis_mass"], binning=(11,np.array(bins_pt),8,np.array(bins_mass)), sel=selection_1btag, wt=weight)
                hists["2D_2btag"][sample]= Hist('TH2F', sample=sample, var=["vis_pt","vis_mass"], binning=(11,np.array(bins_pt),8,np.array(bins_mass)), sel=selection_2btag, wt=weight)
                hists["vis_pt_1btag"][sample]= Hist('TH1F', sample=sample, var=["vis_pt"], binning=bins_pt, sel=selection_1btag, wt=weight)
                hists["vis_pt_2btag"][sample]= Hist('TH1F', sample=sample, var=["vis_pt"], binning=bins_pt, sel=selection_2btag, wt=weight)
                hists["vis_mass_1btag"][sample]= Hist('TH1F', sample=sample, var=["vis_mass"], binning=bins_mass, sel=selection_1btag, wt=weight)
                hists["vis_mass_2btag"][sample]= Hist('TH1F', sample=sample, var=["vis_mass"], binning=bins_mass, sel=selection_2btag, wt=weight)
                #####################3
                hists["Mu1_pt_1btag"][sample]= Hist('TH1F', sample=sample, var=["Mu1_pt"], binning=[30,40,50,60,70,80,100,130], sel=selection_1btag, wt=weight)
                hists["Mu1_pt_2btag"][sample]= Hist('TH1F', sample=sample, var=["Mu1_pt"], binning=[30,40,50,60,70,80,100,130], sel=selection_2btag, wt=weight)
                hists["Mu2_pt_1btag"][sample]= Hist('TH1F', sample=sample, var=["Mu2_pt"], binning=[30,40,50,60,70,80,100,130], sel=selection_1btag, wt=weight)
                hists["Mu2_pt_2btag"][sample]= Hist('TH1F', sample=sample, var=["Mu2_pt"], binning=[30,40,50,60,70,80,100,130], sel=selection_2btag, wt=weight)
                hists["Mu1_eta_1btag"][sample]= Hist('TH1F', sample=sample, var=["Mu1_eta"], binning=(40,-2.5,2.5), sel=selection_1btag, wt=weight)
                hists["Mu2_eta_1btag"][sample]= Hist('TH1F', sample=sample, var=["Mu2_eta"], binning=(40,-2.5,2.5), sel=selection_1btag, wt=weight)
                hists["Mu1_eta_2btag"][sample]= Hist('TH1F', sample=sample, var=["Mu1_eta"], binning=(40,-2.5,2.5), sel=selection_2btag, wt=weight)
                hists["Mu2_eta_2btag"][sample]= Hist('TH1F', sample=sample, var=["Mu2_eta"], binning=(40,-2.5,2.5), sel=selection_2btag, wt=weight)
                if "DYJets" in sample:
                        hists["LHE_Vpt"][sample+"_nostitch"]= Hist('TH1F', sample=sample, var=["LHE_Vpt"], binning=(30,20.,150.), sel=selection, wt=weight_nostitch)
        elif channel=="mutau" or channel=="etau":
                if "WJets" in sample:
                        hists["LHE_Vpt"][sample+"_nostitch"]= Hist('TH1F', sample=sample, var=["LHE_Vpt"], binning=(30,20.,150.), sel=selection, wt=weight_nostitch)
                        hists["vis_pt"][sample+"_nostitch"]= Hist('TH1F', sample=sample, var=["vis_pt"], binning=(20,0.,200.), sel=selection, wt=weight_nostitch)
                        hists["vis_mass"][sample+"_nostitch"]= Hist('TH1F', sample=sample, var=["vis_mass"], binning=(16,50.,130.), sel=selection, wt=weight_nostitch)
        hists["vis_pt"][sample]= Hist('TH1F', sample=sample, var=["vis_pt"], binning=(20,0.,200.), sel=selection, wt=weight)
        hists["vis_mass"][sample]= Hist('TH1F', sample=sample, var=["vis_mass"], binning=(16,50.,130.), sel=selection, wt=weight)
        hists["Tau1_pt"][sample]= Hist('TH1F', sample=sample, var=["Tau1_pt"], binning=[30,40,50,60,70,80,100,130], sel=selection, wt=weight)
        hists["LHE_Vpt"][sample]= Hist('TH1F', sample=sample, var=["LHE_Vpt"], binning=(30,20.,150.), sel=selection, wt=weight)
        hists["Jet1_pt"][sample]= Hist('TH1F', sample=sample, var=["Jet1_pt"], binning=(40,0.,200.), sel=selection, wt=weight)
        hists["Jet1_btag"][sample]= Hist('TH1F', sample=sample, var=["Jet1_btag"], binning=(40,0.,1.), sel=selection, wt=weight)
        hists["Jet1_eta"][sample]= Hist('TH1F', sample=sample, var=["Jet1_eta"], binning=(40,-2.5,2.5), sel=selection, wt=weight)
        hists["Jet1_phi"][sample]= Hist('TH1F', sample=sample, var=["Jet1_phi"], binning=(40,-3.2,3.2), sel=selection, wt=weight)
        hists["Jet1_mass"][sample]= Hist('TH1F', sample=sample, var=["Jet1_mass"], binning=(40,0.,10.), sel=selection, wt=weight)
        hists["Jet2_pt"][sample]= Hist('TH1F', sample=sample, var=["Jet2_pt"], binning=(40,0.,200.), sel=selection, wt=weight)
        hists["Jet2_btag"][sample]= Hist('TH1F', sample=sample, var=["Jet2_btag"], binning=(40,0.,1.), sel=selection, wt=weight)
        hists["Jet2_eta"][sample]= Hist('TH1F', sample=sample, var=["Jet2_eta"], binning=(40,-2.5,2.5), sel=selection, wt=weight)
        hists["Jet2_phi"][sample]= Hist('TH1F', sample=sample, var=["Jet2_phi"], binning=(40,-3.2,3.2), sel=selection, wt=weight)
        hists["Jet2_mass"][sample]= Hist('TH1F', sample=sample, var=["Jet2_mass"], binning=(40,0.,10.), sel=selection, wt=weight)
        hists["H_mass"][sample]= Hist('TH1F', sample=sample, var=["H_mass"], binning=(40,0.,200.), sel=selection, wt=weight)
        hists["MET"][sample]= Hist('TH1F', sample=sample, var=["MET"], binning=(40,0.,150.), sel=selection, wt=weight)
        hists["MET_chs"][sample]= Hist('TH1F', sample=sample, var=["MET_chs"], binning=(40,0.,150.), sel=selection, wt=weight)
        hists["MET_covXX"][sample]= Hist('TH1F', sample=sample, var=["MET_covXX"], binning=(40,0.,200.), sel=selection, wt=weight)
        hists["MET_covXY"][sample]= Hist('TH1F', sample=sample, var=["MET_covXY"], binning=(40,-150.,150.), sel=selection, wt=weight)
        hists["MET_covYY"][sample]= Hist('TH1F', sample=sample, var=["MET_covYY"], binning=(40,0.,300.), sel=selection, wt=weight)
        hists["Dzeta"][sample]= Hist('TH1F', sample=sample, var=["Dzeta"], binning=(40,-100.,100.), sel=selection, wt=weight)
        hists["H_pt"][sample]= Hist('TH1F', sample=sample, var=["H_pt"], binning=(40,0.,300.), sel=selection, wt=weight)
        hists["vistauJ_mass"][sample]= Hist('TH1F', sample=sample, var=["vistauJ_mass"], binning=(40,0.,200.), sel=selection, wt=weight)
        hists["DRHJ"][sample]= Hist('TH1F', sample=sample, var=["DRHJ"], binning=(40,0.,5.), sel=selection, wt=weight)
        hists["TauJ_mass"][sample]= Hist('TH1F', sample=sample, var=["TauJ_mass"], binning=(40,0.,200.), sel=selection, wt=weight)
        hists["HJ_pt"][sample]= Hist('TH1F', sample=sample, var=["HJ_pt"], binning=(40,0.,200.), sel=selection, wt=weight)
        hists["DEta"][sample]= Hist('TH1F', sample=sample, var=["DEta"], binning=(40,0.,5.), sel=selection, wt=weight)
        hists["dijet_pt"][sample]= Hist('TH1F', sample=sample, var=["dijet_pt"], binning=(40,0.,200.), sel=selection, wt=weight)
        hists["transverse_mass_total"][sample]= Hist('TH1F', sample=sample, var=["transverse_mass_total"], binning=(40,0.,300.), sel=selection, wt=weight)
        hists["DRHJ2"][sample]= Hist('TH1F', sample=sample, var=["DRHJ2"], binning=(40,0.,5.), sel=selection, wt=weight)
        hists["Jet3_pt"][sample]= Hist('TH1F', sample=sample, var=["Jet3_pt"], binning=(40,0.,200.), sel=selection, wt=weight)
        hists["dijet_mass"][sample]= Hist('TH1F', sample=sample, var=["dijet_mass"], binning=(40,0.,200.), sel=selection, wt=weight)
        hists["DPhiLepMET"][sample]= Hist('TH1F', sample=sample, var=["DPhiLepMET"], binning=(40,-5.,5.), sel=selection, wt=weight)
        hists["DPhi"][sample]= Hist('TH1F', sample=sample, var=["DPhi"], binning=(40,-5.,5.), sel=selection, wt=weight)
        hists["DEtaTauJ2"][sample]= Hist('TH1F', sample=sample, var=["DEtaTauJ2"], binning=(40,0.,4.), sel=selection, wt=weight)
        hists["DEtaLepJ"][sample]= Hist('TH1F', sample=sample, var=["DEtaLepJ"], binning=(40,0.,4.), sel=selection, wt=weight)
        hists["DEta_jets"][sample]= Hist('TH1F', sample=sample, var=["DEta_jets"], binning=(40,0.,4.), sel=selection, wt=weight)
        hists["DPhi_jets"][sample]= Hist('TH1F', sample=sample, var=["DPhi_jets"], binning=(40,-5.,5.), sel=selection, wt=weight)
        hists["DRjets"][sample]= Hist('TH1F', sample=sample, var=["DRjets"], binning=(40,0.,5.), sel=selection, wt=weight)
        hists["Jet1_pt"][sample + '_btagSF']= Hist('TH1F', sample=sample, var=["Jet1_pt"], binning=(40,0.,200.), sel=selection_nobcut, wt=weight_btagSF)
        hists["Jet1_btag"][sample + '_btagSF']= Hist('TH1F', sample=sample, var=["Jet1_btag"], binning=(40,0.,1.), sel=selection_nobcut, wt=weight_btagSF)
        hists["Jet1_eta"][sample + '_btagSF']= Hist('TH1F', sample=sample, var=["Jet1_eta"], binning=(40,-2.5,2.5), sel=selection_nobcut, wt=weight_btagSF)
        hists["Jet1_phi"][sample + '_btagSF']= Hist('TH1F', sample=sample, var=["Jet1_phi"], binning=(40,-3.2,3.2), sel=selection_nobcut, wt=weight_btagSF)
        hists["Jet1_mass"][sample + '_btagSF']= Hist('TH1F', sample=sample, var=["Jet1_mass"], binning=(40,0.,10.), sel=selection_nobcut, wt=weight_btagSF)
        hists["Jet1_pt"][sample + '_nobtagSF']= Hist('TH1F', sample=sample, var=["Jet1_pt"], binning=(40,0.,200.), sel=selection_nobcut, wt=weight_nobtagSF)
        hists["Jet1_btag"][sample + '_nobtagSF']= Hist('TH1F', sample=sample, var=["Jet1_btag"], binning=(40,0.,1.), sel=selection_nobcut, wt=weight_nobtagSF)
        hists["Jet1_eta"][sample + '_nobtagSF']= Hist('TH1F', sample=sample, var=["Jet1_eta"], binning=(40,-2.5,2.5), sel=selection_nobcut, wt=weight_nobtagSF)
        hists["Jet1_phi"][sample + '_nobtagSF']= Hist('TH1F', sample=sample, var=["Jet1_phi"], binning=(40,-3.2,3.2), sel=selection_nobcut, wt=weight_nobtagSF)
        hists["Jet1_mass"][sample + '_nobtagSF']= Hist('TH1F', sample=sample, var=["Jet1_mass"], binning=(40,0.,10.), sel=selection_nobcut, wt=weight_nobtagSF)
    MultiDraw(hists, samplesdir, getsamples(channel,"UL",year,preVFP), 'tree', mt_cores=4)




hists = Node()
drawPlots(hists,year,channel,preVFP)
if channel=="mumu":
    hists_2D = hists["2D"]
    hists_2D["DYJets_incl"].Add(hists_2D["DYJets_0J"])
    hists_2D["DYJets_incl"].Add(hists_2D["DYJets_1J"])
    hists_2D["DYJets_incl"].Add(hists_2D["DYJets_2J"])
    hists_2D["data_obs"].Add(hists_2D["TTTo2L2Nu"],-1)
    hists_2D["data_obs"].Add(hists_2D["TTToSemiLeptonic"],-1)
    hists_2D["data_obs"].Add(hists_2D["TTToHadronic"],-1)
    hists_2D_1btag = hists["2D_1btag"]
    hists_2D_1btag["DYJets_incl"].Add(hists_2D_1btag["DYJets_0J"])
    hists_2D_1btag["DYJets_incl"].Add(hists_2D_1btag["DYJets_1J"])
    hists_2D_1btag["DYJets_incl"].Add(hists_2D_1btag["DYJets_2J"])
    hists_2D_1btag["data_obs"].Add(hists_2D_1btag["TTTo2L2Nu"],-1)
    hists_2D_1btag["data_obs"].Add(hists_2D_1btag["TTToSemiLeptonic"],-1)
    hists_2D_1btag["data_obs"].Add(hists_2D_1btag["TTToHadronic"],-1)
    hists_2D_2btag = hists["2D_2btag"]
    hists_2D_2btag["DYJets_incl"].Add(hists_2D_2btag["DYJets_0J"])
    hists_2D_2btag["DYJets_incl"].Add(hists_2D_2btag["DYJets_1J"])
    hists_2D_2btag["DYJets_incl"].Add(hists_2D_2btag["DYJets_2J"])
    hists_2D_2btag["data_obs"].Add(hists_2D_2btag["TTTo2L2Nu"],-1)
    hists_2D_2btag["data_obs"].Add(hists_2D_2btag["TTToSemiLeptonic"],-1)
    hists_2D_2btag["data_obs"].Add(hists_2D_2btag["TTToHadronic"],-1)

# Loop through all nodes (just the ones containing TH1s)
for path, node in hists.ListNodes(withObjects=True):
    print('>> %s' % path)
    if path in ["2D","2D_1btag","2D_2btag"]:
        continue
    node['ST'] = node['ST_t_channel_antitop'] + node['ST_t_channel_top'] + node['ST_s_channel'] + node['ST_tW_antitop'] + node['ST_tW_top']
    node['TT'] = node['TTTo2L2Nu'] + node['TTToHadronic'] + node['TTToSemiLeptonic']
    node['DYJets'] = node['DYJets_incl'] + node['DYJets_0J'] + node['DYJets_1J'] + node['DYJets_2J']
    node['WJets'] = node['WJets_incl'] + node['WJets_0J'] + node['WJets_1J'] + node['WJets_2J']
    node['VV'] = node['WWTo2L2Nu'] + node['WWTo1L1Nu2Q'] + node['WWTo4Q'] + node['WZTo3LNu'] + node['WZTo2L2Q'] + node['WZTo1L3Nu'] + node['WZTo1L1Nu2Q'] + node['ZZTo4L'] + node['ZZTo2L2Q'] + node['ZZTo2Nu2Q']
    if channel=="mumu":
        node['dataMinusMC'] = node['data_obs']-node['TT']-node['ST']   
    elif channel=="mutau" or channel=="etau":
        node['dataMinusMC'] = node['data_obs']-node['TT']-node['ST']-node['DYJets']-node['VV']
    elif channel=="tt":
        node['dataMinusMC'] = node['data_obs']-node['ST']-node['DYJets']-node['WJets']-node['VV']

fout = ROOT.TFile('root/%s_UL%s_check.root'%(channel,year), 'RECREATE')
NodeToTDir(fout, hists)
fout.Close()
