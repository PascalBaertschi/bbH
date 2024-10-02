import plotting as plot
from analysis import *
import ROOT
from ROOT import TColor, TLatex
import argparse
import json
import os
import fnmatch
from copy import deepcopy
from array import array

ROOT.TH1.SetDefaultSumw2(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)
plot.ModTDRStyle()

def processComp(leg,plots,colour,norm=1.):
  return dict([('leg_text',leg),('plot_list',plots),('colour',colour),('norm',norm)])

def MakeStackedPlot(name, outdir, hists,selection, cfg):
    if selection=="mumu":
      #bkgscheme =  [processComp("WJets",["WJets_incl","WJets_0J","WJets_1J","WJets_2J"],TColor.GetColor(222,90,106)),processComp("TT",["TT"],TColor.GetColor(155, 152, 204)),processComp("DYJets",["DYJets_incl","DYJets_0J","DYJets_1J","DYJets_2J"],TColor.GetColor(248, 206, 104)),processComp("ST",["ST_t_channel_antitop","ST_t_channel_top","ST_s_channel","ST_tW_antitop","ST_tW_top"],TColor.GetColor(208,240,193)),processComp("VV",["WWTo2L2Nu","WWTo1L1Nu2Q","WWTo4Q","WZTo3LNu","WZTo2L2Q","WZTo1L3Nu","WZTo1L1Nu2Q","ZZTo4L","ZZTo2L2Q","ZZTo2Nu2Q"],TColor.GetColor(111,45,53))]
      #bkgscheme =  [processComp("DYJets stitched",["DYJets"],plot.CreateTransparentColor(TColor.GetColor(187,5,30), 0.5)),processComp("DYJets incl",["DYJets_incl_nostitch"],plot.CreateTransparentColor(TColor.GetColor(0,153,76), 0.5))]
      bkgscheme =  [processComp("DYJets 1b",["DYJets_incl_1btag","DYJets_0J_1btag","DYJets_1J_1btag","DYJets_2J_1btag"],plot.CreateTransparentColor(TColor.GetColor(187,5,30), 0.3)),processComp("DYJets 2b",["DYJets_incl_2btag","DYJets_0J_2btag","DYJets_1J_2btag","DYJets_2J_2btag"],plot.CreateTransparentColor(TColor.GetColor(0,153,76), 0.3))]
    elif selection=="tt":
      bkgscheme = [processComp("TT",["TT"],TColor.GetColor(155, 152, 204)),processComp("WJets",["WJets_incl","WJets_0J","WJets_1J","WJets_2J"],TColor.GetColor(222,90,106)),processComp("DYJets",["DYJets_incl","DYJets_0J","DYJets_1J","DYJets_2J"],TColor.GetColor(248, 206, 104)),processComp("ST",["ST_t_channel_antitop","ST_t_channel_top","ST_s_channel","ST_tW_antitop","ST_tW_top"],TColor.GetColor(208,240,193)),processComp("VV",["WWTo2L2Nu","WWTo1L1Nu2Q","WWTo4Q","WZTo3LNu","WZTo2L2Q","WZTo1L3Nu","WZTo1L1Nu2Q","ZZTo4L","ZZTo2L2Q","ZZTo2Nu2Q"],TColor.GetColor(111,45,53))]
    elif selection=="singlelep":
      bkgscheme =  [processComp("WJets NLO incl",["WJets_NLO_incl"], plot.CreateTransparentColor(632, 0.7)),processComp("WJets NLO",["WJets_incl","WJets_0J","WJets_1J","WJets_2J"], plot.CreateTransparentColor(856, 0.7))]
    elif selection=="mutau" or channel=="etau":
      #bkgscheme =  [processComp("WJets",["WJets_incl","WJets_0J","WJets_1J","WJets_2J"],TColor.GetColor(222,90,106)),processComp("TT",["TT"],TColor.GetColor(155, 152, 204)),processComp("DYJets",["DYJets_incl","DYJets_0J","DYJets_1J","DYJets_2J"],TColor.GetColor(248, 206, 104)),processComp("ST",["ST_t_channel_antitop","ST_t_channel_top","ST_s_channel","ST_tW_antitop","ST_tW_top"],TColor.GetColor(208,240,193)),processComp("VV",["WWTo2L2Nu","WWTo1L1Nu2Q","WWTo4Q","WZTo3LNu","WZTo2L2Q","WZTo1L3Nu","WZTo1L1Nu2Q","ZZTo4L","ZZTo2L2Q","ZZTo2Nu2Q"],TColor.GetColor(111,45,53))]
      #bkgscheme =  [processComp("WJets stitched",["WJets"],plot.CreateTransparentColor(TColor.GetColor(187,5,30), 0.5)),processComp("WJets incl",["WJets_incl_nostitch"],plot.CreateTransparentColor(TColor.GetColor(0,153,76), 0.5))]
      bkgscheme =  [processComp("TT no btag SF",["TTTo2L2Nu_nobtagSF"],plot.CreateTransparentColor(TColor.GetColor(187,5,30), 0.4)),processComp("TT btag SF",["TTTo2L2Nu_btagSF"],plot.CreateTransparentColor(TColor.GetColor(0,153,76), 0.4))]
    copyhists = {}
    for hname, h in hists.items():
        copyhists[hname] = h.Clone()
    
    
    hists = copyhists

    # Canvas and pads
    canv = ROOT.TCanvas(name, name)
  
    pads = plot.TwoPadSplit(0.29,0.01,0.01)
    h_data = hists['TTTo2L2Nu_nobtagSF']
    hist_nobtagSF = hists['TTTo2L2Nu_nobtagSF']
    hist_btagSF = hists['TTTo2L2Nu_btagSF']
    
    h_axes = [h_data.Clone() for x in pads]
    #for h in h_axes:
    #    h.SetTitle("")
    #    h.Reset()

    build_h_tot = True
    h_tot = None
    h_LO = None
    h_NLO = None

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

    pads[0].SetLogy()
    h_axes[0].SetMinimum(50.)

    plot.StandardAxes(h_axes[1].GetXaxis(), h_axes[0].GetYaxis(), x_title, units)
    h_axes[0].GetXaxis().SetLabelSize(0)
    h_axes[0].Draw("AXIS")

    # A dict to keep track of the hists
    h_store = {}
    p_store = {}

    legend = ROOT.TLegend(*([0.6, 0.75, 0.90, 0.91, '', 'NBNDC']))
    legend.SetNColumns(2)
    stack = ROOT.THStack()

    curr_auto_colour = 0
    all_input_hists = []

    for entry in bkgscheme:
        all_input_hists.append(entry['plot_list'])
        hist = hists[entry['plot_list'][0]]
        #if cfg['type'] == 'multihist':
        #    plot.Set(hist, FillColor=col, MarkerColor=col, LineColor=col, Title=info['legend'], MarkerSize=info['marker_size'], LineWidth=info['line_width'], LineStyle=info['line_style'])
        plot.Set(hist, FillColor=entry['colour'], MarkerColor=entry['colour'], Title=entry['leg_text'])
        if len(entry['plot_list']) > 1:
            for addhist in entry['plot_list'][1:]:
                hist.Add(hists[addhist])
        #if hist.Integral()!=0:
        #  hist.Scale(1./hist.Integral()) #normalize to data
        h_store[entry['plot_list'][0]] = hist
        p_store[entry['plot_list'][0]] = hist.Clone()
        print("entry:",entry['plot_list'][0])
        #if entry['plot_list'][0]=="DYJets_incl_nostitch" or entry['plot_list'][0]=="WJets_incl_nostitch":
        #  h_incl = hist.Clone()
        #elif entry['plot_list'][0]=="DYJets" or entry['plot_list'][0]=="WJets":
        #  h_stitch = hist.Clone()
        if build_h_tot:
            if h_tot is None:
                h_tot = hist.Clone()
            else:
                h_tot.Add(hist)
        #if "incl" in entry["leg_text"]:
        #  h_NLO = hist.Clone()
        #else:
        #  h_LO = hist.Clone()        
        
        #if "NLO" in entry["leg_text"]:
        #  h_NLO = hist.Clone()
        #else:
        #  h_LO = hist.Clone()
        stack.Add(hist)

    # h_tot_purity = h_tot.Clone()

    #if not cfg['hide_data']:
    #    legend.AddEntry(h_data, 'Observed', 'PL')

      
    for ele in reversed(bkgscheme):
        legend.AddEntry(h_store[ele['plot_list'][0]], ele['leg_text'], "F")

    #legend.AddEntry(h_tot, 'Stat. Uncertainty', 'F')

    
    #stack.Draw('HISTSAME')  
    stack.Draw('nostackHISTSAME')
    #h_tot.Draw("E2SAME")   


    #if not cfg['hide_data']:
    #    h_data.Draw('E0SAME')
   
    
    if name=="LHE_Vpt":
      plot.FixTopRange(pads[0], 80000., 0.35)
    else:
      plot.FixTopRange(pads[0], plot.GetPadYMax(pads[0]), 0.35)
      
    legend.Draw()
    # if cfg['legend_padding'] > 0.:
    #     plot.FixBoxPadding(pads[0], legend, cfg['legend_padding'])
    """
    # Do the ratio plot
    r_store = {}
    r_data = None
    r_tot = None
    r_ext_tot = None
    pads[1].cd()
    pads[1].SetGrid(0, 1)
    if len(cfg['ratio_range']):
            h_axes[1].GetYaxis().SetRangeUser(*cfg['ratio_range'])
    #h_axes[1].GetYaxis().SetTitle("stitched/incl")
    #h_axes[1].GetYaxis().SetTitle("data/MC")
    h_axes[1].Draw()
    
    if channel!="mutau" and channel!="etau":
      r_stitch = plot.MakeRatioHist(h_stitch, h_incl, True, True)
      r_stitch.SetMarkerColor(1)
      r_stitch.SetFillColor(plot.CreateTransparentColor(1, 0.4))
      r_stitch.Draw('E2SAME')
      
      if name!="LHE_Vpt":
        r_data_LO = plot.MakeRatioHist(h_data, h_LO, True, False)
        r_data_NLO = plot.MakeRatioHist(h_data, h_NLO, True, False)
        r_data_LO.SetMarkerColor(632)
        r_data_LO.SetFillColor(plot.CreateTransparentColor(632, 0.4))
        r_data_NLO.SetMarkerColor(856)
        r_data_NLO.SetFillColor(plot.CreateTransparentColor(856, 0.4))
        r_data_LO.Draw('E2SAME')
        r_data_NLO.Draw('E2SAME')
      else:
        r_data = plot.MakeRatioHist(h_LO, h_NLO, True, False)
        r_data.SetMarkerColor(1)
        r_data.Draw('SAME')
    """
    #### comment here for signal only plot ####
    pads[1].cd()
    pads[1].SetGrid(0,1)
    h_axes[1].GetYaxis().SetRangeUser(0.9,1.1)
    h_axes[1].GetYaxis().SetTitle("no/with b-tag SF")
    h_axes[1].Draw()
    ratio = plot.MakeRatioHist(hist_nobtagSF, hist_btagSF, True, False)
    ratio.SetMarkerColor(1)
    ratio.Draw('SAME')
    ratio_norm = hist_nobtagSF.Integral()/hist_btagSF.Integral() 
    #### end comment here ####
    
    # Go back and tidy up the axes and frame
    pads[0].cd()
    pads[0].GetFrame().Draw()
    pads[0].RedrawAxis()


    # CMS logo
    #plot.DrawCMSLogo(pads[0], "CMS", "Internal", 10, 0.045, 0.05, 1.0, '', 1.0)
    plot.DrawCMSLogo(pads[0], "Private work", "(CMS data/simulation)", 10, 0.045, 0.05, 1.0, '', 1.0)
    plot.DrawTitle(pads[0], cfg["title_right"], 3)

    latex = ROOT.TLatex()
    plot.Set(latex, NDC=None, TextFont=42, TextSize=0.03)
    
    if "1btag" in name:
      latex.DrawLatex(0.20, 0.77, channel_text+", 1 b-jet")
    elif "2btag" in name:
      latex.DrawLatex(0.20, 0.77, channel_text+", 2 b-jets")
    else:
      latex.DrawLatex(0.20, 0.77, channel_text)
    latex.DrawLatex(0.20, 0.24, "norm ratio: %s"%round(ratio_norm,5))  
    #latex.DrawLatex(0.20, 0.75, selection)
    #latex.DrawLatex(0.20, 0.75, channel)
    #latex.DrawLatex(0.20, 0.65, channel)
    # plot.DrawTitle(pads[0], args.title, 1)

    # ... and we're done
    for fmt in cfg["formats"]:
        canv.Print(outdir + '/' + name + '.%s' %fmt)
  

parser = argparse.ArgumentParser()
parser.add_argument('--input', '-i', help='File with histograms to plot')
parser.add_argument('--output', '-o', default='./plots', help='top level output directory')
args = parser.parse_args()

filename = args.input
year = filename.split("_")[1].split(".")[0]
channel=filename.split("_")[0]
if channel == "mutau":
  channel_text = "#mu#tau_{h}"
elif channel == "etau":
  channel_text = "e#tau_{h}"
elif channel == "mumu":
  channel_text = "#mu#mu"
elif channel == "tt":
  channel_text = "tt"

if year=="UL2018":
  lumi = 59.7
elif year=="UL2017":
  lumi = 41.5
else:
  lumi = 35.9

file = ROOT.TFile("root/"+filename)
output = './plots/btagSFcorr/'
node = TDirToNode(file)

made_dirs = set()


for path, subnode in node.ListNodes(withObjects=True):
    print(path)
    #if path not in ["vis_pt","vis_mass"]: continue
    if path!="Jet1_pt": continue
    #if path in ["LHE_Vpt"]: continue
    #if not fnmatch.fnmatch(path, dirfilter):
    #    continue
    # for now work on the assumption that the last component of the path will be the actual filename
    split_path = path.split('/')[:-1]
    name = path.split('/')[-1]
    target_dir = os.path.join(output, *split_path)
    if target_dir not in made_dirs:
        os.system('mkdir -p %s' % target_dir)
        made_dirs.add(target_dir)
    hists = {}
    for opath, objname, obj in subnode.ListObjects(depth=0):
        hists[objname] = obj

 
    titleright = "%s %.1f fb^{-1} (13 TeV)"%(year[2:],float(lumi))

    plotcfg = {
     "x_title" : "test",
     "hide_data" : False,
     "logy" : False,
      "formats" : ["pdf","png"],
      "ratio_range" : [0.5,1.2],
      #"ratio_range" : [0.8, 1.2],
     "title_right" : titleright,
     "do_overlay" : True
    }

    config_by_setting = {
    "x_title": [
      ('Mu1_pt', ('leading #mu p_{T}', 'GeV')),
      ('Mu1_eta', ('leading #mu #eta', '')),
      ('Mu1_phi', ('leading #mu #phi', '')),
      ('Mu1_mass', ('leading #mu mass', 'GeV')),
      ('Mu1_pt_1btag', ('leading #mu p_{T}', 'GeV')),
      ('Mu1_eta_1btag', ('leading #mu #eta', '')),
      ('Mu1_pt_2btag', ('leading #mu p_{T}', 'GeV')),
      ('Mu1_eta_2btag', ('leading #mu #eta', '')),
      ('Mu2_pt_1btag', ('subleading #mu p_{T}', 'GeV')),
      ('Mu2_eta_1btag', ('subleading #mu #eta', '')),
      ('Mu2_pt_2btag', ('subleading #mu p_{T}', 'GeV')),
      ('Mu2_eta_2btag', ('subleading #mu #eta', '')),
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
      ('vis_pt', ('dilepton p_{T}', 'GeV')),
      ('vis_pt_1btag', ('dilepton p_{T}', 'GeV')),
      ('vis_pt_2btag', ('dilepton p_{T}', 'GeV')),
      ('vis_eta', ('#eta^{#tau#tau}_{vis}', '')),
      ('vis_phi', ('#phi^{#tau#tau}_{vis}', '')),
      ('vis_mass', ('m^{#tau#tau}_{vis}', 'GeV')),
      #('vis_mass', ('m_{#mu#mu}', 'GeV')),
      ('vis_mass_1btag', ('m_{#mu#mu}', 'GeV')),
      ('vis_mass_2btag', ('m_{#mu#mu}', 'GeV')),
      ('H_pt', ('H p_{T}', 'GeV')),
      ('H_eta', ('H #eta', '')),
      ('H_phi', ('H #phi', '')),
      ('H_mass', ('H mass', 'GeV')),
      ('NNoutput', ('H mass', 'GeV')),
      ('MET', ('MET', 'GeV')),
      #('MET_phi', ('MET #phi', '')),
      ('MET_chs', ('MET CHS', 'GeV')),
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
      ('LHE_Vpt', ('LHE V p_{T}', 'GeV')),
      ('METJ_pt', ('jet1+MET p_{T}','GeV')),
      ('vistauMET_pt',('#tau+lep+MET p_{T}','GeV')),
      ('HJ_pt', ('Higgs+jet1 p_{T}','GeV')),
      ('DRHJ', ('#DeltaR(Higgs,jet1)','')),
      ('DRHJ2', ('#DeltaR(Higgs,jet2)','')),
      ('collinear_mass', ('collinear mass','GeV')),
],
      
      "hide_data": [('H_mass', True),('LHE_Vpt', True)],
      #"logy":[('LHE_Vpt', True)],
      #"logy_min":[('LHE_Vpt', 3000.)],
      #"logy":[('vis_mass', True),('vis_pt',True)],
      #"logy_min":[('vis_mass', 30),('vis_pt',30)],
      #"logy":[('BDToutput', True),('BDTisSignal', True),('BDTisTT', True),('BDTisDY', True)],
      #"logy_min":[('BDToutput', 30),('BDTisSignal', 30),('BDTisTT', 30),('BDTisDY', 30)],
    }
    # "ratio_range" :[
    #     ('vis_mass', [0,5])]}

    name = name+"_btagSFcorr_"+channel+"_"+year
    for setting, vardict in config_by_setting.items():
        for pathkey, val in vardict:
            if fnmatch.fnmatch(path, pathkey):
                plotcfg[setting] = val
                print('Path %s, setting %s, to value %s' % (path, setting, val))
    MakeStackedPlot(name, target_dir, hists,channel, plotcfg)
