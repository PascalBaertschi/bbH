import ROOT
from analysis import *
from argparse import ArgumentParser
import json
import utils
import sys
import shutil
import numpy as np
sys.path.insert(1, os.path.join(sys.path[0], '..')) #to get file in parent directory
from xsections import xsection
from samplenames import getsamples

# import CombineHarvester.CombineTools.plotting as plot

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.TH1.AddDirectory(False)

parser = ArgumentParser()
parser.add_argument('-y', '--year',    dest='year', type=str, default='2018', action='store')
parser.add_argument('-c', '--channel', dest='channel', type=str, default='mutau', action='store')
parser.add_argument('-b', '--BDT', default=False,action='store_true')
parser.add_argument('-p', '--preVFP',  dest='preVFP', action='store_const', const="_preVFP",default="")
parser.add_argument('-t', '--comb',  dest='UL2016comb', action='store_true',default=False)
parser.add_argument('-s', '--sysvar', dest='sysvar', type=str, default='', action='store')
args = parser.parse_args()

year = args.year
channel = args.channel
sysvar = args.sysvar
preVFP = args.preVFP
isBDT = args.BDT
UL2016comb = args.UL2016comb

if UL2016comb:
    preVFP="_comb"

#LUMI        = 137190.
if year=='2018':
    LUMI = 59740
elif year=='2017':
    LUMI = 41530
elif year=='2016':
    if preVFP=="_preVFP":
        LUMI = 19500
    else:
        LUMI = 16800

if sysvar!="":
    sysvar="_"+sysvar


samplesdir = '/pnfs/psi.ch/cms/trivcat/store/user/pbaertsc/bbh/samples_UL%s%s%s/'%(year,preVFP,sysvar)

hists = Node()

selections_prong = [
    {'name':'1prong',
     'selection':'&& (Tau1_decaymode==0 || Tau1_decaymode==1 || Tau1_decaymode==2)'},
    {'name':'3prong',
     'selection':'&& (Tau1_decaymode==10 || Tau1_decaymode==11)'}]


drawvars = [
    ('Mu1_pt',      'Mu1_pt',       [21., 22., 23., 24., 25., 26., 27., 28., 29., 30., 35., 40., 45., 50. ,75., 100., 200.]),
    ('Mu1_eta',     'Mu1_eta',      (30, -2.5, 2.5)),
    ('Ele1_pt',     'Ele1_pt',       (30, 0, 130)),
    ('Ele1_eta',    'Ele1_eta',      (30, -2.5, 2.5)),
    ('Tau1_pt',     'Tau1_pt',      [30., 31., 32., 33., 34., 35., 40., 45., 50. ,75., 100., 200.]),
    ('Tau1_eta',    'Tau1_eta',     (30, -2.5, 2.5)),
    ('Tau1_phi',    'Tau1_phi',     (30, -3.2, 3.2)),
    ('Tau1_mass',   'Tau1_mass',    (30, 0., 2.)),
    ('Tau1_decaymode', 'Tau1_decaymode', (12,0,12)),

]

binning_2d = (16,np.array([21., 22., 23., 24., 25., 26., 27., 28., 29., 30., 35., 40., 45., 50. ,75., 100., 200.]),11,np.array([30., 31., 32., 33., 34., 35., 40., 45., 50. ,75., 100., 200.]))
tau_pt = [30., 31., 32., 33., 34., 35., 40., 45., 50. ,75., 100.,200.]
mutau_eta = [0., 0.9, 1.2, 2.1]
etau_eta = [0., 0.8, 1.444, 1.566, 2., 2.1]
if channel=="mutau":
    lep_eta = mutau_eta
elif channel=="etau":
    lep_eta = etau_etau

for dirname, var, binning in drawvars:
    for sample in ["TTTo2L2Nu","data_obs"]:
        if channel=="mutau":
            if sample=='data_obs': #no veto on gen matched taus and no selection on EventNumber
                selection = 'METTrigger_fired && isHtoMuTau'
                selection_fired = 'METTrigger_fired && isHtoMuTau && MuTauTrigger_fired && Mu1_ctrig_fired && Tau1_ctrig_fired'
            else:
                selection = 'METTrigger_fired && isHtoMuTau'
                selection_fired = 'METTrigger_fired && isHtoMuTau && MuTauTrigger_fired && Mu1_ctrig_fired && Tau1_ctrig_fired'
        
        if sample=='data_obs':
            weight = '1.'
        else:
            if channel=="mutau":
                weight = 'EventWeight * LumiWeight * wt_tt'
        for j in range(len(lep_eta)-1):
            for selection_prong in selections_prong:
                if dirname=="Mu1_pt":
                    hists["2D"][sample+"_%s_lepeta%s"%(selection_prong["name"],lep_eta[j])] = Hist('TH2F', sample=sample, var=["Mu1_pt","Tau1_pt"], binning=binning_2d, sel=selection+selection_prong["selection"]+" && abs(Mu1_eta)>%s && abs(Mu1_eta)<%s"%(lep_eta[j],lep_eta[j+1]), wt=weight)    
                    hists["2D"][sample+"_fired_%s_lepeta%s"%(selection_prong["name"],lep_eta[j])] = Hist('TH2F', sample=sample, var=["Mu1_pt","Tau1_pt"], binning=binning_2d, sel=selection_fired+selection_prong["selection"]+" && abs(Mu1_eta)>%s && abs(Mu1_eta)<%s"%(lep_eta[j],lep_eta[j+1]), wt=weight)   
                    hists[dirname][sample+"_%s_lepeta%s"%(selection_prong["name"],lep_eta[j])] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection+selection_prong["selection"]+" && abs(Mu1_eta)>%s && abs(Mu1_eta)<%s"%(lep_eta[j],lep_eta[j+1]), wt=weight)    
                    hists[dirname][sample+"_fired_%s_lepeta%s"%(selection_prong["name"],lep_eta[j])] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection_fired+selection_prong["selection"]+" && abs(Mu1_eta)>%s && abs(Mu1_eta)<%s"%(lep_eta[j],lep_eta[j+1]), wt=weight)
                    for i in range(len(tau_pt)-1):
                        if dirname=="Mu1_pt":
                            hists[dirname][sample+"_%s_taupt%s_lepeta%s"%(selection_prong["name"],tau_pt[i],lep_eta[j])] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection+selection_prong["selection"]+" && Tau1_pt>%s && Tau1_pt<%s && abs(Mu1_eta)>%s && abs(Mu1_eta)<%s"%(tau_pt[i],tau_pt[i+1],lep_eta[j],lep_eta[j+1]), wt=weight)    
                            hists[dirname][sample+"_fired_%s_taupt%s_lepeta%s"%(selection_prong["name"],tau_pt[i],lep_eta[j])] = Hist('TH1F', sample=sample, var=[var], binning=binning, sel=selection_fired+selection_prong["selection"]+" && Tau1_pt>%s && Tau1_pt<%s && abs(Mu1_eta)>%s && abs(Mu1_eta)<%s"%(tau_pt[i],tau_pt[i+1],lep_eta[j],lep_eta[j+1]), wt=weight)
                           
MultiDraw(hists, samplesdir, getsamples(channel,"UL",year,preVFP), 'tree', mt_cores=8)


filename = './root/MET%s_UL%s%s%s.root'%(channel,year,preVFP,sysvar)
fout = ROOT.TFile(filename, 'RECREATE')
NodeToTDir(fout, hists)
fout.Close()


