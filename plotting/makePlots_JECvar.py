import plotting as plot
from analysis import *
import ROOT
from ROOT import TColor
import argparse
import json
import os
import fnmatch
from copy import deepcopy
from array import array
import ctypes

ROOT.TH1.SetDefaultSumw2(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)
plot.ModTDRStyle()

def processComp(leg,plots,colour,norm=1.):
  return dict([('leg_text',leg),('plot_list',plots),('colour',colour),('norm',norm)])

def processCompSignal(leg,plots,colour,style,norm=1.):
  return dict([('leg_text',leg),('plot_list',plots),('colour',colour),('style',style),('norm',norm)])


def MakeStackedPlot(name, outdir, hists, sys, cfg):
    #bkgscheme =  [processComp("TT",["TTTo2L2Nu"],plot.CreateTransparentColor(600,0.5)),processComp("TT %s up"%sys,["TTTo2L2Nu_%sUp"%sys],plot.CreateTransparentColor(TColor.GetColor(187,5,30), 0.5)),processComp("TT %s down"%sys,["TTTo2L2Nu_%sDown"%sys],plot.CreateTransparentColor(TColor.GetColor(0,153,76), 0.5))]
    #bkgscheme =  [processComp("MC",["MC"],plot.CreateTransparentColor(600,0.5)),processComp("MC %s up"%sys,["TT_%sUp"%sys,"QCD","WJets_%sUp"%sys,"DYJets_%sUp"%sys,"ST_%sUp"%sys,"VV_%sUp"%sys,"ZH_%sUp"%sys,"VBF_%sUp"%sys,"ttH_%sUp"%sys],plot.CreateTransparentColor(TColor.GetColor(187,5,30), 0.5)),processComp("MC %s down"%sys,["TT_%sDown"%sys,"QCD","WJets_%sDown"%sys,"DYJets_%sDown"%sys,"ST_%sDown"%sys,"VV_%sDown"%sys,"ZH_%sDown"%sys,"VBF_%sDown"%sys,"ttH_%sDown"%sys],plot.CreateTransparentColor(TColor.GetColor(0,153,76), 0.5))]
    bkgscheme =  [processComp("bbHtt",["bbHtt"],plot.CreateTransparentColor(600,0.5)),processComp("bbHtt %s up"%sys,["bbHtt_%sUp"%sys],plot.CreateTransparentColor(TColor.GetColor(187,5,30), 0.5)),processComp("bbHtt %s down"%sys,["bbHtt_%sDown"%sys],plot.CreateTransparentColor(TColor.GetColor(0,153,76), 0.5))]
    copyhists = {}
    for hname, h in hists.items():
        copyhists[hname] = h.Clone()
    
    
    hists = copyhists

    # Canvas and pads
    canv = ROOT.TCanvas(name, name)
    pads = plot.TwoPadSplit(0.29,0.01,0.01)
    #pads = plot.TwoPadSplit(0.13,0.01,0.01) #for signal only plot

    h_data = hists['data_obs']
    #if h_data.Integral()!=0:
    #  h_data.Scale(1./h_data.Integral())
    h_axes = [h_data.Clone() for x in pads]
    
    #for h in h_axes:
    #    h.SetTitle("")
    #    h.Reset()

    build_h_tot = True
    h_tot = None
   
    if isinstance(cfg['x_title'], list) or isinstance(cfg['x_title'], tuple):
        x_title = cfg['x_title'][0]
        units = cfg['x_title'][1]
    else:
        x_title = cfg['x_title']
        units = ''

    #if x_title == '' and h_data.GetXaxis().GetTitle() != '':
    #    x_title = h_data.GetXaxis().GetTitle()

    #if ':' in x_title:
    #    units = x_title.split(':')[1]
    #    x_title = x_title.split(':')[0]
    
    if cfg['logy']:
        pads[0].SetLogy()
        if 'bbHtt' in bkgscheme[0]['plot_list']:
          h_axes[0].SetMinimum(0.1)
        else:
          h_axes[0].SetMinimum(cfg['logy_min'])
    #pads[0].SetLogy()
    #h_axes[0].SetMinimum(10.)
    #h_axes[0].SetMaximum(1000.)

    #plot.StandardAxes(h_axes[0].GetXaxis(), h_axes[0].GetYaxis(), x_title, units) #for signal only plot
    plot.StandardAxes(h_axes[1].GetXaxis(), h_axes[0].GetYaxis(), x_title, units)
    h_axes[0].GetXaxis().SetLabelSize(0) #comment for signal only plot
    h_axes[0].Draw("AXIS")
    #h_axes[1].GetYaxis().SetTitle("flat/polN")
    
    # A dict to keep track of the hists
    h_store = {}
    p_store = {}

    legend = ROOT.TLegend(*([0.6, 0.75, 0.90, 0.91, '', 'NBNDC']))
    legend.SetNColumns(2)
    stack = ROOT.THStack()
    stack1 = ROOT.THStack()

    curr_auto_colour = 0
    all_input_hists = []
    
    output_name = ""
    ##comment here for only signal plot ####
    for entry in bkgscheme:
        all_input_hists.append(entry['plot_list'])
        hist = hists[entry['plot_list'][0]]
        #if cfg['type'] == 'multihist':
        #    plot.Set(hist, FillColor=col, MarkerColor=col, LineColor=col, Title=info['legend'], MarkerSize=info['marker_size'], LineWidth=info['line_width'], LineStyle=info['line_style'])
        plot.Set(hist, FillColor=entry['colour'], MarkerColor=entry['colour'], Title=entry['leg_text'])
        if len(entry['plot_list']) > 1:
            for addhist in entry['plot_list'][1:]:
                hist.Add(hists[addhist])
        h_store[entry['plot_list'][0]] = hist
        p_store[entry['plot_list'][0]] = hist.Clone()
        if 'bbHtt' in entry['plot_list'][0]:
          if entry['plot_list'][0]=='bbHtt':
            h_MC=hist.Clone()
            output_name = "bbHtt_%s"%sys
            if h_tot is None:
                h_tot = hist.Clone()
            else:
                h_tot.Add(hist)
          elif entry['plot_list'][0]=='bbHtt_%sUp'%sys:
            h_MC_up=hist.Clone()
          elif entry['plot_list'][0]=='bbHtt_%sDown'%sys:
            h_MC_down=hist.Clone()
        elif 'TTTo2L2Nu' in entry['plot_list'][0]:
          if entry['plot_list'][0]=='TTTo2L2Nu':
            h_MC=hist.Clone()
            output_name = "TT_%s"%sys
            if h_tot is None:
                h_tot = hist.Clone()
            else:
                h_tot.Add(hist)
          elif entry['plot_list'][0]=='TTTo2L2Nu_%sUp'%sys:
            h_MC_up=hist.Clone()
          elif entry['plot_list'][0]=='TTTo2L2Nu_%sDown'%sys:
            h_MC_down=hist.Clone()
        else:
          if entry['plot_list'][0]=='MC':
            h_MC=hist.Clone()
            output_name = "MC_%s"%sys
            if h_tot is None:
                h_tot = hist.Clone()
            else:
                h_tot.Add(hist)
          elif entry['plot_list'][0]=='TT_%sUp'%sys:
            h_MC_up=hist.Clone()
          elif entry['plot_list'][0]=='TT_%sDown'%sys:
            h_MC_down=hist.Clone()
        stack.Add(hist)
    #h_tot = h_MC.Clone() #for b-tag variations
    # h_tot_purity = h_tot.Clone()
    h_tot.SetFillColor(plot.CreateTransparentColor(12, 0.3))
    #h_tot.SetFillColor(plot.CreateTransparentColor(12, 0.)) #for variations
    h_tot.SetMarkerSize(0)
    
    #if not cfg['hide_data']:
    #    legend.AddEntry(h_data, 'Observed', 'PL')
    
      
    for ele in reversed(bkgscheme):
        legend.AddEntry(h_store[ele['plot_list'][0]], ele['leg_text'], "F")

    #legend.AddEntry(h_tot, 'Stat. Uncertainty', 'F')

    #stack.Draw('HISTSAME')
    #stack1.Draw('nostackHISTSAME')
    stack.Draw('nostackHISTSAME') #for variations
    h_tot.Draw("E2SAME")

    
    #if name in ["BDToutput","BDTisSignal","BDTisTT","BDTisDY","BDToutSig"]:
    #if name in ["BDToutput","BDTisSignal","BDToutSig"]:
    #  h_tot_cut = hists["MC_cut"]
    #  h_data_cut = hists["data_obs_cut"]
    
    
        
    #### end comment here ####

    if 'bbHtt' in output_name:
      plot.FixTopRange(pads[0],10., 0.)
    else:
      plot.FixTopRange(pads[0],80000., 0.)
    legend.Draw()
    
    # if cfg['legend_padding'] > 0.:
    #     plot.FixBoxPadding(pads[0], legend, cfg['legend_padding'])
    
    #### comment here for signal only plot ####
    # Do the ratio plot
    r_store = {}
    r_data = None
    r_tot = None
    r_ext_tot = None
    pads[1].cd()
    pads[1].SetGrid(0, 1)
    if len(cfg['ratio_range']):
            if 'bbHtt' in output_name:
              h_axes[1].GetYaxis().SetRangeUser(0.2,1.8)
            else:
              h_axes[1].GetYaxis().SetRangeUser(*cfg['ratio_range'])
    h_axes[1].Draw() #commment for PR plot
    
    
    chi2test = ""
    chi2 = ctypes.c_double()
    ndf = ctypes.c_int()
    output = ctypes.c_int()
    
    #r_tot = plot.MakeRatioHist(h_MC, h_MC, True, False)
    r_tot = plot.MakeRatioHist(h_tot, h_tot, True, False)
    r_tot.SetMarkerColor(plot.CreateTransparentColor(600, 0.))
    r_tot.Draw('E2SAME')
    r_up = plot.MakeRatioHist(h_MC, h_MC_up, False, True)
    r_down = plot.MakeRatioHist(h_MC, h_MC_down, False, True)

    r_up.SetMarkerColor(plot.CreateTransparentColor(TColor.GetColor(187,5,30), 0.7))
    r_down.SetMarkerColor(plot.CreateTransparentColor(TColor.GetColor(0,153,76), 0.7))
    r_up.Draw('SAME')
    r_down.Draw('SAME')
    
    #### end comment here ####
    
    
    # Go back and tidy up the axes and frame
    pads[0].cd() #comment for PR plot
    pads[0].GetFrame().Draw()
    pads[0].RedrawAxis()
    
    # CMS logo
    plot.DrawCMSLogo(pads[0], "CMS", "Internal", 10, 0.045, 0.05, 1.0, '', 1.0) #Comment for PR plot
    #plot.DrawCMSLogo(pads[0], "Private work", "(CMS simulation)", 10, 0.045, 0.05, 1.0, '', 1.0) #Comment for PR plot
    plot.DrawTitle(pads[0], cfg["title_right"], 3)

    latex = ROOT.TLatex()
    plot.Set(latex, NDC=None, TextFont=42, TextSize=0.03)
    latex.DrawLatex(0.20, 0.75, channel_text)
    latex.DrawLatex(0.20, 0.70, "norm up: %s"%round(h_MC_up.Integral(),2))
    latex.DrawLatex(0.20, 0.65, "norm nominal: %s"%round(h_MC.Integral(),2))
    latex.DrawLatex(0.20, 0.60, "norm down: %s"%round(h_MC_down.Integral(),2))
    #latex.DrawLatex(0.20, 0.24, chi2test)
    #plot.DrawTitle(pads[0], args.title, 1)
    
    # ... and we're done
    for fmt in cfg["formats"]:
        canv.Print(outdir + '/' + name +'_'+output_name+'.%s' %fmt)
  

parser = argparse.ArgumentParser()
parser.add_argument('--input', '-i', help='File with histograms to plot')
parser.add_argument('--output', '-o', default='./plots', help='top level output directory')
parser.add_argument('-s', '--sys', dest='sys', type=str, default='', action='store')
args = parser.parse_args()

filename = args.input
channel =filename.split("_")[0]
year = filename.split("_")[1].split(".")[0]
sys = args.sys
preVFP = ""
if "preVFP" in filename:
  preVFP = "_preVFP"
if "comb" in filename:
  preVFP = "_comb"
if channel == "mutau":
  channel_text = "#mu#tau_{h} channel"
elif channel == "etau":
  channel_text = "e#tau_{h} channel"

if year=="UL2018":
  lumi = 59.7
elif year=="UL2017":
  lumi = 41.5
elif year=="2018":
  lumi = 59.7
else:
  if "comb" in filename:
    lumi = 36.3
  elif preVFP=="_preVFP":
    lumi = 19.5
  else:
    lumi = 16.8

file = ROOT.TFile("./root/"+filename)
output = './plots/BDT/%s/'%filename[:-5]
node = TDirToNode(file)

made_dirs = set()


titleright = "%s %.1f fb^{-1} (13 TeV)"%(year,float(lumi))
#titleright = "%s %.1f fb^{-1} (13 TeV)"%("2018",float(lumi)) #for PR plot

plotcfg = {
  "x_title" : "test",
  "hide_data" : True,
  "logy" : False,
  "formats" : ["pdf","png"],
  "ratio_range" : [0.7,1.3],
  "title_right" : titleright,
  "do_overlay" : True
}

config_by_setting = {
  "x_title": [
    ('BDTisSignal', ('BDT p_{S}','')),
    ('BDToutput', ('BDT p_{comb}','')),
    ('BDTisTT', ('BDT p_{TT}','')),
    ('BDTisDY', ('BDT p_{DY}','')),
    ('BDTisjjH', ('BDT p_{jjH}','')),
    ('BDToutSig', ('max BDT p_{S}','')),
    ('BDToutTT', ('max BDT p_{TT}','')),
    ('BDToutDY', ('max BDT p_{DY}','')),
    ('BDTCR', ('BDT CR','')),
    
    ],
      
    "hide_data": [('H_mass', True),('collinear_mass', False),('BDToutput', True),('Jet1_btag',True),('BDTisSignal', False),('BDTisTT', False),('BDTisDY', False),('BDToutSig',False),('BDToutTT',False),('BDToutDY',False),('MET', False)],
    #"hide_data": [('H_mass', True),('BDToutput', True),('BDTisSignal', True),('BDTisTT', True),('BDTisDY', True),('BDToutSig',True),('BDToutTT',True),('BDToutDY',True),('MET', True)],
    #"logy":[('BDToutput', False),('BDTisSignal', True),('BDTisTT', True),('BDTisDY', True),('BDToutSig', True),('BDToutTT', True),('BDToutDY', True),('H_mass', True)],
    #"logy_min":[('BDToutput', 1),('BDTisSignal', 1),('BDTisTT', 1),('BDTisDY', 1),('BDToutSig', 1),('BDToutTT', 1),('BDToutDY', 1),('H_mass', 30)],
    "logy":[('BDToutput', True),('BDTisSignal', True),('BDTisTT', True),('BDTisDY', True),('BDToutSig', True),('BDToutTT', True),('BDToutDY', True),('BDTCR', True)],
    "logy_min":[('BDToutput', 1),('BDTisSignal', 1),('BDTisTT', 1),('BDTisDY', 1),('BDToutSig', 10),('BDToutTT', 10),('BDToutDY', 10),('BDTCR', 1)],
    "ratio_range" :[('BDToutSig', [0.8,1.2]),('BDToutTT', [0.95,1.05]),('BDToutDY',[0.95,1.05])]
    }

for path, subnode in node.ListNodes(withObjects=True):
  print(path)
  if path not in ["BDToutSig","BDToutTT","BDToutDY"]:
    continue
  split_path = path.split('/')[:-1]
  name = path.split('/')[-1]
  target_dir = os.path.join(output, *split_path)
  if target_dir not in made_dirs:
    os.system('mkdir -p %s' % target_dir)
    made_dirs.add(target_dir)
  hists = {}
  for opath, objname, obj in subnode.ListObjects(depth=0):
    hists[objname] = obj
    
  for setting, vardict in config_by_setting.items():
    for pathkey, val in vardict:
      if fnmatch.fnmatch(path, pathkey):
        plotcfg[setting] = val
        print('Path %s, setting %s, to value %s' % (path, setting, val))
  MakeStackedPlot(name, target_dir, hists, sys, plotcfg)
