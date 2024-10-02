import plotting as plot
from analysis import *
import ROOT
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
    #bkgscheme =  [processComp("WJets",["WJetscomb_%s"%selection],ROOT.TColor.GetColor(222,90,106)),processComp("DYJets",["DYJetscomb_%s"%selection],ROOT.TColor.GetColor(248, 206, 104)),processComp("TT",["TT_%s"%selection],ROOT.TColor.GetColor(155, 152, 204)),processComp("ST",["ST_%s"%selection],ROOT.TColor.GetColor(208,240,193)),processComp("VV",["VV_%s"%selection],ROOT.TColor.GetColor(111,45,53))]
    if "TT" in selection:
      bkgscheme =  [processComp("W+jets",["WJetscomb_%s"%selection],ROOT.TColor.GetColor("#e42536")),processComp("Z+jets",["DYJetscomb_%s"%selection],ROOT.TColor.GetColor("#f89c20")),processComp("t#bar{t} fake #tau",["TT_%s_fakes"%selection],ROOT.TColor.GetColor("#964a8b")),processComp("ST",["ST_%s"%selection],ROOT.TColor.GetColor("#832db6")),processComp("VV",["VV_%s"%selection],ROOT.TColor.GetColor("#b9ac70")),processComp("t#bar{t} true #tau",["TT_%s_true"%selection],ROOT.TColor.GetColor("#92dadd"))]
      #bkgscheme =  [processComp("WJets",["WJetscomb_%s"%selection],ROOT.TColor.GetColor(222,90,106)),processComp("DYJets",["DYJetscomb_%s"%selection],ROOT.TColor.GetColor(248, 206, 104)),processComp("TT fake #tau",["TT_%s_fakes"%selection],ROOT.TColor.GetColor(155, 152, 204)),processComp("ST",["ST_%s"%selection],ROOT.TColor.GetColor(208,240,193)),processComp("VV",["VV_%s"%selection],ROOT.TColor.GetColor(111,45,53)),processComp("TT genuine #tau",["TT_%s_true"%selection],430)]
    else:
      bkgscheme =  [processComp("W+jets",["WJetscomb_%s"%selection],ROOT.TColor.GetColor("#e42536")),processComp("Z+jets",["DYJetscomb_%s"%selection],ROOT.TColor.GetColor("#f89c20")),processComp("t#bar{t}",["TT_%s"%selection],ROOT.TColor.GetColor("#964a8b")), processComp("ST",["ST_%s"%selection],ROOT.TColor.GetColor("#832db6")),processComp("VV",["VV_%s"%selection],ROOT.TColor.GetColor("#b9ac70"))]
      #bkgscheme =  [processComp("WJets",["WJetscomb_%s"%selection],ROOT.TColor.GetColor(222,90,106)),processComp("DYJets",["DYJetscomb_%s"%selection],ROOT.TColor.GetColor(248, 206, 104)),processComp("TT",["TT_%s"%selection],ROOT.TColor.GetColor(155, 152, 204)), processComp("ST",["ST_%s"%selection],ROOT.TColor.GetColor(208,240,193)),processComp("VV",["VV_%s"%selection],ROOT.TColor.GetColor(111,45,53))]
    copyhists = {}
    for hname, h in hists.items():
        copyhists[hname] = h.Clone()
    
    
    hists = copyhists

    # Canvas and pads
    canv = ROOT.TCanvas(name, name)
    pads = plot.TwoPadSplit(0.29,0.01,0.01)

    h_data = hists['data_obs_%s'%selection]


    h_axes = [h_data.Clone() for x in pads]
    for h in h_axes:
        h.SetTitle("")
        h.Reset()

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

    plot.StandardAxes(h_axes[1].GetXaxis(), h_axes[0].GetYaxis(), x_title, units)
    h_axes[0].GetXaxis().SetLabelSize(0)
    h_axes[0].Draw()

    # A dict to keep track of the hists
    h_store = {}
    p_store = {}

    legend = ROOT.TLegend(*([0.55, 0.75, 0.95, 0.93, '', 'NBNDC']))
    legend.SetNColumns(2)
    stack = ROOT.THStack()

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
        if build_h_tot:
            if h_tot is None:
                h_tot = hist.Clone()
            else:
                h_tot.Add(hist)
        stack.Add(hist)

    # h_tot_purity = h_tot.Clone()
    h_tot.SetFillColor(plot.CreateTransparentColor(12, 0.3))
    h_tot.SetMarkerSize(0)
    if not cfg['hide_data']:
        legend.AddEntry(h_data, 'Observed', 'PL')

      
    for ele in reversed(bkgscheme):
        legend.AddEntry(h_store[ele['plot_list'][0]], ele['leg_text'], "F")

    legend.AddEntry(h_tot, 'Stat. Uncertainty', 'F')

    
    stack.Draw('HISTSAME')
    h_tot.Draw("E2SAME")


    if not cfg['hide_data']:
        h_data.Draw('E0SAME')
    #### end comment here ####
    """
    ### only bkg plot #####
    # Build overlays
    if cfg['do_overlay']:
        for entry in signal:
            hist = hists[entry['plot_list'][0]].Clone()
            if len(entry['plot_list'])>1:
                for addhist in entry['plot_list'][1:]:
                    hist.Add(hists[addhist])
            plot.Set(hist,LineColor=entry['colour'],LineWidth=2,MarkerSize=0,FillStyle=0,Title=entry['leg_text'])
            for ib in xrange(1, hist.GetNbinsX() + 1):
                hist.SetBinError(ib, 1E-7)
            h_store[entry['plot_list'][0]] = hist
            hist.Scale(entry['norm'])
            #if hist.Integral()!=0:
            #  hist.Scale(1./hist.Integral())
            hist.Draw("HISTSAME")

        for ele in signal:
            legend.AddEntry(h_store[ele['plot_list'][0]], ele['leg_text'] if entry['norm']==1 else ele['leg_text']+' x '+ str(entry['norm']), "L")
    ###### end comment here #####        
    """
    plot.FixTopRange(pads[0], plot.GetPadYMax(pads[0]), 0.35)
    legend.Draw()
    # if cfg['legend_padding'] > 0.:
    #     plot.FixBoxPadding(pads[0], legend, cfg['legend_padding'])

    # Do the ratio plot
    r_store = {}
    r_data = None
    r_tot = None
    r_ext_tot = None
    pads[1].cd()
    pads[1].SetGrid(0, 1)
    if len(cfg['ratio_range']):
            h_axes[1].GetYaxis().SetRangeUser(*cfg['ratio_range'])
    h_axes[1].GetYaxis().SetTitle("Obs/Exp")
    h_axes[1].Draw()
    
    #### comment here for signal only plot ####
    if not cfg['hide_data']:
        r_data = plot.MakeRatioHist(h_data, h_tot, True, False)
    r_tot = plot.MakeRatioHist(h_tot, h_tot, True, False)
    r_tot.Draw('E2SAME')
    if not cfg['hide_data']:
        r_data.Draw('SAME')
    #### end comment here ####
    
    # Go back and tidy up the axes and frame
    pads[0].cd()
    pads[0].GetFrame().Draw()
    pads[0].RedrawAxis()


    # CMS logo
    #plot.DrawCMSLogo(pads[0], "CMS", "Internal", 10, 0.045, 0.05, 1.0, '', 1.0)
    plot.DrawCMSLogo(pads[0], "Private work", "(CMS data/simulation)", 10, 0.045, 0.05, 1.0, '', 0.8)
    plot.DrawTitle(pads[0], cfg["title_right"], 3)

    latex = ROOT.TLatex()
    plot.Set(latex, NDC=None, TextFont=42, TextSize=0.03)
    #latex.DrawLatex(0.20, 0.75, selection)
    if channel == "mutau":
        channel_text = "#mu#tau_{h}"
    elif channel == "etau":
      channel_text = "e#tau_{h}"
    if "1prong" in selection:
      prong = "1prong"
    elif "3prong" in selection:
      prong = "3prong"
    if "_AR_" in selection:
      region = "anti-iso"
    else:
      region = "iso"
    if "DR_TT" in selection:
      DRregion = "t#bar{t} DR"
    elif "DR_W" in selection:
      DRregion = "W+jets DR"
    elif "DR_QCD" in selection:
      DRregion = "QCD DR"
      
    latex.DrawLatex(0.20, 0.78, "%s, %s"%(channel_text,prong))
    latex.DrawLatex(0.20, 0.73, "%s, %s"%(DRregion,region))
    # plot.DrawTitle(pads[0], args.title, 1)

    # ... and we're done
    split_outdir=outdir.split("/")
    canv.Print(split_outdir[0]+"/"+split_outdir[1]+'/thesis/ff_'+ selection + '_%s.pdf' %split_outdir[2])
    for fmt in cfg["formats"]:
        canv.Print(outdir + '/' +name +"_"+ selection + '.%s' %fmt)

parser = argparse.ArgumentParser()
parser.add_argument('--input', '-i', help='File with histograms to plot')
parser.add_argument('--output', '-o', default='./plots', help='top level output directory')
args = parser.parse_args()

filename = args.input
year = filename.split("_")[2].split(".")[0]
channel=filename.split("_")[1]
if year=="UL2018":
  lumi = 59.7
elif year=="UL2017":
  lumi = 41.5
else:
  lumi = 36.3

preVFP = ""
if "preVFP" in filename:
  preVFP = "_preVFP"
elif "comb" in filename:
  preVFP = "_comb"

file = ROOT.TFile("root/"+filename)
tau_pt = file.Get("Tau1_pt")
vis_mass = file.Get("vis_mass")
output = './plots/%s_%s%s/vars/'%(channel,year,preVFP)
node = TDirToNode(file)

made_dirs = set()
#selections_DR = ['DR_QCD','DR_QCD_AR','DR_W','DR_W_AR','DR_TT','DR_TT_AR','CR_QCD','CR_QCD_AR','CR_W','CR_W_AR','CR_TT','CR_TT_AR']
selections_DR = ['DR_QCD','DR_QCD_AR','DR_W','DR_W_AR','DR_TT','DR_TT_AR']
#selections_DR = ['AR']
#selections_DR = ['LCR_TT','LCR_TT_AR']
#selections_DR = ['CR_QCD','CR_QCD_AR','CR_W','CR_W_AR','CR_TT','CR_TT_AR']
selections_prong = ['1prong','3prong']

for path, subnode in node.ListNodes(withObjects=True):
    if path!="Tau1_pt":
      continue
    #if path!="vis_mass":
    #  continue
    print(path)
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
     "formats" : ["png","pdf"],
     "ratio_range" : [0.5,1.5],
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
       ('Tau1_pt', ('#tau_{h} p_{T}', 'GeV')),
       ('Tau1_eta', ('#tau_{h} #eta', '')),
       ('Tau1_phi', ('#tau_{h} #phi', '')),
       ('Tau1_mass', ('#tau_{h} mass', 'GeV')),
       ('Tau1_decaymode', ('#tau decaymode', '')),
       ('Tau1_Idvsjet', ('#tau Id vs jet', '')),
       ('Tau1_Idvsmu', ('#tau Id vs #mu', '')),
       ('Tau1_Idvse', ('#tau Id vs e', '')),
       ('Jet1_pt', ('Jet1 p_{T}', 'GeV')),
       ('Jet1_eta', ('Jet1 #eta', '')),
       ('Jet1_phi', ('Jet1 #phi', '')),
       ('Jet1_mass', ('Jet1 mass', 'GeV')),
       ('Jet1_btag', ('Largest btag score', '')),
       ('Jet2_pt', ('Jet2 p_{T}', 'GeV')),
       ('Jet2_btag', ('Second largest btag score', '')),
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
       ('MET', ('MET', 'GeV')),
       #('MET_phi', ('MET #phi', '')),
       ('MET_chs', ('MET CHS', 'GeV')),
       ('nMuons', ('nMuons', '')),
       ('nElectrons', ('nElectrons', '')),
       ('nTaus', ('nTaus', '')),
       ('nJets', ('nJets', '')),
       ('nBjets_l', ('Number of loose b-tagged jets', '')),
       ('nBjets_m', ('Number of medium b-tagged jets', '')),
       ('nBjets_t', ('Number of tight b-tagged jets', '')),
       ('nGenBjets', ('Number of gen b-tagged jets', '')),
       ('LHE_Nb', ('LHE_Nb', '')),
       ('LHE_NpNLO', ('LHE_NpNLO', '')),
       ('DPhi', ('DPhi', '')),
       ('DEta', ('DEta', '')),
       ('DPhiLepMET', ('DPhiLepMET', '')),
       ('DRLepMET', ('DRLepMET', '')),
       ('met_var_qcd', ('met_var_qcd', '')),
       ('met_var_w', ('met_var_w', '')),
       ('wpt', ('wpt', '')),
       ('DRLepB', ('DRLepB', '')),
       ('DEtaLepB', ('DEtaLepB', '')),
       ('DPhiLepB', ('DPhiLepB', '')),
       ('DRTauB', ('DRTauB', '')),
       ('DEtaTauB', ('DEtaTauB', '')),
       ('DPhiTauB', ('DPhiTauB', '')),
       ('DRLepB2', ('DRLepB2', '')),
       ('DEtaLepB2', ('DEtaLepB2', '')),
       ('DPhiLepB2', ('DPhiLepB2', '')),
       ('DRTauB2', ('DRTauB2', '')),
       ('DEtaTauB2', ('DEtaTauB2', '')),
       ('DPhiTauB2', ('DPhiTauB2', '')),
       ('DRBjets', ('DRBjets', '')),
       ('DEta_Bjets', ('DEta_Bjets', '')),
       ('DPhi_Bjets', ('DPhi_Bjets', '')),
       ('DRBjets_lm', ('DRBjets_lm', '')),
       ('DPhiLepB', ('DPhiLepB', '')),
       ('HB_mass', ('HB_mass', 'GeV')),
       ('LepB_mass', ('LepB_mass', 'GeV')),
       ('TauB_mass', ('TauB_mass', 'GeV')),
       ('vistauB_mass', ('vistauB_mass', 'GeV')),
       ('vistauBMET_mass', ('vistauBMET_mass', 'GeV')),
       ('TauBMET_mass', ('TauBMET_mass', 'GeV')),
       ('METB_mass', ('METB_mass', 'GeV')),
       ('Dzeta', ('Dzeta', '')),
       ('mt2', ('mt2', 'GeV')),
       ('wt_ff', ('ff', '')),
       ('wt_ff_ttdr', ('ff TT DR', '')),
       ('wt_ff_old', ('ff old method', '')),
       ('BDTisSignal', ('BDT p_{S}','')),
       ('BDToutput', ('BDT p_{comb}','')),
       ('BDTisTT', ('BDT p_{TT}','')),
       ('BDTisDY', ('BDT p_{DY}','')),
       ('transverse_mass_lepmet', ('m_{T}(#ell,MET)', 'GeV')),
       ('transverse_mass_taumet', ('m_{T}(#tau,MET)','GeV')),
       ('transverse_mass_leptau', ('m_{T}(#ell,#tau)','GeV')),
       ('transverse_mass_total', ('m_{T}^{tot}','GeV')),
       ('DRjets', ('DRjets','')),
       ('DEta_jets', ('DEta_jets','')),
       ('DPhi_jets', ('DPhi_jets','')),
       ('dijet_pt', ('dijet_pt','GeV')),
       ('dijet_eta', ('dijet_eta','')),
       ('dijet_phi', ('dijet_phi','')),
       ('dijet_mass', ('dijet_mass','GeV')),
       ('LepB_pt', ('LepB_pt','GeV')),
       ('TauB_pt', ('TauB_pt','GeV')),
       ('vistauB_pt', ('vistauB_pt','GeV')),
       ('vistauBMET_pt', ('vistauBMET_pt','GeV')),
       ('TauBMET_pt', ('TauBMET_pt','GeV')),
       ('LepBMET_pt', ('LepBMET_pt','GeV')),
       ('METB_pt', ('METB_pt','GeV')),
       ('vistauMET_pt',('vistauMET_pt','GeV')),
       ('HB_pt', ('HB_pt','GeV')),
       ('DRHJ', ('DR(H,j with largest btag)','')),],
      
      "hide_data": [('H_mass', True),('BDToutput', True),('BDTisSignal', True),('BDTisTT', True),('BDTisDY', True)],
      #"logy":[('BDToutput', True),('BDTisSignal', True),('BDTisTT', True),('BDTisDY', True)],
      #"logy_min":[('BDToutput', 30),('BDTisSignal', 30),('BDTisTT', 30),('BDTisDY', 30)],
      #"logy":[('Tau1_pt', True)],
      #"logy_min":[('Tau1_pt', 100)],
    }
    # "ratio_range" :[
    #     ('vis_mass', [0,5])]}


    for setting, vardict in config_by_setting.items():
        for pathkey, val in vardict:
            if fnmatch.fnmatch(path, pathkey):
                plotcfg[setting] = val
                print('Path %s, setting %s, to value %s' % (path, setting, val))
    
    for selection_DR in selections_DR:
      for selection_prong in selections_prong:
        selection = selection_DR+"_"+selection_prong
        MakeStackedPlot(name, target_dir, hists,selection, plotcfg)
    
    #for selection_prong in selections_prong:
    #  selection = "AR_"+selection_prong
    #  MakeStackedPlot(name, target_dir, hists,selection, plotcfg)
  
