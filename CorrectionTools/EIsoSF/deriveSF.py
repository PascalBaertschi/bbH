import ROOT
import argparse
from ROOT import TFile, TH2D, TCanvas, gStyle

parser = argparse.ArgumentParser()
parser.add_argument('-y', '--year',     dest='year', action='store', choices=[2016,2017,2018], type=int, default=2018)
parser.add_argument('-t', '--trigger',  dest='trigger', action='store', type=str)
args = parser.parse_args()


year = args.year
trigger = args.trigger

if trigger=="mu":
    data_filename = "root/mutriggerEff_UL%s_data_Fits_dimuon_mass_pt_eta_bins.root"%year
    dy_filename = "root/mutriggerEff_UL%s_mc_Fits_dimuon_mass_pt_eta_bins.root"%year
    histname = "dimuon_mass_pt_eta_bins"
elif trigger=="e":
    data_filename = "root/etriggerEff_UL%s_data_Fits_dielectron_mass_pt_eta_bins.root"%year
    dy_filename = "root/etriggerEff_UL%s_mc_Fits_dielectron_mass_pt_eta_bins.root"%year
    histname = "dielectron_mass_pt_eta_bins"
elif trigger=="mutau":
    data_filename = "root/mutautriggerEff_UL%s_data_Fits_dimuon_mass_pt_eta_bins.root"%year
    dy_filename = "root/mutautriggerEff_UL%s_mc_Fits_dimuon_mass_pt_eta_bins.root"%year
    histname = "dimuon_mass_pt_eta_bins"
elif trigger=="etau":
    data_filename = "root/etautriggerEff_UL%s_data_Fits_dielectron_mass_pt_eta_bins.root"%year
    dy_filename = "root/etautriggerEff_UL%s_mc_Fits_dielectron_mass_pt_eta_bins.root"%year
    histname = "dielectron_mass_pt_eta_bins"

data_file = TFile(data_filename,'READ')
data_hist = data_file.Get(histname)
data_hist.SetDirectory(0)
data_file.Close()

dy_file = TFile(dy_filename,'READ')
dy_hist = dy_file.Get(histname)
dy_hist.SetDirectory(0)
dy_file.Close()

outfile = TFile("./root/%striggerSF_UL%s.root"%(trigger,year),"RECREATE")
data_hist.Divide(dy_hist)
data_hist.SetName("%striggerSF_UL%s"%(trigger,year))
data_hist.Write()

canv = TCanvas("%striggerSF_UL%s"%(trigger,year),"%striggerSF UL%s"%(trigger,year))
gStyle.SetOptStat(0)
data_hist.SetTitle("%striggerSF UL%s"%(trigger,year))
#if trigger=="e":
#    data_hist.GetXaxis().SetRangeUser(25.,100.)
#    data_hist.GetYaxis().SetRangeUser(0.,2.1)
if "mu" in data_hist.GetTitle():
    data_hist.GetXaxis().SetTitle("#mu p_{T} (GeV)")
    data_hist.GetYaxis().SetTitle("#mu |#eta|")
    data_hist.GetZaxis().SetRangeUser(0.8,1.2)
elif "e" in data_hist.GetTitle():
    data_hist.GetXaxis().SetTitle("e p_{T} (GeV)")
    data_hist.GetYaxis().SetTitle("e |#eta|")
    data_hist.GetZaxis().SetRangeUser(0.8,1.2)
data_hist.GetXaxis().SetTitleOffset(0.9)
data_hist.GetYaxis().SetTitleOffset(0.9)
data_hist.Draw("COLZ")
canv.SaveAs("./plots/%striggerSF_UL%s.pdf"%(trigger,year))
canv.SaveAs("./plots/%striggerSF_UL%s.png"%(trigger,year))
outfile.Close()


