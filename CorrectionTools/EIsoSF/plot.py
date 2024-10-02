import ROOT
from ROOT import TFile, TH1D, TCanvas, gStyle, TLegend, TLatex, TGraphErrors
import correctionlib
import os
import numpy as np
from argparse import ArgumentParser
path_root = '/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/EIsoSF/root/'

class EIsoSFs:

    def __init__(self,year,VFPtag):
        self.year = year
        self.VFPtag = VFPtag
        e_data_file = TFile('%sEIsoEff_UL%s%s_data_Fits_dielectron_mass_pt_eta_bins.root'%(path_root,year,VFPtag),'READ')
        self.e_data_hist = e_data_file.Get("dielectron_mass_pt_eta_bins")
        self.e_data_hist.SetDirectory(0)
        e_data_file.Close()
        e_mc_file = TFile('%sEIsoEff_UL%s%s_mc_Fits_dielectron_mass_pt_eta_bins.root'%(path_root,year,VFPtag),'READ')
        self.e_mc_hist = e_mc_file.Get("dielectron_mass_pt_eta_bins")
        self.e_mc_hist.SetDirectory(0)
        e_mc_file.Close()


    def getBinContent(self,hist,pt,eta):
        low_pt = hist.GetXaxis().GetBinCenter(1)
        high_pt = hist.GetXaxis().GetBinCenter(hist.GetNbinsX())
        high_eta = hist.GetYaxis().GetBinCenter(hist.GetNbinsY())
        if pt<low_pt: pt = low_pt
        if pt>high_pt: pt = high_pt
        if abs(eta)>high_eta: eta=high_eta
        return [hist.GetBinContent(hist.GetXaxis().FindBin(pt),hist.GetYaxis().FindBin(abs(eta))),hist.GetBinError(hist.GetXaxis().FindBin(pt),hist.GetYaxis().FindBin(abs(eta)))]

        
    def getEIsoEff(self,pt,eta):
        sl_eff_data = self.getBinContent(self.e_data_hist,pt,eta)
        sl_eff_mc = self.getBinContent(self.e_mc_hist,pt,eta)
        return [sl_eff_data[0],sl_eff_mc[0],sl_eff_data[1],sl_eff_mc[1]]
     


if __name__=="__main__":
    parser = ArgumentParser()
    parser.add_argument('-y', '--year',    dest='year', choices=[2016,2017,2018], type=int, default=2018, action='store')
    parser.add_argument('-p', '--preVFP',  dest='preVFP', action='store_const', const="_preVFP",default="")
    parser.add_argument('-s', '--sys', dest='sys', action='store',default="")
    parser.add_argument('-r', '--turn_on_region', dest='turn_on_region', action='store_true',default=False)
    args = parser.parse_args()
    year = args.year
    preVFP = args.preVFP
    sys= args.sys
    turn_on_region = args.turn_on_region
    ROOT.gROOT.SetBatch(ROOT.kTRUE)
    if year!=2016:
        if turn_on_region:
            lep_pt = [33., 34., 35., 36., 37., 38., 39., 40., 45.]
        else:
            lep_pt = [33., 34., 35., 36., 37., 38., 39., 40., 45., 50. ,75., 100., 200.]
    else:
        if turn_on_region:
            lep_pt = [26., 27., 28., 29., 30., 31., 32., 33., 34., 35., 36., 37., 38., 39., 40., 45.]
        else:
            lep_pt = [26., 27., 28., 29., 30., 31., 32., 33., 34., 35., 36., 37., 38., 39., 40., 45., 50. ,75., 100., 200.]
 
    
    lep_eta = [0., 0.8, 1.444, 1.566, 2., 2.1]
    EIsoSFs = EIsoSFs(year,preVFP)
    if year == 2018:
        lumi = 59.7
    elif year == 2017:
        lumi = 41.5
    elif year == 2016:
        if preVFP=="_preVFP":
            lumi = 19.5
        else:
            lumi = 16.8

    Nbinsx = len(lep_pt)-1
    eta_len = len(lep_eta)-1
    for i in range(eta_len):
        eta_label = "eta%s-%s"%(lep_eta[i],lep_eta[i+1])
        eta_label = eta_label.replace(".",",")
        eta = lep_eta[i]+(lep_eta[i+1]-lep_eta[i])/2.
        data_eff_list = []
        data_eff_error_list = []
        mc_eff_list = []
        mc_eff_error_list = []
        data_pt_list = []
        data_pt_error_list = []
        mc_pt_list = []
        mc_pt_error_list = []
        zeros_list = []
        for j in range(Nbinsx):
            pt = lep_pt[j]+((lep_pt[j+1]-lep_pt[j])/2.)
            pt_error = (lep_pt[j+1]-lep_pt[j])/2.
            effs=EIsoSFs.getEIsoEff(pt,eta)
            eff_data = effs[0]
            eff_mc = effs[1]
            effErr_data = effs[2]
            effErr_mc = effs[3]
            data_eff_list.append(eff_data)
            mc_eff_list.append(eff_mc)
            data_eff_error_list.append(effErr_data)
            mc_eff_error_list.append(effErr_mc)
            data_pt_list.append(pt)
            mc_pt_list.append(pt)
            data_pt_error_list.append(pt_error)
            mc_pt_error_list.append(pt_error)
            zeros_list.append(0.)
        canv = TCanvas("EIsoEff_%s_UL%s%s"%(eta_label,year,preVFP),"EIso %s UL%s%s"%(eta_label,year,preVFP))
        graph_data = TGraphErrors(Nbinsx,np.array(data_pt_list),np.array(data_eff_list),np.array(data_pt_error_list),np.array(data_eff_error_list))
        graph_mc = TGraphErrors(Nbinsx,np.array(mc_pt_list),np.array(mc_eff_list),np.array(mc_pt_error_list),np.array(mc_eff_error_list))
        graph_data.GetXaxis().SetTitle("e p_{T} [GeV]")
        graph_data.GetYaxis().SetTitle("efficiency")
        graph_data.SetMarkerStyle(21)
        graph_mc.SetMarkerStyle(20)
        graph_data.SetMarkerColor(1)
        graph_mc.SetMarkerColor(2)
        graph_data.SetLineColor(1)
        graph_mc.SetLineColor(2)
        graph_data.SetTitle("")
        graph_data.GetYaxis().SetRangeUser(0.,1.1)
        leg = TLegend(0.7,0.4,0.85,0.55)
        leg.AddEntry(graph_data,"data","p")
        leg.AddEntry(graph_mc,"mc","p")
        leg.SetBorderSize(0)
        graph_data.Draw("AP0")
        graph_mc.Draw("P0 SAME")
        leg.Draw("SAME")
        latex = TLatex()
        latex.SetNDC()
        latex.SetTextSize(0.04)
        latex.SetTextColor(1)
        latex.SetTextFont(42)
        latex.DrawLatex(0.55, 0.25, "e iso efficiency")
        latex.DrawLatex(0.55, 0.20, "#eta: [%s-%s]"%(lep_eta[i],lep_eta[i+1]))
        if year==2016:
            if preVFP == "_preVFP": 
                VFPtag = " preVFP"
            else:
                VFPtag = " postVFP"
            latex.DrawLatex(0.54, 0.91, "%s%s %s fb^{-1} (13 TeV)"%(year,VFPtag,lumi))
        else:
            latex.DrawLatex(0.64, 0.91, "%s %s fb^{-1} (13 TeV)"%(year,lumi))
        if sys=="":
            if turn_on_region:
                canv.SaveAs("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/EIsoSF/plots/efficiencies/UL%s%s/turn_on_region/EIsoEff_%s_UL%s%s.pdf"%(year,preVFP,eta_label,year,preVFP))
                canv.SaveAs("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/EIsoSF/plots/efficiencies/UL%s%s/turn_on_region/EIsoEff_%s_UL%s%s.png"%(year,preVFP,eta_label,year,preVFP))
            else:
                canv.SaveAs("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/EIsoSF/plots/efficiencies/UL%s%s/EIsoEff_%s_UL%s%s.pdf"%(year,preVFP,eta_label,year,preVFP))
                canv.SaveAs("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/EIsoSF/plots/efficiencies/UL%s%s/EIsoEff_%s_UL%s%s.png"%(year,preVFP,eta_label,year,preVFP))
             

