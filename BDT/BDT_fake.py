import os, sys
os.environ['OMP_NUM_THREADS'] = "20"
import pandas as pd
import xgboost as xgb
from argparse import ArgumentParser
import numpy as np
from ROOT import TFile
from sklearn.model_selection import train_test_split
import uproot
from sklearn.metrics import accuracy_score, roc_curve, auc, RocCurveDisplay
from sklearn.preprocessing import LabelBinarizer
import pickle
import time
from array import array
import warnings
from matplotlib import pyplot
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import StratifiedKFold
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from samplenames import getsamples
from checkFiles import ensureDirectory
import shap

warnings.filterwarnings(action='ignore', category=DeprecationWarning) #ignore warning which is fixed in new version of scikit-learn

parser = ArgumentParser()
parser.add_argument('-t', '--train', dest="train", action='store_true', default=False)
parser.add_argument('-p', '--predict', dest="predict", action='store_true', default=False)
parser.add_argument('-e', '--evaluate', dest="evaluate", action='store_true', default=False)
parser.add_argument('-c', '--channel', dest='channel', type=str, default='mutau', action='store',)
parser.add_argument('-y', '--year',    dest='year', type=str, default='2018', action='store')
parser.add_argument('-n', '--NN',      dest='NN', action='store_true',default=False)
parser.add_argument('-s', '--sysvar', dest='sysvar', type=str, default='', action='store',choices=["jesTotalUp","jesTotalDown","jerUp","jerDown","met_unclusteredUp","met_unclusteredDown","jesAbsoluteUp","jesAbsoluteDown","jesAbsolute_2018Up","jesAbsolute_2018Down","jesAbsolute_2017Up","jesAbsolute_2017Down","jesAbsolute_2016Up","jesAbsolute_2016Down","jesBBEC1Up","jesBBEC1Down","jesBBEC1_2018Up","jesBBEC1_2018Down","jesBBEC1_2017Up","jesBBEC1_2017Down","jesBBEC1_2016Up","jesBBEC1_2016Down","jesEC2Up","jesEC2Down","jesEC2_2018Up","jesEC2_2018Down","jesEC2_2017Up","jesEC2_2017Down","jesEC2_2016Up","jesEC2_2016Down","jesFlavorQCDUp","jesFlavorQCDDown","jesHFUp","jesHFDown","jesHF_2018Up","jesHF_2018Down","jesHF_2017Up","jesHF_2017Down","jesHF_2016Up","jesHF_2016Down","jesRelativeBalUp","jesRelativeBalDown","jesRelativeSample_2018Up","jesRelativeSample_2018Down","jesRelativeSample_2017Up","jesRelativeSample_2017Down","jesRelativeSample_2016Up","jesRelativeSample_2016Down","scale_t_1prongUp","scale_t_1prongDown","scale_t_1prong1piUp","scale_t_1prong1piDown","scale_t_3prongUp","scale_t_3prongDown"])

args = parser.parse_args()
channel = args.channel
sysvar = args.sysvar
year = args.year
NN = args.NN
preVFP = ""


if year=="2016": #preVFP and postVFP combined for 2016
    preVFP="_comb"

if sysvar!="":
    sysvar="_"+sysvar

if NN:
    filedir = "/pnfs/psi.ch/cms/trivcat/store/user/pbaertsc/bbh/samples_UL%s%s%s_NN/"%(year,preVFP,sysvar)
    outdir = ensureDirectory("/pnfs/psi.ch/cms/trivcat/store/user/pbaertsc/bbh/samples_UL%s%s%s_NNBDT/%s/"%(year,preVFP,sysvar,channel))
else:
    filedir = "/pnfs/psi.ch/cms/trivcat/store/user/pbaertsc/bbh/samples_UL%s%s%s/"%(year,preVFP,sysvar)  
    outdir = ensureDirectory("/pnfs/psi.ch/cms/trivcat/store/user/pbaertsc/bbh/samples_UL%s%s%s_BDT/%s/"%(year,preVFP,sysvar,channel))
rootdir = "/work/pbaertsc/bbh/NanoTreeProducer/BDT/root/"

def getinputfromTree(inputlist):
    valuelist = []
    for label in inputlist:
        item = 'new_tree.%s'%label
        valuelist.append(eval(item))
    return np.array(valuelist).reshape((1,-1))


if sysvar=="":
    #samples = ['bbH_htt','ggH_bb_htt_inc','ggH_bb_htt_excl','intH_bb_htt','intH_htt','bbH_nobb_htt','ggH_htt_inc','ggH_htt_excl']
    samples = ['bbH_htt','ggH_bb_htt_inc','ggH_bb_htt_excl','intH_bb_htt','intH_htt','bbH_nobb_htt','ggH_htt_inc','ggH_htt_excl','data_obs','TTTo2L2Nu','TTToHadronic','TTToSemiLeptonic','WJets_incl','WJets_0J','WJets_1J','WJets_2J','DYJets_incl','DYJets_0J','DYJets_1J','DYJets_2J','ST_t_channel_antitop','ST_t_channel_top','ST_s_channel','ST_tW_antitop','ST_tW_top','VBF','ZH','ttH','WWTo2L2Nu','WWTo1L1Nu2Q','WWTo4Q','WZTo3LNu','WZTo2L2Q','WZTo1L3Nu','WZTo1L1Nu2Q','ZZTo4L','ZZTo2L2Q','ZZTo2Nu2Q']
else: #no data_obs for JEC variations
    samples =  ['bbH_htt','ggH_bb_htt_inc','ggH_bb_htt_excl','intH_bb_htt','intH_htt','WJets_incl','WJets_0J','WJets_1J','WJets_2J','DYJets_incl','DYJets_0J','DYJets_1J','DYJets_2J','TTTo2L2Nu','TTToHadronic','TTToSemiLeptonic','ST_t_channel_antitop','ST_t_channel_top','ST_s_channel','ST_tW_antitop','ST_tW_top','VBF','ZH','bbH_nobb_htt','ggH_htt_inc','ggH_htt_excl','ttH','WWTo2L2Nu','WWTo1L1Nu2Q','WWTo4Q','WZTo3LNu','WZTo2L2Q','WZTo1L3Nu','WZTo1L1Nu2Q','ZZTo4L','ZZTo2L2Q','ZZTo2Nu2Q']

   
name = "%s_UL%s%s%s"%(channel,year,preVFP,sysvar)
modelname = 'xgbmodel_%s_UL%s_fakeclass.sav'%(channel,year)

inputlist = ["H_mass","Jet1_btag","Jet1_pt","vis_mass","Dzeta","Jet2_btag","H_pt","DRHJ","HJ_pt","DEta","Jet2_pt","mt","collinear_mass","TauJ_mass"]
#mt 2016 better than 2018: Jet1_pt, H_pt, mt, Dzeta, DRHJ, HJ_pt, DEta, Jet2_pt, TauJ_mass


if channel=="mutau":
    selection_test = '(isHtoMuTau || isHtoMuTauAR) && Mu1_charge*Tau1_charge==-1 && dimuon_veto==0 && electron_veto==0 && extra_muon_veto==0 && Tau1_genmatch!=6 && mt<60. && nBjets_m>=1 && EventNumber%10>=4' #use Events with endnumber 4 5 6 7 8 9 for testing BDT
    selection_test_data = '(isHtoMuTau || isHtoMuTauAR) && Mu1_charge*Tau1_charge==-1 && dimuon_veto==0 && electron_veto==0 && extra_muon_veto==0 && mt<60. && nBjets_m>=1' #use Events with endnumber 4 5 6 7 8 9 for testing BDT
elif channel=="etau":
    selection_test = '(isHtoETau || isHtoETauAR) && Ele1_charge*Tau1_charge==-1 && dielectron_veto==0 && muon_veto==0 && extra_electron_veto==0 && Tau1_genmatch!=6 && mt<60. && nBjets_m>=1 && EventNumber%10>=4' #use Events with endnumber 4 5 6 7 8 9 for testing BDT
    selection_test_data = '(isHtoETau || isHtoETauAR) && Ele1_charge*Tau1_charge==-1 && dielectron_veto==0 && muon_veto==0 && extra_electron_veto==0 && Tau1_genmatch!=6 && mt<60. && nBjets_m>=1' #use Events with endnumber 4 5 6 7 8 9 for testing BDT


if args.train:
    file_signal_train = uproot.open("%sBDT_UL%s_%s_train_signal.root"%(rootdir,year,channel))
    file_tt_train = uproot.open("%sBDT_UL%s_%s_train_tt.root"%(rootdir,year,channel))
    file_dy_train = uproot.open("%sBDT_UL%s_%s_train_dy.root"%(rootdir,year,channel))
    file_fake_train = uproot.open("%sBDT_UL%s_%s_train_fake.root"%(rootdir,year,channel))
    file_signal_test = uproot.open("%sBDT_UL%s_%s_test_signal.root"%(rootdir,year,channel))
    file_tt_test = uproot.open("%sBDT_UL%s_%s_test_tt.root"%(rootdir,year,channel))
    file_dy_test = uproot.open("%sBDT_UL%s_%s_test_dy.root"%(rootdir,year,channel))
    file_fake_test = uproot.open("%sBDT_UL%s_%s_test_fake.root"%(rootdir,year,channel))

    tree_signal_train = file_signal_train["tree"]
    tree_tt_train = file_tt_train["tree"]
    tree_dy_train = file_dy_train["tree"]
    tree_fake_train = file_fake_train["tree"]
    tree_signal_test = file_signal_test["tree"]
    tree_tt_test = file_tt_test["tree"]
    tree_dy_test = file_dy_test["tree"]
    tree_fake_test = file_fake_test["tree"]
  
    signal_train = tree_signal_train.arrays(library="pd").sample(frac=1).reset_index(drop=True)
    tt_train = tree_tt_train.arrays(library="pd").sample(frac=1).reset_index(drop=True)
    dy_train = tree_dy_train.arrays(library="pd").sample(frac=1).reset_index(drop=True)
    fake_train = tree_fake_train.arrays(library="pd").sample(frac=1).reset_index(drop=True)
    signal_test = tree_signal_test.arrays(library="pd").sample(frac=1).reset_index(drop=True)
    tt_test = tree_tt_test.arrays(library="pd").sample(frac=1).reset_index(drop=True)
    dy_test = tree_dy_test.arrays(library="pd").sample(frac=1).reset_index(drop=True)
    fake_test = tree_fake_test.arrays(library="pd").sample(frac=1).reset_index(drop=True)
    
    
    dy_train_length = len(dy_train.index)
    dy_test_length = len(dy_test.index)
    signal_train_length = len(signal_train.index)
    signal_test_length = len(signal_test.index)
    fake_train_length = len(fake_train.index)
    fake_test_length = len(fake_test.index)
    train_length = min(dy_train_length,signal_train_length)
    test_length = min(dy_test_length,signal_test_length)
    dy_train = dy_train[:train_length]
    dy_test = dy_test[:test_length]
    signal_train = signal_train[:train_length]
    signal_test = signal_test[:test_length]
    tt_train = tt_train[:train_length]
    tt_test = tt_test[:test_length]
    fake_train = fake_train[:train_length]
    fake_test = fake_test[:test_length]

    print("dy train:",len(dy_train.index))
    print("dy test:",len(dy_test.index))
    print("signal train:",len(signal_train.index))
    print("signal test:",len(signal_test.index))
    print("tt train:",len(tt_train.index))
    print("tt test:",len(tt_test.index))
    print("fake train:",len(fake_train.index))
    print("fake test:",len(fake_test.index))
    train = pd.concat([dy_train,tt_train,fake_train,signal_train],ignore_index=True,sort=False).sample(frac=1).reset_index(drop=True)
    test = pd.concat([dy_test,tt_test,fake_test,signal_test],ignore_index=True,sort=False).sample(frac=1).reset_index(drop=True)


    inputs_train = train[inputlist]
    inputs_test = test[inputlist]

    #weights_train = train["eventWeightLumi"]
    weights_train = train["LumiWeight"]

    target_train = train["BDTtarget"]
    target_test = test["BDTtarget"]

    eval_set = [(inputs_train,target_train),(inputs_test,target_test)]
    #model = xgb.XGBClassifier(n_estimators=1000,learning_rate=0.01)
    model = xgb.XGBClassifier(n_estimators=700,learning_rate=0.01,nthread=10, use_label_encoder=False, objective='multi:softmax',num_class=4)
    #model = xgb.XGBClassifier(n_estimators=700,learning_rate=0.01,nthread=10, use_label_encoder=False)
    
    #model.fit(inputs_train,target_train,sample_weight=weights_train, eval_metric=["merror","mlogloss"], eval_set=eval_set, verbose=False)
    model.fit(inputs_train,target_train, eval_metric=["merror","mlogloss"], eval_set=eval_set, verbose=False)
    preds = model.predict(inputs_test)
    accuracy = accuracy_score(target_test,preds)
    
    fig, ax = pyplot.subplots(figsize=(10,8))
    xgb.plot_importance(model,ax=ax,show_values=False)
    pyplot.savefig('plots/feature_importance_weight_%s'%name,dpi=300)
    
    xgb.plot_importance(model,importance_type="cover",show_values=False)
    pyplot.savefig('plots/feature_importance_cover_%s'%name,dpi=300)

    xgb.plot_importance(model,importance_type="gain",show_values=False)
    pyplot.savefig('plots/feature_importance_gain_%s'%name,dpi=300)
    

    fig_shap = pyplot.figure(figsize=(10,8))
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(inputs_train)
    shap.summary_plot(shap_values,inputs_train,title=name,plot_size=[10,8],class_names=["Signal","TT","DY","Fake"],class_inds='original',show=False)
    pyplot.savefig('plots/feature_importance_shap_%s'%name,dpi=300)
  
    print("Accuracy: %.2f%%" % (accuracy * 100.0))

    pickle.dump(model, open(modelname, 'wb'))
    print("saved model as %s"%modelname)
    
    file = open("inputlist.txt","w")
    file.write("%s"%inputlist)
    file.close()
    
   
    

  
if args.predict:
    model = pickle.load(open(modelname, 'rb'))
    file = open("inputlist.txt","r")
    listfromfile = file.read()[1:-1].replace("'","").replace(" ","")
    inputlist = list(listfromfile.split(","))
    print("evaluating BDT on all samples for %s, this will take a while..."%name)
    for sample_shortname in samples:
        if sample_shortname == "data_obs":
            selection = selection_test_data
        else:
            selection = selection_test
        sample = getsamples(channel,year,preVFP)[sample_shortname]
        print("predicting for sample:",sample)
        BDToutput = array('f', [-1.])
        BDToutSig = array('f', [-1.])
        BDToutTT = array('f', [-1.])
        BDToutDY = array('f', [-1.])
        BDToutFake = array('f', [-1.])
        BDTisSignal = array('f', [-1.])
        BDTisTT = array('f', [-1.])
        BDTisDY = array('f', [-1.])
        BDTisFake = array('f', [-1.])
        BDTSigmax = array('f',[-1.])
        BDTDYmax = array('f',[-1.])
        BDTTTmax = array('f',[-1.])
        BDTFakemax = array('f',[-1.])
        BDTCR = array('f',[-1.])
        infile = TFile(filedir+"/"+sample+".root")
        intree = infile.Get("tree")
        outfile = TFile(outdir+"/"+sample+".root","RECREATE")
        new_tree=intree.CopyTree(selection)
        infile.Close()
        BDToutputBranch = new_tree.Branch('BDToutput', BDToutput, 'BDToutput/F')
        BDToutSigBranch = new_tree.Branch('BDToutSig', BDToutSig, 'BDToutSig/F')
        BDToutTTBranch = new_tree.Branch('BDToutTT', BDToutTT, 'BDToutTT/F')
        BDToutDYBranch = new_tree.Branch('BDToutDY', BDToutDY, 'BDToutDY/F')
        BDToutFakeBranch = new_tree.Branch('BDToutFake', BDToutFake, 'BDToutFake/F')
        BDTisSignalBranch = new_tree.Branch('BDTisSignal', BDTisSignal, 'BDTisSignal/F')
        BDTisTTBranch = new_tree.Branch('BDTisTT', BDTisTT, 'BDTisTT/F')
        BDTisDYBranch = new_tree.Branch('BDTisDY', BDTisDY, 'BDTisDY/F')
        BDTisFakeBranch = new_tree.Branch('BDTisFake', BDTisFake, 'BDTisFake/F')
        BDTSigmaxBranch = new_tree.Branch('BDTSigmax', BDTSigmax, 'BDTSigmax/F')
        BDTDYmaxBranch = new_tree.Branch('BDTDYmax', BDTDYmax, 'BDTDYmax/F')
        BDTTTmaxBranch = new_tree.Branch('BDTTTmax', BDTTTmax, 'BDTTTmax/F')
        BDTFakemaxBranch = new_tree.Branch('BDTFakemax', BDTFakemax, 'BDTFakemax/F')
        BDTCRBranch = new_tree.Branch('BDTCR', BDTCR, 'BDTCR/F')
        for event in range(0,new_tree.GetEntries()):
            new_tree.GetEntry(event)
            inputs = getinputfromTree(inputlist)
            prediction = model.predict_proba(inputs)
            pred_isSignal = prediction[:,0][0]
            pred_isTT = prediction[:,1][0]
            pred_isDY = prediction[:,2][0]
            pred_isFake = prediction[:,3][0]
            maxindex = np.argmax([pred_isSignal,pred_isTT,pred_isDY,pred_isFake])
            if maxindex==0:
                BDToutput[0] = pred_isSignal
                BDToutSig[0] = pred_isSignal
                BDToutTT[0] = -1.
                BDToutDY[0] = -1.
                BDToutFake[0] = -1.
                BDTSigmax[0] = 1.
                BDTTTmax[0] = 0.
                BDTDYmax[0] = 0.
                BDTFakemax[0] = 0.
                BDTCR[0] = -1.
            elif maxindex==1:
                BDToutput[0] = abs(pred_isTT-1.)
                BDToutTT[0] = pred_isTT
                BDToutSig[0] = -1.
                BDToutDY[0] = -1.
                BDToutFake[0] = -1.
                BDTTTmax[0] = 1.
                BDTSigmax[0] = 0.
                BDTDYmax[0] = 0.
                BDTFakemax[0] = 0.
                BDTCR[0] = abs(pred_isTT-1.)
            elif maxindex==2:
                BDToutput[0] = abs(pred_isDY-1.)
                BDToutDY[0] = pred_isDY
                BDToutTT[0] = -1.
                BDToutSig[0] = -1.
                BDToutFake[0] = -1.
                BDTDYmax[0] = 1.
                BDTSigmax[0] = 0.
                BDTTTmax[0] = 0.
                BDTFakemax[0] = 0.
                BDTCR[0] = abs(pred_isDY-1.)
            elif maxindex==3:
                BDToutput[0] = abs(pred_isFake-1.)
                BDToutDY[0] = -1.
                BDToutTT[0] = -1.
                BDToutSig[0] = -1.
                BDToutFake[0] = pred_isFake
                BDTDYmax[0] = 0.
                BDTSigmax[0] = 0.
                BDTTTmax[0] = 0.
                BDTFakemax[0] = 1.
                BDTCR[0] = abs(pred_isFake-1.)
            BDTisSignal[0] = prediction[:,0][0]
            BDTisTT[0] = prediction[:,1][0]
            BDTisDY[0] = prediction[:,2][0]
            BDTisFake[0] = prediction[:,3][0]
            BDToutputBranch.Fill()
            BDToutSigBranch.Fill()
            BDToutTTBranch.Fill()
            BDToutDYBranch.Fill()
            BDToutFakeBranch.Fill()
            BDTisSignalBranch.Fill()
            BDTisTTBranch.Fill()
            BDTisDYBranch.Fill()
            BDTisFakeBranch.Fill()
            BDTSigmaxBranch.Fill()
            BDTTTmaxBranch.Fill()
            BDTDYmaxBranch.Fill()
            BDTFakemaxBranch.Fill()
            BDTCRBranch.Fill()
        outfile.Write()
        outfile.Close()
    print("finished successfully")


if args.evaluate:
    file = open("inputlist.txt","r")
    listfromfile = file.read()[1:-1].replace("'","").replace(" ","")
    inputlist = list(listfromfile.split(","))
    
    file_signal_train_2018 = uproot.open("%sBDT_UL2018_%s_train_signal.root"%(rootdir,channel))
    file_tt_train_2018 = uproot.open("%sBDT_UL2018_%s_train_tt.root"%(rootdir,channel))
    file_dy_train_2018 = uproot.open("%sBDT_UL2018_%s_train_dy.root"%(rootdir,channel))
    file_signal_test_2018 = uproot.open("%sBDT_UL2018_%s_test_signal.root"%(rootdir,channel))
    file_tt_test_2018 = uproot.open("%sBDT_UL2018_%s_test_tt.root"%(rootdir,channel))
    file_dy_test_2018 = uproot.open("%sBDT_UL2018_%s_test_dy.root"%(rootdir,channel))

    tree_signal_train_2018 = file_signal_train_2018["tree"]
    tree_tt_train_2018 = file_tt_train_2018["tree"]
    tree_dy_train_2018 = file_dy_train_2018["tree"]
    tree_signal_test_2018 = file_signal_test_2018["tree"]
    tree_tt_test_2018 = file_tt_test_2018["tree"]
    tree_dy_test_2018 = file_dy_test_2018["tree"]

    signal_train_2018 = tree_signal_train_2018.arrays(library="pd").sample(frac=1).reset_index(drop=True)
    tt_train_2018 = tree_tt_train_2018.arrays(library="pd").sample(frac=1).reset_index(drop=True)
    dy_train_2018 = tree_dy_train_2018.arrays(library="pd").sample(frac=1).reset_index(drop=True)
    signal_test_2018 = tree_signal_test_2018.arrays(library="pd").sample(frac=1).reset_index(drop=True)
    tt_test_2018 = tree_tt_test_2018.arrays(library="pd").sample(frac=1).reset_index(drop=True)
    dy_test_2018 = tree_dy_test_2018.arrays(library="pd").sample(frac=1).reset_index(drop=True)

    train_length_2018 = min(len(dy_train_2018.index),len(signal_train_2018.index))
    test_length_2018 = min(len(dy_test_2018.index),len(signal_test_2018.index))
    dy_train_2018 = dy_train_2018[:train_length_2018]
    dy_test_2018 = dy_test_2018[:test_length_2018]
    signal_train_2018 = signal_train_2018[:train_length_2018]
    signal_test_2018 = signal_test_2018[:test_length_2018]
    tt_train_2018 = tt_train_2018[:train_length_2018]
    tt_test_2018 = tt_test_2018[:test_length_2018]

    train_2018 = pd.concat([dy_train_2018,tt_train_2018,signal_train_2018],ignore_index=True,sort=False).sample(frac=1).reset_index(drop=True)
    test_2018 = pd.concat([dy_test_2018,tt_test_2018,signal_test_2018],ignore_index=True,sort=False).sample(frac=1).reset_index(drop=True)

    inputs_train_2018 = train_2018[inputlist]
    inputs_test_2018 = test_2018[inputlist]
    target_train_2018 = train_2018["BDTtarget"]
    target_test_2018 = test_2018["BDTtarget"]

    ####

    file_signal_train_2017 = uproot.open("%sBDT_UL2017_%s_train_signal.root"%(rootdir,channel))
    file_tt_train_2017 = uproot.open("%sBDT_UL2017_%s_train_tt.root"%(rootdir,channel))
    file_dy_train_2017 = uproot.open("%sBDT_UL2017_%s_train_dy.root"%(rootdir,channel))
    file_signal_test_2017 = uproot.open("%sBDT_UL2017_%s_test_signal.root"%(rootdir,channel))
    file_tt_test_2017 = uproot.open("%sBDT_UL2017_%s_test_tt.root"%(rootdir,channel))
    file_dy_test_2017 = uproot.open("%sBDT_UL2017_%s_test_dy.root"%(rootdir,channel))

    tree_signal_train_2017 = file_signal_train_2017["tree"]
    tree_tt_train_2017 = file_tt_train_2017["tree"]
    tree_dy_train_2017 = file_dy_train_2017["tree"]
    tree_signal_test_2017 = file_signal_test_2017["tree"]
    tree_tt_test_2017 = file_tt_test_2017["tree"]
    tree_dy_test_2017 = file_dy_test_2017["tree"]
   
    signal_train_2017 = tree_signal_train_2017.arrays(library="pd").sample(frac=1).reset_index(drop=True)
    tt_train_2017 = tree_tt_train_2017.arrays(library="pd").sample(frac=1).reset_index(drop=True)
    dy_train_2017 = tree_dy_train_2017.arrays(library="pd").sample(frac=1).reset_index(drop=True)
    signal_test_2017 = tree_signal_test_2017.arrays(library="pd").sample(frac=1).reset_index(drop=True)
    tt_test_2017 = tree_tt_test_2017.arrays(library="pd").sample(frac=1).reset_index(drop=True)
    dy_test_2017 = tree_dy_test_2017.arrays(library="pd").sample(frac=1).reset_index(drop=True)

    train_length_2017 = min(len(dy_train_2017.index),len(signal_train_2017.index))
    test_length_2017 = min(len(dy_test_2017.index),len(signal_test_2017.index))
    dy_train_2017 = dy_train_2017[:train_length_2017]
    dy_test_2017 = dy_test_2017[:test_length_2017]
    signal_train_2017 = signal_train_2017[:train_length_2017]
    signal_test_2017 = signal_test_2017[:test_length_2017]
    tt_train_2017 = tt_train_2017[:train_length_2017]
    tt_test_2017 = tt_test_2017[:test_length_2017]

    train_2017 = pd.concat([dy_train_2017,tt_train_2017,signal_train_2017],ignore_index=True,sort=False).sample(frac=1).reset_index(drop=True)
    test_2017 = pd.concat([dy_test_2017,tt_test_2017,signal_test_2017],ignore_index=True,sort=False).sample(frac=1).reset_index(drop=True)

    inputs_train_2017 = train_2017[inputlist]
    inputs_test_2017 = test_2017[inputlist]
    target_train_2017 = train_2017["BDTtarget"]
    target_test_2017 = test_2017["BDTtarget"]

    #####

    file_signal_train_2016 = uproot.open("%sBDT_UL2016_%s_train_signal.root"%(rootdir,channel))
    file_tt_train_2016 = uproot.open("%sBDT_UL2016_%s_train_tt.root"%(rootdir,channel))
    file_dy_train_2016 = uproot.open("%sBDT_UL2016_%s_train_dy.root"%(rootdir,channel))
    file_signal_test_2016 = uproot.open("%sBDT_UL2016_%s_test_signal.root"%(rootdir,channel))
    file_tt_test_2016 = uproot.open("%sBDT_UL2016_%s_test_tt.root"%(rootdir,channel))
    file_dy_test_2016 = uproot.open("%sBDT_UL2016_%s_test_dy.root"%(rootdir,channel))

    tree_signal_train_2016 = file_signal_train_2016["tree"]
    tree_tt_train_2016 = file_tt_train_2016["tree"]
    tree_dy_train_2016 = file_dy_train_2016["tree"]
    tree_signal_test_2016 = file_signal_test_2016["tree"]
    tree_tt_test_2016 = file_tt_test_2016["tree"]
    tree_dy_test_2016 = file_dy_test_2016["tree"]

    signal_train_2016 = tree_signal_train_2016.arrays(library="pd").sample(frac=1).reset_index(drop=True)
    tt_train_2016 = tree_tt_train_2016.arrays(library="pd").sample(frac=1).reset_index(drop=True)
    dy_train_2016 = tree_dy_train_2016.arrays(library="pd").sample(frac=1).reset_index(drop=True)
    signal_test_2016 = tree_signal_test_2016.arrays(library="pd").sample(frac=1).reset_index(drop=True)
    tt_test_2016 = tree_tt_test_2016.arrays(library="pd").sample(frac=1).reset_index(drop=True)
    dy_test_2016 = tree_dy_test_2016.arrays(library="pd").sample(frac=1).reset_index(drop=True)

    train_length_2016 = min(len(dy_train_2016.index),len(signal_train_2016.index))
    test_length_2016 = min(len(dy_test_2016.index),len(signal_test_2016.index))
    dy_train_2016 = dy_train_2016[:train_length_2016]
    dy_test_2016 = dy_test_2016[:test_length_2016]
    signal_train_2016 = signal_train_2016[:train_length_2016]
    signal_test_2016 = signal_test_2016[:test_length_2016]
    tt_train_2016 = tt_train_2016[:train_length_2016]
    tt_test_2016 = tt_test_2016[:test_length_2016]

    train_2016 = pd.concat([dy_train_2016,tt_train_2016,signal_train_2016],ignore_index=True,sort=False).sample(frac=1).reset_index(drop=True)
    test_2016 = pd.concat([dy_test_2016,tt_test_2016,signal_test_2016],ignore_index=True,sort=False).sample(frac=1).reset_index(drop=True)

    inputs_train_2016 = train_2016[inputlist]
    inputs_test_2016 = test_2016[inputlist]
    target_train_2016 = train_2016["BDTtarget"]
    target_test_2016 = test_2016["BDTtarget"]

    #####

    model_2018 = pickle.load(open('xgbmodel_%s_UL2018.sav'%channel, 'rb'))
    y_score_2018 = model_2018.predict_proba(inputs_test_2018)
    model_2017 = pickle.load(open('xgbmodel_%s_UL2017.sav'%channel, 'rb'))
    y_score_2017 = model_2017.predict_proba(inputs_test_2017)
    model_2016 = pickle.load(open('xgbmodel_%s_UL2016.sav'%channel, 'rb'))
    y_score_2016 = model_2016.predict_proba(inputs_test_2016)

    #####
    """
    cut_off_signal = 0.95
    y_score_2018_high = []
    target_test_2018_high = []
    for i,score in enumerate(y_score_2018):
        if score[0]>cut_off_signal:
            y_score_2018_high.append(score)
            target_test_2018_high.append(target_test_2018[i])
    
    y_score_2018 = np.array(y_score_2018_high)
    target_test_2018 = np.array(target_test_2018_high)

    y_score_2017_high = []
    target_test_2017_high = []
    for i,score in enumerate(y_score_2017):
        if score[0]>cut_off_signal:
            y_score_2017_high.append(score)
            target_test_2017_high.append(target_test_2017[i])
    
    y_score_2017 = np.array(y_score_2017_high)
    target_test_2017 = np.array(target_test_2017_high)

    y_score_2016_high = []
    target_test_2016_high = []
    for i,score in enumerate(y_score_2016):
        if score[0]>cut_off_signal:
            y_score_2016_high.append(score)
            target_test_2016_high.append(target_test_2016[i])
    
    y_score_2016 = np.array(y_score_2016_high)
    target_test_2016 = np.array(target_test_2016_high)
    """
    #####

    label_binarizer_2018 = LabelBinarizer().fit(target_train_2018)
    y_onehot_test_2018 = label_binarizer_2018.transform(target_test_2018)
    label_binarizer_2017 = LabelBinarizer().fit(target_train_2017)
    y_onehot_test_2017 = label_binarizer_2017.transform(target_test_2017)
    label_binarizer_2016 = LabelBinarizer().fit(target_train_2016)
    y_onehot_test_2016 = label_binarizer_2016.transform(target_test_2016)

    fig_roc, ax_roc = pyplot.subplots(figsize=(8,8))
    #class_id = 0
    #class_of_interest = "Signal"
    class_id = 1
    class_of_interest = "TT"
    #class_id = 2
    #class_of_interest = "DY"
    RocCurveDisplay.from_predictions(
        y_onehot_test_2018[:, class_id],
    y_score_2018[:, class_id],
    name=f"{class_of_interest} vs the rest 2018",
    color="darkorange",
    ax=ax_roc,
    )
    RocCurveDisplay.from_predictions(
        y_onehot_test_2017[:, class_id],
    y_score_2017[:, class_id],
    name=f"{class_of_interest} vs the rest 2017",
    color="red",
    ax=ax_roc,
    )
    RocCurveDisplay.from_predictions(
        y_onehot_test_2016[:, class_id],
    y_score_2016[:, class_id],
    name=f"{class_of_interest} vs the rest 2016",
    color="blue",
    ax=ax_roc,
    )
    pyplot.axis("square")
    pyplot.xlabel("False Positive Rate")
    pyplot.ylabel("True Positive Rate")
    pyplot.title("ROC curves %s %s"%(class_of_interest,channel))
    pyplot.legend()
    pyplot.savefig('plots/roc_%s_%s.png'%(class_of_interest,channel))
