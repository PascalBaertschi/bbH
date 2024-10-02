import os, sys
os.environ['OMP_NUM_THREADS'] = "20"
from sklearn.datasets import load_boston
import pandas as pd
import xgboost as xgb
from argparse import ArgumentParser
import numpy as np
from ROOT import TFile, TLegend, TGraph, TCanvas
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
np.random.seed(1337)
#numpy.random.seed(246)
import random
import time
import math
import sys
import csv
from keras.models import Sequential, load_model
from keras.optimizers import Adam
from keras.callbacks import LearningRateScheduler
from keras.layers import Dense, Dropout,Activation
from keras.layers.normalization import BatchNormalization
from sklearn import preprocessing
import multiprocessing



warnings.filterwarnings(action='ignore', category=DeprecationWarning) #ignore warning which is fixed in new version of scikit-learn

parser = ArgumentParser()
parser.add_argument('-t', '--train', dest="train_BDT", action='store_true', default=False)
parser.add_argument('-p', '--predict', dest="predict", action='store_true', default=False)
parser.add_argument('-y', '--year',    dest='year', type=str, default='2018', action='store')
parser.add_argument('-c', '--channel', dest='channel', choices=['mutau','etau','tautau'], type=str, default='mutau', action='store',)
parser.add_argument('-s', '--preVFP',  dest='preVFP', action='store_const', const="_preVFP",default="")
parser.add_argument('-a', '--comb',  dest='UL2016comb', action='store_true',default=False)
args = parser.parse_args()
year = args.year
channel = args.channel
preVFP = args.preVFP
UL2016comb = args.UL2016comb

if UL2016comb:
    preVFP="_comb"
filedir = "/pnfs/psi.ch/cms/trivcat/store/user/pbaertsc/bbh/samples_UL%s%s/"%(year,preVFP)
rootdir = "/work/pbaertsc/bbh/NanoTreeProducer/NN/root/"
outdir = "/pnfs/psi.ch/cms/trivcat/store/user/pbaertsc/bbh/samples_UL%s%s_NN/"%(year,preVFP)

batch_size = 128 #128
epochs = 200 #100


if year=="2018":
   #samples = ['bbH','ggH_inc','ggbbH','ggbbH_ext','WJets','W1Jets','W2Jets','W3Jets','W4Jets','DYJets','DY1Jets','DY2Jets','DY3Jets','DY4Jets','ST_t_channel_antitop','ST_t_channel_top','ST_s_channel','ST_tW_antitop','ST_tW_top','VBF','ZH','ggF','ggF_inc','ggF_ext','JJH','ttH','WWTo2L2Nu','WWToLNuQQ','WWTo4Q','WZTo3LNu','WZTo2L2Q','WZTo1L3Nu','WZTo1L1Nu2Q','ZZTo4L','ZZTo2L2Q','ZZTo2Q2Nu','TTToHadronic','TTToSemiLeptonic','TTTo2L2Nu','data_obs1','data_obs2','data_obs3','data_obs4','data_obs5']
   #samples = ['bbH','ggH_inc','ggbbH','ggbbH_ext','WJets','W1Jets','W2Jets','W3Jets','W4Jets','DYJets','DY1Jets','DY2Jets','DY3Jets','DY4Jets','ST_t_channel_antitop','ST_t_channel_top','ST_s_channel','ST_tW_antitop','ST_tW_top','VBF','ZH','ggF','ggF_inc','ggF_ext','JJH','ttH','WWTo2L2Nu','WWToLNuQQ','WWTo4Q','WZTo3LNu','WZTo2L2Q','WZTo1L3Nu','WZTo1L1Nu2Q','ZZTo4L','ZZTo2L2Q','ZZTo2Q2Nu','TTToHadronic','TTToSemiLeptonic'] 
   samples = ['TTTo2L2Nu','data_obs1','data_obs2','data_obs3','data_obs4','data_obs5']
   #samples = ['bbH','ggH_inc','ggbbH','ggbbH_ext']
   #samples = ['bbH_M-80','bbH_M-90','bbH_M-100','bbH_M-110','bbH_M-120','bbH_M-125','bbH_M-130','bbH_M-140','bbH_M-160','bbH_M-180','bbH_M-200','bbH_M-250','bbH_M-300']
else:
   samples = ['bbH','ggH_inc','ggbbH','WJets','W1Jets','W2Jets','W3Jets','W4Jets','DYJets','DY1Jets','DY2Jets','DY3Jets','DY4Jets','TTTo2L2Nu','TTToHadronic','TTToSemiLeptonic','ST_t_channel_antitop','ST_t_channel_top','ST_s_channel','ST_tW_antitop','ST_tW_top','VBF','ZH','ggF','ggF_inc','JJH','ttH','data_obs1','data_obs2','WWTo2L2Nu','WWToLNuQQ','WWTo4Q','WZTo3LNu','WZTo2L2Q','WZTo1L3Nu','WZTo1L1Nu2Q','ZZTo4L','ZZTo2L2Q','ZZTo2Q2Nu'] 


modelname = 'NNmodel__UL%s.sav'%year


#inputlist = ["vistau1_pt","vistau1_eta","vistau1_phi","vistau1_mass","vistau1_energy","vistau2_pt","vistau2_eta","vistau2_phi","vistau2_mass","vistau2_energy","MET","MET_phi","collinear_mass"]
inputlist = ["vistau1_pt","vistau1_eta","vistau1_phi","vistau1_mass","vistau1_energy","vistau2_pt","vistau2_eta","vistau2_phi","vistau2_mass","vistau2_energy","MET","MET_phi","collinear_mass"]


def neural_network_train(batch_size,epochs,nninput,nntarget,nninput_test,nntarget_test):
    print ("train NEURAL NETWORK")
    NNmodel = Sequential()
    #NNmodel.add(Dropout(0.3),input_shape(13,))
    #NNmodel.add(Dense(200,input_dim=13,kernel_initializer='random_uniform',activation='relu'))
    NNmodel.add(Dense(200,input_dim=13,kernel_initializer='random_uniform',activation='relu'))
    NNmodel.add(Dropout(0.1))
    #NNmodel.add(Dense(200,kernel_initializer='random_uniform',activation='relu'))
    NNmodel.add(Dense(200,kernel_initializer='random_uniform',activation='relu'))
    NNmodel.add(Dropout(0.1))
    #NNmodel.add(Dense(200,kernel_initializer='random_uniform',activation='relu'))
    NNmodel.add(Dense(200,kernel_initializer='random_uniform',activation='relu'))
    NNmodel.add(Dropout(0.1))
    #NNmodel.add(Dense(200,kernel_initializer='random_uniform',activation='relu'))
    NNmodel.add(Dense(200,kernel_initializer='random_uniform',activation='relu'))
    NNmodel.add(Dropout(0.1))
    NNmodel.add(Dense(1,kernel_initializer='random_uniform',activation='relu'))
    NNmodel.compile(loss='mean_squared_error',optimizer='adam')
    history = NNmodel.fit(nninput,nntarget,batch_size,epochs,validation_data = (nninput_test,nntarget_test),verbose = 2)
    mass_score = NNmodel.evaluate(nninput_test,nntarget_test,batch_size,verbose=0)
    NNmodel.summary()
    loss_values = np.array(history.history['loss'])
    val_loss_values = np.array(history.history['val_loss'])
    print ("mass_model(",batch_size,epochs,")")
    print ("loss (MSE):",mass_score)
    NNmodel.save('nnmodel')
    epochs_range = np.array([float(i) for i in range(1,epochs+1)])
    loss_graph = TGraph(epochs,epochs_range,np.array(history.history['loss']))
    loss_graph.SetTitle("model loss")
    loss_graph.GetXaxis().SetTitle("epochs")
    loss_graph.GetYaxis().SetTitle("loss")
    loss_graph.SetMarkerColor(4)
    loss_graph.SetMarkerSize(0.8)
    loss_graph.SetMarkerStyle(21)
    val_loss_graph = TGraph(epochs,epochs_range,np.array(history.history['val_loss']))
    val_loss_graph.SetMarkerColor(2)
    val_loss_graph.SetMarkerSize(0.8)
    val_loss_graph.SetMarkerStyle(21)
    #plots of the loss of train and test sample
    canv1 = TCanvas("loss di-tau mass")
    loss_graph.Draw("AP")
    val_loss_graph.Draw("P")
    leg1 = TLegend(0.6,0.7,0.87,0.87)
    leg1.AddEntry(loss_graph,"loss on train sample","P")
    leg1.AddEntry(val_loss_graph,"loss on test sample","P")
    leg1.Draw()
    canv1.SaveAs("loss.pdf")

def neural_network_predict(nninput):
    NNmodel = load_model('nnmodel_thesis')
    return NNmodel.predict(nninput,128)


if args.train_BDT:
    file_M80_train = uproot.open("%sbbH_M-80_train_UL%s.root"%(rootdir,year))
    file_M90_train = uproot.open("%sbbH_M-90_train_UL%s.root"%(rootdir,year))
    file_M100_train = uproot.open("%sbbH_M-100_train_UL%s.root"%(rootdir,year))
    file_M110_train = uproot.open("%sbbH_M-110_train_UL%s.root"%(rootdir,year))
    file_M120_train = uproot.open("%sbbH_M-120_train_UL%s.root"%(rootdir,year))
    file_M125_train = uproot.open("%sbbH_M-125_train_UL%s.root"%(rootdir,year))
    file_M130_train = uproot.open("%sbbH_M-130_train_UL%s.root"%(rootdir,year))
    file_M140_train = uproot.open("%sbbH_M-140_train_UL%s.root"%(rootdir,year))
    file_M160_train = uproot.open("%sbbH_M-160_train_UL%s.root"%(rootdir,year))
    file_M180_train = uproot.open("%sbbH_M-180_train_UL%s.root"%(rootdir,year))
    file_M200_train = uproot.open("%sbbH_M-200_train_UL%s.root"%(rootdir,year))
    file_M250_train = uproot.open("%sbbH_M-250_train_UL%s.root"%(rootdir,year))
    file_M300_train = uproot.open("%sbbH_M-300_train_UL%s.root"%(rootdir,year))
    file_M80_test = uproot.open("%sbbH_M-80_test_UL%s.root"%(rootdir,year))
    file_M90_test = uproot.open("%sbbH_M-90_test_UL%s.root"%(rootdir,year))
    file_M100_test = uproot.open("%sbbH_M-100_test_UL%s.root"%(rootdir,year))
    file_M110_test = uproot.open("%sbbH_M-110_test_UL%s.root"%(rootdir,year))
    file_M120_test = uproot.open("%sbbH_M-120_test_UL%s.root"%(rootdir,year))
    file_M125_test = uproot.open("%sbbH_M-125_test_UL%s.root"%(rootdir,year))
    file_M130_test = uproot.open("%sbbH_M-130_test_UL%s.root"%(rootdir,year))
    file_M140_test = uproot.open("%sbbH_M-140_test_UL%s.root"%(rootdir,year))
    file_M160_test = uproot.open("%sbbH_M-160_test_UL%s.root"%(rootdir,year))
    file_M180_test = uproot.open("%sbbH_M-180_test_UL%s.root"%(rootdir,year))
    file_M200_test = uproot.open("%sbbH_M-200_test_UL%s.root"%(rootdir,year))
    file_M250_test = uproot.open("%sbbH_M-250_test_UL%s.root"%(rootdir,year))
    file_M300_test = uproot.open("%sbbH_M-300_test_UL%s.root"%(rootdir,year))

    tree_M80_train = file_M80_train["tree"]
    tree_M90_train = file_M90_train["tree"]
    tree_M100_train = file_M100_train["tree"]
    tree_M110_train = file_M110_train["tree"]
    tree_M120_train = file_M120_train["tree"]
    tree_M125_train = file_M125_train["tree"]
    tree_M130_train = file_M130_train["tree"]
    tree_M140_train = file_M140_train["tree"]
    tree_M160_train = file_M160_train["tree"]
    tree_M180_train = file_M180_train["tree"]
    tree_M200_train = file_M200_train["tree"]
    tree_M250_train = file_M250_train["tree"]
    tree_M300_train = file_M300_train["tree"]
    tree_M80_test = file_M80_test["tree"]
    tree_M90_test = file_M90_test["tree"]
    tree_M100_test = file_M100_test["tree"]
    tree_M110_test = file_M110_test["tree"]
    tree_M120_test = file_M120_test["tree"]
    tree_M125_test = file_M125_test["tree"]
    tree_M130_test = file_M130_test["tree"]
    tree_M140_test = file_M140_test["tree"]
    tree_M160_test = file_M160_test["tree"]
    tree_M180_test = file_M180_test["tree"]
    tree_M200_test = file_M200_test["tree"]
    tree_M250_test = file_M250_test["tree"]
    tree_M300_test = file_M300_test["tree"]

    
    M80_train = tree_M80_train.pandas.df().sample(frac=1).reset_index(drop=True)
    M90_train = tree_M90_train.pandas.df().sample(frac=1).reset_index(drop=True)
    M100_train = tree_M100_train.pandas.df().sample(frac=1).reset_index(drop=True)
    M110_train = tree_M110_train.pandas.df().sample(frac=1).reset_index(drop=True)
    M120_train = tree_M120_train.pandas.df().sample(frac=1).reset_index(drop=True)
    M125_train = tree_M125_train.pandas.df().sample(frac=1).reset_index(drop=True)
    M130_train = tree_M130_train.pandas.df().sample(frac=1).reset_index(drop=True)
    M140_train = tree_M140_train.pandas.df().sample(frac=1).reset_index(drop=True)
    M160_train = tree_M160_train.pandas.df().sample(frac=1).reset_index(drop=True)
    M180_train = tree_M180_train.pandas.df().sample(frac=1).reset_index(drop=True)
    M200_train = tree_M200_train.pandas.df().sample(frac=1).reset_index(drop=True)
    M250_train = tree_M250_train.pandas.df().sample(frac=1).reset_index(drop=True)
    M300_train = tree_M300_train.pandas.df().sample(frac=1).reset_index(drop=True)
    M80_test = tree_M80_test.pandas.df().sample(frac=1).reset_index(drop=True)
    M90_test = tree_M90_test.pandas.df().sample(frac=1).reset_index(drop=True)
    M100_test = tree_M100_test.pandas.df().sample(frac=1).reset_index(drop=True)
    M110_test = tree_M110_test.pandas.df().sample(frac=1).reset_index(drop=True)
    M120_test = tree_M120_test.pandas.df().sample(frac=1).reset_index(drop=True)
    M125_test = tree_M125_test.pandas.df().sample(frac=1).reset_index(drop=True)
    M130_test = tree_M130_test.pandas.df().sample(frac=1).reset_index(drop=True)
    M140_test = tree_M140_test.pandas.df().sample(frac=1).reset_index(drop=True)
    M160_test = tree_M160_test.pandas.df().sample(frac=1).reset_index(drop=True)
    M180_test = tree_M180_test.pandas.df().sample(frac=1).reset_index(drop=True)
    M200_test = tree_M200_test.pandas.df().sample(frac=1).reset_index(drop=True)
    M250_test = tree_M250_test.pandas.df().sample(frac=1).reset_index(drop=True)
    M300_test = tree_M300_test.pandas.df().sample(frac=1).reset_index(drop=True)
    """
    M80_train = tree_M80_train.pandas.df()
    M90_train = tree_M90_train.pandas.df()
    M100_train = tree_M100_train.pandas.df()
    M110_train = tree_M110_train.pandas.df()
    M120_train = tree_M120_train.pandas.df()
    M125_train = tree_M125_train.pandas.df()
    M130_train = tree_M130_train.pandas.df()
    M140_train = tree_M140_train.pandas.df()
    M160_train = tree_M160_train.pandas.df()
    M180_train = tree_M180_train.pandas.df()
    M200_train = tree_M200_train.pandas.df()
    M250_train = tree_M250_train.pandas.df()
    M300_train = tree_M300_train.pandas.df()
    M80_test = tree_M80_test.pandas.df()
    M90_test = tree_M90_test.pandas.df()
    M100_test = tree_M100_test.pandas.df()
    M110_test = tree_M110_test.pandas.df()
    M120_test = tree_M120_test.pandas.df()
    M125_test = tree_M125_test.pandas.df()
    M130_test = tree_M130_test.pandas.df()
    M140_test = tree_M140_test.pandas.df()
    M160_test = tree_M160_test.pandas.df()
    M180_test = tree_M180_test.pandas.df()
    M200_test = tree_M200_test.pandas.df()
    M250_test = tree_M250_test.pandas.df()
    M300_test = tree_M300_test.pandas.df()
    """


    #M100_train = pd.concat([M100_train,M100_train,M100_train],ignore_index=True,sort=False).sample(frac=1).reset_index(drop=True)
    #M110_train = pd.concat([M110_train,M110_train],ignore_index=True,sort=False).sample(frac=1).reset_index(drop=True)
    #M120_train = pd.concat([M120_train,M120_train],ignore_index=True,sort=False).sample(frac=1).reset_index(drop=True)
    #M100_test = pd.concat([M100_test,M100_test,M100_test],ignore_index=True,sort=False).sample(frac=1).reset_index(drop=True)
    #M110_test = pd.concat([M110_test,M110_test],ignore_index=True,sort=False).sample(frac=1).reset_index(drop=True)
    #M120_test = pd.concat([M120_test,M120_test],ignore_index=True,sort=False).sample(frac=1).reset_index(drop=True)

    #M100_train = pd.concat([M100_train,M100_train,M100_train,M100_train,M100_train,M100_train],ignore_index=True,sort=False).sample(frac=1).reset_index(drop=True)
    #M110_train = pd.concat([M110_train,M110_train,M110_train,M110_train],ignore_index=True,sort=False).sample(frac=1).reset_index(drop=True)
    #M120_train = pd.concat([M120_train,M120_train,M120_train],ignore_index=True,sort=False).sample(frac=1).reset_index(drop=True)
    #M125_train = pd.concat([M125_train,M125_train],ignore_index=True,sort=False).sample(frac=1).reset_index(drop=True)
    #M130_train = pd.concat([M130_train,M130_train],ignore_index=True,sort=False).sample(frac=1).reset_index(drop=True)
    #M140_train = pd.concat([M140_train,M140_train],ignore_index=True,sort=False).sample(frac=1).reset_index(drop=True)
    #M200_train = pd.concat([M200_train,M200_train],ignore_index=True,sort=False).sample(frac=1).reset_index(drop=True)
    #M100_test = pd.concat([M100_test,M100_test,M100_test,M100_test,M100_test,M100_test],ignore_index=True,sort=False).sample(frac=1).reset_index(drop=True)
    #M110_test = pd.concat([M110_test,M110_test,M110_test,M110_test],ignore_index=True,sort=False).sample(frac=1).reset_index(drop=True)
    #M120_test = pd.concat([M120_test,M120_test,M120_test],ignore_index=True,sort=False).sample(frac=1).reset_index(drop=True)
    #M125_test = pd.concat([M125_test,M125_test],ignore_index=True,sort=False).sample(frac=1).reset_index(drop=True)
    #M130_test = pd.concat([M130_test,M130_test],ignore_index=True,sort=False).sample(frac=1).reset_index(drop=True)
    #M140_test = pd.concat([M140_test,M140_test],ignore_index=True,sort=False).sample(frac=1).reset_index(drop=True)
    #M200_test = pd.concat([M200_test,M200_test],ignore_index=True,sort=False).sample(frac=1).reset_index(drop=True)
    #cut_length_train = min(len(M80_train.index),len(M90_train.index),len(M100_train.index),len(M110_train.index),len(M120_train.index),len(M125_train.index),len(M130_train.index),len(M140_train.index),len(M160_train.index),len(M180_train.index),len(M200_train.index),len(M250_train.index),len(M300_train.index))
    #cut_length_test = min(len(M80_test.index),len(M90_test.index),len(M100_test.index),len(M110_test.index),len(M120_test.index),len(M125_test.index),len(M130_test.index),len(M140_test.index),len(M160_test.index),len(M180_test.index),len(M200_test.index),len(M250_test.index),len(M300_test.index))
    cut_length_train = min(len(M100_train.index),len(M110_train.index),len(M120_train.index),len(M125_train.index),len(M130_train.index),len(M140_train.index),len(M160_train.index),len(M180_train.index),len(M200_train.index))
    cut_length_test = min(len(M100_test.index),len(M110_test.index),len(M120_test.index),len(M125_test.index),len(M130_test.index),len(M140_test.index),len(M160_test.index),len(M180_test.index),len(M200_test.index))



    #cut_length_train = len(M125_train.index)
    #cut_length_test = len(M125_test.index)
    #cut_length_train = 40000
    #cut_length_test = len(M160_test.index)

    max_length_train = max(len(M100_train.index),len(M110_train.index),len(M120_train.index),len(M125_train.index),len(M130_train.index),len(M140_train.index),len(M160_train.index),len(M180_train.index),len(M200_train.index),len(M250_train.index),len(M300_train.index))
    max_length_test = max(len(M100_test.index),len(M110_test.index),len(M120_test.index),len(M125_test.index),len(M130_test.index),len(M140_test.index),len(M160_test.index),len(M180_test.index),len(M200_test.index),len(M250_test.index),len(M300_test.index))

    print "cut length train:",cut_length_train
    print "cut length test:",cut_length_test
    print "max length train:",max_length_train
    print "max length test:",max_length_test
    

    print "length M80 train:",len(M80_train.index)
    print "length M90 train:",len(M90_train.index)
    print "length M100 train:",len(M100_train.index)
    print "length M110 train:",len(M110_train.index)
    print "length M120 train:",len(M120_train.index)
    print "length M125 train:",len(M125_train.index)
    print "length M130 train:",len(M130_train.index)
    print "length M140 train:",len(M140_train.index)
    print "length M160 train:",len(M160_train.index)
    print "length M180 train:",len(M180_train.index)
    print "length M200 train:",len(M200_train.index)
    print "length M250 train:",len(M250_train.index)
    print "length M300 train:",len(M300_train.index)

    """
    M80_train = M80_train[:cut_length_train]
    M90_train = M90_train[:cut_length_train]
    M100_train = M100_train[:cut_length_train]
    M110_train = M110_train[:cut_length_train]
    M120_train = M120_train[:cut_length_train]
    M125_train = M125_train[:cut_length_train]
    M130_train = M130_train[:cut_length_train]
    M140_train = M140_train[:cut_length_train]
    M160_train = M160_train[:cut_length_train]
    M180_train = M180_train[:cut_length_train]
    M200_train = M200_train[:cut_length_train]
    M250_train = M250_train[:cut_length_train]
    M300_train = M300_train[:cut_length_train]
    M80_test = M80_test[:cut_length_test]
    M90_test = M90_test[:cut_length_test]
    M100_test = M100_test[:cut_length_test]
    M110_test = M110_test[:cut_length_test]
    M120_test = M120_test[:cut_length_test]
    M125_test = M125_test[:cut_length_test]
    M130_test = M130_test[:cut_length_test]
    M140_test = M140_test[:cut_length_test]
    M160_test = M160_test[:cut_length_test]
    M180_test = M180_test[:cut_length_test]
    M200_test = M200_test[:cut_length_test]
    M250_test = M250_test[:cut_length_test]
    M300_test = M300_test[:cut_length_test]
    """

    
    train = pd.concat([M80_train,M90_train,M100_train,M110_train,M120_train,M125_train,M130_train,M140_train,M160_train,M180_train,M200_train,M250_train,M300_train],ignore_index=True,sort=False).sample(frac=1).reset_index(drop=True)
    test = pd.concat([M80_test,M90_test,M100_test,M110_test,M120_test,M125_test,M130_test,M140_test,M160_test,M180_test,M200_test,M250_test,M300_test],ignore_index=True,sort=False).sample(frac=1).reset_index(drop=True)       
   
    #train = pd.concat([M100_train,M110_train,M120_train,M125_train,M130_train,M140_train,M160_train,M180_train,M200_train,M250_train,M300_train],ignore_index=True,sort=False).sample(frac=1).reset_index(drop=True)
    #test = pd.concat([M100_test,M110_test,M120_test,M125_test,M130_test,M140_test,M160_test,M180_test,M200_test,M250_test,M300_test],ignore_index=True,sort=False).sample(frac=1).reset_index(drop=True)

    #train = pd.concat([M110_train,M120_train,M125_train,M130_train,M140_train],ignore_index=True,sort=False).sample(frac=1).reset_index(drop=True)
    #test = pd.concat([M110_test,M120_test,M125_test,M130_test,M140_test],ignore_index=True,sort=False).sample(frac=1).reset_index(drop=True)

    #train = pd.concat([M80_train,M90_train,M100_train,M110_train,M120_train,M125_train,M130_train,M140_train,M160_train,M180_train,M200_train,M250_train,M300_train],ignore_index=True,sort=False)
    #test = pd.concat([M80_test,M90_test,M100_test,M110_test,M120_test,M125_test,M130_test,M140_test,M160_test,M180_test,M200_test,M250_test,M300_test],ignore_index=True,sort=False)
    #train, test= train_test_split(all_sample, test_size=0.5, shuffle=True)
    

    inputs_train = train[inputlist]
    inputs_test = test[inputlist]

    target_train = train["H_mass_gen"]
    target_test = test["H_mass_gen"]

    inputs_train = (inputs_train-inputs_train.mean())/inputs_train.std() #standardize input variables
    inputs_test = (inputs_test-inputs_test.mean())/inputs_test.std()

    inputs_train = inputs_train.values  #make numpy arrays to avoid mismatch in label names for prediction
    inputs_test = inputs_test.values
    target_train = target_train.values
    target_test = target_test.values
    #weights_train = weights_train.values

    eval_set = [(inputs_train,target_train),(inputs_test,target_test)]

    #model = xgb.XGBClassifier(n_estimators=1000,learning_rate=0.01)
    #model = xgb.XGBClassifier(n_estimators=2000,learning_rate=0.01)
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
    """
    #model.fit(inputs_train,target_train,sample_weight=weights_train, eval_metric=["merror","mlogloss"], eval_set=eval_set, verbose=False)
    model.fit(inputs_train,target_train, eval_metric=["merror","mlogloss"], eval_set=eval_set, verbose=False)
    preds = model.predict(inputs_test)
    accuracy = accuracy_score(target_test,preds)
    
    xgb.plot_importance(model)
    pyplot.show()

    print("Accuracy: %.2f%%" % (accuracy * 100.0))

    pickle.dump(model, open(modelname, 'wb'))
    print "saved model as %s"%modelname
    """
    file = open("inputlist.txt","w")
    file.write("%s"%inputlist)
    file.close()
    neural_network_train(batch_size,epochs,inputs_train,target_train,inputs_test,target_test)


  
if args.predict:
    #model = pickle.load(open(modelname, 'rb'))
    file = open("inputlist.txt","r")
    listfromfile = file.read()[1:-1].replace("'","").replace(" ","")
    inputlist = list(listfromfile.split(","))
    print "evaluating NN on all samples, this will take a while..."
    for sample_shortname in samples:
        start_sample = time.time()
        sample = getsamples("comb","UL",year,preVFP)[sample_shortname]
        print "predicting for sample:",sample
        rootfile = uproot.open(filedir+"/"+sample+".root")
        tree = rootfile["tree"]
        dataframe = tree.pandas.df()
        inputs = dataframe[inputlist]
        inputs = (inputs-inputs.mean())/inputs.std() #standardize inputs
        zero_list = ['0.0']*inputs.shape[0]
        one_list = ['1.0']*inputs.shape[0]
        inputs.insert(0,"",zero_list,True)
        inputs.insert(1,"",one_list,True)
        inputs.insert(2,"",zero_list,True)
        inputs.insert(3,"",zero_list,True)
        inputs = inputs.values
        prediction = neural_network_predict(inputs)
        infile = TFile(filedir+"/"+sample+".root")
        middle_time = time.time()
        intree = infile.Get("tree")
        outfile = TFile(outdir+"/"+sample+".root","RECREATE")
        new_tree=intree.CopyTree("")
        infile.Close()
        NNoutput = array('f',[0.0])
        NNoutputBranch = new_tree.Branch('NNoutput', NNoutput, 'NNoutput/F')
        for event in range(0,new_tree.GetEntries()):
            NNoutput[0] = prediction[event]
            NNoutputBranch.Fill()
        outfile.Write()
        outfile.Close()
        end_sample = time.time()
        print "time for prediction:",middle_time-start_sample
        print "time for adding:",end_sample-middle_time
        print "time for sample:",end_sample-start_sample
        
        
    print "finished successfully"

