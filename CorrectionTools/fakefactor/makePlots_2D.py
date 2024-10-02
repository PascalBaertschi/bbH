import plotting as plot
from analysis import *
import ROOT
import argparse
import json
import os
import fnmatch
from copy import deepcopy
from array import array
from ROOT import gStyle,TCanvas,TH1D, TLatex, TH2D

ROOT.TH1.SetDefaultSumw2(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)
plot.ModTDRStyle()

def processComp(leg,plots,colour,norm=1.):
  return dict([('leg_text',leg),('plot_list',plots),('colour',colour),('norm',norm)])

def MakeStackedPlot(name, outdir, hists,selection, cfg):
    bkgscheme =  [processComp("WJets",["WJetscomb_%s"%selection],881),processComp("DYJets",["DYJetscomb_%s"%selection], 856),processComp("TT",["TT_%s"%selection], 798)]
    #bkgscheme =  [processComp("WJets",["WJets_%s"%selection],881),processComp("W1Jets",["W1Jets_%s"%selection], 856),processComp("W2Jets",["W2Jets_%s"%selection], 798),processComp("W3Jets",["W3Jets_%s"%selection], 602),processComp("W4Jets",["W4Jets_%s"%selection], 801)]
    #bkgscheme =  [processComp("WJets",["WJets_%s"%selection],881),processComp("DYJets",["DYJetscomb_%s"%selection], 856),processComp("TTTo2L2Nu",["TTTo2L2Nu_%s"%selection], 798),processComp("TTToHadronic",["TTToHadronic_%s"%selection], 801),processComp("TTToSemiLeptonic",["TTToSemiLeptonic_%s"%selection], 432)]
    #bkgscheme =  [processComp("jet#rightarrow#tau_{h} fakes",["QCD"],602),processComp("WJets",["WJets"],881),processComp("DYJets",["DYJets","DY1Jets","DY2Jets","DY3Jets","DY4Jets"], 856),processComp("ST",["ST"], 801),processComp("TT",["TT"], 798)]
    #bkgscheme =  [processComp("ttH",["ttH"],432)]
    #bkgscheme = [processComp("TT",["TT"], 798)]
    #bkgscheme = [processComp("DYJets",["DYJets","DY1Jets","DY2Jets","DY3Jets","DY4Jets"], 856)]
    #bkgscheme =  [processComp("ggF",["ggF"],618)]
    #bkgscheme =  [processComp("jjH",["jjH"],634)]
    #bkgscheme = [processComp("ST",["ST"], 801)]
    #bkgscheme = [processComp("VV",["VV"],418)]
    #bkgscheme = [processComp("jet#rightarrow#tau_{h} fakes",["QCD"],602)]
    #signal = [processComp("bbHtautau",["bbHtautau"],2,1)]
    #signal = [processComp("bbH+ggH",["bbHtautau"],2,1)]
    #signal = [processComp("ggH+bb signal",["ggbbH"],2,1)]
    #signal = [processComp("bbH signal",["bbH"],2,1),processComp("ggH+bb signal",["ggbbH"],4,1)]
    #signal = [processComp("bbH",["bbH"],2,1),processComp("bbH PDF4LHC",["bbH_pdf"],4,1)]
    #signal = [processComp("ggH signal",["ggH"],2,1)]
    copyhists = {}
    for hname, h in hists.iteritems():
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

    legend = ROOT.TLegend(*([0.6, 0.75, 0.90, 0.91, '', 'NBNDC']))
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
    h_axes[1].Draw()
    """
    #### comment here for signal only plot ####
    if not cfg['hide_data']:
        r_data = plot.MakeRatioHist(h_data, h_tot, True, False)
    r_tot = plot.MakeRatioHist(h_tot, h_tot, True, False)
    r_tot.Draw('E2SAME')
    if not cfg['hide_data']:
        r_data.Draw('SAME')
    #### end comment here ####
    """
    # Go back and tidy up the axes and frame
    pads[0].cd()
    pads[0].GetFrame().Draw()
    pads[0].RedrawAxis()


    # CMS logo
    plot.DrawCMSLogo(pads[0], "CMS", "Internal", 11, 0.045, 0.05, 1.0, '', 1.0)
    plot.DrawTitle(pads[0], cfg["title_right"], 3)

    latex = ROOT.TLatex()
    plot.Set(latex, NDC=None, TextFont=42, TextSize=0.03)
    latex.DrawLatex(0.20, 0.75, selection)
    latex.DrawLatex(0.20, 0.65, channel)
    # plot.DrawTitle(pads[0], args.title, 1)

    # ... and we're done
    for fmt in cfg["formats"]:
        canv.Print(outdir + '/' + selection + '.%s' %fmt)
  

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
  lumi = 35.9

file = ROOT.TFile("root/"+filename)
tau_pt = file.Get("Tau1_pt")
vis_mass = file.Get("vis_mass")
pt_mass = file.Get("2D")
output = './plots/%s_%s/'%(channel,year)
node = TDirToNode(file)

made_dirs = set()
selections_DR = ['DR_QCD','DR_QCD_AR','DR_W','DR_W_AR','DR_TT','DR_TT_AR']
selections_prong = ['1prong','3prong']

for path, subnode in node.ListNodes(withObjects=True):
    if path!="2D":
      continue
    #if path!="vis_mass":
    #  continue
    print path
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

 
    titleright = "%s %.1f fb^{-1} (13 TeV)"%(year,float(lumi))

    plotcfg = {
     "x_title" : "test",
     "hide_data" : False,
     "logy" : False,
     "formats" : ["pdf"],
     "ratio_range" : [0.5,1.5],
     "title_right" : titleright,
     "do_overlay" : True
    }

    config_by_setting = {
    "x_title": [
       ('Tau1_pt', ('#tau p_{T}', 'GeV')),
       ('vis_mass', ('m_{vis}', 'GeV')),

],
      
      "hide_data": [('H_mass', True),('BDToutput', True),('BDTisSignal', True),('BDTisTT', True),('BDTisDY', True)],
      #"logy":[('BDToutput', True),('BDTisSignal', True),('BDTisTT', True),('BDTisDY', True)],
      #"logy_min":[('BDToutput', 30),('BDTisSignal', 30),('BDTisTT', 30),('BDTisDY', 30)],
    }
    # "ratio_range" :[
    #     ('vis_mass', [0,5])]}


    for setting, vardict in config_by_setting.iteritems():
        for pathkey, val in vardict:
            if fnmatch.fnmatch(path, pathkey):
                plotcfg[setting] = val
                print 'Path %s, setting %s, to value %s' % (path, setting, val)
    for selection_DR in selections_DR:
      for selection_prong in selections_prong:
        selection = selection_DR+"_"+selection_prong
        #MakeStackedPlot(name, target_dir, hists,selection, plotcfg)
        canv = ROOT.TCanvas("%s"%selection,"%s"%selection,600,400)
        #ROOT.gStyle.SetOptStat(0)
        #hist = tau_pt.Get(selection)
        #hist = vis_mass.Get(selection)
        hist = pt_mass.Get(selection)
        #hist.SetMarkerStyle(8)
        #hist.SetLineColor(1)
        #hist.SetTitle("%s"%selection)
        #hist.GetXaxis().SetTitle("Tau pt (GeV)")
        #hist.GetXaxis().SetTitle("visible mass (GeV)")
        hist.GetXaxis().SetTitle("Tau pt (GeV)")
        hist.GetYaxis().SetTitle("visible mass (GeV)")
        hist.Draw("Text")
        hist.SetTitle("%s"%selection)
        latex = TLatex()
        latex.SetNDC()
        latex.SetTextFont(42)
        latex.DrawLatex(0.3, 0.95,"%s %s  %s"%(selection,channel, year))
        canv.SaveAs("%s/%s_%s.pdf"%(output,path,selection))
