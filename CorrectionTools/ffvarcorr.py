from ROOT import TFile

cut_values = {
  "UL2018":{
    "mutau":{
      "1prong":{
        "qcd":90.,
        "w":115.,
        "tt":115.
      },
      "3prong":{
        "qcd":90.,
        "w":115.,
        "tt":90.
      },
    },
    "etau":{
      "1prong":{
        "qcd":90.,
        "w":115.,
        "tt":115.
      },
      "3prong":{
        "qcd":90.,
        "w":115.,
        "tt":90.
      },
    },
  },
  "UL2017":{
    "mutau":{
      "1prong":{
        "qcd":105.,
        "w":115.,
        "tt":115.
      },
      "3prong":{
        "qcd":105.,
        "w":115.,
        "tt":115.
      },
    },
    "etau":{
      "1prong":{
        "qcd":90.,
        "w":115.,
        "tt":75.
      },
      "3prong":{
        "qcd":90.,
        "w":115.,
        "tt":75.
      },
    },
  },
  "UL2016":{
    "mutau":{
      "1prong":{
        "qcd":90.,
        "w":115.,
        "tt":115.
      },
      "3prong":{
        "qcd":105.,
        "w":115.,
        "tt":90.
      },
    },
    "etau":{
      "1prong":{
        "qcd":90.,
        "w":115.,
        "tt":115.
      },
      "3prong":{
        "qcd":90.,
        "w":115.,
        "tt":115.
      },
    },
  },
}


class ffvarcorrclass:
    def __init__(self,year):
        #mutau
        self.year = "UL%s"%year
        #corrections
        corr_mutau_file = TFile("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/fakefactor/root/ffvarcorrection_mutau_%s.root"%self.year,'READ')
        #hmass correction
        self.hmass_mutau_qcd_1prong = corr_mutau_file.Get("ff_qcd_1prong_H_mass")
        self.hmass_mutau_tt_1prong = corr_mutau_file.Get("ff_tt_1prong_H_mass")
        self.hmass_mutau_qcd_3prong = corr_mutau_file.Get("ff_qcd_3prong_H_mass")
        self.hmass_mutau_tt_3prong = corr_mutau_file.Get("ff_tt_3prong_H_mass")
        self.hmass_mutau_qcd_1prong.SetDirectory(0)
        self.hmass_mutau_tt_1prong.SetDirectory(0)
        self.hmass_mutau_qcd_3prong.SetDirectory(0)
        self.hmass_mutau_tt_3prong.SetDirectory(0)
        #Jet pt correction
        self.jetpt_mutau_qcd_1prong = corr_mutau_file.Get("ff_qcd_1prong_Jet1_pt")
        self.jetpt_mutau_tt_1prong = corr_mutau_file.Get("ff_tt_1prong_Jet1_pt")
        self.jetpt_mutau_qcd_3prong = corr_mutau_file.Get("ff_qcd_3prong_Jet1_pt")
        self.jetpt_mutau_tt_3prong = corr_mutau_file.Get("ff_tt_3prong_Jet1_pt")
        self.jetpt_mutau_qcd_1prong.SetDirectory(0)
        self.jetpt_mutau_tt_1prong.SetDirectory(0)
        self.jetpt_mutau_qcd_3prong.SetDirectory(0)
        self.jetpt_mutau_tt_3prong.SetDirectory(0)
        #collinear mass correction
        self.collinearmass_mutau_qcd_1prong = corr_mutau_file.Get("ff_qcd_1prong_collinear_mass")
        self.collinearmass_mutau_tt_1prong = corr_mutau_file.Get("ff_tt_1prong_collinear_mass")
        self.collinearmass_mutau_qcd_3prong = corr_mutau_file.Get("ff_qcd_3prong_collinear_mass")
        self.collinearmass_mutau_tt_3prong = corr_mutau_file.Get("ff_tt_3prong_collinear_mass")
        self.collinearmass_mutau_qcd_1prong.SetDirectory(0)
        self.collinearmass_mutau_tt_1prong.SetDirectory(0)
        self.collinearmass_mutau_qcd_3prong.SetDirectory(0)
        self.collinearmass_mutau_tt_3prong.SetDirectory(0)
        #TauJ mass correction
        self.taujmass_mutau_qcd_1prong = corr_mutau_file.Get("ff_qcd_1prong_TauJ_mass")
        self.taujmass_mutau_tt_1prong = corr_mutau_file.Get("ff_tt_1prong_TauJ_mass")
        self.taujmass_mutau_qcd_3prong = corr_mutau_file.Get("ff_qcd_3prong_TauJ_mass")
        self.taujmass_mutau_tt_3prong = corr_mutau_file.Get("ff_tt_3prong_TauJ_mass")
        self.taujmass_mutau_qcd_1prong.SetDirectory(0)
        self.taujmass_mutau_tt_1prong.SetDirectory(0)
        self.taujmass_mutau_qcd_3prong.SetDirectory(0)
        self.taujmass_mutau_tt_3prong.SetDirectory(0)
        corr_mutau_file.Close()
        #etau
        corr_etau_file = TFile("/work/pbaertsc/bbh/NanoTreeProducer/CorrectionTools/fakefactor/root/ffvarcorrection_etau_%s.root"%self.year,'READ')
        #H mass correction
        self.hmass_etau_qcd_1prong = corr_etau_file.Get("ff_qcd_1prong_H_mass")
        self.hmass_etau_tt_1prong = corr_etau_file.Get("ff_tt_1prong_H_mass")
        self.hmass_etau_qcd_3prong = corr_etau_file.Get("ff_qcd_3prong_H_mass")
        self.hmass_etau_tt_3prong = corr_etau_file.Get("ff_tt_3prong_H_mass")
        self.hmass_etau_qcd_1prong.SetDirectory(0)
        self.hmass_etau_tt_1prong.SetDirectory(0)
        self.hmass_etau_qcd_3prong.SetDirectory(0)
        self.hmass_etau_tt_3prong.SetDirectory(0)
        #Jet pt correction
        self.jetpt_etau_qcd_1prong = corr_etau_file.Get("ff_qcd_1prong_Jet1_pt")
        self.jetpt_etau_tt_1prong = corr_etau_file.Get("ff_tt_1prong_Jet1_pt")
        self.jetpt_etau_qcd_3prong = corr_etau_file.Get("ff_qcd_3prong_Jet1_pt")
        self.jetpt_etau_tt_3prong = corr_etau_file.Get("ff_tt_3prong_Jet1_pt")
        self.jetpt_etau_qcd_1prong.SetDirectory(0)
        self.jetpt_etau_tt_1prong.SetDirectory(0)
        self.jetpt_etau_qcd_3prong.SetDirectory(0)
        self.jetpt_etau_tt_3prong.SetDirectory(0)
        #collinear mass correction
        self.collinearmass_etau_qcd_1prong = corr_etau_file.Get("ff_qcd_1prong_collinear_mass")
        self.collinearmass_etau_tt_1prong = corr_etau_file.Get("ff_tt_1prong_collinear_mass")
        self.collinearmass_etau_qcd_3prong = corr_etau_file.Get("ff_qcd_3prong_collinear_mass")
        self.collinearmass_etau_tt_3prong = corr_etau_file.Get("ff_tt_3prong_collinear_mass")
        self.collinearmass_etau_qcd_1prong.SetDirectory(0)
        self.collinearmass_etau_tt_1prong.SetDirectory(0)
        self.collinearmass_etau_qcd_3prong.SetDirectory(0)
        self.collinearmass_etau_tt_3prong.SetDirectory(0)
        #TauJ mass correction
        self.taujmass_etau_qcd_1prong = corr_etau_file.Get("ff_qcd_1prong_TauJ_mass")
        self.taujmass_etau_tt_1prong = corr_etau_file.Get("ff_tt_1prong_TauJ_mass")
        self.taujmass_etau_qcd_3prong = corr_etau_file.Get("ff_qcd_3prong_TauJ_mass")
        self.taujmass_etau_tt_3prong = corr_etau_file.Get("ff_tt_3prong_TauJ_mass")
        self.taujmass_etau_qcd_1prong.SetDirectory(0)
        self.taujmass_etau_tt_1prong.SetDirectory(0)
        self.taujmass_etau_qcd_3prong.SetDirectory(0)
        self.taujmass_etau_tt_3prong.SetDirectory(0)
        corr_etau_file.Close()

    def getcorr(self,val,hist):
        first_val = hist.GetBinCenter(1) 
        if val<first_val: val = first_val
        last_val = hist.GetBinCenter(hist.GetNbinsX())
        if val>last_val: val = last_val
        bin = hist.GetXaxis().FindBin(val)
        Content = hist.GetBinContent(bin)
        if Content<0.: Content = 1.
        Error = hist.GetBinError(bin)
        return 1.+((Content-1.)/(1.+Error)**3)

    def ffweightcorr_hmass(self,h_mass,decaymode,channel):
        if decaymode in [0,1,2]:
            prong="1prong"
        elif decaymode in [10,11]:
            prong="3prong"
        else:
            return [1.,1.,1.]
        if channel=="mutau":
            if prong=="1prong":
                hist_corr_qcd = self.hmass_mutau_qcd_1prong
                hist_corr_tt = self.hmass_mutau_tt_1prong
            elif prong=="3prong":
                hist_corr_qcd = self.hmass_mutau_qcd_3prong
                hist_corr_tt = self.hmass_mutau_tt_3prong
        elif channel=="etau":
            if prong=="1prong":
                hist_corr_qcd = self.hmass_etau_qcd_1prong
                hist_corr_tt = self.hmass_etau_tt_1prong
            elif prong=="3prong":
                hist_corr_qcd = self.hmass_etau_qcd_3prong
                hist_corr_tt = self.hmass_etau_tt_3prong
        corr_qcd = self.getcorr(h_mass,hist_corr_qcd)
        corr_tt = self.getcorr(h_mass,hist_corr_tt)
        return [corr_qcd,corr_tt]

    def ffweightcorr_collinearmass(self,collinear_mass,decaymode,channel):
        if decaymode in [0,1,2]:
            prong="1prong"
        elif decaymode in [10,11]:
            prong="3prong"
        else:
            return [1.,1.,1.]
        if channel=="mutau":
            if prong=="1prong":
                hist_corr_qcd = self.collinearmass_mutau_qcd_1prong
                hist_corr_tt = self.collinearmass_mutau_tt_1prong
            elif prong=="3prong":
                hist_corr_qcd = self.collinearmass_mutau_qcd_3prong
                hist_corr_tt = self.collinearmass_mutau_tt_3prong
        elif channel=="etau":
            if prong=="1prong":
                hist_corr_qcd = self.collinearmass_etau_qcd_1prong
                hist_corr_tt = self.collinearmass_etau_tt_1prong
            elif prong=="3prong":
                hist_corr_qcd = self.collinearmass_etau_qcd_3prong
                hist_corr_tt = self.collinearmass_etau_tt_3prong
        corr_qcd = self.getcorr(collinear_mass,hist_corr_qcd)
        corr_tt = self.getcorr(collinear_mass,hist_corr_tt)
        return [corr_qcd,corr_tt]

    def ffweightcorr_taujmass(self,tauj_mass,decaymode,channel):
        if decaymode in [0,1,2]:
            prong="1prong"
        elif decaymode in [10,11]:
            prong="3prong"
        else:
            return [1.,1.,1.]
        if channel=="mutau":
            if prong=="1prong":
                hist_corr_qcd = self.taujmass_mutau_qcd_1prong
                hist_corr_tt = self.taujmass_mutau_tt_1prong
            elif prong=="3prong":
                hist_corr_qcd = self.taujmass_mutau_qcd_3prong
                hist_corr_tt = self.taujmass_mutau_tt_3prong
        elif channel=="etau":
            if prong=="1prong":
                hist_corr_qcd = self.taujmass_etau_qcd_1prong
                hist_corr_tt = self.taujmass_etau_tt_1prong
            elif prong=="3prong":
                hist_corr_qcd = self.taujmass_etau_qcd_3prong
                hist_corr_tt = self.taujmass_etau_tt_3prong
        corr_qcd = self.getcorr(tauj_mass,hist_corr_qcd)
        corr_tt = self.getcorr(tauj_mass,hist_corr_tt)
        return [corr_qcd,corr_tt]


    def ffweightcorr_jetpt(self,jetpt,decaymode,channel):
        if decaymode in [0,1,2]:
            prong="1prong"
        elif decaymode in [10,11]:
            prong="3prong"
        else:
            return 1.
        if channel=="mutau":
            if prong=="1prong":
                hist_corr_qcd = self.jetpt_mutau_qcd_1prong
                hist_corr_tt = self.jetpt_mutau_tt_1prong
            elif prong=="3prong":
                hist_corr_qcd = self.jetpt_mutau_qcd_3prong
                hist_corr_tt = self.jetpt_mutau_tt_3prong
        elif channel=="etau":
            if prong=="1prong":
                hist_corr_qcd = self.jetpt_etau_qcd_1prong
                hist_corr_tt = self.jetpt_etau_tt_1prong
            elif prong=="3prong":
                hist_corr_qcd = self.jetpt_etau_qcd_3prong
                hist_corr_tt = self.jetpt_etau_tt_3prong
        corr_qcd = self.getcorr(jetpt,hist_corr_qcd)
        corr_tt = self.getcorr(jetpt,hist_corr_tt)
        return [corr_qcd,corr_tt]

 


if __name__== "__main__":
    #ffclass(2018).ffweight_ttdr(75,10)
    #for hmass in range(130,250):
    #    print(ffclass(2017).ffweightcorr_hmass(hmass,1,"mutau"))
    for jet1pt in range(10,210):
        print(ffvarcorrclass(2018).ffweightcorr_jetpt(jet1pt,1,"mutau"))
