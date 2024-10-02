import os, re
from ROOT import TFile, TH2D
import numpy as np
path    = 'CorrectionTools/leptonEfficiencies/ElectronPOG/'


def ensureTFile(filename,option='update'):
  """Open TFile, checking if the file in the given path exists."""
  if not os.path.isfile(filename):
    print '>>> ERROR! ScaleFactorTool.ensureTFile: File in path "%s" does not exist!!'%(filename)
    exit(1)
  file = TFile(filename,option)
  if not file or file.IsZombie():
    print '>>> ERROR! ScaleFactorTool.ensureTFile Could not open file by name "%s"'%(filename)
    exit(1)
  return file

"""
def merge_sf(filename, histname, name, ptvseta=True):
    file     = ensureTFile(filename)
    hist     = file.Get(histname)
    nxbin = hist.GetXaxis().GetNbins()
    nybin = hist.GetYaxis().GetNbins()
    new_histname = "%s_ABSOLUTE" % histname
    if "2016" in filename:
      new_hist     = TH2D(new_histname,"histogram with absolute value",nxbin,0,2.5,nybin,0,500)
    else:
      new_hist     = TH2D(new_histname,"histogram with absolute value",nxbin,0,1000,nybin,0,2.5)
    for pt in np.arange(0,1000,10):
        for eta in np.arange(0,2.5,0.1):
            if ptvseta:
              negative_eta_bin = hist.GetXaxis().FindBin(-eta)
              positive_eta_bin = hist.GetXaxis().FindBin(eta)
              ptbin = hist.GetYaxis().FindBin(pt)
              value_negative_eta = hist.GetBinContent(negative_eta_bin,ptbin)
              value_positive_eta = hist.GetBinContent(positive_eta_bin,ptbin)
              value_absolute_eta = (value_negative_eta+value_positive_eta)/2
              etabin_new = new_hist.GetXaxis().FindBin(eta)
              ptbin_new = new_hist.GetYaxis().FindBin(pt)
              new_hist.SetBinContent(etabin_new,ptbin_new,value_absolute_eta)
            else:
              ptbin = hist.GetXaxis().FindBin(pt)
              negative_eta_bin = hist.GetYaxis().FindBin(-eta)
              positive_eta_bin = hist.GetYaxis().FindBin(eta)
              value_negative_eta = hist.GetBinContent(ptbin,negative_eta_bin)
              value_positive_eta = hist.GetBinContent(ptbin,positive_eta_bin)
              value_absolute_eta = (value_negative_eta+value_positive_eta)/2
              ptbin_new = new_hist.GetXaxis().FindBin(pt)
              etabin_new = new_hist.GetYaxis().FindBin(eta)
              new_hist.SetBinContent(ptbin_new,etabin_new,value_absolute_eta)
    new_hist.Write()
    file.Close
"""
def merge_sf(filename, histname_barrel, histname_endcap):
    file     = ensureTFile(filename)
    hist_barrel     = file.Get(histname_barrel)
    hist_endcap     = file.Get(histname_endcap)
    nxbin = hist_barrel.GetXaxis().GetNbins()
    nybin = hist_barrel.GetYaxis().GetNbins()
    new_histname = "%s" % histname_barrel[:-7]
    if '2017' in filename:
      ptmax = 1000
    else:
      ptmax = 2000
    new_hist     = TH2D(new_histname,"SF for barrel and endcap",nxbin,-2.5,2.5,nybin,0,ptmax)
    for pt in np.arange(0,ptmax,10):
        for eta in np.arange(-2.5,2.5,0.1):
          if abs(eta)>1.5:
            etabin = hist_endcap.GetXaxis().FindBin(eta)
            ptbin = hist_endcap.GetYaxis().FindBin(pt)
            value = hist_endcap.GetBinContent(etabin,ptbin)
          else:
            etabin = hist_barrel.GetXaxis().FindBin(eta)
            ptbin = hist_barrel.GetYaxis().FindBin(pt)
            value = hist_barrel.GetBinContent(etabin,ptbin)
          etabin_new = new_hist.GetXaxis().FindBin(eta)
          ptbin_new = new_hist.GetYaxis().FindBin(pt)
          new_hist.SetBinContent(etabin_new,ptbin_new,value)
    new_hist.Write()
    file.Close

merge_sf(path+"Run2016/Ele115orEleIso27orPho175_SF_2016.root","SF_TH2F_Barrel","SF_TH2F_EndCap")
merge_sf(path+"Run2017/Ele115orEleIso35orPho200_SF_2017.root","SF_TH2F_Barrel","SF_TH2F_EndCap")
merge_sf(path+"Run2018/Ele115orEleIso32orPho200_SF_2018.root","SF_TH2F_Barrel","SF_TH2F_EndCap")

#merge_sf(path+"Run2016/Ele115_passingTight_2016.root",'EGamma_EffData2D','ele_trig_data',ptvseta=True)
#merge_sf(path+"Run2016/Ele115_passingTight_2016.root",'EGamma_EffMC2D','ele_trig_mc',ptvseta=True)
#merge_sf(path+"Run2017/Ele115orEle35_SF_2017.root",'ELE_DATA','ele_trig_data',ptvseta=False)
#merge_sf(path+"Run2017/Ele115orEle35_SF_2017.root",'ELE_MC','ele_trig_mc',ptvseta=False)
#merge_sf(path+"Run2018/Ele115orEle35_SF_2018.root",'ELE_DATA','ele_trig_data',ptvseta=False)
#merge_sf(path+"Run2018/Ele115orEle35_SF_2018.root",'ELE_MC','ele_trig_mc',ptvseta=False)
