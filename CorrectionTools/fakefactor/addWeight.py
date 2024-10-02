#! /usr/bin/env python

import os, multiprocessing, math
import numpy as np
from array import array
from ROOT import TFile, TH1, TF1, TLorentzVector
import ROOT
from argparse import ArgumentParser
from submit import ensureDirectory
import sys 
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from ffvarcorr import ffvarcorrclass
from shutil import copyfile, rmtree
import time

##############################

def processFile(sample, sample_scratch, year):
    ffvarcorr = ffvarcorrclass(year)

    # Unweighted input
    ref_file_name = sample
    print("processing sample:",ref_file_name,"...")
    
    # Weighted output
    new_file_name = sample_scratch
    new_file = TFile(new_file_name, 'NEW')
    new_file.cd()
    
    # Open old file
    ref_file = TFile(ref_file_name, 'READ')
 

    # Variables declaration
    wt_ffvarcorr_hmass_qcd = array('f', [1.])
    wt_ffvarcorr_jetpt_qcd = array('f', [1.])
    wt_ffvarcorr_collinearmass_qcd = array('f', [1.])
    wt_ffvarcorr_taujmass_qcd = array('f', [1.])
    wt_ffvarcorr_hmass_tt = array('f', [1.])
    wt_ffvarcorr_jetpt_tt = array('f', [1.])
    wt_ffvarcorr_collinearmass_tt = array('f', [1.])
    wt_ffvarcorr_taujmass_tt = array('f', [1.])
    # Looping over file content
    for key in ref_file.GetListOfKeys():
        obj = key.ReadObj()
        if obj.IsA().InheritsFrom('TTree'):
            new_file.cd()
            new_tree = obj.CopyTree("")
            # New branches
            wt_ffvarcorr_hmass_qcd_Branch = new_tree.Branch('wt_ffvarcorr_hmass_qcd',wt_ffvarcorr_hmass_qcd,'wt_ffvarcorr_hmass_qcd/F')
            wt_ffvarcorr_jetpt_qcd_Branch = new_tree.Branch('wt_ffvarcorr_jetpt_qcd',wt_ffvarcorr_jetpt_qcd,'wt_ffvarcorr_jetpt_qcd/F')
            wt_ffvarcorr_collinearmass_qcd_Branch = new_tree.Branch('wt_ffvarcorr_collinearmass_qcd',wt_ffvarcorr_collinearmass_qcd,'wt_ffvarcorr_collinearmass_qcd/F')
            wt_ffvarcorr_taujmass_qcd_Branch = new_tree.Branch('wt_ffvarcorr_taujmass_qcd',wt_ffvarcorr_taujmass_qcd,'wt_ffvarcorr_taujmass_qcd/F')
            wt_ffvarcorr_hmass_tt_Branch = new_tree.Branch('wt_ffvarcorr_hmass_tt',wt_ffvarcorr_hmass_tt,'wt_ffvarcorr_hmass_tt/F')
            wt_ffvarcorr_jetpt_tt_Branch = new_tree.Branch('wt_ffvarcorr_jetpt_tt',wt_ffvarcorr_jetpt_tt,'wt_ffvarcorr_jetpt_tt/F')
            wt_ffvarcorr_collinearmass_tt_Branch = new_tree.Branch('wt_ffvarcorr_collinearmass_tt',wt_ffvarcorr_collinearmass_tt,'wt_ffvarcorr_collinearmass_tt/F')
            wt_ffvarcorr_taujmass_tt_Branch = new_tree.Branch('wt_ffvarcorr_taujmass_tt',wt_ffvarcorr_taujmass_tt,'wt_ffvarcorr_taujmass_tt/F')
            # looping over events
            for event in range(0, obj.GetEntries()):
                obj.GetEntry(event)
                #Initialize
                wt_ffvarcorr_hmass_qcd[0] = 1.
                wt_ffvarcorr_jetpt_qcd[0] = 1.
                wt_ffvarcorr_collinearmass_qcd[0] = 1.
                wt_ffvarcorr_taujmass_qcd[0] = 1.
                channel = ""
                if any([obj.isHtoMuTau,obj.isHtoMuTauAR,obj.isHtolooseMuTau,obj.isHtolooseMuTauAR]):
                    channel = "mutau"
                elif any([obj.isHtoETau,obj.isHtoETauAR,obj.isHtolooseETau,obj.isHtolooseETauAR]):
                    channel = "etau"

                Tau1_decaymode = obj.Tau1_decaymode
                H_mass = obj.H_mass
                Jet1_pt = obj.Jet1_pt
                collinear_mass = obj.collinear_mass
                TauJ_mass  = obj.TauJ_mass
                if channel in ["mutau","etau"]:
                    wt_ffvarcorr_hmass_qcd[0]  = ffvarcorr.ffweightcorr_hmass(H_mass,Tau1_decaymode,channel)[0]
                    wt_ffvarcorr_jetpt_qcd[0] = ffvarcorr.ffweightcorr_jetpt(Jet1_pt,Tau1_decaymode,channel)[0]
                    wt_ffvarcorr_collinearmass_qcd[0] = ffvarcorr.ffweightcorr_collinearmass(collinear_mass,Tau1_decaymode,channel)[0]
                    wt_ffvarcorr_taujmass_qcd[0] = ffvarcorr.ffweightcorr_taujmass(TauJ_mass,Tau1_decaymode,channel)[0]
                    wt_ffvarcorr_hmass_tt[0]  = ffvarcorr.ffweightcorr_hmass(H_mass,Tau1_decaymode,channel)[1]
                    wt_ffvarcorr_jetpt_tt[0] = ffvarcorr.ffweightcorr_jetpt(Jet1_pt,Tau1_decaymode,channel)[1]
                    wt_ffvarcorr_collinearmass_tt[0] = ffvarcorr.ffweightcorr_collinearmass(collinear_mass,Tau1_decaymode,channel)[1]
                    wt_ffvarcorr_taujmass_tt[0] = ffvarcorr.ffweightcorr_taujmass(TauJ_mass,Tau1_decaymode,channel)[1]
                # Fill the branches
                wt_ffvarcorr_hmass_qcd_Branch.Fill()
                wt_ffvarcorr_jetpt_qcd_Branch.Fill()
                wt_ffvarcorr_collinearmass_qcd_Branch.Fill()
                wt_ffvarcorr_taujmass_qcd_Branch.Fill()
                wt_ffvarcorr_hmass_tt_Branch.Fill()
                wt_ffvarcorr_jetpt_tt_Branch.Fill()
                wt_ffvarcorr_collinearmass_tt_Branch.Fill()
                wt_ffvarcorr_taujmass_tt_Branch.Fill()
            new_file.cd()
            new_tree.Write("", obj.kOverwrite)
       
    new_file.Close() 
    print("finished processing sample")
    return 0

if __name__== "__main__":
    parser = ArgumentParser()
    parser.add_argument('-y', '--year',    dest='year', type=str, default='2018', action='store')
    parser.add_argument('-u', '--UL',      dest='ULtag', action='store_const', const="UL",default="")
    parser.add_argument('-p', '--preVFP',  dest='preVFP', action='store_const', const="_preVFP",default="")
    parser.add_argument('-c', '--corr',    dest='corr', type=str, action='store')
    parser.add_argument('-o', '--origin',  dest='origin', type=str, action='store')
    args = parser.parse_args()

    year = args.year
    ULtag = args.ULtag
    preVFP = args.preVFP
    corr = args.corr
    origin = args.origin


    origin = '/pnfs/psi.ch/cms/trivcat/store/user/pbaertsc/bbh/samples_UL%s%s/'%(year,preVFP)
    target_scratch = '/scratch/pbaertsc/bbh/samples_newweight/samples_UL%s%s/'%(year,preVFP)
    #target = '/pnfs/psi.ch/cms/trivcat/store/user/pbaertsc/bbh/samples_newweight/samples_UL%s%s/'%(year,preVFP)
    target = '/pnfs/psi.ch/cms/trivcat/store/user/pbaertsc/bbh/ffvarcorr/samples_UL%s%s/'%(year,preVFP)

    ensureDirectory(target_scratch)
    samples = ['DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8','DYJetsToLL_0J_TuneCP5_13TeV-amcatnloFXFX-pythia8','DYJetsToLL_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8','DYJetsToLL_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8','WJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-pythia8','WJetsToLNu_0J_TuneCP5_13TeV-amcatnloFXFX-pythia8','WJetsToLNu_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8','WJetsToLNu_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8','TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8','TTToHadronic_TuneCP5_13TeV-powheg-pythia8','TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8','ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8','ST_t-channel_top_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8','ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-amcatnlo-pythia8','ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8','ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8']
    for sample in samples:
        sample = origin+sample+".root"
        print("processing ",sample)
        sample_scratch = target_scratch+"%s"%sample.split("/")[-1]
        start = time.time()
        processFile(sample, sample_scratch, year)
        copyfile_from=target_scratch+"/"+sample
        copyfile_to=target+"/"+sample
        print("copying ",copyfile_from,"to ",copyfile_to)
        os.system("xrdcp -f %s root://t3dcachedb.psi.ch:1094/%s"%(copyfile_from,copyfile_to))
        end = time.time()
        print("time:",(end-start)/60.,"min")
        
    print("deleting scratch directory:",target_scratch)
    rmtree(target_scratch,ignore_errors=True)
    print('\nDone.')

