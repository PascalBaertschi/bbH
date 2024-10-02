import ROOT
import glob
import sys
# import json
from array import array
from analysis import *
from argparse import ArgumentParser
ROOT.RooWorkspace.imp = getattr(ROOT.RooWorkspace, 'import')
ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.TH1.AddDirectory(0)

parser = ArgumentParser()

parser.add_argument('-y', '--year',     dest='year', action='store', choices=[2016,2017,2018], type=int, default=2018)
parser.add_argument('-v', '--variation', dest='variation',action='store',type=str,default="")
parser.add_argument('-p', '--preVFP',  dest='preVFP', action='store_const', const="_preVFP",default="")
args = parser.parse_args()

year     = args.year
variation = args.variation
preVFPtag    = args.preVFP


if year!=2016:
    cfg =   {
        'name': 'dielectron_mass_pt_eta_bins',
        'var': 'dielectron_mass',
        'binvar1_x': 'Ele1_pt',
        'binvar2_x': 'Ele2_pt',
        'binvar_x': 'Ele_pt',
        'bins_x': [33., 34., 35., 36., 37., 38., 39., 40., 45., 50. ,75., 100., 200.],
        'binvar1_y': 'abs(Ele1_eta)',
        'binvar2_y': 'abs(Ele2_eta)',
        'binvar_y': 'abs(Ele_eta)',
        'bins_y': [0, 0.8, 1.444, 1.566, 2., 2.1],
    }
else:
    cfg =   {
        'name': 'dielectron_mass_pt_eta_bins',
        'var': 'dielectron_mass',
        'binvar1_x': 'Ele1_pt',
        'binvar2_x': 'Ele2_pt',
        'binvar_x': 'Ele_pt',
        'bins_x': [26., 27., 28., 29., 30., 31., 32., 33., 34., 35., 36., 37., 38., 39., 40., 45., 50. ,75., 100., 200.],
        'binvar1_y': 'abs(Ele1_eta)',
        'binvar2_y': 'abs(Ele2_eta)',
        'binvar_y': 'abs(Ele_eta)',
        'bins_y': [0, 0.8, 1.444, 1.566, 2., 2.1],
    }




if variation=="gen":
    cfg['var'] = 'gen'+cfg['var']
if variation=="" or variation=="gen" or variation=="tag":
    binning = (50, 75, 125)
elif variation=="up":
    binning = (50, 80, 130)
elif variation=="down":
    binning = (50, 70, 120)

cfg['hist'] = ROOT.TH2D(cfg['name'], cfg['name'],
len(cfg['bins_x'])-1, array('d', cfg['bins_x']),
len(cfg['bins_y'])-1, array('d', cfg['bins_y']))

hist = cfg['hist']
hist.GetXaxis().SetTitle(cfg['binvar_x'])
hist.GetYaxis().SetTitle(cfg['binvar_y'])
"""
hist = cfg['hist']
hist.GetXaxis().SetTitle(cfg['binvar1_x'])
hist.GetYaxis().SetTitle(cfg['binvar1_y'])
"""
cfg['bins'] = []

for i in range(1, hist.GetNbinsX()+1):
    for j in range(1, hist.GetNbinsY()+1):
        cfg['bins'].append('%s>=%g && %s<%g && %s>=%g && %s<%g' % (
            cfg['binvar1_x'], hist.GetXaxis().GetBinLowEdge(i),
            cfg['binvar1_x'], hist.GetXaxis().GetBinUpEdge(i),
            cfg['binvar1_y'], hist.GetYaxis().GetBinLowEdge(j),
            cfg['binvar1_y'], hist.GetYaxis().GetBinUpEdge(j),
        ))
        cfg['bins'].append('%s>=%g && %s<%g && %s>=%g && %s<%g' % (
            cfg['binvar2_x'], hist.GetXaxis().GetBinLowEdge(i),
            cfg['binvar2_x'], hist.GetXaxis().GetBinUpEdge(i),
            cfg['binvar2_y'], hist.GetYaxis().GetBinLowEdge(j),
            cfg['binvar2_y'], hist.GetYaxis().GetBinUpEdge(j),
        ))
       

remaps = {
    '2016_preVFP': {
        'mc': 'DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8',
        'data':'SingleElectron_Run2016BCDEF',
    },
    '2016': {
        'mc': 'DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8',
        'data':'SingleElectron_Run2016FGH',
    },
    '2017': {
        'mc': 'DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8',
        'data':'SingleElectron_Run2017BCDEF',
    },
    '2018': {
       'mc': 'DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8',
        'data':'EGamma_Run2018ABCD-UL2018',
    },
}




remap = remaps['%s%s'%(year,preVFPtag)]
samplesdir = '/pnfs/psi.ch/cms/trivcat/store/user/pbaertsc/bbh/EIsoSF/samples_UL%s%s/'%(year,preVFPtag)
samples = {}
for sa in remap:
    samples[sa] = remap[sa]


#hists = Node()

gentag = ""
for sample in remap:
    if variation=="gen" and sample=="data": 
        break
    if "Run" in sample:
        weight = '1.'
    else:
        if variation=="gen":
            weight = 'GenWeight * LumiWeight'
        else:
            weight = 'EventWeight * LumiWeight'
    if variation!="":
        outfile = ROOT.TFile('root/EIsoEff_UL%s%s_%s_%s.root' % (year,preVFPtag,sample,variation), 'RECREATE')
    else:
        outfile = ROOT.TFile('root/EIsoEff_UL%s%s_%s.root' % (year,preVFPtag,sample), 'RECREATE')

    hists = Node()

    for b in cfg['bins']:
        if "Ele1" in b:
            hists[cfg['name']]['%s:fail' % b] = Hist('TH1F', sample=sample, var=[cfg['var']], binning=binning, sel='((%s) && Ele2_tag && Ele1_id && Ele2_id && Ele1_iso>0.1)' %b, wt=weight)
            hists[cfg['name']]['%s:pass' % b] = Hist('TH1F', sample=sample, var=[cfg['var']], binning=binning, sel='((%s) && Ele2_tag && Ele1_id && Ele2_id && Ele1_iso<0.1)' %b, wt=weight)
        elif "Ele2" in b:
            hists[cfg['name']]['%s:fail' % b] = Hist('TH1F', sample=sample, var=[cfg['var']], binning=binning, sel='((%s) && Ele1_tag && Ele1_id && Ele2_id && Ele2_iso>0.1)' %b, wt=weight)
            hists[cfg['name']]['%s:pass' % b] = Hist('TH1F', sample=sample, var=[cfg['var']], binning=binning, sel='((%s) && Ele1_tag && Ele1_id && Ele2_id && Ele2_iso<0.1)' %b, wt=weight)
                
  
    MultiDraw(hists, samplesdir, samples, 'tree', mt_cores=4)
    
    for path, node in hists.ListNodes(withObjects=True):
        if cfg["name"]!=path: continue
        for b in cfg['bins']:
           if "Ele2" in b: continue
           b_both = b.replace("Ele1_pt","Ele_pt").replace("Ele1_eta","Ele_eta")
           b2 = b.replace("Ele1_pt","Ele2_pt").replace("Ele1_eta","Ele2_eta")
           node['%s:fail'%b_both] = node['%s:fail'%b] + node['%s:fail'%b2]
           node['%s:pass'%b_both] = node['%s:pass'%b] + node['%s:pass'%b2]
           
           
    NodeToTDir(outfile, hists)
    wsp = ROOT.RooWorkspace('wsp_'+cfg['name'], '')
    if variation=="":
        dilepton_mass_binning = "[50,75,125]"
    elif variation=="up":
        dilepton_mass_binning = "[50,80,130]"
    elif variation=="down":
        dilepton_mass_binning = "[50,70,120]"
    print('%s%s'%(cfg['var'],dilepton_mass_binning))
    var = wsp.factory('%s%s'%(cfg['var'],dilepton_mass_binning))
    
    for b in cfg['bins']:
        if "Ele2" in b: continue
        b_name = b.replace("Ele1_pt","Ele_pt").replace("Ele1_eta","Ele_eta")
        dat = wsp.imp(ROOT.RooDataHist(b_name, '', ROOT.RooArgList(var),ROOT.RooFit.Index(wsp.factory('cat[fail,pass]')),ROOT.RooFit.Import('fail', hists[cfg['name']]['%s:fail' % b_name]),ROOT.RooFit.Import('pass', hists[cfg['name']]['%s:pass' % b_name])))
    outfile.cd()
    wsp.Write()
    cfg['hist'].Write()
    #wsp.Delete()
    outfile.Close()
