#!/bin/env python
import numpy
numpy.random.seed(1337)
#numpy.random.seed(246)
import pandas
import ROOT
import random
import time
import math
import sys
import csv
from sklearn import preprocessing


#################  choose size of used dataset ######################
#fixed_dataset_length = 2640000
#fixed_dataset_length = 1910000
fixed_dataset_length = 1000000
fixed_train_length = 560000
fixed_test_length = 100000
#fulllep_fixed_length = int(round(0.1226*fixed_dataset_length))
#semilep_fixed_length = int(round(0.4553*fixed_dataset_length))
#fullhad_fixed_length = int(round(0.422* fixed_dataset_length))
###################################################################################
list_name = "/mnt/t3nfs01/data01/shome/pbaertsc/tauinitial/CMSSW_8_0_25/src/XtautauML/batch_output/reg_ditau_mass_skim_correct40.csv"
dataframe_ditaumass = pandas.read_csv(list_name,delim_whitespace=False,header=None)
dataframe_ditaumass_shuffled = dataframe_ditaumass.sample(frac=1,random_state =1337)
dataset_ditaumass = dataframe_ditaumass_shuffled.values
dataset_total_length = len(dataset_ditaumass[:,0])

inputNN = []
inputSVfit = []
ditaumass = []
ditaumasspt = []
ditaumassEpxpypz = []
ditauEpxpypz = []
ditaumassE = []
ditaumassptE = []
ditauvismass = []
ditaucollinearmass = []
decaymode_count = 0
decaymode_count_fulllep = 0
decaymode_count_semilep = 0
decaymode_count_fullhad = 0
loop_length = 1000
decaymode_count_fulllep_loop = 0
decaymode_count_semilep_loop = 0
decaymode_count_fullhad_loop = 0

histCOV00 = ROOT.TH1D("COV00","histogram of COV00",100,-20,20)
histCOV11 = ROOT.TH1D("COV11","histogram of COV11",100,-20,20)

for i in range(0,fixed_dataset_length):
    genMissingET_MET = dataset_ditaumass[i,26]
    genMissingET_Phi = dataset_ditaumass[i,27]
    MissingET_MET = dataset_ditaumass[i,28]
    MissingET_Phi = dataset_ditaumass[i,29]
    genMETpx = genMissingET_MET*numpy.cos(genMissingET_Phi)
    genMETpy = genMissingET_MET*numpy.sin(genMissingET_Phi)
    METpx = MissingET_MET*numpy.cos(MissingET_Phi)
    METpy = MissingET_MET*numpy.sin(MissingET_Phi)
    METCOV00 = METpx-genMETpx
    METCOV11 = METpy-genMETpy
    histCOV00.Fill(METCOV00)
    histCOV11.Fill(METCOV11)

histCOV00.Fit("gaus")
COV00_fit = histCOV00.GetFunction("gaus")
COV00_width = COV00_fit.GetParameter(2)
histCOV11.Fit("gaus")
COV11_fit = histCOV11.GetFunction("gaus")
COV11_width = COV11_fit.GetParameter(2)
COV_width_mean = (COV00_width+COV11_width)/2
METCOV = ROOT.TMath.Power(COV_width_mean,2.)

for i in range(0,dataset_total_length):
    tau1_pt = dataset_ditaumass[i,0]
    tau1_eta = dataset_ditaumass[i,1] 
    tau1_phi = dataset_ditaumass[i,2]
    tau1_mass = dataset_ditaumass[i,3]
    vistau1_pt = dataset_ditaumass[i,4]
    vistau1_eta = dataset_ditaumass[i,5]
    vistau1_phi = dataset_ditaumass[i,6]
    vistau1_mass = dataset_ditaumass[i,7]
    vistau1_att = dataset_ditaumass[i,8]
    vistau1_prongs = dataset_ditaumass[i,9]
    vistau1_pi0 = dataset_ditaumass[i,10]
    tau2_pt = dataset_ditaumass[i,11]
    tau2_eta = dataset_ditaumass[i,12] 
    tau2_phi = dataset_ditaumass[i,13]
    tau2_mass = dataset_ditaumass[i,14]
    vistau2_pt = dataset_ditaumass[i,15]
    vistau2_eta = dataset_ditaumass[i,16]
    vistau2_phi = dataset_ditaumass[i,17]
    vistau2_mass = dataset_ditaumass[i,18]
    vistau2_att = dataset_ditaumass[i,19]
    vistau2_prongs = dataset_ditaumass[i,20]
    vistau2_pi0 = dataset_ditaumass[i,21]
    nu_pt = dataset_ditaumass[i,22]
    nu_eta = dataset_ditaumass[i,23]
    nu_phi = dataset_ditaumass[i,24]
    nu_mass = dataset_ditaumass[i,25]
    genMissingET_MET = dataset_ditaumass[i,26]
    genMissingET_Phi = dataset_ditaumass[i,27]
    MissingET_MET = dataset_ditaumass[i,28]
    MissingET_Phi = dataset_ditaumass[i,29]
    genMETpx = genMissingET_MET*numpy.cos(genMissingET_Phi)
    genMETpy = genMissingET_MET*numpy.sin(genMissingET_Phi)
    METpx = MissingET_MET*numpy.cos(MissingET_Phi)
    METpy = MissingET_MET*numpy.sin(MissingET_Phi)
    v_tau1 = ROOT.TLorentzVector()
    v_tau1.SetPtEtaPhiM(tau1_pt,tau1_eta,tau1_phi,tau1_mass)
    v_tau2 = ROOT.TLorentzVector()
    v_tau2.SetPtEtaPhiM(tau2_pt,tau2_eta,tau2_phi,tau2_mass)
    v_vistau1 = ROOT.TLorentzVector()
    v_vistau1.SetPtEtaPhiM(vistau1_pt,vistau1_eta,vistau1_phi,vistau1_mass)
    v_vistau2 = ROOT.TLorentzVector()
    v_vistau2.SetPtEtaPhiM(vistau2_pt,vistau2_eta,vistau2_phi,vistau2_mass)
    v_nu = ROOT.TLorentzVector()
    v_nu.SetPtEtaPhiM(nu_pt,nu_eta,nu_phi,nu_mass)
    v_mot = v_vistau1+v_vistau2+v_nu
    v_vismot = v_vistau1+v_vistau2
    ditaumass_value = v_mot.M()
    ditauvismass_value = v_vismot.M()
    pt_nu = v_nu.Pt()
    nu_px = v_nu.Px()
    nu_py = v_nu.Py()
    vistau1_decaymode = int(5*(vistau1_prongs-1)+vistau1_pi0)
    vistau2_decaymode = int(5*(vistau2_prongs-1)+vistau2_pi0)
    vistau1_E = v_vistau1.E()
    vistau2_E = v_vistau2.E()
    vismass = v_vismot.M()
    p_vis = v_vismot.P()
    pt_vis = v_vismot.Pt()
    pt_nu = v_nu.Pt()
    pt = v_mot.Pt()
    E = v_mot.E()
    px = v_mot.Px()
    py = v_mot.Py()
    pz = v_mot.Pz()
    #ditaumass_collinear = vismass/numpy.sqrt(vistau1_pt/(vistau1_pt+pt_nu)*vistau2_pt/(vistau2_pt+pt_nu))
    ditaumass_collinear = vismass/numpy.sqrt(vistau1_pt/(vistau1_pt+MissingET_MET)*vistau2_pt/(vistau2_pt+MissingET_MET))
    mass_no_pz = v_vismot.E()**2-v_vismot.Pz()**2-pt_vis**2
    if decaymode_count % 999 == 0:
        decaymode_count_fulllep_loop = 0
        decaymode_count_semilep_loop = 0
        decaymode_count_fullhad_loop = 0
        #loop_length += 100
    fulllep_fixed_length = int(round(0.1226*loop_length))
    semilep_fixed_length = int(round(0.4553*loop_length))
    fullhad_fixed_length = int(round(0.422* loop_length))
    if decaymode_count < fixed_dataset_length and ditaumass_value > 78.0:
        if vistau1_att in (1,2) and vistau2_att in (1,2) and decaymode_count_fulllep_loop < fulllep_fixed_length:
            #if vistau1_att in (1,2) and vistau2_att in (1,2):
            #inputNN.append([1.0,0.0,0.0,0.0,vistau1_pt,vistau1_eta,vistau1_phi,vistau1_E,vistau1_mass,vistau2_pt,vistau2_eta,vistau2_phi,vistau2_E,vistau2_mass, genMissingET_MET,genMissingET_Phi,ditaumass_collinear])
            inputNN.append([1.0,0.0,0.0,0.0,vistau1_pt,vistau1_eta,vistau1_phi,vistau1_E,vistau2_pt,vistau2_eta,vistau2_phi,vistau2_E, genMissingET_MET,genMissingET_Phi])
            inputSVfit.append([vistau1_pt,vistau1_eta,vistau1_phi,vistau1_mass,vistau1_att,vistau1_prongs,vistau1_pi0,vistau2_pt,vistau2_eta,vistau2_phi,vistau2_mass,vistau2_att,vistau2_prongs,vistau2_pi0,METpx,METpy,METCOV,ditaumass_value,ditauvismass_value])
            #inputNN.append([vistau1_pt,vistau1_eta,vistau1_phi,vistau1_mass,vistau2_pt,vistau2_eta,vistau2_phi,vistau2_mass,v_nu.Px(),v_nu.Py(),p_vis,vismass])
            ditaumass.append(ditaumass_value)
            ditaumasspt.append([ditaumass_value,pt])
            ditaumassEpxpypz.append([ditaumass_value,E,px,py,pz])
            ditauEpxpypz.append([E,px,py,pz])
            ditaumassE.append([ditaumass_value,E])
            ditaumassptE.append([ditaumass_value,pt,E])
            ditauvismass.append(ditauvismass_value)
            ditaucollinearmass.append(ditaumass_collinear)
            decaymode_count_fulllep += 1
            decaymode_count_fulllep_loop += 1
            decaymode_count += 1
        elif vistau1_att in (1,2) and vistau2_att == 3 and decaymode_count_semilep_loop < semilep_fixed_length:
            #elif vistau1_att in (1,2) and vistau2_att == 3:
            #inputNN.append([0.0,1.0,0.0,0.0,vistau1_pt,vistau1_eta,vistau1_phi,vistau1_E,vistau1_mass,vistau2_pt,vistau2_eta,vistau2_phi,vistau2_E,vistau2_mass, genMissingET_MET,genMissingET_Phi,ditaumass_collinear])
            inputNN.append([0.0,1.0,0.0,0.0,vistau1_pt,vistau1_eta,vistau1_phi,vistau1_E,vistau2_pt,vistau2_eta,vistau2_phi,vistau2_E, genMissingET_MET,genMissingET_Phi])
            inputSVfit.append([vistau1_pt,vistau1_eta,vistau1_phi,vistau1_mass,vistau1_att,vistau1_prongs,vistau1_pi0,vistau2_pt,vistau2_eta,vistau2_phi,vistau2_mass,vistau2_att,vistau2_prongs,vistau2_pi0,METpx,METpy,METCOV,ditaumass_value,ditauvismass_value])
            #inputNN.append([vistau1_pt,vistau1_eta,vistau1_phi,vistau1_mass,vistau2_pt,vistau2_eta,vistau2_phi,vistau2_mass,v_nu.Px(),v_nu.Py(),p_vis,vismass])
            ditaumass.append(ditaumass_value)
            ditaumasspt.append([ditaumass_value,pt])
            ditaumassEpxpypz.append([ditaumass_value,E,px,py,pz])
            ditauEpxpypz.append([E,px,py,pz])
            ditaumassE.append([ditaumass_value,E])
            ditaumassptE.append([ditaumass_value,pt,E])
            ditauvismass.append(ditauvismass_value)
            ditaucollinearmass.append(ditaumass_collinear)
            decaymode_count_semilep += 1
            decaymode_count_semilep_loop += 1
            decaymode_count += 1
        elif vistau1_att == 3 and vistau2_att in (1,2) and decaymode_count_semilep_loop < semilep_fixed_length:
            #elif vistau1_att == 3 and vistau2_att in (1,2):
            #inputNN.append([0.0,0.0,1.0,0.0,vistau1_pt,vistau1_eta,vistau1_phi,vistau1_E,vistau1_mass,vistau2_pt,vistau2_eta,vistau2_phi,vistau2_E,vistau2_mass, genMissingET_MET,genMissingET_Phi,ditaumass_collinear])
            inputNN.append([0.0,0.0,1.0,0.0,vistau1_pt,vistau1_eta,vistau1_phi,vistau1_E,vistau2_pt,vistau2_eta,vistau2_phi,vistau2_E, genMissingET_MET,genMissingET_Phi])
            inputSVfit.append([vistau1_pt,vistau1_eta,vistau1_phi,vistau1_mass,vistau1_att,vistau1_prongs,vistau1_pi0,vistau2_pt,vistau2_eta,vistau2_phi,vistau2_mass,vistau2_att,vistau2_prongs,vistau2_pi0,METpx,METpy,METCOV,ditaumass_value,ditauvismass_value])
            #inputNN.append([vistau1_pt,vistau1_eta,vistau1_phi,vistau1_mass,vistau2_pt,vistau2_eta,vistau2_phi,vistau2_mass,v_nu.Px(),v_nu.Py(),p_vis,vismass])
            ditaumass.append(ditaumass_value)
            ditaumasspt.append([ditaumass_value,pt])
            ditaumassEpxpypz.append([ditaumass_value,E,px,py,pz])
            ditauEpxpypz.append([E,px,py,pz])
            ditaumassE.append([ditaumass_value,E])
            ditaumassptE.append([ditaumass_value,pt,E])
            ditauvismass.append(ditauvismass_value)
            ditaucollinearmass.append(ditaumass_collinear)
            decaymode_count_semilep += 1
            decaymode_count_semilep_loop += 1
            decaymode_count += 1
        elif vistau1_att == 3 and vistau2_att == 3 and decaymode_count_fullhad_loop < fullhad_fixed_length:
            #elif vistau1_att == 3 and vistau2_att == 3:
            #inputNN.append([0.0,0.0,0.0,1.0,vistau1_pt,vistau1_eta,vistau1_phi,vistau1_E,vistau1_mass,vistau2_pt,vistau2_eta,vistau2_phi,vistau2_E,vistau2_mass, genMissingET_MET,genMissingET_Phi,ditaumass_collinear])
            inputNN.append([0.0,0.0,0.0,1.0,vistau1_pt,vistau1_eta,vistau1_phi,vistau1_E,vistau2_pt,vistau2_eta,vistau2_phi,vistau2_E, genMissingET_MET,genMissingET_Phi])
            inputSVfit.append([vistau1_pt,vistau1_eta,vistau1_phi,vistau1_mass,vistau1_att,vistau1_prongs,vistau1_pi0,vistau2_pt,vistau2_eta,vistau2_phi,vistau2_mass,vistau2_att,vistau2_prongs,vistau2_pi0,METpx,METpy,METCOV,ditaumass_value,ditauvismass_value])
            #inputNN.append([vistau1_pt,vistau1_eta,vistau1_phi,vistau1_mass,vistau2_pt,vistau2_eta,vistau2_phi,vistau2_mass,v_nu.Px(),v_nu.Py(),p_vis,vismass])
            ditaumass.append(ditaumass_value)
            ditaumasspt.append([ditaumass_value,pt])
            ditaumassEpxpypz.append([ditaumass_value,E,px,py,pz])
            ditauEpxpypz.append([E,px,py,pz])
            ditaumassE.append([ditaumass_value,E])
            ditaumassptE.append([ditaumass_value,pt,E])
            ditauvismass.append(ditauvismass_value)
            ditaucollinearmass.append(ditaumass_collinear)
            decaymode_count_fullhad += 1 
            decaymode_count_fullhad_loop += 1 
            decaymode_count += 1


print "decaymode_count:",decaymode_count
print "decaymode_count_fulllep:",decaymode_count_fulllep
print "decaymode_count_semilep:",decaymode_count_semilep
print "decaymode_count_fullhad:",decaymode_count_fullhad


inputNN = numpy.array(inputNN,numpy.float64)
ditaumasspt = numpy.array(ditaumasspt,numpy.float64)
ditaumassEpxpypz = numpy.array(ditaumassEpxpypz,numpy.float64)
ditauEpxpypz = numpy.array(ditauEpxpypz,numpy.float64)
ditaumassE = numpy.array(ditaumassE,numpy.float64)
ditaumassptE = numpy.array(ditaumassptE,numpy.float64)
inputSVfit = numpy.array(inputSVfit,numpy.float64)


train_inputNN_forselection = inputNN[fixed_test_length:,:]
train_inputSVfit_forselection = inputSVfit[fixed_test_length:,:]
train_ditaumass_forselection = ditaumass[fixed_test_length:]
train_ditaumasspt_forselection = ditaumasspt[fixed_test_length:,:]
train_ditaumassEpxpypz_forselection = ditaumassEpxpypz[fixed_test_length:,:]
train_ditauEpxpypz_forselection = ditauEpxpypz[fixed_test_length:,:]
train_ditaumassE_forselection = ditaumassE[fixed_test_length:,:]
train_ditaumassptE_forselection = ditaumassptE[fixed_test_length:,:]
test_inputNN_selected = inputNN[0:fixed_test_length,:]
test_inputSVfit_selected = inputSVfit[0:fixed_test_length,:]
test_ditaumass_selected = ditaumass[0:fixed_test_length]
test_ditaumasspt_selected = ditaumasspt[0:fixed_test_length,:]
test_ditaumassEpxpypz_selected = ditaumassEpxpypz[0:fixed_test_length,:]
test_ditauEpxpypz_selected = ditauEpxpypz[0:fixed_test_length,:]
test_ditaumassE_selected = ditaumassE[0:fixed_test_length,:]
test_ditaumassptE_selected = ditaumassptE[0:fixed_test_length,:]
test_ditauvismass_selected = ditauvismass[0:fixed_test_length]
test_ditaucollinearmass_selected = ditaucollinearmass[0:fixed_test_length]


decaymode_test_count = 0
decaymode_test_count_fulllep = 0
decaymode_test_count_semilep = 0
decaymode_test_count_fullhad = 0

test_inputNN_selected_fulllep = []
test_inputNN_selected_semilep = []
test_inputNN_selected_fullhad = []
test_ditaumass_selected_fulllep = []
test_ditaumass_selected_semilep = []
test_ditaumass_selected_fullhad = []
test_inputSVfit_selected_fulllep = []
test_inputSVfit_selected_semilep = []
test_inputSVfit_selected_fullhad = []


for i,value in enumerate(test_inputNN_selected[:,0]):
    decaymode_test_count += 1
    if test_inputNN_selected[i,0] == 1.0:
        decaymode_test_count_fulllep += 1
        test_inputNN_selected_fulllep.append(test_inputNN_selected[i,:])
        test_ditaumass_selected_fulllep.append(test_ditaumass_selected[i])
        test_inputSVfit_selected_fulllep.append(test_inputSVfit_selected[i,:])
    if test_inputNN_selected[i,1] == 1.0 or test_inputNN_selected[i,2] == 1.0:
        decaymode_test_count_semilep += 1
        test_inputNN_selected_semilep.append(test_inputNN_selected[i,:])
        test_ditaumass_selected_semilep.append(test_ditaumass_selected[i])
        test_inputSVfit_selected_semilep.append(test_inputSVfit_selected[i,:])
    if test_inputNN_selected[i,3] == 1.0:
        decaymode_test_count_fullhad += 1
        test_inputNN_selected_fullhad.append(test_inputNN_selected[i,:])
        test_ditaumass_selected_fullhad.append(test_ditaumass_selected[i])
        test_inputSVfit_selected_fullhad.append(test_inputSVfit_selected[i,:])
print "decaymode_test_count:",decaymode_test_count
print "decaymode_test_count_fulllep:",decaymode_test_count_fulllep
print "decaymode_test_count_semilep:",decaymode_test_count_semilep
print "decaymode_test_count_fullhad:",decaymode_test_count_fullhad

test_inputNN_selected_fulllep = numpy.array(test_inputNN_selected_fulllep,numpy.float64)
test_inputNN_selected_semilep = numpy.array(test_inputNN_selected_semilep,numpy.float64)
test_inputNN_selected_fullhad = numpy.array(test_inputNN_selected_fullhad,numpy.float64)
test_inputSVfit_selected_fulllep = numpy.array(test_inputSVfit_selected_fulllep,numpy.float64)
test_inputSVfit_selected_semilep = numpy.array(test_inputSVfit_selected_semilep,numpy.float64)
test_inputSVfit_selected_fullhad = numpy.array(test_inputSVfit_selected_fullhad,numpy.float64)



######### make flat mass distribution with less events ######################
#min_bincontent = 4900
min_bincontent = 3000
histtrainditaumasscalc = ROOT.TH1D("trainditaumasscalc","trainditaumasscalc",300,0,300)


train_inputNN_selected = []
train_ditaumass_selected = []
train_ditauvismass_selected = []
train_ditaucollinearmass_selected = []
train_ditaumasspt_selected = []
train_ditaumassEpxpypz_selected = []
train_ditauEpxpypz_selected = []
train_ditaumassE_selected =[]
train_ditaumassptE_selected =[]
train_inputNN_notused = []
train_inputSVfit_notused = []
train_ditaumass_notused = []
train_ditaumasspt_notused = []
train_ditaumassEpxpypz_notused = []
train_ditauEpxpypz_notused = []
train_ditaumassE_notused = []
train_ditaumassptE_notused = []

for k,ditaumass_loopvalue in enumerate(train_ditaumass_forselection):
    bin_index = histtrainditaumasscalc.GetXaxis().FindBin(ditaumass_loopvalue)
    bin_content = histtrainditaumasscalc.GetBinContent(bin_index)
    if bin_content < min_bincontent:
        histtrainditaumasscalc.SetBinContent(bin_index,bin_content+1)
        train_inputNN_selected.append(train_inputNN_forselection[k,:])
        train_ditaumass_selected.append(ditaumass_loopvalue)
        train_ditaumasspt_selected.append(train_ditaumasspt_forselection[k,:])
        train_ditaumassEpxpypz_selected.append(train_ditaumassEpxpypz_forselection[k,:])
        train_ditauEpxpypz_selected.append(train_ditauEpxpypz_forselection[k,:])
        train_ditaumassE_selected.append(train_ditaumassE_forselection[k,:])
        train_ditaumassptE_selected.append(train_ditaumassptE_forselection[k,:])
    else:
        train_inputNN_notused.append(train_inputNN_forselection[k,:])
        train_inputSVfit_notused.append(train_inputSVfit_forselection[k,:])
        train_ditaumass_notused.append(ditaumass_loopvalue)
        train_ditaumasspt_notused.append(train_ditaumasspt_forselection[k,:])
        train_ditaumassEpxpypz_notused.append(train_ditaumassEpxpypz_forselection[k,:])
        train_ditauEpxpypz_notused.append(train_ditauEpxpypz_forselection[k,:])
        train_ditaumassE_notused.append(train_ditaumassE_forselection[k,:])
        train_ditaumassptE_notused.append(train_ditaumassptE_forselection[k,:])

train_inputNN_selected = numpy.array(train_inputNN_selected,numpy.float64)
train_ditaumasspt_selected = numpy.array(train_ditaumasspt_selected,numpy.float64)
train_ditaumassEpxpypz_selected = numpy.array(train_ditaumassEpxpypz_selected,numpy.float64)
train_ditauEpxpypz_selected = numpy.array(train_ditauEpxpypz_selected,numpy.float64)
train_ditaumassE_selected = numpy.array(train_ditaumassE_selected,numpy.float64)
train_ditaumassptE_selected = numpy.array(train_ditaumassptE_selected,numpy.float64)
train_inputNN_notused = numpy.array(train_inputNN_notused,numpy.float64)
train_inputSVfit_notused = numpy.array(train_inputSVfit_notused,numpy.float64)
train_ditaumasspt_notused = numpy.array(train_ditaumasspt_notused,numpy.float64)
train_ditaumassEpxpypz_notused = numpy.array(train_ditaumassEpxpypz_notused,numpy.float64)
train_ditauEpxpypz_notused = numpy.array(train_ditauEpxpypz_notused,numpy.float64)
train_ditaumassE_notused = numpy.array(train_ditaumassE_notused,numpy.float64)
train_ditaumassptE_notused = numpy.array(train_ditaumassptE_notused,numpy.float64)

decaymode_train_count = 0
decaymode_train_count_fulllep = 0
decaymode_train_count_semilep = 0
decaymode_train_count_fullhad = 0

for i,value in enumerate(train_inputNN_selected[:,0]):
    decaymode_train_count += 1
    if train_inputNN_selected[i,0] == 1.0:
        decaymode_train_count_fulllep += 1
    if train_inputNN_selected[i,1] == 1.0 or train_inputNN_selected[i,2] == 1.0:
        decaymode_train_count_semilep += 1
    if train_inputNN_selected[i,3] == 1.0:
        decaymode_train_count_fullhad += 1
print "decaymode_train_count:",decaymode_train_count
print "decaymode_train_count_fulllep:",decaymode_train_count_fulllep
print "decaymode_train_count_semilep:",decaymode_train_count_semilep
print "decaymode_train_count_fullhad:",decaymode_train_count_fullhad


inputNN_180GeV = []
inputSVfit_180GeV = []
ditaumass_180GeV = []
ditaumasspt_180GeV = []
ditaumassEpxpypz_180GeV = []
ditauEpxpypz_180GeV = []
ditaumassE_180GeV = []
ditaumassptE_180GeV = []
inputNN_250GeV = []
inputSVfit_250GeV = []
ditaumass_250GeV = []
ditaumasspt_250GeV = []
ditaumassEpxpypz_250GeV = []
ditauEpxpypz_250GeV = []
ditaumassE_250GeV = []
ditaumassptE_250GeV = []


for j,ditaumass_loopvalue in enumerate(train_ditaumass_notused):
    if 179.0 < ditaumass_loopvalue and 181.0 > ditaumass_loopvalue:
        inputNN_180GeV.append(train_inputNN_notused[j,:])
        inputSVfit_180GeV.append(train_inputSVfit_notused[j,:])
        ditaumass_180GeV.append(ditaumass_loopvalue)
        ditaumasspt_180GeV.append(train_ditaumasspt_notused[j,:])
        ditaumassEpxpypz_180GeV.append(train_ditaumassEpxpypz_notused[j,:])
        ditauEpxpypz_180GeV.append(train_ditauEpxpypz_notused[j,:])
        ditaumassE_180GeV.append(train_ditaumassE_notused[j,:])
        ditaumassptE_180GeV.append(train_ditaumassptE_notused[j,:])
    if 249.0 < ditaumass_loopvalue and 251.0 > ditaumass_loopvalue:
        inputNN_250GeV.append(train_inputNN_notused[j,:])
        inputSVfit_250GeV.append(train_inputSVfit_notused[j,:])
        ditaumass_250GeV.append(ditaumass_loopvalue)
        ditaumasspt_250GeV.append(train_ditaumasspt_notused[j,:])
        ditaumassEpxpypz_250GeV.append(train_ditaumassEpxpypz_notused[j,:])
        ditauEpxpypz_250GeV.append(train_ditauEpxpypz_notused[j,:])
        ditaumassE_250GeV.append(train_ditaumassE_notused[j,:])
        ditaumassptE_250GeV.append(train_ditaumassptE_notused[j,:])
for g,ditaumass_loopvalue in enumerate(test_ditaumass_selected):
    if 179.0 < ditaumass_loopvalue and 181.0 > ditaumass_loopvalue:
        inputNN_180GeV.append(test_inputNN_selected[g,:])
        inputSVfit_180GeV.append(test_inputSVfit_selected[g,:])
        ditaumass_180GeV.append(ditaumass_loopvalue)
        ditaumasspt_180GeV.append(test_ditaumasspt_selected[g,:])
        ditaumassEpxpypz_180GeV.append(test_ditaumassEpxpypz_selected[g,:])
        ditauEpxpypz_180GeV.append(test_ditauEpxpypz_selected[g,:])
        ditaumassE_180GeV.append(test_ditaumassE_selected[g,:])
        ditaumassptE_180GeV.append(test_ditaumassptE_selected[g,:])
    if 249.0 < ditaumass_loopvalue and 251.0 > ditaumass_loopvalue:
        inputNN_250GeV.append(test_inputNN_selected[g,:])
        inputSVfit_250GeV.append(test_inputSVfit_selected[g,:])
        ditaumass_250GeV.append(ditaumass_loopvalue)
        ditaumasspt_250GeV.append(test_ditaumasspt_selected[g,:])
        ditaumassEpxpypz_250GeV.append(test_ditaumassEpxpypz_selected[g,:])
        ditauEpxpypz_250GeV.append(test_ditauEpxpypz_selected[g,:])
        ditaumassE_250GeV.append(test_ditaumassE_selected[g,:])
        ditaumassptE_250GeV.append(test_ditaumassptE_selected[g,:])

inputNN_180GeV = numpy.array(inputNN_180GeV,numpy.float64)
inputSVfit_180GeV = numpy.array(inputSVfit_180GeV,numpy.float64)
ditaumasspt_180GeV = numpy.array(ditaumasspt_180GeV,numpy.float64)
ditaumassEpxpypz_180GeV = numpy.array(ditaumassEpxpypz_180GeV,numpy.float64)
ditauEpxpypz_180GeV = numpy.array(ditauEpxpypz_180GeV,numpy.float64)
ditaumassE_180GeV = numpy.array(ditaumassE_180GeV,numpy.float64)
ditaumassptE_180GeV = numpy.array(ditaumassptE_180GeV,numpy.float64)
inputNN_250GeV = numpy.array(inputNN_250GeV,numpy.float64)
inputSVfit_250GeV = numpy.array(inputSVfit_250GeV,numpy.float64)
ditaumasspt_250GeV = numpy.array(ditaumasspt_250GeV,numpy.float64)
ditaumassEpxpypz_250GeV = numpy.array(ditaumassEpxpypz_250GeV,numpy.float64)
ditauEpxpypz_250GeV = numpy.array(ditauEpxpypz_250GeV,numpy.float64)
ditaumassE_250GeV = numpy.array(ditaumassE_250GeV,numpy.float64)
ditaumassptE_250GeV = numpy.array(ditaumassptE_250GeV,numpy.float64)


def scale_ditaumass(input_list,control_list,fixed_length):
    decaymode_count = 0
    loop_length = 1000
    fulllep_fixed_length = int(round(0.1226*loop_length))
    semilep_fixed_length = int(round(0.4553*loop_length))
    fullhad_fixed_length = int(round(0.422* loop_length))
    output_list = []
    for i,value in enumerate(control_list[:,0]):
        if decaymode_count < fixed_length:
            if decaymode_count % 999 == 0:
                decaymode_count_fulllep = 0
                decaymode_count_semilep = 0
                decaymode_count_fullhad = 0
            if control_list[i,0] == 1.0:
                if decaymode_count_fulllep < fulllep_fixed_length:
                    output_list.append(input_list[i])
                    decaymode_count_fulllep += 1
                    decaymode_count += 1
            if control_list[i,1] == 1.0 or control_list[i,2] == 1.0:
                if decaymode_count_semilep < semilep_fixed_length:
                    output_list.append(input_list[i])
                    decaymode_count_semilep += 1
                    decaymode_count += 1
            if control_list[i,3] == 1.0:
                if decaymode_count_fullhad < fullhad_fixed_length:
                    output_list.append(input_list[i])
                    decaymode_count_fullhad += 1
                    decaymode_count += 1
    return output_list

def scale_inputs(input_list,control_list,fixed_length):
    decaymode_count = 0
    loop_length = 1000
    fulllep_fixed_length = int(round(0.1226*loop_length))
    semilep_fixed_length = int(round(0.4553*loop_length))
    fullhad_fixed_length = int(round(0.422* loop_length))
    output_list = []
    for i,value in enumerate(control_list[:,0]):
        if decaymode_count < fixed_length:
            if decaymode_count % 999 == 0:
                decaymode_count_fulllep = 0
                decaymode_count_semilep = 0
                decaymode_count_fullhad = 0
            if control_list[i,0] == 1.0:
                if decaymode_count_fulllep < fulllep_fixed_length:
                    output_list.append(input_list[i,:])
                    decaymode_count_fulllep += 1
                    decaymode_count += 1
            if control_list[i,1] == 1.0 or control_list[i,2] == 1.0:
                if decaymode_count_semilep < semilep_fixed_length:
                    output_list.append(input_list[i,:])
                    decaymode_count_semilep += 1
                    decaymode_count += 1
            if control_list[i,3] == 1.0:
                if decaymode_count_fullhad < fullhad_fixed_length:
                    output_list.append(input_list[i,:])
                    decaymode_count_fullhad += 1
                    decaymode_count += 1
    output_list = numpy.array(output_list,numpy.float64)
    return output_list


test_ditaumass_180GeV = scale_ditaumass(ditaumass_180GeV,inputNN_180GeV,12000)
test_inputSVfit_180GeV = scale_inputs(inputSVfit_180GeV,inputNN_180GeV,12000)
test_ditaumasspt_180GeV = scale_inputs(ditaumasspt_180GeV,inputNN_180GeV,12000)
test_ditaumassEpxpypz_180GeV = scale_inputs(ditaumassEpxpypz_180GeV,inputNN_180GeV,12000)
test_ditauEpxpypz_180GeV = scale_inputs(ditauEpxpypz_180GeV,inputNN_180GeV,12000)
test_ditaumassE_180GeV = scale_inputs(ditaumassE_180GeV,inputNN_180GeV,12000)
test_ditaumassptE_180GeV = scale_inputs(ditaumassptE_180GeV,inputNN_180GeV,12000)
test_inputNN_180GeV = scale_inputs(inputNN_180GeV,inputNN_180GeV,12000)
test_ditaumass_250GeV = scale_ditaumass(ditaumass_250GeV,inputNN_250GeV,12000)
test_inputSVfit_250GeV = scale_inputs(inputSVfit_250GeV,inputNN_250GeV,12000)
test_ditaumasspt_250GeV = scale_inputs(ditaumasspt_250GeV,inputNN_250GeV,12000)
test_ditaumassEpxpypz_250GeV = scale_inputs(ditaumassEpxpypz_250GeV,inputNN_250GeV,12000)
test_ditauEpxpypz_250GeV = scale_inputs(ditauEpxpypz_250GeV,inputNN_250GeV,12000)
test_ditaumassE_250GeV = scale_inputs(ditaumassE_250GeV,inputNN_250GeV,12000)
test_ditaumassptE_250GeV = scale_inputs(ditaumassptE_250GeV,inputNN_250GeV,12000)
test_inputNN_250GeV = scale_inputs(inputNN_250GeV,inputNN_250GeV,12000)


decaymode_180GeV_test_count = 0
decaymode_180GeV_test_count_fulllep = 0
decaymode_180GeV_test_count_semilep = 0
decaymode_180GeV_test_count_fullhad = 0
for i,value in enumerate(test_inputNN_180GeV[:,0]):
    decaymode_180GeV_test_count += 1
    if test_inputNN_180GeV[i,0] == 1.0:
        decaymode_180GeV_test_count_fulllep += 1
    if test_inputNN_180GeV[i,1] == 1.0 or test_inputNN_180GeV[i,2] == 1.0:
        decaymode_180GeV_test_count_semilep += 1
    if test_inputNN_180GeV[i,3] == 1.0:
        decaymode_180GeV_test_count_fullhad += 1
print "decaymode_180GeV_test_count:",decaymode_180GeV_test_count
print "decaymode_180GeV_test_count_fulllep:",decaymode_180GeV_test_count_fulllep
print "decaymode_180GeV_test_count_semilep:",decaymode_180GeV_test_count_semilep
print "decaymode_180GeV_test_count_fullhad:",decaymode_180GeV_test_count_fullhad


decaymode_250GeV_test_count = 0
decaymode_250GeV_test_count_fulllep = 0
decaymode_250GeV_test_count_semilep = 0
decaymode_250GeV_test_count_fullhad = 0
for i,value in enumerate(test_inputNN_250GeV[:,0]):
    decaymode_250GeV_test_count += 1
    if test_inputNN_250GeV[i,0] == 1.0:
        decaymode_250GeV_test_count_fulllep += 1
    if test_inputNN_250GeV[i,1] == 1.0 or test_inputNN_250GeV[i,2] == 1.0:
        decaymode_250GeV_test_count_semilep += 1
    if test_inputNN_250GeV[i,3] == 1.0:
        decaymode_250GeV_test_count_fullhad += 1
print "decaymode_250GeV_test_count:",decaymode_250GeV_test_count
print "decaymode_250GeV_test_count_fulllep:",decaymode_250GeV_test_count_fulllep
print "decaymode_250GeV_test_count_semilep:",decaymode_250GeV_test_count_semilep
print "decaymode_250GeV_test_count_fullhad:",decaymode_250GeV_test_count_fullhad

histtrainditaumasscheck = ROOT.TH1D("trainditaumasscheck","train sample of neural network",350,0,350)
histtrainditaumasscheck.GetXaxis().SetTitle("di-#tau_{gen} mass [GeV]")
histtrainditaumasscheck.GetYaxis().SetTitle("number of occurence")
histtrainditaumasscheck.GetYaxis().SetTitleOffset(1.3)
histtrainditaumasscheck.SetStats(0)

for j in train_ditaumass_selected:
    histtrainditaumasscheck.Fill(j)


canv = ROOT.TCanvas("nninput")
histtrainditaumasscheck.Draw()

img = ROOT.TImage.Create()
img.FromPad(canv)
img.WriteImage("nninput_small.png")


overfit_inputNN_selected = train_inputNN_selected[0:len(test_ditaumass_selected),:]
overfit_ditaumass_selected = train_ditaumass_selected[0:len(test_ditaumass_selected)]

"""
#########################################################################
#################  choose size of used new dataset ######################
new_fixed_dataset_length = 12010
new_fixed_train_length = 0
new_fixed_test_length = 12000
savefile_name = "dy_nostand_small"

#new_list_name = "/mnt/t3nfs01/data01/shome/pbaertsc/tauinitial/CMSSW_8_0_25/src/XtautauML/batch_output/reg_ditau_mass_higgs_100GeV.csv"
#new_list_name = "/mnt/t3nfs01/data01/shome/pbaertsc/tauinitial/CMSSW_8_0_25/src/XtautauML/batch_output/reg_ditau_mass_higgs_110GeV.csv"
#new_list_name = "/mnt/t3nfs01/data01/shome/pbaertsc/tauinitial/CMSSW_8_0_25/src/XtautauML/batch_output/reg_ditau_mass_higgs_125GeV.csv"
#new_list_name = "/mnt/t3nfs01/data01/shome/pbaertsc/tauinitial/CMSSW_8_0_25/src/XtautauML/batch_output/reg_ditau_mass_higgs_140GeV.csv"
new_list_name = "/mnt/t3nfs01/data01/shome/pbaertsc/tauinitial/CMSSW_8_0_25/src/XtautauML/batch_output/reg_ditau_mass_dy.csv"
new_dataframe_ditaumass = pandas.read_csv(new_list_name,delim_whitespace=False,header=None)
new_dataframe_ditaumass_shuffled = new_dataframe_ditaumass.sample(frac=1,random_state =1337)
new_dataset_ditaumass = new_dataframe_ditaumass_shuffled.values
new_dataset_total_length = len(new_dataset_ditaumass[:,0])

new_inputNN = []
new_inputSVfit =[]
new_ditaumass = []
new_ditauvismass = []
new_ditaumasspt = []
new_ditaumassEpxpypz = []
new_ditauEpxpypz = []
new_ditaumassE = []
new_ditaumassptE = []
new_ditaucollinearmass = []
new_decaymode_count = 0
new_decaymode_count_fulllep = 0
new_decaymode_count_semilep = 0
new_decaymode_count_fullhad = 0
new_loop_length = 100

newhistCOV00 = ROOT.TH1D("newCOV00","histogram of COV00",100,-20,20)
newhistCOV11 = ROOT.TH1D("newCOV11","histogram of COV11",100,-20,20)

for i in range(0,new_fixed_dataset_length):
    genMissingET_MET = new_dataset_ditaumass[i,26]
    genMissingET_Phi = new_dataset_ditaumass[i,27]
    MissingET_MET = new_dataset_ditaumass[i,28]
    MissingET_Phi = new_dataset_ditaumass[i,29]
    genMETpx = genMissingET_MET*numpy.cos(genMissingET_Phi)
    genMETpy = genMissingET_MET*numpy.sin(genMissingET_Phi)
    METpx = MissingET_MET*numpy.cos(MissingET_Phi)
    METpy = MissingET_MET*numpy.sin(MissingET_Phi)
    METCOV00 = METpx-genMETpx
    METCOV11 = METpy-genMETpy
    newhistCOV00.Fill(METCOV00)
    newhistCOV11.Fill(METCOV11)

newhistCOV00.Fit("gaus")
COV00_fit = newhistCOV00.GetFunction("gaus")
COV00_width = COV00_fit.GetParameter(2)
newhistCOV11.Fit("gaus")
COV11_fit = newhistCOV11.GetFunction("gaus")
COV11_width = COV11_fit.GetParameter(2)
COV_width_mean = (COV00_width+COV11_width)/2
METCOV = ROOT.TMath.Power(COV_width_mean,2.)

for i in range(0,new_dataset_total_length):
    tau1_pt = new_dataset_ditaumass[i,0]
    tau1_eta = new_dataset_ditaumass[i,1] 
    tau1_phi = new_dataset_ditaumass[i,2]
    tau1_mass = new_dataset_ditaumass[i,3]
    vistau1_pt = new_dataset_ditaumass[i,4]
    vistau1_eta = new_dataset_ditaumass[i,5]
    vistau1_phi = new_dataset_ditaumass[i,6]
    vistau1_mass = new_dataset_ditaumass[i,7]
    vistau1_att = new_dataset_ditaumass[i,8]
    vistau1_prongs = new_dataset_ditaumass[i,9]
    vistau1_pi0 = new_dataset_ditaumass[i,10]
    tau2_pt = new_dataset_ditaumass[i,11]
    tau2_eta = new_dataset_ditaumass[i,12] 
    tau2_phi = new_dataset_ditaumass[i,13]
    tau2_mass = new_dataset_ditaumass[i,14]
    vistau2_pt = new_dataset_ditaumass[i,15]
    vistau2_eta = new_dataset_ditaumass[i,16]
    vistau2_phi = new_dataset_ditaumass[i,17]
    vistau2_mass = new_dataset_ditaumass[i,18]
    vistau2_att = new_dataset_ditaumass[i,19]
    vistau2_prongs = new_dataset_ditaumass[i,20]
    vistau2_pi0 = new_dataset_ditaumass[i,21]
    nu_pt = new_dataset_ditaumass[i,22]
    nu_eta = new_dataset_ditaumass[i,23]
    nu_phi = new_dataset_ditaumass[i,24]
    nu_mass = new_dataset_ditaumass[i,25]
    genMissingET_MET = new_dataset_ditaumass[i,26]
    genMissingET_Phi = new_dataset_ditaumass[i,27]
    MissingET_MET = new_dataset_ditaumass[i,28]
    MissingET_Phi = new_dataset_ditaumass[i,29]
    genMETpx = genMissingET_MET*numpy.cos(genMissingET_Phi)
    genMETpy = genMissingET_MET*numpy.sin(genMissingET_Phi)
    METpx = MissingET_MET*numpy.cos(MissingET_Phi)
    METpy = MissingET_MET*numpy.sin(MissingET_Phi)
    v_tau1 = ROOT.TLorentzVector()
    v_tau1.SetPtEtaPhiM(tau1_pt,tau1_eta,tau1_phi,tau1_mass)
    v_tau2 = ROOT.TLorentzVector()
    v_tau2.SetPtEtaPhiM(tau2_pt,tau2_eta,tau2_phi,tau2_mass)
    v_vistau1 = ROOT.TLorentzVector()
    v_vistau1.SetPtEtaPhiM(vistau1_pt,vistau1_eta,vistau1_phi,vistau1_mass)
    v_vistau2 = ROOT.TLorentzVector()
    v_vistau2.SetPtEtaPhiM(vistau2_pt,vistau2_eta,vistau2_phi,vistau2_mass)
    v_nu = ROOT.TLorentzVector()
    v_nu.SetPtEtaPhiM(nu_pt,nu_eta,nu_phi,nu_mass)
    v_mot = v_vistau1+v_vistau2+v_nu
    v_vismot = v_vistau1+v_vistau2
    ditaumass_value = v_mot.M()
    ditauvismass_value = v_vismot.M()
    pt_nu = v_nu.Pt()
    nu_px = v_nu.Px()
    nu_py = v_nu.Py()
    vistau1_decaymode = int(5*(vistau1_prongs-1)+vistau1_pi0)
    vistau2_decaymode = int(5*(vistau2_prongs-1)+vistau2_pi0)
    vistau1_E = v_vistau1.E()
    vistau2_E = v_vistau2.E()
    vismass = v_vismot.M()
    p_vis = v_vismot.P()
    pt_vis = v_vismot.Pt()
    pt_nu = v_nu.Pt()
    pt = v_mot.Pt()
    E = v_mot.E()
    px = v_mot.Px()
    py = v_mot.Py()
    pz = v_mot.Pz()
    ditaumass_collinear = vismass/numpy.sqrt(vistau1_pt/(vistau1_pt+pt_nu)*vistau2_pt/(vistau2_pt+pt_nu))
    mass_no_pz = v_vismot.E()**2-v_vismot.Pz()**2-pt_vis**2
    if new_decaymode_count % 100 == 0:
        new_loop_length += 100
    new_fulllep_fixed_length = int(round(0.1226*new_loop_length))
    new_semilep_fixed_length = int(round(0.4553*new_loop_length))
    new_fullhad_fixed_length = int(round(0.422* new_loop_length))
    if new_decaymode_count < new_fixed_dataset_length:
        if vistau1_att in (1,2) and vistau2_att in (1,2) and new_decaymode_count_fulllep < new_fulllep_fixed_length:
            new_inputNN.append([1.0,0.0,0.0,0.0,vistau1_pt,vistau1_eta,vistau1_phi,vistau1_E,vistau1_mass,vistau2_pt,vistau2_eta,vistau2_phi,vistau2_E,vistau2_mass, genMissingET_MET,genMissingET_Phi,ditaumass_collinear])
            new_inputSVfit.append([vistau1_pt,vistau1_eta,vistau1_phi,vistau1_mass,vistau1_att,vistau1_prongs,vistau1_pi0,vistau2_pt,vistau2_eta,vistau2_phi,vistau2_mass,vistau2_att,vistau2_prongs,vistau2_pi0,METpx,METpy,METCOV,ditaumass_value,ditauvismass_value])
            new_ditaumass.append(ditaumass_value)
            new_ditaumasspt.append([ditaumass_value,pt])
            new_ditaumassEpxpypz.append([ditaumass_value,E,px,py,pz])
            new_ditauEpxpypz.append([E,px,py,pz])
            new_ditaumassE.append([ditaumass_value,E])
            new_ditaumassptE.append([ditaumass_value,pt,E])
            new_ditauvismass.append(ditauvismass_value)
            new_ditaucollinearmass.append(ditaumass_collinear)
            new_decaymode_count_fulllep += 1
            new_decaymode_count += 1
        elif vistau1_att in (1,2) and vistau2_att == 3 and new_decaymode_count_semilep < new_semilep_fixed_length:
            new_inputNN.append([0.0,1.0,0.0,0.0,vistau1_pt,vistau1_eta,vistau1_phi,vistau1_E,vistau1_mass,vistau2_pt,vistau2_eta,vistau2_phi,vistau2_E,vistau2_mass, genMissingET_MET,genMissingET_Phi,ditaumass_collinear])
            new_inputSVfit.append([vistau1_pt,vistau1_eta,vistau1_phi,vistau1_mass,vistau1_att,vistau1_prongs,vistau1_pi0,vistau2_pt,vistau2_eta,vistau2_phi,vistau2_mass,vistau2_att,vistau2_prongs,vistau2_pi0,METpx,METpy,METCOV,ditaumass_value,ditauvismass_value])
            new_ditaumass.append(ditaumass_value)
            new_ditaumasspt.append([ditaumass_value,pt])
            new_ditaumassEpxpypz.append([ditaumass_value,E,px,py,pz])
            new_ditauEpxpypz.append([E,px,py,pz])
            new_ditaumassE.append([ditaumass_value,E])
            new_ditaumassptE.append([ditaumass_value,pt,E])
            new_ditauvismass.append(ditauvismass_value)
            new_ditaucollinearmass.append(ditaumass_collinear)
            new_decaymode_count_semilep += 1
            new_decaymode_count += 1
        elif vistau1_att == 3 and vistau2_att in (1,2) and new_decaymode_count_semilep < new_semilep_fixed_length:
            new_inputNN.append([0.0,0.0,1.0,0.0,vistau1_pt,vistau1_eta,vistau1_phi,vistau1_E,vistau1_mass,vistau2_pt,vistau2_eta,vistau2_phi,vistau2_E,vistau2_mass, genMissingET_MET,genMissingET_Phi,ditaumass_collinear])
            new_inputSVfit.append([vistau1_pt,vistau1_eta,vistau1_phi,vistau1_mass,vistau1_att,vistau1_prongs,vistau1_pi0,vistau2_pt,vistau2_eta,vistau2_phi,vistau2_mass,vistau2_att,vistau2_prongs,vistau2_pi0,METpx,METpy,METCOV,ditaumass_value,ditauvismass_value])
            new_ditaumass.append(ditaumass_value)
            new_ditaumasspt.append([ditaumass_value,pt])
            new_ditaumassEpxpypz.append([ditaumass_value,E,px,py,pz])
            new_ditauEpxpypz.append([E,px,py,pz])
            new_ditaumassE.append([ditaumass_value,E])
            new_ditaumassptE.append([ditaumass_value,pt,E])
            new_ditauvismass.append(ditauvismass_value)
            new_ditaucollinearmass.append(ditaumass_collinear)
            new_decaymode_count_semilep += 1
            new_decaymode_count += 1
        elif vistau1_att == 3 and vistau2_att == 3 and new_decaymode_count_fullhad < new_fullhad_fixed_length:
            new_inputNN.append([0.0,0.0,0.0,1.0,vistau1_pt,vistau1_eta,vistau1_phi,vistau1_E,vistau1_mass,vistau2_pt,vistau2_eta,vistau2_phi,vistau2_E,vistau2_mass, genMissingET_MET,genMissingET_Phi,ditaumass_collinear])
            new_inputSVfit.append([vistau1_pt,vistau1_eta,vistau1_phi,vistau1_mass,vistau1_att,vistau1_prongs,vistau1_pi0,vistau2_pt,vistau2_eta,vistau2_phi,vistau2_mass,vistau2_att,vistau2_prongs,vistau2_pi0,METpx,METpy,METCOV,ditaumass_value,ditauvismass_value])
            new_ditaumass.append(ditaumass_value)
            new_ditaumasspt.append([ditaumass_value,pt])
            new_ditaumassEpxpypz.append([ditaumass_value,E,px,py,pz])
            new_ditauEpxpypz.append([E,px,py,pz])
            new_ditaumassE.append([ditaumass_value,E])
            new_ditaumassptE.append([ditaumass_value,pt,E])
            new_ditauvismass.append(ditauvismass_value)
            new_ditaucollinearmass.append(ditaumass_collinear)
            new_decaymode_count_fullhad += 1 
            new_decaymode_count += 1

new_inputNN = numpy.array(new_inputNN,numpy.float64)
new_inputSVfit = numpy.array(new_inputSVfit,numpy.float64)
new_ditaumasspt = numpy.array(new_ditaumasspt,numpy.float64)
new_ditaumassEpxpypz = numpy.array(new_ditaumassEpxpypz,numpy.float64)
new_ditauEpxpypz = numpy.array(new_ditauEpxpypz,numpy.float64)
new_ditaumassE = numpy.array(new_ditaumassE,numpy.float64)
new_ditaumassptE = numpy.array(new_ditaumassptE,numpy.float64)
new_dataset_length = len(new_inputNN[:,0])
new_ditaumass_length = len(new_ditaumass)
new_ditaumasspt_length = len(new_ditaumasspt[:,0])
new_ditaumassEpxpypz_length = len(new_ditaumassEpxpypz[:,0])
new_ditauEpxpypz_length = len(new_ditauEpxpypz[:,0])
new_ditaumassE_length = len(new_ditaumassE[:,0])
new_ditaumassptE_length = len(new_ditaumassptE[:,0])

print "nninput length:",new_dataset_length
print "nntarget mass length:",new_ditaumass_length
print "nntarget masspt length:",new_ditaumasspt_length
print "nntarget massEpxpypz length:",new_ditaumassEpxpypz_length
print "nntarget Epxpypz length:",new_ditauEpxpypz_length
print "nntarget massE length:",new_ditaumassE_length
print "nntarget massptE length:",new_ditaumassptE_length
print ""

new_train_inputNN = new_inputNN[new_fixed_test_length:,:]
new_train_inputSVfit = new_inputSVfit[new_fixed_test_length:,:]
new_train_ditaumass = new_ditaumass[new_fixed_test_length:]
new_train_ditaumasspt = new_ditaumasspt[new_fixed_test_length:,:]
new_train_ditaumassEpxpypz = new_ditaumassEpxpypz[new_fixed_test_length:,:]
new_train_ditauEpxpypz = new_ditauEpxpypz[new_fixed_test_length:,:]
new_train_ditaumassE = new_ditaumassE[new_fixed_test_length:,:]
new_train_ditaumassptE = new_ditaumassptE[new_fixed_test_length:,:]
new_train_ditauvismass = new_ditauvismass[new_fixed_test_length:]
new_test_inputNN = new_inputNN[0:new_fixed_test_length,:]
new_test_inputSVfit = new_inputSVfit[0:new_fixed_test_length,:]
new_test_ditaumass = new_ditaumass[0:new_fixed_test_length]
new_test_ditaumasspt = new_ditaumasspt[0:new_fixed_test_length,:]
new_test_ditaumassEpxpypz = new_ditaumassEpxpypz[0:new_fixed_test_length,:]
new_test_ditauEpxpypz = new_ditauEpxpypz[0:new_fixed_test_length,:]
new_test_ditaumassE = new_ditaumassE[0:new_fixed_test_length,:]
new_test_ditaumassptE = new_ditaumassptE[0:new_fixed_test_length,:]
new_test_ditauvismass = new_ditauvismass[0:new_fixed_test_length]
new_test_ditaucollinearmass = new_ditaucollinearmass[0:new_fixed_test_length]

new_test_inputNN_length = len(new_test_inputNN[:,0])
new_test_ditaumass_length = len(new_test_ditaumass)
new_test_ditaumasspt_length = len(new_test_ditaumasspt[:,0])
new_test_ditaumassEpxpypz_length = len(new_test_ditaumassEpxpypz[:,0])
new_test_ditauEpxpypz_length = len(new_test_ditauEpxpypz[:,0])
new_test_ditaumassE_length = len(new_test_ditaumassE[:,0])
new_test_ditaumassptE_length = len(new_test_ditaumassptE[:,0])

print "test nninput length:",new_test_inputNN_length
print "test nntarget mass length:",new_test_ditaumass_length
print "test nntarget masspt length:",new_test_ditaumasspt_length
print "test nntarget massEpxpypz length:",new_test_ditaumassEpxpypz_length
print "test nntarget Epxpypz length:",new_test_ditauEpxpypz_length
print "test nntarget massE length:",new_test_ditaumassE_length
print "test nntarget massptE length:",new_test_ditaumassptE_length

new_decaymode_train_count = 0
new_decaymode_train_count_fulllep = 0
new_decaymode_train_count_semilep = 0
new_decaymode_train_count_fullhad = 0

for i,value in enumerate(new_train_inputNN[:,0]):
    new_decaymode_train_count += 1
    if new_train_inputNN[i,0] == 1.0:
        new_decaymode_train_count_fulllep += 1
    if new_train_inputNN[i,1] == 1.0 or new_train_inputNN[i,2] == 1.0:
        new_decaymode_train_count_semilep += 1
    if new_train_inputNN[i,3] == 1.0:
        new_decaymode_train_count_fullhad += 1
print "new_decaymode_train_count:",new_decaymode_train_count
print "new_decaymode_train_count_fulllep:",new_decaymode_train_count_fulllep
print "new_decaymode_train_count_semilep:",new_decaymode_train_count_semilep
print "new_decaymode_train_count_fullhad:",new_decaymode_train_count_fullhad


new_decaymode_test_count = 0
new_decaymode_test_count_fulllep = 0
new_decaymode_test_count_semilep = 0
new_decaymode_test_count_fullhad = 0
for i,value in enumerate(new_test_inputNN[:,0]):
    new_decaymode_test_count += 1
    if new_test_inputNN[i,0] == 1.0:
        new_decaymode_test_count_fulllep += 1
    if new_test_inputNN[i,1] == 1.0 or new_test_inputNN[i,2] == 1.0:
        new_decaymode_test_count_semilep += 1
    if new_test_inputNN[i,3] == 1.0:
        new_decaymode_test_count_fullhad += 1
print "new_decaymode_test_count:",new_decaymode_test_count
print "new_decaymode_test_count_fulllep:",new_decaymode_test_count_fulllep
print "new_decaymode_test_count_semilep:",new_decaymode_test_count_semilep
print "new_decaymode_test_count_fullhad:",new_decaymode_test_count_fullhad
"""
"""
test_inputNN_100GeV_stand = test_inputNN_100GeV
test_inputNN_125GeV_stand = test_inputNN_125GeV
test_inputNN_140GeV_stand = test_inputNN_140GeV
test_inputNN_180GeV_stand = test_inputNN_180GeV
test_inputNN_250GeV_stand = test_inputNN_250GeV
test_inputNN_selected_stand = test_inputNN_selected
new_test_inputNN_stand = new_test_inputNN

test_inputNN_selected = numpy.array(test_inputNN_selected_stand,numpy.float64)
test_inputNN_100GeV_stand = numpy.array(test_inputNN_100GeV_stand,numpy.float64)        
test_inputNN_125GeV_stand = numpy.array(test_inputNN_125GeV_stand,numpy.float64)
test_inputNN_140GeV_stand = numpy.array(test_inputNN_140GeV_stand,numpy.float64)
test_inputNN_180GeV_stand = numpy.array(test_inputNN_180GeV_stand,numpy.float64)
test_inputNN_250GeV_stand = numpy.array(test_inputNN_250GeV_stand,numpy.float64)
new_test_inputNN_stand = numpy.array(new_test_inputNN_stand,numpy.float64)

###########     standardization of input data     ##################

for j in range(4,len(train_inputNN_selected[0,:])):
    mean = numpy.mean(train_inputNN_selected[:,j])
    std = numpy.std(train_inputNN_selected[:,j])
    for i in range(0,len(test_ditaumass_selected)):
        value = test_inputNN_selected[i,j]
        new_value = (value-mean)/std
        test_inputNN_selected_stand[i,j] = new_value
    for k in range(0,len(test_ditaumass_125GeV)):
        value = test_inputNN_125GeV[k,j]
        new_value = (value-mean)/std
        test_inputNN_125GeV_stand[k,j] = new_value
    for g in range(0,len(test_ditaumass_140GeV)):
        value = test_inputNN_140GeV[g,j]
        new_value = (value-mean)/std
        test_inputNN_140GeV_stand[g,j] = new_value
    for m in range(0,len(test_ditaumass_180GeV)):
        value = test_inputNN_180GeV[m,j]
        new_value = (value-mean)/std
        test_inputNN_180GeV_stand[m,j] = new_value
    for p in range(0,len(test_ditaumass_250GeV)):
        value = test_inputNN_250GeV[p,j]
        new_value = (value-mean)/std
        test_inputNN_250GeV_stand[p,j] = new_value
    for i in range(0,len(new_test_ditaumass)):
        value = new_test_inputNN[i,j]
        new_value = (value-mean)/std
        new_test_inputNN_stand[i,j] = new_value

test_inputNN_selected = numpy.array(test_inputNN_selected_stand,numpy.float64)        
test_inputNN_125GeV_stand = numpy.array(test_inputNN_125GeV_stand,numpy.float64)
test_inputNN_140GeV_stand = numpy.array(test_inputNN_140GeV_stand,numpy.float64)
test_inputNN_180GeV_stand = numpy.array(test_inputNN_180GeV_stand,numpy.float64)
test_inputNN_250GeV_stand = numpy.array(test_inputNN_250GeV_stand,numpy.float64)
new_test_inputNN_stand = numpy.array(new_test_inputNN_stand,numpy.float64)

train_stand = preprocessing.scale(train_inputNN_selected[:,4:])
train_inputNN_set = []
test_inputNN_set = []
for j in range(0,len(train_ditaumass_selected)):
    train_inputNN_set.append([train_inputNN_selected[j,0],train_inputNN_selected[j,1],train_inputNN_selected[j,2],train_inputNN_selected[j,3],train_stand[j,0],train_stand[j,1],train_stand[j,2],train_stand[j,3],train_stand[j,4],train_stand[j,5],train_stand[j,6],train_stand[j,7],train_stand[j,8],train_stand[j,9],train_stand[j,10],train_stand[j,11],train_stand[j,12]])

train_inputNN_selected = numpy.array(train_inputNN_set,numpy.float64)

test_inputNN_stand = test_inputNN
for j in range(4,len(test_inputNN[0,:])):
    mean = numpy.mean(test_inputNN[:,j])
    std = numpy.std(test_inputNN[:,j])
    for i in range(0,len(test_ditaumass)):
        value = test_inputNN[i,j]
        new_value = (value-mean)/std
        test_inputNN_stand[i,j] = new_value

test_inputNN_stand = numpy.array(test_inputNN_stand,numpy.float64)
"""

#############       save neural network inputs to file        ###########################


numpy.savetxt("nninput_train_nostand_novismassandcollmass.csv", train_inputNN_selected, delimiter=",")
numpy.savetxt("nntarget_train_nostand_novismassandcollmass.csv", train_ditaumass_selected, delimiter=",")
numpy.savetxt("nninput_test_nostand_novismassandcollmass.csv", test_inputNN_selected, delimiter=",")
numpy.savetxt("nntarget_test_nostand_novismassandcollmass.csv", test_ditaumass_selected, delimiter=",")


"""
nninput_name = "nninput_test_%s.csv" % (savefile_name)
svfitinput_name = "svfitinput_test_%s.csv" % (savefile_name)
nntarget_name = "nntarget_test_%s.csv" % (savefile_name)
nntarget_masspt_name = "nntarget_masspt_test_%s.csv" % (savefile_name)
nntarget_massEpxpypz_name = "nntarget_massEpxpypz_test_%s.csv" % (savefile_name)
nntarget_Epxpypz_name = "nntarget_Epxpypz_test_%s.csv" % (savefile_name)
nntarget_massE_name = "nntarget_massE_test_%s.csv" % (savefile_name)
nntarget_massptE_name = "nntarget_massptE_test_%s.csv" % (savefile_name)
numpy.savetxt(nninput_name, new_test_inputNN, delimiter=",")
numpy.savetxt(svfitinput_name, new_test_inputSVfit, delimiter =",")
numpy.savetxt(nntarget_name, new_test_ditaumass, delimiter=",")
numpy.savetxt(nntarget_masspt_name, new_test_ditaumasspt, delimiter=",")
numpy.savetxt(nntarget_massEpxpypz_name, new_test_ditaumassEpxpypz, delimiter=",")
numpy.savetxt(nntarget_Epxpypz_name, new_test_ditauEpxpypz, delimiter=",")
numpy.savetxt(nntarget_massE_name, new_test_ditaumassE, delimiter=",")
numpy.savetxt(nntarget_massptE_name, new_test_ditaumassptE, delimiter=",")


numpy.savetxt("nninput_train_nostand_small.csv", train_inputNN_selected, delimiter=",")
numpy.savetxt("nntarget_train_nostand_small.csv", train_ditaumass_selected, delimiter=",")
numpy.savetxt("nntarget_masspt_train_nostand_small.csv", train_ditaumasspt_selected, delimiter=",")
numpy.savetxt("nntarget_massEpxpypz_train_nostand_small.csv", train_ditaumassEpxpypz_selected, delimiter=",")
numpy.savetxt("nntarget_Epxpypz_train_nostand_small.csv", train_ditauEpxpypz_selected, delimiter=",")
numpy.savetxt("nntarget_massE_train_nostand_small.csv", train_ditaumassE_selected, delimiter=",")
numpy.savetxt("nntarget_massptE_train_nostand_small.csv", train_ditaumassptE_selected, delimiter=",")
numpy.savetxt("nninput_test_nostand_small.csv", test_inputNN_selected, delimiter=",")
numpy.savetxt("nntarget_test_nostand_small.csv", test_ditaumass_selected, delimiter=",")
numpy.savetxt("nninput_test_nostand_small_fulllep.csv", test_inputNN_selected_fulllep, delimiter=",")
numpy.savetxt("nntarget_test_nostand_small_fulllep.csv", test_ditaumass_selected_fulllep, delimiter=",")
numpy.savetxt("nninput_test_nostand_small_semilep.csv", test_inputNN_selected_semilep, delimiter=",")
numpy.savetxt("nntarget_test_nostand_small_semilep.csv", test_ditaumass_selected_semilep, delimiter=",")
numpy.savetxt("nninput_test_nostand_small_fullhad.csv", test_inputNN_selected_fullhad, delimiter=",")
numpy.savetxt("nntarget_test_nostand_small_fullhad.csv", test_ditaumass_selected_fullhad, delimiter=",")
numpy.savetxt("ditauvismass_test_nostand_small.csv", test_ditauvismass_selected, delimiter=",")
numpy.savetxt("ditaucollinearmass_test_nostand_small.csv", test_ditaucollinearmass_selected, delimiter=",")
numpy.savetxt("svfitinput_test_nostand_small.csv", test_inputSVfit_selected, delimiter =",")
numpy.savetxt("svfitinput_test_nostand_small_fulllep.csv", test_inputSVfit_selected_fulllep, delimiter =",")
numpy.savetxt("svfitinput_test_nostand_small_semilep.csv", test_inputSVfit_selected_semilep, delimiter =",")
numpy.savetxt("svfitinput_test_nostand_small_fullhad.csv", test_inputSVfit_selected_fullhad, delimiter =",")
numpy.savetxt("nntarget_masspt_test_nostand_small.csv", test_ditaumasspt_selected, delimiter=",")
numpy.savetxt("nntarget_massEpxpypz_test_nostand_small.csv", test_ditaumassEpxpypz_selected, delimiter=",")
numpy.savetxt("nntarget_Epxpypz_test_nostand_small.csv", test_ditauEpxpypz_selected, delimiter=",")
numpy.savetxt("nntarget_massE_test_nostand_small.csv", test_ditaumassE_selected, delimiter=",")
numpy.savetxt("nntarget_massptE_test_nostand_small.csv", test_ditaumassptE_selected, delimiter=",")
numpy.savetxt("nninput_test_180GeV_nostand_small.csv", test_inputNN_180GeV, delimiter=",")
numpy.savetxt("svfitinput_test_180GeV_nostand_small.csv", test_inputSVfit_180GeV, delimiter=",")
numpy.savetxt("nninput_test_250GeV_nostand_small.csv", test_inputNN_250GeV, delimiter=",")
numpy.savetxt("svfitinput_test_250GeV_nostand_small.csv", test_inputSVfit_250GeV, delimiter=",")
numpy.savetxt("nntarget_test_180GeV_nostand_small.csv", test_ditaumass_180GeV, delimiter=",")
numpy.savetxt("nntarget_masspt_test_180GeV_nostand_small.csv", test_ditaumasspt_180GeV, delimiter=",")
numpy.savetxt("nntarget_massEpxpypz_test_180GeV_nostand_small.csv", test_ditaumassEpxpypz_180GeV, delimiter=",")
numpy.savetxt("nntarget_Epxpypz_test_180GeV_nostand_small.csv", test_ditauEpxpypz_180GeV, delimiter=",")
numpy.savetxt("nntarget_massE_test_180GeV_nostand_small.csv", test_ditaumassE_180GeV, delimiter=",")
numpy.savetxt("nntarget_massptE_test_180GeV_nostand_small.csv", test_ditaumassptE_180GeV, delimiter=",")
numpy.savetxt("nntarget_test_250GeV_nostand_small.csv", test_ditaumass_250GeV, delimiter=",")
numpy.savetxt("nntarget_masspt_test_250GeV_nostand_small.csv", test_ditaumasspt_250GeV, delimiter=",")
numpy.savetxt("nntarget_massEpxpypz_test_250GeV_nostand_small.csv", test_ditaumassEpxpypz_250GeV, delimiter=",")
numpy.savetxt("nntarget_Epxpypz_test_250GeV_nostand_small.csv", test_ditauEpxpypz_250GeV, delimiter=",")
numpy.savetxt("nntarget_massE_test_250GeV_nostand_small.csv", test_ditaumassE_250GeV, delimiter=",")
numpy.savetxt("nntarget_massptE_test_250GeV_nostand_small.csv", test_ditaumassptE_250GeV, delimiter=",")
"""
