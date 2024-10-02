from collections import OrderedDict
import ROOT
import json
import sys,os



processlist =OrderedDict([
    ('data',[['data_BTagCSV'], '#000000']),
    #('data',[['data_single_muon'], '#000000']),
    ('bbH',[['bbHbb'],'#4daf4a']),
    ('bbH_yt2',[['bbHbb_yt2'],'#fed976']),
    ('ggFbb',[['GluGluHToBB'],'#377eb8']),
    ('Single H',[['VBFHToBB','ZH','WminusH','WplusH',],'#ffffb2']),
    ('ZZ',[['ZZ'],'#fed976']),
    ('ttbar',[['ttbar'],'#e41a1c']),
    ('QCD',[['QCD_200','QCD_300','QCD_500','QCD_700','QCD_1000','QCD_1500','QCD_2000',],'#ff7f00']),
    ('Wjets',[['Wjets'],'#fed976']),
])

def Unroll(h):
    '''Unroll a 2D histogram to 1d'''
    import copy
    nbinsx = h.GetNbinsX()
    nbinsy = h.GetNbinsY()
    
    hunroll = ROOT.TH1D(h.GetName().replace(":","_"),h.GetName().replace(":","_"),nbinsx*nbinsy,0,nbinsx*nbinsy)
    bin_count = 0
    for binx in range(nbinsx):
        for biny in range(nbinsy):
            hunroll.SetBinContent(bin_count+1,h.GetBinContent(binx+1,biny+1))
            hunroll.SetBinError(bin_count+1,h.GetBinError(binx+1,biny+1))
            bin_count+=1
        
    return copy.deepcopy(hunroll)


#Plotting funcionality

def getJSON(dir,file,year,ULtag,preVFP):
    path = dir+file+'__%s%s%s.json'%(ULtag,year,preVFP)
    with open(path) as json_file:
        dict = json.load(json_file)
        return dict['sumw']

def getXsec(sample,year,ULtag):
    return xsection[samples['%s%s'%(ULtag,year)]['%s'%sample]]['xsec']


def SetupBox(box_,yy_,fill = ROOT.kBlack):
    box_.SetLineStyle( ROOT.kSolid )
    box_.SetLineWidth( 1 )
    box_.SetLineColor( ROOT.kBlack )
    box_.SetFillColor(fill)


def SetupCanvas(c,logy):
    c.SetFillColor(0)
    c.SetBorderMode(0)
    c.SetFrameFillStyle(0)
    c.SetFrameBorderMode(0)
    c.SetLeftMargin( L/W_ref)
    c.SetRightMargin( R/W_ref)
    c.SetTopMargin( T/H )
    c.SetBottomMargin( B/H )
    c.SetTickx(0)
    c.SetTicky(0)
    if logy: c.SetLogy()


def AddOverflow(h):
    b0 = h.GetBinContent(0)
    e0 = h.GetBinError(0)
    nb = h.GetNbinsX()
    bn = h.GetBinContent(nb + 1)
    en = h.GetBinError(nb + 1)

    h.SetBinContent(0, 0)
    h.SetBinContent(nb+1, 0)
    h.SetBinError(0, 0)
    h.SetBinError(nb+1, 0)

    h.SetBinContent(1, h.GetBinContent(1) + b0)
    h.SetBinError(1, (h.GetBinError(1)**2 + e0**2)**0.5 )

    h.SetBinContent(nb, h.GetBinContent(nb) + bn)
    h.SetBinError(nb, (h.GetBinError(nb)**2 + en**2)**0.5 )

def AddOverflow2D(h):
    nbx = h.GetNbinsX()
    nby = h.GetNbinsY()
    for ix in range(nbx):
        b0x=h.GetBinContent(ix,0)
        e0x=h.GetBinError(ix,0)
        h.SetBinContent(ix,0, 0)
        h.SetBinError(ix,0, 0)
        h.SetBinContent(ix,1, h.GetBinContent(ix,1) + b0x)
        h.SetBinError(ix,1, (h.GetBinError(ix,1)**2 + e0x**2)**0.5 )


        bx = h.GetBinContent(ix,nby+1)
        ex = h.GetBinContent(ix,nby+1)
        h.SetBinContent(ix,nby+1, 0)
        h.SetBinError(ix,nby+1, 0)
        h.SetBinContent(ix,nby, h.GetBinContent(ix,nby) + bx)
        h.SetBinError(ix,nby, (h.GetBinError(ix,nby)**2 + ex**2)**0.5 )

    for iy in range(nby):
        b0y=h.GetBinContent(0,iy+1)
        e0y=h.GetBinError(0,iy+1)
        h.SetBinContent(0,iy+1,0)
        h.SetBinError(0,iy+1,0)
        h.SetBinContent(1,iy+1, h.GetBinContent(1,iy+1) + b0y)
        h.SetBinError(1,iy+1, (h.GetBinError(1,iy+1)**2 + e0y**2)**0.5 )


        by = h.GetBinContent(nbx+1,iy+1)
        ey = h.GetBinContent(nbx+1,iy+1)
        h.SetBinContent(nbx+1,ix+1, 0)
        h.SetBinError(nbx+1,iy+1, 0)
        h.SetBinContent(nbx,iy+1, h.GetBinContent(nbx,iy+1) + by)
        h.SetBinError(nbx,iy+1, (h.GetBinError(nbx,iy+1)**2 + ey**2)**0.5 )


def StackPlot(hstack,fit,plotName,plotData=True,is_log=True):
    import copy
    lumi = 33.5
    herr = None
    c = ROOT.TCanvas(plotName,plotName,5,30,W_ref,H_ref)
    pad1 = ROOT.TPad("pad1", "pad1", 0.0, 0.2 if plotData else 0.0, 1, 1.0)
    pad1.Draw()
    pad1.cd()
    SetupCanvas(pad1, is_log)

    hframe = fit[list(fit.keys())[0]].Clone('frame')
    hframe.Reset()
    
    hframe.SetAxisRange(1, hstack.GetMaximum()*FRMLOG if is_log else hstack.GetMaximum()*FRML,"Y");
    xAxis = hframe.GetXaxis()
    xAxis.SetLabelSize(0.)
    xAxis.SetTitleSize(0.)
    
    yAxis = hframe.GetYaxis()
    yAxis.SetNdivisions(6,5,0)
    yAxis.SetLabelSize(FLS)
    yAxis.SetTitleSize(FTS)
    yAxis.SetTitleOffset(FTO)
    #yAxis.SetMaxDigits(3)
    yAxis.SetTitle("Events / bin")
    hframe.Draw()
    hstack.Draw("histsame")
    c.Update()
    c.Modified()
    # print(hstack.GetNhists())
    # input()
    


    for hprocess in list(fit.keys()):
        if 'data' in hprocess: continue
        if herr == None:
            herr = fit[hprocess].Clone(plotName+'err')
        else:
            herr.Add(fit[hprocess].Clone(plotName+hprocess+'err'))


    herr.SetFillColor( ROOT.kBlack )
    herr.SetMarkerStyle(0)
    herr.SetFillStyle(3354)
    ROOT.gStyle.SetHatchesLineWidth(1)
    ROOT.gStyle.SetHatchesSpacing(1)
    if plotData:
        fit['data'].Draw("esamex0")

    herr.Draw('e2same')


    box = create_paves(lumi, "DataPAS", CMSposX=0.12, CMSposY=0.9,
                             prelimPosX=0.12, prelimPosY=0.85,
                             lumiPosX=0.967, lumiPosY=0.87, alignRight=False)
    box["lumi"].Draw("same")
    box["CMS"].Draw("same")
    box["label"].Draw()



    pad1.cd()
    pad1.Update()
    pad1.RedrawAxis()
    frame = c.GetFrame()
    
    latex = ROOT.TLatex()
    
    legend =  ROOT.TPad("legend_0","legend_0",x0_l + xshiftm,y0_l + yshiftm,x1_l+xshiftp, y1_l + yshiftp )
    
    legend.Draw()
    legend.cd()

    if plotData:
        gr_l =  ROOT.TGraphErrors(1, x_l, y_l, ex_l, ey_l)
        ROOT.gStyle.SetEndErrorSize(0)
        gr_l.SetMarkerSize(0.9)
        gr_l.Draw("0P")

    latex.SetTextFont(42)
    latex.SetTextAngle(0)
    latex.SetTextColor(ROOT.kBlack)
    latex.SetTextSize(0.20)
    latex.SetTextAlign(12)
    yy_ = y_l[0]
    if plotData:
        latex.DrawLatex(xx_+1.*bwx_,yy_,"Data")
    nkey=0

    for key in list(fit.keys()):
        if 'data' in key: continue
        box_ = ROOT.TBox()
        SetupBox(box_,yy_,ROOT.TColor.GetColor(processlist[key][1]))
        if nkey %2 == 0:
            xdist = xgap
        else:
            yy_ -= gap_
            xdist = 0
        box_.DrawBox( xx_-bwx_/2 - xdist, yy_-bwy_/2, xx_+bwx_/2 - xdist, yy_+bwy_/2 )
        box_.SetFillStyle(0)
        box_.DrawBox( xx_-bwx_/2 -xdist, yy_-bwy_/2, xx_+bwx_/2-xdist, yy_+bwy_/2 )
        latex.DrawLatex(xx_+1.*bwx_-xdist,yy_,key)
        nkey+=1


    box_ = ROOT.TBox()
    if nkey %2!=0:
        yy_ -= gap_
    c.Update()



    if plotData:
        c.cd()
        p1r = ROOT.TPad("p4","",0,0,1,0.26)
        
        p1r.SetRightMargin(P2RM)
        p1r.SetLeftMargin(P2LM)
        p1r.SetTopMargin(P2TM)
        p1r.SetBottomMargin(P2BM)
        p1r.SetTicks()
        p1r.Draw()
        p1r.cd()
        
        xmin = float(herr.GetXaxis().GetXmin())
        xmax = float(herr.GetXaxis().GetXmax())
        one = ROOT.TF1("one","1",xmin,xmax)
        one.SetLineColor(1)
        one.SetLineStyle(2)
        one.SetLineWidth(1)
        
        nxbins = herr.GetNbinsX()
        hratio = fit['data'].Clone()
        
        he = herr.Clone()
        he.SetFillColor( 16 )
        he.SetFillStyle( 1001 )
        
        for b in range(nxbins):
            nbkg = herr.GetBinContent(b+1)
            ebkg = herr.GetBinError(b+1)
            
            ndata = fit['data'].GetBinContent(b+1)
            edata = fit['data'].GetBinError(b+1)
            r = ndata / nbkg if nbkg>0 else 0
            rerr = edata / nbkg if nbkg>0 else 0
            
            hratio.SetBinContent(b+1, r)
            hratio.SetBinError(b+1,rerr)
            
            he.SetBinContent(b+1, 1)
            he.SetBinError(b+1, ebkg/nbkg if nbkg>0 else 0 )
            
        hratio.GetYaxis().SetRangeUser(RMIN,RMAX)

        hratio.SetTitle("")
        
        hratio.GetXaxis().SetTitle(plotName)
        hratio.GetXaxis().SetTitleSize(RTSX)
        hratio.GetXaxis().SetTitleOffset(RTOX)
        hratio.GetXaxis().SetLabelSize(RLSX)
        #hratio.GetXaxis().SetTickLength(0.09)
        
        
        #for b in range(hratio.GetNbinsX()):
        #    hratio.GetXaxis().SetBinLabel(b+1, str(int(hratio.GetBinLowEdge(b+1))) )
        
        hratio.GetXaxis().SetLabelOffset(0.02)
        
        hratio.GetYaxis().SetTitleSize(RTSY)
        hratio.GetYaxis().SetLabelSize(RLSY)
        hratio.GetYaxis().SetTitleOffset(RTOY)
        hratio.GetYaxis().SetTitle("      Data/Sim.")
        hratio.GetYaxis().SetDecimals(1)
        hratio.GetYaxis().SetNdivisions(2,2,0) #was 402
        #hratio.GetXaxis().SetNdivisions(6,5,0)
        
        hratio.Draw("pe")
        #    setex2.Draw()
        he.Draw("e2same")
        one.Draw("SAME")
        #turn off horizontal error bars
        #    setex1.Draw()
        #hratio.Draw("PEsame")
        hratio.Draw("PE0X0same")
        hratio.Draw("sameaxis") #redraws the axes
        p1r.Update()
            #raw_input("")


    return copy.deepcopy(c)





def create_paves(lumi, label, CMSposX=0.11, CMSposY=0.9, prelimPosX=0.11, prelimPosY=0.85, lumiPosX=0.95, lumiPosY=0.951, alignRight=False, CMSsize=0.75*0.08, prelimSize=0.75*0.08*0.76, lumiSize=0.6*0.08):

    #pt_lumi = ROOT.TPaveText(xhi-0.25, ylo, xhi, yhi,"brNDC")
    pt_lumi = ROOT.TPaveText(lumiPosX-0.25, lumiPosY, lumiPosX, 1.0,"brNDC")
    pt_lumi.SetFillStyle(0)
    pt_lumi.SetBorderSize(0)
    pt_lumi.SetFillColor(0)
    pt_lumi.SetTextFont(42)
    pt_lumi.SetTextSize(lumiSize)
    pt_lumi.SetTextAlign(31) #left=10, bottom=1, centre=2
    pt_lumi.AddText( "{0:.1f}".format(lumi)+" fb^{-1} (13 TeV)" )

    # if CMSpos == 0: #outside frame
    #     pt_CMS = ROOT.TPaveText(xlo, ylo, xlo+0.1, yhi,"brNDC")
    # elif CMSpos == 1: #left
    #     pt_CMS = ROOT.TPaveText(xlo+0.04, ylo-0.09, xlo+0.14, ylo-0.04,"brNDC")
    # elif CMSpos == 2: #center
    #     pt_CMS = ROOT.TPaveText(xlo+0.4, ylo-0.09, xlo+0.5, ylo-0.04,"brNDC")
    # elif CMSpos == 3: #right
    #     pt_CMS = ROOT.TPaveText(xhi-0.2, ylo-0.09, xhi-0.1, ylo-0.04,"brNDC")
    if alignRight:
        pt_CMS = ROOT.TPaveText(CMSposX-0.1, CMSposY, CMSposX, CMSposY+0.05,"brNDC")
    else:
        pt_CMS = ROOT.TPaveText(CMSposX, CMSposY, CMSposX+0.1, CMSposY+0.05,"brNDC")
    pt_CMS.SetFillStyle(0)
    pt_CMS.SetBorderSize(0)
    pt_CMS.SetFillColor(0)
    pt_CMS.SetTextFont(61)
    pt_CMS.SetTextSize(CMSsize)
    #pt_CMS.SetTextAlign(31 if CMSpos==3 else 11)
    pt_CMS.SetTextAlign(31 if alignRight else 11 )
    pt_CMS.AddText("CMS")

    # if PrelimPos == 0: #outside frame
    #     pt_prelim = ROOT.TPaveText(xlo+0.09, ylo, xlo+0.3, yhi,"brNDC")
    # elif PrelimPos == 1: #left beside CMS
    #     pt_prelim = ROOT.TPaveText(xlo+0.13, ylo-0.09, xlo+0.34, ylo-0.04,"brNDC")
    # elif PrelimPos == 2: #left under CMS
    #     pt_prelim = ROOT.TPaveText(xlo+0.04, ylo-0.15, xlo+0.14, ylo-0.10,"brNDC")
    # elif PrelimPos == 3: #right under CMS
    #     pt_prelim = ROOT.TPaveText(xhi-0.2, ylo-0.15, xhi-0.1, ylo-0.10,"brNDC")
    if alignRight:
        pt_prelim = ROOT.TPaveText(prelimPosX-0.2, prelimPosY, prelimPosX, prelimPosY+0.05,"brNDC")
    else:
        pt_prelim = ROOT.TPaveText(prelimPosX, prelimPosY, prelimPosX+0.2, prelimPosY+0.05,"brNDC")
    pt_prelim.SetFillStyle(0)
    pt_prelim.SetBorderSize(0)
    pt_prelim.SetFillColor(0)
    pt_prelim.SetTextFont(52)
    pt_prelim.SetTextSize(prelimSize)
    #pt_prelim.SetTextAlign(31 if PrelimPos==3 else 11)
    pt_prelim.SetTextAlign(31 if alignRight else 11 )
    if label == "SimPAS":
        pt_prelim.AddText("Simulation Preliminary")
    elif label == "DataPAS":
        pt_prelim.AddText("Preliminary")
    elif label == "Sim":
        pt_prelim.AddText("Simulation")
    elif label == "Data":
        pt_prelim.AddText("")
    elif label == "SimSupp":
        pt_prelim.AddText("Simulation Supplementary")
    elif label == "DataSupp":
        pt_prelim.AddText("Supplementary")
    elif label == "Int":
        pt_prelim.AddText("Internal")

    return {"lumi":pt_lumi, "CMS":pt_CMS, "label":pt_prelim}


def create_hists(var_dict):
    '''Create a dictionary with histograms with the same keys used in var_dict input
    Input:
    dictionary[var_list]:[name,[nbins,min,max]]
    Output:
    dictionary[var_list]:TH1D(name,name,nbins,min,max)
    '''
    histogram_dict = {}
    for var in var_dict:
        histogram_dict[var]=ROOT.TH1D(var_dict[var][0],var_dict[var][0],var_dict[var][1][0],var_dict[var][1][1],var_dict[var][1][2])
    return histogram_dict

class Container():
    def __init__(self,name,root_file,tree_name='Events'):
        self.name=name
        self.file = ROOT.TFile(root_file,'READ')
        self.tree = self.file.Get(tree_name)



    def create_hists(self,var_dict,icolor):
        '''Create a dictionary with histograms with the same keys used in var_dict input
        Input:
        dictionary[var_list]:[name,[nbins,min,max]]
        Output:
        dictionary[var_list]:TH1D(name,name,nbins,min,max)
        '''
        
        self.histograms = {}
        for var in var_dict:
            self.histograms[var]=ROOT.TH1D('{}_{}'.format(self.name,var_dict[var][0]),'{}_{}'.format(self.name,var_dict[var][0]),var_dict[var][1][0],var_dict[var][1][1],var_dict[var][1][2])
            self.histograms[var].GetYaxis().SetTitle("Normalized events / bin")
            self.histograms[var].GetXaxis().SetTitle(var_dict[var][0])
            self.histograms[var].SetMarkerColor(ROOT.TColor.GetColor(histFillColor[icolor]))
            self.histograms[var].SetLineColor(ROOT.TColor.GetColor(histFillColor[icolor]))
            self.histograms[var].SetLineWidth(2)
            
    def normalize_hists(self):
        for hist in self.histograms:
            self.histograms[hist].Scale(1.0/self.histograms[hist].Integral())
            

