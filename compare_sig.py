from ROOT import TH1D, TFile, TCanvas, TLegend, gStyle, TPad
import os


path_2018 = "/pnfs/psi.ch/cms/trivcat/store/user/pbaertsc/bbh/SUSYGluGluToBBHToTauTau_M-125_TuneCP5_13TeV-amcatnlo-pythia8/SUSYGluGluToBBHToTauTau_M-125_TuneCP5_13TeV-amcatnlo-pythia8__2018/201029_154405/0000/"
path_UL2018 ="/pnfs/psi.ch/cms/trivcat/store/user/pbaertsc/bbh/BBHToTauTau/BBHToTauTau__UL2018/210330_100819/0000/"


hist_Hpt_2018 = TH1D("Hpt_2018","LHE Higgs pt",30,0,200)
hist_Hpt_UL2018 = TH1D("Hpt_UL2018","LHE Higgs pt",30,0,200)
#hist_Taupt_2018 = TH1D("Taupt_2018","Tau pt",30,0,100)
#hist_Taupt_UL2018 = TH1D("Taupt_UL2018","Tau pt",30,0,100)
#hist_Mupt_2018 = TH1D("Mupt_2018","Muon pt",30,0,100)
#hist_Mupt_UL2018 = TH1D("Mupt_UL2018","Muon pt",30,0,100)
hist_Taupt_2018 = TH1D("Taupt_2018","Gen Tau pt",30,0,100)
hist_Taupt_UL2018 = TH1D("Taupt_UL2018","Gen Tau pt",30,0,100)
hist_Mupt_2018 = TH1D("Mupt_2018","Gen Muon pt",30,0,100)
hist_Mupt_UL2018 = TH1D("Mupt_UL2018","Gen Muon pt",30,0,100)


#takefiles = ["tree_1.root","tree_2.root","tree_3.root","tree_4.root","tree_5.root","tree_6.root","tree_7.root","tree_8.root","tree_9.root","tree_10.root","tree_11.root","tree_12.root","tree_13.root","tree_14.root","tree_15.root","tree_16.root","tree_17.root","tree_18.root","tree_19.root","tree_20.root"]
takefiles_2018 = ["tree_1.root","tree_2.root","tree_3.root","tree_4.root","tree_5.root"]
takefiles_UL2018 = ["tree_1.root","tree_2.root","tree_3.root","tree_4.root","tree_5.root","tree_6.root","tree_7.root","tree_8.root","tree_9.root","tree_10.root","tree_11.root","tree_12.root","tree_13.root","tree_14.root","tree_15.root","tree_16.root","tree_17.root","tree_18.root","tree_19.root","tree_20.root"]
count_2018 = 0
count_UL2018 = 0

def MakeRatioHist(num, den, num_err, den_err):
    """Make a new ratio TH1 from numerator and denominator TH1s with optional
    error propagation

    Args:
        num (TH1): Numerator histogram  den (TH1): Denominator histogram
        num_err (bool): Propagate the error in the numerator TH1
        den_err (bool): Propagate the error in the denominator TH1

    Returns:
        TH1: A new TH1 containing the ratio
    """
    result = num.Clone()
    if not num_err:
        for i in xrange(1, result.GetNbinsX()+1):
            result.SetBinError(i, 0.)
    den_fix = den.Clone()
    if not den_err:
        for i in xrange(1, den_fix.GetNbinsX()+1):
            den_fix.SetBinError(i, 0.)
    result.Divide(den_fix)
    return result

def TwoPadSplit(split_point, gap_low, gap_high):
    upper = TPad('upper', 'upper', 0., 0., 1., 1.)
    upper.SetBottomMargin(split_point + gap_high)
    upper.SetFillStyle(4000)
    upper.Draw()
    lower = TPad('lower', 'lower', 0., 0., 1., 1.)
    lower.SetTopMargin(1 - split_point + gap_low)
    lower.SetFillStyle(4000)
    lower.Draw()
    upper.cd()
    result = [upper, lower]
    return result

for root, dirs, files in os.walk(path_UL2018,topdown=True):
    [dirs.remove(d) for d in list(dirs) if d=="log"]
    for rootname in files:
        if rootname not in takefiles_UL2018:
            continue
        rootfile = TFile(path_UL2018+"/"+rootname)
        tree = rootfile.Get("Events")
        for i in range(tree.GetEntries()):
            tree.GetEntry(i)
            count_UL2018 +=1
            for igen in range(tree.nGenPart):
                if tree.GenPart_pdgId[igen]==15:
                    if tree.GenPart_pdgId[tree.GenPart_genPartIdxMother[igen]]!=15:
                        hist_Taupt_UL2018.Fill(tree.GenPart_pt[igen])
                elif tree.GenPart_pdgId[igen]==13:
                    hist_Mupt_UL2018.Fill(tree.GenPart_pt[igen])
            #for imu in range(tree.nMuon):
            #    hist_Mupt_UL2018.Fill(tree.Muon_pt[imu])
            #for itau in range(tree.nTau):
            #    hist_Taupt_UL2018.Fill(tree.Tau_pt[itau])
            #for ipar in range(tree.nLHEPart):
            #    if tree.LHEPart_pdgId[ipar]==25:
            #        hist_Hpt_UL2018.Fill(tree.LHEPart_pt[ipar])

for root, dirs, files in os.walk(path_2018,topdown=True):
    [dirs.remove(d) for d in list(dirs) if d=="log"]
    for rootname in files:
        if rootname not in takefiles_2018:
            continue
        rootfile = TFile(path_2018+"/"+rootname)
        tree = rootfile.Get("Events")
        for i in range(tree.GetEntries()):
            tree.GetEntry(i)
            count_2018 +=1
            for igen in range(tree.nGenPart):
                if tree.GenPart_pdgId[igen]==15:
                    try:
                        tree.GenPart_pdgId[tree.GenPart_genPartIdxMother[igen]]
                    except:
                        print "index error"
                        continue
                    if tree.GenPart_pdgId[tree.GenPart_genPartIdxMother[igen]]!=15:
                        hist_Taupt_2018.Fill(tree.GenPart_pt[igen])
                elif tree.GenPart_pdgId[igen]==13:
                    hist_Mupt_2018.Fill(tree.GenPart_pt[igen])
            #for imu in range(tree.nMuon):
            #    hist_Mupt_2018.Fill(tree.Muon_pt[imu])
            #for itau in range(tree.nTau):
            #    hist_Taupt_2018.Fill(tree.Tau_pt[itau])
            #for ipar in range(tree.nLHEPart):
            #    if tree.LHEPart_pdgId[ipar]==25:
            #        hist_Hpt_2018.Fill(tree.LHEPart_pt[ipar])



print "2018 count:",count_2018
print "UL2018 count:",count_UL2018

 
gStyle.SetOptStat(0)
canv1 = TCanvas("Taupt","Taupt",600,400)
pads1 = TwoPadSplit(0.29,0.01,0.01)
hist_Taupt_2018.Scale(1./hist_Taupt_2018.Integral())
hist_Taupt_UL2018.Scale(1./hist_Taupt_UL2018.Integral())
hist_Taupt_2018.GetXaxis().SetLabelSize(0)
hist_Taupt_2018.GetYaxis().SetTitle("Events")
hist_Taupt_2018.SetLineColor(4)
hist_Taupt_UL2018.SetLineColor(2)
hist_Taupt_2018.SetLineWidth(2)
hist_Taupt_UL2018.SetLineWidth(2)
hist_Taupt_2018.Draw("HIST")
hist_Taupt_UL2018.Draw("HIST SAME")
leg = TLegend(0.7, 0.7, 0.85, 0.85)
leg.SetBorderSize(0)
leg.SetFillStyle(0)
leg.SetFillColor(0)
leg.AddEntry(hist_Taupt_2018,"MC 2018","L")
leg.AddEntry(hist_Taupt_UL2018,"MC UL2018","L")
leg.Draw("SAME")
pads1[1].cd()
pads1[1].SetGrid(0,1)
ratio = MakeRatioHist(hist_Taupt_UL2018, hist_Taupt_2018, True, True)
ratio.GetYaxis().SetRangeUser(0.5,1.5)
ratio.GetYaxis().SetTitle("UL2018/2018")
#ratio.GetXaxis().SetTitle("Tau pt (GeV)")
ratio.GetXaxis().SetTitle("Gen Tau pt (GeV)")
ratio.SetLineColor(1)
ratio.SetMarkerStyle(7)
ratio.GetYaxis().SetNdivisions(5)
ratio.Draw('E SAME')
pads1[0].cd()
pads1[0].RedrawAxis()
#canv1.SaveAs("Sigcompare_TauPt.png")
#canv1.SaveAs("Sigcompare_TauPt.pdf")
canv1.SaveAs("Sigcompare_GenTauPt.png")
canv1.SaveAs("Sigcompare_GenTauPt.pdf")
"""
canv2 = TCanvas("Hpt","Hpt",600,400)
pads2 = TwoPadSplit(0.29,0.01,0.01)
hist_Hpt_2018.Scale(1./hist_Hpt_2018.Integral())
hist_Hpt_UL2018.Scale(1./hist_Hpt_UL2018.Integral())
hist_Hpt_2018.GetXaxis().SetLabelSize(0)
hist_Hpt_2018.GetYaxis().SetTitle("Events")
hist_Hpt_2018.SetLineColor(4)
hist_Hpt_UL2018.SetLineColor(2)
hist_Hpt_2018.SetLineWidth(2)
hist_Hpt_UL2018.SetLineWidth(2)
hist_Hpt_2018.Draw("HIST")
hist_Hpt_UL2018.Draw("HIST SAME")
leg = TLegend(0.7, 0.7, 0.85, 0.85)
leg.SetBorderSize(0)
leg.SetFillStyle(0)
leg.SetFillColor(0)
leg.AddEntry(hist_Hpt_2018,"MC 2018","L")
leg.AddEntry(hist_Hpt_UL2018,"MC UL2018","L")
leg.Draw("SAME")
pads2[1].cd()
pads2[1].SetGrid(0,1)
ratio = MakeRatioHist(hist_Hpt_UL2018, hist_Hpt_2018, True, True)
ratio.GetYaxis().SetRangeUser(0.5,1.5)
ratio.GetYaxis().SetTitle("UL2018/2018")
ratio.GetXaxis().SetTitle("Higgs pt (GeV)")
ratio.SetLineColor(1)
ratio.SetMarkerStyle(7)
ratio.GetYaxis().SetNdivisions(5)
ratio.Draw('E SAME')
pads2[0].cd()
pads2[0].RedrawAxis()
canv2.SaveAs("Sigcompare_Hpt.png")
canv2.SaveAs("Sigcompare_Hpt.pdf")
"""

canv3 = TCanvas("Mupt","Mupt",600,400)
pads3 = TwoPadSplit(0.29,0.01,0.01)
hist_Mupt_2018.Scale(1./hist_Mupt_2018.Integral())
hist_Mupt_UL2018.Scale(1./hist_Mupt_UL2018.Integral())
hist_Mupt_2018.GetXaxis().SetLabelSize(0)
hist_Mupt_2018.GetYaxis().SetTitle("Events")
hist_Mupt_2018.SetLineColor(4)
hist_Mupt_UL2018.SetLineColor(2)
hist_Mupt_2018.SetLineWidth(2)
hist_Mupt_UL2018.SetLineWidth(2)
hist_Mupt_2018.Draw("HIST")
hist_Mupt_UL2018.Draw("HIST SAME")
leg = TLegend(0.7, 0.7, 0.85, 0.85)
leg.SetBorderSize(0)
leg.SetFillStyle(0)
leg.SetFillColor(0)
leg.AddEntry(hist_Mupt_2018,"MC 2018","L")
leg.AddEntry(hist_Mupt_UL2018,"MC UL2018","L")
leg.Draw("SAME")
pads3[1].cd()
pads3[1].SetGrid(0,1)
ratio = MakeRatioHist(hist_Mupt_UL2018, hist_Mupt_2018, True, True)
ratio.GetYaxis().SetRangeUser(0.5,1.5)
ratio.GetYaxis().SetTitle("UL2018/2018")
#ratio.GetXaxis().SetTitle("Muon pt (GeV)")
ratio.GetXaxis().SetTitle("Gen Muon pt (GeV)")
ratio.SetLineColor(1)
ratio.SetMarkerStyle(7)
ratio.GetYaxis().SetNdivisions(5)
ratio.Draw('E SAME')
pads3[0].cd()
pads3[0].RedrawAxis()
#canv3.SaveAs("Sigcompare_Mupt.png")
#canv3.SaveAs("Sigcompare_Mupt.pdf")
canv3.SaveAs("Sigcompare_GenMupt.png")
canv3.SaveAs("Sigcompare_GenMupt.pdf")
