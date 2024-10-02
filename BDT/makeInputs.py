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
from samplenames import getsamples

parser = ArgumentParser()

parser.add_argument('-c', '--channel', dest='channel', type=str, default='mutau', action='store',)
parser.add_argument('-y', '--year',    dest='year', type=str, default='2018', action='store')
parser.add_argument('-n', '--NN',      dest='NN', action='store_true',default=False)
parser.add_argument('-p', '--preVFP',  dest='preVFP', action='store_const', const="_preVFP",default="")
parser.add_argument('-t', '--comb',  dest='UL2016comb', action='store_true',default=False)
args = parser.parse_args()


year = args.year
channel = args.channel
NN = args.NN
UL2016comb = args.UL2016comb
preVFP = args.preVFP
outdir = "/work/pbaertsc/bbh/NanoTreeProducer/BDT/root/"


if year=="2016":
    preVFP="_comb"

mc_samples = ['TTTo2L2Nu','TTToHadronic','TTToSemiLeptonic','bbH_htt','ggH_bb_htt_inc','ggH_bb_htt_excl','DYJets_incl','DYJets_0J','DYJets_1J','DYJets_2J'] #intH_bb_htt
#mc_samples = ['TTTo2L2Nu','TTToHadronic','TTToSemiLeptonic','bbH_htt','ggH_bb_htt_inc','ggH_bb_htt_excl','DYJets_incl','DYJets_0J','DYJets_1J','DYJets_2J','bbH_nobb_htt','ggH_htt_excl','ggH_htt_inc'] 

#not used: bbH_nobb_htt. ggH_htt_excl, ggH_htt_inc
#not used samples: WJets','W1Jets','W2Jets','W3Jets','W4Jets','ST_t_channel_antitop','ST_t_channel_top','ST_s_channel','ST_tW_antitop','ST_tW_top','VBF','ZH','ggF','ggF_ext','JJH','ttH'


signal_chain_train = TChain("tree")
bbh_chain_train = TChain("tree")
ggh_chain_train = TChain("tree")
#jjh_chain_train = TChain("tree")
tt_chain_train = TChain("tree")
dy_chain_train = TChain("tree")
bkg_chain_train = TChain("tree")
#fake_chain_train = TChain("tree")
st_chain_train = TChain("tree")
vv_chain_train = TChain("tree")
ggf_chain_train = TChain("tree")
signal_chain_test = TChain("tree")
bbh_chain_test = TChain("tree")
ggh_chain_test = TChain("tree")
#jjh_chain_test = TChain("tree")
tt_chain_test = TChain("tree")
dy_chain_test = TChain("tree")
bkg_chain_test = TChain("tree")
#fake_chain_test = TChain("tree")
st_chain_test = TChain("tree")
vv_chain_test = TChain("tree")
ggf_chain_test = TChain("tree")



if channel=="mutau":
    selection_train = 'isHtoMuTau && Mu1_charge*Tau1_charge==-1 && dimuon_veto==0 && electron_veto==0 && extra_muon_veto==0 && Tau1_genmatch!=6 && mt<60 && nBjets_m>=1 && EventNumber%10<=3' #use Events with endnumber 0 1 2 3 for training BDT
    selection_test = 'isHtoMuTau && Mu1_charge*Tau1_charge==-1 && dimuon_veto==0 && electron_veto==0 && extra_muon_veto==0 && Tau1_genmatch!=6 && mt<60 && nBjets_m>=1 && EventNumber%10>=4'  #use Events with endnumber 4 5 6 7 8 9 for testing BDT
    #selection_train = 'isHtoMuTau && Mu1_charge*Tau1_charge==-1 && dimuon_veto==0 && electron_veto==0 && extra_muon_veto==0 && Tau1_genmatch!=6 && mt<60 && nBjets_m>=1 && EventNumber%10<=3' #use Events with endnumber 0 1 2 3 for training BDT
    #selection_test = 'isHtoMuTau && Mu1_charge*Tau1_charge==-1 && dimuon_veto==0 && electron_veto==0 && extra_muon_veto==0 && Tau1_genmatch!=6 && mt<60 && nBjets_m>=1 && EventNumber%10>=4'  #use Events with endnumber 4 5 6 7 8 9 for testing BDT
    #selection_train = 'isHtoMuTau && Mu1_charge*Tau1_charge==-1 && dimuon_veto==0 && electron_veto==0 && extra_muon_veto==0 && Tau1_genmatch!=6 && mt<60 && nBjets_m>=1 && EventNumber%10<=3 && (H_mass > 100 && H_mass < 140)' #use Events with endnumber 0 1 2 3 for training BDT
    #selection_test = 'isHtoMuTau && Mu1_charge*Tau1_charge==-1 && dimuon_veto==0 && electron_veto==0 && extra_muon_veto==0 && Tau1_genmatch!=6 && mt<60 && nBjets_m>=1 && EventNumber%10>=4 && (H_mass > 100 && H_mass < 140)'  #use Events with endnumber 4 5 6 7 8 9 for testing BDT
elif channel=="etau":
    selection_train = 'isHtoETau && Ele1_charge*Tau1_charge==-1 && dielectron_veto==0 && muon_veto==0 && extra_electron_veto==0 && Tau1_genmatch!=6 && mt<60 && nBjets_m>=1 && EventNumber%10<=3' #use Events with endnumber 0 1 2 3 for training BDT
    selection_test = 'isHtoETau && Ele1_charge*Tau1_charge==-1 && dielectron_veto==0 && muon_veto==0 && extra_electron_veto==0 && Tau1_genmatch!=6 && mt<60 && nBjets_m>=1 && EventNumber%10>=4' #use Events with endnumber 4 5 6 7 8 9 for testing BDT
    #selection_train = 'isHtoETau && Ele1_charge*Tau1_charge==-1 && dielectron_veto==0 && muon_veto==0 && extra_electron_veto==0 && Tau1_genmatch!=6 && mt<60 && nBjets_m>=1 && EventNumber%10<=3 && (H_mass > 100 && H_mass < 140)' #use Events with endnumber 0 1 2 3 for training BDT
    #selection_test = 'isHtoETau && Ele1_charge*Tau1_charge==-1 && dielectron_veto==0 && muon_veto==0 && extra_electron_veto==0 && Tau1_genmatch!=6 && mt<60 && nBjets_m>=1 && EventNumber%10>=4 && (H_mass > 100 && H_mass < 140)' #use Events with endnumber 4 5 6 7 8 9 for testing BDT

# get skimmed signal and bkg samples



def BDTinput(sample_shortname,filetype,year,preVFP):
    if NN:
        filedir = "/pnfs/psi.ch/cms/trivcat/store/user/pbaertsc/bbh/samples_UL%s%s_NN"%(year,preVFP)
    else:
        filedir = "/pnfs/psi.ch/cms/trivcat/store/user/pbaertsc/bbh/samples_UL%s%s"%(year,preVFP)
    if filetype=="train":
        selection = selection_train
    else:
        selection = selection_test
    isSignal = array('I', [0])
    isbbH = array('I',[0])
    isggH = array('I', [0])
    isTT = array('I', [0])
    isDY = array('I', [0])
    isBkg = array('I', [0])
    BDTtarget = array('I', [0])
    sample = getsamples(channel,year,preVFP)[sample_shortname]
    infile = TFile(filedir+"/"+sample+".root")
    intree = infile.Get("tree")
    outfile = TFile("%s%s_skimmed_%s_UL%s%s.root"%(outdir,sample,filetype,year,preVFP),"RECREATE")
    skimmed_tree=intree.CopyTree(selection)
    infile.Close()
    isSignalBranch = skimmed_tree.Branch('isSignal', isSignal, 'isSignal/I')
    isbbHBranch = skimmed_tree.Branch('isbbH',isbbH,'isbbH/I')
    isggHBranch = skimmed_tree.Branch('isggH',isggH,'isggH/I')
    isTTBranch = skimmed_tree.Branch('isTT', isTT, 'isTT/I')
    isDYBranch = skimmed_tree.Branch('isDY', isDY, 'isDY/I')
    isBkgBranch = skimmed_tree.Branch('isBkg', isBkg, 'isBkg/I')
    BDTtargetBranch = skimmed_tree.Branch('BDTtarget', BDTtarget, 'BDTtarget/I')
    for event in range(0,skimmed_tree.GetEntries()):
        skimmed_tree.GetEntry(event)
        if sample_shortname in ['bbH_htt','ggH_bb_htt_inc','ggH_bb_htt_excl','intH_bb_htt']:
            isSignal[0] = 1
            BDTtarget[0] = 0
        elif "TTTo" in sample:
            isTT[0] = 1
            BDTtarget[0] = 1
        elif sample_shortname in ['DYJets_incl','DYJets_0J','DYJets_1J','DYJets_2J']:
            isDY[0] = 1
            BDTtarget[0] = 2
        else:
            BDTtarget[0] = 3
        isSignalBranch.Fill()
        isTTBranch.Fill()
        isDYBranch.Fill()
        BDTtargetBranch.Fill()
    outfile.Write()
    outfile.Close()
    if filetype=="train":
        if "TTTo" in sample:
            tt_chain_train.Add("%s%s_skimmed_train_UL%s%s.root"%(outdir,sample,year,preVFP))
        elif sample_shortname in ['DYJets_incl','DYJets_0J','DYJets_1J','DYJets_2J']:
            dy_chain_train.Add("%s%s_skimmed_train_UL%s%s.root"%(outdir,sample,year,preVFP))
        elif sample_shortname in ['bbH_htt','ggH_bb_htt_excl','ggH_bb_htt_inc','intH_bb_htt']:
            signal_chain_train.Add("%s%s_skimmed_train_UL%s%s.root"%(outdir,sample,year,preVFP))
    else:
        if "TTTo" in sample:
            tt_chain_test.Add("%s%s_skimmed_test_UL%s%s.root"%(outdir,sample,year,preVFP))
        elif sample_shortname in ['DYJets_incl','DYJets_0J','DYJets_1J','DYJets_2J']:
            dy_chain_test.Add("%s%s_skimmed_test_UL%s%s.root"%(outdir,sample,year,preVFP))
        elif sample_shortname in ['bbH_htt','ggH_bb_htt_excl','ggH_bb_htt_inc','intH_bb_htt']:
            signal_chain_test.Add("%s%s_skimmed_test_UL%s%s.root"%(outdir,sample,year,preVFP))




if __name__=="__main__":
    for sample_shortname in mc_samples:
        print("sample:",sample_shortname)
        for filetype in ["train","test"]:
            
            BDTinput(sample_shortname,filetype,year,preVFP)

  
    if NN:
        signal_chain_train.Merge("%sNNBDT_UL%s_%s_train_signal.root"%(outdir,year,channel))
        tt_chain_train.Merge("%sNNBDT_UL%s_%s_train_tt.root"%(outdir,year,channel))
        dy_chain_train.Merge("%sNNBDT_UL%s_%s_train_dy.root"%(outdir,year,channel))
        signal_chain_test.Merge("%sNNBDT_UL%s_%s_test_signal.root"%(outdir,year,channel))
        tt_chain_test.Merge("%sNNBDT_UL%s_%s_test_tt.root"%(outdir,year,channel))
        dy_chain_test.Merge("%sNNBDT_UL%s_%s_test_dy.root"%(outdir,year,channel))
    else:
        signal_chain_train.Merge("%sBDT_UL%s_%s_train_signal.root"%(outdir,year,channel))
        tt_chain_train.Merge("%sBDT_UL%s_%s_train_tt.root"%(outdir,year,channel))
        dy_chain_train.Merge("%sBDT_UL%s_%s_train_dy.root"%(outdir,year,channel))
        signal_chain_test.Merge("%sBDT_UL%s_%s_test_signal.root"%(outdir,year,channel))
        tt_chain_test.Merge("%sBDT_UL%s_%s_test_tt.root"%(outdir,year,channel))
        dy_chain_test.Merge("%sBDT_UL%s_%s_test_dy.root"%(outdir,year,channel))
        #signal_chain_train.Merge("%sBDT_UL%s_%s_train_signal_Hcut.root"%(outdir,year,channel))
        #tt_chain_train.Merge("%sBDT_UL%s_%s_train_tt_Hcut.root"%(outdir,year,channel))
        #dy_chain_train.Merge("%sBDT_UL%s_%s_train_dy_Hcut.root"%(outdir,year,channel))
        #signal_chain_test.Merge("%sBDT_UL%s_%s_test_signal_Hcut.root"%(outdir,year,channel))
        #tt_chain_test.Merge("%sBDT_UL%s_%s_test_tt_Hcut.root"%(outdir,year,channel))
        #dy_chain_test.Merge("%sBDT_UL%s_%s_test_dy_Hcut.root"%(outdir,year,channel))

    for sample_shortname in mc_samples:
        sample = getsamples(channel,year,preVFP)[sample_shortname]
        os.remove("%s%s_skimmed_train_UL%s%s.root"%(outdir,sample,year,preVFP))
        os.remove("%s%s_skimmed_test_UL%s%s.root"%(outdir,sample,year,preVFP))




