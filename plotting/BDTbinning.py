import plotting as plot
from analysis import *
import ROOT
from ROOT import TColor
import argparse
import json
import os
import fnmatch
from copy import deepcopy
import numpy as np
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


def MakeStackedPlot(name, outdir, hists, cfg):
    #QCD TColor.GetColor(0,153,76)
    #WJets TColor.GetColor(222,90,106)
    #DYJets TColor.GetColor(248, 206, 104)
    #ST TColor.GetColor(208,240,193)
    #TT TColor.GetColor(155, 152, 204)
    #VV TColor.GetColor(111,45,53)
    #ZH TColor.GetColor(255, 163, 4)
    #VBF TColor.GetColor(187, 5, 30)
    #ttH TColor.GetColor(255,0,255)
    bkgscheme =  [processComp("jet#rightarrow#tau_{h} fakes",["QCD"],TColor.GetColor(0,153,76)),processComp("WJets",["WJets_incl","WJets_0J","WJets_1J","WJets_2J"],TColor.GetColor(222,90,106)),processComp("DYJets",["DYJets_incl","DYJets_0J","DYJets_1J","DYJets_2J"], TColor.GetColor(248, 206, 104)),processComp("ST",["ST"], TColor.GetColor(208,240,193)),processComp("TT",["TT"], TColor.GetColor(155, 152, 204)),processComp("VV",["VV"],TColor.GetColor(111,45,53)),processComp("VH",["ZH"],TColor.GetColor(255, 163, 4)),processComp("VBF",["VBF"],TColor.GetColor(187, 5, 30)),processComp("ttH",["ttH"],TColor.GetColor(255, 0, 255))]
    #bkgscheme =  [processComp("jet#rightarrow#tau_{h} fakes",["QCD_Hcut"],TColor.GetColor(0,153,76)),processComp("WJets",["WJets_incl_Hcut","WJets_0J_Hcut","WJets_1J_Hcut","WJets_2J_Hcut"],TColor.GetColor(222,90,106)),processComp("DYJets",["DYJets_incl_Hcut","DYJets_0J_Hcut","DYJets_1J_Hcut","DYJets_2J_Hcut"], TColor.GetColor(248, 206, 104)),processComp("ST",["ST_Hcut"], TColor.GetColor(208,240,193)),processComp("TT",["TT_Hcut"], TColor.GetColor(155, 152, 204)),processComp("VV",["VV_Hcut"],TColor.GetColor(111,45,53)),processComp("VH",["ZH_Hcut"],TColor.GetColor(255, 163, 4)),processComp("VBF",["VBF_Hcut"],TColor.GetColor(187, 5, 30)),processComp("ttH",["ttH_Hcut"],TColor.GetColor(255, 0, 255))]
    #bkgscheme =  [processComp("jet#rightarrow#tau_{h} fakes",["QCD_Hsigcut"],TColor.GetColor(0,153,76)),processComp("WJets",["WJets_incl_Hsigcut","WJets_0J_Hsigcut","WJets_1J_Hsigcut","WJets_2J_Hsigcut"],TColor.GetColor(222,90,106)),processComp("DYJets",["DYJets_incl_Hsigcut","DYJets_0J_Hsigcut","DYJets_1J_Hsigcut","DYJets_2J_Hsigcut"], TColor.GetColor(248, 206, 104)),processComp("ST",["ST_Hsigcut"], TColor.GetColor(208,240,193)),processComp("TT",["TT_Hsigcut"], TColor.GetColor(155, 152, 204)),processComp("VV",["VV_Hsigcut"],TColor.GetColor(111,45,53)),processComp("VH",["ZH_Hsigcut"],TColor.GetColor(255, 163, 4)),processComp("VBF",["VBF_Hsigcut"],TColor.GetColor(187, 5, 30)),processComp("ttH",["ttH_Hsigcut"],TColor.GetColor(255, 0, 255))]
  
    #bkgscheme =  [processComp("ZZTo2L2Nu",["ZZTo2L2Nu"],plot.CreateTransparentColor(TColor.GetColor(255,0,255),0.3)),processComp("ZZ",["ZZTo4L","ZZTo2L2Q","ZZTo2Nu2Q"],plot.CreateTransparentColor(TColor.GetColor(155, 152, 204),0.3))]
    #bkgscheme =  [processComp("ttWJets",["ttWJets"],TColor.GetColor(255,0,255)),processComp("ttZJets",["ttZJets"],TColor.GetColor(187,5,30)),processComp("tZq",["tZq"],TColor.GetColor(255,163,4)),processComp("ttH",["ttH"],TColor.GetColor(111,45,53))]
    #bkgscheme =  [processComp("ttWJets",["ttWJets"],plot.CreateTransparentColor(TColor.GetColor(255,0,255),0.3)),processComp("ttZJets",["ttZJets"],plot.CreateTransparentColor(TColor.GetColor(187,5,30),0.3)),processComp("tZq",["tZq"],plot.CreateTransparentColor(TColor.GetColor(255,163,4),0.3)),processComp("ttH",["ttH"],plot.CreateTransparentColor(TColor.GetColor(111,45,53),0.3))]
    #bkgscheme =  [processComp("tZq",["tZq"],plot.CreateTransparentColor(TColor.GetColor(0,153,76),0.3)),processComp("ttH",["ttH"],plot.CreateTransparentColor(TColor.GetColor(255,0,255),0.3))]
    #bkgscheme =  [processComp("DYJets",["DYJets_incl","DYJets_0J","DYJets_1J","DYJets_2J"],TColor.GetColor(248, 206, 104)),processComp("embedded",["TauEmbedding"],plot.CreateTransparentColor(TColor.GetColor(222,90,106),0.5)),processComp("TT",["TT"], TColor.GetColor(155, 152, 204))]
    #bkgscheme =  [processComp("MC",["MC"],plot.CreateTransparentColor(634,0.3)),processComp("embedded",["TauEmbedding"],plot.CreateTransparentColor(602, 0.3))]
    #bkgscheme = [processComp("VBF",["VBF"],TColor.GetColor(187, 5, 30))]
    #bkgscheme = [processComp("ttH",["ttH"],TColor.GetColor(255, 0, 255))]
    #bkgscheme = [processComp("VH",["ZH"],TColor.GetColor(255, 163, 4))]
    #bkgscheme =  [processComp("MC",["MC"],plot.CreateTransparentColor(634,0.3)),processComp("MC H_mass SB",["MC_Hcut"],plot.CreateTransparentColor(602, 0.3))]
    #bkgscheme = [processComp("jet#rightarrow#tau_{h} fakes",["QCD"],602)]
    signal = [processCompSignal("bbH+ggH",["bbHtt"],2,2,100),processCompSignal("jjH+ggjjH",["jjHtt"],2,1,100)]
    #signal = [processCompSignal("bbH+ggH",["bbHtt_Hcut"],2,2,100),processCompSignal("jjH+ggjjH",["jjHtt_Hcut"],2,1,100)]
    #signal = [processCompSignal("bbH+ggH",["bbHtt_Hsigcut"],2,2,100),processCompSignal("jjH+ggjjH",["jjHtt_Hsigcut"],2,1,100)]
    #for hname, h in hists.items():
    #    copyhists[hname] = h.Clone()
    
    
    #hists = copyhists

    # Canvas and pads
    canv = ROOT.TCanvas(name, name)
    pads = plot.TwoPadSplit(0.29,0.01,0.01)
    #pads = plot.TwoPadSplit(0.13,0.01,0.01) #for signal only plot

    h_data = hists['data_obs']
    #h_data = hists['data_obs_Hcut']
    #h_data = hists['data_obs_Hsigcut']

    h_axes = [h_data.Clone() for x in pads]
    #h_axes = [hists['ZZTo4L'].Clone() for x in pads]
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
        h_axes[0].SetMinimum(cfg['logy_min'])
        #h_axes[0].SetMinimum(0.001)
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
        if entry['plot_list'][0]=='QCD_norm':
          h_norm=hist.Clone()
        if entry['plot_list'][0]=='QCD':
          h_nominal=hist.Clone()
        if entry['plot_list'][0]=='MC':
          h_MC=hist.Clone()
        if entry['plot_list'][0]=='TT':
          h_TT=hist.Clone()
        if build_h_tot:
            if h_tot is None:
                h_tot = hist.Clone()
            else:
                h_tot.Add(hist)

        #if name=="collinear_mass":
        #  print("hist norm for:",entry['leg_text'],"from ",hist.GetXaxis().GetBinCenter(1),"to ",hist.GetXaxis().GetBinCenter(hist.GetNbinsX()))
        #  print("is ",hist.Integral())
        #if 'embedded' in entry['leg_text']:
        #  stack1.Add(hist)
        #else:
        #  stack.Add(hist)
        stack.Add(hist)
    #h_tot = h_MC.Clone() #for b-tag variations
    # h_tot_purity = h_tot.Clone()
    h_tot.SetFillColor(plot.CreateTransparentColor(12, 0.3))
    #h_tot.SetFillColor(plot.CreateTransparentColor(12, 0.)) #for variations
    h_tot.SetMarkerSize(0)
    
    h_tot.Add(hists["jjHtt"])

    
    if name=="BDToutSig":
      hist_bbH = hists["bbHtt"]
      hist_bkg = h_tot
      Nbins = hist_bbH.GetNbinsX()
      signal_integral = hist_bbH.Integral()
      bkg_integral = hist_bkg.Integral()
      integral_ratio = signal_integral/np.sqrt(bkg_integral)
      print("bbH Integral:",signal_integral," bkg integral:",bkg_integral," with cut:",0.09)
      bins = []
      for i in range(Nbins):
        bins.append(round(hist_bbH.GetBinLowEdge(i+1),5))
      bins.append(1.)
      BinNumber = Nbins
      for i in range(Nbins):
        i = Nbins-i
        bin_bbH = hist_bbH.GetBinContent(i)
        error_sig = hist_bbH.GetBinError(i)
        bin_bkg = hist_bkg.GetBinContent(i)
        error_bkg = hist_bkg.GetBinError(i)
        low_edge = round(hist_bbH.GetBinLowEdge(i),5)
        high_edge = round(hist_bbH.GetBinLowEdge(i+1),5)
        if bin_bbH>signal_integral/10. and error_sig/bin_bbH<0.25 and error_bkg/bin_bkg<0.25 and (high_edge-low_edge)>0.05:
          print(low_edge,"-",high_edge," sig unc:",round(error_sig/bin_bbH,4), "       bkg unc:",round(error_bkg/bin_bkg,4))
          #print("bin_bbH:",bin_bbH," bin_bkg:",bin_bkg)
        else:
          if low_edge!=0.:
            bins.remove(low_edge)
            BinNumber -= 1
            hist_bbH = hist_bbH.Rebin(BinNumber,"rebinned_bbH",np.array(bins))
            hist_bkg = hist_bkg.Rebin(BinNumber,"rebinned_bkg",np.array(bins))
      print("bins:",bins)


    if not cfg['hide_data']:
        legend.AddEntry(h_data, 'Observed', 'PL')
    
      
    for ele in reversed(bkgscheme):
        legend.AddEntry(h_store[ele['plot_list'][0]], ele['leg_text'], "F")

    legend.AddEntry(h_tot, 'Stat. Uncertainty', 'F')

    stack.Draw('HISTSAME')
    #stack1.Draw('nostackHISTSAME')
    #stack.Draw('nostackHISTSAME') #for variations
    h_tot.Draw("E2SAME")

    
    #if name in ["BDToutput","BDTisSignal","BDTisTT","BDTisDY","BDToutSig"]:
    if name in ["BDToutput","BDTisSignal","BDToutSig"]:
      h_tot_cut = hists["MC_cut"]
      h_data_cut = hists["data_obs_cut"]
    
    if name == "H_mass":
      h_tot_cut = hists["MC_Hcut"]
      h_data_cut = hists["data_obs_Hcut"]
    
    if not cfg['hide_data']:
      #if name in ["BDToutput","BDTisSignal","BDTisTT","BDTisDY","BDToutSig"]:
      if name in ["BDToutput","BDTisSignal","BDToutSig"]:
        h_data_cut.Draw('E0SAME')
      elif name == "H_mass":
        h_data_cut.Draw('ESAME')
      else:
        h_data.Draw('E0SAME')
    
        
    #### end comment here ####
    
    ### only bkg plot #####
    # Build overlays
    if cfg['do_overlay']:
        for entry in signal:
            hist = hists[entry['plot_list'][0]].Clone()
            if len(entry['plot_list'])>1:
                for addhist in entry['plot_list'][1:]:
                    hist.Add(hists[addhist])
            plot.Set(hist,LineColor=entry['colour'],LineWidth=2,LineStyle=entry['style'],MarkerSize=0,FillStyle=0,Title=entry['leg_text'])
            for ib in range(1, hist.GetNbinsX() + 1):
                hist.SetBinError(ib, 1E-7)
            h_store[entry['plot_list'][0]] = hist
            hist.Scale(entry['norm'])
            #if hist.Integral()!=0:
            #  hist.Scale(1./hist.Integral())
            hist.Draw("HISTSAME")

        for ele in signal:
            legend.AddEntry(h_store[ele['plot_list'][0]], ele['leg_text'] if entry['norm']==1 else ele['leg_text']+' x '+ str(entry['norm']), "L")
    ###### end comment here #####        
    
    plot.FixTopRange(pads[0], plot.GetPadYMax(pads[0]), 0.35) #change number to change Y axis range
    #plot.FixTopRange(pads[0], plot.GetPadYMax(pads[0]), 0.25) #change number to change Y axis range
    #plot.FixTopRange(pads[0],3510., 0.) #change number to change Y axis range
    #plot.FixTopRange(pads[0],1535., 0.) #change number to change Y axis range 
    #plot.FixTopRange(pads[0],4000., 0.) #change number to change Y axis range
    if name=="mt" or name=="transverse_mass_lepmet":
      plot.FixBothRanges(pads[0],0.,0.,plot.GetPadYMax(pads[0]),0.35)

    #if name in ["Jet1_pt","Jet2_pt","Jet3_pt"]:
    #  plot.FixTopRange(pads[0],8000., 0.)
    #if name=="Jet3_pt":
    #  plot.FixTopRange(pads[0],6000., 0.)
    #plot.FixTopRange(pads[0],100., 0.) #change number to change Y axis range
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
            h_axes[1].GetYaxis().SetRangeUser(*cfg['ratio_range'])
    h_axes[1].Draw() #commment for PR plot
    
    
    chi2test = ""
    chi2 = ctypes.c_double()
    ndf = ctypes.c_int()
    output = ctypes.c_int()
    
    if not cfg['hide_data']:
        #if name in  ["BDToutput","BDTisSignal","BDTisTT","BDTisDY","BDToutSig"]:
        if name in  ["BDToutput","BDTisSignal","BDToutSig"]:
          r_data = plot.MakeRatioHist(h_data_cut, h_tot, True, False)
        elif name == "H_mass":
          r_data = plot.MakeRatioHist(h_data_cut, h_tot, True, False)
        else:
          r_data = plot.MakeRatioHist(h_data, h_tot, True, False)
        r_data.Draw('SAME')
    
    r_tot = plot.MakeRatioHist(h_tot, h_tot, True, False)
    r_tot.Draw('E2SAME')
    if not cfg['hide_data']:
        #if name in ["BDToutput","BDTisSignal","BDTisDY","BDTisTT","BDToutSig"]:
        if name in ["BDToutput","BDTisSignal","BDToutSig"]:
          pvalue = round(h_data_cut.Chi2TestX(h_tot_cut,chi2,ndf,output,"UW"),4)
        elif name == "H_mass":
          pvalue = round(h_data_cut.Chi2TestX(h_tot_cut,chi2,ndf,output,"UW"),4)
        else:
          pvalue = round(h_data.Chi2TestX(h_tot,chi2,ndf,output,"UW"),4)
        chi2test = "p-value:%.4f chi2/ndf=%.1f/%.0f"%(pvalue,chi2.value,ndf.value)
    

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
    latex.DrawLatex(0.20, 0.24, chi2test)
    #plot.DrawTitle(pads[0], args.title, 1)
    
    # ... and we're done
    for fmt in cfg["formats"]:
        canv.Print(outdir + '/' + name + '.%s' %fmt)
  

parser = argparse.ArgumentParser()
parser.add_argument('-y', '--year',    dest='year', type=str, default='2018', action='store')
parser.add_argument('-c', '--channel', dest='channel', type=str, default='mutau', action='store')
parser.add_argument('--output', '-o', default='./plots', help='top level output directory')
args = parser.parse_args()
year = args.year
channel = args.channel
preVFP = ""
if year=="2016":
  preVFP="_comb"
filename = "%s_UL%s%s_finebinning_BDT.root"%(channel,year,preVFP)
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
output = './plots/%s/'%filename[:-5]
node = TDirToNode(file)

made_dirs = set()


titleright = "%s %.1f fb^{-1} (13 TeV)"%(year,float(lumi))
#titleright = "%s %.1f fb^{-1} (13 TeV)"%("2018",float(lumi)) #for PR plot

plotcfg = {
  "x_title" : "test",
  "hide_data" : False,
  "logy" : False,
  "formats" : ["pdf","png"],
  "ratio_range" : [0.5,1.5],#[0.5,1.5]
  "title_right" : titleright,
  "do_overlay" : True
}

config_by_setting = {
  "x_title": [
    ('Mu1_pt', ('#mu p_{T}', 'GeV')),
    ('Mu1_eta', ('#mu #eta', '')),
    ('Mu1_phi', ('#mu #phi', '')),
    ('Mu1_mass', ('#mu mass', 'GeV')),
    ('Ele1_pt', ('e p_{T}', 'GeV')),
    ('Ele1_eta', ('e #eta', '')),
    ('Ele1_phi', ('e #phi', '')),
    ('Ele1_mass', ('e mass', 'GeV')),
    ('Tau1_pt', ('#tau p_{T}', 'GeV')),
    ('Tau1_eta', ('#tau #eta', '')),
    ('Tau1_phi', ('#tau #phi', '')),
    ('Tau1_mass', ('#tau mass', 'GeV')),
    ('Tau1_decaymode', ('#tau decaymode', '')),
    ('Tau1_Idvsjet', ('#tau Id vs jet', '')),
    ('Tau1_Idvsmu', ('#tau Id vs #mu', '')),
    ('Tau1_Idvse', ('#tau Id vs e', '')),
    ('vistau1_pt', ('lep p_{T}', 'GeV')),
    ('vistau1_eta', ('lep #eta', '')),
    ('vistau1_phi', ('lep #phi', '')),
    ('vistau1_mass', ('lep mass', 'GeV')),
    ('Jet1_pt', ('leading Jet p_{T}', 'GeV')),
    ('Jet1_eta', ('leading Jet #eta', '')),
    ('Jet1_phi', ('leading Jet #phi', '')),
    ('Jet1_mass', ('leading Jet mass', 'GeV')),
    ('Jet1_btag', ('Largest btag score', '')),
    ('Jet2_pt', ('subleading Jet p_{T}', 'GeV')),
    ('Jet2_btag', ('Second largest btag score', '')),
    ('Jet3_pt', ('jet3 p_{T}', 'GeV')),
    ('Bjet1_pt', ('leading b Jet p_{T}', 'GeV')),
    ('Bjet1_eta', ('leading b Jet #eta', '')),
    ('Bjet1_phi', ('leading b Jet #phi', '')),
    ('Bjet1_mass', ('leading b Jet mass', 'GeV')),
    ('Bjet2_pt', ('subleading b Jet p_{T}', 'GeV')),
    ('Bjet2_eta', ('subleading b Jet #eta', '')),
    ('Bjet2_phi', ('subleading b Jet #phi', '')),
    ('Bjet2_mass', ('subleading b Jet mass', 'GeV')),
    ('vis_pt', ('p_{T}^{#tau#tau}_{vis}', 'GeV')),
    ('vis_eta', ('#eta^{#tau#tau}_{vis}', '')),
    ('vis_phi', ('#phi^{#tau#tau}_{vis}', '')),
    ('vis_mass', ('m^{#tau#tau}_{vis}', 'GeV')),
    ('H_pt', ('H p_{T}', 'GeV')),
    ('H_eta', ('H #eta', '')),
    ('H_phi', ('H #phi', '')),
    ('H_mass', ('H mass', 'GeV')),
    ('NNoutput', ('H mass', 'GeV')),
    ('MET', ('MET', 'GeV')),
    #('MET_phi', ('MET #phi', '')),
    ('MET_chs', ('MET CHS', 'GeV')),
    ('MET_covXX', ('MET covXX', 'GeV')),
    ('MET_covXY', ('MET covXY', 'GeV')),
    ('MET_covYY', ('MET covYY', 'GeV')),
    ('nMuons', ('nMuons', '')),
    ('nElectrons', ('nElectrons', '')),
    ('nTaus', ('nTaus', '')),
    ('nJets', ('nJets', '')),
    ('nJets_forward', ('Number of forward jets', '')),
    ('nBjets_l', ('Number of loose b-tagged jets', '')),
    ('nBjets_m', ('Number of medium b-tagged jets', '')),
    ('nBjets_t', ('Number of tight b-tagged jets', '')),
    ('nGenBjets', ('Number of gen b-tagged jets', '')),
    ('LHE_Nb', ('LHE_Nb', '')),
    ('LHE_NpNLO', ('LHE_NpNLO', '')),
    ('DPhi', ('#Delta#phi(#tau,lep)', '')),
    ('DEta', ('#Delta#eta(#tau,lep)', '')),
    ('DPhiLepMET', ('#Delta#phi(lep,MET)', '')),
    ('DRLepMET', ('#DeltaR(lep,MET)', '')),
    ('met_var_qcd', ('met_var_qcd', '')),
    ('met_var_w', ('met_var_w', '')),
    ('wpt', ('wpt', '')),
    ('DRLepJ', ('#DeltaR(Lep,jet1)', '')),
    ('DEtaLepJ', ('#Delta#eta(Lep,jet1)', '')),
    ('DPhiLepJ', ('#Delta#phi(Lep,jet1)', '')),
    ('DRTauJ', ('#DeltaR(#tau,jet1)', '')),
    ('DEtaTauJ', ('#Delta#eta(#tau,jet1)', '')),
    ('DPhiTauJ', ('#Delta#phi(#tau,jet1)', '')),
    ('DRLepJ2', ('#DeltaR(lep,jet2)', '')),
    ('DEtaLepJ2', ('#Delta#eta(lep,jet2)', '')),
    ('DPhiLepJ2', ('#Delta#phi(lep,jet2)', '')),
    ('DRTauJ2', ('#DeltaR(#tau,jet2)', '')),
    ('DEtaTauJ2', ('#Delta#eta(#tau,jet2)', '')),
    ('DPhiTauJ2', ('#Delta#phi(#tau,jet2)', '')),
    ('DRBjets', ('DRBjets', '')),
    ('DEta_Bjets', ('DEta Bjets', '')),
    ('DPhi_Bjets', ('DPhi Bjets', '')),
    ('DRBjets_lm', ('DRBjets_lm', '')),
    ('Bjets_pt', ('Bjets p_{T}', 'GeV')),
    ('HJ_mass', ('Higgs+jet1 mass', 'GeV')),
    ('LepJ_mass', ('lep+jet1 mass', 'GeV')),
    ('TauJ_mass', ('#tau+jet1 mass', 'GeV')),
    ('vistauJ_mass', ('#tau+lep+jet1 mass', 'GeV')),
    ('vistauJMET_mass', ('#tau+lep+jet1+MET mass', 'GeV')),
    ('TauJMET_mass', ('#tau+jet1+MET mass', 'GeV')),
    ('METJ_mass', ('jet1+MET mass', 'GeV')),
    ('Dzeta', ('#Delta#zeta', '')),
    ('mt2', ('mt2', 'GeV')),
    ('wt_ff', ('ff', '')),
    ('wt_ff_ttdr', ('ff TT DR', '')),
    ('wt_ff_old', ('ff old method', '')),
    ('BDTisSignal', ('BDT p_{S}','')),
    ('BDToutput', ('BDT p_{comb}','')),
    ('BDTisTT', ('BDT p_{TT}','')),
    ('BDTisDY', ('BDT p_{DY}','')),
    ('BDTisBkg', ('BDT p_{Bkg}','')),
    ('BDTisfake', ('BDT p_{fake}','')),
    ('BDTisjjH', ('BDT p_{jjH}','')),
    ('BDToutSig', ('max BDT p_{S}','')),
    ('BDToutTT', ('max BDT p_{TT}','')),
    ('BDToutDY', ('max BDT p_{DY}','')),
    ('BDToutBkg', ('max BDT p_{Bkg}','')),
    ('BDTCR', ('BDT CR','')),
    ('transverse_mass_lepmet', ('m_{T}', 'GeV')),
    ('mt', ('m_{T}', 'GeV')),
    ('transverse_mass_taumet', ('m_{T}(#tau,MET)','GeV')),
    ('transverse_mass_leptau', ('m_{T}(#ell,#tau)','GeV')),
    ('transverse_mass_total', ('m_{T}^{tot}','GeV')),
    ('DRjets', ('DRjets','')),
    ('DEta_jets', ('DEta jets','')),
    ('DEta_jets_forward', ('DEta jets forward','')),
    ('DPhi_jets', ('DPhi jets','')),
    ('dijet_pt', ('dijet p_{T}','GeV')),
    ('dijet_eta', ('dijet #eta','')),
    ('dijet_phi', ('dijet #phi','')),
    ('dijet_mass', ('dijet mass','GeV')),
    ('LepJ_pt', ('LepJ p_{T}','GeV')),
    ('TauJ_pt', ('TauJ p_{T}','GeV')),
    ('vistauJ_pt', ('#tau+lep+jet1 p_{T}','GeV')),
    ('vistauJMET_pt', ('#tau+lep+jet1+MET p_{T}','GeV')),
    ('TauJMET_pt', ('#tau+jet1+MET p_{T}','GeV')),
    ('LepJMET_pt', ('+lep+jet1+MET p_{T}','GeV')),
    ('METJ_pt', ('jet1+MET p_{T}','GeV')),
    ('vistauMET_pt',('#tau+lep+MET p_{T}','GeV')),
    ('HJ_pt', ('Higgs+jet1 p_{T}','GeV')),
    ('DRHJ', ('#DeltaR(Higgs,jet1)','')),
    ('DRHJ2', ('#DeltaR(Higgs,jet2)','')),
    ('collinear_mass', ('collinear mass','GeV')),
    ('BTagWeight', ('BTagWeight','')),
    
    ],
      
    "hide_data": [('H_mass', True),('vis_mass', False),('BDToutput', False),('BDTisSignal', False),('BDTisTT', False),('BDTisDY', False),('BDTisfake', False),('BDToutSig',True),('BDToutTT',False),('BDToutDY',False),('BDTisBkg', False), ('BDToutBkg', False),('MET', False)],
    "logy":[('BDToutput', True),('BDTisSignal', True),('BDTisTT', True),('BDTisDY', True),('BDTisfake', True),('BDToutSig', True),('BDToutTT', True),('BDToutDY', True),('BDTCR', True),('BDTisBkg', True),('BDToutBkg', True),('H_mass', False)],
    "logy_min":[('BDToutput', 1),('BDTisSignal', 1),('BDTisTT', 1),('BDTisDY', 1),('BDTisfake', 1),('BDToutSig', 10),('BDToutTT', 100),('BDToutDY', 100),('BDTCR', 1),('BDTisBkg', 1), ('BDToutBkg', 1)],
    }
    # "ratio_range" :[
    #     ('vis_mass', [0,5])]}

for path, subnode in node.ListNodes(withObjects=True):
  print(path)
  if ("Ele" in path and channel=="mutau") or ("Mu" in path and channel=="etau"):
    continue
  if path!="BDToutSig": continue
  if "2D" in path:
    print("skip 2D histograms")
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
  MakeStackedPlot(name, target_dir, hists, plotcfg)
