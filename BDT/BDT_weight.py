import os, sys
os.environ['OMP_NUM_THREADS'] = "20"
from sklearn.datasets import load_boston
import pandas as pd
import xgboost as xgb
from argparse import ArgumentParser
import numpy as np
from ROOT import TFile
from sklearn.model_selection import train_test_split
import uproot
from sklearn.metrics import accuracy_score
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
parser.add_argument('-t', '--train', dest="train_BDT", action='store_true', default=False)
parser.add_argument('-p', '--predict', dest="predict", action='store_true', default=False)
parser.add_argument('-c', '--channel', dest='channel', type=str, default='mutau', action='store',)
parser.add_argument('-y', '--year',    dest='year', type=str, default='2018', action='store')
parser.add_argument('-n', '--NN',      dest='NN', action='store_true',default=False)
parser.add_argument('-s', '--sysvar', dest='sysvar', type=str, default='', action='store')

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
    samples = ['bbH_htt','ggH_bb_htt_inc','ggH_bb_htt_excl','intH_bb_htt','intH_htt','WJets_incl','WJets_0J','WJets_1J','WJets_2J','DYJets_incl','DYJets_0J','DYJets_1J','DYJets_2J','TTTo2L2Nu','TTToHadronic','TTToSemiLeptonic','ST_t_channel_antitop','ST_t_channel_top','ST_s_channel','ST_tW_antitop','ST_tW_top','VBF','ZH','bbH_nobb_htt','ggH_htt_inc','ggH_htt_excl','ttH','WWTo2L2Nu','WWTo1L1Nu2Q','WWTo4Q','WZTo3LNu','WZTo2L2Q','WZTo1L3Nu','WZTo1L1Nu2Q','ZZTo4L','ZZTo2L2Q','ZZTo2Nu2Q','data_obs']
    #samples = ['data_obs']
else: #no data_obs for JEC variations
    samples =  ['bbH_htt','ggH_bb_htt_inc','ggH_bb_htt_excl','intH_bb_htt','intH_htt','WJets_incl','WJets_0J','WJets_1J','WJets_2J','DYJets_incl','DYJets_0J','DYJets_1J','DYJets_2J','TTTo2L2Nu','TTToHadronic','TTToSemiLeptonic','ST_t_channel_antitop','ST_t_channel_top','ST_s_channel','ST_tW_antitop','ST_tW_top','VBF','ZH','bbH_nobb_htt','ggH_htt_inc','ggH_htt_excl','ttH','WWTo2L2Nu','WWTo1L1Nu2Q','WWTo4Q','WZTo3LNu','WZTo2L2Q','WZTo1L3Nu','WZTo1L1Nu2Q','ZZTo4L','ZZTo2L2Q','ZZTo2Nu2Q']

   

modelname = 'xgbmodel_%s_UL%s.sav'%(channel,year)
#inputlist = ["Bjet1_pt","TauB_mass","vistauB_mass","vis_pt","vis_mass","MET","Dzeta","DPhi","DEta","H_pt","H_mass","Jet1_pt","Jet1_btag","Jet2_pt","Jet2_btag","HB_pt","transverse_mass_total","DRHB","Bjets_pt","DEtaMuB","DEtaTauB","DPhiMuMET"]
#inputlist = ["TauB_mass","vistauB_mass","vis_pt","vis_mass","MET","Dzeta","DPhi","DEta","H_pt","H_mass","Jet1_pt","Jet1_btag","Jet2_pt","Jet2_btag","Jet3_pt","HB_pt","transverse_mass_total","DRHB","DEtaMuB","DPhiMuMET","Bjets_pt","DEtaTauB"]

#inputlist = ["H_mass","Jet1_btag","Jet1_pt","MET","vis_mass","Dzeta","Jet2_btag","H_pt","vistauJ_mass","DRHJ","TauJ_mass","HJ_pt","DEta","Jet2_pt","dijet_pt","transverse_mass_total","DRHJ2","Jet3_pt","dijet_mass","DPhiLepMET","DPhi","DEtaTauJ2","vis_pt","DEtaLepJ","vistau1_pt","vistau1_eta","vistau2_pt","vistau2_eta","collinear_mass"]

inputlist = ["H_mass","Jet1_btag","Jet1_pt","MET","vis_mass","Dzeta","Jet2_btag","H_pt","vistauJ_mass","DRHJ","TauJ_mass","HJ_pt","DEta","Jet2_pt","dijet_pt","transverse_mass_total","DRHJ2","Jet3_pt","dijet_mass","DPhiLepMET","DPhi","DEtaTauJ2","vis_pt","DEtaLepJ","collinear_mass","vistau1_pt","vistau1_eta"]
#inputlist = ["Jet1_btag","Jet1_pt","MET","vis_mass","Dzeta","Jet2_btag","H_pt","vistauJ_mass","DRHJ","TauJ_mass","HJ_pt","DEta","Jet2_pt","dijet_pt","transverse_mass_total","DRHJ2","Jet3_pt","dijet_mass","DPhiLepMET","DPhi","DEtaTauJ2","vis_pt","DEtaLepJ","collinear_mass","vistau1_pt","vistau1_eta"]
#inputlist = ["H_mass","Jet1_btag","Jet1_pt","MET","vis_mass","Dzeta","Jet2_btag","H_pt","vistauJ_mass","DRHJ","TauJ_mass","HJ_pt","DEta","Jet2_pt","dijet_pt","transverse_mass_total","DRHJ2","Jet3_pt","dijet_mass","DPhiLepMET","DPhi","DEtaTauJ2","vis_pt","DEtaLepJ","vistau1_pt","vistau1_eta"]
#inputlist = ["H_mass","Jet1_btag","Jet1_pt","H_pt","HJ_pt","DEta","Jet2_pt","DRHJ2","DEtaTauJ2","vis_pt","DEtaLepJ","vistau1_pt","vistau1_eta"]

#inputlist = ["Bjet1_pt","vis_pt","vis_mass","MET","Dzeta","DEta","H_pt","H_mass","Jet1_pt","Jet1_btag","Jet2_pt","Jet2_btag","transverse_mass_total","DPhi","Tau1_pt","Tau1_mass","Bjet1_eta","TauB_mass","DEtaMuB","DEtaTauB"] #"TauB_mass","vistauB_mass" "DEtaMuB""vistauB_pt","HB_pt"
#inputlist = ["Bjet1_pt","TauB_mass","vistauB_mass","vis_pt","vis_mass","MET","Dzeta","DEta","DRMuMET","H_pt","H_mass","DEtaMuB","Jet1_pt","Jet1_btag","Jet2_pt","Jet2_btag","vistauB_pt","HB_pt","transverse_mass_total"] #14
#inputlist = ["Mu1_pt","Tau1_pt","Tau1_mass","Bjet1_pt","Bjet1_eta","Bjet1_mass","HB_mass","MuB_mass","TauB_mass","vistauB_mass","vis_pt","vis_mass","MET","Dzeta","DPhi","DEta","DPhiMuMET","DRMuMET","H_pt","H_phi","H_mass","DPhiMuB","DEtaMuB","DRMuB","Jet1_pt","Jet1_eta","Jet1_btag","Jet2_pt","Jet2_eta","Jet2_btag","transverse_mass_taumet","TauB_pt","vistauB_pt","vistauMET_pt","HB_pt","nBjets_l","met_var_qcd","transverse_mass_mutau","transverse_mass_total"]
#not good inputs: Mu1_eta,Mu1_phi,Mu1_iso, Mu1_charge, Mu1_mass dijet_pt,dijet_eta,dijet_phi,dijet_mass, MuB_pt,vistauBMET_pt,MuBMET_pt,Tau1_charge,Bjet1_phi,Bjet2_pt,Bjet2_phi,Bjet2_eta,Bjet2_mass,nBjets_m,DRBjets, Jet1_mass,Jet2_mass, DRjets,DEta_jets,DPhi_jets,Tau1_phi,Tau1_eta,Tau1_iso,Jet2_phi,Jet1_phi,METB_mass,MuBMet_mass,TauBMET_mass,vistauBMET_mass,nJets,H_eta,vis_phi,vis_eta
#inputlist = ["Mu1_pt","Mu1_eta","Mu1_phi","Mu1_mass","Mu1_charge","Mu1_iso","Tau1_pt","Tau1_eta","Tau1_phi","Tau1_mass","Tau1_charge","Bjet1_pt","Bjet1_eta","Bjet1_phi","Bjet1_mass","vis_pt","vis_eta","vis_phi","vis_mass","MET","Dzeta","TauBMET_mass","METB_mass","vistauB_mass","vistauBMET_mass","MuBMET_mass","DPhi","DEta","DPhiMuMET","DRMuMET","DPhiMuB","DEtaMuB","DRMuB","DRBjets","nJets"]

if channel=="mutau":
    #selection_test = '(isHtoMuTau || isHtoMuTauAR) && Mu1_charge*Tau1_charge==-1 && dimuon_veto==0 && electron_veto==0 && Tau1_genmatch!=6 && transverse_mass_mumet<60 && nBjets_l!=2 && nBjets_m==1 && EventNumber%10>=4' #use Events with endnumber 4 5 6 7 8 9 for testing BDT
    selection_test = '(isHtoMuTau || isHtoMuTauAR) && Mu1_charge*Tau1_charge==-1 && dimuon_veto==0 && electron_veto==0 && Tau1_genmatch!=6 && transverse_mass_lepmet<60 && nBjets_m>=1 && EventNumber%10>=4' #use Events with endnumber 4 5 6 7 8 9 for testing BDT
    selection_test_data = '(isHtoMuTau || isHtoMuTauAR) && Mu1_charge*Tau1_charge==-1 && dimuon_veto==0 && electron_veto==0 && Tau1_genmatch!=6 && transverse_mass_lepmet<60 && nBjets_m>=1' 
elif channel=="etau":
    #selection_test = '(isHtoETau || isHtoETauAR) && Ele1_charge*Tau1_charge==-1 && dielectron_veto==0 && muon_veto==0 && Tau1_genmatch!=6 && transverse_mass_lepmet<60 && nBjets_l!=2 && nBjets_m==1 && EventNumber%10>=4' #use Events with endnumber 4 5 6 7 8 9 for testing BDT
    selection_test = '(isHtoETau || isHtoETauAR) && Ele1_charge*Tau1_charge==-1 && dielectron_veto==0 && muon_veto==0 && Tau1_genmatch!=6 && transverse_mass_lepmet<60 && nBjets_m>=1 && EventNumber%10>=4' #use Events with endnumber 4 5 6 7 8 9 for testing BDT
    selection_test_data = '(isHtoETau || isHtoETauAR) && Ele1_charge*Tau1_charge==-1 && dielectron_veto==0 && muon_veto==0 && Tau1_genmatch!=6 && transverse_mass_lepmet<60 && nBjets_m>=1'

if args.train_BDT:
    file_signal_train = uproot.open("%sBDT_UL%s_%s_train_signal.root"%(rootdir,year,channel))
    #file_bbh_train = uproot.open("%sBDT_UL%s_%s_train_bbh.root"%(rootdir,year,channel))
    #file_ggh_train = uproot.open("%sBDT_UL%s_%s_train_ggh.root"%(rootdir,year,channel))
    #file_jjh_train = uproot.open("%sBDT_UL%s_%s_train_jjh.root"%(rootdir,year,channel))
    file_tt_train = uproot.open("%sBDT_UL%s_%s_train_tt.root"%(rootdir,year,channel))
    file_dy_train = uproot.open("%sBDT_UL%s_%s_train_dy.root"%(rootdir,year,channel))
    file_signal_test = uproot.open("%sBDT_UL%s_%s_test_signal.root"%(rootdir,year,channel))
    #file_bbh_test = uproot.open("%sBDT_UL%s_%s_test_bbh.root"%(rootdir,year,channel))
    #file_ggh_test = uproot.open("%sBDT_UL%s_%s_test_ggh.root"%(rootdir,year,channel))
    #file_jjh_test = uproot.open("%sBDT_UL%s_%s_test_jjh.root"%(rootdir,year,channel))
    file_tt_test = uproot.open("%sBDT_UL%s_%s_test_tt.root"%(rootdir,year,channel))
    file_dy_test = uproot.open("%sBDT_UL%s_%s_test_dy.root"%(rootdir,year,channel))

    tree_signal_train = file_signal_train["tree"]
    #tree_bbh_train = file_bbh_train["tree"]
    #tree_ggh_train = file_ggh_train["tree"]
    #tree_jjh_train = file_jjh_train["tree"]
    tree_tt_train = file_tt_train["tree"]
    tree_dy_train = file_dy_train["tree"]
    tree_signal_test = file_signal_test["tree"]
    #tree_bbh_test = file_bbh_test["tree"]
    #tree_ggh_test = file_ggh_test["tree"]
    #tree_jjh_test = file_jjh_test["tree"]
    tree_tt_test = file_tt_test["tree"]
    tree_dy_test = file_dy_test["tree"]
    

    #python2.7
    #signal_train = tree_signal_train.pandas.df().sample(frac=1).reset_index(drop=True)
    #bbh_train = tree_bbh_train.pandas.df().sample(frac=1).reset_index(drop=True)
    #ggh_train = tree_ggh_train.pandas.df().sample(frac=1).reset_index(drop=True)
    #tt_train = tree_tt_train.pandas.df().sample(frac=1).reset_index(drop=True)
    #dy_train = tree_dy_train.pandas.df().sample(frac=1).reset_index(drop=True)
    #signal_test = tree_signal_test.pandas.df().sample(frac=1).reset_index(drop=True)
    #bbh_test = tree_bbh_test.pandas.df().sample(frac=1).reset_index(drop=True)
    #ggh_test = tree_ggh_test.pandas.df().sample(frac=1).reset_index(drop=True)
    #tt_test = tree_tt_test.pandas.df().sample(frac=1).reset_index(drop=True)
    #dy_test = tree_dy_test.pandas.df().sample(frac=1).reset_index(drop=True)
  
    signal_train = tree_signal_train.arrays(library="pd").sample(frac=1).reset_index(drop=True)
    #bbh_train = tree_bbh_train.arrays(library="pd").sample(frac=1).reset_index(drop=True)
    #ggh_train = tree_ggh_train.arrays(library="pd").sample(frac=1).reset_index(drop=True)
    #jjh_train = tree_jjh_train.arrays(library="pd").sample(frac=1).reset_index(drop=True)
    tt_train = tree_tt_train.arrays(library="pd").sample(frac=1).reset_index(drop=True)
    dy_train = tree_dy_train.arrays(library="pd").sample(frac=1).reset_index(drop=True)
    signal_test = tree_signal_test.arrays(library="pd").sample(frac=1).reset_index(drop=True)
    #bbh_test = tree_bbh_test.arrays(library="pd").sample(frac=1).reset_index(drop=True)
    #ggh_test = tree_ggh_test.arrays(library="pd").sample(frac=1).reset_index(drop=True)
    #jjh_test = tree_jjh_test.arrays(library="pd").sample(frac=1).reset_index(drop=True)
    tt_test = tree_tt_test.arrays(library="pd").sample(frac=1).reset_index(drop=True)
    dy_test = tree_dy_test.arrays(library="pd").sample(frac=1).reset_index(drop=True)

    """
    signal_train_length = len(signal_train.index)
    signal_test_length = len(signal_test.index)
    tt_train_length = len(tt_train.index)
    tt_test_length = len(tt_test.index)
    dy_train_length = len(dy_train.index)
    dy_test_length = len(dy_test.index)
    print("signal train:",signal_train_length)
    print("signal test:", signal_test_length)
    print("tt train:",tt_train_length)
    print("tt test:",tt_test_length)
    print("dy train:",dy_train_length)
    print("dy test:",dy_test_length)
    """
    """
    signal_train_length = len(signal_train.index)
    tt_train = tt_train[:signal_train_length]
    signal_test_length = len(signal_test.index)
    tt_test = tt_test[:signal_test_length]
    
    bbh_train_length = len(bbh_train.index)
    bbh_test_length = len(bbh_test.index)
    ggh_train = ggh_train[:bbh_train_length]
    ggh_test = ggh_test[:bbh_test_length]
    dy_train = dy_train[:bbh_train_length]
    dy_test = dy_test[:bbh_test_length]
    tt_train = tt_train[:bbh_train_length]
    tt_test = tt_test[:bbh_test_length]
    """
    dy_train_length = len(dy_train.index)
    dy_test_length = len(dy_test.index)
    signal_train = signal_train[:dy_train_length]
    signal_test = signal_test[:dy_test_length]
    tt_train = tt_train[:dy_train_length]
    tt_test = tt_test[:dy_test_length]
    
    #jjh_train = jjh_train[:dy_train_length]
    #jjh_test = jjh_test[:dy_test_length]

    
    print("dy train:",len(dy_train.index))
    print("dy test:",len(dy_test.index))
    print("signal train:",len(signal_train.index))
    print("signal test:",len(signal_test.index))
    #print("jjh train:",len(jjh_train.index))
    #print("jjh test:",len(jjh_test.index))
    #print("bbH train:",len(bbh_train.index))
    #print("bbH test:",len(bbh_test.index))
    #print("ggH train:",len(ggh_train.index))
    #print("ggH test:",len(ggh_test.index))
    print("tt train:",len(tt_train.index))
    print("tt test:",len(tt_test.index))
    #print("st train:",len(st_train.index)
    #print("st test:",len(st_test.index)
    
    #train = pd.concat([dy_train,tt_train,bbh_train,ggh_train],ignore_index=True,sort=False).sample(frac=1).reset_index(drop=True)
    #test = pd.concat([dy_test,tt_test,bbh_test,ggh_test],ignore_index=True,sort=False).sample(frac=1).reset_index(drop=True)
    train = pd.concat([dy_train,tt_train,signal_train],ignore_index=True,sort=False).sample(frac=1).reset_index(drop=True)
    test = pd.concat([dy_test,tt_test,signal_test],ignore_index=True,sort=False).sample(frac=1).reset_index(drop=True)  
    #train = pd.concat([dy_train,tt_train,signal_train,jjh_train],ignore_index=True,sort=False).sample(frac=1).reset_index(drop=True)
    #test = pd.concat([dy_test,tt_test,signal_test,jjh_test],ignore_index=True,sort=False).sample(frac=1).reset_index(drop=True) 
    #train = pd.concat([dy_train,tt_train,bbh_train,ggh_train],ignore_index=True,sort=False).sample(frac=1).reset_index(drop=True)
    #test = pd.concat([dy_test,tt_test,bbh_test,ggh_test],ignore_index=True,sort=False).sample(frac=1).reset_index(drop=True)
    #train = pd.concat([dy_train,tt_train,bbh_train,ggh_train],ignore_index=True,sort=False).sample(frac=1).reset_index(drop=True)
    #test = pd.concat([dy_test,tt_test,bbh_test,ggh_test],ignore_index=True,sort=False).sample(frac=1).reset_index(drop=True)
    #train = pd.concat([dy_train,tt_train],ignore_index=True,sort=False).sample(frac=1).reset_index(drop=True)
    #test = pd.concat([dy_test,tt_test],ignore_index=True,sort=False).sample(frac=1).reset_index(drop=True)

    #train, test= train_test_split(all_sample, test_size=0.5, shuffle=True)

    inputs_train = train[inputlist]
    inputs_test = test[inputlist]

    #weights_train = train["eventWeightLumi"]
    weights_train = train["LumiWeight"]

    target_train = train["BDTtarget"]
    target_test = test["BDTtarget"]
    

    #inputs_train = inputs_train.values  #make numpy arrays to avoid mismatch in label names for prediction
    #inputs_test = inputs_test.values
    #target_train = target_train.values
    #target_test = target_test.values
    weights_train = weights_train.values


    eval_set = [(inputs_train,target_train),(inputs_test,target_test)]

    #model = xgb.XGBClassifier(n_estimators=1000,learning_rate=0.01)
    model = xgb.XGBClassifier(n_estimators=700,learning_rate=0.01,nthread=10, use_label_encoder=False)
    """
    n_estimators = [100,200,300,400,500,550,600,650,700]
    learning_rate = [0.1,0.2, 0.3, 0.35, 0.4]
    param_grid = dict(learning_rate=learning_rate, n_estimators=n_estimators)
    kfold = StratifiedKFold(n_splits=10, shuffle=True, random_state=7)
    grid_search = GridSearchCV(model, param_grid, scoring="neg_log_loss", n_jobs=-1, cv=kfold)
    grid_result = grid_search.fit(inputs_train,target_train)
    #grid_result = grid_search.fit(inputs_train,target_train, eval_metric=["merror","mlogloss"], eval_set=eval_set, verbose=False)
    # summarize results
    print("Best: %f using %s" % (grid_result.best_score_, grid_result.best_params_))
    means = grid_result.cv_results_['mean_test_score']
    stds = grid_result.cv_results_['std_test_score']
    params = grid_result.cv_results_['params']
    for mean, stdev, param in zip(means, stds, params):
	print("%f (%f) with: %r" % (mean, stdev, param))
    # plot results
    scores = np.array(means).reshape(len(learning_rate), len(n_estimators))
    for i, value in enumerate(learning_rate):
        pyplot.plot(n_estimators, scores[i], label='learning_rate: ' + str(value))
    pyplot.legend()
    pyplot.xlabel('n_estimators')
    pyplot.ylabel('Log Loss')
    pyplot.savefig('n_estimators_vs_learning_rate.png')
    """
    model.fit(inputs_train,target_train,sample_weight=weights_train, eval_metric=["merror","mlogloss"], eval_set=eval_set, verbose=False)
    #model.fit(inputs_train,target_train, eval_metric=["merror","mlogloss"], eval_set=eval_set, verbose=False)
    preds = model.predict(inputs_test)
    accuracy = accuracy_score(target_test,preds)
    
    fig, ax = pyplot.subplots(figsize=(10,8))
    xgb.plot_importance(model,ax=ax,show_values=False)
    pyplot.savefig('feature_importance_weight',dpi=300)
    
    xgb.plot_importance(model,importance_type="cover",show_values=False)
    pyplot.savefig('feature_importance_cover',dpi=300)

    xgb.plot_importance(model,importance_type="gain",show_values=False)
    pyplot.savefig('feature_importance_gain',dpi=300)
    

    fig_shap = pyplot.figure(figsize=(10,8))
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(inputs_train)
    shap.summary_plot(shap_values,inputs_train,plot_size=[10,8],show=False)
    pyplot.savefig('feature_importance_shap',dpi=300)
    

    print("Accuracy: %.2f%%" % (accuracy * 100.0))

    pickle.dump(model, open(modelname, 'wb'))
    print("saved model as %s"%modelname)
    
    file = open("inputlist.txt","w")
    file.write("%s"%inputlist)
    file.close()
    
    """
    results = model.evals_result()
    epochs = len(results['validation_0']['merror'])
    x_axis = range(0, epochs)
    # plot log loss
    fig, ax = pyplot.subplots()
    ax.plot(x_axis, results['validation_0']['mlogloss'], label='Train')
    ax.plot(x_axis, results['validation_1']['mlogloss'], label='Test')
    ax.legend()
    pyplot.ylabel('Log Loss')
    pyplot.title('XGBoost Log Loss')
    pyplot.show()
    
    
    # plot classification error
    fig, ax = pyplot.subplots()
    ax.plot(x_axis, results['validation_0']['merror'], label='Train')
    ax.plot(x_axis, results['validation_1']['merror'], label='Test')
    ax.legend()
    pyplot.ylabel('Classification Error')
    pyplot.title('XGBoost Classification Error')
    pyplot.show()
    """

  
if args.predict:
    model = pickle.load(open(modelname, 'rb'))
    file = open("inputlist.txt","r")
    listfromfile = file.read()[1:-1].replace("'","").replace(" ","")
    inputlist = list(listfromfile.split(","))
    print("evaluating BDT on all samples, this will take a while...")
    for sample_shortname in samples:
        if sample_shortname == "data_obs":
            selection = selection_test_data
        else:
            selection = selection_test
        sample = getsamples(channel,"UL",year,preVFP)[sample_shortname]
        print("predicting for sample:",sample)
        BDToutput = array('f', [-1.])
        BDToutSig = array('f', [-1.])
        BDToutTT = array('f', [-1.])
        BDToutDY = array('f', [-1.])
        #BDToutjjH = array('f', [-1.])
        BDTisSignal = array('f', [-1.])
        BDTisTT = array('f', [-1.])
        BDTisDY = array('f', [-1.])
        #BDTisjjH = array('f', [-1.])
        BDTSigmax = array('f',[-1.])
        BDTDYmax = array('f',[-1.])
        BDTTTmax = array('f',[-1.])
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
        #BDToutjjHBranch = new_tree.Branch('BDToutjjH', BDToutjjH, 'BDToutjjH/F')
        BDTisSignalBranch = new_tree.Branch('BDTisSignal', BDTisSignal, 'BDTisSignal/F')
        BDTisTTBranch = new_tree.Branch('BDTisTT', BDTisTT, 'BDTisTT/F')
        BDTisDYBranch = new_tree.Branch('BDTisDY', BDTisDY, 'BDTisDY/F')
        #BDTisjjHBranch = new_tree.Branch('BDTisjjH', BDTisjjH, 'BDTisjjH/F')
        BDTSigmaxBranch = new_tree.Branch('BDTSigmax', BDTSigmax, 'BDTSigmax/F')
        BDTDYmaxBranch = new_tree.Branch('BDTDYmax', BDTDYmax, 'BDTDYmax/F')
        BDTTTmaxBranch = new_tree.Branch('BDTTTmax', BDTTTmax, 'BDTTTmax/F')
        BDTCRBranch = new_tree.Branch('BDTCR', BDTCR, 'BDTCR/F')
        for event in range(0,new_tree.GetEntries()):
            new_tree.GetEntry(event)
            inputs = getinputfromTree(inputlist)
            prediction = model.predict_proba(inputs)
            pred_isSignal = prediction[:,0][0]
            pred_isTT = prediction[:,1][0]
            pred_isDY = prediction[:,2][0]
            #pred_isjjH = prediction[:,3][0]
            maxindex = np.argmax([pred_isSignal,pred_isTT,pred_isDY])
            if maxindex==0:
                BDToutput[0] = pred_isSignal
                BDToutSig[0] = pred_isSignal
                BDToutTT[0] = -1.
                BDToutDY[0] = -1.
                BDTSigmax[0] = 1.
                BDTTTmax[0] = 0.
                BDTDYmax[0] = 0.
                BDTCR[0] = -1.
            elif maxindex==1:
                BDToutput[0] = abs(pred_isTT-1.)
                BDToutTT[0] = pred_isTT
                BDToutSig[0] = -1.
                BDToutDY[0] = -1.
                BDTTTmax[0] = 1.
                BDTSigmax[0] = 0.
                BDTDYmax[0] = 0.
                BDTCR[0] = abs(pred_isTT-1.)
            elif maxindex==2:
                BDToutput[0] = abs(pred_isDY-1.)
                BDToutDY[0] = pred_isDY
                BDToutTT[0] = -1.
                BDToutSig[0] = -1.
                BDTDYmax[0] = 1.
                BDTSigmax[0] = 0.
                BDTTTmax[0] = 0.
                BDTCR[0] = abs(pred_isDY-1.)
            #elif maxindex==3:
            #    BDToutput[0] = abs(pred_isjjH-1.)
            #    BDToutjjH[0] = pred_isjjH    
            BDTisSignal[0] = prediction[:,0][0]
            BDTisTT[0] = prediction[:,1][0]
            BDTisDY[0] = prediction[:,2][0]
            #BDTisjjH[0] = prediction[:,3][0]
            BDToutputBranch.Fill()
            BDToutSigBranch.Fill()
            BDToutTTBranch.Fill()
            BDToutDYBranch.Fill()
            #BDToutjjHBranch.Fill()
            BDTisSignalBranch.Fill()
            BDTisTTBranch.Fill()
            BDTisDYBranch.Fill()
            #BDTisjjHBranch.Fill()
            BDTSigmaxBranch.Fill()
            BDTTTmaxBranch.Fill()
            BDTDYmaxBranch.Fill()
            BDTCRBranch.Fill()
        outfile.Write()
        outfile.Close()
    """
    if sample_shortname == "data_obs":
        selection = selection_test_data
    else:
        selection = selection_test
    model = pickle.load(open(modelname, 'rb'))
    file = open("inputlist.txt","r")
    listfromfile = file.read()[1:-1].replace("'","").replace(" ","")
    inputlist = list(listfromfile.split(","))
    print("evaluating BDT on all samples, this will take a while...")
    for sample_shortname in samples:
        sample = samples_name["%s%s"%("UL",year)][sample_shortname]
        print("predicting for sample:",sample)
        BDToutput = array('f', [0.0])
        #BDTisSignal = array('f', [0.0])
        BDTisbbH = array('f', [0.0])
        BDTisggH = array('f', [0.0])
        BDTisTT = array('f', [0.0])
        BDTisDY = array('f', [0.0])
        #BDTisggF = array('f', [0.0])
        infile = TFile(filedir+"/"+sample+".root")
        intree = infile.Get("tree")
        outfile = TFile(outdir+"/"+sample+".root","RECREATE")
        new_tree=intree.CopyTree(selection)
        infile.Close()
        BDToutputBranch = new_tree.Branch('BDToutput', BDToutput, 'BDToutput/F')
        #BDTisSignalBranch = new_tree.Branch('BDTisSignal', BDTisSignal, 'BDTisSignal/F')
        BDTisbbHBranch = new_tree.Branch('BDTisbbH', BDTisbbH, 'BDTisbbH/F')
        BDTisggHBranch = new_tree.Branch('BDTisggH', BDTisggH, 'BDTisggH/F')
        BDTisTTBranch = new_tree.Branch('BDTisTT', BDTisTT, 'BDTisTT/F')
        BDTisDYBranch = new_tree.Branch('BDTisDY', BDTisDY, 'BDTisDY/F')
        #BDTisggFBranch = new_tree.Branch('BDTisggF', BDTisggF, 'BDTisggF/F')
        for event in range(0,new_tree.GetEntries()):
            new_tree.GetEntry(event)
            inputs = getinputfromTree(inputlist)
            prediction = model.predict_proba(inputs)
            #pred_isSignal = prediction[:,0][0]
            pred_isbbH = prediction[:,0][0]
            pred_isggH = prediction[:,1][0]
            pred_isTT = prediction[:,2][0]
            pred_isDY = prediction[:,3][0]
            #pred_isggF = prediction[:,4][0]
            maxindex = np.argmax([pred_isbbH,pred_isggH,pred_isTT,pred_isDY])
            if maxindex==0:
                BDToutput[0] = pred_isbbH
            elif maxindex==1:
                BDToutput[0] = pred_isggH
            elif maxindex==2:    
                BDToutput[0] = abs(pred_isTT-1.)
            elif maxindex==3:
                BDToutput[0] = abs(pred_isDY-1.)
            #elif maxindex==4:
            #    BDToutput[0] = abs(pred_isggF-1.)
            #BDTisSignal[0] = prediction[:,0][0]
            BDTisbbH[0] = prediction[:,0][0]
            BDTisggH[0] = prediction[:,1][0]
            BDTisTT[0] = prediction[:,2][0]
            BDTisDY[0] = prediction[:,3][0]
            #BDTisggF[0] = prediction[:,4][0]
            BDToutputBranch.Fill()
            #BDTisSignalBranch.Fill()
            BDTisbbHBranch.Fill()
            BDTisggHBranch.Fill()
            BDTisTTBranch.Fill()
            BDTisDYBranch.Fill()
            #BDTisggFBranch.Fill()
        outfile.Write()
        outfile.Close()
    """
    print("finished successfully")

