from ROOT import TFile


class ffclass:
    def __init__(self,year,ULtag,path):
        #mutau
        ff_mutau_file = TFile("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/fakefactor/root/ffcorrection_mutau_%s%s.root"%(ULtag,year),'READ')
        self.ff_mutau_qcd_1prong = ff_mutau_file.Get("ff_qcd_1prong_%s"%path)
        self.ff_mutau_w_1prong = ff_mutau_file.Get("ff_w_1prong_%s"%path)
        self.ff_mutau_tt_1prong = ff_mutau_file.Get("ff_tt_1prong_%s"%path)
        self.ff_mutau_qcd_3prong = ff_mutau_file.Get("ff_qcd_3prong_%"%path)
        self.ff_mutau_w_3prong = ff_mutau_file.Get("ff_w_3prong_%s"%path)
        self.ff_mutau_tt_3prong = ff_mutau_file.Get("ff_tt_3prong_%s"%path)
        self.ff_mutau_qcd_1prong.SetDirectory(0)
        self.ff_mutau_w_1prong.SetDirectory(0)
        self.ff_mutau_tt_1prong.SetDirectory(0)
        self.ff_mutau_qcd_3prong.SetDirectory(0)
        self.ff_mutau_w_3prong.SetDirectory(0)
        self.ff_mutau_tt_3prong.SetDirectory(0)
        ff_mutau_file.Close()
        frac_mutau_1prong_file=TFile("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/fakefactor/root/fractions_mutau_%s%s_1prong.root"%(ULtag,year),'READ')
        self.frac_mutau_1prong_qcd = frac_mutau_1prong_file.Get("Multijet_AR_1prong")
        self.frac_mutau_1prong_w = frac_mutau_1prong_file.Get("WJetscomb_AR_1prong")
        self.frac_mutau_1prong_dy = frac_mutau_1prong_file.Get("DYJetscomb_AR_1prong")
        self.frac_mutau_1prong_tt = frac_mutau_1prong_file.Get("TT_AR_1prong")
        self.frac_mutau_1prong_qcd.SetDirectory(0)
        self.frac_mutau_1prong_w.SetDirectory(0)
        self.frac_mutau_1prong_dy.SetDirectory(0)
        self.frac_mutau_1prong_tt.SetDirectory(0)
        frac_mutau_1prong_file.Close()
        frac_mutau_3prong_file=TFile("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/fakefactor/root/fractions_mutau_%s%s_3prong.root"%(ULtag,year),'READ')
        self.frac_mutau_3prong_qcd = frac_mutau_3prong_file.Get("Multijet_AR_3prong")
        self.frac_mutau_3prong_w = frac_mutau_3prong_file.Get("WJetscomb_AR_3prong")
        self.frac_mutau_3prong_dy = frac_mutau_3prong_file.Get("DYJetscomb_AR_3prong")
        self.frac_mutau_3prong_tt = frac_mutau_3prong_file.Get("TT_AR_3prong")
        self.frac_mutau_3prong_qcd.SetDirectory(0)
        self.frac_mutau_3prong_w.SetDirectory(0)
        self.frac_mutau_3prong_dy.SetDirectory(0)
        self.frac_mutau_3prong_tt.SetDirectory(0)
        frac_mutau_3prong_file.Close()
        #etau
        ff_etau_file = TFile("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/fakefactor/root/ffcorrection_etau_%s%s.root"%(ULtag,year),'READ')
        self.ff_etau_qcd_1prong = ff_etau_file.Get("ff_qcd_1prong_%s"%path)
        self.ff_etau_w_1prong = ff_etau_file.Get("ff_w_1prong_%s"%path)
        self.ff_etau_tt_1prong = ff_etau_file.Get("ff_tt_1prong_%s"%path)
        self.ff_etau_qcd_3prong = ff_etau_file.Get("ff_qcd_3prong_%s"%path)
        self.ff_etau_w_3prong = ff_etau_file.Get("ff_w_3prong_%s"%path)
        self.ff_etau_tt_3prong = ff_etau_file.Get("ff_tt_3prong_%s"%path)
        self.ff_etau_qcd_1prong.SetDirectory(0)
        self.ff_etau_w_1prong.SetDirectory(0)
        self.ff_etau_tt_1prong.SetDirectory(0)
        self.ff_etau_qcd_3prong.SetDirectory(0)
        self.ff_etau_w_3prong.SetDirectory(0)
        self.ff_etau_tt_3prong.SetDirectory(0)
        ff_etau_file.Close()
        frac_etau_1prong_file=TFile("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/fakefactor/root/fractions_etau_%s%s_1prong.root"%(ULtag,year),'READ')
        self.frac_etau_1prong_qcd = frac_etau_1prong_file.Get("Multijet_AR_1prong")
        self.frac_etau_1prong_w = frac_etau_1prong_file.Get("WJetscomb_AR_1prong")
        self.frac_etau_1prong_dy = frac_etau_1prong_file.Get("DYJetscomb_AR_1prong")
        self.frac_etau_1prong_tt = frac_etau_1prong_file.Get("TT_AR_1prong")
        self.frac_etau_1prong_qcd.SetDirectory(0)
        self.frac_etau_1prong_w.SetDirectory(0)
        self.frac_etau_1prong_dy.SetDirectory(0)
        self.frac_etau_1prong_tt.SetDirectory(0)
        frac_etau_1prong_file.Close()
        frac_etau_3prong_file=TFile("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/fakefactor/root/fractions_etau_%s%s_3prong.root"%(ULtag,year),'READ')
        self.frac_etau_3prong_qcd = frac_etau_3prong_file.Get("Multijet_AR_3prong")
        self.frac_etau_3prong_w = frac_etau_3prong_file.Get("WJetscomb_AR_3prong")
        self.frac_etau_3prong_dy = frac_etau_3prong_file.Get("DYJetscomb_AR_3prong")
        self.frac_etau_3prong_tt = frac_etau_3prong_file.Get("TT_AR_3prong")
        self.frac_etau_3prong_qcd.SetDirectory(0)
        self.frac_etau_3prong_w.SetDirectory(0)
        self.frac_etau_3prong_dy.SetDirectory(0)
        self.frac_etau_3prong_tt.SetDirectory(0)
        frac_etau_3prong_file.Close()
      


    def getff(self,pt_initial,hist):
        pt = pt_initial
        ff_initial = hist.GetBinContent(hist.GetXaxis().FindBin(pt))
        while (hist.GetBinContent(hist.GetXaxis().FindBin(pt)) < 0. or hist.GetBinContent(hist.GetXaxis().FindBin(pt)) == 0. or hist.GetBinContent(hist.GetXaxis().FindBin(pt)) > 1.):
            #print "correcting pt"
            pt-=5.
        return hist.GetBinContent(hist.GetXaxis().FindBin(pt))
        

    def ffweight(self,pt,decaymode,channel):
        if channel=="mutau":
            if decaymode in [0,1,2]:
                hist_ff_qcd = self.ff_mutau_qcd_1prong
                hist_ff_w = self.ff_mutau_w_1prong
                hist_ff_tt = self.ff_mutau_tt_1prong
                hist_frac_qcd = self.frac_mutau_1prong_qcd
                hist_frac_w = self.frac_mutau_1prong_w
                hist_frac_dy = self.frac_mutau_1prong_dy
                hist_frac_tt = self.frac_mutau_1prong_tt
            elif decaymode in [10,11]:
                hist_ff_qcd = self.ff_mutau_qcd_3prong
                hist_ff_w = self.ff_mutau_w_3prong
                hist_ff_tt = self.ff_mutau_tt_3prong
                hist_frac_qcd = self.frac_mutau_3prong_qcd
                hist_frac_w = self.frac_mutau_3prong_w
                hist_frac_dy = self.frac_mutau_3prong_dy
                hist_frac_tt = self.frac_mutau_3prong_tt
        elif channel=="etau":
            if decaymode in [0,1,2]:
                hist_ff_qcd = self.ff_etau_qcd_1prong
                hist_ff_w = self.ff_etau_w_1prong
                hist_ff_tt = self.ff_etau_tt_1prong
                hist_frac_qcd = self.frac_etau_1prong_qcd
                hist_frac_w = self.frac_etau_1prong_w
                hist_frac_dy = self.frac_etau_1prong_dy
                hist_frac_tt = self.frac_etau_1prong_tt
            elif decaymode in [10,11]:
                hist_ff_qcd = self.ff_etau_qcd_3prong
                hist_ff_w = self.ff_etau_w_3prong
                hist_ff_tt = self.ff_etau_tt_3prong
                hist_frac_qcd = self.frac_etau_3prong_qcd
                hist_frac_w = self.frac_etau_3prong_w
                hist_frac_dy = self.frac_etau_3prong_dy
                hist_frac_tt = self.frac_etau_3prong_tt
        ff_qcd = self.getff(pt,hist_ff_qcd)
        ff_w = self.getff(pt,hist_ff_w)
        ff_tt = self.getff(pt,hist_ff_tt)
        frac_qcd = hist_frac_qcd.GetBinContent(hist_frac_qcd.GetXaxis().FindBin(pt))
        frac_w = hist_frac_w.GetBinContent(hist_frac_w.GetXaxis().FindBin(pt))
        frac_dy = hist_frac_dy.GetBinContent(hist_frac_dy.GetXaxis().FindBin(pt))
        frac_tt = hist_frac_tt.GetBinContent(hist_frac_tt.GetXaxis().FindBin(pt))
        #print("frac_qcd:",frac_qcd," ff_qcd:",ff_qcd," frac_w:",frac_w," ff_w:",ff_w," frac_tt:",frac_tt," ff_tt:",ff_tt))
        #print("ff_qcd:",ff_qcd, " frac_qcd:",frac_qcd)
        #print("ff_w:",ff_w," frac_w:",frac_w," frac_dy:",frac_dy)
        #print("ff_tt:",ff_tt," frac_tt:",frac_tt)
        #print("total ff:",((frac_qcd*ff_qcd)+((frac_w+frac_dy)*ff_w)+(frac_tt*ff_tt))/(frac_qcd+frac_w+frac_dy+frac_tt))
        return ((frac_qcd*ff_qcd)+((frac_w+frac_dy)*ff_w)+(frac_tt*ff_tt))/(frac_qcd+frac_w+frac_dy+frac_tt)


    def ffweight_sep(self,pt,decaymode,channel):
        if channel=="mutau":
            if decaymode in [0,1,2]:
                hist_ff_qcd = self.ff_mutau_qcd_1prong
                hist_ff_w = self.ff_mutau_w_1prong
                hist_ff_tt = self.ff_mutau_tt_1prong
            elif decaymode in [10,11]:
                hist_ff_qcd = self.ff_mutau_qcd_3prong
                hist_ff_w = self.ff_mutau_w_3prong
                hist_ff_tt = self.ff_mutau_tt_3prong
        elif channel=="etau":
            if decaymode in [0,1,2]:
                hist_ff_qcd = self.ff_etau_qcd_1prong
                hist_ff_w = self.ff_etau_w_1prong
                hist_ff_tt = self.ff_etau_tt_1prong
            elif decaymode in [10,11]:
                hist_ff_qcd = self.ff_etau_qcd_3prong
                hist_ff_w = self.ff_etau_w_3prong
                hist_ff_tt = self.ff_etau_tt_3prong
        ff_qcd = self.getff(pt,hist_ff_qcd)
        ff_w = self.getff(pt,hist_ff_w)
        ff_tt = self.getff(pt,hist_ff_tt)
        return [ff_qcd,ff_w,ff_tt]

    
    def ffweight_ttdr(self,pt,decaymode,channel):
        if channel=="mutau":
            if decaymode in [0,1,2]:
                hist_ff_qcd = self.ff_mutau_qcd_1prong
                hist_ff_w = self.ff_mutau_w_1prong
                hist_ff_tt = self.ff_mutau_tt_1prong
                hist_ttfrac_qcd = self.ttfrac_mutau_1prong_qcd
                hist_ttfrac_w = self.ttfrac_mutau_1prong_w
                hist_ttfrac_dy = self.ttfrac_mutau_1prong_dy
                hist_ttfrac_tt = self.ttfrac_mutau_1prong_tt
            elif decaymode in [10,11]:
                hist_ff_qcd = self.ff_mutau_qcd_3prong
                hist_ff_w = self.ff_mutau_w_3prong
                hist_ff_tt = self.ff_mutau_tt_3prong
                hist_ttfrac_qcd = self.ttfrac_mutau_3prong_qcd
                hist_ttfrac_w = self.ttfrac_mutau_3prong_w
                hist_ttfrac_dy = self.ttfrac_mutau_3prong_dy
                hist_ttfrac_tt = self.ttfrac_mutau_3prong_tt
        elif channel=="etau":
            if decaymode in [0,1,2]:
                hist_ff_qcd = self.ff_etau_qcd_1prong
                hist_ff_w = self.ff_etau_w_1prong
                hist_ff_tt = self.ff_etau_tt_1prong
                hist_ttfrac_qcd = self.ttfrac_etau_1prong_qcd
                hist_ttfrac_w = self.ttfrac_etau_1prong_w
                hist_ttfrac_dy = self.ttfrac_etau_1prong_dy
                hist_ttfrac_tt = self.ttfrac_etau_1prong_tt
            elif decaymode in [10,11]:
                hist_ff_qcd = self.ff_etau_qcd_3prong
                hist_ff_w = self.ff_etau_w_3prong
                hist_ff_tt = self.ff_etau_tt_3prong
                hist_ttfrac_qcd = self.ttfrac_etau_3prong_qcd
                hist_ttfrac_w = self.ttfrac_etau_3prong_w
                hist_ttfrac_dy = self.ttfrac_etau_3prong_dy
                hist_ttfrac_tt = self.ttfrac_etau_3prong_tt
        ff_qcd = self.getff(pt,hist_ff_qcd)
        ff_w = self.getff(pt,hist_ff_w)
        ff_tt = self.getff(pt,hist_ff_tt)
        ttfrac_qcd = hist_ttfrac_qcd.GetBinContent(hist_ttfrac_qcd.GetXaxis().FindBin(pt))
        ttfrac_w = hist_ttfrac_w.GetBinContent(hist_ttfrac_w.GetXaxis().FindBin(pt))
        ttfrac_dy = hist_ttfrac_dy.GetBinContent(hist_ttfrac_dy.GetXaxis().FindBin(pt))
        ttfrac_tt = hist_ttfrac_tt.GetBinContent(hist_ttfrac_tt.GetXaxis().FindBin(pt))
        #print("ttfrac_qcd:",ttfrac_qcd," ff_qcd:",ff_qcd," ttfrac_w:",ttfrac_w," ff_w:",ff_w," ttfrac_tt:",ttfrac_tt," ff_tt:",ff_tt)
        #print("ff_qcd:",ff_qcd, " ttfrac_qcd:",ttfrac_qcd)
        #print("ff_w:",ff_w," ttfrac_w:",ttfrac_w," ttfrac_dy:",ttfrac_dy)
        #print("ff_tt:",ff_tt," ttfrac_tt:",ttfrac_tt)
        #print("total ff:",((ttfrac_qcd*ff_qcd)+((ttfrac_w+ttfrac_dy)*ff_w)+(ttfrac_tt*ff_tt))/(ttfrac_qcd+ttfrac_w+ttfrac_dy+ttfrac_tt))
        return ((ttfrac_qcd*ff_qcd)+((ttfrac_w+ttfrac_dy)*ff_w)+(ttfrac_tt*ff_tt))/(ttfrac_qcd+ttfrac_w+ttfrac_dy+ttfrac_tt)


if __name__== "__main__":
    #ffclass(2018,"UL").ffweight_ttdr(75,10)
    for pt in range(30,130):
        print("ffweight for pt:",pt,"is:",)
        ffclass(2018,"UL").ffweight(pt,1,"etau")
    #    #ffclass(2018,"UL").ffweight_ttdr(pt,10)
